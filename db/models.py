"""
Database models for Cereal Bot
"""

from datetime import datetime
from typing import Optional
from sqlalchemy import BigInteger, String, DateTime, Boolean, Integer, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class User(Base):
    """User data model"""
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=False)  # Discord user ID
    username: Mapped[str] = mapped_column(String(32), nullable=False)
    discriminator: Mapped[Optional[str]] = mapped_column(String(4), nullable=True)  # For legacy usernames
    avatar_hash: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
    bot: Mapped[bool] = mapped_column(Boolean, default=False)

    # Bot-specific data
    coins: Mapped[int] = mapped_column(Integer, default=0)
    joined_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    last_active: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # Relationships
    guild_memberships: Mapped[list["GuildMember"]] = relationship(back_populates="user")

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', level={self.level})>"


class Guild(Base):
    """Guild/Server data model"""
    __tablename__ = 'guilds'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=False)  # Discord guild ID
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    owner_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    member_count: Mapped[int] = mapped_column(Integer, default=0)
    joined_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # Guild settings
    prefix: Mapped[str] = mapped_column(String(5), default='!')
    timezone: Mapped[str] = mapped_column(String(50), default='UTC')
    welcome_enabled: Mapped[bool] = mapped_column(Boolean, default=False)
    welcome_channel_id: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)
    welcome_message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    log_channel_id: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)

    # Relationships
    members: Mapped[list["GuildMember"]] = relationship(back_populates="guild")

    def __repr__(self):
        return f"<Guild(id={self.id}, name='{self.name}')>"


class GuildMember(Base):
    """Guild member data model (many-to-many relationship)"""
    __tablename__ = 'guild_members'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    guild_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('guilds.id'), nullable=False)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('users.id'), nullable=False)

    # Member-specific data
    joined_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    nickname: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
    roles: Mapped[str] = mapped_column(Text, default='[]')  # JSON array of role IDs

    # Relationships
    user: Mapped["User"] = relationship(back_populates="guild_memberships")
    guild: Mapped["Guild"] = relationship(back_populates="members")

    def __repr__(self):
        return f"<GuildMember(guild_id={self.guild_id}, user_id={self.user_id})>"


class Warning(Base):
    """Warning/moderation data model"""
    __tablename__ = 'warnings'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    guild_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    user_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    moderator_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    reason: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Warning(id={self.id}, user_id={self.user_id}, reason='{self.reason[:50]}...')>"


class CustomCommand(Base):
    """Custom command data model"""
    __tablename__ = 'custom_commands'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    guild_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    response: Mapped[str] = mapped_column(Text, nullable=False)
    created_by: Mapped[int] = mapped_column(BigInteger, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    usage_count: Mapped[int] = mapped_column(Integer, default=0)

    def __repr__(self):
        return f"<CustomCommand(name='{self.name}', guild_id={self.guild_id})>"


class Giveaway(Base):
    """Giveaway data model"""
    __tablename__ = 'giveaways'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    guild_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    channel_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    message_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    prize: Mapped[str] = mapped_column(String(200), nullable=False)
    winner_count: Mapped[int] = mapped_column(Integer, default=1)
    end_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    created_by: Mapped[int] = mapped_column(BigInteger, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    participants: Mapped[str] = mapped_column(Text, default='[]')  # JSON array of user IDs

    def __repr__(self):
        return f"<Giveaway(id={self.id}, title='{self.title}', active={self.active})>"