import discord
from discord.ext import commands
import os
import asyncio
import time
from aiohttp import web

# Core modules
from core import config, setup_logging, get_logger

# Database imports
from db import init_db, close_db, initialize_repositories

# Setup logging
setup_logging()
logger = get_logger(__name__)

class CerealBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        intents.voice_states = True
        
        super().__init__(
            command_prefix='!',
            intents=intents,
            help_command=None,
        )
        
        self.start_time = time.time()
    
    async def setup_hook(self):
        """Load all cogs and sync slash commands when bot starts"""
        logger.info("Initializing bot...")

        # Initialize database
        logger.info('Initializing database...')
        await init_db()
        logger.info('✓ Database ready')

        # Initialize repositories
        await initialize_repositories()
        logger.info('✓ Repositories ready')

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
                logger.info(f'✓ Loaded {cog}')
            except Exception as e:
                logger.error(f'✗ Failed to load {cog}: {e}')

        # Sync slash commands
        try:
            logger.info('Syncing slash commands...')

            # Get guild ID from environment (optional - for dev/testing)
            guild_id = config.GUILD_ID

            if guild_id and guild_id != 0:
                # DEV MODE: Sync to specific server only (instant)
                # Clear global commands first to avoid duplicates
                self.tree.clear_commands(guild=None)
                
                guild = discord.Object(id=int(guild_id))
                self.tree.copy_global_to(guild=guild)
                synced = await self.tree.sync(guild=guild)
                logger.info(f'✓ [DEV] Synced {len(synced)} commands to server {guild_id} (INSTANT)')
                logger.info('  Global commands cleared - no duplicates!')
            else:
                # PRODUCTION MODE: Sync globally (takes up to 1 hour)
                # Clear any guild-specific commands first
                synced = await self.tree.sync()
                logger.info(f'✓ [PRODUCTION] Synced {len(synced)} commands globally')
                logger.info('  Note: Commands may take up to 1 hour to appear in all servers')
            
        except Exception as e:
            logger.error(f'✗ Failed to sync commands: {e}')
    
    async def on_ready(self):
        """Called when bot is ready"""
        logger.info(f'{self.user} is now online! 🥣')
        logger.info(f'Bot ID: {self.user.id}')
        logger.info(f'Servers: {len(self.guilds)}')
        logger.info(f'Users: {len(self.users)}')
        logger.info('-' * 40)
        
        # Set bot status
        await self.change_presence(
            activity=discord.Game(name=config.BOT_STATUS)
        )
        
        # Start health check server
        self.health_app = web.Application()
        self.health_app.router.add_get('/health', self.health_check)
        self.health_app.router.add_get('/ping', self.ping_check)  # Simple ping endpoint
        self.health_runner = web.AppRunner(self.health_app)
        await self.health_runner.setup()
        site = web.TCPSite(self.health_runner, '0.0.0.0', 8080)
        await site.start()
        logger.info('Health check server started on port 8080 (/health and /ping endpoints)')
        
        # Give health server time to be ready
        await asyncio.sleep(2)
        logger.info('Bot fully ready and health server operational')
    
    async def health_check(self, request):
        """Health check endpoint for monitoring"""
        try:
            # Quick response check
            return web.json_response({
                'status': 'healthy',
                'bot_name': str(self.user) if self.user else 'Unknown',
                'guilds': len(self.guilds) if self.guilds else 0,
                'users': len(self.users) if self.users else 0,
                'latency': round(self.latency * 1000, 2) if self.latency else 0,
                'uptime': str(time.time() - self.start_time) if hasattr(self, 'start_time') else 'unknown',
                'timestamp': time.time()
            })
        except Exception as e:
            logger.error(f"Health check error: {e}")
            return web.json_response({
                'status': 'error',
                'error': str(e),
                'timestamp': time.time()
            }, status=500)
    
    async def ping_check(self, request):
        """Simple ping endpoint for uptime monitoring"""
        return web.json_response({'status': 'pong', 'timestamp': time.time()})
    
    async def close(self):
        """Clean shutdown"""
        # Stop health check server
        if hasattr(self, 'health_runner'):
            await self.health_runner.cleanup()
        
        # Close database connections
        await close_db()
        
        await super().close()
    
    async def on_command_error(self, ctx: commands.Context, error: commands.CommandError):
        """Global error handler"""
        if isinstance(error, commands.CommandNotFound):
            return  # Ignore command not found errors
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send("❌ You don't have permission to use this command!", ephemeral=True)
        elif isinstance(error, commands.BotMissingPermissions):
            await ctx.send("❌ I don't have the required permissions!", ephemeral=True)
        else:
            logger.error(f"Command error: {error}", exc_info=True)

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
    """Main bot startup function"""
    logger.info("Starting Cereal Bot...")

    # Validate configuration
    try:
        from core import load_config
        load_config()
        logger.info("Configuration loaded successfully")
    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        return

    bot = CerealBot()

    # Add sync commands to the bot
    bot.add_command(sync_global)
    bot.add_command(sync_guild)
    bot.add_command(unsync_guild)

    try:
        logger.info("Starting bot connection...")
        await bot.start(config.DISCORD_TOKEN)
    except KeyboardInterrupt:
        logger.info('Shutting down gracefully...')
        await bot.close()
    except Exception as e:
        logger.error(f'Error during bot operation: {e}')
    finally:
        # Clean up database connections
        await close_db()
        logger.info('✓ Cleanup complete')

# Run the bot
if __name__ == '__main__':
    asyncio.run(main())