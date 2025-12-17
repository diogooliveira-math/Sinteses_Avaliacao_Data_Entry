#!/usr/bin/env python3
"""
Test script to verify CLI behavior when database doesn't exist
"""
import sqlite3
import os
import tempfile
import shutil
from unittest import mock
from io import StringIO

# Import the functions from cli
from cli import build_and_run_query, main

def test_missing_database():
    """Test that the error occurs when database file doesn't exist"""
    print("Test 1: Missing database file")
    print("-" * 50)
    
    # Use a non-existent database path
    fake_db = "nonexistent_base.db"
    
    # Ensure it doesn't exist
    if os.path.exists(fake_db):
        os.remove(fake_db)
    
    try:
        result = build_and_run_query(
            db_path=fake_db,
            genero="M",
            assid=1,
            punt=1,
            part=1,
            inter=1,
            empen=1,
            diff=1
        )
        print(f"❌ FAILED: Expected error but got result: {result}")
    except sqlite3.OperationalError as e:
        print(f"✅ PASSED: Got expected error: {e}")
    except Exception as e:
        print(f"❌ FAILED: Got unexpected error: {type(e).__name__}: {e}")
    
    print()

def test_empty_database():
    """Test that the error occurs when database exists but table doesn't"""
    print("Test 2: Database exists but sinteses table missing")
    print("-" * 50)
    
    # Create a temporary database without the sinteses table
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
        temp_db = tmp.name
    
    try:
        # Create empty database (no tables)
        conn = sqlite3.connect(temp_db)
        conn.close()
        
        # Try to query
        try:
            result = build_and_run_query(
                db_path=temp_db,
                genero="M",
                assid=1,
                punt=1,
                part=1,
                inter=1,
                empen=1,
                diff=1
            )
            print(f"❌ FAILED: Expected error but got result: {result}")
        except sqlite3.OperationalError as e:
            if "no such table" in str(e):
                print(f"✅ PASSED: Got expected error: {e}")
            else:
                print(f"❌ FAILED: Got wrong OperationalError: {e}")
        except Exception as e:
            print(f"❌ FAILED: Got unexpected error: {type(e).__name__}: {e}")
    
    finally:
        # Cleanup - give it a moment for connections to close
        import time
        time.sleep(0.1)
        try:
            if os.path.exists(temp_db):
                os.remove(temp_db)
        except PermissionError:
            pass  # Windows may still have the file locked
    
    print()

def test_full_simulation():
    """Simulate the full CLI interaction that caused the error"""
    print("Test 3: Full CLI simulation with missing database")
    print("-" * 50)
    
    # Do not modify or backup existing base.db — backup feature removed
    db_existed = os.path.exists("base.db")
    
    try:
        # Mock user inputs matching the error scenario
        inputs = [
            "",      # Press enter to continue
            "M",     # Gender
            "y",     # Assíduo
            "y",     # Pontual
            "y",     # Participativo
            "y",     # Interesse
            "y",     # Empenho
            "y"      # Dificuldades
        ]
        
        with mock.patch('builtins.input', side_effect=inputs):
            try:
                main()
                print("❌ FAILED: Expected sqlite3.OperationalError but program completed")
            except sqlite3.OperationalError as e:
                if "no such table: sinteses" in str(e):
                    print(f"✅ PASSED: Got expected error: {e}")
                else:
                    print(f"⚠️  PARTIAL: Got OperationalError but different message: {e}")
            except Exception as e:
                print(f"❌ FAILED: Got unexpected error: {type(e).__name__}: {e}")
    
    finally:
        # No backup files created; nothing to restore
        pass
    
    print()

def test_with_correct_database():
    """Verify that it works when database is properly set up"""
    print("Test 4: Verify correct behavior with proper database")
    print("-" * 50)
    
    if not os.path.exists("base.db"):
        print("⚠️  SKIPPED: base.db doesn't exist. Run create_sqlite_db.py first.")
        print()
        return
    
    try:
        result = build_and_run_query(
            db_path="base.db",
            genero="M",
            assid=1,
            punt=1,
            part=1,
            inter=1,
            empen=1,
            diff=1
        )
        if result:
            print(f"✅ PASSED: Query returned result (length: {len(result)} chars)")
            print(f"Preview: {result[:100]}...")
        else:
            print("⚠️  WARNING: Query completed but no matching record found")
    except Exception as e:
        print(f"❌ FAILED: Unexpected error: {type(e).__name__}: {e}")
    
    print()

if __name__ == '__main__':
    print("=" * 50)
    print("CLI Error Simulation Tests")
    print("=" * 50)
    print()
    
    test_missing_database()
    test_empty_database()
    test_full_simulation()
    test_with_correct_database()
    
    print("=" * 50)
    print("Tests completed")
    print("=" * 50)
