# Cardiovascular Disease Dataset - Comprehensive Analysis

## Project Overview

This project provides a comprehensive statistical and machine learning analysis of cardiovascular disease data. The analysis includes descriptive, inferential, and exploratory statistics, univariate, bivariate, and multivariate analyses, comprehensive EDA, and machine learning model development in both Python and R.

## Dataset Information

- **Dataset Name**: Cardiovascular Disease Dataset
- **Rows**: 1,000
- **Features**: 14
- **Target Variable**: `target` (binary: 0 = no disease, 1 = disease)

### Features

1. `patientid` - Unique patient identifier
2. `age` - Age of the patient
3. `gender` - Gender (0 = female, 1 = male)
4. `chestpain` - Chest pain type (0-3)
5. `restingBP` - Resting blood pressure
6. `serumcholestrol` - Serum cholesterol level
7. `fastingbloodsugar` - Fasting blood sugar > 120 mg/dl (0 = no, 1 = yes)
8. `restingrelectro` - Resting electrocardiographic results (0-2)
9. `maxheartrate` - Maximum heart rate achieved
10. `exerciseangia` - Exercise induced angina (0 = no, 1 = yes)
11. `oldpeak` - ST depression induced by exercise relative to rest
12. `slope` - The slope of the peak exercise ST segment (0-3)
13. `noofmajorvessels` - Number of major vessels colored by fluoroscopy (0-3)
14. `target` - Presence of cardiovascular disease (0 = no, 1 = yes)

## Dataset License

**Important License Information**: This dataset is provided for educational and research purposes only. Please ensure you have proper authorization and comply with the original dataset's license terms before using this data.

### Original Dataset Source

This cardiovascular disease dataset may be derived from:
- **UCI Machine Learning Repository**: If the dataset originates from UCI, it typically falls under their [citation policy](https://archive.ics.uci.edu/ml/citation_policy.html) which requires proper citation but allows use for research and educational purposes.
- **Kaggle**: If obtained from Kaggle, please refer to the specific dataset's license on the Kaggle platform.
- **Other Sources**: Please reference the original source and comply with their specific license terms.

### License Compliance

1. **Citation**: If you use this dataset, please cite the original source appropriately.
2. **Healthcare Data Considerations**: Healthcare/medical data may have additional privacy and ethical considerations. Ensure compliance with:
   - HIPAA (Health Insurance Portability and Accountability Act) if applicable
   - GDPR (General Data Protection Regulation) if applicable
   - Local data protection laws
   - Institutional review board (IRB) requirements for research
3. **Data Usage**: This dataset should only be used for:
   - Educational purposes
   - Research purposes
   - Non-commercial applications
4. **Disclaimer**: The authors and contributors of this repository are not responsible for any misuse of the dataset. Users are solely responsible for ensuring compliance with all applicable laws and regulations.

### Recommended Citation Format

If using this dataset, please cite as:
```
Cardiovascular Disease Dataset. [Original Source]. 
Accessed: [Date]. 
License: [License Type - Please verify from original source]
```

**Note**: Always verify the current license status from the original data source before publication or commercial use.

## Project Structure

```
Cardiovascular_Disease_Dataset/
│
├── data/
│   └── Cardiovascular_Disease_Dataset.csv
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
│   │   ├── univariate_analysis.py
│   │   ├── bivariate_analysis.py
│   │   └── multivariate_analysis.py
│   │
│   └── r/
│       ├── statistical_analysis.R
│       ├── univariate_analysis.R
│       ├── bivariate_analysis.R
│       └── multivariate_analysis.R
│
├── results/
│   └── (analysis outputs, plots, etc.)
│
├── models/
│   └── (trained ML models)
│
├── docs/
│   └── (documentation files)
│
├── requirements.txt
├── R_packages.R
├── .gitignore
├── LICENSE.md
└── README.md
```

## GitHub Repository Setup

### Initializing the Repository

1. **Initialize Git repository** (if not already initialized):
```bash
git init
```

2. **Add all files**:
```bash
git add .
```

3. **Create initial commit**:
```bash
git commit -m "Initial commit: Cardiovascular Disease Analysis Project"
```

4. **Create GitHub repository**:
   - Go to GitHub and create a new repository
   - Link local repository to remote:
```bash
git remote add origin https://github.com/yourusername/cardiovascular-disease-analysis.git
git branch -M main
git push -u origin main
```

### Repository Structure

The project follows a well-organized structure suitable for:
- Version control with Git
- Collaborative development
- Reproducible research
- Documentation and sharing

## Installation

### Python Environment

1. Create a virtual environment:
```bash
python -m venv venv
```

2. Activate the virtual environment:
- Windows: `venv\Scripts\activate`
- macOS/Linux: `source venv/bin/activate`

3. Install dependencies:
```bash
pip install -r requirements.txt
```

### R Environment

1. Install required R packages (run in R or RStudio):
```r
install.packages(c("tidyverse", "ggplot2", "dplyr", "corrplot", "caret", 
                   "randomForest", "e1071", "rpart", "xgboost", "VIM", 
                   "psych", "Hmisc", "car", "vcd", "gridExtra", "pROC",
                   "pander", "factoextra", "FactoMineR", "GGally", "ggcorrplot"))
```

2. For R Markdown notebooks, ensure you have `rmarkdown` installed:
```r
install.packages("rmarkdown")
```

3. **Alternative: Use the installation script**:
```r
source("R_packages.R")
```

This will automatically install and load all required packages.

## Usage

### Python Analysis

1. **Statistical Analysis**: Open `notebooks/python/01_statistical_analysis.ipynb`
2. **Univariate/Bivariate/Multivariate**: Open `notebooks/python/02_univariate_bivariate_multivariate.ipynb`
3. **Comprehensive EDA**: Open `notebooks/python/03_comprehensive_eda.ipynb`
4. **ML Analysis**: Open `notebooks/python/04_ml_analysis.ipynb`

### R Analysis

1. **Statistical Analysis**: Open `notebooks/r/01_statistical_analysis.Rmd`
2. **Univariate/Bivariate/Multivariate**: Open `notebooks/r/02_univariate_bivariate_multivariate.Rmd`
3. **Comprehensive EDA**: Open `notebooks/r/03_comprehensive_eda.Rmd`
4. **ML Analysis**: Open `notebooks/r/04_ml_analysis.Rmd`

### Scripts

Run Python scripts:
```bash
# From the project root directory
python scripts/python/statistical_analysis.py
python scripts/python/univariate_analysis.py
python scripts/python/bivariate_analysis.py
python scripts/python/multivariate_analysis.py
```

Run R scripts:
```bash
# From the project root directory
Rscript scripts/r/statistical_analysis.R
Rscript scripts/r/univariate_analysis.R
Rscript scripts/r/bivariate_analysis.R
Rscript scripts/r/multivariate_analysis.R
```

## Analysis Components

### 1. Statistical Analysis
- Descriptive statistics
- Inferential statistics
- Exploratory data analysis
- Hypothesis testing

### 2. Univariate Analysis
- Distribution analysis
- Central tendency measures
- Dispersion measures
- Outlier detection

### 3. Bivariate Analysis
- Correlation analysis
- Cross-tabulations
- Association tests
- Feature-target relationships

### 4. Multivariate Analysis
- Principal Component Analysis (PCA)
- Factor Analysis
- Multivariate relationships
- Feature interactions

### 5. Comprehensive EDA
- Data quality assessment
- Missing value analysis
- Data visualization
- Pattern recognition

### 6. Machine Learning Analysis
- Data preprocessing
- Feature engineering
- Model selection
- Model evaluation
- Hyperparameter tuning
- Model comparison

## Machine Learning Models

The project includes implementations of:
- Logistic Regression
- Random Forest
- XGBoost
- LightGBM
- Support Vector Machine (SVM)
- Decision Tree
- K-Nearest Neighbors (KNN)
- Neural Networks (optional)

## Results

All analysis results, visualizations, and model outputs are saved in the `results/` directory. Make sure this directory exists before running scripts:

```bash
mkdir -p results
```

### Output Files

- **Python Scripts**: Generate PNG plots in the `results/` directory
- **R Scripts**: Generate PNG plots in the `results/` directory  
- **Notebooks**: Display plots inline and can export to HTML/PDF
- **ML Models**: Trained models are saved in the `models/` directory (if implemented)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

Please refer to [LICENSE.md](LICENSE.md) for detailed license information. 

**Summary**:
- **Dataset**: Please refer to the original dataset license for data usage terms. See the [Dataset License](#dataset-license) section above for details.
- **Code**: Analysis code in this repository is provided under the MIT License for educational and research purposes.
- **Important**: Always verify and comply with the original dataset's license terms and applicable healthcare data regulations before use.

## Author

[Your Name/Organization]

## Acknowledgments

- Original dataset creators
- Open-source community for tools and libraries
- Medical and healthcare data science community

## References

- [UCI Machine Learning Repository](https://archive.ics.uci.edu/ml/index.php)
- [Kaggle](https://www.kaggle.com/)
- Scikit-learn documentation
- R documentation

