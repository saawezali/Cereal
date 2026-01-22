"""
Configuration management for Cereal Bot
Handles environment variables and settings
"""

import os
from typing import Optional, Union, List
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Configuration manager for the bot"""

    # Discord Configuration
    DISCORD_TOKEN: str = os.getenv('DISCORD_TOKEN', '')
    GUILD_ID: Optional[int] = int(os.getenv('GUILD_ID', 0)) if os.getenv('GUILD_ID') and os.getenv('GUILD_ID') != 'None' else None

    # Database Configuration
    DATABASE_URL: str = os.getenv('DATABASE_URL', 'sqlite:///cereal.db')
    DATABASE_TYPE: str = os.getenv('DATABASE_TYPE', 'sqlite')  # sqlite or postgresql

    # Bot Configuration
    BOT_PREFIX: str = os.getenv('BOT_PREFIX', '!')
    BOT_STATUS: str = os.getenv('BOT_STATUS', '/help | Cereal Bot 🥣')
    BOT_ACTIVITY_TYPE: str = os.getenv('BOT_ACTIVITY_TYPE', 'playing')  # playing, watching, listening

    # Logging Configuration
    LOG_LEVEL: str = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE: str = os.getenv('LOG_FILE', 'logs/cereal.log')
    LOG_MAX_SIZE: int = int(os.getenv('LOG_MAX_SIZE', '10485760'))  # 10MB
    LOG_BACKUP_COUNT: int = int(os.getenv('LOG_BACKUP_COUNT', '5'))

    # API Keys (add as needed)
    WEATHER_API_KEY: Optional[str] = os.getenv('WEATHER_API_KEY')
    JOKE_API_KEY: Optional[str] = os.getenv('JOKE_API_KEY')

    # Feature Flags
    ENABLE_XP_SYSTEM: bool = os.getenv('ENABLE_XP_SYSTEM', 'true').lower() == 'true'
    ENABLE_ECONOMY: bool = os.getenv('ENABLE_ECONOMY', 'false').lower() == 'true'
    ENABLE_MUSIC: bool = os.getenv('ENABLE_MUSIC', 'false').lower() == 'true'
    ENABLE_AUTO_MOD: bool = os.getenv('ENABLE_AUTO_MOD', 'false').lower() == 'true'

    # Moderation Settings
    WARN_LIMIT: int = int(os.getenv('WARN_LIMIT', '3'))
    MUTE_DURATION_MINUTES: int = int(os.getenv('MUTE_DURATION_MINUTES', '60'))
    BAN_DURATION_DAYS: int = int(os.getenv('BAN_DURATION_DAYS', '7'))

    # XP System Settings
    XP_PER_MESSAGE: int = int(os.getenv('XP_PER_MESSAGE', '1'))
    XP_COOLDOWN_SECONDS: int = int(os.getenv('XP_COOLDOWN_SECONDS', '60'))
    LEVEL_XP_BASE: int = int(os.getenv('LEVEL_XP_BASE', '100'))
    LEVEL_XP_MULTIPLIER: float = float(os.getenv('LEVEL_XP_MULTIPLIER', '1.5'))

    # Economy Settings
    DAILY_COINS: int = int(os.getenv('DAILY_COINS', '100'))
    WEEKLY_COINS: int = int(os.getenv('WEEKLY_COINS', '500'))

    # Performance Settings
    COMMAND_COOLDOWN_GLOBAL: float = float(os.getenv('COMMAND_COOLDOWN_GLOBAL', '1.0'))
    CACHE_TTL_SECONDS: int = int(os.getenv('CACHE_TTL_SECONDS', '300'))  # 5 minutes

    # Development Settings
    DEBUG_MODE: bool = os.getenv('DEBUG_MODE', 'false').lower() == 'true'
    DEV_GUILD_ID: Optional[int] = int(os.getenv('DEV_GUILD_ID', 0)) if os.getenv('DEV_GUILD_ID') else None

    @classmethod
    def validate_config(cls) -> List[str]:
        """
        Validate configuration and return list of missing required settings

        Returns:
            List of missing configuration keys
        """
        missing = []

        if not cls.DISCORD_TOKEN:
            missing.append('DISCORD_TOKEN')

        # Check database URL format
        if cls.DATABASE_TYPE == 'postgresql' and not cls.DATABASE_URL.startswith('postgresql'):
            missing.append('DATABASE_URL (must be PostgreSQL URL for DATABASE_TYPE=postgresql)')

        # Check for required API keys when features are enabled
        if cls.ENABLE_MUSIC and not os.getenv('LAVALINK_HOST'):
            missing.append('LAVALINK_HOST (required when ENABLE_MUSIC=true)')

        return missing

    @classmethod
    def get_database_url(cls) -> str:
        """
        Get the appropriate database URL based on configuration

        Returns:
            Database URL string
        """
        if cls.DATABASE_TYPE == 'sqlite':
            # Ensure SQLite path is absolute or relative to project root
            if cls.DATABASE_URL.startswith('sqlite:///'):
                db_path = cls.DATABASE_URL.replace('sqlite:///', '')
                if not os.path.isabs(db_path):
                    # Make relative to project root
                    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                    db_path = os.path.join(project_root, db_path)
                return f'sqlite+aiosqlite:///{db_path}'
            else:
                return cls.DATABASE_URL
        else:
            return cls.DATABASE_URL

    @classmethod
    def is_development(cls) -> bool:
        """
        Check if running in development mode

        Returns:
            True if in development mode
        """
        return cls.DEBUG_MODE or cls.DEV_GUILD_ID is not None

    @classmethod
    def get_log_level(cls) -> str:
        """
        Get appropriate log level

        Returns:
            Log level string
        """
        if cls.DEBUG_MODE:
            return 'DEBUG'
        return cls.LOG_LEVEL.upper()


# Global config instance
config = Config()


def load_config() -> Config:
    """
    Load and validate configuration

    Returns:
        Config instance

    Raises:
        ValueError: If required configuration is missing
    """
    missing = config.validate_config()
    if missing:
        raise ValueError(f"Missing required configuration: {', '.join(missing)}")

    return config