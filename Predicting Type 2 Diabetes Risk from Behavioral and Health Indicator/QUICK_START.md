# Quick Start Guide

## Prerequisites

- Python 3.7+ or R 4.0+
- Jupyter Notebook (for Python notebooks)
- RStudio (for R notebooks, optional)

## Quick Start - Python

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Analysis

**Option A: Use Jupyter Notebooks**
```bash
jupyter notebook notebooks/python/01_statistical_analysis.ipynb
```

**Option B: Run Python Scripts**
```bash
# From project root
python scripts/python/comprehensive_eda.py
python scripts/python/univariate_bivariate_multivariate_analysis.py
python scripts/python/ml_analysis.py
```

## Quick Start - R

### 1. Install R Packages
```r
install.packages(c("ggplot2", "dplyr", "corrplot", "caret", "randomForest", 
                   "e1071", "pROC", "VIM", "moments", "gridExtra", "tidyr"))
```

### 2. Run Analysis

**Option A: Use R Scripts**
```r
# From R or RStudio
setwd("path/to/project/root")
source("scripts/r/statistical_analysis.R")
source("scripts/r/comprehensive_eda.R")
source("scripts/r/univariate_bivariate_multivariate_analysis.R")
source("scripts/r/ml_analysis.R")
```

**Option B: Use R Notebooks (.Rmd)**
- Open `.Rmd` files in RStudio
- Click "Knit" to run the entire notebook
- Or run chunks individually

## Expected Output

After running the analysis, you should see:
- **Figures**: Saved in `results/figures/` directory
- **Models**: Performance metrics saved in `results/models/` directory
- **Console Output**: Statistical summaries and model performance metrics

## File Paths

All scripts and notebooks assume:
- **Working Directory**: Project root (`diabetes_binary_health_indicators_BRFSS2021/`)
- **Data Path**: `data/diabetes_binary_health_indicators_BRFSS2021.csv`
- **Output Path**: `results/figures/` and `results/models/`

## Troubleshooting

### Path Issues
If you get file not found errors:
- Make sure you're running from the project root directory
- Check that the data file is in the `data/` directory
- Verify the `results/` directory exists

### Import Errors
- **Python**: Make sure virtual environment is activated and dependencies are installed
- **R**: Install missing packages using `install.packages("package_name")`

### Memory Issues
- The dataset is large (236K records)
- Consider using a sample for testing
- Close other applications to free up memory

## Next Steps

1. Run the statistical analysis notebook/script
2. Review the comprehensive EDA
3. Explore the univariate/bivariate/multivariate analysis
4. Train and evaluate machine learning models
5. Review generated visualizations and results

## Support

For issues or questions:
- Check the README.md for detailed documentation
- Review SETUP.md for installation instructions
- Check PROJECT_SUMMARY.md for an overview of all components

