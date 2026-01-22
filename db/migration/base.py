"""
Base migration utilities for database migrations
Supports migration from SQLite to PostgreSQL
"""

import asyncio
import os
from typing import Dict, List, Any, Optional
from datetime import datetime
from pathlib import Path

from core import get_logger, config
from db import db, Base

logger = get_logger(__name__)


class MigrationError(Exception):
    """Custom exception for migration errors"""
    pass


class DatabaseMigrator:
    """Handles database migrations between different database types"""

    def __init__(self, source_db_path: str, target_db_url: str):
        """
        Initialize migrator

        Args:
            source_db_path: Path to source SQLite database
            target_db_url: Target database URL (PostgreSQL)
        """
        self.source_db_path = source_db_path
        self.target_db_url = target_db_url
        self.backup_path = f"{source_db_path}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

    async def create_backup(self) -> str:
        """
        Create backup of source database

        Returns:
            Path to backup file
        """
        import shutil

        logger.info(f"Creating backup: {self.source_db_path} -> {self.backup_path}")
        shutil.copy2(self.source_db_path, self.backup_path)
        logger.info("Backup created successfully")
        return self.backup_path

    async def validate_source_data(self) -> Dict[str, int]:
        """
        Validate source database and get table row counts

        Returns:
            Dictionary of table names to row counts
        """
        logger.info("Validating source database...")

        # This would need to be implemented based on your specific models
        # For now, return empty dict
        return {}

    async def migrate_table_data(self, table_name: str, batch_size: int = 1000) -> int:
        """
        Migrate data for a specific table

        Args:
            table_name: Name of table to migrate
            batch_size: Number of rows to migrate at once

        Returns:
            Number of rows migrated
        """
        logger.info(f"Migrating table: {table_name}")

        # This would need to be implemented based on your specific models
        # For now, return 0
        return 0

    async def run_migration(self, tables: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Run the complete migration process

        Args:
            tables: List of tables to migrate (None for all)

        Returns:
            Migration results dictionary
        """
        results = {
            'success': False,
            'backup_path': None,
            'migrated_tables': {},
            'errors': [],
            'start_time': datetime.now()
        }

        try:
            # Create backup
            results['backup_path'] = await self.create_backup()

            # Validate source data
            source_stats = await self.validate_source_data()
            logger.info(f"Source database stats: {source_stats}")

            # Migrate tables
            if tables is None:
                # Get all tables from models
                from db.models import Base
                tables = [table.name for table in Base.metadata.tables.values()]

            for table in tables:
                try:
                    row_count = await self.migrate_table_data(table)
                    results['migrated_tables'][table] = row_count
                    logger.info(f"Migrated {row_count} rows from {table}")
                except Exception as e:
                    error_msg = f"Failed to migrate table {table}: {str(e)}"
                    results['errors'].append(error_msg)
                    logger.error(error_msg)

            results['success'] = len(results['errors']) == 0
            results['end_time'] = datetime.now()
            results['duration'] = (results['end_time'] - results['start_time']).total_seconds()

            if results['success']:
                logger.info("Migration completed successfully!")
            else:
                logger.error(f"Migration completed with {len(results['errors'])} errors")

        except Exception as e:
            results['errors'].append(f"Migration failed: {str(e)}")
            logger.error(f"Migration failed: {str(e)}")

        return results


async def migrate_sqlite_to_postgres(
    sqlite_path: str = "cereal.db",
    postgres_url: Optional[str] = None
) -> Dict[str, Any]:
    """
    Convenience function to migrate from SQLite to PostgreSQL

    Args:
        sqlite_path: Path to SQLite database file
        postgres_url: PostgreSQL connection URL

    Returns:
        Migration results
    """
    if postgres_url is None:
        postgres_url = config.DATABASE_URL

    migrator = DatabaseMigrator(sqlite_path, postgres_url)
    return await migrator.run_migration()


def create_migration_script_template(migration_name: str) -> str:
    """
    Create a template for a new migration script

    Args:
        migration_name: Name of the migration

    Returns:
        Migration script template as string
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    template = f'''"""
Migration: {migration_name}
Created: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
"""

import asyncio
from core import get_logger
from migration.base import migrate_sqlite_to_postgres

logger = get_logger(__name__)


async def run_migration():
    """Run the {migration_name} migration"""
    logger.info("Starting migration: {migration_name}")

    try:
        # Configure migration settings
        sqlite_path = "cereal.db"
        postgres_url = None  # Will use config.DATABASE_URL

        # Run migration
        results = await migrate_sqlite_to_postgres(sqlite_path, postgres_url)

        if results['success']:
            logger.info(f"✅ Migration '{migration_name}' completed successfully!")
            logger.info(f"Duration: {{results['duration']:.2f}} seconds")
            logger.info(f"Migrated tables: {{results['migrated_tables']}}")
        else:
            logger.error(f"❌ Migration '{migration_name}' failed!")
            for error in results['errors']:
                logger.error(f"  - {{error}}")

        return results

    except Exception as e:
        logger.error(f"Migration '{migration_name}' failed with exception: {{e}}")
        raise


if __name__ == "__main__":
    # Run migration
    results = asyncio.run(run_migration())

    # Exit with appropriate code
    exit(0 if results.get('success', False) else 1)
'''

    return template


def list_available_migrations() -> List[str]:
    """
    List all available migration scripts

    Returns:
        List of migration script names
    """
    migration_dir = Path(__file__).parent
    migrations = []

    for file in migration_dir.glob("*.py"):
        if file.name not in ["__init__.py", "base.py"]:
            migrations.append(file.stem)

    return sorted(migrations)