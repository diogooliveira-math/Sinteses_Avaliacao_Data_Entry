# Fix Summary: Database Path Resolution Issue

**Date:** December 17, 2025  
**Status:** ✅ RESOLVED  
**Issue:** `sqlite3.OperationalError: no such table: sinteses` when running from PowerShell alias

---

## Problem

When running `sintese.exe` from the PowerShell alias (`s`) from any directory, the application crashed with:

```
sqlite3.OperationalError: no such table: sinteses
```

This occurred because:
1. The application was using `db_path = "base.db"` (relative path)
2. When invoked via PowerShell alias from `C:\Users\diogo>`, the working directory was the home folder, not the dist folder
3. The relative path resolved to `C:\Users\diogo\base.db` instead of `C:\...\dist\base.db`

---

## Root Cause

The `find_resource()` function in [cli.py](cli.py) had an incorrect priority order:
- For executables, it was checking the CWD before the app directory
- This meant when run from any directory, it looked for the database in the wrong place

---

## Solution Implemented

### Updated `find_resource()` Function

The priority order was corrected in [cli.py](cli.py#L24-L67) to:

**For frozen executables (compiled with PyInstaller):**
1. Environment variable `SINT_BASE_DIR` (if set)
2. **Application directory (executable location)** ← PRIORITIZED
3. Parent of application directory

**For Python scripts:**
1. Environment variable `SINT_BASE_DIR` (if set)
2. Current working directory (only if file exists there)
3. Application directory (script location)
4. Parent of application directory

### Key Changes

```python
# For frozen executables, prioritize app dir to work from any CWD
if is_frozen:
    p = os.path.join(app_dir, name)
    if os.path.exists(p):
        return os.path.abspath(p)
else:
    # For scripts, check CWD only if it actually has the file
    p = os.path.join(os.getcwd(), name)
    if os.path.exists(p):
        return os.path.abspath(p)

# Fallback to app directory
p = os.path.join(app_dir, name)
if os.path.exists(p):
    return os.path.abspath(p)
```

---

## Files Modified

- [cli.py](cli.py) - Updated `find_resource()` function (lines 24-67)

---

## Testing Results

✅ **Test 1: Database Path Resolution** - PASSED
- Correctly resolves to absolute path: `C:\Users\diogo\AAA\Projects\Sinteses_Avaliacao_Data_Entry\base.db`
- Detects file exists
- Returns proper absolute path

✅ **Test 2: Query from Different Directory** - PASSED
- Changed working directory to `C:\Users\diogo`
- Successfully found database
- Query executed and returned results

---

## Verification Steps

From any directory, the executable now works:

```powershell
# From user home directory
PS C:\Users\diogo> s
Novo aluno? PRESS ENTER TO CONTINUE
Qual o género do aluno (M/F): F
...
✓ Texto encontrado e copiado para a área de transferência
```

---

## How the Fix Works

1. When `sintese.exe` runs, `sys.frozen = True` (PyInstaller sets this)
2. The `find_resource()` function checks `is_frozen`
3. For frozen executables, it prioritizes the app directory (where .exe is located)
4. The database is found in `dist\base.db` regardless of CWD
5. Query executes successfully

---

## Environment Variable Override

For advanced use cases, users can set `SINT_BASE_DIR` to specify a custom location:

```powershell
$env:SINT_BASE_DIR = "C:\Custom\Path"
s  # Will now look for base.db in C:\Custom\Path
```

---

## Distribution

When distributing the application:
- ✅ Both `sintese.exe` and `base.db` must be in the same folder (dist/)
- ✅ Users can place the dist folder anywhere
- ✅ PowerShell alias works from any directory
- ✅ No additional configuration needed

---

## Build & Deploy

1. Updated source: [cli.py](cli.py)
2. Rebuilt executable:
   ```powershell
   python -m PyInstaller --noconfirm sintese.spec
   ```
3. Verified both files in `dist/`:
   - `sintese.exe` (13.4 MB)
   - `base.db` (32 KB)

