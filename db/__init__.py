"""
Database module for Cereal Bot
"""

from .base import db, init_db, close_db, Base, Database
from .models import User, Guild, GuildMember, Warning, CustomCommand, Giveaway, AutomemeConfig
from .repository import (
    BaseRepository,
    UserRepository,
    GuildRepository,
    GuildMemberRepository,
    WarningRepository,
    CustomCommandRepository,
    GiveawayRepository,
    AutomemeRepository,
    user_repo,
    guild_repo,
    guild_member_repo,
    warning_repo,
    custom_command_repo,
    giveaway_repo,
    automeme_repo,
    initialize_repositories
)

__all__ = [
    'db',
    'init_db',
    'close_db',
    'Base',
    'Database',
    'User',
    'Guild',
    'GuildMember',
    'Warning',
    'CustomCommand',
    'Giveaway',
    'AutomemeConfig',
    'BaseRepository',
    'UserRepository',
    'GuildRepository',
    'GuildMemberRepository',
    'WarningRepository',
    'CustomCommandRepository',
    'GiveawayRepository',
    'AutomemeRepository',
    'user_repo',
    'guild_repo',
    'guild_member_repo',
    'warning_repo',
    'custom_command_repo',
    'giveaway_repo',
    'automeme_repo',
    'initialize_repositories'
]