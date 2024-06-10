# 🚀 Getting Started Guide

Welcome! This guide will help you get up and running with the Differential Gene Expression Analysis project based on your needs and experience level.

## 📋 Table of Contents

1. [Choose Your Path](#choose-your-path)
2. [Installation](#installation)
3. [Quick Start Tutorials](#quick-start-tutorials)
4. [Common Workflows](#common-workflows)
5. [Troubleshooting](#troubleshooting)
6. [Next Steps](#next-steps)

---

## 🎯 Choose Your Path

### I'm a biologist with DESeq2/edgeR results (CSV file)
**→ Use the Python Dashboard**
- Time: 5 minutes to get started
- Difficulty: ⭐ Easy
- [Jump to Dashboard Quick Start](#python-dashboard-quick-start)

### I'm a bioinformatician with raw RNA-seq counts
**→ Use the R Scripts**
- Time: 30-60 minutes for full analysis
- Difficulty: ⭐⭐⭐ Intermediate
- [Jump to R Analysis Quick Start](#r-analysis-quick-start)

### I'm a student learning differential expression
**→ Start with Jupyter Notebooks**
- Time: 2-4 hours for full tutorial series
- Difficulty: ⭐⭐ Beginner-Intermediate
- [Jump to Notebooks Quick Start](#notebooks-quick-start)

### I'm a developer wanting to contribute
**→ Set up development environment**
- Time: 15 minutes
- Difficulty: ⭐⭐⭐ Intermediate
- [Jump to Developer Setup](#developer-setup)

---

## 💻 Installation

### Prerequisites

**For Python Dashboard & Notebooks:**
- Python 3.8 or higher
- pip package manager

**For R Scripts:**
- R 4.0 or higher
- Bioconductor

**For Notebooks:**
- Jupyter Notebook or JupyterLab

### Python Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/Differential-Gene-Expression.git
cd Differential-Gene-Expression

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt
```

### R Installation

```r
# Install Bioconductor if not already installed
if (!requireNamespace("BiocManager", quietly = TRUE))
    install.packages("BiocManager")

# Install required Bioconductor packages
BiocManager::install(c(
    "DESeq2",
    "edgeR",
    "limma"
))

# Install CRAN packages
install.packages(c(
    "ggplot2",
    "pheatmap",
    "RColorBrewer",
    "ggrepel",
    "dplyr",
    "tibble"
))
```

---

## 🚀 Quick Start Tutorials

### Python Dashboard Quick Start

**What you need:**
- A CSV file with differential expression results
- Columns: Gene names, log2FoldChange, adjusted p-values

**Steps:**

1. **Install and launch**:
```bash
pip install -r requirements.txt
streamlit run app/dashboard.py
```

2. **Your browser opens automatically** (or go to http://localhost:8501)

3. **Upload your data**:
   - Click "Browse files"
   - Select your CSV file
   - Or try with `data/examples/sample_data.csv`

4. **Map your columns**:
   - Select which column contains gene names
   - Select which column contains log2 fold changes
   - Select which column contains adjusted p-values

5. **Explore**:
   - View volcano plots
   - Adjust significance thresholds
   - Filter genes
   - Export results

**That's it!** You're now visualizing your data interactively.

---

### R Analysis Quick Start

**What you need:**
- Raw count matrix (CSV): genes × samples
- Metadata file (CSV): sample information

**Steps:**

1. **Prepare your data**:

Create `data/raw/counts.csv`:
```csv
,Sample1,Sample2,Sample3,Sample4
GENE1,1523,1832,234,189
GENE2,45,67,2341,2567
GENE3,789,654,432,567
```

Create `data/raw/metadata.csv`:
```csv
,condition
Sample1,control
Sample2,control
Sample3,treated
Sample4,treated
```

2. **Choose your method**:
   - DESeq2: Most common, robust
   - edgeR: Fast, flexible
   - limma-voom: Best for large datasets

3. **Run analysis**:
```r
# Open R or RStudio
source("R/deseq2_analysis.R")

# Load your data
data <- load_data(
  count_file = "data/raw/counts.csv",
  metadata_file = "data/raw/metadata.csv"
)

# Run analysis
results <- run_deseq2(
  counts = data$counts,
  metadata = data$metadata
)

# Export results
export_results(results$results, "data/processed/my_results.csv")
```

4. **Visualize with dashboard**:
```bash
streamlit run app/dashboard.py
# Upload data/processed/my_results.csv
```

---

### Notebooks Quick Start

**What you need:**
- Python and Jupyter installed
- Basic Python knowledge (helpful but not required)

**Steps:**

1. **Install Jupyter**:
```bash
pip install -r requirements.txt jupyter
```

2. **Launch Jupyter**:
```bash
jupyter notebook notebooks/
```

3. **Start with Notebook 01**:
   - Open `01_Introduction_and_Setup.ipynb`
   - Read the introduction
   - Run cells one by one (Shift+Enter)
   - Follow along with explanations

4. **Progress through series**:
   - 01: Introduction and Setup
   - 02: Data Exploration and Visualization
   - 03: Statistical Analysis
   - 04: Advanced Analysis and Export

5. **Experiment**:
   - Modify parameters
   - Try with your own data
   - Create new analyses

---

## 🔄 Common Workflows

### Workflow A: Complete Beginner

```
Day 1: Read README and GETTING_STARTED
Day 2: Install software and dependencies
Day 3: Work through Notebook 01 & 02
Day 4: Work through Notebook 03 & 04
Day 5: Try dashboard with sample data
Day 6: Apply to your own data
```

### Workflow B: I Have Results Already

```
Step 1: Install Python dependencies (5 min)
Step 2: Launch dashboard (1 min)
Step 3: Upload your results (1 min)
Step 4: Explore and export (30 min)
```

### Workflow C: Starting from Scratch

```
Week 1: Prepare count matrix and metadata
Week 1: Run R analysis (DESeq2/edgeR/limma)
Week 2: QC checks and troubleshooting
Week 2: Visualize with dashboard
Week 3: Gene set enrichment analysis
Week 3: Prepare figures for publication
```

---

## 🐛 Troubleshooting

### Common Issues and Solutions

#### Python: Import Errors

**Problem**: `ModuleNotFoundError: No module named 'streamlit'`

**Solution**:
```bash
pip install -r requirements.txt
```

---

#### R: Package Installation Fails

**Problem**: Bioconductor packages won't install

**Solution**:
```r
# Update R to latest version
# Then try:
BiocManager::install("DESeq2", force = TRUE, update = TRUE)
```

---

#### Dashboard: Can't Upload File

**Problem**: File upload button not working

**Solution**:
- Check file is CSV format
- Ensure file is < 200MB
- Try restarting the dashboard
- Check browser console for errors

---

#### R: Memory Errors

**Problem**: R runs out of memory with large datasets

**Solution**:
```r
# Increase memory limit (Windows)
memory.limit(size = 32000)

# Or filter more aggressively
keep <- rowSums(counts) >= 50  # Stricter filtering
```

---

#### Jupyter: Kernel Crashes

**Problem**: Jupyter kernel dies during analysis

**Solution**:
```bash
# Update jupyter
pip install --upgrade jupyter notebook

# Or try JupyterLab
pip install jupyterlab
jupyter lab
```

---

### Getting More Help

1. **Check documentation**:
   - `docs/USER_GUIDE.md` - Comprehensive guide
   - `R/README.md` - R scripts documentation
   - `notebooks/README.md` - Notebooks guide

2. **Search existing issues**:
   - GitHub Issues page
   - Stack Overflow

3. **Ask for help**:
   - Open a GitHub issue
   - Include error messages
   - Describe what you've tried

---

## 📚 Next Steps

### After Quick Start

1. **Customize analyses**:
   - Adjust significance thresholds
   - Try different visualization styles
   - Filter for specific gene sets

2. **Explore advanced features**:
   - Gene set enrichment
   - Pathway analysis
   - Batch effect correction

3. **Prepare for publication**:
   - Export high-resolution figures
   - Generate supplementary tables
   - Document analysis parameters

### Learning Resources

**Differential Expression**:
- [StatQuest: DESeq2 explained](https://www.youtube.com/c/joshstarmer)
- [RNA-seq Analysis Course](https://www.bioconductor.org/help/course-materials/)

**R Programming**:
- [R for Data Science](https://r4ds.had.co.nz/)
- [Bioconductor Workflows](https://www.bioconductor.org/packages/release/BiocViews.html#___Workflow)

**Python Data Analysis**:
- [Python for Biologists](https://pythonforbiologists.com/)
- [Pandas Documentation](https://pandas.pydata.org/docs/)

---

## 💡 Pro Tips

### For Best Results

1. **Start with sample data** to learn the interface
2. **Document your analyses** as you go
3. **Version control your scripts** if you modify them
4. **Keep raw data separate** from processed data
5. **Save your plots** at high resolution (300 dpi)

### Reproducibility Checklist

- ✅ Document software versions
- ✅ Save analysis parameters
- ✅ Keep raw data unchanged
- ✅ Use version control for custom scripts
- ✅ Document any manual filtering steps

---

## 🎓 Suggested Learning Path

### Level 1: Beginner (Week 1-2)
- ✅ Complete all Jupyter notebooks
- ✅ Use dashboard with sample data
- ✅ Understand volcano plots and MA plots
- ✅ Learn about p-values and fold changes

### Level 2: Intermediate (Week 3-4)
- ✅ Run R analysis with sample data
- ✅ Apply to your own dataset
- ✅ Customize visualizations
- ✅ Understand different DE methods

### Level 3: Advanced (Week 5-6)
- ✅ Modify R scripts for complex designs
- ✅ Integrate pathway analysis
- ✅ Handle batch effects
- ✅ Create publication figures

### Level 4: Expert (Ongoing)
- ✅ Contribute improvements
- ✅ Share your workflows
- ✅ Help others in community
- ✅ Stay updated with best practices

---

## 🎉 Success Milestones

Track your progress:

- [ ] Successfully installed all dependencies
- [ ] Launched dashboard and viewed sample data
- [ ] Uploaded my own data to dashboard
- [ ] Created my first volcano plot
- [ ] Completed at least one Jupyter notebook
- [ ] Ran an R analysis script
- [ ] Exported significant genes list
- [ ] Created publication-ready figure
- [ ] Understood statistical thresholds
- [ ] Ready to apply to my research project

---

## 🤝 Community & Support

### Ways to Engage

1. **Ask questions**: Open GitHub issues
2. **Share examples**: Contribute notebooks
3. **Report bugs**: Help improve the tool
4. **Suggest features**: Tell us what you need
5. **Contribute code**: Submit pull requests

### Stay Updated

- ⭐ Star the repository on GitHub
- 👀 Watch for new releases
- 📧 Subscribe to release notifications
- 🐦 Follow project updates

---

**Ready to analyze some genes? Pick your path above and get started!** 🧬✨

*Need help? Check out the [USER_GUIDE.md](docs/USER_GUIDE.md) or open an issue on GitHub.*

