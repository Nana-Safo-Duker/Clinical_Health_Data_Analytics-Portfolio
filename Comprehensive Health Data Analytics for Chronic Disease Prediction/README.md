# Health Data Analysis - Cardiovascular Disease Prediction

## Project Overview

This project provides a comprehensive analysis of cardiovascular disease prediction using health data. The analysis includes statistical analysis, exploratory data analysis, univariate/bivariate/multivariate analysis, and machine learning model development using both Python and R.

## Dataset

The dataset contains 70,000 records with the following features:

- **id**: Patient identifier
- **age**: Age in days
- **gender**: Gender (1 = male, 2 = female)
- **height**: Height in cm
- **weight**: Weight in kg
- **ap_hi**: Systolic blood pressure
- **ap_lo**: Diastolic blood pressure
- **cholesterol**: Cholesterol level (0 = normal, 1 = above normal, 2 = well above normal)
- **gluc**: Glucose level (0 = normal, 1 = above normal, 2 = well above normal)
- **smoke**: Smoking (0 = no, 1 = yes)
- **alco**: Alcohol intake (0 = no, 1 = yes)
- **active**: Physical activity (0 = no, 1 = yes)
- **cardio**: Presence or absence of cardiovascular disease (0 = no, 1 = yes) - **Target Variable**

## Dataset License

This dataset is provided for educational and research purposes. Please refer to the original data source for specific licensing information. If you are the original data provider or have licensing concerns, please contact the repository maintainers.

**Note**: The dataset appears to be a synthetic or anonymized health dataset. Users should ensure they have appropriate permissions and comply with data usage agreements when working with health-related data.

## Project Structure

```
health_data/
├── data/
│   └── health_data.csv          # Original dataset
├── python_notebooks/             # Python Jupyter notebooks
│   ├── 01_statistical_analysis.ipynb
│   ├── 02_univariate_bivariate_multivariate.ipynb
│   ├── 03_comprehensive_eda.ipynb
│   └── 04_ml_analysis.ipynb
├── python_scripts/               # Python scripts
│   ├── statistical_analysis.py
│   ├── univariate_bivariate_multivariate.py
│   ├── comprehensive_eda.py
│   └── ml_analysis.py
├── r_notebooks/                  # R Jupyter notebooks
│   └── README.md
├── r_scripts/                    # R scripts
│   ├── statistical_analysis.R
│   ├── univariate_bivariate_multivariate.R
│   ├── comprehensive_eda.R
│   └── ml_analysis.R
├── results/                      # Analysis results
├── figures/                      # Generated visualizations
├── docs/                         # Documentation
├── requirements.txt              # Python dependencies
├── environment.yml               # Conda environment
├── renv.lock                     # R environment lock file
├── .gitignore                    # Git ignore file
└── README.md                     # This file
```

## Installation

### Python Environment

1. **Using pip:**
```bash
pip install -r requirements.txt
```

2. **Using conda:**
```bash
conda env create -f environment.yml
conda activate health_data_analysis
```

### R Environment

1. **Install required packages:**
```r
install.packages(c("ggplot2", "dplyr", "corrplot", "caret", "VIM", 
                   "psych", "randomForest", "e1071", "pROC", "xgboost",
                   "lightgbm", "GGally", "moments"))
```

2. **Setup R kernel for Jupyter (optional):**
```r
install.packages('IRkernel')
IRkernel::installspec()
```

## Usage

### Python Analysis

#### Running Notebooks:
1. Start Jupyter Notebook:
```bash
jupyter notebook
```

2. Navigate to `python_notebooks/` and open the desired notebook:
   - `01_statistical_analysis.ipynb` - Descriptive, inferential, and exploratory statistics
   - `02_univariate_bivariate_multivariate.ipynb` - Univariate, bivariate, and multivariate analysis
   - `03_comprehensive_eda.ipynb` - Comprehensive exploratory data analysis
   - `04_ml_analysis.ipynb` - Machine learning analysis

#### Running Scripts:
```bash
# Statistical analysis
python python_scripts/statistical_analysis.py

# Univariate, bivariate, multivariate analysis
python python_scripts/univariate_bivariate_multivariate.py

# Comprehensive EDA
python python_scripts/comprehensive_eda.py

# Machine learning analysis
python python_scripts/ml_analysis.py
```

### R Analysis

#### Running Scripts:
```bash
# Statistical analysis
Rscript r_scripts/statistical_analysis.R

# Univariate, bivariate, multivariate analysis
Rscript r_scripts/univariate_bivariate_multivariate.R

# Comprehensive EDA
Rscript r_scripts/comprehensive_eda.R

# Machine learning analysis
Rscript r_scripts/ml_analysis.R
```

#### Running Notebooks:
1. Start Jupyter Notebook:
```bash
jupyter notebook
```

2. Navigate to `r_notebooks/` and open the desired R notebook

## Analysis Components

### 1. Statistical Analysis
- **Descriptive Statistics**: Summary statistics for all variables
- **Inferential Statistics**: T-tests, chi-square tests, correlation analysis
- **Exploratory Data Analysis**: Distribution analysis, visualizations

### 2. Univariate Analysis
- Distribution analysis of individual variables
- Histograms and density plots for numerical variables
- Bar charts for categorical variables
- Statistical measures (mean, median, skewness, kurtosis)

### 3. Bivariate Analysis
- Scatter plots for numerical variable pairs
- Box plots for numerical vs categorical variables
- Heatmaps for categorical variable associations
- Correlation analysis

### 4. Multivariate Analysis
- Correlation matrices
- Pair plots
- 3D scatter plots
- Principal component analysis (if applicable)

### 5. Comprehensive EDA
- Data overview and quality assessment
- Outlier detection and analysis
- Distribution analysis
- Relationship analysis
- Target variable analysis
- Feature engineering insights

### 6. Machine Learning Analysis
- **Models Implemented**:
  - Logistic Regression
  - Random Forest
  - Gradient Boosting
  - XGBoost
  - LightGBM
  - Support Vector Machine (SVM)
- **Evaluation Metrics**:
  - ROC-AUC score
  - Confusion matrix
  - Classification report
  - Cross-validation
- **Feature Importance**: Analysis of feature contributions
- **Hyperparameter Tuning**: Optimization of model parameters

## Results

All generated figures and results are saved in the `figures/` and `results/` directories respectively.

### Key Visualizations:
- Correlation matrices
- Distribution plots
- Box plots by target variable
- ROC curves
- Confusion matrices
- Feature importance plots

## Key Findings

(To be updated based on analysis results)

## Dependencies

### Python:
- pandas >= 2.0.0
- numpy >= 1.24.0
- scipy >= 1.10.0
- matplotlib >= 3.7.0
- seaborn >= 0.12.0
- scikit-learn >= 1.3.0
- xgboost >= 2.0.0
- lightgbm >= 4.0.0
- jupyter >= 1.0.0
- missingno >= 0.5.0

### R:
- ggplot2
- dplyr
- corrplot
- caret
- randomForest
- e1071
- pROC
- xgboost
- lightgbm
- VIM
- psych
- GGally
- moments

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is provided for educational and research purposes. Please ensure you comply with the dataset's original license and any applicable data usage agreements.

## Acknowledgments

- Dataset providers
- Open-source community for excellent data science libraries
- Contributors to this project

## Contact

For questions or issues, please open an issue on the GitHub repository.

## Citation

If you use this project in your research, please cite:

```bibtex
@misc{health_data_analysis,
  title={Health Data Analysis - Cardiovascular Disease Prediction},
  author={Your Name},
  year={2024},
  url={https://github.com/yourusername/health_data_analysis}
}
```

## Changelog

### Version 1.0.0 (2024)
- Initial release
- Comprehensive statistical analysis
- Univariate, bivariate, and multivariate analysis
- Comprehensive EDA
- Machine learning model development
- Support for both Python and R

## Future Work

- [ ] Deep learning models (Neural Networks)
- [ ] Feature engineering enhancements
- [ ] Model interpretation (SHAP values, LIME)
- [ ] Deployment pipeline
- [ ] Interactive dashboards
- [ ] Additional evaluation metrics
- [ ] Cross-validation improvements
- [ ] Ensemble methods

---

**Note**: This project is for educational purposes. Always consult healthcare professionals for medical advice.

