# Setup Guide

## Python Setup

### 1. Create Virtual Environment

```bash
python -m venv venv
```

### 2. Activate Virtual Environment

**Windows:**
```bash
venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Launch Jupyter Notebook

```bash
jupyter notebook
```

## R Setup

### 1. Install R

Download and install R from: https://www.r-project.org/

### 2. Install RStudio (Optional but Recommended)

Download and install RStudio from: https://www.rstudio.com/

### 3. Install Required R Packages

Open R or RStudio and run:

```r
install.packages(c("ggplot2", "dplyr", "corrplot", "caret", "randomForest", 
                   "e1071", "pROC", "VIM", "moments", "gridExtra", "tidyr"))
```

### 4. Install IRkernel for Jupyter (Optional)

To use R in Jupyter notebooks:

```r
install.packages('IRkernel')
IRkernel::installspec()
```

### 5. Run R Scripts

```r
source("scripts/r/statistical_analysis.R")
source("scripts/r/univariate_bivariate_multivariate_analysis.R")
source("scripts/r/comprehensive_eda.R")
source("scripts/r/ml_analysis.R")
```

## Running Analysis

### Python Notebooks

1. Navigate to the project directory
2. Launch Jupyter: `jupyter notebook`
3. Open notebooks from `notebooks/python/` directory
4. Run cells sequentially

### Python Scripts

```bash
# From project root
python scripts/python/comprehensive_eda.py
python scripts/python/univariate_bivariate_multivariate_analysis.py
python scripts/python/ml_analysis.py
```

### R Scripts

```r
# From R or RStudio
setwd("path/to/project")
source("scripts/r/statistical_analysis.R")
source("scripts/r/univariate_bivariate_multivariate_analysis.R")
source("scripts/r/comprehensive_eda.R")
source("scripts/r/ml_analysis.R")
```

### R Notebooks

1. Open RStudio
2. Open `.Rmd` files from `notebooks/r/` directory
3. Click "Knit" to run the entire notebook
4. Or run chunks individually

## Project Structure

```
diabetes_binary_health_indicators_BRFSS2021/
├── data/                          # Dataset
├── notebooks/
│   ├── python/                    # Python Jupyter notebooks
│   └── r/                         # R notebooks (.Rmd or .ipynb)
├── scripts/
│   ├── python/                    # Python scripts
│   └── r/                         # R scripts
└── results/
    ├── figures/                   # Generated visualizations
    └── models/                    # Saved models and metrics
```

## Troubleshooting

### Python Issues

1. **Import Error**: Make sure virtual environment is activated and dependencies are installed
2. **Path Error**: Run scripts from project root directory
3. **Memory Error**: Consider using a sample of the data for testing

### R Issues

1. **Package Not Found**: Install missing packages using `install.packages()`
2. **Path Error**: Use `setwd()` to set working directory to project root
3. **Memory Error**: Consider using a sample of the data for testing

## Notes

- R notebooks are provided as both `.Rmd` (R Markdown) and can be converted to `.ipynb` (Jupyter) format
- All scripts assume the working directory is the project root
- Results are saved in the `results/` directory
- Large data files should be in the `data/` directory

