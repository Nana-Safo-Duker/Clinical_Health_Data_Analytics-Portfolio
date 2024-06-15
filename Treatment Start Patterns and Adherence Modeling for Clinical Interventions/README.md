# Clinical Data Science & Health Analytics: Treatment Starts 2016 Analysis

## Project Overview

This project performs comprehensive statistical analysis, exploratory data analysis (EDA), and machine learning analysis on a clinical dataset containing treatment starts for cancer patients in 2016. The dataset includes patient treatment information for two drugs: Cisplatin and Nivolumab.

## Dataset Description

The dataset (`mock_treatment_starts_2016.csv`) contains the following variables:
- **PatientID**: Unique patient identifier
- **TreatmentStart**: Date when treatment started (MM/DD/YY format)
- **Drug**: Type of drug administered (Cisplatin or Nivolumab)
- **Dosage**: Dosage amount in milligrams

### Dataset Statistics
- **Total Records**: 25 treatment records
- **Unique Patients**: 20 patients
- **Date Range**: January 2, 2016 to June 17, 2016
- **Drugs**: Cisplatin (16 treatments) and Nivolumab (9 treatments)

## Project Structure

```
.
├── data/
│   └── mock_treatment_starts_2016.csv
├── notebooks/
│   ├── python/
│   │   ├── 01_statistical_analysis.ipynb
│   │   ├── 02_univariate_bivariate_multivariate_analysis.ipynb
│   │   ├── 03_comprehensive_eda.ipynb
│   │   └── 04_ml_analysis.ipynb
│   └── r/
│       ├── 01_statistical_analysis.Rmd
│       ├── 02_univariate_bivariate_multivariate_analysis.Rmd
│       ├── 03_comprehensive_eda.Rmd
│       └── 04_ml_analysis.Rmd
├── scripts/
│   ├── python/
│   │   ├── univariate_bivariate_multivariate_analysis.py
│   │   └── comprehensive_eda.py
│   └── r/
│       ├── univariate_bivariate_multivariate_analysis.R
│       └── comprehensive_eda.R
├── docs/
├── .gitignore
├── requirements.txt
├── environment.yml
├── packages.R (R dependencies)
└── README.md
```

## Analysis Components

### 1. Statistical Analysis
- **Descriptive Statistics**: Summary statistics, central tendencies, dispersion measures
- **Inferential Statistics**: Hypothesis testing, confidence intervals, normality tests
- **Exploratory Statistics**: Outlier detection, temporal patterns, data anomalies

### 2. Univariate, Bivariate, and Multivariate Analysis
- **Univariate**: Single variable analysis (distribution, summary statistics)
- **Bivariate**: Two-variable relationships (correlations, associations)
- **Multivariate**: Multiple variable interactions (heatmaps, grouped analyses)

### 3. Comprehensive EDA
- Data quality assessment
- Missing value analysis
- Outlier detection and treatment
- Distribution analysis
- Relationship exploration
- Temporal pattern analysis
- Patient-level analysis

### 4. Machine Learning Analysis
- Feature engineering
- Model selection and training (Linear Regression, Random Forest, Gradient Boosting, XGBoost)
- Model evaluation and comparison
- Feature importance analysis
- Cross-validation

## Setup Instructions

### Python Environment

#### Option 1: Using Conda (Recommended)
```bash
# Create conda environment
conda env create -f environment.yml

# Activate environment
conda activate clinical_data_analysis
```

#### Option 2: Using pip
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### R Environment

#### Install R Packages
```r
# Run the packages.R script to install all required packages
source("packages.R")

# Or install manually:
install.packages(c("dplyr", "ggplot2", "tidyr", "lubridate", 
                   "corrplot", "gridExtra", "moments", "caret",
                   "randomForest", "gbm", "xgboost", "VIM"))
```

## Usage

### Python Notebooks

1. Navigate to the notebooks directory:
```bash
cd notebooks/python
```

2. Start Jupyter Notebook:
```bash
jupyter notebook
```

3. Open and run the notebooks in order:
   - `01_statistical_analysis.ipynb`
   - `02_univariate_bivariate_multivariate_analysis.ipynb`
   - `03_comprehensive_eda.ipynb`
   - `04_ml_analysis.ipynb`

### Python Scripts

Run the Python scripts from the project root:
```bash
# Univariate, Bivariate, Multivariate Analysis
python scripts/python/univariate_bivariate_multivariate_analysis.py

# Comprehensive EDA
python scripts/python/comprehensive_eda.py
```

### R Notebooks

1. Open RStudio or R console
2. Navigate to the notebooks/r directory
3. Open the `.Rmd` files and knit them to HTML or run interactively

### R Scripts

Run the R scripts from the project root:
```r
# Univariate, Bivariate, Multivariate Analysis
source("scripts/r/univariate_bivariate_multivariate_analysis.R")

# Comprehensive EDA
source("scripts/r/comprehensive_eda.R")
```

## Key Findings

1. **Drug Distribution**: Cisplatin is used more frequently (64%) compared to Nivolumab (36%)
2. **Dosage Patterns**: Significant difference in dosage between the two drugs
3. **Temporal Trends**: Treatment starts are distributed across months, with some seasonal patterns
4. **Outliers**: One potential data entry error detected (PT12 with dosage 1800, likely should be 180)
5. **Patient Patterns**: Some patients have multiple treatment records, indicating combination or sequential therapy

## Machine Learning Results

The ML analysis compares multiple algorithms:
- **Linear Regression**: Baseline model
- **Random Forest**: Ensemble method with good interpretability
- **Gradient Boosting**: Strong performance for regression tasks
- **XGBoost**: Advanced gradient boosting with regularization

Best performing model varies based on evaluation metrics (RMSE, R², MAE).

## Dataset License

**Note**: This is a mock dataset created for educational and analytical purposes. 

### Original Dataset License Reference

If this dataset is based on or derived from a real clinical dataset, please refer to the original dataset's license terms. Common licenses for clinical/health data include:

- **HIPAA Compliance**: All patient identifiers have been anonymized
- **Research Use Only**: This dataset is intended for research and educational purposes only
- **No Commercial Use**: The dataset may not be used for commercial purposes without proper authorization
- **Attribution Required**: If using this dataset, please cite the original source

### Data Usage Guidelines

1. **Privacy**: All patient identifiers are anonymized (mock data)
2. **Ethical Use**: Use this data responsibly and in accordance with medical research ethics
3. **No Medical Advice**: This analysis is for educational purposes and should not be used for medical decision-making
4. **Attribution**: If publishing results, please acknowledge the data source

## Contributing

This is an educational project. Contributions, suggestions, and improvements are welcome!

## Author

Clinical Data Science & Health Analytics Project

## Acknowledgments

- Dataset: Mock treatment starts data for 2016
- Tools: Python, R, Jupyter Notebooks, RStudio
- Libraries: pandas, scikit-learn, ggplot2, dplyr, and others

## License

This project is provided for educational purposes. Please refer to the original dataset license for data usage terms.

## Contact

For questions or issues, please open an issue in the repository or contact the project maintainer.

---

**Disclaimer**: This is a mock dataset created for educational purposes. Any resemblance to real patient data is purely coincidental. This analysis should not be used for actual medical decision-making.


