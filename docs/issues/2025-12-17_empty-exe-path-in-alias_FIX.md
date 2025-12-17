# Fix Summary: Empty Executable Path in Alias

**Date:** 2025-12-17  
**Status:** ✅ RESOLVED  
**Issue:** Empty path in PowerShell alias causing execution failure

---

## Problem

The PowerShell profile contained an invalid alias with an empty executable path: `& '' @args`, causing the `s` command to fail with "The expression after '&' produced an object that was not valid."

## Root Cause

Two issues combined to cause this problem:

1. **PyInstaller launcher issue:** The `pyinstaller.exe` launcher had a hardcoded path to a different project ("Automation Data Entry"), preventing the build from completing
2. **Variable interpolation:** The `build.ps1` script wasn't properly capturing the `$ExePath` variable before writing it to the PowerShell profile

## Solution Implemented

### 1. Fixed PyInstaller Build Command

Changed from calling `pyinstaller.exe` directly to using `python -m PyInstaller`:

**Before:**
```powershell
& $PyInstallerExe $SpecFile --noconfirm
```

**After:**
```powershell
& $PythonExe -m PyInstaller $SpecFile --noconfirm
```

This avoids launcher issues and uses the correct Python interpreter.

### 2. Fixed Spec File Path

Changed from absolute path to relative path in `sintese.spec`:

**Before:**
```python
a = Analysis(
    ['C:\\Users\\diogo\\AAA\\Projects\\Sinteses_Avaliacao_Data_Entry\\cli.py'],
```

**After:**
```python
a = Analysis(
    ['cli.py'],
```

This makes the build more portable and prevents path resolution issues.

### 3. Fixed Variable Interpolation in Alias Code

Added proper variable expansion using `$($ExePath)` instead of `'$ExePath'`:

**Before:**
```powershell
& '$ExePath' @args  # Results in empty string
```

**After:**
```powershell
& '$($ExePath)' @args  # Properly expands the variable
```

### 4. Added Database File Copying

Added automatic copy of `base.db` to the `dist/` folder during build:

```powershell
$DbSource = Join-Path $ProjectRoot "base.db"
$DbDest = Join-Path $ProjectRoot "dist\base.db"
Copy-Item -Path $DbSource -Destination $DbDest -Force
```

## Code Changes

### File: `build.ps1`

**Changes:**
1. Line 50-53: Changed PyInstaller invocation to use Python module
2. Lines 69-72: Added database file copying
3. Added proper variable verification before profile update

### File: `sintese.spec`

**Changes:**
1. Line 5: Changed from absolute to relative path for `cli.py`

### File: `Microsoft.PowerShell_profile.ps1`

**Updated alias code:**
```powershell
function Invoke-Sintese {
    & 'C:\Users\diogo\AAA\Projects\Sinteses_Avaliacao_Data_Entry\dist\sintese.exe' @args
}
Set-Alias -Name sintese -Value Invoke-Sintese -Force
Set-Alias -Name s -Value Invoke-Sintese -Force
```

## Testing Results

✅ **All tests passing:**

1. **Build completes successfully:**
   ```
   [✓] PyInstaller executes without errors
   [✓] sintese.exe created in dist/
   [✓] base.db copied to dist/
   ```

2. **Alias works from any directory:**
   ```powershell
   PS C:\Users\diogo> s
   # ✅ Application launches successfully
   ```

3. **Application functions correctly:**
   ```
   Novo aluno? PRESS ENTER TO CONTINUE
   Qual o género do aluno (M/F): F
   ...
   Texto copiado para a área de transferência.
   # ✅ Full functionality working
   ```

## Files Modified

- `build.ps1` - Fixed PyInstaller command and added database copying
- `sintese.spec` - Changed to relative path for better portability
- `Microsoft.PowerShell_profile.ps1` - Updated with correct executable path

## Benefits

- ✅ `s` alias now works from any directory
- ✅ Build script executes successfully without errors
- ✅ Executable is properly created and functional
- ✅ Database file automatically deployed with build
- ✅ Better error messages if issues occur
- ✅ More portable build configuration

## Prevention

For future builds:
1. Use `python -m [module]` instead of calling .exe launchers directly
2. Use relative paths in config files when possible
3. Always verify variable expansion in PowerShell string interpolation
4. Test alias execution from different directories

## Status

**✅ RESOLVED** - All issues fixed, alias working correctly, application fully functional
