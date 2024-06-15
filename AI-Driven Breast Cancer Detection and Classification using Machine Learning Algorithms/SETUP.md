# Setup Guide

## Python Environment Setup

### 1. Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Verify Installation

```bash
python -c "import pandas, numpy, sklearn, matplotlib, seaborn; print('All packages installed successfully!')"
```

## R Environment Setup

### 1. Install R Packages

Open R or RStudio and run:

```r
# Install required packages
packages <- c("dplyr", "tidyr", "readr", "ggplot2", "plotly", "corrplot", 
              "VIM", "naniar", "stats", "car", "psych", "Hmisc", "caret", 
              "randomForest", "e1071", "xgboost", "glmnet", "rpart", "ranger", 
              "pROC", "rmarkdown", "knitr", "tidyverse", "FactoMineR", "factoextra")

install.packages(packages)
```

### 2. Verify Installation

```r
# Check if all packages are installed
all_installed <- all(packages %in% installed.packages()[,"Package"])
if (all_installed) {
  print("All packages installed successfully!")
} else {
  missing <- packages[!packages %in% installed.packages()[,"Package"]]
  print(paste("Missing packages:", paste(missing, collapse = ", ")))
}
```

## Running the Analysis

### Python Scripts

```bash
# From project root directory
python scripts/python/statistical_analysis.py
python scripts/python/univariate_bivariate_multivariate_analysis.py
python scripts/python/comprehensive_eda.py
python scripts/python/ml_analysis.py
```

### Python Notebooks

```bash
# Start Jupyter Notebook
jupyter notebook

# Navigate to notebooks/python/ and open the desired notebook
```

### R Scripts

```r
# From R or RStudio, set working directory to project root
setwd("path/to/breast_cancer")

# Run scripts
source("scripts/r/statistical_analysis.R")
source("scripts/r/univariate_bivariate_multivariate_analysis.R")
source("scripts/r/comprehensive_eda.R")
source("scripts/r/ml_analysis.R")
```

### R Notebooks

```r
# In RStudio, open the .Rmd files in notebooks/r/
# Click "Knit" to render the notebooks
```

## Project Structure

Make sure your project structure looks like this:

```
breast_cancer/
├── data/
│   └── breast_cancer.csv
├── notebooks/
│   ├── python/
│   └── r/
├── scripts/
│   ├── python/
│   └── r/
├── results/
│   ├── univariate/
│   ├── bivariate/
│   ├── multivariate/
│   ├── eda/
│   └── ml/
├── requirements.txt
├── requirements_r.txt
└── README.md
```

## Troubleshooting

### Python Issues

1. **ModuleNotFoundError**: Make sure you've installed all requirements
   ```bash
   pip install -r requirements.txt
   ```

2. **Path Issues**: Make sure you're running scripts from the project root directory

3. **Jupyter Issues**: Make sure Jupyter is installed
   ```bash
   pip install jupyter
   ```

### R Issues

1. **Package Installation Errors**: Try installing packages individually
   ```r
   install.packages("package_name")
   ```

2. **Path Issues**: Make sure your working directory is set correctly
   ```r
   getwd()  # Check current directory
   setwd("path/to/breast_cancer")  # Set to project root
   ```

## Next Steps

1. Run the statistical analysis scripts
2. Review the results in the `results/` directory
3. Explore the notebooks for interactive analysis
4. Review the README.md for detailed project information

## Support

For issues or questions, please open an issue in the repository.

