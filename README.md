# 🧬 Differential Gene Expression Dashboard

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/streamlit-1.28%2B-red)](https://streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://img.shields.io/badge/tests-passing-brightgreen)](tests/)

A comprehensive, interactive web dashboard for analyzing and visualizing differential gene expression data from RNA-seq experiments. Built with Streamlit, this tool provides researchers with publication-quality visualizations and flexible data exploration capabilities.

![Dashboard Preview](docs/images/dashboard-preview.png)

---

## ✨ Features

### 🎯 Core Capabilities
- **📊 Multiple Visualization Types**
  - Interactive volcano plots (Plotly & Altair)
  - MA plots for expression-dependent bias detection
  - Top genes bar charts
  - Distribution analysis plots
  
- **🔧 Flexible Data Input**
  - Works with any CSV format
  - User-defined column mapping
  - Compatible with DESeq2, edgeR, limma outputs
  
- **🔍 Advanced Filtering**
  - Adjustable log2 fold change thresholds
  - P-value significance cutoffs
  - Regulation status filtering
  - Multi-gene search functionality
  
- **💾 Export Options**
  - CSV format (universal)
  - Excel format (formatted)
  - Complete or filtered datasets
  
- **📈 Real-time Statistics**
  - Total genes analyzed
  - Significant genes count
  - Up/downregulated gene counts
  - Distribution metrics

### 🛡️ Quality Assurance
- Comprehensive data validation
- Error checking and user-friendly messages
- Automated test suite (100% passing)
- Quality control visualizations

---

## 🚀 Quick Start

### Option 0: Streamlit Cloud (Recommended - No Installation!)

🌐 **Deploy instantly to Streamlit Cloud:**

1. Go to https://share.streamlit.io/
2. Sign in with GitHub
3. Select repository: `Nana-Safo-Duker/Differential-Gene-Expression-Dashboard`
4. Set main file: `app/dashboard.py`
5. Click "Deploy!"

Your dashboard will be live at: `https://[your-app].streamlit.app/`

📖 **Full deployment guide:** See [STREAMLIT_CLOUD_DEPLOY.md](STREAMLIT_CLOUD_DEPLOY.md)

---

### Option 1: Python Dashboard (Visualization)

```bash
# Clone the repository
git clone https://github.com/yourusername/Differential-Gene-Expression.git
cd Differential-Gene-Expression

# Install Python dependencies
pip install -r requirements.txt

# Launch the dashboard
streamlit run app/dashboard.py
```

Or use the quick start script:
```bash
python scripts/quick_start.py
```

**Try with sample data**:
1. Launch the dashboard
2. Upload `data/examples/sample_data.csv`
3. Explore interactive visualizations
4. Export your results

### Option 2: R Analysis (Full Pipeline)

```r
# Install R dependencies
if (!requireNamespace("BiocManager", quietly = TRUE))
    install.packages("BiocManager")

BiocManager::install(c("DESeq2", "edgeR", "limma"))
install.packages(c("ggplot2", "pheatmap", "ggrepel", "dplyr"))

# Run analysis
source("R/deseq2_analysis.R")
# See R/README.md for detailed usage
```

### Option 3: Jupyter Notebooks (Learning)

```bash
# Install dependencies
pip install -r requirements.txt jupyter

# Launch Jupyter
jupyter notebook notebooks/01_Introduction_and_Setup.ipynb
```

---

## 🔄 Workflows

### Workflow 1: Complete Analysis (Raw Counts → Results)
```
Raw Data → R Scripts → Dashboard → Export
```
1. Place count matrix in `data/raw/counts.csv`
2. Run `Rscript R/deseq2_analysis.R`
3. Upload results to dashboard for visualization
4. Export significant genes

### Workflow 2: Visualization Only (Existing Results)
```
Results CSV → Dashboard → Explore & Export
```
1. Have DESeq2/edgeR/limma results as CSV
2. Launch dashboard: `streamlit run app/dashboard.py`
3. Upload and visualize interactively

### Workflow 3: Learning Path
```
Notebooks → Practice → Apply to Your Data
```
1. Start with `notebooks/01_Introduction_and_Setup.ipynb`
2. Progress through tutorial series
3. Apply techniques to your own data

---

## 📊 Detailed Usage

### Python Dashboard Usage

### Step 1: Prepare Your Data

Export your differential expression results as CSV:

```R
# From DESeq2
results_df <- as.data.frame(results(dds))
results_df$Gene <- rownames(results_df)
write.csv(results_df, "my_results.csv", row.names=FALSE)
```

**Required columns:**
- Gene identifiers
- log2 Fold Change values
- Adjusted p-values

**Optional columns:**
- Regulation status
- Base mean expression
- Raw p-values

### Step 2: Launch Dashboard

```bash
streamlit run app/dashboard.py
```

### Step 3: Analyze

1. **Upload** your CSV file
2. **Map** your column names
3. **Set** significance thresholds
4. **Explore** interactive visualizations
5. **Search** for specific genes
6. **Export** significant genes

---

## 📁 Project Structure

```
Differential-Gene-Expression/
├── 📱 app/                          # Streamlit Dashboard
│   ├── dashboard.py                 # Main application
│   └── utils/                       # Utility modules
│
├── 📊 R/                            # R Analysis Scripts
│   ├── deseq2_analysis.R            # DESeq2 pipeline
│   ├── edger_analysis.R             # edgeR pipeline
│   ├── limma_analysis.R             # limma-voom pipeline
│   └── README.md                    # R documentation
│
├── 📚 notebooks/                    # Jupyter Tutorials
│   ├── 01_Introduction_and_Setup.ipynb
│   ├── 02_Data_Exploration_and_Visualization.ipynb
│   ├── 03_Statistical_Analysis.ipynb
│   ├── 04_Advanced_Analysis_and_Export.ipynb
│   └── README.md                    # Notebook guide
│
├── 📁 data/                         # Data Storage
│   ├── raw/                         # Raw input data
│   ├── processed/                   # Analysis outputs
│   ├── examples/                    # Sample datasets
│   └── README.md                    # Data guide
│
├── 🧪 tests/                        # Test Suite
│   ├── test_dashboard.py            # Dashboard tests
│   └── __init__.py
│
├── 📖 docs/                         # Documentation
│   ├── USER_GUIDE.md
│   ├── INSTALLATION.md
│   ├── IMPROVEMENTS.md
│   └── images/
│
├── 🔧 scripts/                      # Utility Scripts
│   └── quick_start.py
│
├── 📄 Project Files
│   ├── README.md                    # This file
│   ├── LICENSE
│   ├── CONTRIBUTING.md
│   ├── CHANGELOG.md
│   ├── PROJECT_ORGANIZATION.md      # Detailed structure guide
│   ├── requirements.txt
│   ├── requirements-dev.txt
│   └── setup.py
│
└── .github/                         # GitHub Actions
    └── workflows/
```

📘 See [PROJECT_ORGANIZATION.md](PROJECT_ORGANIZATION.md) for detailed structure and workflows.

---

## 🔧 Requirements

- Python 3.8 or higher
- streamlit >= 1.28.0
- pandas >= 2.0.0
- numpy >= 1.24.0
- altair >= 5.0.0
- plotly >= 5.17.0
- openpyxl >= 3.1.0

See `requirements.txt` for complete list.

---

## 📖 Documentation

- **[User Guide](docs/USER_GUIDE.md)** - Comprehensive tutorials and examples
- **[API Documentation](docs/API.md)** - Function reference
- **[Improvements](docs/IMPROVEMENTS.md)** - Feature comparison and enhancements
- **[Contributing](CONTRIBUTING.md)** - How to contribute

---

## 🧪 Testing

Run the test suite to verify installation:

```bash
python tests/test_dashboard.py
```

Expected output:
```
✅ Test 1: Loading sample data - PASSED
✅ Test 2: Validating required columns - PASSED
✅ Test 3: Checking optional columns - PASSED
✅ Test 4: Testing calculations - PASSED
✅ Test 5: Checking dependencies - PASSED
✅ Test 6: Checking file structure - PASSED
✅ Test 7: Testing export functions - PASSED

📊 Final Score: 7/7 (100%) ✅
```

---

## 🎯 Use Cases & Tools

### 🧬 Research Applications
- RNA-seq differential expression analysis
- Microarray data visualization  
- Quality control for sequencing experiments
- Candidate gene identification
- Pathway analysis preparation
- Biomarker discovery
- Drug response studies

### 🛠️ Analysis Tools Provided

#### Python Dashboard (Visualization)
- ✅ Interactive volcano plots
- ✅ MA plots and distributions
- ✅ Gene filtering and search
- ✅ CSV/Excel export
- ✅ Publication-ready figures

#### R Scripts (Statistical Analysis)
- ✅ **DESeq2**: Complete pipeline with QC plots
- ✅ **edgeR**: GLM-based analysis
- ✅ **limma-voom**: Fast analysis for large datasets
- ✅ Automated filtering and normalization

#### Jupyter Notebooks (Education)
- ✅ Step-by-step tutorials
- ✅ Interactive learning
- ✅ Customizable analyses
- ✅ Best practices guidance

### 🔄 Compatible with Results From
- ✅ DESeq2 (R/Bioconductor)
- ✅ edgeR (R/Bioconductor)
- ✅ limma (R/Bioconductor)
- ✅ Any tool producing log2FC and adjusted p-values

---

## 📸 Screenshots

### Volcano Plot
![Volcano Plot](docs/images/volcano-plot.png)

### MA Plot
![MA Plot](docs/images/ma-plot.png)

### Top Genes
![Top Genes](docs/images/top-genes.png)

---

## 🤝 Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

### Development Setup

```bash
# Clone repository
git clone https://github.com/yourusername/Differential-Gene-Expression.git
cd Differential-Gene-Expression

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run tests
python tests/test_dashboard.py
```

---

## 📝 Citation

If you use this dashboard in your research, please cite:

```bibtex
@software{differential_gene_expression_dashboard,
  title = {Differential Gene Expression Dashboard},
  author = {Your Name},
  year = {2025},
  url = {https://github.com/yourusername/Differential-Gene-Expression}
}
```

---

## 📚 Complete Documentation Index

| Document | Purpose |
|----------|---------|
| **README.md** | Project overview (you are here) |
| **[GETTING_STARTED.md](GETTING_STARTED.md)** | 🚀 Quick start guide for new users |
| **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** | ⚡ Fast access to commands and info |
| **[PROJECT_ORGANIZATION.md](PROJECT_ORGANIZATION.md)** | 📁 Detailed structure and workflows |
| **[PROJECT_TREE.md](PROJECT_TREE.md)** | 🌳 Complete file tree visualization |
| **[docs/USER_GUIDE.md](docs/USER_GUIDE.md)** | 📖 Comprehensive user guide |
| **[R/README.md](R/README.md)** | 📊 R scripts documentation |
| **[notebooks/README.md](notebooks/README.md)** | 📚 Jupyter tutorials guide |
| **[src/README.md](src/README.md)** | 💻 Python modules documentation |

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- Visualizations powered by [Plotly](https://plotly.com/) and [Altair](https://altair-viz.github.io/)
- Data processing with [Pandas](https://pandas.pydata.org/) and [NumPy](https://numpy.org/)
- Inspired by bioinformatics community needs

---

## 📧 Contact & Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/Differential-Gene-Expression/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/Differential-Gene-Expression/discussions)
- **Email**: your.email@example.com

---

## 🗺️ Roadmap

### Current Version: 2.0
- ✅ Interactive visualizations
- ✅ Flexible column mapping
- ✅ Export functionality
- ✅ Gene search
- ✅ Comprehensive documentation

### Future Plans
- [ ] Gene Set Enrichment Analysis (GSEA)
- [ ] Pathway enrichment integration
- [ ] Heatmap visualizations
- [ ] Batch comparison mode
- [ ] PDF report generation
- [ ] Docker containerization

---

## ⭐ Star History

If you find this project useful, please consider giving it a star! ⭐

---

## 📊 Project Statistics

![GitHub stars](https://img.shields.io/github/stars/yourusername/Differential-Gene-Expression?style=social)
![GitHub forks](https://img.shields.io/github/forks/yourusername/Differential-Gene-Expression?style=social)
![GitHub issues](https://img.shields.io/github/issues/yourusername/Differential-Gene-Expression)
![GitHub pull requests](https://img.shields.io/github/issues-pr/yourusername/Differential-Gene-Expression)

---

<div align="center">
  <b>Made with ❤️ for the bioinformatics community</b>
  <br><br>
  <sub>Built with Python • Streamlit • Plotly • Altair</sub>
</div>
