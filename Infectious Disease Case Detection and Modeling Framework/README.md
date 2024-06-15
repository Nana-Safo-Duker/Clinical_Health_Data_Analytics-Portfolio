# Cancer Incidence Data Analysis

## Project Overview

This project presents a comprehensive statistical and machine learning analysis of cancer incidence data at the county level across the United States. The analysis includes descriptive statistics, inferential statistics, exploratory data analysis, univariate/bivariate/multivariate analyses, and machine learning modeling.

## Dataset

**Dataset Name:** Cancer Incidence Data (INCD)

**Source:** The dataset contains age-adjusted cancer incidence rates at the county level for the United States, including:
- County-level FIPS codes
- Age-adjusted incidence rates (cases per 100,000)
- Confidence intervals
- Average annual counts
- Recent trends and 5-year trends in incidence rates

**Dataset License:** 
This dataset appears to be from the SEER (Surveillance, Epidemiology, and End Results) and NPCR (National Program of Cancer Registries) programs. The data is typically made available for research purposes. Please refer to the original data source for specific licensing terms:

- **SEER Data**: Available through the National Cancer Institute (NCI) 
- **NPCR Data**: Available through the Centers for Disease Control and Prevention (CDC)

**Important Note:** Users of this dataset should comply with the data use agreements and licensing terms provided by the original data sources (NCI/CDC). This analysis is for educational and research purposes only.

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
│   │   ├── descriptive_stats.py
│   │   ├── univariate_analysis.py
│   │   ├── bivariate_analysis.py
│   │   ├── multivariate_analysis.py
│   │   ├── eda.py
│   │   └── ml_models.py
│   └── r/
│       ├── descriptive_stats.R
│       ├── univariate_analysis.R
│       ├── bivariate_analysis.R
│       ├── multivariate_analysis.R
│       ├── eda.R
│       └── ml_models.R
├── docs/
│   └── (documentation files)
├── requirements.txt                # Python dependencies
├── .gitignore
└── README.md

```

## Features

### 1. Descriptive, Inferential, and Exploratory Statistical Analysis
- **Descriptive Statistics**: Mean, median, mode, standard deviation, quartiles, skewness, kurtosis
- **Inferential Statistics**: Hypothesis testing, confidence intervals, t-tests, ANOVA, correlation tests
- **Exploratory Analysis**: Data distribution, outliers detection, missing values analysis

### 2. Univariate, Bivariate, and Multivariate Analysis
- **Univariate Analysis**: Distribution plots, histograms, box plots, summary statistics for individual variables
- **Bivariate Analysis**: Correlation analysis, scatter plots, cross-tabulation, chi-square tests
- **Multivariate Analysis**: Principal Component Analysis (PCA), factor analysis, multiple regression

### 3. Comprehensive EDA
- Data quality assessment
- Feature engineering
- Visualizations (histograms, box plots, scatter plots, heatmaps, geographic visualizations)
- Statistical summaries
- Pattern identification

### 4. Machine Learning Analysis
- **Regression Models**: Linear Regression, Ridge, Lasso, Elastic Net
- **Tree-based Models**: Random Forest, Gradient Boosting, XGBoost, LightGBM
- **Model Evaluation**: Cross-validation, metrics (RMSE, MAE, R²)
- **Feature Importance**: Identification of key predictors
- **Model Comparison**: Performance comparison across different algorithms

## Installation

### Python Environment

1. Clone the repository:
```bash
git clone <repository-url>
cd incd
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

### R Environment

1. Install R (>= 4.0.0) from [CRAN](https://cran.r-project.org/)

2. Install required R packages:
```r
install.packages(c("tidyverse", "ggplot2", "dplyr", "corrplot", 
                   "car", "psych", "caret", "randomForest", 
                   "xgboost", "glmnet", "plotly", "leaflet"))
```

## Usage

### Python Analysis

#### Running Jupyter Notebooks:
```bash
jupyter notebook notebooks/python/
```

#### Running Python Scripts:
```bash
python scripts/python/descriptive_stats.py
python scripts/python/eda.py
python scripts/python/ml_models.py
```

### R Analysis

#### Running R Notebooks:
Open RStudio and navigate to `notebooks/r/` directory

#### Running R Scripts:
```r
source("scripts/r/descriptive_stats.R")
source("scripts/r/eda.R")
source("scripts/r/ml_models.R")
```

## Key Findings

(To be updated after analysis completion)

## Methodology

1. **Data Preprocessing**: Data cleaning, handling missing values, outlier treatment
2. **Exploratory Data Analysis**: Understanding data distributions and relationships
3. **Statistical Analysis**: Descriptive and inferential statistics
4. **Feature Engineering**: Creating relevant features for modeling
5. **Model Development**: Training and evaluating multiple ML models
6. **Model Selection**: Choosing the best-performing model based on evaluation metrics

## Results

(To be updated after analysis completion)

## Contributing

This is a research project. For contributions, please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is for educational and research purposes. Please refer to the original dataset's license terms from NCI/CDC for data usage rights.

## References

- Surveillance, Epidemiology, and End Results (SEER) Program: https://seer.cancer.gov/
- National Program of Cancer Registries (NPCR): https://www.cdc.gov/cancer/npcr/
- National Cancer Institute (NCI): https://www.cancer.gov/

## Author

[Your Name/Institution]

## Acknowledgments

- Data provided by SEER and NPCR programs
- National Cancer Institute (NCI)
- Centers for Disease Control and Prevention (CDC)

## Contact

For questions or issues, please open an issue on the GitHub repository.

---

**Last Updated:** November 2025

