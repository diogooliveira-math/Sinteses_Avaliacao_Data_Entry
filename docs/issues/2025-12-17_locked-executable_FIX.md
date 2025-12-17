# Fix Summary: Locked Executable Preventing Rebuild

**Date:** 2025-12-17  
**Status:** ✅ RESOLVED  
**Issue:** Locked executable prevented `dist/` cleanup and caused alias failures

---

## Problem

`dist\sintese.exe` was locked by a running process. `build.ps1` failed to remove the `dist/` folder, causing the PyInstaller build to fail and leaving the PowerShell alias unconfigured or pointing to a non-existent executable.

## Root Cause

- `Remove-Item` failed when the executable was in use; the cleanup step lacked a recovery strategy.
- The build aborted before verifying the executable existed, so the profile update step could be skipped or left inconsistent.

## Solution Implemented

Changes applied to `build.ps1`:

- Cleanup retry: If `Remove-Item` fails, the script now attempts to find and stop any running `sintese` processes (`Get-Process -Name sintese`) and retries removal.
- Validation: The script now verifies `dist\sintese.exe` exists before writing the alias into the PowerShell profile; if the executable is missing the profile is not modified and a clear error is shown.
- Robust logging: Improved messages during cleanup and build so users see why a step failed.
- Minor quoting fix for safer `Write-Host` output.

## Files Modified

- `build.ps1` — Added cleanup retry and validation logic.

## Testing Results

- Ran `.uild.ps1` while `dist\sintese.exe` was previously running. The script stopped the running process, removed the `dist/` folder, rebuilt the executable, copied `base.db`, updated the PowerShell profile, and loaded the alias into the current session.

Validation:

- `dist\sintese.exe` exists after the build.
- `s` and `sintese` aliases work from other directories in PowerShell.

## Benefits

- Developers can rebuild without manually closing the running app.
- The profile is only updated when the executable is present—no invalid alias is written.
- Clearer error output helps triage other build failures.

Status: ✅ RESOLVED

Maintainer: build automation
