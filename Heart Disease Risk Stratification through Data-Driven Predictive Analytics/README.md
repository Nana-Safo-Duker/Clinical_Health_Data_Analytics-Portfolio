# Heart Disease Analysis - Clinical Data Science & Health Analytics

A comprehensive data science project analyzing heart disease dataset using statistical analysis, exploratory data analysis (EDA), and machine learning techniques in both Python and R.

## 📋 Table of Contents

- [Project Overview](#project-overview)
- [Dataset Information](#dataset-information)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Analysis Components](#analysis-components)
- [Results](#results)
- [License](#license)
- [References](#references)

## 🎯 Project Overview

This project provides a comprehensive analysis of heart disease data, including:

- **Descriptive Statistics**: Summary statistics, distributions, and data quality assessment
- **Inferential Statistics**: Hypothesis testing, correlation analysis, and statistical significance testing
- **Exploratory Data Analysis (EDA)**: Univariate, bivariate, and multivariate analysis
- **Machine Learning**: Multiple ML algorithms for heart disease prediction and classification

All analyses are implemented in both **Python** and **R** for comprehensive coverage.

## 📊 Dataset Information

### Dataset Description

The heart disease dataset contains patient information including:
- **Age**: Patient age
- **Sex**: Patient sex (male/female)
- **Chest Pain**: Type of chest pain (0-3)
- **Rest BP**: Resting blood pressure
- **Cholesterol**: Serum cholesterol level
- **Max HR**: Maximum heart rate achieved
- **ST Depression**: ST depression induced by exercise
- **Heart Disease**: Target variable (0 = No, 1 = Yes)

### Dataset License

**Original Dataset Source**: UCI Machine Learning Repository  
**Dataset**: Heart Disease Dataset  
**URL**: https://archive.ics.uci.edu/ml/datasets/heart+disease

**License Information**:
- The dataset is available under the UCI Machine Learning Repository license
- UCI Citation Policy: https://archive.ics.uci.edu/ml/citation_policy.html
- This dataset is provided for research and educational purposes
- Please refer to the original dataset source for detailed license terms and citation requirements

**Citation**:
```
Dua, D. and Graff, C. (2019). UCI Machine Learning Repository 
[http://archive.ics.uci.edu/ml]. Irvine, CA: University of California, 
School of Information and Computer Science.
```

## 📁 Project Structure

```
heart-disease/
├── data/
│   └── heart-disease.csv          # Dataset
├── notebooks/
│   ├── python/
│   │   ├── 01_statistical_analysis.ipynb
│   │   ├── 02_univariate_bivariate_multivariate_analysis.ipynb
│   │   ├── 03_comprehensive_eda.ipynb
│   │   └── 04_ml_analysis.ipynb
│   └── r/
│       ├── 01_statistical_analysis.ipynb
│       ├── 02_univariate_bivariate_multivariate_analysis.ipynb
│       ├── 03_comprehensive_eda.ipynb
│       └── 04_ml_analysis.ipynb
├── scripts/
│   ├── python/
│   │   ├── univariate_bivariate_multivariate_analysis.py
│   │   ├── comprehensive_eda.py
│   │   └── ml_analysis.py
│   └── r/
│       ├── statistical_analysis.R
│       ├── univariate_bivariate_multivariate_analysis.R
│       ├── comprehensive_eda.R
│       └── ml_analysis.R
├── results/
│   ├── figures/                   # Generated visualizations
│   ├── models/                    # Saved ML models
│   └── model_results.csv          # Model performance metrics
├── docs/                          # Documentation
├── requirements.txt               # Python dependencies
├── requirements-r.txt             # R package requirements
├── .gitignore
├── LICENSE
└── README.md
```

## 🚀 Installation

### Python Environment

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd heart-disease
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

### R Environment

1. **Install R** (if not already installed):
   - Download from: https://www.r-project.org/

2. **Install R packages**:
   ```r
   # Open R or RStudio
   install.packages(c("tidyverse", "ggplot2", "corrplot", "Hmisc", 
                     "psych", "gridExtra", "caret", "randomForest", 
                     "e1071", "rpart", "glmnet", "pROC"))
   ```

   Or use the requirements file as a reference:
   ```bash
   # Review requirements-r.txt for package list
   ```

### Jupyter Notebooks

1. **Install Jupyter**:
   ```bash
   pip install jupyter notebook
   ```

2. **Install R kernel for Jupyter** (optional, for R notebooks):
   ```r
   install.packages(c('IRkernel'))
   IRkernel::installspec()
   ```

3. **Launch Jupyter**:
   ```bash
   jupyter notebook
   ```

## 💻 Usage

### Python Scripts

Run Python scripts directly:

```bash
# Statistical Analysis
cd scripts/python
python univariate_bivariate_multivariate_analysis.py

# Comprehensive EDA
python comprehensive_eda.py

# Machine Learning Analysis
python ml_analysis.py
```

### R Scripts

Run R scripts:

```bash
# Statistical Analysis
cd scripts/r
Rscript statistical_analysis.R

# Univariate, Bivariate, Multivariate Analysis
Rscript univariate_bivariate_multivariate_analysis.R

# Comprehensive EDA
Rscript comprehensive_eda.R

# Machine Learning Analysis
Rscript ml_analysis.R
```

### Jupyter Notebooks

1. Launch Jupyter Notebook:
   ```bash
   jupyter notebook
   ```

2. Navigate to `notebooks/python/` or `notebooks/r/`

3. Open and run notebooks in sequence:
   - `01_statistical_analysis.ipynb`
   - `02_univariate_bivariate_multivariate_analysis.ipynb`
   - `03_comprehensive_eda.ipynb`
   - `04_ml_analysis.ipynb`

## 📈 Analysis Components

### 1. Statistical Analysis

**Python**: `notebooks/python/01_statistical_analysis.ipynb`  
**R**: `notebooks/r/01_statistical_analysis.ipynb`

Includes:
- Descriptive statistics (mean, median, mode, variance, skewness, kurtosis)
- Inferential statistics (t-tests, chi-square tests, correlation tests)
- Normality tests
- Hypothesis testing

### 2. Univariate, Bivariate, Multivariate Analysis

**Python**: `notebooks/python/02_univariate_bivariate_multivariate_analysis.ipynb`  
**R**: `notebooks/r/02_univariate_bivariate_multivariate_analysis.ipynb`

Includes:
- **Univariate**: Individual variable distributions and statistics
- **Bivariate**: Relationships between two variables
- **Multivariate**: Complex relationships between multiple variables

### 3. Comprehensive EDA

**Python**: `notebooks/python/03_comprehensive_eda.ipynb`  
**R**: `notebooks/r/03_comprehensive_eda.ipynb`

Includes:
- Data quality assessment
- Missing value analysis
- Outlier detection
- Distribution analysis
- Correlation analysis
- Visualizations

### 4. Machine Learning Analysis

**Python**: `notebooks/python/04_ml_analysis.ipynb`  
**R**: `notebooks/r/04_ml_analysis.ipynb`

**Algorithms Implemented**:
- Logistic Regression
- Random Forest
- Support Vector Machine (SVM)
- K-Nearest Neighbors (KNN)
- Naive Bayes
- Gradient Boosting
- XGBoost
- LightGBM

**Evaluation Metrics**:
- Accuracy
- Precision
- Recall
- F1-Score
- ROC-AUC
- Confusion Matrix
- Cross-Validation

## 📊 Results

### Generated Outputs

All analysis results are saved in the `results/` directory:

- **Figures**: Visualizations saved in `results/figures/`
- **Models**: Trained ML models saved in `results/models/`
- **Metrics**: Model performance metrics in `results/model_results.csv`

### Key Findings

1. **Data Quality**: Clean dataset with no missing values
2. **Target Distribution**: Balanced dataset for heart disease classification
3. **Feature Correlations**: Strong correlations identified between certain features and heart disease
4. **Model Performance**: Multiple ML algorithms achieve high accuracy in heart disease prediction

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

**Dataset License**: The heart disease dataset is provided under the UCI Machine Learning Repository license. Please refer to the original dataset source for detailed license terms and citation requirements.

## 📚 References

1. **UCI Machine Learning Repository**: https://archive.ics.uci.edu/ml/index.php
2. **Heart Disease Dataset**: https://archive.ics.uci.edu/ml/datasets/heart+disease
3. **UCI Citation Policy**: https://archive.ics.uci.edu/ml/citation_policy.html

### Citation

If you use this dataset, please cite:

```
Dua, D. and Graff, C. (2019). UCI Machine Learning Repository 
[http://archive.ics.uci.edu/ml]. Irvine, CA: University of California, 
School of Information and Computer Science.
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Contact

For questions or suggestions, please open an issue on the repository.

## 🙏 Acknowledgments

- UCI Machine Learning Repository for providing the dataset
- All contributors and researchers who have worked on heart disease analysis
- Open-source community for excellent data science tools and libraries

---

**Note**: This project is for educational and research purposes. Always consult healthcare professionals for medical advice and diagnosis.

**Last Updated**: June 2024
