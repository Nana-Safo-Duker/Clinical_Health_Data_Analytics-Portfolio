# 📚 Jupyter Notebooks - Tutorial Series

This directory contains comprehensive Jupyter notebooks that guide you through differential gene expression analysis using Python.

## 📖 Notebooks

### 1. Introduction and Setup
**File**: `01_Introduction_and_Setup.ipynb`

Learn the fundamentals:
- What is differential gene expression?
- Setting up your environment
- Loading and inspecting data
- Understanding key metrics (log2FC, p-values)

### 2. Data Exploration and Visualization
**File**: `02_Data_Exploration_and_Visualization.ipynb`

Create publication-quality visualizations:
- Volcano plots (interactive and static)
- MA plots
- Distribution plots
- Heatmaps
- PCA plots

### 3. Statistical Analysis
**File**: `03_Statistical_Analysis.ipynb`

Understand the statistics:
- Significance thresholds
- Multiple testing correction
- False discovery rate (FDR)
- Effect size vs. statistical significance
- Gene filtering strategies

### 4. Advanced Analysis and Export
**File**: `04_Advanced_Analysis_and_Export.ipynb`

Advanced techniques:
- Gene set enrichment analysis
- Pathway analysis integration
- Batch effect correction
- Exporting results
- Creating publication-ready figures

## 🚀 Getting Started

### Prerequisites

```bash
# Install required packages
pip install -r ../requirements.txt
```

Required Python packages:
- pandas
- numpy
- matplotlib
- seaborn
- plotly
- scipy
- jupyter

### Running the Notebooks

1. **Start Jupyter**:
   ```bash
   jupyter notebook
   ```

2. **Or use JupyterLab**:
   ```bash
   jupyter lab
   ```

3. **Navigate to the notebooks directory** and open the notebooks in order.

## 📊 Sample Data

The notebooks use sample data located in `../data/examples/sample_data.csv`. This dataset contains:
- Real gene expression results
- Multiple conditions
- Statistical metrics (log2FC, p-values, adjusted p-values)

## 💡 Tips for Best Results

1. **Run cells in order**: Each notebook builds on the previous cells
2. **Modify parameters**: Feel free to experiment with thresholds and settings
3. **Use your own data**: Adapt the code to analyze your own datasets
4. **Save outputs**: Export plots and results as you go

## 🎯 Learning Objectives

By completing these notebooks, you will be able to:

- ✅ Load and preprocess gene expression data
- ✅ Perform quality control checks
- ✅ Create standard visualizations (volcano, MA plots)
- ✅ Apply appropriate statistical thresholds
- ✅ Identify differentially expressed genes
- ✅ Export results for downstream analysis
- ✅ Create publication-ready figures

## 📚 Additional Resources

### Books and Papers
- "RNA-seq Data Analysis: A Practical Approach" by Korpelainen et al.
- "Statistical Analysis of Gene Expression Microarray Data" by Speed (Ed.)

### Online Courses
- [Bioconductor RNA-seq Workflow](https://www.bioconductor.org/help/course-materials/)
- [Harvard Chan Bioinformatics Core Training](https://hbctraining.github.io/main/)

### Documentation
- [DESeq2](https://bioconductor.org/packages/DESeq2/)
- [edgeR](https://bioconductor.org/packages/edgeR/)
- [limma](https://bioconductor.org/packages/limma/)

## 🐛 Troubleshooting

### Common Issues

**Import errors**:
```bash
pip install --upgrade pandas numpy matplotlib seaborn plotly scipy
```

**Kernel issues**:
```bash
python -m ipykernel install --user --name=myenv
```

**Memory issues with large datasets**:
- Filter low-count genes early
- Use chunking for large files
- Consider using R scripts for very large analyses

## 📞 Getting Help

- **Issues**: Open an issue on GitHub
- **Questions**: Check the documentation
- **Contributions**: Pull requests are welcome!

---

## 🔄 Update History

- **v2.0.0** (2025): Comprehensive tutorial series with 4 notebooks
- **v1.0.0** (2024): Initial release

---

*Happy analyzing! 🧬✨*

