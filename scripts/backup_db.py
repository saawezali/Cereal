#!/usr/bin/env python3
"""
Database backup script for Cereal Bot
Creates timestamped backups of the SQLite database
"""

import os
import shutil
from datetime import datetime
from pathlib import Path

def create_backup():
    """Create a timestamped backup of the database"""
    db_path = Path("cereal.db")
    backup_dir = Path("backups")

    # Create backup directory if it doesn't exist
    backup_dir.mkdir(exist_ok=True)

    if not db_path.exists():
        print("❌ Database file not found!")
        return False

    # Create timestamped backup filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_filename = f"cereal_backup_{timestamp}.db"
    backup_path = backup_dir / backup_filename

    try:
        # Copy database file
        shutil.copy2(db_path, backup_path)
        print(f"✅ Database backup created: {backup_path}")

        # Clean up old backups (keep last 10)
        backups = sorted(backup_dir.glob("cereal_backup_*.db"), reverse=True)
        if len(backups) > 10:
            for old_backup in backups[10:]:
                old_backup.unlink()
                print(f"🗑️  Removed old backup: {old_backup.name}")

        return True

    except Exception as e:
        print(f"❌ Backup failed: {e}")
        return False

def list_backups():
    """List all available backups"""
    backup_dir = Path("backups")
    if not backup_dir.exists():
        print("No backups directory found.")
        return

    backups = list(backup_dir.glob("cereal_backup_*.db"))
    if not backups:
        print("No backups found.")
        return

    print("Available backups:")
    for backup in sorted(backups, reverse=True):
        size = backup.stat().st_size / 1024  # Size in KB
        print(".1f")

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "list":
        list_backups()
    else:
        success = create_backup()
        sys.exit(0 if success else 1)