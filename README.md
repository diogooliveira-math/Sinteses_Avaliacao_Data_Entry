# Sintese CLI - Student Assessment Text Generator

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A command-line tool that generates personalized assessment texts based on student behavior characteristics.

## 📋 Overview

Sintese CLI is a Windows application that helps educators quickly generate standardized assessment texts by answering simple yes/no questions about a student's behavior. The tool queries a pre-configured database and returns appropriate text snippets that can be directly copied to the clipboard.

## 🚀 Quick Start

### Running the Application

Simply use the alias from anywhere:

```powershell
s
```

Or use the full command:

```powershell
sintese
```

### Usage Flow

1. Press ENTER to start a new assessment
2. Select student gender (M/F)
3. Answer yes/no questions about:
   - Attendance (Assiduidade)
   - Punctuality (Pontualidade)
   - Participation (Participação)
   - Interest (Interesse)
   - Effort (Empenho)
   - Difficulties (Dificuldades)
4. The matching text is displayed and automatically copied to clipboard

## 📁 Project Structure

```
Sinteses_Avaliacao_Data_Entry/
│
├── cli.py                      # Main application script
├── create_sqlite_db.py         # Database initialization script
├── build.ps1                   # Automated build script
├── sintese.spec                # PyInstaller specification
│
├── base.json                   # Source data for assessments
├── base.db                     # SQLite database (generated)
│
├── dist/                       # Built executable distribution
│   ├── sintese.exe            # Compiled application
│   └── base.db                # Database (must be alongside .exe)
│
├── docs/                       # Documentation
│   ├── QUERY.md               # Database query documentation
│   ├── VISUAL_SUMMARY.md      # Visual project summary
│   ├── build/                 # Build-related documentation
│   │   ├── BUILD_GUIDE.md     # Comprehensive build guide
│   │   ├── BUILD_SUCCESS.md   # Build completion summary
│   │   └── INSTALL_SQLITE.md  # SQLite setup instructions
│   └── issues/                # Issue tracking & fixes
│       ├── 2025-12-17_database-path-resolution_ISSUE.md
│       └── 2025-12-17_database-path-resolution_FIX.md
│
└── tests/                      # Test files
    ├── test_cli.py            # CLI functionality tests
    └── test_path_fix.py       # Database path resolution tests
```

## 🛠️ Setup & Installation

### Prerequisites

- Python 3.11+
- Windows OS
- PowerShell

### From GitHub

```powershell
git clone https://github.com/diogooliveira-math/Sinteses_Avaliacao_Data_Entry.git
cd Sinteses_Avaliacao_Data_Entry
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt  # optional: create this file if your project has deps
```

### First-Time Setup

1. **Create the database:**
   ```powershell
   python create_sqlite_db.py
   ```

2. **Build the executable (optional):**
   ```powershell
   .\build.ps1
   ```
   
   This will:
   - Create a virtual environment
   - Install dependencies
   - Build the executable with PyInstaller
   - Configure PowerShell aliases

3. **Verify the installation:**
   ```powershell
   s
   ```

## 📖 Documentation

- **[Query Documentation](docs/QUERY.md)** - Database schema and query details
- **[Visual Summary](docs/VISUAL_SUMMARY.md)** - Project workflow visualization
- **[Build Guide](docs/build/BUILD_GUIDE.md)** - Complete build instructions
- **[Build Success](docs/build/BUILD_SUCCESS.md)** - Build completion checklist
- **[SQLite Installation](docs/build/INSTALL_SQLITE.md)** - Database setup guide

## 🐛 Issue Tracking

Issues and fixes are documented in `docs/issues/` with the following naming convention:

```
YYYY-MM-DD_issue-description_ISSUE.md  (Problem report)
YYYY-MM-DD_issue-description_FIX.md    (Solution summary)
```

### Recent Issues

- **2025-12-17:** [Database Path Resolution](docs/issues/2025-12-17_database-path-resolution_ISSUE.md)
  - **Problem:** Executable couldn't find database when run from different directories
  - **Solution:** [Implemented absolute path resolution](docs/issues/2025-12-17_database-path-resolution_FIX.md)
  - **Status:** ✅ Resolved

## 🧪 Testing

Run tests from the project root:

```powershell
# Test CLI functionality
python tests/test_cli.py

# Test database path resolution
python tests/test_path_fix.py
```

## 🔧 Development

### Running as Python Script

```powershell
python cli.py
```

### Rebuilding the Executable

```powershell
# Automated build
.\build.ps1

# Manual build
python -m PyInstaller --noconfirm sintese.spec
Copy-Item base.db dist\base.db -Force
```

## 📦 Distribution

To distribute the application:

1. Navigate to `dist/` folder
2. Copy both files:
   - `sintese.exe`
   - `base.db`
3. These two files must stay together in the same folder

## ⚙️ Configuration

### PowerShell Alias

The build script automatically configures aliases:
- `sintese` - Full command name
- `s` - Short alias

To manually configure (if needed):

```powershell
notepad $PROFILE
```

Add:
```powershell
function Invoke-Sintese {
    & 'C:\path\to\dist\sintese.exe' @args
}
Set-Alias -Name sintese -Value Invoke-Sintese -Force
Set-Alias -Name s -Value Invoke-Sintese -Force
```

## 📊 Database

The application uses SQLite with the following schema:

```sql
CREATE TABLE sinteses (
    id INTEGER PRIMARY KEY,
    Texto TEXT,
    Genero TEXT,
    Assiduidade INTEGER,
    Pontualidade INTEGER,
    Participacao INTEGER,
    Interesse INTEGER,
    Empenho INTEGER,
    Dificuldades INTEGER
)
```

Data source: `base.json`

## 🤝 Contributing

When adding new features or fixing issues:

1. Create tests in `tests/` folder
2. Document issues in `docs/issues/` with date-based naming
3. Update relevant documentation
4. Test both Python script and compiled executable

## 📝 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

## 👤 Author

Diogo Freitas Oliveira email: diogolll@outlook.pt

---

**Version:** 1.0.0  
**Last Updated:** December 17, 2025
