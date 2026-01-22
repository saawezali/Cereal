"""
Database migration module for Cereal Bot
Handles migrations between different database types
"""

from .base import (
    DatabaseMigrator,
    migrate_sqlite_to_postgres,
    create_migration_script_template,
    list_available_migrations,
    MigrationError
)

__all__ = [
    'DatabaseMigrator',
    'migrate_sqlite_to_postgres',
    'create_migration_script_template',
    'list_available_migrations',
    'MigrationError'
]