# Issue Report: Locked Executable Preventing Rebuild

**Date:** 2025-12-17  
**Status:** 🔴 High  
**Severity:** High

---

## Problem Summary

Running `.uild.ps1` failed to fully clean and rebuild the `dist/` folder because `dist\sintese.exe` was locked by a running process. The script then either aborted or wrote an outdated alias into the PowerShell profile, causing the `s` alias to be missing or invalid.

## Error Message

Excerpt from the failed build run:

```
Remove-Item : Cannot remove item C:\Users\diogo\projects\Sinteses_Avaliacao_Data_Entry\dist\sintese.exe: Access is denied
...
PermissionError: [WinError 5] Access is denied: 'C:\Users\diogo\projects\Sinteses_Avaliacao_Data_Entry\dist\sintese.exe'
Error: Build failed!
```

## Root Cause Analysis

- The `dist\sintese.exe` file was still running (or otherwise locked) when the cleanup step attempted to remove the `dist/` folder.
- `Remove-Item -Recurse -Force` fails with access denied when the file is in use, and the script originally did not attempt to recover from this state.
- Because the build aborted or failed, the later steps that validate the executable and update the PowerShell profile were not reliably executed, leaving the `s` alias missing or pointing to a non-existent executable.

## Reproduction Steps

1. Build and run the application (or run an existing `dist\sintese.exe`).
2. Without closing the running application, re-run `.uild.ps1` from the project root.
3. Observe that the cleanup step fails with an access-denied error and the build aborts.

## Impact

- Developers cannot rebuild the application while an older instance is running.
- `s` alias may not be configured or may point to a missing executable, resulting in `s : The term 's' is not recognized...` or other alias errors.

## Solution Plan

1. Modify `build.ps1` cleanup to detect locked files and attempt to stop any running `sintese` process, retry removal, and then continue the build.
2. Add validation so the PowerShell profile is only updated when the executable exists.
3. Provide clear error messages when cleanup or build cannot succeed, rather than writing an invalid alias.

---

Filed by: build automation


