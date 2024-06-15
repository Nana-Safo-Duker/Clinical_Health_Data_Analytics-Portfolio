# Project Summary

## Cancer Incidence Data Analysis Project

This project provides a comprehensive statistical and machine learning analysis of cancer incidence data at the county level across the United States.

## Project Structure

```
incd/
├── data/
│   └── incd.csv                    # Main dataset
├── notebooks/
│   ├── python/
│   │   ├── 01_descriptive_inferential_exploratory_statistics.ipynb
│   │   ├── 02_univariate_bivariate_multivariate_analysis.ipynb
│   │   ├── 03_comprehensive_eda.ipynb
│   │   └── 04_ml_analysis.ipynb
│   └── r/
│       ├── 01_descriptive_inferential_exploratory_statistics.ipynb
│       ├── 02_univariate_bivariate_multivariate_analysis.ipynb
│       ├── 03_comprehensive_eda.ipynb
│       └── 04_ml_analysis.ipynb
├── scripts/
│   ├── python/
│   │   ├── data_loader.py
│   │   ├── descriptive_stats.py
│   │   ├── univariate_analysis.py
│   │   ├── bivariate_analysis.py
│   │   ├── multivariate_analysis.py
│   │   ├── eda.py
│   │   └── ml_models.py
│   └── r/
│       ├── data_loader.R
│       ├── descriptive_stats.R
│       ├── univariate_analysis.R
│       ├── bivariate_analysis.R
│       ├── multivariate_analysis.R
│       ├── eda.R
│       ├── ml_models.R
│       ├── install_packages.R
│       └── requirements.R
├── docs/
├── README.md
├── requirements.txt
└── .gitignore
```

## Analysis Components

### 1. Descriptive, Inferential, and Exploratory Statistical Analysis
- **Descriptive Statistics**: Mean, median, mode, standard deviation, quartiles, skewness, kurtosis
- **Inferential Statistics**: Hypothesis testing, confidence intervals, t-tests, ANOVA, normality tests
- **Exploratory Analysis**: Data distribution, outliers detection, missing values analysis

### 2. Univariate, Bivariate, and Multivariate Analysis
- **Univariate Analysis**: Distribution plots, histograms, box plots, summary statistics for individual variables
- **Bivariate Analysis**: Correlation analysis, scatter plots, cross-tabulation, chi-square tests, ANOVA
- **Multivariate Analysis**: Principal Component Analysis (PCA), factor analysis, cluster analysis (K-means)

### 3. Comprehensive EDA
- Data quality assessment
- Feature engineering
- Visualizations (histograms, box plots, scatter plots, heatmaps)
- Statistical summaries
- Pattern identification

### 4. Machine Learning Analysis
- **Regression Models**: Linear Regression, Ridge, Lasso, Elastic Net
- **Tree-based Models**: Random Forest, Gradient Boosting, XGBoost, LightGBM
- **Model Evaluation**: Cross-validation, metrics (RMSE, MAE, R²)
- **Feature Importance**: Identification of key predictors
- **Model Comparison**: Performance comparison across different algorithms

## Technologies Used

### Python
- pandas, numpy
- matplotlib, seaborn, plotly
- scipy, statsmodels
- scikit-learn, xgboost, lightgbm
- jupyter

### R
- tidyverse (dplyr, tidyr, ggplot2)
- psych, e1071
- caret, randomForest, xgboost
- FactoMineR, factoextra
- corrplot, cluster

## Getting Started

### Python Setup
1. Install dependencies: `pip install -r requirements.txt`
2. Run notebooks in `notebooks/python/` directory
3. Or run scripts directly from `scripts/python/` directory

### R Setup
1. Install R packages: Run `scripts/r/install_packages.R`
2. Or install manually: `install.packages(c("package1", "package2", ...))`
3. Run notebooks in `notebooks/r/` directory
4. Or run scripts directly from `scripts/r/` directory

## Dataset

The dataset contains age-adjusted cancer incidence rates at the county level for the United States, including:
- County-level FIPS codes
- Age-adjusted incidence rates (cases per 100,000)
- Confidence intervals
- Average annual counts
- Recent trends and 5-year trends in incidence rates

**Data Source**: SEER (Surveillance, Epidemiology, and End Results) and NPCR (National Program of Cancer Registries) programs.

## License

Please refer to the original dataset's license terms from NCI/CDC for data usage rights. This analysis is for educational and research purposes only.

## Author

Clinical Data Science & Health Analytics Project

## Last Updated

November 2025

