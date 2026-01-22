"""
Structured logging configuration for Cereal Bot
"""

import logging
import logging.handlers
import sys
from pathlib import Path
from typing import Optional

from .config import config


class CerealLogger:
    """Custom logger for Cereal Bot with structured formatting"""

    def __init__(self):
        self.logger = logging.getLogger('cereal_bot')
        self.logger.setLevel(getattr(logging, config.LOG_LEVEL.upper(), logging.INFO))

        # Remove any existing handlers
        self.logger.handlers.clear()

        # Create formatters
        self._setup_formatters()

        # Add handlers
        self._setup_handlers()

    def _setup_formatters(self):
        """Setup logging formatters"""
        # Console formatter (colored for development)
        if config.DEBUG_MODE:
            self.console_formatter = logging.Formatter(
                '%(asctime)s | %(levelname)s | %(name)s | %(message)s',
                datefmt='%H:%M:%S'
            )
        else:
            self.console_formatter = logging.Formatter(
                '%(asctime)s | %(levelname)s | %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )

        # File formatter (detailed)
        self.file_formatter = logging.Formatter(
            '%(asctime)s | %(levelname)s | %(name)s | %(filename)s:%(lineno)d | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

    def _setup_handlers(self):
        """Setup logging handlers"""
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(getattr(logging, config.LOG_LEVEL.upper(), logging.INFO))
        console_handler.setFormatter(self.console_formatter)
        self.logger.addHandler(console_handler)

        # File handler (rotating)
        if config.LOG_FILE:
            log_path = Path(config.LOG_FILE)
            log_path.parent.mkdir(parents=True, exist_ok=True)

            file_handler = logging.handlers.RotatingFileHandler(
                config.LOG_FILE,
                maxBytes=config.LOG_MAX_SIZE,
                backupCount=config.LOG_BACKUP_COUNT,
                encoding='utf-8'
            )
            file_handler.setLevel(logging.DEBUG)  # Log everything to file
            file_handler.setFormatter(self.file_formatter)
            self.logger.addHandler(file_handler)

    def get_logger(self, name: Optional[str] = None) -> logging.Logger:
        """
        Get a logger instance

        Args:
            name: Logger name (usually __name__)

        Returns:
            Logger instance
        """
        if name:
            return self.logger.getChild(name)
        return self.logger

    def log_command(self, user: str, command: str, guild: Optional[str] = None, **kwargs):
        """
        Log command usage

        Args:
            user: User who executed the command
            command: Command name
            guild: Guild name (optional)
            **kwargs: Additional context
        """
        context = f"user={user}, command={command}"
        if guild:
            context += f", guild={guild}"
        if kwargs:
            context += f", {', '.join(f'{k}={v}' for k, v in kwargs.items())}"

        self.logger.info(f"Command executed: {context}")

    def log_error(self, error: Exception, context: Optional[str] = None, **kwargs):
        """
        Log errors with context

        Args:
            error: Exception that occurred
            context: Additional context
            **kwargs: Additional data
        """
        error_msg = f"{type(error).__name__}: {str(error)}"
        if context:
            error_msg = f"{context} - {error_msg}"
        if kwargs:
            error_msg += f" | {', '.join(f'{k}={v}' for k, v in kwargs.items())}"

        self.logger.error(error_msg, exc_info=True)

    def log_database_operation(self, operation: str, table: str, **kwargs):
        """
        Log database operations

        Args:
            operation: Operation type (CREATE, READ, UPDATE, DELETE)
            table: Table name
            **kwargs: Additional context
        """
        context = f"operation={operation}, table={table}"
        if kwargs:
            context += f", {', '.join(f'{k}={v}' for k, v in kwargs.items())}"

        self.logger.debug(f"Database: {context}")


# Global logger instance
_logger_instance = None


def get_logger(name: Optional[str] = None) -> logging.Logger:
    """
    Get the global logger instance

    Args:
        name: Logger name (usually __name__)

    Returns:
        Logger instance
    """
    global _logger_instance
    if _logger_instance is None:
        _logger_instance = CerealLogger()
    return _logger_instance.get_logger(name)


def setup_logging():
    """Setup logging for the entire application"""
    global _logger_instance
    _logger_instance = CerealLogger()

    # Set up Discord.py logging
    discord_logger = logging.getLogger('discord')
    discord_logger.setLevel(logging.WARNING)  # Only show warnings and errors from discord.py

    # Set up other library loggers
    logging.getLogger('aiosqlite').setLevel(logging.WARNING)
    logging.getLogger('sqlalchemy').setLevel(logging.WARNING)

    logger = get_logger()
    logger.info("Logging system initialized")


# Convenience functions
def log_command(user: str, command: str, guild: Optional[str] = None, **kwargs):
    """Log command usage"""
    global _logger_instance
    if _logger_instance:
        _logger_instance.log_command(user, command, guild, **kwargs)


def log_error(error: Exception, context: Optional[str] = None, **kwargs):
    """Log errors with context"""
    global _logger_instance
    if _logger_instance:
        _logger_instance.log_error(error, context, **kwargs)


def log_db_operation(operation: str, table: str, **kwargs):
    """Log database operations"""
    global _logger_instance
    if _logger_instance:
        _logger_instance.log_database_operation(operation, table, **kwargs)