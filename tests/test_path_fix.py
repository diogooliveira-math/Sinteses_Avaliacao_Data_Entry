#!/usr/bin/env python3
"""
Test the fixed cli.py to verify database path resolution works correctly
"""
import os
import sys
import shutil
from unittest import mock

# Add project directory to path
project_dir = r"C:\Users\diogo\AAA\Projects\Sinteses_Avaliacao_Data_Entry"
sys.path.insert(0, project_dir)

from cli import get_database_path, build_and_run_query, main

def test_database_path_resolution():
    """Test that get_database_path returns correct path"""
    print("=" * 60)
    print("Test 1: Database Path Resolution")
    print("=" * 60)
    
    db_path = get_database_path()
    print(f"\n✓ Resolved database path: {db_path}")
    
    # Check if it's an absolute path
    if os.path.isabs(db_path):
        print(f"✓ Path is absolute: YES")
    else:
        print(f"✗ Path is absolute: NO (This is a problem!)")
        return False
    
    # Check if database exists
    if os.path.exists(db_path):
        print(f"✓ Database file exists: YES")
    else:
        print(f"✗ Database file exists: NO at {db_path}")
        return False
    
    # Check if it ends with base.db
    if db_path.endswith("base.db"):
        print(f"✓ Path ends with 'base.db': YES")
    else:
        print(f"✗ Path ends with 'base.db': NO")
        return False
    
    print(f"\n✅ Database path resolution: PASSED\n")
    return True

def test_query_from_different_directory():
    """Test that query works when running from a different directory"""
    print("=" * 60)
    print("Test 2: Query from Different Directory")
    print("=" * 60)
    
    # Save current directory
    original_dir = os.getcwd()
    
    # Change to a different directory (user's home)
    test_dir = os.path.expanduser("~")
    os.chdir(test_dir)
    print(f"\n✓ Changed working directory to: {os.getcwd()}")
    
    try:
        db_path = get_database_path()
        print(f"✓ Resolved database path: {db_path}")
        
        # Try a query
        result = build_and_run_query(
            db_path=db_path,
            genero="M",
            assid=1,
            punt=1,
            part=1,
            inter=1,
            empen=1,
            diff=1
        )
        
        if result:
            print(f"✓ Query succeeded!")
            print(f"✓ Result length: {len(result)} characters")
            print(f"✓ Preview: {result[:80]}...")
            print(f"\n✅ Query from different directory: PASSED\n")
            return True
        else:
            print(f"✗ Query returned no results")
            print(f"\n❌ Query from different directory: FAILED\n")
            return False
            
    except Exception as e:
        print(f"✗ Query failed with error: {type(e).__name__}: {e}")
        print(f"\n❌ Query from different directory: FAILED\n")
        return False
    finally:
        # Restore original directory
        os.chdir(original_dir)

def test_full_cli_simulation():
    """Test full CLI flow with mocked inputs"""
    print("=" * 60)
    print("Test 3: Full CLI Simulation")
    print("=" * 60)
    
    # Change to a different directory
    original_dir = os.getcwd()
    test_dir = os.path.expanduser("~")
    os.chdir(test_dir)
    print(f"\n✓ Changed working directory to: {os.getcwd()}")
    
    try:
        # Mock user inputs
        inputs = [
            "",      # Press enter
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
                print(f"\n✅ Full CLI simulation: PASSED\n")
                return True
            except SystemExit as e:
                if e.code == 0:
                    print(f"\n✅ Full CLI simulation: PASSED (exited cleanly)\n")
                    return True
                else:
                    print(f"\n❌ Full CLI simulation: FAILED (exit code {e.code})\n")
                    return False
            except Exception as e:
                print(f"✗ CLI failed with error: {type(e).__name__}: {e}")
                print(f"\n❌ Full CLI simulation: FAILED\n")
                return False
    finally:
        os.chdir(original_dir)

if __name__ == '__main__':
    print("\n" + "=" * 60)
    print("TESTING DATABASE PATH FIX")
    print("=" * 60 + "\n")
    
    results = []
    
    # Run tests
    results.append(("Database Path Resolution", test_database_path_resolution()))
    results.append(("Query from Different Directory", test_query_from_different_directory()))
    results.append(("Full CLI Simulation", test_full_cli_simulation()))
    
    # Summary
    print("=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    for test_name, passed in results:
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{status} - {test_name}")
    
    total = len(results)
    passed_count = sum(1 for _, passed in results if passed)
    
    print(f"\nTotal: {passed_count}/{total} tests passed")
    
    if passed_count == total:
        print("\n🎉 ALL TESTS PASSED! The fix is working correctly.")
    else:
        print(f"\n⚠️  {total - passed_count} test(s) failed. Review the output above.")
    
    print("=" * 60)
