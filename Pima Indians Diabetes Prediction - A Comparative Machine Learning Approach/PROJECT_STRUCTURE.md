# Project Structure Overview

This document provides an overview of the project structure and what each component does.

## Directory Structure

```
pima-indians-diabetes/
│
├── data/                                    # Dataset directory
│   └── pima-indians-diabetes.csv            # Main dataset file
│
├── notebooks/                               # Jupyter notebooks and R Markdown files
│   ├── python/                              # Python notebooks
│   │   ├── 01_statistical_analysis.ipynb   # Descriptive & inferential statistics
│   │   ├── 02_eda_analysis.ipynb           # Exploratory data analysis
│   │   └── 03_ml_analysis.ipynb            # Machine learning analysis
│   │
│   └── r/                                   # R Markdown notebooks
│       ├── 01_statistical_analysis.Rmd     # Descriptive & inferential statistics (R)
│       ├── 02_eda_analysis.Rmd             # Exploratory data analysis (R)
│       └── 03_ml_analysis.Rmd              # Machine learning analysis (R)
│
├── scripts/                                 # Executable scripts
│   ├── python/                              # Python scripts
│   │   └── univariate_bivariate_multivariate_analysis.py
│   │
│   └── r/                                   # R scripts
│       └── univariate_bivariate_multivariate_analysis.R
│
├── outputs/                                 # Generated outputs (plots, results)
│   └── .gitkeep                             # Keeps directory in git
│
├── docs/                                    # Additional documentation
│   └── .gitkeep                             # Keeps directory in git
│
├── requirements.txt                         # Python dependencies
├── requirements-r.txt                       # R dependencies
├── LICENSE                                  # License file
├── .gitignore                               # Git ignore rules
├── .gitattributes                           # Git attributes for line endings
├── README.md                                # Main project documentation
└── PROJECT_STRUCTURE.md                     # This file
```

## File Descriptions

### Data Files
- **data/pima-indians-diabetes.csv**: The main dataset containing 768 observations with 8 features and 1 target variable.

### Python Notebooks
1. **01_statistical_analysis.ipynb**: 
   - Descriptive statistics (mean, median, std, etc.)
   - Inferential statistics (t-tests, chi-square tests)
   - Correlation analysis
   - Confidence intervals

2. **02_eda_analysis.ipynb**: 
   - Univariate analysis (distributions, box plots)
   - Bivariate analysis (feature vs outcome)
   - Multivariate analysis (correlation heatmaps, PCA)
   - Outlier detection

3. **03_ml_analysis.ipynb**: 
   - Data preprocessing
   - Multiple ML algorithms (Logistic Regression, Random Forest, SVM, etc.)
   - Model evaluation and comparison
   - ROC curves and cross-validation

### R Notebooks (R Markdown)
1. **01_statistical_analysis.Rmd**: 
   - Same as Python version but in R
   - Uses R-specific packages (psych, car, corrplot)

2. **02_eda_analysis.Rmd**: 
   - EDA using ggplot2 and other R visualization packages
   - PCA analysis using R's prcomp function

3. **03_ml_analysis.Rmd**: 
   - ML analysis using caret package
   - Multiple algorithms with R implementations

### Scripts
- **Python Script**: Standalone script for univariate, bivariate, and multivariate analysis
- **R Script**: Standalone script for the same analysis in R

### Configuration Files
- **requirements.txt**: Python package dependencies
- **requirements-r.txt**: R package dependencies
- **.gitignore**: Git ignore rules for Python, R, and output files
- **.gitattributes**: Git attributes for consistent line endings

### Documentation
- **README.md**: Comprehensive project documentation
- **LICENSE**: MIT License for project code
- **PROJECT_STRUCTURE.md**: This file

## Analysis Workflow

### Recommended Order

1. **Start with Statistical Analysis**:
   - Run `01_statistical_analysis.ipynb` (Python) or `01_statistical_analysis.Rmd` (R)
   - Understand data distributions and basic statistics

2. **Perform Exploratory Data Analysis**:
   - Run `02_eda_analysis.ipynb` (Python) or `02_eda_analysis.Rmd` (R)
   - Explore relationships between features and outcome

3. **Build Machine Learning Models**:
   - Run `03_ml_analysis.ipynb` (Python) or `03_ml_analysis.Rmd` (R)
   - Compare different algorithms and select the best model

### Alternative: Use Scripts

You can also run the analysis scripts directly:
- Python: `python scripts/python/univariate_bivariate_multivariate_analysis.py`
- R: `Rscript scripts/r/univariate_bivariate_multivariate_analysis.R`

## Outputs

All generated outputs (plots, results, etc.) should be saved in the `outputs/` directory. This directory is ignored by git (except for .gitkeep) to avoid committing large files.

## Dependencies

### Python
- Core: pandas, numpy, scipy
- Visualization: matplotlib, seaborn, plotly
- Machine Learning: scikit-learn, xgboost
- Statistics: statsmodels
- Jupyter: jupyter, ipykernel, notebook

### R
- Core: dplyr, tidyverse, data.table
- Statistics: stats, car, psych
- Visualization: ggplot2, GGally, corrplot, VIM
- Machine Learning: caret, randomForest, e1071, glmnet, gbm, rpart
- Reporting: rmarkdown, knitr
- Missing Data: mice, naniar

## Notes

- All notebooks assume the dataset is located at `../../data/pima-indians-diabetes.csv` relative to the notebook location
- Scripts also assume the same relative path
- Outputs are saved to `../../outputs/` relative to script/notebook location
- The project uses consistent random seeds (42) for reproducibility

## GitHub Repository Setup

To set up this project as a GitHub repository:

1. Initialize git repository:
```bash
git init
```

2. Add all files:
```bash
git add .
```

3. Commit:
```bash
git commit -m "Initial commit: Pima Indians Diabetes Analysis"
```

4. Create repository on GitHub and push:
```bash
git remote add origin <repository-url>
git push -u origin main
```

## License

- Dataset: UCI Machine Learning Repository license (for research and educational purposes)
- Code: MIT License (see LICENSE file)


