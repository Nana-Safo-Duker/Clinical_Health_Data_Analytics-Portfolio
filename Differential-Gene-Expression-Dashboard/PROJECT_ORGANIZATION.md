# 📁 Project Organization Guide

This document describes the complete structure of the Differential Gene Expression Analysis project and how everything fits together.

## 🗂️ Complete Directory Structure

```
Differential-Gene-Expression/
│
├── 📱 app/                          # Streamlit Dashboard Application
│   ├── __init__.py
│   ├── dashboard.py                 # Main Streamlit app
│   └── utils/                       # Utility modules
│       ├── __init__.py
│       ├── validators.py            # Data validation (future)
│       ├── plotters.py              # Plotting functions (future)
│       └── exporters.py             # Export utilities (future)
│
├── 📊 R/                            # R Analysis Scripts
│   ├── README.md                    # R scripts documentation
│   ├── deseq2_analysis.R            # DESeq2 pipeline
│   ├── edger_analysis.R             # edgeR pipeline
│   ├── limma_analysis.R             # limma-voom pipeline
│   └── scripts/                     # Additional R utilities
│
├── 📚 notebooks/                    # Jupyter Tutorial Notebooks
│   ├── README.md                    # Notebooks guide
│   ├── 01_Introduction_and_Setup.ipynb
│   ├── 02_Data_Exploration_and_Visualization.ipynb
│   ├── 03_Statistical_Analysis.ipynb
│   ├── 04_Advanced_Analysis_and_Export.ipynb
│   └── [legacy notebooks]           # Older notebook versions
│
├── 📁 data/                         # Data Storage
│   ├── README.md                    # Data organization guide
│   ├── raw/                         # Raw input data (not in git)
│   ├── processed/                   # Analysis outputs (not in git)
│   └── examples/                    # Sample datasets (in git)
│       └── sample_data.csv
│
├── 🧪 tests/                        # Test Suite
│   ├── __init__.py
│   ├── test_dashboard.py            # Dashboard tests
│   └── test_utils.py                # Utility tests (future)
│
├── 📖 docs/                         # Documentation
│   ├── images/                      # Screenshots and plots
│   │   └── README.md
│   ├── USER_GUIDE.md                # Comprehensive user guide
│   ├── INSTALLATION.md              # Installation instructions
│   ├── IMPROVEMENTS.md              # Version changelog
│   ├── PROJECT_SUMMARY.md           # Project overview
│   └── README_ENHANCED_DASHBOARD.md # Dashboard features
│
├── 🔧 scripts/                      # Utility Scripts
│   └── quick_start.py               # Quick launcher
│
├── 📜 Configuration & Setup Files
│   ├── .gitignore                   # Git ignore rules
│   ├── .github/                     # GitHub Actions
│   │   └── workflows/
│   │       ├── lint.yml
│   │       └── tests.yml
│   ├── setup.py                     # Package setup
│   ├── MANIFEST.in                  # Package manifest
│   ├── requirements.txt             # Python dependencies
│   └── requirements-dev.txt         # Development dependencies
│
├── 📄 Project Documentation
│   ├── README.md                    # Main project README
│   ├── LICENSE                      # MIT License
│   ├── CONTRIBUTING.md              # Contribution guidelines
│   ├── CONTRIBUTORS.md              # Contributors list
│   ├── CHANGELOG.md                 # Version history
│   ├── PROJECT_ORGANIZATION.md      # This file
│   ├── PROJECT_STRUCTURE.md         # Technical structure
│   └── PROJECT_SUMMARY.md           # Executive summary
│
└── 🗑️ Legacy Files (to be archived/removed)
    ├── Differential_Gene_Dashboard*.py    # Old dashboard versions
    ├── Differential_Gene_Epression_Analysis*.py
    └── [other duplicate files]
```

## 🎯 Component Purposes

### 1. **Streamlit Dashboard** (`app/`)
Interactive web application for visualizing differential expression results.

**When to use**:
- You have DESeq2/edgeR/limma results as CSV
- You want interactive exploration
- You need publication-quality plots
- You want to filter and export results

**How to use**:
```bash
streamlit run app/dashboard.py
```

### 2. **R Analysis Scripts** (`R/`)
Complete analysis pipelines for RNA-seq differential expression.

**When to use**:
- You have raw count data
- You need to run DESeq2, edgeR, or limma
- You want statistical analysis from scratch
- You're starting a new RNA-seq project

**How to use**:
```r
source("R/deseq2_analysis.R")
# Then follow function calls in script
```

### 3. **Jupyter Notebooks** (`notebooks/`)
Educational tutorials and interactive analysis.

**When to use**:
- You're learning differential expression analysis
- You want step-by-step guidance
- You prefer Python for analysis
- You want to customize analyses

**How to use**:
```bash
jupyter notebook notebooks/
```

### 4. **Data Directory** (`data/`)
Organized storage for all data files.

**Structure**:
- `raw/` - Your original count matrices and metadata
- `processed/` - Analysis outputs and results
- `examples/` - Sample data for tutorials

## 🔄 Typical Workflows

### Workflow 1: Complete Analysis (Raw Data → Results)

```
1. Place raw data in data/raw/
   ├── counts.csv
   └── metadata.csv

2. Run R analysis
   Rscript R/deseq2_analysis.R
   → Generates data/processed/deseq2_results.csv

3. Visualize with dashboard
   streamlit run app/dashboard.py
   → Upload deseq2_results.csv

4. Export results
   → Download filtered significant genes
```

### Workflow 2: Visualization Only (Existing Results)

```
1. Have results CSV with required columns
   ├── Gene
   ├── log2FoldChange
   └── padj

2. Launch dashboard
   streamlit run app/dashboard.py

3. Upload and explore
   → Interactive visualizations
   → Filter and export
```

### Workflow 3: Learning and Tutorial

```
1. Start with notebooks
   jupyter notebook notebooks/01_Introduction_and_Setup.ipynb

2. Work through series
   01 → 02 → 03 → 04

3. Apply to your data
   Modify notebook code for your dataset

4. Export results
   Use dashboard for final visualizations
```

## 📦 Installation Paths

### For End Users
```bash
# Clone repository
git clone https://github.com/yourusername/Differential-Gene-Expression.git
cd Differential-Gene-Expression

# Install Python dependencies
pip install -r requirements.txt

# Run dashboard
streamlit run app/dashboard.py
```

### For Developers
```bash
# Clone repository
git clone https://github.com/yourusername/Differential-Gene-Expression.git
cd Differential-Gene-Expression

# Install with dev dependencies
pip install -r requirements-dev.txt

# Run tests
python tests/test_dashboard.py

# Make changes and contribute
git checkout -b feature/my-feature
```

### For R Users
```r
# Install R dependencies
if (!requireNamespace("BiocManager", quietly = TRUE))
    install.packages("BiocManager")

BiocManager::install(c("DESeq2", "edgeR", "limma"))
install.packages(c("ggplot2", "pheatmap", "ggrepel", "dplyr"))

# Run analysis
source("R/deseq2_analysis.R")
```

## 🎨 Design Principles

### 1. **Separation of Concerns**
- R scripts: Statistical analysis
- Python dashboard: Visualization
- Notebooks: Education and exploration

### 2. **Data Organization**
- Raw data: Never modified
- Processed data: Regenerable from raw
- Examples: Tracked in git

### 3. **Modularity**
- Each component works independently
- Mix and match as needed
- Clear interfaces between components

### 4. **Documentation**
- README in every directory
- Inline code comments
- Tutorial notebooks
- User guides

## 🚀 Quick Start by Role

### I'm a Biologist with RNA-seq results
→ Use the **Streamlit Dashboard** (`app/dashboard.py`)

### I'm a Bioinformatician starting from counts
→ Use the **R Scripts** (`R/deseq2_analysis.R`)

### I'm a Student learning the concepts
→ Start with **Jupyter Notebooks** (`notebooks/01_...`)

### I'm a Developer wanting to contribute
→ Read **CONTRIBUTING.md** and set up dev environment

## 📊 File Size Considerations

| Directory | Typical Size | Git Tracked |
|-----------|--------------|-------------|
| `app/` | < 1 MB | Yes |
| `R/` | < 1 MB | Yes |
| `notebooks/` | 1-5 MB | Yes |
| `data/raw/` | 10-1000 MB | No |
| `data/processed/` | 1-100 MB | No |
| `data/examples/` | < 1 MB | Yes |
| `docs/` | 1-10 MB | Yes |
| `tests/` | < 1 MB | Yes |

## 🔐 Security & Privacy

### Committed to Git (Public)
- ✅ Code and scripts
- ✅ Documentation
- ✅ Example data (anonymized)
- ✅ Tests

### NOT Committed (Private)
- ❌ Large datasets
- ❌ Patient/sensitive data
- ❌ API keys/credentials
- ❌ Personal metadata

## 🛠️ Maintenance

### Regular Tasks
- Update dependencies (requirements.txt)
- Run tests before commits
- Update documentation with changes
- Archive old versions

### Version Control
- Main branch: stable releases
- Dev branch: active development
- Feature branches: new features
- Tag releases: v1.0.0, v2.0.0, etc.

## 📞 Getting Help

**Can't find something?**
- Check directory READMEs
- Search documentation
- Open an issue on GitHub

**Want to contribute?**
- Read CONTRIBUTING.md
- Fork and create PR
- Follow code style guidelines

---

## 🎓 Learning Path

1. **Beginner**: Start with notebooks and sample data
2. **Intermediate**: Use dashboard with your own results
3. **Advanced**: Run full R pipelines and customize
4. **Expert**: Contribute code and improvements

---

*Well-organized projects lead to well-organized research! 🧬✨*

