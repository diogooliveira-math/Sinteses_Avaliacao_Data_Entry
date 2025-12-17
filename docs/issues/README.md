# Issues & Fixes Documentation

This folder contains documentation for all issues encountered and their resolutions.

## Naming Convention

All issue documentation follows this naming pattern:

```
YYYY-MM-DD_brief-description_ISSUE.md
YYYY-MM-DD_brief-description_FIX.md
```

**Example:**
- `2025-12-17_database-path-resolution_ISSUE.md` - Problem report
- `2025-12-17_database-path-resolution_FIX.md` - Solution summary

## Issue Documentation Structure

### ISSUE.md Template

Each `_ISSUE.md` file should contain:

1. **Problem Summary** - Brief description of the issue
````markdown
# Issues & Fixes Documentation

This folder contains documentation for all issues encountered and their resolutions.

## Naming Convention

All issue documentation follows this naming pattern:

```
YYYY-MM-DD_brief-description_ISSUE.md
YYYY-MM-DD_brief-description_FIX.md
```

**Example:**
- `2025-12-17_database-path-resolution_ISSUE.md` - Problem report
- `2025-12-17_database-path-resolution_FIX.md` - Solution summary

## Issue Documentation Structure

### ISSUE.md Template

Each `_ISSUE.md` file should contain:

1. **Problem Summary** - Brief description of the issue
2. **Error Message** - Complete error output
3. **Root Cause Analysis** - Technical explanation
4. **Reproduction Steps** - How to reproduce the issue
5. **Impact** - What is affected
6. **Testing Evidence** - Proof of the problem
7. **Solution Plan** - Proposed approach

### FIX.md Template

Each `_FIX.md` file should contain:

1. **Problem** - Brief recap
2. **Root Cause** - One-line explanation
3. **Solution Implemented** - What was changed
4. **Code Changes** - Specific modifications
5. **Testing Results** - Verification tests
6. **Files Modified** - List of changed files
7. **Benefits** - Improvements gained
8. **Status** - Current state

## Quick Start - Documenting New Issues

### 1. Create Issue Report

```powershell
# In docs/issues/ folder
# Use today's date and descriptive name
YYYY-MM-DD_issue-name_ISSUE.md
```

### 2. Document the Problem

Use the template in `ISSUE_TEMPLATE.md`

### 3. Implement and Test Fix

Work through the solution...

### 4. Create Fix Summary

```powershell
# Same date and name as issue report
YYYY-MM-DD_issue-name_FIX.md
```

### 5. Update Main README

Add entry to the "Recent Issues" section in main `README.md`

## Issue Index

### 2025-12-17: Empty Executable Path in Alias
- **Issue:** [empty-exe-path-in-alias_ISSUE.md](2025-12-17_empty-exe-path-in-alias_ISSUE.md)
- **Fix:** [empty-exe-path-in-alias_FIX.md](2025-12-17_empty-exe-path-in-alias_FIX.md)
- **Status:** ✅ Resolved
- **Summary:** PowerShell alias contained empty path due to PyInstaller launcher issue and variable interpolation problem; resolved by using `python -m PyInstaller` and fixing variable expansion

### 2025-12-17: Locked Executable Preventing Rebuild
- **Issue:** [locked-executable_ISSUE.md](2025-12-17_locked-executable_ISSUE.md)
- **Fix:** [locked-executable_FIX.md](2025-12-17_locked-executable_FIX.md)
- **Status:** ✅ Resolved
- **Summary:** `dist\sintese.exe` could be locked by a running process, causing cleanup/remove to fail and the build to abort; `build.ps1` now attempts to stop running `sintese` processes and retries removal, and only writes alias when the executable exists.

### 2025-12-17: Missing Executable
- **Issue:** [missing-executable_ISSUE.md](2025-12-17_missing-executable_ISSUE.md)
- **Fix:** [missing-executable_FIX.md](2025-12-17_missing-executable_FIX.md)
- **Status:** ✅ Resolved
- **Summary:** PowerShell alias `s` failed because `sintese.exe` didn't exist in `dist/` folder; resolved by running `build.ps1`

### 2025-12-17: Database Path Resolution
- **Issue:** [database-path-resolution_ISSUE.md](2025-12-17_database-path-resolution_ISSUE.md)
- **Fix:** [database-path-resolution_FIX.md](2025-12-17_database-path-resolution_FIX.md)
- **Status:** ✅ Resolved
- **Summary:** Executable couldn't find database when run from different directories via PowerShell alias

### 2025-12-17: Backup Creation Failure
- **Issue:** [backup-creation_ISSUE.md](2025-12-17_backup-creation_ISSUE.md)
- **Fix:** [backup-creation_FIX.md](2025-12-17_backup-creation_FIX.md)
- **Status:** ✅ Resolved
- **Summary:** `backup_json()` could fail silently when copying `base.json`; replaced manual read/write with `shutil.copy2()` and improved error messages.

---

## Tips for Good Documentation

✅ **DO:**
- Be specific and detailed
- Include code snippets and error messages
- Document testing procedures
- Link related files
- Update the index above

❌ **DON'T:**
- Use vague descriptions
- Skip reproduction steps
- Forget to document the fix
- Leave status unclear

## Statistics

- **Total Issues:** 2
- **Resolved:** 2
- **Open:** 0
- **In Progress:** 0

---

**Last Updated:** December 17, 2025

````
