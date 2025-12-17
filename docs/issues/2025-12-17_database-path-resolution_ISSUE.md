# Issue Report: Database Path Resolution in Executable

**Date:** December 17, 2025  
**Status:** 🔴 Critical - Prevents executable from functioning  
**Severity:** High - Executable unusable from PowerShell alias

---

## Problem Summary

The compiled `sintese.exe` executable fails with `sqlite3.OperationalError: no such table: sinteses` when invoked from any directory other than its own location. The Python script version (`python cli.py`) works correctly.

## Error Message

```
PS C:\Users\diogo> s
Novo aluno? PRESS ENTER TO CONTINUE
Qual o género do aluno (M/F): M
O aluno é assíduo? (y/n): y
O aluno é pontual? (y/n): y
O aluno é participativo? (y/n): y
O aluno mostra interesse? (y/n): y
O aluno mostra empenho? (y/n): y
O aluno mostra dificuldades? (y/n): y
Traceback (most recent call last):
  File "cli.py", line 101, in <module>
  File "cli.py", line 87, in main
  File "cli.py", line 71, in build_and_run_query
sqlite3.OperationalError: no such table: sinteses
[PYI-28256:ERROR] Failed to execute script 'cli' due to unhandled exception!
```

## Root Cause Analysis

### Current Code Issue

In [cli.py](cli.py#L78):
```python
def main():
    press_enter_prompt()
    db_path = "base.db"  # ⚠️ RELATIVE PATH - This is the problem!
    ...
```

### The Problem

1. **Relative path behavior:**
   - `db_path = "base.db"` resolves relative to the **current working directory (CWD)**
   - When running from `C:\Users\diogo>`, it looks for `C:\Users\diogo\base.db`
   - The actual database is at `C:\Users\diogo\AAA\Projects\Sinteses_Avaliacao_Data_Entry\dist\base.db`

2. **Why it happens:**
   - PowerShell alias: `s` → `C:\...\dist\sintese.exe`
   - User runs from: `C:\Users\diogo>`
   - Executable CWD: `C:\Users\diogo>` (not the dist folder)
   - Database lookup fails

3. **Why Python script worked:**
   - Was likely run from the project directory
   - CWD was `C:\Users\diogo\AAA\Projects\Sinteses_Avaliacao_Data_Entry`
   - Relative path found the database

### File Structure

```
dist/
├── sintese.exe         ← The executable
└── base.db             ← Database is HERE

Current Working Directory when user runs 's':
C:\Users\diogo\         ← Executable looks for base.db HERE (doesn't exist!)
```

## Reproduction Steps

1. ✅ Have `sintese.exe` and `base.db` in `dist/` folder
2. ✅ Set PowerShell alias: `s` → full path to `sintese.exe`
3. ✅ Navigate to any other directory: `cd C:\Users\diogo`
4. ✅ Run: `s`
5. ❌ Error occurs: `no such table: sinteses`

## Impact

- **User Experience:** Alias is completely broken
- **Usability:** Executable only works when run from `dist/` folder
- **Distribution:** Cannot share the tool with others reliably

## Testing Evidence

The test suite ([test_cli.py](test_cli.py)) confirmed:
- ✅ Database structure is correct
- ✅ Python script works with correct database
- ✅ Error occurs when database is missing/wrong location
- ✅ Error matches the reported issue exactly

---

## Solution Plan

### Strategy

Fix the path resolution to make it **executable-aware** instead of CWD-dependent.

### Approach Options

**Option A: Bundle database inside executable (PyInstaller)**
- ❌ Requires database updates to be redistributed
- ❌ Can't modify data without recompiling

**Option B: Resolve path relative to executable location** ✅ RECOMMENDED
- ✅ Database stays alongside executable
- ✅ Works from any directory
- ✅ Easy to update database independently
- ✅ Portable - copy folder anywhere

**Option C: Environment variable for database path**
- ⚠️ Extra setup required
- ⚠️ User configuration complexity

### Selected Solution: Option B

Modify `cli.py` to:
1. Detect if running as PyInstaller executable or Python script
2. Resolve `base.db` path relative to executable/script location
3. Maintain backward compatibility

## Implementation Details

### Code Changes Required

**File:** [cli.py](cli.py#L78)

**Current:**
```python
def main():
    press_enter_prompt()
    db_path = "base.db"
```

**New:**
```python
import sys
import os

def get_database_path():
    """Get the absolute path to base.db relative to the executable/script."""
    if getattr(sys, 'frozen', False):
        # Running as PyInstaller executable
        application_path = os.path.dirname(sys.executable)
    else:
        # Running as Python script
        application_path = os.path.dirname(os.path.abspath(__file__))
    
    return os.path.join(application_path, "base.db")

def main():
    press_enter_prompt()
    db_path = get_database_path()
```

### Additional Improvements

1. **Error handling:** Check if database exists before querying
2. **User-friendly message:** Guide user if database is missing
3. **Spec file update:** Ensure `base.db` is packaged/copied correctly

## Testing Plan

1. **Test Python script:**
   - Run from project root
   - Run from other directories
   - Verify database path resolution

2. **Test compiled executable:**
   - Run from `dist/` folder
   - Run from user home directory (alias scenario)
   - Run from completely different path
   - Verify database is found in all cases

3. **Test edge cases:**
   - Missing database file
   - Read-only directory
   - Network path (if applicable)

## Rollout Steps

1. ✅ Update `cli.py` with new path resolution logic
2. ✅ Add error handling for missing database
3. ✅ Test with Python script
4. ✅ Rebuild executable with PyInstaller
5. ✅ Test executable from various directories
6. ✅ Verify alias functionality
7. ✅ Update documentation

---

## Success Criteria

- ✅ Executable runs successfully from any directory
- ✅ PowerShell alias `s` works globally
- ✅ Database is found automatically
- ✅ User-friendly error if database is missing
- ✅ Python script backward compatible

## Priority

**HIGH** - This blocks the primary use case (global alias usage)

---

**Next Action:** Implement the fix in cli.py
