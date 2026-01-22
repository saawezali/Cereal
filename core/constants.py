"""
Constants and configuration values for Cereal Bot
"""

import discord
from typing import Dict, List

# Bot Information
BOT_NAME = "Cereal Bot"
BOT_VERSION = "2.0.0"
BOT_DESCRIPTION = "🥣 A fun and moderation Discord bot with games and utilities"

# Discord Colors (for embeds)
class Colors:
    """Discord embed colors"""
    PRIMARY = discord.Color.blue()
    SUCCESS = discord.Color.green()
    ERROR = discord.Color.red()
    WARNING = discord.Color.orange()
    INFO = discord.Color.blurple()

    # Custom colors
    FUN = discord.Color.purple()
    MODERATION = discord.Color.dark_red()
    GAMES = discord.Color.gold()
    UTILITY = discord.Color.teal()

# Emojis
class Emojis:
    """Common emojis used throughout the bot"""
    SUCCESS = "✅"
    ERROR = "❌"
    WARNING = "⚠️"
    INFO = "ℹ️"
    LOADING = "⏳"
    CHECK = "✔️"
    CROSS = "✖️"

    # Fun emojis
    CERAL = "🥣"
    PARTY = "🎉"
    STAR = "⭐"
    FIRE = "🔥"
    COOL = "😎"
    THINK = "🤔"

    # Status emojis
    ONLINE = "🟢"
    IDLE = "🟡"
    DND = "🔴"
    OFFLINE = "⚫"

    # Moderation
    BAN = "🔨"
    KICK = "👢"
    MUTE = "🔇"
    WARN = "⚠️"
    LOCK = "🔒"
    UNLOCK = "🔓"

    # Games
    DICE = "🎲"
    CARD = "🃏"
    TROPHY = "🏆"
    MEDAL = "🏅"

# Permission Levels
class Permissions:
    """Permission level constants"""
    USER = 0
    MODERATOR = 1
    ADMIN = 2
    OWNER = 3

# Time Constants
class Time:
    """Time constants in seconds"""
    SECOND = 1
    MINUTE = 60
    HOUR = 3600
    DAY = 86400
    WEEK = 604800
    MONTH = 2592000  # 30 days

# Database Constants
class Database:
    """Database-related constants"""
    DEFAULT_DB_PATH = "cereal.db"

    # Table names
    USERS_TABLE = "users"
    GUILDS_TABLE = "guilds"
    GUILD_MEMBERS_TABLE = "guild_members"
    WARNINGS_TABLE = "warnings"
    CUSTOM_COMMANDS_TABLE = "custom_commands"
    GIVEAWAYS_TABLE = "giveaways"

# API Constants
class APIs:
    """External API endpoints and settings"""
    # Add your API endpoints here when needed
    # WEATHER_API = "https://api.weatherapi.com/v1"
    # JOKE_API = "https://v2.jokeapi.dev"
    pass

# Game Constants
class Games:
    """Constants for game features"""
    DEFAULT_XP_PER_MESSAGE = 1
    XP_COOLDOWN_SECONDS = 60  # 1 minute cooldown between XP gains

    LEVEL_XP_BASE = 100  # Base XP needed for level 1
    LEVEL_XP_MULTIPLIER = 1.5  # XP requirement increases by this factor per level

    # Coin rewards
    DAILY_COINS = 100
    WEEKLY_COINS = 500

# Moderation Constants
class Moderation:
    """Constants for moderation features"""
    DEFAULT_WARN_LIMIT = 3  # Warnings before action
    DEFAULT_MUTE_DURATION = Time.HOUR  # Default mute time
    DEFAULT_BAN_DURATION = Time.DAY * 7  # Default ban time (1 week)

    # Auto-moderation settings
    SPAM_THRESHOLD = 5  # Messages per minute
    DUPLICATE_THRESHOLD = 3  # Duplicate messages allowed

# Pagination Constants
class Pagination:
    """Constants for pagination features"""
    DEFAULT_PAGE_SIZE = 10
    MAX_PAGE_SIZE = 25
    EMBED_TIMEOUT = Time.MINUTE * 5  # 5 minutes

# Error Messages
class ErrorMessages:
    """Common error messages"""
    PERMISSION_DENIED = "You don't have permission to use this command."
    USER_NOT_FOUND = "User not found."
    COMMAND_COOLDOWN = "This command is on cooldown. Please wait {time} seconds."
    DATABASE_ERROR = "Database error occurred. Please try again later."
    API_ERROR = "External service is currently unavailable."
    INVALID_ARGUMENTS = "Invalid arguments provided."

# Success Messages
class SuccessMessages:
    """Common success messages"""
    COMMAND_SUCCESS = "Command executed successfully!"
    USER_UPDATED = "User data updated successfully."
    SETTINGS_SAVED = "Settings saved successfully."
    DATA_DELETED = "Data deleted successfully."

# Command Categories
COMMAND_CATEGORIES = {
    "moderation": {
        "name": "Moderation",
        "description": "Server moderation commands",
        "emoji": Emojis.BAN
    },
    "games": {
        "name": "Games",
        "description": "Fun games and activities",
        "emoji": Emojis.DICE
    },
    "fun": {
        "name": "Fun",
        "description": "Fun and meme commands",
        "emoji": Emojis.PARTY
    },
    "utility": {
        "name": "Utility",
        "description": "Useful utility commands",
        "emoji": Emojis.INFO
    }
}

# Default Guild Settings
DEFAULT_GUILD_SETTINGS = {
    "prefix": "!",
    "timezone": "UTC",
    "welcome_enabled": False,
    "welcome_channel_id": None,
    "welcome_message": "Welcome {user} to {guild}!",
    "log_channel_id": None,
    "xp_enabled": True,
    "auto_mod_enabled": False,
    "spam_filter_enabled": False
}