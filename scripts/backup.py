# ===== scripts/backup.py =====
#!/usr/bin/env python3
"""
Backup script for ASTHA application data
"""

import os
import shutil
import sqlite3
import datetime
import argparse
from pathlib import Path

def backup_database(db_path: str, backup_dir: str):
    """Backup SQLite database"""
    if not os.path.exists(db_path):
        print(f"Database not found: {db_path}")
        return False
    
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_filename = f"astha_backup_{timestamp}.db"
    backup_path = os.path.join(backup_dir, backup_filename)
    
    try:
        # Create backup directory if it doesn't exist
        os.makedirs(backup_dir, exist_ok=True)
        
        # Copy database file
        shutil.copy2(db_path, backup_path)
        
        # Verify backup
        with sqlite3.connect(backup_path) as conn:
            cursor = conn.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table'")
            table_count = cursor.fetchone()[0]
            print(f"Backup created successfully: {backup_path}")
            print(f"Tables backed up: {table_count}")
        
        return True
        
    except Exception as e:
        print(f"Backup failed: {e}")
        return False

def backup_data_files(data_dir: str, backup_dir: str):
    """Backup data files"""
    if not os.path.exists(data_dir):
        print(f"Data directory not found: {data_dir}")
        return False
    
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_subdir = os.path.join(backup_dir, f"data_backup_{timestamp}")
    
    try:
        shutil.copytree(data_dir, backup_subdir)
        print(f"Data files backed up to: {backup_subdir}")
        return True
        
    except Exception as e:
        print(f"Data backup failed: {e}")
        return False

def cleanup_old_backups(backup_dir: str, keep_days: int = 30):
    """Remove backups older than specified days"""
    if not os.path.exists(backup_dir):
        return
    
    cutoff_date = datetime.datetime.now() - datetime.timedelta(days=keep_days)
    removed_count = 0
    
    for filename in os.listdir(backup_dir):
        filepath = os.path.join(backup_dir, filename)
        if os.path.isfile(filepath):
            file_time = datetime.datetime.fromtimestamp(os.path.getmtime(filepath))
            if file_time < cutoff_date:
                os.remove(filepath)
                removed_count += 1
        elif os.path.isdir(filepath) and filename.startswith('data_backup_'):
            dir_time = datetime.datetime.fromtimestamp(os.path.getmtime(filepath))
            if dir_time < cutoff_date:
                shutil.rmtree(filepath)
                removed_count += 1
    
    if removed_count > 0:
        print(f"Cleaned up {removed_count} old backup files")

def main():
    parser = argparse.ArgumentParser(description='Backup ASTHA application data')
    parser.add_argument('--db-path', default='data/astha.db', help='Database file path')
    parser.add_argument('--data-dir', default='data/', help='Data directory path')
    parser.add_argument('--backup-dir', default='backups/', help='Backup directory path')
    parser.add_argument('--keep-days', type=int, default=30, help='Days to keep backups')
    parser.add_argument('--cleanup-only', action='store_true', help='Only cleanup old backups')
    
    args = parser.parse_args()
    
    if args.cleanup_only:
        cleanup_old_backups(args.backup_dir, args.keep_days)
        return
    
    print(f"Starting backup at {datetime.datetime.now()}")
    
    # Backup database
    db_success = backup_database(args.db_path, args.backup_dir)
    
    # Backup data files
    data_success = backup_data_files(args.data_dir, args.backup_dir)
    
    # Cleanup old backups
    cleanup_old_backups(args.backup_dir, args.keep_days)
    
    if db_success and data_success:
        print("✅ Backup completed successfully")
    else:
        print("❌ Backup completed with errors")

if __name__ == "__main__":
    main()
