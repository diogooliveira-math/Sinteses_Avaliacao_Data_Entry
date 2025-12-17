# Issue Report: Empty Executable Path in Alias

**Date:** 2025-12-17  
**Status:** 🔴 Critical  
**Severity:** Critical

---

## Problem Summary

The `build.ps1` script runs but fails to create a valid alias. The PowerShell profile is written with an empty executable path, causing the alias to be invalid and produce the error: "The expression after '&' in a pipeline element produced an object that was not valid."

## Error Message

```
PS C:\Users\diogo> s
The expression after '&' in a pipeline element produced an object that was not valid. It must result in a command
name, a script block, or a CommandInfo object.
At C:\Users\diogo\Documents\WindowsPowerShell\Microsoft.PowerShell_profile.ps1:7 char:7
+     & '' @args
+       ~~
    + CategoryInfo          : InvalidOperation: (:String) [], RuntimeException
    + FullyQualifiedName : BadExpression
```

## Root Cause Analysis

### Current Behavior

- `build.ps1` runs without obvious errors
- PowerShell profile is updated but contains: `& '' @args` (empty path)
- The alias function `Invoke-Sintese` tries to execute an empty string
- Calling `s` results in a runtime error

### Expected Behavior

- PowerShell profile should contain the full path to `sintese.exe`
- The alias should execute: `& 'C:\Users\diogo\AAA\Projects\Sinteses_Avaliacao_Data_Entry\dist\sintese.exe' @args`

### Technical Details

The issue is in `build.ps1` at the alias code block generation. The `$ExePath` variable is being set but appears to be empty when the code block is created. This could be due to:

1. The PyInstaller build is failing silently
2. Variable scope issues in the string interpolation
3. The path to the executable is not being captured correctly

### Why It Happens

1. Variable `$ExePath` is calculated but may not contain a valid path
2. The string interpolation in the `@"` ... `"@` block may not be evaluating the variable correctly
3. The build process may be completing with exit code 0 even if the executable wasn't created

### Affected Components

```
├── build.ps1 (has variable capture issue)
├── PowerShell profile (contains invalid alias)
└── dist/sintese.exe (may not be created by PyInstaller)
```

## Reproduction Steps

1. Run `.\build.ps1`
2. Check the PowerShell profile with `cat $PROFILE`
3. Observe the function contains `& '' @args` instead of actual path
4. Try to run `s`
5. Get the error above

## Impact

- The alias is completely broken
- Users cannot execute the application
- Build appears successful but actually fails
- Misleading user feedback from the build script

## Testing Evidence

Profile content shows:
```powershell
function Invoke-Sintese {
    & '' @args
}
```

Instead of:
```powershell
function Invoke-Sintese {
    & 'C:\Users\diogo\AAA\Projects\Sinteses_Avaliacao_Data_Entry\dist\sintese.exe' @args
}
```

## Solution Plan

1. Debug the `build.ps1` script to identify why `$ExePath` is empty
2. Verify PyInstaller build is actually creating the executable
3. Fix variable scope or interpolation in the alias code block
4. Add better error checking and validation
