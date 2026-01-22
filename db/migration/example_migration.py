"""
Example migration script
This demonstrates how to create a migration from SQLite to PostgreSQL
"""

import asyncio
from core import get_logger
from .base import migrate_sqlite_to_postgres

logger = get_logger(__name__)


async def run_migration():
    """Run the example migration"""
    logger.info("Starting example migration")

    try:
        # Configure migration settings
        sqlite_path = "cereal.db"
        postgres_url = None  # Will use config.DATABASE_URL

        # Run migration
        results = await migrate_sqlite_to_postgres(sqlite_path, postgres_url)

        if results['success']:
            logger.info("✅ Example migration completed successfully!")
            logger.info(f"Duration: {results['duration']:.2f} seconds")
            logger.info(f"Migrated tables: {results['migrated_tables']}")
        else:
            logger.error("❌ Example migration failed!")
            for error in results['errors']:
                logger.error(f"  - {error}")

        return results

    except Exception as e:
        logger.error(f"Example migration failed with exception: {e}")
        raise


if __name__ == "__main__":
    # Run migration
    results = asyncio.run(run_migration())

    # Exit with appropriate code
    exit(0 if results.get('success', False) else 1)