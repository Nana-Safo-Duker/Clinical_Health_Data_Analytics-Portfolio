# Breast Cancer Diagnosis Analysis

## Project Overview

This project provides a comprehensive analysis of the Breast Cancer Wisconsin (Diagnostic) dataset. The goal is to classify breast cancer tumors as malignant (M) or benign (B) using various machine learning algorithms and statistical analysis techniques.

## Dataset Information

- **Dataset**: Breast Cancer Wisconsin (Diagnostic) Dataset
- **Source**: UCI Machine Learning Repository
- **License**: This dataset is made available under the Creative Commons Attribution 4.0 International (CC BY 4.0) license
- **Original Dataset**: Available at [UCI ML Repository](https://archive.ics.uci.edu/ml/datasets/Breast+Cancer+Wisconsin+%28Diagnostic%29)
- **Features**: 30 numerical features computed from digitized images of fine needle aspirates (FNA) of breast masses
- **Target**: Diagnosis (M = Malignant, B = Benign)
- **Samples**: 569 instances

### Dataset License

The original dataset from the UCI Machine Learning Repository is provided under the following terms:
- **Creative Commons Attribution 4.0 International (CC BY 4.0) License**
- **Attribution**: The dataset should be attributed to the original creators:
  - Dr. William H. Wolberg, General Surgery Dept., University of Wisconsin
  - W. Nick Street, Computer Sciences Dept., University of Wisconsin
  - Olvi L. Mangasarian, Computer Sciences Dept., University of Wisconsin
  - Original Source: UCI Machine Learning Repository

For more information about the dataset and license, please visit:
https://archive.ics.uci.edu/ml/datasets/Breast+Cancer+Wisconsin+%28Diagnostic%29

## Project Structure

```
breast_cancer/
│
├── data/
│   └── breast_cancer.csv          # Dataset file
│
├── notebooks/
│   ├── python/
│   │   ├── 01_statistical_analysis.ipynb
│   │   ├── 02_univariate_bivariate_multivariate.ipynb
│   │   ├── 03_comprehensive_eda.ipynb
│   │   └── 04_ml_analysis.ipynb
│   │
│   └── r/
│       ├── 01_statistical_analysis.Rmd
│       ├── 02_univariate_bivariate_multivariate.Rmd
│       ├── 03_comprehensive_eda.Rmd
│       └── 04_ml_analysis.Rmd
│
├── scripts/
│   ├── python/
│   │   ├── statistical_analysis.py
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
│   ├── univariate/                # Univariate analysis results
│   ├── bivariate/                 # Bivariate analysis results
│   ├── multivariate/              # Multivariate analysis results
│   ├── eda/                       # Exploratory data analysis results
│   └── ml/                        # Machine learning results
│
├── docs/                          # Additional documentation
│
├── requirements.txt               # Python dependencies
├── requirements_r.txt             # R package requirements
├── .gitignore
└── README.md                      # This file
```

## Features

The dataset contains the following features (10 features × 3 measurements = 30 features):

### Mean Features (10):
- radius_mean
- texture_mean
- perimeter_mean
- area_mean
- smoothness_mean
- compactness_mean
- concavity_mean
- concave points_mean
- symmetry_mean
- fractal_dimension_mean

### Standard Error Features (10):
- radius_se
- texture_se
- perimeter_se
- area_se
- smoothness_se
- compactness_se
- concavity_se
- concave points_se
- symmetry_se
- fractal_dimension_se

### Worst Features (10):
- radius_worst
- texture_worst
- perimeter_worst
- area_worst
- smoothness_worst
- compactness_worst
- concavity_worst
- concave points_worst
- symmetry_worst
- fractal_dimension_worst

## Analysis Components

### 1. Statistical Analysis
- **Descriptive Statistics**: Mean, median, mode, variance, skewness, kurtosis
- **Inferential Statistics**: T-tests, Mann-Whitney U tests, confidence intervals, effect sizes
- **Exploratory Analysis**: Correlation analysis, group comparisons, outlier detection

### 2. Univariate, Bivariate, and Multivariate Analysis
- **Univariate Analysis**: Distribution analysis, normality tests, box plots
- **Bivariate Analysis**: Scatter plots, correlation analysis, feature vs target analysis
- **Multivariate Analysis**: Principal Component Analysis (PCA), correlation matrices, pair plots

### 3. Comprehensive Exploratory Data Analysis (EDA)
- Data overview and quality checks
- Target variable analysis
- Feature analysis and visualization
- Correlation analysis
- Outlier detection
- Feature engineering insights

### 4. Machine Learning Analysis
- **Models Implemented**:
  - Logistic Regression
  - Decision Tree
  - Random Forest
  - Gradient Boosting
  - Support Vector Machine (SVM)
  - K-Nearest Neighbors (KNN)
  - Naive Bayes
  - XGBoost
  - LightGBM
  
- **Evaluation Metrics**:
  - Accuracy
  - Precision
  - Recall
  - F1 Score
  - ROC AUC
  
- **Features**:
  - Model comparison
  - Hyperparameter tuning
  - Feature importance analysis
  - Confusion matrices
  - ROC curves

## Installation and Setup

### Python Environment

1. **Create a virtual environment** (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

### R Environment

1. **Install R packages**:
```r
# Install required packages
install.packages(c("dplyr", "tidyr", "ggplot2", "corrplot", "caret", 
                   "randomForest", "e1071", "xgboost", "glmnet", "rpart", 
                   "ranger", "pROC", "psych", "VIM", "naniar", "FactoMineR", 
                   "factoextra"))
```

## Usage

### Python Scripts

Run the analysis scripts from the project root directory:

```bash
# Statistical analysis
python scripts/python/statistical_analysis.py

# Univariate, bivariate, multivariate analysis
python scripts/python/univariate_bivariate_multivariate_analysis.py

# Comprehensive EDA
python scripts/python/comprehensive_eda.py

# Machine learning analysis
python scripts/python/ml_analysis.py
```

### Python Notebooks

Open and run the Jupyter notebooks:

```bash
jupyter notebook notebooks/python/
```

### R Scripts

Run the R scripts from the project root directory:

```r
# In R or RStudio
source("scripts/r/statistical_analysis.R")
source("scripts/r/univariate_bivariate_multivariate_analysis.R")
source("scripts/r/comprehensive_eda.R")
source("scripts/r/ml_analysis.R")
```

### R Notebooks

Open and run the R Markdown notebooks in RStudio:

```r
# In RStudio
rmarkdown::render("notebooks/r/01_statistical_analysis.Rmd")
```

## Results

All analysis results, including visualizations and model outputs, are saved in the `results/` directory:

- `results/univariate/`: Univariate analysis plots and statistics
- `results/bivariate/`: Bivariate analysis plots and correlations
- `results/multivariate/`: Multivariate analysis including PCA results
- `results/eda/`: Comprehensive EDA visualizations
- `results/ml/`: Machine learning model comparisons and evaluations

## Key Findings

1. **Dataset Balance**: The dataset is relatively balanced between malignant and benign cases.

2. **Feature Correlations**: Many features are highly correlated, suggesting potential for dimensionality reduction.

3. **Significant Differences**: Statistical tests confirm significant differences in feature means between malignant and benign cases.

4. **Model Performance**: Multiple machine learning models achieve high accuracy (>95%) in classifying breast cancer tumors.

5. **Feature Importance**: Certain features (e.g., radius_mean, perimeter_mean, area_mean) show high importance in classification.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License. However, please note that the dataset itself is subject to the Creative Commons Attribution 4.0 International (CC BY 4.0) license as specified above.

## Acknowledgments

- **Dataset Creators**: Dr. William H. Wolberg, W. Nick Street, and Olvi L. Mangasarian
- **UCI Machine Learning Repository**: For providing the dataset
- **Original Source**: University of Wisconsin, Madison

## References

1. Wolberg, W. H., Street, W. N., & Mangasarian, O. L. (1995). Breast cancer Wisconsin (diagnostic) data set. UCI Machine Learning Repository. https://doi.org/10.24432/C5DW2B

2. Street, W. N., Wolberg, W. H., & Mangasarian, O. L. (1993). Nuclear feature extraction for breast tumor diagnosis. In IS&T/SPIE 1993 International Symposium on Electronic Imaging: Science and Technology (pp. 861-870). SPIE.

## Contact

For questions or suggestions, please open an issue in the repository.

---

**Note**: This project is for educational and research purposes. The analysis and results should not be used as a substitute for professional medical diagnosis or treatment.

