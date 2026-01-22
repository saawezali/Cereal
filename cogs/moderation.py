import discord
from discord import app_commands
from discord.ext import commands
from datetime import timedelta
import asyncio

class Moderation(commands.Cog):
    """Moderation commands for server management"""
    
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name='kick', description='Kick a member from the server')
    @app_commands.describe(member='The member to kick', reason='Reason for kicking')
    @commands.has_permissions(kick_members=True)
    @commands.bot_has_permissions(kick_members=True)
    async def kick(self, interaction: discord.Interaction, member: discord.Member, reason: str = None):
        """Kick a member from the server"""
        if member.top_role >= interaction.user.top_role:
            return await interaction.response.send_message("❌ You cannot kick someone with equal or higher role!", ephemeral=True)
        
        if member.id == interaction.guild.owner_id:
            return await interaction.response.send_message("❌ Cannot kick the server owner!", ephemeral=True)
        
        if member.id == interaction.client.user.id:
            return await interaction.response.send_message("❌ I cannot kick myself!", ephemeral=True)
        
        try:
            await member.kick(reason=reason)
            
            embed = discord.Embed(
                title="👢 Member Kicked",
                description=f"{member.mention} has been kicked",
                color=discord.Color.orange()
            )
            embed.add_field(name="Reason", value=reason or "No reason provided")
            embed.add_field(name="Moderator", value=interaction.user.mention)
            await interaction.response.send_message(embed=embed)
        except discord.Forbidden:
            return await interaction.response.send_message("❌ I don't have permission to kick this member!", ephemeral=True)
    
    @app_commands.command(name='ban', description='Ban a member from the server')
    @app_commands.describe(member='The member to ban', reason='Reason for banning')
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def ban(self, interaction: discord.Interaction, member: discord.Member, reason: str = None):
        """Ban a member from the server"""
        if member.top_role >= interaction.user.top_role:
            return await interaction.response.send_message("❌ You cannot ban someone with equal or higher role!", ephemeral=True)
        
        if member.id == interaction.guild.owner_id:
            return await interaction.response.send_message("❌ Cannot ban the server owner!", ephemeral=True)
        
        if member.id == interaction.client.user.id:
            return await interaction.response.send_message("❌ I cannot ban myself!", ephemeral=True)
        
        try:
            await member.ban(reason=reason)
            
            embed = discord.Embed(
                title="🔨 Member Banned",
                description=f"{member.mention} has been banned",
                color=discord.Color.red()
            )
            embed.add_field(name="Reason", value=reason or "No reason provided")
            embed.add_field(name="Moderator", value=interaction.user.mention)
            await interaction.response.send_message(embed=embed)
        except discord.Forbidden:
            return await interaction.response.send_message("❌ I don't have permission to ban this member!", ephemeral=True)
    
    @app_commands.command(name='unban', description='Unban a user by their ID')
    @app_commands.describe(user_id='The ID of the user to unban')
    @commands.has_permissions(ban_members=True)
    async def unban(self, interaction: discord.Interaction, user_id: str):
        """Unban a member by their ID"""
        try:
            user_id_int = int(user_id)
            user = await self.bot.fetch_user(user_id_int)
            await interaction.guild.unban(user)
            await interaction.response.send_message(f"✅ {user.mention} has been unbanned")
        except ValueError:
            await interaction.response.send_message("❌ Invalid user ID!", ephemeral=True)
        except discord.NotFound:
            await interaction.response.send_message("❌ User not found or not banned", ephemeral=True)
    
    @app_commands.command(name='mute', description='Timeout a member')
    @app_commands.describe(
        member='The member to timeout',
        duration='Duration in minutes',
        reason='Reason for timeout'
    )
    @commands.has_permissions(moderate_members=True)
    @commands.bot_has_permissions(moderate_members=True)
    async def mute(self, interaction: discord.Interaction, member: discord.Member, duration: int = 60, reason: str = None):
        """Timeout a member (duration in minutes, max 40320)"""
        if member.top_role >= interaction.user.top_role:
            return await interaction.response.send_message("❌ You cannot mute someone with equal or higher role!", ephemeral=True)
        
        if member.id == interaction.guild.owner_id:
            return await interaction.response.send_message("❌ Cannot mute the server owner!", ephemeral=True)
        
        if member.id == interaction.client.user.id:
            return await interaction.response.send_message("❌ I cannot mute myself!", ephemeral=True)
        
        if duration > 40320:
            return await interaction.response.send_message("❌ Duration cannot exceed 40320 minutes (28 days)!", ephemeral=True)
        
        try:
            await member.timeout(timedelta(minutes=duration), reason=reason)
            
            embed = discord.Embed(
                title="🔇 Member Muted",
                description=f"{member.mention} has been muted for {duration} minutes",
                color=discord.Color.blue()
            )
            embed.add_field(name="Reason", value=reason or "No reason provided")
            embed.add_field(name="Moderator", value=interaction.user.mention)
            await interaction.response.send_message(embed=embed)
        except Exception as e:
            await interaction.response.send_message(f"❌ Error: {e}", ephemeral=True)
    
    @app_commands.command(name='unmute', description='Remove timeout from a member')
    @app_commands.describe(member='The member to unmute')
    @commands.has_permissions(moderate_members=True)
    @commands.bot_has_permissions(moderate_members=True)
    async def unmute(self, interaction: discord.Interaction, member: discord.Member):
        """Remove timeout from a member"""
        try:
            await member.timeout(None)
            await interaction.response.send_message(f"✅ {member.mention} has been unmuted")
        except discord.Forbidden:
            await interaction.response.send_message("❌ I don't have permission to unmute this member!", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"❌ Error: {e}", ephemeral=True)
    
    @app_commands.command(name='clear', description='Delete messages from the channel')
    @app_commands.describe(amount='Number of messages to delete (max 100)')
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True)
    async def clear(self, interaction: discord.Interaction, amount: int = 10):
        """Delete messages from the channel (max 100)"""
        if amount > 100:
            return await interaction.response.send_message("❌ Cannot delete more than 100 messages at once", ephemeral=True)
        
        if amount < 1:
            return await interaction.response.send_message("❌ Amount must be at least 1", ephemeral=True)
        
        try:
            await interaction.response.defer(ephemeral=True)
            
            deleted = await interaction.channel.purge(limit=amount)
            
            await interaction.followup.send(f"🗑️ Deleted {len(deleted)} messages", ephemeral=True)
        except discord.Forbidden:
            await interaction.followup.send("❌ I don't have permission to delete messages!", ephemeral=True)
        except discord.HTTPException:
            await interaction.followup.send("❌ Failed to delete messages. They might be too old (14+ days).", ephemeral=True)
    
    @app_commands.command(name='warn', description='Warn a member')
    @app_commands.describe(member='The member to warn', reason='Reason for warning')
    @commands.has_permissions(moderate_members=True)
    async def warn(self, interaction: discord.Interaction, member: discord.Member, reason: str = None):
        """Warn a member (stores in memory for now)"""
        embed = discord.Embed(
            title="⚠️ Member Warned",
            description=f"{member.mention} has been warned",
            color=discord.Color.yellow()
        )
        embed.add_field(name="Reason", value=reason or "No reason provided")
        embed.add_field(name="Moderator", value=interaction.user.mention)
        await interaction.response.send_message(embed=embed)
        
        # Try to DM the user
        try:
            await member.send(f"⚠️ You have been warned in {interaction.guild.name}\n**Reason:** {reason or 'No reason provided'}")
        except:
            pass
    
    @app_commands.command(name='slowmode', description='Set slowmode for the current channel')
    @app_commands.describe(seconds='Slowmode delay in seconds (0 to disable, max 21600)')
    @commands.has_permissions(manage_channels=True)
    @commands.bot_has_permissions(manage_channels=True)
    async def slowmode(self, interaction: discord.Interaction, seconds: int = 0):
        """Set slowmode for the current channel"""
        if seconds > 21600:
            return await interaction.response.send_message("❌ Slowmode cannot exceed 6 hours (21600 seconds)", ephemeral=True)
        
        if seconds < 0:
            return await interaction.response.send_message("❌ Slowmode cannot be negative", ephemeral=True)
        
        try:
            await interaction.channel.edit(slowmode_delay=seconds)
            if seconds == 0:
                await interaction.response.send_message("✅ Slowmode disabled")
            else:
                await interaction.response.send_message(f"✅ Slowmode set to {seconds} seconds")
        except discord.Forbidden:
            await interaction.response.send_message("❌ I don't have permission to manage this channel!", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Moderation(bot))