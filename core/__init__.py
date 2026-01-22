"""
Core module for Cereal Bot
Provides configuration, constants, and logging functionality
"""

from .config import config, load_config, Config
from .constants import (
    Colors, Emojis, Permissions, Time, Database, APIs, Games,
    Moderation, Pagination, ErrorMessages, SuccessMessages,
    COMMAND_CATEGORIES, DEFAULT_GUILD_SETTINGS
)
from .logger import (
    get_logger, setup_logging, log_command, log_error, log_db_operation
)

__all__ = [
    # Config
    'config',
    'load_config',
    'Config',

    # Constants
    'Colors',
    'Emojis',
    'Permissions',
    'Time',
    'Database',
    'APIs',
    'Games',
    'Moderation',
    'Pagination',
    'ErrorMessages',
    'SuccessMessages',
    'COMMAND_CATEGORIES',
    'DEFAULT_GUILD_SETTINGS',

    # Logging
    'get_logger',
    'setup_logging',
    'log_command',
    'log_error',
    'log_db_operation'
]