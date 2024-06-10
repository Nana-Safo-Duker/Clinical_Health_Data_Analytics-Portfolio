# ⚡ Quick Reference Guide

**Fast access to everything you need in the Differential Gene Expression Analysis project.**

---

## 🚀 I Want To...

### ...Visualize My Results
```bash
streamlit run app/dashboard.py
```
📄 Upload your CSV with Gene, log2FoldChange, padj columns

### ...Run DESeq2 Analysis
```r
source("R/deseq2_analysis.R")
```
📁 Place `counts.csv` and `metadata.csv` in `data/raw/`

### ...Run edgeR Analysis
```r
source("R/edger_analysis.R")
```
📁 Same data requirements as DESeq2

### ...Run limma-voom Analysis
```r
source("R/limma_analysis.R")
```
📁 Same data requirements as DESeq2

### ...Learn Step by Step
```bash
jupyter notebook notebooks/01_Introduction_and_Setup.ipynb
```
📚 Follow the tutorial series

### ...Use Python for Analysis
```python
from src.python_analysis import *
df = load_results("my_data.csv")
df = add_regulation_status(df)
create_volcano_plot(df, "volcano.png")
```

---

## 📂 Where Is...?

| What | Where | Description |
|------|-------|-------------|
| **Main dashboard** | `app/dashboard.py` | Interactive visualization app |
| **R scripts** | `R/*.R` | DESeq2, edgeR, limma pipelines |
| **Python analysis** | `src/python_analysis.py` | Python template script |
| **Tutorials** | `notebooks/01_*.ipynb` | Learning materials |
| **Sample data** | `data/examples/sample_data.csv` | Example dataset |
| **Documentation** | `docs/USER_GUIDE.md` | Comprehensive guide |
| **Getting started** | `GETTING_STARTED.md` | Quick start guide |
| **Project structure** | `PROJECT_ORGANIZATION.md` | Detailed structure |
| **Tests** | `tests/test_dashboard.py` | Test suite |

---

## 🎯 Quick Commands

### Installation
```bash
# Python
pip install -r requirements.txt

# R
Rscript -e "BiocManager::install(c('DESeq2', 'edgeR', 'limma'))"
```

### Running
```bash
# Dashboard
streamlit run app/dashboard.py

# Tests
python tests/test_dashboard.py

# Notebooks
jupyter notebook notebooks/
```

### R Scripts
```r
# From R console
source("R/deseq2_analysis.R")
source("R/edger_analysis.R")
source("R/limma_analysis.R")
```

---

## 📊 Data Formats

### For Dashboard (Results CSV)
```csv
Gene,log2FoldChange,padj,baseMean,regulation
TP53,2.5,0.001,5432.21,Upregulated
BRCA1,-1.8,0.01,4521.33,Downregulated
```

### For R Scripts (Count Matrix)
```csv
,Sample1,Sample2,Sample3,Sample4
GENE1,1523,1832,234,189
GENE2,45,67,2341,2567
```

### For R Scripts (Metadata)
```csv
,condition,batch
Sample1,control,batch1
Sample2,control,batch1
Sample3,treated,batch2
Sample4,treated,batch2
```

---

## 🔧 Common Parameters

### Significance Thresholds
- **P-value**: `0.05` (standard), `0.01` (stringent)
- **Log2FC**: `1.0` (2-fold), `1.5` (3-fold), `2.0` (4-fold)

### Plot Types
- **Volcano plot**: log2FC vs -log10(padj)
- **MA plot**: log2FC vs mean expression
- **PCA**: Sample similarity
- **Heatmap**: Top significant genes

---

## 🆘 Troubleshooting

### Dashboard Won't Start
```bash
# Reinstall streamlit
pip install --upgrade streamlit
streamlit run app/dashboard.py
```

### R Package Error
```r
# Update and reinstall
BiocManager::install("DESeq2", force = TRUE)
```

### Can't Upload File
- Check file is `.csv` format
- Ensure file is < 200MB
- Verify column names are correct

### Import Errors in Python
```bash
pip install -r requirements.txt
```

---

## 📖 Documentation Map

```
Start Here
    ↓
README.md → Overview and features
    ↓
GETTING_STARTED.md → Installation and quick start
    ↓
Choose Your Path:
    ├→ Dashboard: app/dashboard.py
    ├→ R Analysis: R/README.md
    ├→ Python: src/README.md
    └→ Learning: notebooks/README.md
    ↓
Need More Help?
    ├→ User Guide: docs/USER_GUIDE.md
    ├→ Structure: PROJECT_ORGANIZATION.md
    └→ File Tree: PROJECT_TREE.md
```

---

## 💡 Pro Tips

### Tip 1: Start with Sample Data
```bash
streamlit run app/dashboard.py
# Upload: data/examples/sample_data.csv
```

### Tip 2: Use R Scripts for New Analysis
```r
# Your count data → R script → Results CSV → Dashboard
```

### Tip 3: Customize Python Analysis
```python
from src.python_analysis import *
# Modify thresholds, filters, plots
```

### Tip 4: Learn with Notebooks
```bash
jupyter notebook notebooks/01_Introduction_and_Setup.ipynb
# Interactive learning with explanations
```

---

## 🎓 Learning Path

**Beginner**: 
1. Read README.md
2. Open dashboard with sample data
3. Start notebook 01

**Intermediate**:
1. Run R script with your data
2. Visualize in dashboard
3. Complete all notebooks

**Advanced**:
1. Customize R scripts
2. Modify Python modules
3. Contribute improvements

---

## 📞 Get Help

### Documentation
- `README.md` - Project overview
- `GETTING_STARTED.md` - Quick start
- `docs/USER_GUIDE.md` - Comprehensive guide
- `PROJECT_ORGANIZATION.md` - Structure details

### Code Examples
- `notebooks/` - Interactive tutorials
- `R/README.md` - R script examples
- `src/README.md` - Python examples

### Community
- GitHub Issues - Bug reports
- GitHub Discussions - Questions
- Contributing Guide - `CONTRIBUTING.md`

---

## 🔗 Important Links

| Resource | Location |
|----------|----------|
| Main README | `README.md` |
| Getting Started | `GETTING_STARTED.md` |
| Dashboard Code | `app/dashboard.py` |
| R Scripts | `R/deseq2_analysis.R` |
| Python Module | `src/python_analysis.py` |
| Notebooks | `notebooks/` |
| Sample Data | `data/examples/sample_data.csv` |
| User Guide | `docs/USER_GUIDE.md` |
| Project Structure | `PROJECT_ORGANIZATION.md` |
| File Tree | `PROJECT_TREE.md` |

---

## ⚙️ Configuration

### Python Requirements
```
streamlit>=1.28.0
pandas>=2.0.0
numpy>=1.24.0
altair>=5.0.0
plotly>=5.17.0
openpyxl>=3.1.0
```

### R Requirements
```
DESeq2
edgeR
limma
ggplot2
pheatmap
dplyr
```

---

## 🎯 Quick Checklist

**New User Setup**:
- [ ] Clone repository
- [ ] Install Python dependencies
- [ ] Install R dependencies (if using R)
- [ ] Test with sample data
- [ ] Read GETTING_STARTED.md

**First Analysis**:
- [ ] Prepare your data
- [ ] Choose workflow (Dashboard/R/Python/Notebook)
- [ ] Run analysis
- [ ] Review results
- [ ] Export significant genes

**Next Steps**:
- [ ] Explore other workflows
- [ ] Customize parameters
- [ ] Create publication figures
- [ ] Apply to your research

---

## 📊 Workflow Comparison

| Workflow | Time | Difficulty | Best For |
|----------|------|------------|----------|
| **Dashboard** | 5 min | ⭐ Easy | Existing results |
| **R Scripts** | 60 min | ⭐⭐⭐ Medium | Raw counts |
| **Python** | 30 min | ⭐⭐ Easy-Medium | Scripting |
| **Notebooks** | 4 hrs | ⭐⭐ Easy-Medium | Learning |

---

## 🚀 One-Liners

```bash
# Start dashboard
streamlit run app/dashboard.py

# Run tests
python tests/test_dashboard.py

# Launch notebooks
jupyter notebook notebooks/

# Install everything
pip install -r requirements.txt && \
Rscript -e "BiocManager::install(c('DESeq2','edgeR','limma'))"
```

---

**Bookmark this page for quick access!** 🔖

*Everything you need, one click away* ⚡

