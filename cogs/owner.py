import discord
from discord import app_commands
from discord.ext import commands


class Owner(commands.Cog):
    """Owner-only private commands. Skipped by /help on purpose."""

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='servers', description='List servers the bot is in (owner only)')
    async def servers(self, interaction: discord.Interaction):
        """List all guilds, visible only to the owner (ephemeral)."""
        if not await self.bot.is_owner(interaction.user):
            return await interaction.response.send_message(
                "❌ Only the bot owner can use this command.", ephemeral=True
            )

        guilds = sorted(self.bot.guilds, key=lambda g: (g.name or '').lower())

        lines = [
            f"**{g.name}** — id `{g.id}` — {g.member_count or '?'} members"
            for g in guilds
        ]
        description = '\n'.join(lines)[:4000] or 'No servers.'

        embed = discord.Embed(
            title=f"Servers ({len(guilds)})",
            description=description,
            color=discord.Color.blue()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)


async def setup(bot):
    await bot.add_cog(Owner(bot))
