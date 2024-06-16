# Pima Indians Diabetes Dataset - Comprehensive Data Science Analysis

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![R](https://img.shields.io/badge/R-4.0%2B-blue.svg)](https://www.r-project.org/)

A comprehensive data science project analyzing the Pima Indians Diabetes dataset using both Python and R. This project includes descriptive statistics, inferential statistics, exploratory data analysis (EDA), and machine learning modeling to predict diabetes outcomes.

## 📋 Table of Contents

- [Overview](#overview)
- [Dataset Information](#dataset-information)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Analysis Components](#analysis-components)
- [Results](#results)
- [License](#license)
- [References](#references)
- [Contributing](#contributing)

## 🔍 Overview

This project provides a comprehensive analysis of the Pima Indians Diabetes dataset, including:

1. **Descriptive Statistics**: Summary statistics, distributions, and data quality assessment
2. **Inferential Statistics**: Hypothesis testing, confidence intervals, and correlation analysis
3. **Exploratory Data Analysis (EDA)**: Univariate, bivariate, and multivariate analysis
4. **Machine Learning Analysis**: Multiple algorithms including Logistic Regression, Random Forest, SVM, Gradient Boosting, KNN, and Neural Networks

The analysis is implemented in both **Python** and **R** to provide a comprehensive view of the data using different statistical and machine learning approaches.

## 📊 Dataset Information

### Dataset Source

The Pima Indians Diabetes dataset is from the [UCI Machine Learning Repository](https://archive.ics.uci.edu/ml/datasets/Pima+Indians+Diabetes).

### Dataset Citation

Smith, J.W., Everhart, J.E., Dickson, W.C., Knowler, W.C., & Johannes, R.S. (1988). "Using the ADAP learning algorithm to forecast the onset of diabetes mellitus". In Proceedings of the Symposium on Computer Applications and Medical Care (pp. 261-265). IEEE Computer Society Press.

### Dataset Description

The dataset contains 768 observations with 8 predictor variables and 1 target variable (Outcome). All patients are females at least 21 years old of Pima Indian heritage.

### Features

1. **Pregnancies**: Number of times pregnant
2. **Glucose**: Plasma glucose concentration a 2 hours in an oral glucose tolerance test
3. **BloodPressure**: Diastolic blood pressure (mm Hg)
4. **SkinThickness**: Triceps skin fold thickness (mm)
5. **Insulin**: 2-Hour serum insulin (mu U/ml)
6. **BMI**: Body mass index (weight in kg/(height in m)^2)
7. **DiabetesPedigreeFunction**: Diabetes pedigree function
8. **Age**: Age (years)
9. **Outcome**: Class variable (0 or 1) - 0 indicates no diabetes, 1 indicates diabetes

### Data Quality Notes

- The dataset contains zeros in several features (Glucose, BloodPressure, SkinThickness, Insulin, BMI) which may represent missing data
- Class distribution: Approximately 65% no diabetes, 35% diabetes (class imbalance)

## 📁 Project Structure

```
pima-indians-diabetes/
│
├── data/
│   └── pima-indians-diabetes.csv          # Dataset file
│
├── notebooks/
│   ├── python/
│   │   ├── 01_statistical_analysis.ipynb  # Descriptive & inferential statistics
│   │   ├── 02_eda_analysis.ipynb          # Exploratory data analysis
│   │   └── 03_ml_analysis.ipynb           # Machine learning analysis
│   │
│   └── r/
│       ├── 01_statistical_analysis.Rmd    # Descriptive & inferential statistics (R)
│       ├── 02_eda_analysis.Rmd            # Exploratory data analysis (R)
│       └── 03_ml_analysis.Rmd             # Machine learning analysis (R)
│
├── scripts/
│   ├── python/
│   │   └── univariate_bivariate_multivariate_analysis.py  # Analysis script
│   │
│   └── r/
│       └── univariate_bivariate_multivariate_analysis.R   # Analysis script (R)
│
├── outputs/                                # Generated outputs (plots, results)
│
├── docs/                                   # Additional documentation
│
├── requirements.txt                        # Python dependencies
├── requirements-r.txt                      # R dependencies
├── LICENSE                                 # License file
├── .gitignore                              # Git ignore file
└── README.md                               # This file
```

## 🚀 Installation

### Prerequisites

- **Python 3.8+** or higher
- **R 4.0+** or higher
- **Jupyter Notebook** (for Python notebooks)
- **RStudio** or **R Markdown** (for R notebooks)

### Python Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/pima-indians-diabetes.git
cd pima-indians-diabetes
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install Python dependencies:
```bash
pip install -r requirements.txt
```

### R Setup

1. Install R packages:
```bash
Rscript -e "install.packages(c('dplyr', 'tidyverse', 'ggplot2', 'caret', 'randomForest', 'e1071', 'glmnet', 'gbm', 'rpart', 'pROC', 'corrplot', 'psych', 'car', 'gridExtra', 'VIM', 'GGally', 'plotly'))"
```

Or install from the requirements file:
```bash
Rscript -e "source('requirements-r.txt')"
```

## 📖 Usage

### Python Analysis

#### Running Jupyter Notebooks

1. Start Jupyter Notebook:
```bash
jupyter notebook
```

2. Navigate to `notebooks/python/` and open the notebooks in order:
   - `01_statistical_analysis.ipynb` - Statistical analysis
   - `02_eda_analysis.ipynb` - Exploratory data analysis
   - `03_ml_analysis.ipynb` - Machine learning analysis

#### Running Python Scripts

```bash
cd scripts/python
python univariate_bivariate_multivariate_analysis.py
```

### R Analysis

#### Running R Markdown Notebooks

1. Open RStudio or your preferred R environment
2. Navigate to `notebooks/r/` and open the `.Rmd` files
3. Knit the documents to generate HTML reports

#### Running R Scripts

```bash
cd scripts/r
Rscript univariate_bivariate_multivariate_analysis.R
```

## 🔬 Analysis Components

### 1. Descriptive Statistics

- **Summary Statistics**: Mean, median, standard deviation, quartiles
- **Distribution Analysis**: Histograms, box plots, violin plots
- **Data Quality Assessment**: Missing values, zero values analysis
- **Outcome Distribution**: Class balance analysis

### 2. Inferential Statistics

- **Hypothesis Testing**: Independent t-tests, chi-square tests
- **Correlation Analysis**: Pearson correlation coefficients
- **Confidence Intervals**: 95% confidence intervals for key features
- **Statistical Significance**: P-value analysis

### 3. Exploratory Data Analysis (EDA)

#### Univariate Analysis
- Distribution plots for each feature
- Summary statistics
- Normality tests
- Outlier detection

#### Bivariate Analysis
- Feature vs. Outcome analysis
- Correlation with outcome
- Statistical tests between groups
- Scatter plots

#### Multivariate Analysis
- Correlation heatmaps
- Principal Component Analysis (PCA)
- 3D scatter plots
- Interaction effects

### 4. Machine Learning Analysis

#### Algorithms Implemented
1. **Logistic Regression**: Baseline linear model
2. **Random Forest**: Ensemble method with feature importance
3. **Support Vector Machine (SVM)**: Kernel-based classification
4. **Gradient Boosting**: Boosting ensemble method
5. **K-Nearest Neighbors (KNN)**: Instance-based learning
6. **Neural Network**: Multi-layer perceptron
7. **Decision Tree**: Interpretable tree-based model

#### Evaluation Metrics
- Accuracy
- Precision
- Recall (Sensitivity)
- F1-Score
- ROC-AUC
- Confusion Matrix
- Cross-Validation

#### Model Comparison
- Performance comparison across all models
- ROC curves comparison
- Feature importance analysis
- Cross-validation results

## 📈 Results

### Key Findings

1. **Data Quality**: 
   - Zero values in Glucose, BloodPressure, SkinThickness, Insulin, and BMI may represent missing data
   - Class imbalance: ~65% no diabetes, ~35% diabetes

2. **Feature Importance**:
   - **Glucose** shows the strongest correlation with diabetes outcome
   - **BMI** and **Age** are significant predictors
   - **Diabetes Pedigree Function** provides additional predictive power

3. **Statistical Insights**:
   - Significant differences between diabetic and non-diabetic groups for all features
   - Strong positive correlations: Glucose, BMI, Age with Outcome
   - Clear separation between groups in key features

4. **Machine Learning Results**:
   - Random Forest and Gradient Boosting typically perform best
   - ROC-AUC scores range from 0.75 to 0.85 depending on the algorithm
   - Feature importance confirms Glucose, BMI, and Age as key predictors

### Model Performance

Typical performance metrics (may vary with data splits):
- **Random Forest**: Accuracy ~77%, ROC-AUC ~0.82
- **Gradient Boosting**: Accuracy ~76%, ROC-AUC ~0.81
- **Logistic Regression**: Accuracy ~77%, ROC-AUC ~0.81
- **SVM**: Accuracy ~76%, ROC-AUC ~0.80
- **KNN**: Accuracy ~72%, ROC-AUC ~0.75
- **Neural Network**: Accuracy ~75%, ROC-AUC ~0.79

## 📄 License

### Dataset License

This dataset is provided under the UCI Machine Learning Repository's default license terms. The dataset is available for research and educational purposes.

For the original dataset license and terms, please refer to:
https://archive.ics.uci.edu/ml/datasets/Pima+Indians+Diabetes

### Project Code License

The analysis code, notebooks, and scripts in this repository are provided under the **MIT License**.

See the [LICENSE](LICENSE) file for details.

## 📚 References

1. **Dataset Source**: [UCI Machine Learning Repository - Pima Indians Diabetes](https://archive.ics.uci.edu/ml/datasets/Pima+Indians+Diabetes)

2. **Original Paper**: 
   - Smith, J.W., Everhart, J.E., Dickson, W.C., Knowler, W.C., & Johannes, R.S. (1988). "Using the ADAP learning algorithm to forecast the onset of diabetes mellitus". In Proceedings of the Symposium on Computer Applications and Medical Care (pp. 261-265). IEEE Computer Society Press.

3. **Libraries and Tools**:
   - Python: pandas, numpy, scikit-learn, matplotlib, seaborn
   - R: dplyr, caret, randomForest, ggplot2, corrplot

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

### Contribution Guidelines

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 Notes

- This project is for educational and research purposes
- The dataset contains medical information and should be handled with care
- Results may vary based on random seeds and data splits
- Always consult with medical professionals for real-world diabetes prediction

## 👤 Author

Data Science Analysis Project

## 🙏 Acknowledgments

- UCI Machine Learning Repository for providing the dataset
- The Pima Indian community for their contribution to medical research
- Open-source community for excellent data science tools and libraries

## 📧 Contact

For questions or suggestions, please open an issue on GitHub.

---

**Disclaimer**: This analysis is for educational purposes only. It should not be used for actual medical diagnosis or treatment decisions. Always consult with qualified healthcare professionals for medical advice.


