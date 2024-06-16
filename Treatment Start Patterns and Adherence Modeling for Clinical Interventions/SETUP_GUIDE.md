# Setup Guide

## Quick Start

### 1. Clone the Repository
```bash
git clone <repository-url>
cd mock_treatment_starts_2016
```

### 2. Python Setup

#### Using Conda (Recommended)
```bash
# Create and activate environment
conda env create -f environment.yml
conda activate clinical_data_analysis

# Verify installation
python --version
jupyter --version
```

#### Using pip
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. R Setup

```r
# Install R packages
source("packages.R")

# Or install manually
install.packages(c("dplyr", "ggplot2", "tidyr", "lubridate", 
                   "corrplot", "gridExtra", "moments", "caret",
                   "randomForest", "gbm", "xgboost", "VIM"))
```

### 4. Verify Installation

#### Python
```bash
python -c "import pandas, numpy, matplotlib, seaborn, sklearn; print('All packages installed!')"
```

#### R
```r
library(dplyr)
library(ggplot2)
library(caret)
# If no errors, packages are installed correctly
```

## Running Analyses

### Python Notebooks
1. Start Jupyter Notebook:
   ```bash
   jupyter notebook
   ```
2. Navigate to `notebooks/python/`
3. Open and run notebooks in order:
   - `01_statistical_analysis.ipynb`
   - `02_univariate_bivariate_multivariate_analysis.ipynb`
   - `03_comprehensive_eda.ipynb`
   - `04_ml_analysis.ipynb`

### Python Scripts
```bash
# From project root
python scripts/python/univariate_bivariate_multivariate_analysis.py
python scripts/python/comprehensive_eda.py
```

### R Notebooks
1. Open RStudio
2. Open `.Rmd` files in `notebooks/r/`
3. Knit to HTML or run interactively

### R Scripts
```r
# From project root in R
source("scripts/r/univariate_bivariate_multivariate_analysis.R")
source("scripts/r/comprehensive_eda.R")
```

## Troubleshooting

### Python Issues

**Issue**: Package not found
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Issue**: Jupyter not found
```bash
pip install jupyter
```

### R Issues

**Issue**: Package installation fails
```r
# Update R to latest version
# Install packages from CRAN
install.packages("package_name", dependencies = TRUE)
```

**Issue**: RStudio not recognizing packages
```r
# Restart RStudio
# Check library path
.libPaths()
```

## Next Steps

1. Explore the data using the notebooks
2. Run the analyses
3. Review the results
4. Modify and extend the analyses as needed

## Getting Help

- Check the README.md for detailed information
- Review the notebook comments and markdown cells
- Open an issue on GitHub for bugs or questions


