# Diabetes Binary Health Indicators - BRFSS 2021 Analysis

## Project Overview

This project provides a comprehensive analysis of the Diabetes Binary Health Indicators dataset from the Behavioral Risk Factor Surveillance System (BRFSS) 2021. The analysis includes descriptive statistics, inferential statistics, exploratory data analysis, univariate/bivariate/multivariate analysis, and machine learning models for diabetes prediction.

## Dataset Information

- **Dataset**: Diabetes Binary Health Indicators - BRFSS 2021
- **Source**: Behavioral Risk Factor Surveillance System (BRFSS)
- **Year**: 2021
- **Records**: 236,380
- **Features**: 22 (including target variable)
- **Target Variable**: Diabetes_binary (0 = No diabetes, 1 = Diabetes)

### Dataset License

This dataset is from the Behavioral Risk Factor Surveillance System (BRFSS), which is a collaborative project between all of the states in the United States and participating US territories and the Centers for Disease Control and Prevention (CDC). 

**License Information:**
- The BRFSS data are in the public domain and are provided without restrictions.
- Data are collected by state health departments with funding from the CDC.
- Users are free to use, modify, and distribute the data for any purpose.
- Attribution to the CDC and BRFSS is appreciated but not required.

**Original Dataset Source:**
- Kaggle: [Diabetes Health Indicators Dataset](https://www.kaggle.com/datasets/alexteboul/diabetes-health-indicators-dataset)
- CDC BRFSS: [Behavioral Risk Factor Surveillance System](https://www.cdc.gov/brfss/)

## Project Structure

```
diabetes_binary_health_indicators_BRFSS2021/
│
├── data/
│   └── diabetes_binary_health_indicators_BRFSS2021.csv
│
├── notebooks/
│   ├── python/
│   │   ├── 01_statistical_analysis.ipynb
│   │   ├── 02_univariate_bivariate_multivariate_analysis.ipynb
│   │   ├── 03_comprehensive_eda.ipynb
│   │   └── 04_ml_analysis.ipynb
│   │
│   └── r/
│       ├── 01_statistical_analysis.ipynb
│       ├── 02_univariate_bivariate_multivariate_analysis.ipynb
│       ├── 03_comprehensive_eda.ipynb
│       └── 04_ml_analysis.ipynb
│
├── scripts/
│   ├── python/
│   │   ├── univariate_bivariate_multivariate_analysis.py
│   │   ├── comprehensive_eda.py
│   │   └── ml_analysis.py
│   │
│   └── r/
│       ├── statistical_analysis.R
│       ├── univariate_bivariate_multivariate_analysis.R
│       ├── comprehensive_eda.R
│       └── ml_analysis.R
│
├── results/
│   ├── figures/
│   └── models/
│
├── requirements.txt
├── .gitignore
└── README.md
```

## Features

### 1. Statistical Analysis
- **Descriptive Statistics**: Mean, median, mode, standard deviation, variance, skewness, kurtosis
- **Inferential Statistics**: Chi-square tests, t-tests, Mann-Whitney U tests
- **Correlation Analysis**: Pearson and Spearman correlations
- **Confidence Intervals**: 95% confidence intervals for key variables

### 2. Univariate Analysis
- Distribution analysis for numerical variables
- Frequency analysis for categorical variables
- Statistical measures (mean, median, mode, variance, etc.)
- Visualization of distributions

### 3. Bivariate Analysis
- Correlation between variables and target
- Box plots for numerical variables by diabetes status
- Categorical variable analysis by diabetes status
- Scatter plots for variable pairs

### 4. Multivariate Analysis
- Correlation heatmaps
- Multivariate group analysis
- Interaction effects
- Feature relationship analysis

### 5. Comprehensive EDA
- Data quality assessment
- Missing value analysis
- Outlier detection
- Pattern recognition
- Feature engineering insights

### 6. Machine Learning Analysis
- **Models Implemented**:
  - Logistic Regression
  - Random Forest
  - Gradient Boosting
  - Support Vector Machine (SVM)
- **Evaluation Metrics**:
  - Accuracy
  - Precision
  - Recall
  - F1 Score
  - AUC-ROC
- **Feature Importance Analysis**
- **Model Comparison and Selection**

## Installation

### Python Environment

1. Clone the repository:
```bash
git clone <repository-url>
cd diabetes_binary_health_indicators_BRFSS2021
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install requirements:
```bash
pip install -r requirements.txt
```

### R Environment

1. Install required R packages:
```r
install.packages(c("ggplot2", "dplyr", "corrplot", "caret", "randomForest", 
                   "e1071", "pROC", "VIM", "moments", "gridExtra"))
```

## Usage

### Python Notebooks

1. **Statistical Analysis**:
```bash
jupyter notebook notebooks/python/01_statistical_analysis.ipynb
```

2. **Univariate/Bivariate/Multivariate Analysis**:
```bash
jupyter notebook notebooks/python/02_univariate_bivariate_multivariate_analysis.ipynb
```

3. **Comprehensive EDA**:
```bash
jupyter notebook notebooks/python/03_comprehensive_eda.ipynb
```

4. **Machine Learning Analysis**:
```bash
jupyter notebook notebooks/python/04_ml_analysis.ipynb
```

### Python Scripts

Run scripts from the project root:
```bash
python scripts/python/statistical_analysis.py
python scripts/python/univariate_bivariate_multivariate_analysis.py
python scripts/python/comprehensive_eda.py
python scripts/python/ml_analysis.py
```

### R Scripts

Run R scripts from the project root:
```r
source("scripts/r/statistical_analysis.R")
source("scripts/r/univariate_bivariate_multivariate_analysis.R")
source("scripts/r/comprehensive_eda.R")
source("scripts/r/ml_analysis.R")
```

### R Notebooks

Open R notebooks in Jupyter or RStudio:
```bash
jupyter notebook notebooks/r/01_statistical_analysis.ipynb
```

## Key Findings

### Dataset Characteristics
- **Total Records**: 236,380
- **Features**: 22
- **Diabetes Prevalence**: ~13-15% (varies by analysis)
- **Missing Values**: Minimal to none
- **Data Quality**: High

### Key Predictors of Diabetes
Based on the analysis, the following factors show strong associations with diabetes:
1. High Blood Pressure (HighBP)
2. High Cholesterol (HighChol)
3. Body Mass Index (BMI)
4. General Health (GenHlth)
5. Age
6. Physical Activity (PhysActivity)
7. Heart Disease or Attack
8. Difficulty Walking (DiffWalk)

### Machine Learning Results
- **Best Performing Model**: Random Forest (typically highest AUC-ROC)
- **Model Performance**: All models show good predictive performance
- **Feature Importance**: BMI, Age, GenHlth, HighBP, and HighChol are among the most important features

## Results

All results are saved in the `results/` directory:
- **Figures**: Visualizations and plots saved as PNG files
- **Models**: Trained models and performance metrics saved as CSV files

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project uses data from the BRFSS, which is in the public domain. The analysis code and methodology are provided as-is for educational and research purposes.

## Acknowledgments

- **CDC BRFSS**: For providing the Behavioral Risk Factor Surveillance System data
- **Kaggle**: For hosting the dataset
- **Data Contributors**: All state health departments and the CDC

## References

1. Centers for Disease Control and Prevention (CDC). Behavioral Risk Factor Surveillance System Survey Data. Atlanta, Georgia: U.S. Department of Health and Human Services, Centers for Disease Control and Prevention, 2021.

2. BRFSS Website: https://www.cdc.gov/brfss/

3. Dataset Source: https://www.kaggle.com/datasets/alexteboul/diabetes-health-indicators-dataset

## Contact

For questions or issues, please open an issue in the repository.

## Version History

- **v1.0.0** (2024): Initial release with comprehensive analysis in Python and R

