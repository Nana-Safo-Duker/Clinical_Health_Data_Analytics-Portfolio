# R Notebooks

This directory contains R notebooks for data analysis. To run these notebooks, you need:

1. R installed on your system
2. Jupyter with R kernel (IRkernel)
3. Required R packages installed

## Setup R Kernel for Jupyter

```r
# Install IRkernel
install.packages('IRkernel')

# Register the kernel
IRkernel::installspec()
```

## Running the Notebooks

Alternatively, you can run the R scripts directly:
- `../r_scripts/statistical_analysis.R`
- `../r_scripts/univariate_bivariate_multivariate.R`
- `../r_scripts/comprehensive_eda.R`
- `../r_scripts/ml_analysis.R`

## Required R Packages

```r
install.packages(c("ggplot2", "dplyr", "corrplot", "caret", "VIM", 
                   "psych", "randomForest", "e1071", "pROC", "xgboost",
                   "lightgbm", "GGally", "moments"))
```

