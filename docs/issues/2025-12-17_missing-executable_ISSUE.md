# Issue Report: Missing Executable

**Date:** 2025-12-17  
**Status:** 🔴 Critical  
**Severity:** Critical

---

## Problem Summary

The PowerShell alias `s` fails when attempting to execute `sintese.exe` because the executable doesn't exist at the expected path `C:\Users\diogo\AAA\Projects\Sinteses_Avaliacao_Data_Entry\dist\sintese.exe`.

## Error Message

```
PS C:\Users\diogo> s
& : The term 'C:\Users\diogo\AAA\Projects\Sinteses_Avaliacao_Data_Entry\dist\sintese.exe' is not recognized as the
name of a cmdlet, function, script file, or operable program. Check the spelling of the name, or if a path was
included, verify that the path is correct and try again.
At C:\Users\diogo\Documents\WindowsPowerShell\Microsoft.PowerShell_profile.ps1:5 char:7
+     & 'C:\Users\diogo\AAA\Projects\Sinteses_Avaliacao_Data_Entry\dist ...
+       ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : ObjectNotFound: (C:\Users\diogo\...ist\sintese.exe:String) [], CommandNotFoundException
    + FullyQualifiedName : CommandNotFoundException
```

## Root Cause Analysis

### Current Behavior

- PowerShell alias `s` is configured in the profile to run `sintese.exe`
- The executable file does not exist at `dist/sintese.exe`
- Users cannot use the `s` alias globally as intended

### Expected Behavior

- Running `s` from any PowerShell location should execute the Sintese CLI application
- The application should load with the correct database path

### Technical Details

The `build.ps1` script uses PyInstaller to compile `cli.py` into a standalone executable. This executable has not been created yet, either because:
1. The build process hasn't been run
2. The build process failed
3. The executable was deleted

### Why It Happens

1. Fresh installation or development environment
2. Build script not executed after project setup
3. Missing or incomplete build artifacts

### Affected Components

```
├── dist/
│   ├── sintese.exe (MISSING)
│   └── base.db
│
├── build.ps1 (builds the exe)
├── sintese.spec (PyInstaller configuration)
└── cli.py (source code to build)
```

## Reproduction Steps

1. Open PowerShell
2. Navigate to any directory (e.g., `PS C:\Users\diogo>`)
3. Run the command `s`
4. Observe the error message above

## Impact

- Users cannot use the global `s` alias
- The application cannot be launched from anywhere in the system
- Build artifacts are missing
- Development workflow is blocked

## Testing Evidence

Error occurs consistently when attempting to use the `s` alias from any PowerShell session.

## Solution Plan

Execute the build script to create the executable:
```powershell
.\build.ps1
```

This will:
1. Compile `cli.py` using PyInstaller
2. Generate `sintese.exe` in the `dist/` folder
3. Make the `s` alias functional
