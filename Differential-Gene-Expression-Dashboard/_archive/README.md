# 📦 Archive Directory

This directory contains older versions and duplicate files that have been superseded by the current organized project structure.

## 📜 Contents

### Old Dashboard Versions
- `Differential_Gene_Dashboard*.py` - Previous versions of the dashboard
- These have been consolidated into `app/dashboard.py`

### Old Analysis Scripts
- `Differential_Gene_Epression_Analysis*.py` - Previous Python analysis scripts
- Functionality has been improved and moved to:
  - `src/python_analysis.py` (Python template)
  - `R/deseq2_analysis.R` (R pipeline)
  - `R/edger_analysis.R` (R pipeline)
  - `R/limma_analysis.R` (R pipeline)

### Old Notebooks
- Previous notebook versions are kept for reference
- Current tutorial series is in `notebooks/01-04_*.ipynb`

## ⚠️ Important Notes

### Do NOT use these files for new analyses
These files are:
- ❌ Not maintained
- ❌ May have bugs or outdated methods
- ❌ Not documented
- ❌ Not tested

### Use the current versions instead:
- ✅ `app/dashboard.py` - Main dashboard
- ✅ `R/*.R` - R analysis scripts
- ✅ `src/python_analysis.py` - Python template
- ✅ `notebooks/*.ipynb` - Tutorials

## 🗑️ Deletion Policy

These files are kept temporarily for reference during the transition period.

**They may be permanently deleted in future versions.**

If you need something from these files:
1. Check if the functionality exists in current versions
2. Open an issue on GitHub if something is missing
3. Extract what you need before they're deleted

## 📅 Archive History

- **2025-10-29**: Initial archival of duplicate files during project reorganization
- Files archived as part of creating organized, professional project structure

## 🔄 Migration Guide

If you were using old files, here's where to find the new equivalents:

| Old File | New Location | Notes |
|----------|--------------|-------|
| `Differential_Gene_Dashboard.py` | `app/dashboard.py` | Enhanced with better UI |
| `Differential_Gene_Dashboard_Enhanced.py` | `app/dashboard.py` | Features merged |
| `Differential_Gene_Epression_Analysis.py` | `src/python_analysis.py` | Improved and documented |
| Old notebooks | `notebooks/01-04_*.ipynb` | Complete tutorial series |

## 💡 Why Archive?

**Benefits of the new structure:**
1. **Clearer organization** - Easy to find what you need
2. **Better documentation** - Everything explained
3. **Tested and maintained** - Quality assured
4. **Professional structure** - Industry best practices
5. **Multiple options** - Python, R, and Jupyter workflows

## 🤝 Questions?

If you have questions about:
- **Missing features**: Open a GitHub issue
- **File contents**: Check git history
- **Migration help**: See GETTING_STARTED.md

---

*This archive exists for historical purposes only. Always use the current project structure.*

