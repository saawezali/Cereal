"""
Auto-meme poster for Cereal Bot

Server admins enable automatic meme posting in a channel with a configurable
interval (minimum 15 minutes). A single shared scheduler loop posts memes on
schedule with deliberate load thresholds:

- ONE tasks.loop ticked every minute (no per-guild loops)
- In-memory cache of configs: zero DB reads per tick, one DB write per send
- Global cap of MEMES_PER_TICK sends per tick, staggered with jitter
- MEME_RETRIES silent retries per scheduled send, then a single notification
  (subsequent failures stay silent until the next successful send)
- Configs auto-disable after MAX_CONSECUTIVE_FAILURES failed sends
"""

import asyncio
import random
from collections import deque
from datetime import datetime, timedelta

import aiohttp
import discord
from discord import app_commands
from discord.ext import commands, tasks

from core import get_logger
from core.memes import build_meme_embed, fetch_random_meme
from db import automeme_repo

logger = get_logger(__name__)

# -----------------------------
# Load thresholds (conservative by design)
# -----------------------------
MIN_INTERVAL_MINUTES = 15       # minimum per-guild interval
MAX_INTERVAL_MINUTES = 1440     # 24 hours
MEMES_PER_TICK = 15             # global cap on sends per 60s tick
MEME_RETRIES = 3                # silent retries before the single notification
MAX_CONSECUTIVE_FAILURES = 5    # auto-disable after this many failed sends
RECENT_LIMIT = 10               # recent-post dedupe entries per guild

INTERVAL_CHOICES = [15, 30, 60, 120, 180, 360, 720, 1440]

FAILURE_NOTIFY_TEXT = (
    "⚠ Auto-meme couldn't fetch a meme right now (the meme API seems down). "
    "I'll keep retrying quietly — use /automeme status to check on it."
)

PERM_NOTIFY_TEXT = (
    "⚠ Auto-meme can't post here anymore: I need the Send Messages and "
    "Embed Links permissions in this channel. Re-enable me once fixed with "
    "/automeme enable."
)


def is_due(last_sent_at, interval_minutes, now):
    """Pure scheduling predicate: should this config post now?"""
    if last_sent_at is None:
        return True
    return now >= last_sent_at + timedelta(minutes=interval_minutes)


def validate_interval(minutes):
    """True when the interval respects the load thresholds."""
    return MIN_INTERVAL_MINUTES <= minutes <= MAX_INTERVAL_MINUTES


class Automeme(commands.Cog):
    """Admin-configured automatic meme posting"""

    automeme_group = app_commands.Group(
        name='automeme',
        description='Automatic meme posting (admins only)',
        default_permissions=discord.Permissions(manage_channels=True),
        guild_only=True,
    )

    def __init__(self, bot):
        self.bot = bot
        self.session = None   # aiohttp session for meme-api
        self._configs = {}    # guild_id -> AutomemeConfig (enabled only)
        self._recent = {}     # guild_id -> deque of recently posted meme URLs

    async def cog_load(self):
        """Create HTTP session, load the config cache, then start scheduling"""
        self.session = aiohttp.ClientSession()
        await self._reload_cache()
        self.meme_loop.start()

    async def cog_unload(self):
        """Stop the loop and clean up"""
        self.meme_loop.cancel()
        if self.session:
            await self.session.close()
            self.session = None

    async def _reload_cache(self):
        """Load all enabled configs into memory (startup + verification)"""
        try:
            configs = await automeme_repo.get_enabled_all()
        except Exception as e:
            logger.error(f"Automeme: failed to load configs: {e}")
            return
        self._configs = {c.guild_id: c for c in configs}
        if self._configs:
            logger.info(f"Automeme: loaded {len(self._configs)} enabled config(s)")

    # -------------------------
    # Scheduler
    # -------------------------

    @tasks.loop(minutes=1)
    async def meme_loop(self):
        """Single scheduler loop — an idle tick costs nothing when no configs."""
        if self.session is None or not self._configs:
            return

        now = datetime.utcnow()
        due = [
            c for c in list(self._configs.values())
            if is_due(c.last_sent_at, c.interval_minutes, now)
        ]
        if not due:
            return

        # Long-overdue configs post first (crash/restart recovery order)
        due.sort(key=lambda c: c.last_sent_at or datetime.min)

        sends_remaining = MEMES_PER_TICK
        for cfg in due:
            if sends_remaining <= 0:
                logger.info("Automeme: tick budget exhausted — deferring remaining sends")
                break
            if not cfg.enabled:
                continue

            sends_remaining -= 1
            await self._post_for_config(cfg, now)

            # Stagger sends so the meme API never gets bursted
            if sends_remaining > 0:
                await asyncio.sleep(random.uniform(2, 6))

    @meme_loop.before_loop
    async def before_meme_loop(self):
        await self.bot.wait_until_ready()

    async def _post_for_config(self, cfg, now):
        """Attempt one scheduled meme send (with silent retries)."""
        channel = self.bot.get_channel(cfg.channel_id)
        if channel is None:
            # Channel gone (deleted / bot removed) — nothing to notify into,
            # count the failure and let the counter auto-disable if persistent.
            await self._record_failure(cfg, now)
            return

        perms = channel.permissions_for(channel.guild.me)
        if not (perms.send_messages and perms.embed_links):
            await self._record_failure(cfg, now, notify_text=PERM_NOTIFY_TEXT)
            return

        recent = self._recent.setdefault(cfg.guild_id, deque(maxlen=RECENT_LIMIT))
        data = None
        for _ in range(MEME_RETRIES):
            # Each attempt is one capped API call; failures stay silent
            candidate = await fetch_random_meme(self.session, max_attempts=1)
            if candidate is None:
                continue
            if candidate.get('url') and candidate['url'] in recent:
                continue  # avoid reposting the same meme back-to-back
            data = candidate
            break

        if data is None:
            # All retries failed silently — notify once per outage episode
            await self._record_failure(cfg, now, notify_text=FAILURE_NOTIFY_TEXT)
            return

        embed = build_meme_embed(data, footer_prefix='Auto-meme')
        try:
            await channel.send(embed=embed)
        except discord.Forbidden:
            await self._record_failure(cfg, now, notify_text=PERM_NOTIFY_TEXT)
            return
        except asyncio.CancelledError:
            raise
        except discord.HTTPException:
            await self._record_failure(cfg, now)
            return

        # Success: reset failure state, persist, and remember the meme
        url = data.get('url')
        if url:
            recent.append(url)
        cfg.last_sent_at = now
        cfg.consecutive_failures = 0
        cfg.failure_notified = False
        try:
            await automeme_repo.update(
                {'guild_id': cfg.guild_id},
                last_sent_at=now,
                consecutive_failures=0,
                failure_notified=False,
            )
        except Exception as e:
            logger.error(f"Automeme: DB update failed for guild {cfg.guild_id}: {e}")

    async def _record_failure(self, cfg, now, notify_text=None, permanent=False):
        """
        Register a failed send.

        - Sends `notify_text` once per outage episode (failure_notified flag),
          using plain text so it still works when embed permissions are missing.
        - Schedules the next attempt one full interval away (avoids API hammering).
        - Auto-disables the config on permanent failures or when the consecutive
          failure threshold is reached.
        """
        failures = (cfg.consecutive_failures or 0) + 1
        cfg.consecutive_failures = failures

        updates = {'last_sent_at': now, 'consecutive_failures': failures}

        if notify_text and not cfg.failure_notified:
            channel = self.bot.get_channel(cfg.channel_id)
            if channel is not None:
                try:
                    await channel.send(content=notify_text, silent=True)
                except discord.HTTPException:
                    pass
                cfg.failure_notified = True
                updates['failure_notified'] = True

        disable = permanent or failures >= MAX_CONSECUTIVE_FAILURES
        if disable:
            updates['enabled'] = False
            logger.warning(
                f"Automeme auto-disabled for guild {cfg.guild_id} "
                f"(channel {cfg.channel_id}) after {failures} consecutive failure(s)"
            )

        try:
            await automeme_repo.update({'guild_id': cfg.guild_id}, **updates)
        except Exception as e:
            logger.error(f"Automeme: DB update failed for guild {cfg.guild_id}: {e}")

        cfg.last_sent_at = now
        if disable:
            self._configs.pop(cfg.guild_id, None)
            self._recent.pop(cfg.guild_id, None)

    # -------------------------
    # Admin commands
    # -------------------------

    @automeme_group.command(name='enable', description='Post memes automatically in a channel')
    @app_commands.describe(
        channel='Channel to post memes in',
        interval='How often to post (minutes, minimum 15)'
    )
    @app_commands.choices(
        interval=[app_commands.Choice(name=f'{m} minutes', value=m) for m in INTERVAL_CHOICES]
    )
    @app_commands.default_permissions(manage_channels=True)
    async def enable_automeme(
        self,
        interaction: discord.Interaction,
        channel: discord.TextChannel,
        interval: int = 15
    ):
        """Enable or update automatic meme posting"""
        if not interaction.user.guild_permissions.manage_channels:
            return await interaction.response.send_message(
                "✗ You need Manage Channels permission!", ephemeral=True
            )

        if not validate_interval(interval):
            return await interaction.response.send_message(
                f"✗ Interval must be between {MIN_INTERVAL_MINUTES} and "
                f"{MAX_INTERVAL_MINUTES} minutes!", ephemeral=True
            )

        perms = channel.permissions_for(interaction.guild.me)
        if not (perms.send_messages and perms.embed_links):
            return await interaction.response.send_message(
                f"✗ I need Send Messages + Embed Links permission in {channel.mention}!",
                ephemeral=True
            )

        try:
            await automeme_repo.upsert_config(
                guild_id=interaction.guild.id,
                channel_id=channel.id,
                interval_minutes=interval,
            )
        except Exception:
            return await interaction.response.send_message(
                "✗ Couldn't save the configuration. Try again later.",
                ephemeral=True
            )

        cfg = await automeme_repo.get_config(interaction.guild.id)
        self._configs[interaction.guild.id] = cfg
        self._recent.pop(interaction.guild.id, None)

        interval = cfg.interval_minutes
        next_post = datetime.utcnow() + timedelta(minutes=interval)
        embed = discord.Embed(
            title="Auto-meme Enabled",
            description=f"Posting a meme in {channel.mention} every **{interval}** minutes.",
            color=discord.Color.green()
        )
        embed.add_field(name="Next post", value=discord.utils.format_dt(next_post, style='R'), inline=False)
        await interaction.response.send_message(embed=embed)

    @automeme_group.command(name='disable', description='Stop automatic meme posting')
    @app_commands.default_permissions(manage_channels=True)
    async def disable_automeme(self, interaction: discord.Interaction):
        """Disable automatic meme posting"""
        if not interaction.user.guild_permissions.manage_channels:
            return await interaction.response.send_message(
                "✗ You need Manage Channels permission!", ephemeral=True
            )

        deleted = await automeme_repo.delete(guild_id=interaction.guild.id)
        self._configs.pop(interaction.guild.id, None)
        self._recent.pop(interaction.guild.id, None)

        if deleted:
            await interaction.response.send_message("✔ Auto-meme disabled.")
        else:
            await interaction.response.send_message(
                "Auto-meme isn't configured in this server.", ephemeral=True
            )

    @automeme_group.command(name='status', description='Show the auto-meme configuration')
    @app_commands.default_permissions(manage_channels=True)
    async def status_automeme(self, interaction: discord.Interaction):
        """Show the current auto-meme configuration"""
        if not interaction.user.guild_permissions.manage_channels:
            return await interaction.response.send_message(
                "✗ You need Manage Channels permission!", ephemeral=True
            )

        cfg = self._configs.get(interaction.guild.id)
        if cfg is None:
            row = await automeme_repo.get_config(interaction.guild.id)
            if row and not row.enabled:
                return await interaction.response.send_message(
                    "Auto-meme is configured but currently disabled (it failed too many "
                    "times). Re-enable it with /automeme enable.",
                    ephemeral=True
                )
            return await interaction.response.send_message(
                "Auto-meme isn't set up in this server. Use /automeme enable to turn it on.",
                ephemeral=True
            )

        if cfg.last_sent_at:
            next_post = cfg.last_sent_at + timedelta(minutes=cfg.interval_minutes)
        else:
            next_post = datetime.utcnow()

        embed = discord.Embed(title="Auto-meme Status", color=discord.Color.blue())
        embed.add_field(name="Channel", value=f"<#{cfg.channel_id}>", inline=False)
        embed.add_field(name="Interval", value=f"{cfg.interval_minutes} minutes", inline=True)
        embed.add_field(
            name="Next post",
            value=discord.utils.format_dt(next_post, style='R'),
            inline=False
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)


async def setup(bot):
    await bot.add_cog(Automeme(bot))
