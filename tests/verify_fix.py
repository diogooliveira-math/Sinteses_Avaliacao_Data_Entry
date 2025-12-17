#!/usr/bin/env python3
"""
Verification test for the database path resolution fix.
This test simulates the exact error scenario from the issue report.
"""
import sys
import os

def test_original_issue():
    """
    Reproduce and verify the fix for the original issue.
    """
    print("=" * 70)
    print("VERIFICATION TEST: Original Issue Reproduction")
    print("=" * 70)
    
    print("\n📋 Original Issue:")
    print("   Error: sqlite3.OperationalError: no such table: sinteses")
    print("   When: Running executable from PowerShell alias from different directory")
    print("   Cause: Database path resolution using relative path")
    
    print("\n🔍 Testing the fix...")
    
    # Add project to path
    project_dir = r"C:\Users\diogo\AAA\Projects\Sinteses_Avaliacao_Data_Entry"
    sys.path.insert(0, project_dir)
    
    from cli import get_database_path, build_and_run_query
    
    # Test 1: Verify database path resolution
    print("\n✓ Test 1: Database Path Resolution")
    db_path = get_database_path()
    if not os.path.exists(db_path):
        print(f"  ✗ FAILED: Database not found at {db_path}")
        return False
    print(f"  ✓ Database found: {db_path}")
    
    # Test 2: Verify database has the sinteses table
    print("\n✓ Test 2: Database Table Access")
    try:
        result = build_and_run_query(
            db_path=db_path,
            genero="F",
            assid=0,
            punt=0,
            part=0,
            inter=0,
            empen=0,
            diff=0
        )
        if result:
            print(f"  ✓ Query executed successfully")
            print(f"  ✓ Found matching text: {result[:50]}...")
        else:
            print(f"  ✓ Query executed (no matching criteria)")
    except Exception as e:
        print(f"  ✗ FAILED: {e}")
        return False
    
    # Test 3: Verify from different working directory
    print("\n✓ Test 3: Query from Different Working Directory")
    original_dir = os.getcwd()
    try:
        os.chdir(os.path.expanduser("~"))
        print(f"  ✓ Changed to: {os.getcwd()}")
        
        db_path = get_database_path()
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
            print(f"  ✓ Query successful from different directory")
        else:
            print(f"  ✓ Query executed (no matching criteria)")
    finally:
        os.chdir(original_dir)
    
    print("\n" + "=" * 70)
    print("✅ VERIFICATION COMPLETE: Issue is RESOLVED")
    print("=" * 70)
    print("\n📝 Summary:")
    print("   ✓ Database found correctly")
    print("   ✓ Sinteses table accessible")
    print("   ✓ Queries execute from any directory")
    print("   ✓ Original error is FIXED")
    print("\n" + "=" * 70)
    
    return True

if __name__ == "__main__":
    success = test_original_issue()
    sys.exit(0 if success else 1)
