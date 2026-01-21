import discord
from discord.ext import commands
import os
import asyncio
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class CerealBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        intents.voice_states = True
        
        super().__init__(
            command_prefix='!',
            intents=intents,
            help_command=commands.DefaultHelpCommand(),
        )
    
    async def setup_hook(self):
        """Load all cogs and sync slash commands when bot starts"""
        # Load cogs
        cogs = [
            'cogs.moderation',
            'cogs.games',
            'cogs.fun',
            'cogs.utility'
        ]
        
        for cog in cogs:
            try:
                await self.load_extension(cog)
                print(f'✓ Loaded {cog}')
            except Exception as e:
                print(f'✗ Failed to load {cog}: {e}')
        
        # Sync slash commands
        try:
            print('Syncing slash commands...')
            
            # Get guild ID from environment (optional - for dev/testing)
            guild_id = os.getenv('GUILD_ID')
            
            if guild_id and guild_id != 'None':
                # DEV MODE: Sync to specific server only (instant)
                # Clear global commands first to avoid duplicates
                self.tree.clear_commands(guild=None)
                
                guild = discord.Object(id=int(guild_id))
                self.tree.copy_global_to(guild=guild)
                synced = await self.tree.sync(guild=guild)
                print(f'✓ [DEV] Synced {len(synced)} commands to server {guild_id} (INSTANT)')
                print('  Global commands cleared - no duplicates!')
            else:
                # PRODUCTION MODE: Sync globally (takes up to 1 hour)
                # Clear any guild-specific commands first
                synced = await self.tree.sync()
                print(f'✓ [PRODUCTION] Synced {len(synced)} commands globally')
                print('  Note: Commands may take up to 1 hour to appear in all servers')
            
        except Exception as e:
            print(f'✗ Failed to sync commands: {e}')
    
    async def on_ready(self):
        print(f'\n{self.user} is now online! 🥣')
        print(f'Bot ID: {self.user.id}')
        print(f'Servers: {len(self.guilds)}')
        print(f'Users: {len(self.users)}')
        print('-' * 40)
        
        # Set bot status
        await self.change_presence(
            activity=discord.Game(name="/help | Cereal Bot 🥣")
        )
    
    async def on_command_error(self, ctx: commands.Context, error: commands.CommandError):
        """Global error handler"""
        if isinstance(error, commands.CommandNotFound):
            return  # Ignore command not found errors
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send("❌ You don't have permission to use this command!", ephemeral=True)
        elif isinstance(error, commands.BotMissingPermissions):
            await ctx.send("❌ I don't have the required permissions!", ephemeral=True)
        else:
            print(f"Error: {error}")

# Owner-only sync commands (for managing slash commands)
@commands.command(name='sync')
@commands.is_owner()
async def sync_global(ctx: commands.Context):
    """Sync slash commands globally (owner only)"""
    try:
        synced = await ctx.bot.tree.sync()
        await ctx.send(f"✅ Synced {len(synced)} commands globally. May take up to 1 hour to appear everywhere.")
    except Exception as e:
        await ctx.send(f"❌ Error: {e}")

@commands.command(name='syncguild')
@commands.is_owner()
async def sync_guild(ctx: commands.Context):
    """Sync slash commands to current server instantly (owner only)"""
    try:
        ctx.bot.tree.copy_global_to(guild=ctx.guild)
        synced = await ctx.bot.tree.sync(guild=ctx.guild)
        await ctx.send(f"✅ Synced {len(synced)} commands to this server (instant)")
    except Exception as e:
        await ctx.send(f"❌ Error: {e}")

@commands.command(name='unsync')
@commands.is_owner()
async def unsync_guild(ctx: commands.Context):
    """Remove slash commands from current server (owner only)"""
    try:
        ctx.bot.tree.clear_commands(guild=ctx.guild)
        await ctx.bot.tree.sync(guild=ctx.guild)
        await ctx.send(f"✅ Removed all commands from this server")
    except Exception as e:
        await ctx.send(f"❌ Error: {e}")

async def main():
    bot = CerealBot()
    
    # Add sync commands to the bot
    bot.add_command(sync_global)
    bot.add_command(sync_guild)
    bot.add_command(unsync_guild)
    
    try:
        await bot.start(os.getenv('DISCORD_TOKEN'))
    except KeyboardInterrupt:
        await bot.close()

if __name__ == '__main__':
    asyncio.run(main())