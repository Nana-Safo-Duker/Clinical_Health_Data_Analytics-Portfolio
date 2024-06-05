# 🧬 Advanced Differential Gene Expression Dashboard

A comprehensive, interactive Streamlit dashboard for analyzing and visualizing differential gene expression data.

## 🌟 Features

### Core Capabilities
- **Flexible Column Mapping**: Automatically adapts to any CSV structure - you select which columns contain your data
- **Interactive Visualizations**: 
  - Volcano plots (Altair & Plotly)
  - MA plots
  - Top genes bar charts
  - Distribution plots
- **Advanced Filtering**: 
  - Customizable log2FC and p-value thresholds
  - Regulation status filtering
  - Gene search functionality
- **Statistical Summaries**: Comprehensive gene expression statistics
- **Export Options**: Download results in CSV or Excel format
- **Data Validation**: Automatic validation of uploaded data with helpful error messages

### Enhanced Features Over Original
1. ✅ **Multiple Visualization Engines**: Choose between Altair and Plotly for different use cases
2. ✅ **MA Plot Support**: Visualize fold change vs mean expression
3. ✅ **Distribution Analysis**: View log2FC and p-value distributions
4. ✅ **Top Genes Chart**: Automatically identify and visualize most DE genes
5. ✅ **Gene Search**: Quickly find specific genes of interest
6. ✅ **Excel Export**: Export to formatted Excel files
7. ✅ **Better Error Handling**: Comprehensive validation and user-friendly error messages
8. ✅ **Enhanced UI/UX**: Modern, intuitive interface with better organization
9. ✅ **Statistical Metrics**: Real-time summary statistics
10. ✅ **Publication-Ready Plots**: High-quality, customizable visualizations

## 📋 Requirements

- Python 3.8 or higher
- See `requirements.txt` for package dependencies

## 🚀 Installation

### Option 1: Using pip

```bash
# Clone or download this repository
cd Differential-Gene-Expression

# Install dependencies
pip install -r requirements.txt
```

### Option 2: Using conda

```bash
# Create a new conda environment
conda create -n gene-expression python=3.10

# Activate the environment
conda activate gene-expression

# Install dependencies
pip install -r requirements.txt
```

## 💻 Usage

### Starting the Dashboard

```bash
streamlit run Differential_Gene_Dashboard_Enhanced.py
```

The dashboard will open in your default web browser at `http://localhost:8501`

### Using the Dashboard

1. **Upload Your Data**
   - Click "Browse files" in the sidebar
   - Select your CSV file containing gene expression data

2. **Map Your Columns**
   - Select which columns contain:
     - Gene names
     - log2 Fold Change values
     - Adjusted P-values
     - (Optional) Regulation status, base mean, raw p-values

3. **Set Thresholds**
   - Adjust log2 Fold Change threshold (default: ±1.0)
   - Adjust adjusted P-value threshold (default: 0.05)

4. **Explore Visualizations**
   - Navigate through tabs to view different plot types
   - Interact with plots (zoom, pan, hover for details)

5. **Search and Filter**
   - Use regulation filters to focus on up/downregulated genes
   - Search for specific genes by name

6. **Export Results**
   - Download significant genes as CSV or Excel
   - Download all filtered data

## 📊 Expected Data Format

Your CSV file should contain at minimum:

| Gene | log2FoldChange | padj |
|------|----------------|------|
| TP53 | 2.5 | 0.001 |
| BRCA1 | -1.8 | 0.01 |
| EGFR | 3.2 | 0.0001 |

**Required columns:**
- Gene identifiers (any format)
- log2 Fold Change values (numeric)
- Adjusted P-values (numeric)

**Optional columns:**
- `regulation`: Upregulated/Downregulated status
- `baseMean`: Mean expression values (enables MA plot)
- `pvalue`: Raw p-values
- Any other metadata columns

### Compatible Data Sources

This dashboard works with output from popular differential expression tools:
- ✅ DESeq2 (R)
- ✅ edgeR (R)
- ✅ limma (R)
- ✅ Any tool producing log2FC and adjusted p-values

## 🎨 Visualization Guide

### Volcano Plot
- **X-axis**: log2 Fold Change
- **Y-axis**: -log10 Adjusted P-value
- **Colors**: 
  - 🔴 Red: Upregulated (significant)
  - 🟢 Green: Downregulated (significant)
  - ⚪ Gray: Not significant

### MA Plot
- **X-axis**: log10 Mean Expression
- **Y-axis**: log2 Fold Change
- Shows relationship between expression level and fold change

### Top Genes Chart
- Horizontal bar chart showing most differentially expressed genes
- Automatically selects top upregulated and downregulated genes

### Distribution Plots
- **log2FC Distribution**: Shows overall expression changes
- **P-value Distribution**: Shows statistical significance distribution

## 🔧 Customization

### Modifying Thresholds
Default thresholds can be changed in the code:

```python
# In the slider definitions
logfc_threshold = st.slider(
    "log₂ Fold Change Threshold",
    min_value=0.0,
    max_value=5.0,
    value=1.0,  # Change this default value
    step=0.1
)

padj_threshold = st.slider(
    "Adjusted P-value Threshold",
    min_value=0.0,
    max_value=0.1,
    value=0.05,  # Change this default value
    step=0.005
)
```

### Changing Color Schemes
Modify the color maps in the plotting functions:

```python
color_map = {
    'Upregulated': '#d62728',      # Change to your preferred color
    'Downregulated': '#2ca02c',    # Change to your preferred color
    'Not Significant': '#7f7f7f'   # Change to your preferred color
}
```

## 📝 Example Workflow

1. Export results from DESeq2:
```R
# In R
write.csv(results, "deseq2_results.csv", row.names=TRUE)
```

2. Upload to dashboard
3. Map columns: 
   - Gene: Row names
   - log2FoldChange: log2FoldChange
   - padj: padj
4. Adjust thresholds as needed
5. Explore visualizations
6. Export significant genes

## 🐛 Troubleshooting

### Common Issues

**Issue**: "Data validation failed"
- **Solution**: Ensure your log2FC and p-value columns contain numeric values

**Issue**: "No significant genes found"
- **Solution**: Try relaxing your thresholds (lower log2FC, higher p-value cutoff)

**Issue**: "MA Plot not available"
- **Solution**: Ensure you've mapped a column containing mean expression values

**Issue**: Dashboard won't start
- **Solution**: Check that all dependencies are installed: `pip install -r requirements.txt`

## 📚 Additional Resources

- [DESeq2 Documentation](https://bioconductor.org/packages/release/bioc/html/DESeq2.html)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Plotly Documentation](https://plotly.com/python/)

## 🤝 Contributing

Suggestions and improvements are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests

## 📄 License

This dashboard is provided as-is for research and educational purposes.

## 🙏 Acknowledgments

Built with:
- Streamlit
- Plotly & Altair for visualizations
- Pandas & NumPy for data processing

## 📧 Support

For questions or issues:
1. Check the Troubleshooting section
2. Review the expected data format
3. Ensure all dependencies are properly installed

---

**Version**: 2.0 Enhanced  
**Last Updated**: October 2025  
**Status**: Production Ready ✅

