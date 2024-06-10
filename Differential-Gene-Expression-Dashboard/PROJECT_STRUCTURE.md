# Project Structure

Complete overview of the Differential Gene Expression Dashboard project organization.

## Directory Tree

```
Differential-Gene-Expression/
│
├── .github/                          # GitHub configuration
│   └── workflows/
│       ├── tests.yml                 # Automated testing workflow
│       └── lint.yml                  # Code quality checks
│
├── app/                              # Main application code
│   ├── __init__.py                   # Package initialization
│   ├── dashboard.py                  # Main Streamlit dashboard (ENTRY POINT)
│   └── utils/                        # Utility modules
│       ├── __init__.py
│       ├── validators.py             # Data validation functions
│       ├── plotters.py               # Visualization functions
│       └── exporters.py              # Export utilities
│
├── tests/                            # Test suite
│   ├── __init__.py
│   ├── test_dashboard.py             # Main test file
│   └── test_utils.py                 # Utility tests
│
├── docs/                             # Documentation
│   ├── images/                       # Screenshots and diagrams
│   │   ├── dashboard-preview.png
│   │   ├── volcano-plot.png
│   │   ├── ma-plot.png
│   │   └── top-genes.png
│   ├── USER_GUIDE.md                 # Comprehensive user guide
│   ├── API.md                        # API documentation
│   ├── INSTALLATION.md               # Installation instructions
│   ├── IMPROVEMENTS.md               # Feature comparison
│   └── PROJECT_SUMMARY.md            # Project overview
│
├── examples/                         # Example data and demos
│   ├── sample_data.csv               # Test dataset (51 genes)
│   ├── demo_analysis.ipynb           # Jupyter notebook demo
│   └── README.md                     # Examples guide
│
├── scripts/                          # Utility scripts
│   ├── quick_start.py                # Easy launcher
│   └── setup_dev.py                  # Development setup
│
├── .gitignore                        # Git ignore rules
├── LICENSE                           # MIT License
├── README.md                         # Main README (GitHub homepage)
├── CONTRIBUTING.md                   # Contribution guidelines
├── CONTRIBUTORS.md                   # List of contributors
├── CHANGELOG.md                      # Version history
├── MANIFEST.in                       # Package data manifest
├── setup.py                          # Package installation script
├── requirements.txt                  # Production dependencies
└── requirements-dev.txt              # Development dependencies
```

---

## Key Files Explained

### Entry Points

| File | Purpose | Usage |
|------|---------|-------|
| `app/dashboard.py` | Main application | `streamlit run app/dashboard.py` |
| `scripts/quick_start.py` | Easy launcher | `python scripts/quick_start.py` |
| `setup.py` | Package installer | `pip install .` |

### Configuration Files

| File | Purpose |
|------|---------|
| `.gitignore` | Specifies untracked files |
| `requirements.txt` | Production dependencies |
| `requirements-dev.txt` | Development dependencies |
| `MANIFEST.in` | Package data inclusion rules |
| `setup.py` | Package metadata and installation |

### Documentation Files

| File | Audience | Content |
|------|----------|---------|
| `README.md` | All users | Project overview, quick start |
| `docs/USER_GUIDE.md` | End users | Tutorials, examples |
| `docs/API.md` | Developers | Function reference |
| `docs/INSTALLATION.md` | New users | Detailed installation |
| `CONTRIBUTING.md` | Contributors | Development guide |
| `CHANGELOG.md` | All users | Version history |

### Testing Files

| File | Purpose |
|------|---------|
| `tests/test_dashboard.py` | Main test suite (7 tests) |
| `tests/test_utils.py` | Utility function tests |
| `.github/workflows/tests.yml` | CI/CD testing |
| `.github/workflows/lint.yml` | Code quality checks |

---

## Module Organization

### app/ (Main Application)

```
app/
├── dashboard.py           # Streamlit UI and main logic
│   ├── File upload handling
│   ├── Column mapping interface
│   ├── Threshold controls
│   ├── Visualization rendering
│   └── Export functionality
│
└── utils/                 # Supporting utilities
    ├── validators.py      # Data validation
    │   ├── validate_data()
    │   └── validate_columns()
    │
    ├── plotters.py        # Visualization functions
    │   ├── create_volcano_plot_plotly()
    │   ├── create_volcano_plot_altair()
    │   ├── create_ma_plot()
    │   ├── create_top_genes_chart()
    │   └── create_distribution_plot()
    │
    └── exporters.py       # Export utilities
        ├── export_to_excel()
        └── export_to_csv()
```

### tests/ (Testing)

```
tests/
├── test_dashboard.py      # Integration tests
│   ├── test_sample_data()
│   ├── test_required_columns()
│   ├── test_optional_columns()
│   ├── test_data_calculations()
│   ├── test_dependencies()
│   ├── test_file_structure()
│   └── test_data_export()
│
└── test_utils.py          # Unit tests
    ├── test_validators()
    ├── test_plotters()
    └── test_exporters()
```

---

## Data Flow

```
┌─────────────────┐
│  User uploads   │
│   CSV file      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Column mapping │
│  (user selects) │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Data validation│
│  (validators.py)│
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Data processing│
│  & calculations │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Visualizations │
│  (plotters.py)  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Export options │
│  (exporters.py) │
└─────────────────┘
```

---

## File Size Reference

| Directory/File | Size | Lines of Code |
|----------------|------|---------------|
| `app/dashboard.py` | ~31 KB | ~470 LOC |
| `app/utils/` | ~15 KB | ~200 LOC |
| `tests/` | ~10 KB | ~150 LOC |
| `docs/` | ~200 KB | ~4000+ lines |
| Total Project | ~300 KB | ~5000+ lines |

---

## Dependencies Hierarchy

```
streamlit (UI framework)
├── altair (declarative viz)
├── plotly (interactive viz)
├── pandas (data manipulation)
│   └── numpy (numerical ops)
└── openpyxl (Excel export)
```

---

## Development Workflow

### 1. Clone & Setup
```bash
git clone <repo-url>
cd Differential-Gene-Expression
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Make Changes
```bash
# Edit code in app/
# Add tests in tests/
# Update docs in docs/
```

### 3. Test
```bash
python tests/test_dashboard.py
flake8 app/ tests/
black app/ tests/
```

### 4. Commit
```bash
git add .
git commit -m "feat: add new feature"
git push origin feature-branch
```

### 5. Pull Request
- Automated tests run
- Code review
- Merge to main

---

## Release Process

### Version Bumping

1. Update `app/__init__.py` - `__version__`
2. Update `setup.py` - `version`
3. Update `CHANGELOG.md` - Add new version section
4. Tag release in git

```bash
git tag -a v2.0.0 -m "Release version 2.0.0"
git push origin v2.0.0
```

### PyPI Release (Future)

```bash
python setup.py sdist bdist_wheel
twine upload dist/*
```

---

## CI/CD Pipeline

```
Push to GitHub
      │
      ▼
┌─────────────┐
│  Run Tests  │ (tests.yml)
│  on 3 OS    │
│  5 Python   │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Lint Code  │ (lint.yml)
│  flake8     │
│  black      │
└──────┬──────┘
       │
       ▼
   ✅ Pass
   ❌ Fail
```

---

## Best Practices Implemented

### Code Organization
- ✅ Modular design (separate utilities)
- ✅ Clear naming conventions
- ✅ Proper package structure
- ✅ Type hints where appropriate

### Documentation
- ✅ Comprehensive README
- ✅ Detailed user guide
- ✅ API documentation
- ✅ Inline code comments

### Testing
- ✅ Automated test suite
- ✅ CI/CD integration
- ✅ Multiple platform testing
- ✅ Code coverage tracking

### Version Control
- ✅ Meaningful commit messages
- ✅ Proper .gitignore
- ✅ Branch protection
- ✅ Pull request templates

### Distribution
- ✅ setup.py for packaging
- ✅ requirements.txt
- ✅ LICENSE file
- ✅ MANIFEST.in for data files

---

## Quick Reference

### Common Commands

```bash
# Development
streamlit run app/dashboard.py          # Run dashboard
python tests/test_dashboard.py          # Run tests
python scripts/quick_start.py           # Easy start
black app/ tests/                       # Format code
flake8 app/ tests/                      # Lint code

# Installation
pip install -r requirements.txt         # Install deps
pip install -e .                        # Dev install
pip install .                           # Regular install

# Git
git checkout -b feature/name            # New branch
git commit -m "type: message"           # Commit
git push origin branch-name             # Push

# Package
python setup.py sdist                   # Source dist
python setup.py bdist_wheel             # Wheel dist
pip install dist/package.whl            # Install wheel
```

---

## Future Structure Plans

### Version 2.1.0
```
+ app/
  + analysis/
    + gsea.py              # Gene Set Enrichment
    + pathway.py           # Pathway analysis
+ docs/
  + tutorials/             # Step-by-step guides
```

### Version 2.2.0
```
+ app/
  + integrations/
    + ncbi.py              # NCBI integration
    + ensembl.py           # Ensembl integration
+ docker/
  + Dockerfile             # Container setup
```

---

## Contributing to Structure

When adding new features, follow this structure:

1. **New utility module**: Add to `app/utils/`
2. **New tests**: Add to `tests/`
3. **New docs**: Add to `docs/`
4. **New examples**: Add to `examples/`
5. **Update**: CHANGELOG.md, relevant README sections

---

**Last Updated**: October 2025  
**Version**: 2.0.0  
**Maintainer**: Project Team


