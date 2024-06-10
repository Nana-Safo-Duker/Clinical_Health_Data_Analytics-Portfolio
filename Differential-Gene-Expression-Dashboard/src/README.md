# 🔧 Source Code Directory

This directory contains utility Python scripts and modules for differential gene expression analysis.

## 📁 Contents

### `python_analysis.py`
**Python-based analysis template script**

A comprehensive Python script providing functions for:
- Data loading and validation
- Statistical analysis
- Visualization (volcano plots, MA plots)
- Results export

**When to use:**
- You prefer Python over R
- You want to customize analysis workflows
- You need to integrate with other Python pipelines
- You're building automated analysis scripts

**Usage:**
```python
# Import the module
from src.python_analysis import load_results, add_regulation_status, create_volcano_plot

# Load data
df = load_results("data/examples/sample_data.csv")

# Add regulation status
df = add_regulation_status(df, logfc_threshold=1.0, padj_threshold=0.05)

# Create plots
fig = create_volcano_plot(df, output_path="my_volcano_plot.png")
```

**Or run as standalone script:**
```bash
python src/python_analysis.py
```

### `utils/` (future)
Planned utility modules:
- `validators.py` - Data validation functions
- `plotters.py` - Visualization utilities
- `exporters.py` - Export format handlers
- `stats.py` - Statistical functions

## 🎯 Purpose

This directory provides:

1. **Reusable code** - Functions you can import in your own scripts
2. **Templates** - Starting points for custom analyses
3. **Utilities** - Helper functions for common tasks
4. **Integration** - Easy to incorporate into pipelines

## 🔄 Comparison with Other Tools

| Tool | Purpose | Best For |
|------|---------|----------|
| **src/python_analysis.py** | Python scripting | Automation, integration |
| **app/dashboard.py** | Interactive visualization | Exploration, publication plots |
| **R/*.R** | Statistical analysis | DESeq2/edgeR/limma from scratch |
| **notebooks/*.ipynb** | Education | Learning, step-by-step guidance |

## 💡 Examples

### Example 1: Basic Analysis

```python
from src.python_analysis import *

# Load and analyze
df = load_results("my_results.csv")
df = add_regulation_status(df)

# Get statistics
stats = calculate_statistics(df)
print_statistics(stats)

# Create plots
create_volcano_plot(df, "volcano.png")
create_ma_plot(df, "ma_plot.png")

# Export
export_results(df, "filtered_results.csv")
```

### Example 2: Custom Filtering

```python
from src.python_analysis import load_results
import pandas as pd

# Load data
df = load_results("results.csv")

# Custom filtering
high_confidence = df[
    (df['padj'] < 0.01) &  # Stricter p-value
    (df['log2FoldChange'].abs() > 2)  # Larger fold change
].copy()

print(f"Found {len(high_confidence)} high-confidence genes")

# Export
high_confidence.to_csv("high_confidence_genes.csv", index=False)
```

### Example 3: Batch Processing

```python
from src.python_analysis import *
import glob

# Process multiple result files
for filepath in glob.glob("data/processed/*.csv"):
    print(f"\nProcessing {filepath}...")
    
    df = load_results(filepath)
    df = add_regulation_status(df)
    
    # Create output filename
    base = filepath.split('/')[-1].replace('.csv', '')
    
    # Generate plots
    create_volcano_plot(df, f"plots/{base}_volcano.png")
    
    # Export significant genes
    sig_genes = df[df['regulation'] != 'Not Significant']
    sig_genes.to_csv(f"results/{base}_significant.csv", index=False)
```

## 🛠️ Development

### Adding New Features

1. **Create new functions** in `python_analysis.py`
2. **Document with docstrings**
3. **Add examples** to this README
4. **Write tests** in `tests/`
5. **Update version** in `setup.py`

### Code Style

- Follow PEP 8
- Use type hints
- Write comprehensive docstrings
- Include usage examples

### Testing

```bash
# Run tests
python -m pytest tests/

# Run with coverage
python -m pytest --cov=src tests/
```

## 📚 Dependencies

Required Python packages:
```
pandas>=2.0.0
numpy>=1.24.0
matplotlib>=3.7.0
seaborn>=0.12.0
scipy>=1.10.0
```

Install with:
```bash
pip install -r requirements.txt
```

## 🔗 Integration Examples

### With Jupyter Notebooks

```python
# In a Jupyter notebook
import sys
sys.path.append('..')

from src.python_analysis import *

df = load_results("../data/examples/sample_data.csv")
# Continue analysis...
```

### With Streamlit Dashboard

```python
# Custom analysis before dashboard
from src.python_analysis import load_results, add_regulation_status

# Pre-process data
df = load_results("raw_results.csv")
df = add_regulation_status(df, logfc_threshold=1.5)

# Save for dashboard
df.to_csv("processed_for_dashboard.csv", index=False)

# Then upload to dashboard
```

### With Snakemake Pipeline

```python
# In a Snakemake rule
rule analyze_degs:
    input:
        "results/{sample}_results.csv"
    output:
        "plots/{sample}_volcano.png",
        "processed/{sample}_significant.csv"
    script:
        "src/python_analysis.py"
```

## 📞 Support

- **Questions**: Open an issue on GitHub
- **Bug reports**: Include minimal reproducible example
- **Feature requests**: Describe use case and benefits
- **Contributions**: See CONTRIBUTING.md

## 🚀 Future Enhancements

Planned additions:
- [ ] Enhanced statistical tests
- [ ] More plot types (heatmaps, PCA)
- [ ] Gene set enrichment analysis
- [ ] Pathway analysis integration
- [ ] Batch effect correction
- [ ] Interactive HTML reports

## 📖 Related Documentation

- [Main README](../README.md) - Project overview
- [Getting Started](../GETTING_STARTED.md) - Quick start guide
- [User Guide](../docs/USER_GUIDE.md) - Comprehensive documentation
- [Notebooks](../notebooks/README.md) - Tutorial series

---

*Modular code for flexible analysis! 🧬💻*

