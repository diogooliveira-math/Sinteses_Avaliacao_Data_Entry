#!/usr/bin/env python3
import sqlite3
import os

# This script is a moved copy of the root-level `check_db.py`.
# It assumes the same working directory as the project root when run.

db_path = "base.db"
print(f"Database path: {db_path}")
print(f"Exists: {os.path.exists(db_path)}")

if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cur.fetchall()
    print(f"Tables: {tables}")
    
    if tables:
        for table in tables:
            table_name = table[0]
            cur.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cur.fetchone()[0]
            print(f"  - {table_name}: {count} rows")
    
    conn.close()
