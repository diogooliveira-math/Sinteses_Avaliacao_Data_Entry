# Quick Reference Guide

**Project:** Sintese CLI - Student Assessment Text Generator  
**Version:** 1.0.0  
**Last Updated:** December 17, 2025

---

## 🚀 Quick Commands

### Run the Application
```powershell
s                    # Short alias
sintese             # Full command
```

### Run Tests
```powershell
python tests/test_cli.py          # Test CLI functionality
python tests/test_path_fix.py     # Test path resolution
```

### Build
```powershell
.\build.ps1                       # Automated build
python -m PyInstaller sintese.spec # Manual build
```

### Database
```powershell
python create_sqlite_db.py        # Create/recreate database
```

---

## 📁 Where to Find Things

### Documentation
- **Main README:** `README.md`
- **Database queries:** `docs/QUERY.md`
- **Visual summary:** `docs/VISUAL_SUMMARY.md`
- **Build guide:** `docs/build/BUILD_GUIDE.md`
- **Issues/Fixes:** `docs/issues/`

### Source Code
- **Main app:** `cli.py`
- **DB creation:** `create_sqlite_db.py`
- **Build script:** `build.ps1`
- **PyInstaller config:** `sintese.spec`

### Tests
- **All tests:** `tests/` folder
- **CLI tests:** `tests/test_cli.py`
- **Path tests:** `tests/test_path_fix.py`

### Data
- **Source data:** `base.json`
- **Database:** `base.db`
- **Executable:** `dist/sintese.exe`

---

## 🐛 Reporting Issues

### 1. Create Issue Report
```powershell
# Copy template
copy docs\issues\ISSUE_TEMPLATE.md docs\issues\2025-MM-DD_issue-name_ISSUE.md

# Edit the file
notepad docs\issues\2025-MM-DD_issue-name_ISSUE.md
```

### 2. Document the Fix
```powershell
# Copy template
copy docs\issues\FIX_TEMPLATE.md docs\issues\2025-MM-DD_issue-name_FIX.md

# Edit the file
notepad docs\issues\2025-MM-DD_issue-name_FIX.md
```

### 3. Update Index
Edit `docs/issues/README.md` to add your issue to the index.

---

## 📊 Project Structure

```
Root (clean!)
├── 📄 Core files (8 files)
│   ├── cli.py
│   ├── create_sqlite_db.py
│   ├── build.ps1
│   ├── base.json
│   └── base.db
│
├── 📚 docs/ - All documentation
│   ├── 🏗️ build/ - Build docs
│   └── 🐛 issues/ - Issue tracking
│
├── 🧪 tests/ - Test files
└── 📦 dist/ - Executable & database
```

---

## ✅ Common Tasks

### Add a New Assessment Text
1. Edit `base.json`
2. Run `python create_sqlite_db.py`
3. Copy new `base.db` to `dist/` if needed

### Rebuild After Code Changes
```powershell
.\build.ps1
```

### Test Everything
```powershell
python tests/test_cli.py
python tests/test_path_fix.py
```

### Check Executable Works Globally
```powershell
cd ~
s
```

---

## 🔧 Troubleshooting

### "no such table: sinteses"
**Solution:** Run `python create_sqlite_db.py`

### Alias not working
**Solution:** 
1. Run `.\build.ps1` to reconfigure
2. Or manually add to PowerShell profile

### Database not found
**Solution:** Ensure `base.db` is in same folder as `sintese.exe` in `dist/`

### Tests failing
**Solution:**
1. Ensure you're in project root
2. Check database exists
3. Verify Python environment

---

## 📞 Quick Links

- **Main Documentation:** [README.md](README.md)
- **Build Guide:** [docs/build/BUILD_GUIDE.md](docs/build/BUILD_GUIDE.md)
- **Issues Index:** [docs/issues/README.md](docs/issues/README.md)
- **Project Organization:** [PROJECT_ORGANIZATION.md](PROJECT_ORGANIZATION.md)

---

## 💡 Tips

- Use `s` alias for quick access from anywhere
- Keep `base.db` with `sintese.exe` in `dist/`
- Document issues using provided templates
- Run tests after making changes
- Check `docs/issues/` for past solutions

---

**Need more details?** See the main [README.md](README.md)
