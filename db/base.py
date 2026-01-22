"""
Database base module for Cereal Bot
Provides async SQLite database functionality using SQLAlchemy + aiosqlite
"""

import asyncio
import os
from typing import Optional, Any, Dict, List
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker
from sqlalchemy import select, update, delete, func
from contextlib import asynccontextmanager


class Base(DeclarativeBase):
    """Base class for all database models"""
    pass


class Database:
    """Async SQLite database manager for the bot"""

    def __init__(self, db_path: str = "cereal.db"):
        """
        Initialize database connection

        Args:
            db_path: Path to SQLite database file (relative to project root)
        """
        # Ensure db directory exists
        os.makedirs(os.path.dirname(db_path) if os.path.dirname(db_path) else ".", exist_ok=True)

        # Create async engine
        self.engine = create_async_engine(
            f"sqlite+aiosqlite:///{db_path}",
            echo=False,  # Set to True for SQL query logging
            connect_args={"check_same_thread": False}
        )

        # Create async session factory
        self.async_session = async_sessionmaker(
            self.engine,
            class_=AsyncSession,
            expire_on_commit=False
        )

        self._initialized = False

    async def initialize(self) -> None:
        """Initialize database and create all tables"""
        if self._initialized:
            return

        try:
            # Create all tables
            async with self.engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)

            self._initialized = True
            print("✓ Database initialized successfully")

        except Exception as e:
            print(f"✗ Database initialization failed: {e}")
            raise

    async def close(self) -> None:
        """Close database connections"""
        if hasattr(self, 'engine'):
            await self.engine.dispose()
            print("✓ Database connections closed")

    @asynccontextmanager
    async def session(self):
        """Async context manager for database sessions"""
        async with self.async_session() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()

    # Generic CRUD operations

    async def get(self, model: type[Base], **filters) -> Optional[Base]:
        """
        Get a single record by filters

        Args:
            model: SQLAlchemy model class
            **filters: Column filters (e.g., id=1, name="test")

        Returns:
            Model instance or None if not found
        """
        async with self.session() as session:
            stmt = select(model).filter_by(**filters)
            result = await session.execute(stmt)
            return result.scalar_one_or_none()

    async def get_all(self, model: type[Base], **filters) -> List[Base]:
        """
        Get all records matching filters

        Args:
            model: SQLAlchemy model class
            **filters: Column filters

        Returns:
            List of model instances
        """
        async with self.session() as session:
            stmt = select(model).filter_by(**filters)
            result = await session.execute(stmt)
            return list(result.scalars().all())

    async def create(self, model: type[Base], **data) -> Base:
        """
        Create a new record

        Args:
            model: SQLAlchemy model class
            **data: Column data

        Returns:
            Created model instance
        """
        async with self.session() as session:
            instance = model(**data)
            session.add(instance)
            await session.flush()  # Get the ID without committing
            await session.refresh(instance)  # Load any defaults
            return instance

    async def update(self, model: type[Base], filters: Dict[str, Any], **data) -> int:
        """
        Update records matching filters

        Args:
            model: SQLAlchemy model class
            filters: Dict of column filters
            **data: Data to update

        Returns:
            Number of rows updated
        """
        async with self.session() as session:
            stmt = update(model).filter_by(**filters).values(**data)
            result = await session.execute(stmt)
            return result.rowcount

    async def delete(self, model: type[Base], **filters) -> int:
        """
        Delete records matching filters

        Args:
            model: SQLAlchemy model class
            **filters: Column filters

        Returns:
            Number of rows deleted
        """
        async with self.session() as session:
            stmt = delete(model).filter_by(**filters)
            result = await session.execute(stmt)
            return result.rowcount

    async def count(self, model: type[Base], **filters) -> int:
        """
        Count records matching filters

        Args:
            model: SQLAlchemy model class
            **filters: Column filters

        Returns:
            Number of matching records
        """
        async with self.session() as session:
            stmt = select(func.count()).select_from(model).filter_by(**filters)
            result = await session.execute(stmt)
            return result.scalar()

    async def exists(self, model: type[Base], **filters) -> bool:
        """
        Check if any records match filters

        Args:
            model: SQLAlchemy model class
            **filters: Column filters

        Returns:
            True if any records exist, False otherwise
        """
        count = await self.count(model, **filters)
        return count > 0


# Global database instance
db = Database()


async def init_db():
    """Initialize the global database instance"""
    await db.initialize()


async def close_db():
    """Close the global database instance"""
    await db.close()