"""
AI Cog for Cereal Bot
Provides /ask (smart chat) and /summarize (message summarisation) commands.
All AI API calls are delegated to the service layer — never called directly.
"""

import discord
from discord import app_commands
from discord.ext import commands
from typing import List, Dict

from services.ai_service import ai_service
from core.logger import get_logger

logger = get_logger(__name__)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

MAX_CONTEXT_MESSAGES: int = 10       # recent messages to include as context for /ask
MAX_SUMMARY_MESSAGES: int = 200      # upper limit for /summarize fetch
DEFAULT_SUMMARY_MESSAGES: int = 50   # default when user doesn't specify a count
DISCORD_MAX_CONTENT: int = 2000       # Discord message content limit


class AI(commands.Cog):
    """AI-powered commands: smart chat and message summarisation."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # ------------------------------------------------------------------
    # /ask — Smart Chat
    # ------------------------------------------------------------------

    @app_commands.command(
        name="ask",
        description="Ask Cereal anything — get a smart, concise answer"
    )
    @app_commands.describe(question="Your question for Cereal")
    async def ask(self, interaction: discord.Interaction, question: str):
        """Smart chat: answer a user's question using AI with conversation context."""

        # Defer immediately — AI calls may take a few seconds
        await interaction.response.defer(thinking=True)

        # Gather recent messages from the channel for conversational context
        context_messages = await self._gather_context(interaction.channel)

        # Call the service layer
        response = await ai_service.ask(
            user_message=question,
            context_messages=context_messages,
        )

        # Send the response — may need to split if it exceeds Discord's limit
        await self._send_response(interaction, question, response)

        logger.info(
            f"/ask used by {interaction.user} in #{interaction.channel.name}: "
            f"{question[:80]}{'…' if len(question) > 80 else ''}"
        )

    # ------------------------------------------------------------------
    # /summarize — Message Summarisation
    # ------------------------------------------------------------------

    @app_commands.command(
        name="summarize",
        description="Summarise recent messages in this channel"
    )
    @app_commands.describe(
        count="Number of recent messages to summarise (default: 50, max: 200)"
    )
    async def summarize(self, interaction: discord.Interaction, count: int = DEFAULT_SUMMARY_MESSAGES):
        """Summarise the last N messages in the current channel."""

        # Clamp count
        count = max(1, min(count, MAX_SUMMARY_MESSAGES))

        await interaction.response.defer(thinking=True)

        # Fetch messages
        messages_text, fetched_count = await self._fetch_channel_messages(
            interaction.channel, limit=count
        )

        if not messages_text.strip():
            await interaction.followup.send(
                "⚠️ No messages found to summarise.", ephemeral=True
            )
            return

        # Call the service layer
        channel_name = getattr(interaction.channel, "name", "dm")
        summary = await ai_service.summarize(
            messages_text=messages_text,
            channel_name=channel_name,
        )

        # Build embed
        embed = discord.Embed(
            title=f"📝 Summary of #{channel_name}",
            description=self._truncate(summary, 4096),
            color=discord.Color.blurple(),
            timestamp=interaction.created_at,
        )
        embed.set_footer(text=f"Summarised {fetched_count} messages • Powered by Groq")
        embed.set_author(
            name=interaction.user.display_name,
            icon_url=interaction.user.display_avatar.url,
        )

        await interaction.followup.send(embed=embed)

        logger.info(
            f"/summarize used by {interaction.user} in #{channel_name}: "
            f"{fetched_count} messages"
        )

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    async def _gather_context(
        self, channel: discord.TextChannel | discord.Thread | discord.DMChannel
    ) -> List[Dict[str, str]]:
        """
        Fetch the last few messages from a channel and format them as
        Groq-compatible message dicts for conversational context.
        """
        context: List[Dict[str, str]] = []

        try:
            messages = [
                msg
                async for msg in channel.history(
                    limit=MAX_CONTEXT_MESSAGES,
                    oldest_first=True,
                )
            ]

            # oldest → newest order
            for msg in messages:
                if msg.author.bot:
                    role = "assistant"
                else:
                    role = "user"

                # Keep content short to save tokens
                content = msg.content[:300] if msg.content else "(attachment/embed)"
                if not content.strip():
                    continue

                context.append({"role": role, "content": content})

        except discord.Forbidden:
            logger.warning(f"Missing read permissions in #{getattr(channel, 'name', 'dm')}")
        except Exception as exc:
            logger.error(f"Error gathering context: {exc}", exc_info=True)

        return context

    async def _fetch_channel_messages(
        self,
        channel: discord.TextChannel | discord.Thread | discord.DMChannel,
        limit: int,
    ) -> tuple[str, int]:
        """
        Fetch recent messages from a channel and return them as a formatted
        string suitable for the summarisation prompt.

        Returns:
            (formatted_text, actual_fetched_count)
        """
        lines: List[str] = []

        try:
            messages = [
                msg
                async for msg in channel.history(
                    limit=limit,
                    oldest_first=True,
                )
            ]

            # oldest → newest
            for msg in messages:
                if msg.author.bot:
                    continue  # skip bot messages in summaries

                timestamp = msg.created_at.strftime("%H:%M")
                author = msg.author.display_name
                content = msg.content[:200] if msg.content else ""

                # Include attachment indicators
                if msg.attachments:
                    content += " [attachment]" if content else "[attachment]"

                if not content.strip():
                    continue

                lines.append(f"[{timestamp}] {author}: {content}")

        except discord.Forbidden:
            logger.warning(f"Missing read permissions in #{getattr(channel, 'name', 'dm')}")
        except Exception as exc:
            logger.error(f"Error fetching messages for summary: {exc}", exc_info=True)

        return "\n".join(lines), len(lines)

    async def _send_response(
        self,
        interaction: discord.Interaction,
        question: str,
        response: str,
    ):
        """Send the AI response as a nicely formatted embed, splitting if needed."""

        # Truncate question for embed title
        title = f"{question[:80]}{'…' if len(question) > 80 else ''}"

        # If the response fits in a single embed, send it directly
        if len(response) <= 4096:
            embed = discord.Embed(
                title=title,
                description=response,
                color=discord.Color.blurple(),
                timestamp=interaction.created_at,
            )
            embed.set_footer(text="Powered by Groq")
            await interaction.followup.send(embed=embed)
            return

        # Otherwise, split into multiple messages
        chunks = self._split_text(response, max_len=4096)

        # First chunk as embed
        embed = discord.Embed(
            title=title,
            description=chunks[0],
            color=discord.Color.blurple(),
            timestamp=interaction.created_at,
        )
        embed.set_footer(text="Powered by Groq")
        await interaction.followup.send(embed=embed)

        # Remaining chunks as follow-ups
        for chunk in chunks[1:]:
            embed = discord.Embed(
                description=chunk,
                color=discord.Color.blurple(),
            )
            await interaction.followup.send(embed=embed)

    @staticmethod
    def _truncate(text: str, max_len: int = 4096) -> str:
        """Truncate text to fit within Discord embed limits."""
        if len(text) <= max_len:
            return text
        return text[: max_len - 3] + "..."

    @staticmethod
    def _split_text(text: str, max_len: int = 4096) -> List[str]:
        """Split text into chunks that fit within Discord embed description limits."""
        if len(text) <= max_len:
            return [text]

        chunks: List[str] = []
        while text:
            # Try to split at a newline to keep formatting clean
            split_at = text.rfind("\n", 0, max_len)
            if split_at == -1 or split_at < max_len // 2:
                split_at = max_len

            chunks.append(text[:split_at])
            text = text[split_at:].lstrip("\n")

        return chunks


async def setup(bot: commands.Bot):
    """Called by discord.py when loading the cog."""
    await bot.add_cog(AI(bot))