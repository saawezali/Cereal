import discord
from discord.ext import commands


class Owner(commands.Cog):
    """Owner-only private text commands. Never synced, never in /help."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='servers')
    @commands.is_owner()
    async def servers(self, ctx: commands.Context):
        """List all guilds. Owner only — use in a private channel."""
        guilds = sorted(self.bot.guilds, key=lambda g: (g.name or '').lower())

        if not guilds:
            return await ctx.send("No servers.")

        # Chunk lines so every message stays under Discord's 2000-char limit
        pages = []
        current = f"Servers ({len(guilds)}):\n"
        for g in guilds:
            line = f"• {g.name} — id `{g.id}` — {g.member_count or '?'} members\n"
            if len(current) + len(line) > 1900:
                pages.append(current)
                current = ""
            current += line
        pages.append(current)

        for page in pages:
            await ctx.send(page)

    @servers.error
    async def servers_error(self, ctx: commands.Context, error: commands.CommandError):
        """Non-owners get a brief denial instead of silence."""
        if isinstance(error, commands.NotOwner):
            await ctx.send("❌ Only the bot owner can use this command.", delete_after=10)
        else:
            raise error


async def setup(bot):
    await bot.add_cog(Owner(bot))
