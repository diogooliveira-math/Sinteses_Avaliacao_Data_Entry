# Comprehensive Guide: Building and Deploying Sintese CLI

## Table of Contents
1. [Overview](#overview)
2. [The Build Process](#the-build-process)
3. [Components Explained](#components-explained)
4. [System Modifications](#system-modifications)
5. [File Structure](#file-structure)
6. [Usage Instructions](#usage-instructions)
7. [Troubleshooting](#troubleshooting)

---

## Overview

This guide explains the automated build process for converting the `cli.py` Python script into a standalone Windows executable (`sintese.exe`) and setting up convenient aliases for seamless execution.

### What Was Done
1. ✅ Created an automated build script (`build.ps1`)
2. ✅ Configured PyInstaller to bundle Python code into a single executable
3. ✅ Set up PowerShell aliases (`sintese` and `s`) for easy access
4. ✅ Modified your PowerShell profile for persistent alias availability

---

## The Build Process

### How to Build the Executable

Simply run this command from the project directory:

```powershell
.\build.ps1
```

This single command will:
- Verify your Python environment
- Check/install PyInstaller
- Clean previous build artifacts
- Build a new executable
- Configure PowerShell aliases
- Load the aliases into your current session

### What Happens Behind the Scenes

The build process follows 5 main steps:

#### Step 1: Environment Verification
- **Purpose**: Ensures the Python virtual environment exists
- **Location**: `.venv/` directory in your project
- **Why**: The virtual environment contains all necessary Python packages (PyInstaller, pyperclip, etc.) isolated from your system Python

#### Step 2: PyInstaller Check
- **Purpose**: Verifies PyInstaller is installed
- **Action**: Auto-installs if missing
- **Why**: PyInstaller is the tool that converts Python scripts into standalone executables

#### Step 3: Clean Previous Builds
- **Purpose**: Removes old `build/` and `dist/` directories
- **Why**: Ensures a fresh build without conflicts from previous versions
- **Safety**: Prevents accumulation of outdated artifacts

#### Step 4: Executable Creation
- **Purpose**: Converts `cli.py` into `sintese.exe`
- **How**: Uses the `sintese.spec` configuration file
- **Output**: Single executable file in `dist/sintese.exe`

#### Step 5: Alias Configuration
- **Purpose**: Sets up convenient shortcuts to run the executable
- **Where**: Modifies your PowerShell profile
- **Result**: You can type `sintese` or `s` instead of the full path

---

## Components Explained

### 1. `cli.py` - The Source Application

**What it is**: Your original Python script for student assessment synthesis.

**Purpose**: 
- Prompts user for student characteristics
- Queries a SQLite database (`base.db`)
- Returns matching assessment text
- Copies result to clipboard

**Dependencies**:
- `sqlite3` (built-in to Python)
- `pyperclip` (for clipboard operations)
- `tkinter` (fallback for clipboard, included with Python on Windows)

### 2. `sintese.spec` - PyInstaller Configuration

**What it is**: A specification file that tells PyInstaller how to build your executable.

**Key settings explained**:

```python
a = Analysis(
    ['C:\\Users\\diogo\\...\\cli.py'],  # Your source script
    pathex=[],                           # Additional import paths (none needed)
    binaries=[],                         # External binaries (none needed)
    datas=[],                            # Data files (none needed)
    hiddenimports=[],                    # Imports PyInstaller might miss
)
```

```python
exe = EXE(
    ...
    name='sintese',          # Output filename (becomes sintese.exe)
    console=True,            # Shows console window (needed for interactive prompts)
    upx=True,                # Compresses the executable (smaller file size)
)
```

**Why this file exists**: Pre-configured settings ensure consistent, optimal builds without remembering complex command-line arguments.

### 3. `build.ps1` - Automated Build Script

**What it is**: A PowerShell script that automates the entire build and deployment process.

**Key functions**:

#### Function: Environment Detection
```powershell
$VenvPath = Join-Path $ProjectRoot ".venv"
```
- Locates your virtual environment
- Ensures all commands use the correct Python installation

#### Function: Build Cleaning
```powershell
Remove-Item -Path $path -Recurse -Force
```
- Deletes old build artifacts
- Prevents version confusion

#### Function: Executable Creation
```powershell
& $PyInstallerExe $SpecFile --noconfirm
```
- Runs PyInstaller with your spec file
- `--noconfirm` overwrites without prompting

#### Function: Alias Injection
```powershell
function Invoke-Sintese {
    & '$ExePath' @args
}
Set-Alias -Name sintese -Value Invoke-Sintese -Force
```
- Creates a function that calls your executable
- Sets up two aliases: `sintese` and `s`
- `@args` passes all arguments to the executable

### 4. PowerShell Profile

**What it is**: A special script file that runs automatically when you open PowerShell.

**Location**: 
```
C:\Users\diogo\Documents\WindowsPowerShell\Microsoft.PowerShell_profile.ps1
```
or
```
C:\Users\diogo\Documents\PowerShell\Microsoft.PowerShell_profile.ps1
```
(Depends on PowerShell version)

**What was added**:
```powershell
# ===== Sintese CLI Alias =====
function Invoke-Sintese {
    & 'C:\Users\diogo\AAA\Projects\Sinteses_Avaliacao_Data_Entry\dist\sintese.exe' @args
}
Set-Alias -Name sintese -Value Invoke-Sintese -Force
Set-Alias -Name s -Value Invoke-Sintese -Force
# ==============================
```

**Why this matters**:
- Makes the aliases available in **all** future PowerShell sessions
- No need to navigate to the project directory to use the tool
- Works from anywhere in your system

---

## System Modifications

### Files Created

| File | Location | Purpose |
|------|----------|---------|
| `build.ps1` | Project root | Automated build script |
| `sintese.exe` | `dist/` folder | Standalone executable |
| Profile additions | `$PROFILE` | Persistent alias configuration |

### Directories Created/Modified

| Directory | Purpose | Persistent? |
|-----------|---------|-------------|
| `build/` | Temporary build files | No (cleaned each build) |
| `dist/` | Final executable output | Yes (contains your exe) |

### System-Wide Changes

#### 1. PowerShell Profile Modification
- **File**: Your PowerShell profile (`$PROFILE`)
- **Change**: Added alias configuration block
- **Impact**: Aliases load automatically in new PowerShell sessions
- **Reversible**: Yes, edit/remove the marked section in your profile

#### 2. No Registry Changes
- The solution does NOT modify Windows Registry
- Does NOT add to system PATH
- Does NOT create Start Menu shortcuts
- Clean, non-invasive approach

---

## File Structure

### Before Build
```
Sinteses_Avaliacao_Data_Entry/
├── .venv/                    # Python virtual environment
├── base.db                   # SQLite database
├── base.json                 # Source data
├── cli.py                    # ⭐ Source Python script
├── sintese.spec              # ⭐ PyInstaller config
├── build.ps1                 # ⭐ Build automation script
├── create_sqlite_db.py       # Database creation script
└── ...
```

### After Build
```
Sinteses_Avaliacao_Data_Entry/
├── .venv/
├── base.db                   # ⚠️ Must be in same folder as exe!
├── base.json
├── cli.py
├── sintese.spec
├── build.ps1
├── build/                    # 🔨 Temporary build files
│   └── sintese/
├── dist/                     # 📦 Final output
│   └── sintese.exe          # ⭐⭐⭐ Your executable!
└── ...
```

**Important Notes**:
- The executable expects `base.db` to be in the same directory where you run it
- By default, it looks for `base.db` in the current working directory
- The alias/function helps ensure you run it from the correct location

---

## Usage Instructions

### Method 1: Using the Alias (Recommended)

From **any** PowerShell window, simply type:

```powershell
sintese
```

or the shorter version:

```powershell
s
```

### Method 2: Direct Execution

Navigate to the project folder and run:

```powershell
.\dist\sintese.exe
```

### Method 3: From File Explorer

Double-click `sintese.exe` in the `dist/` folder.

**Note**: If double-clicking, make sure `base.db` is in the same folder as the executable.

---

## How the Alias Works

### The Mechanism

When you type `sintese` in PowerShell:

1. PowerShell loads your profile (if not already loaded)
2. Profile contains the `Invoke-Sintese` function
3. The alias `sintese` redirects to `Invoke-Sintese`
4. Function executes: `& 'C:\...\dist\sintese.exe' @args`
5. Your application runs with any provided arguments

### Why Use a Function Instead of Direct Alias?

```powershell
# ❌ This won't work with arguments:
Set-Alias sintese "C:\...\sintese.exe"

# ✅ This works with arguments:
function Invoke-Sintese { & 'C:\...\sintese.exe' @args }
Set-Alias sintese Invoke-Sintese
```

**Reason**: PowerShell aliases can't directly accept arguments. The function wrapper enables argument passing with `@args`.

---

## Understanding PyInstaller

### What PyInstaller Does

1. **Analyzes** your Python script to find all dependencies
2. **Bundles** the Python interpreter, your code, and all imported modules
3. **Packages** everything into a single executable file
4. **Creates** a bootloader that extracts and runs everything

### Single-File vs Directory Mode

Your build uses **single-file mode** (`onefile`):

**Advantages**:
- ✅ One portable file
- ✅ Easy to distribute
- ✅ Clean deployment

**How it works**:
1. When you run `sintese.exe`, it extracts contents to a temporary folder
2. Runs the Python code from there
3. Cleans up when finished

### Why the Executable is Large

Even a simple Python script becomes 20-30+ MB because it includes:
- Python interpreter (~15 MB)
- Standard library modules
- PyInstaller bootloader
- Your imported packages (sqlite3, tkinter, pyperclip)

This is normal and expected.

---

## Troubleshooting

### Issue: "Alias not found"

**Symptoms**: Typing `sintese` gives "command not found" error

**Solutions**:
1. Reload your profile:
   ```powershell
   . $PROFILE
   ```

2. Check if profile loaded correctly:
   ```powershell
   Get-Alias sintese
   ```

3. Manually run the build script again:
   ```powershell
   .\build.ps1
   ```

### Issue: "Execution Policy" Error

**Symptoms**: Cannot run `build.ps1` or profile scripts

**Solution**:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**Why**: Windows blocks unsigned scripts by default. This command allows locally created scripts to run.

### Issue: Database Not Found

**Symptoms**: Program runs but says "unable to open database file"

**Cause**: The executable looks for `base.db` in the current working directory

**Solutions**:

1. **Option A**: Always use the alias (it handles paths correctly)
   ```powershell
   sintese
   ```

2. **Option B**: Run from project directory
   ```powershell
   cd C:\Users\diogo\AAA\Projects\Sinteses_Avaliacao_Data_Entry
   .\dist\sintese.exe
   ```

3. **Option C**: Modify `cli.py` to use absolute path:
   ```python
   import os
   script_dir = os.path.dirname(os.path.abspath(__file__))
   db_path = os.path.join(script_dir, "base.db")
   ```
   Then rebuild.

### Issue: Antivirus Quarantines Executable

**Symptoms**: Antivirus flags or deletes `sintese.exe`

**Cause**: PyInstaller executables sometimes trigger false positives

**Solutions**:
1. Add `dist/sintese.exe` to antivirus exceptions
2. Add `C:\Users\diogo\AAA\Projects\` to trusted folders
3. Use `--debug` mode to diagnose (see advanced options)

### Issue: Changes to cli.py Not Reflected

**Symptoms**: Modified code but executable behavior unchanged

**Cause**: Forgot to rebuild after changing source code

**Solution**:
```powershell
.\build.ps1
```

Always rebuild after any changes to `cli.py`!

---

## Advanced Topics

### Rebuilding After Code Changes

Whenever you modify `cli.py`, you must rebuild:

```powershell
.\build.ps1
```

The script automatically:
- Cleans old build
- Creates new executable
- Updates alias paths

### Distributing the Executable

To share with others:

1. **Copy these files**:
   - `dist/sintese.exe`
   - `base.db`

2. **Place in same folder** on target machine

3. **No Python installation needed** on target machine

4. **Optional**: Create a batch file for easier execution:
   ```batch
   @echo off
   sintese.exe
   pause
   ```
   Save as `run_sintese.bat` in the same folder.

### Customizing the Spec File

Edit `sintese.spec` to:

**Add data files**:
```python
datas=[('base.db', '.')],  # Include database in exe
```

**Hide console window**:
```python
console=False,  # For GUI apps only
```

**Add an icon**:
```python
icon='icon.ico',
```

**Include hidden imports**:
```python
hiddenimports=['pyperclip'],
```

After modifying, rebuild with `.\build.ps1`.

### Uninstalling/Removing

To completely remove:

1. **Delete build artifacts**:
   ```powershell
   Remove-Item -Path build, dist -Recurse -Force
   ```

2. **Remove alias from profile**:
   ```powershell
   notepad $PROFILE
   ```
   Delete the section marked "Sintese CLI Alias"

3. **Reload profile**:
   ```powershell
   . $PROFILE
   ```

No other system changes to revert!

---

## Summary of What Changed

### ✅ Files Added to Project
- `build.ps1` - Automated build script
- `BUILD_GUIDE.md` - This comprehensive guide
- `dist/sintese.exe` - Your executable (regenerated on each build)
- `build/` folder - Temporary files (cleaned on each build)

### ✅ System-Level Modifications
- **PowerShell Profile** (`$PROFILE`):
  - Added `Invoke-Sintese` function
  - Added `sintese` alias
  - Added `s` alias shortcut
  - All changes marked with comments for easy identification

### ❌ Not Modified
- Windows Registry - Untouched
- System PATH - Unchanged
- Start Menu - No shortcuts added
- File associations - None created
- Other applications - Unaffected

### 🔄 Reversible Changes
Everything can be undone by:
1. Deleting build artifacts
2. Removing the marked section from PowerShell profile

---

## Why This Approach?

### Benefits of This Solution

1. **Fully Automated**: Single command builds everything
2. **Non-Invasive**: Minimal system modifications
3. **Portable**: Executable works on any Windows machine
4. **Convenient**: Aliases work from anywhere
5. **Maintainable**: Easy to rebuild after code changes
6. **Professional**: Clean, organized structure
7. **Documented**: Comprehensive guide for future reference

### Design Decisions Explained

| Decision | Rationale |
|----------|-----------|
| PowerShell script | Native to Windows, no additional tools needed |
| Profile modification | Persistent aliases without complex setup |
| Single-file executable | Easy distribution, one file to manage |
| Marked sections in profile | Easy to identify and remove later |
| Build cleaning | Prevents version conflicts |
| Virtual environment | Isolated, reproducible builds |

---

## Quick Reference Card

### Build the Executable
```powershell
.\build.ps1
```

### Run the Application
```powershell
sintese
# or
s
```

### Rebuild After Code Changes
```powershell
.\build.ps1
```

### Check Alias Configuration
```powershell
Get-Alias sintese
Get-Command Invoke-Sintese
```

### View Profile Location
```powershell
echo $PROFILE
```

### Edit Profile Manually
```powershell
notepad $PROFILE
```

---

## Conclusion

You now have:
- ✅ A fully automated build process
- ✅ A standalone executable that runs without Python
- ✅ Convenient aliases (`sintese` and `s`) accessible from anywhere
- ✅ A comprehensive understanding of how everything works
- ✅ The ability to rebuild and maintain the solution

The setup is clean, professional, and easy to maintain or remove if needed. All system modifications are minimal, well-documented, and reversible.

---

**Last Updated**: December 17, 2025  
**Project**: Sinteses Avaliação Data Entry  
**Build Tool**: PyInstaller 6.17.0  
**Python Version**: 3.14.0
