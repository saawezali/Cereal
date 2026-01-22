"""
Repository pattern implementation for Cereal Bot
Provides high-level data access methods for database entities
"""

from typing import List, Optional, Dict, Any, Type, TypeVar, Generic
from sqlalchemy import select, update, delete, func, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession

from .base import db
from .models import User, Guild, GuildMember, Warning, CustomCommand, Giveaway
from core import get_logger

logger = get_logger(__name__)

T = TypeVar('T')


class BaseRepository(Generic[T]):
    """Base repository class with common CRUD operations"""

    def __init__(self, model: Type[T]):
        self.model = model

    async def get_by_id(self, id: int) -> Optional[T]:
        """Get entity by ID"""
        return await db.get(self.model, id=id)

    async def get_all(self, **filters) -> List[T]:
        """Get all entities matching filters"""
        return await db.get_all(self.model, **filters)

    async def create(self, **data) -> T:
        """Create new entity"""
        return await db.create(self.model, **data)

    async def update(self, filters: Dict[str, Any], **data) -> int:
        """Update entities matching filters"""
        return await db.update(self.model, filters, **data)

    async def delete(self, **filters) -> int:
        """Delete entities matching filters"""
        return await db.delete(self.model, **filters)

    async def exists(self, **filters) -> bool:
        """Check if any entities match filters"""
        return await db.exists(self.model, **filters)

    async def count(self, **filters) -> int:
        """Count entities matching filters"""
        return await db.count(self.model, **filters)

    async def get_first(self, **filters) -> Optional[T]:
        """Get first entity matching filters"""
        results = await self.get_all(**filters)
        return results[0] if results else None

    async def get_paginated(self, page: int = 1, per_page: int = 10, **filters) -> Dict[str, Any]:
        """Get paginated results"""
        offset = (page - 1) * per_page

        async with db.session() as session:
            # Get total count
            count_query = select(func.count()).select_from(self.model).filter_by(**filters)
            total_result = await session.execute(count_query)
            total = total_result.scalar()

            # Get paginated results
            query = select(self.model).filter_by(**filters).offset(offset).limit(per_page)
            result = await session.execute(query)
            items = list(result.scalars().all())

        return {
            'items': items,
            'total': total,
            'page': page,
            'per_page': per_page,
            'pages': (total + per_page - 1) // per_page
        }


class UserRepository(BaseRepository[User]):
    """Repository for User entities"""

    def __init__(self):
        super().__init__(User)

    async def get_by_discord_id(self, discord_id: int) -> Optional[User]:
        """Get user by Discord ID"""
        return await self.get_by_id(discord_id)

    async def create_or_update_from_discord(self, discord_user) -> User:
        """Create or update user from Discord user object"""
        user_data = {
            'id': discord_user.id,
            'username': discord_user.name,
            'discriminator': getattr(discord_user, 'discriminator', None),
            'avatar_hash': discord_user.avatar.key if discord_user.avatar else None,
            'bot': discord_user.bot
        }

        existing = await self.get_by_discord_id(discord_user.id)
        if existing:
            # Update existing user
            await self.update({'id': discord_user.id}, **user_data)
            return await self.get_by_discord_id(discord_user.id)
        else:
            # Create new user
            return await self.create(**user_data)

    async def get_active_users(self, days: int = 7) -> List[User]:
        """Get users active within the last N days"""
        from datetime import datetime, timedelta

        cutoff = datetime.utcnow() - timedelta(days=days)
        async with db.session() as session:
            stmt = select(User).where(User.last_active >= cutoff).order_by(User.last_active.desc())
            result = await session.execute(stmt)
            return list(result.scalars().all())


class GuildRepository(BaseRepository[Guild]):
    """Repository for Guild entities"""

    def __init__(self):
        super().__init__(Guild)

    async def get_by_discord_id(self, discord_id: int) -> Optional[Guild]:
        """Get guild by Discord ID"""
        return await self.get_by_id(discord_id)

    async def create_or_update_from_discord(self, discord_guild) -> Guild:
        """Create or update guild from Discord guild object"""
        guild_data = {
            'id': discord_guild.id,
            'name': discord_guild.name,
            'owner_id': discord_guild.owner_id,
            'member_count': discord_guild.member_count
        }

        existing = await self.get_by_discord_id(discord_guild.id)
        if existing:
            await self.update({'id': discord_guild.id}, **guild_data)
            return await self.get_by_discord_id(discord_guild.id)
        else:
            return await self.create(**guild_data)

    async def update_member_count(self, guild_id: int, count: int) -> bool:
        """Update member count for guild"""
        updated = await self.update({'id': guild_id}, member_count=count)
        return updated > 0

    async def get_guild_settings(self, guild_id: int) -> Optional[Dict[str, Any]]:
        """Get guild settings as dictionary"""
        guild = await self.get_by_discord_id(guild_id)
        if not guild:
            return None

        return {
            'prefix': guild.prefix,
            'timezone': guild.timezone,
            'welcome_enabled': guild.welcome_enabled,
            'welcome_channel_id': guild.welcome_channel_id,
            'welcome_message': guild.welcome_message,
            'log_channel_id': guild.log_channel_id
        }


class GuildMemberRepository(BaseRepository[GuildMember]):
    """Repository for GuildMember entities"""

    def __init__(self):
        super().__init__(GuildMember)

    async def get_member(self, guild_id: int, user_id: int) -> Optional[GuildMember]:
        """Get guild member by guild and user ID"""
        return await db.get(GuildMember, guild_id=guild_id, user_id=user_id)

    async def create_or_update_member(self, guild_id: int, user_id: int, **data) -> GuildMember:
        """Create or update guild member"""
        member_data = {
            'guild_id': guild_id,
            'user_id': user_id,
            **data
        }

        existing = await self.get_member(guild_id, user_id)
        if existing:
            await self.update({'guild_id': guild_id, 'user_id': user_id}, **member_data)
            return await self.get_member(guild_id, user_id)
        else:
            return await self.create(**member_data)


class WarningRepository(BaseRepository[Warning]):
    """Repository for Warning entities"""

    def __init__(self):
        super().__init__(Warning)

    async def get_guild_warnings(self, guild_id: int, user_id: Optional[int] = None) -> List[Warning]:
        """Get warnings for a guild, optionally filtered by user"""
        if user_id:
            return await self.get_all(guild_id=guild_id, user_id=user_id)
        return await self.get_all(guild_id=guild_id)

    async def add_warning(self, guild_id: int, user_id: int, moderator_id: int, reason: str) -> Warning:
        """Add a warning"""
        return await self.create(
            guild_id=guild_id,
            user_id=user_id,
            moderator_id=moderator_id,
            reason=reason
        )

    async def get_warning_count(self, guild_id: int, user_id: int) -> int:
        """Get warning count for a user in a guild"""
        return await self.count(guild_id=guild_id, user_id=user_id)


class CustomCommandRepository(BaseRepository[CustomCommand]):
    """Repository for CustomCommand entities"""

    def __init__(self):
        super().__init__(CustomCommand)

    async def get_guild_commands(self, guild_id: int) -> List[CustomCommand]:
        """Get all custom commands for a guild"""
        return await self.get_all(guild_id=guild_id)

    async def get_command(self, guild_id: int, name: str) -> Optional[CustomCommand]:
        """Get a specific custom command"""
        return await db.get(CustomCommand, guild_id=guild_id, name=name)

    async def increment_usage(self, command_id: int) -> bool:
        """Increment usage count for a command"""
        async with db.session() as session:
            stmt = update(CustomCommand).where(CustomCommand.id == command_id).values(
                usage_count=CustomCommand.usage_count + 1
            )
            result = await session.execute(stmt)
            return result.rowcount > 0


class GiveawayRepository(BaseRepository[Giveaway]):
    """Repository for Giveaway entities"""

    def __init__(self):
        super().__init__(Giveaway)

    async def get_active_giveaways(self, guild_id: Optional[int] = None) -> List[Giveaway]:
        """Get active giveaways, optionally filtered by guild"""
        filters = {'active': True}
        if guild_id:
            filters['guild_id'] = guild_id
        return await self.get_all(**filters)

    async def get_expired_giveaways(self) -> List[Giveaway]:
        """Get expired giveaways that need processing"""
        from datetime import datetime

        async with db.session() as session:
            stmt = select(Giveaway).where(
                and_(Giveaway.active == True, Giveaway.end_time <= datetime.utcnow())
            )
            result = await session.execute(stmt)
            return list(result.scalars().all())

    async def add_participant(self, giveaway_id: int, user_id: int) -> bool:
        """Add a participant to a giveaway"""
        giveaway = await self.get_by_id(giveaway_id)
        if not giveaway or not giveaway.active:
            return False

        participants = giveaway.participants or '[]'
        import json
        try:
            participant_list = json.loads(participants)
        except:
            participant_list = []

        if user_id not in participant_list:
            participant_list.append(user_id)
            participants = json.dumps(participant_list)
            await self.update({'id': giveaway_id}, participants=participants)
            return True
        return False

    async def end_giveaway(self, giveaway_id: int) -> Optional[Giveaway]:
        """End a giveaway and mark as inactive"""
        await self.update({'id': giveaway_id}, active=False)
        return await self.get_by_id(giveaway_id)


# Global repository instances
user_repo = UserRepository()
guild_repo = GuildRepository()
guild_member_repo = GuildMemberRepository()
warning_repo = WarningRepository()
custom_command_repo = CustomCommandRepository()
giveaway_repo = GiveawayRepository()


async def initialize_repositories():
    """Initialize all repositories (called during bot startup)"""
    logger.info("Repositories initialized")


# Export repositories
__all__ = [
    'BaseRepository',
    'UserRepository',
    'GuildRepository',
    'GuildMemberRepository',
    'WarningRepository',
    'CustomCommandRepository',
    'GiveawayRepository',
    'user_repo',
    'guild_repo',
    'guild_member_repo',
    'warning_repo',
    'custom_command_repo',
    'giveaway_repo',
    'initialize_repositories'
]