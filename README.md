# Clinical Data Science & Health Analytics

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![R](https://img.shields.io/badge/R-4.0%2B-blue.svg)](https://www.r-project.org/)
[![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-orange.svg)](https://jupyter.org/)

A comprehensive repository of clinical data science and health analytics projects focusing on disease prediction, risk stratification, and treatment pattern analysis using advanced machine learning algorithms and statistical modeling techniques.

**Portfolio Website**: [https://nana-safo-duker.github.io/](https://nana-safo-duker.github.io/)

---

## 📋 Table of Contents

- [Overview](#overview)
- [Research Projects](#research-projects)
- [Technologies & Tools](#technologies--tools)
- [Repository Structure](#repository-structure)
- [Getting Started](#getting-started)
- [Project Details](#project-details)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

---

## 🎯 Overview

This repository contains a collection of **8 comprehensive clinical data science projects** that demonstrate the application of machine learning, statistical analysis, and data-driven approaches to healthcare challenges. Each project includes:

- **Statistical Analysis**: Descriptive, inferential, and exploratory statistics
- **Exploratory Data Analysis (EDA)**: Univariate, bivariate, and multivariate analysis
- **Machine Learning Models**: Multiple algorithms for prediction and classification
- **Dual Implementation**: Complete analysis in both **Python** and **R**
- **Comprehensive Documentation**: Detailed README files, setup guides, and project summaries

### Key Focus Areas

- 🫀 **Cardiovascular Disease Prediction**
- 🦠 **Infectious Disease Modeling**
- 🧬 **Cancer Detection and Classification**
- 💉 **Diabetes Risk Assessment**
- 💊 **Treatment Pattern Analysis**

---

## 🔬 Research Projects

### 1. AI-Driven Breast Cancer Detection and Classification using Machine Learning Algorithms

**Description**: Developed an AI-driven pipeline for breast cancer detection and classification using advanced machine learning algorithms to improve diagnostic accuracy. The project analyzes the Breast Cancer Wisconsin (Diagnostic) dataset with 569 instances and 30 features computed from digitized images of fine needle aspirates.

**Key Features**:
- Classification of tumors as malignant (M) or benign (B)
- Multiple ML algorithms: Logistic Regression, Random Forest, SVM, Gradient Boosting, KNN, Neural Networks
- Comprehensive statistical and exploratory data analysis
- Python and R implementations

**Dataset**: Breast Cancer Wisconsin (Diagnostic) Dataset from UCI Machine Learning Repository

---

### 2. Cardiovascular Disease Prediction using Machine Learning and Clinical Data

**Description**: Implemented machine learning models for cardiovascular disease prediction leveraging clinical and demographic datasets. The analysis includes 1,000 patient records with 14 features including age, gender, chest pain type, blood pressure, cholesterol levels, and electrocardiographic results.

**Key Features**:
- Binary classification (disease/no disease)
- Feature engineering and selection
- Model evaluation with cross-validation
- Comprehensive statistical analysis

**Dataset**: Cardiovascular Disease Dataset (1,000 records, 14 features)

---

### 3. Comprehensive Health Data Analytics for Chronic Disease Prediction

**Description**: Created a comprehensive health data analytics framework for chronic disease risk assessment and prediction. The project analyzes a large-scale health dataset with 70,000 records containing patient demographics, vital signs, lifestyle factors, and cardiovascular disease indicators.

**Key Features**:
- Large-scale data analysis (70,000+ records)
- Multiple chronic disease risk factors
- Advanced feature engineering
- Ensemble modeling approaches

**Dataset**: Health Data (70,000 records with 13 features)

---

### 4. Heart Disease Risk Stratification through Data-Driven Predictive Analytics

**Description**: Built a data-driven predictive analytics model for heart disease risk stratification and patient profiling. The project provides comprehensive analysis including descriptive statistics, hypothesis testing, correlation analysis, and multiple ML algorithms for heart disease prediction.

**Key Features**:
- Risk stratification models
- Patient profiling and segmentation
- Statistical significance testing
- Comprehensive EDA

**Dataset**: Heart Disease Dataset from UCI Machine Learning Repository

---

### 5. Infectious Disease Case Detection and Modeling Framework

**Description**: Developed an infectious disease detection and modeling framework using real-world clinical surveillance data. The project analyzes cancer incidence data at the county level across the United States, including age-adjusted incidence rates, confidence intervals, and trend analysis.

**Key Features**:
- County-level epidemiological analysis
- Trend detection and forecasting
- Spatial analysis capabilities
- Public health surveillance modeling

**Dataset**: Cancer Incidence Data (INCD) from SEER/NPCR programs

---

### 6. Pima Indians Diabetes Prediction - A Comparative Machine Learning Approach

**Description**: Performed a comparative machine learning study for the Pima Indians dataset to predict diabetes susceptibility. The project includes comprehensive analysis of 768 observations with 8 predictor variables, comparing multiple ML algorithms to identify the most effective prediction model.

**Key Features**:
- Comparative ML algorithm analysis
- Feature importance analysis
- Model performance benchmarking
- Statistical validation

**Dataset**: Pima Indians Diabetes Dataset from UCI Machine Learning Repository (768 observations, 8 features)

---

### 7. Predicting Type 2 Diabetes Risk from Behavioral and Health Indicator

**Description**: Implemented a predictive model for Type 2 Diabetes risk assessment using behavioral and health indicators from the Behavioral Risk Factor Surveillance System (BRFSS) 2021. The analysis includes 236,380 records with 22 features covering demographics, health behaviors, and medical history.

**Key Features**:
- Large-scale behavioral health analysis
- Risk factor identification
- Population health insights
- BRFSS 2021 dataset analysis

**Dataset**: Diabetes Binary Health Indicators - BRFSS 2021 (236,380 records, 22 features)

---

### 8. Treatment Start Patterns and Adherence Modeling for Clinical Interventions

**Description**: Analyzed treatment start patterns and modeled patient adherence behaviors for clinical interventions. The project examines cancer treatment data including treatment start dates, drug types (Cisplatin and Nivolumab), dosages, and patient adherence patterns.

**Key Features**:
- Treatment pattern analysis
- Patient adherence modeling
- Temporal pattern detection
- Clinical intervention evaluation

**Dataset**: Mock Treatment Starts 2016 (25 treatment records, 20 unique patients)

---

## 🛠️ Technologies & Tools

### Programming Languages
- **Python 3.8+**: Primary language for data analysis and machine learning
- **R 4.0+**: Statistical analysis and advanced modeling

### Key Libraries & Frameworks

#### Python
- **Data Science**: pandas, numpy, scipy
- **Machine Learning**: scikit-learn, xgboost, lightgbm
- **Visualization**: matplotlib, seaborn, plotly
- **Statistical Analysis**: statsmodels
- **Deep Learning**: tensorflow, keras (where applicable)

#### R
- **Data Manipulation**: dplyr, tidyr, data.table
- **Statistical Analysis**: stats, car, psych
- **Machine Learning**: caret, randomForest, e1071, xgboost
- **Visualization**: ggplot2, plotly, corrplot
- **Reporting**: rmarkdown, knitr

### Development Tools
- **Jupyter Notebooks**: Interactive analysis and documentation
- **R Markdown**: Reproducible research reports
- **Git**: Version control
- **GitHub**: Repository hosting and collaboration

---

## 📁 Repository Structure

```
Clinical-Data-Science-Health-Analytics/
│
├── AI-Driven Breast Cancer Detection and Classification using Machine Learning Algorithms/
│   ├── data/
│   ├── notebooks/ (python/ & r/)
│   ├── scripts/ (python/ & r/)
│   ├── results/
│   ├── models/
│   ├── docs/
│   └── README.md
│
├── Cardiovascular Disease Prediction using Machine Learning and Clinical Data/
│   ├── data/
│   ├── notebooks/ (python/ & r/)
│   ├── scripts/ (python/ & r/)
│   ├── results/
│   ├── models/
│   └── README.md
│
├── Comprehensive Health Data Analytics for Chronic Disease Prediction/
│   ├── data/
│   ├── python_notebooks/
│   ├── python_scripts/
│   ├── r_notebooks/
│   ├── r_scripts/
│   ├── results/
│   └── README.md
│
├── Heart Disease Risk Stratification through Data-Driven Predictive Analytics/
│   ├── data/
│   ├── notebooks/ (python/ & r/)
│   ├── scripts/ (python/ & r/)
│   ├── results/
│   └── README.md
│
├── Infectious Disease Case Detection and Modeling Framework/
│   ├── data/
│   ├── notebooks/ (python/ & r/)
│   ├── scripts/ (python/ & r/)
│   └── README.md
│
├── Pima Indians Diabetes Prediction - A Comparative Machine Learning Approach/
│   ├── data/
│   ├── notebooks/ (python/ & r/)
│   ├── scripts/ (python/ & r/)
│   ├── outputs/
│   └── README.md
│
├── Predicting Type 2 Diabetes Risk from Behavioral and Health Indicator/
│   ├── data/
│   ├── notebooks/ (python/ & r/)
│   ├── scripts/ (python/ & r/)
│   ├── results/
│   └── README.md
│
└── Treatment Start Patterns and Adherence Modeling for Clinical Interventions/
    ├── data/
    ├── notebooks/ (python/ & r/)
    ├── scripts/ (python/ & r/)
    ├── docs/
    └── README.md
```

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.8+** with pip
- **R 4.0+** with CRAN packages
- **Jupyter Notebook** (for Python notebooks)
- **RStudio** or R with rmarkdown (for R notebooks)
- **Git** for version control

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Nana-Safo-Duker/Clinical-Data-Science-Health-Analytics.git
   cd Clinical-Data-Science-Health-Analytics
   ```

2. **Set up Python environment**:
   ```bash
   # Navigate to a specific project folder
   cd "AI-Driven Breast Cancer Detection and Classification using Machine Learning Algorithms"
   
   # Install Python dependencies
   pip install -r requirements.txt
   ```

3. **Set up R environment**:
   ```r
   # In R or RStudio
   # Navigate to project folder and run:
   source("packages.R")  # or install packages from requirements_r.txt
   ```

4. **Run Jupyter Notebooks**:
   ```bash
   jupyter notebook
   ```

### Project-Specific Setup

Each project folder contains:
- `README.md`: Detailed project documentation
- `requirements.txt`: Python dependencies
- `requirements_r.txt` or `packages.R`: R dependencies
- `SETUP.md` or `SETUP_GUIDE.md`: Step-by-step setup instructions

**Note**: Refer to individual project README files for specific setup instructions and dataset information.

---

## 📊 Project Details

Each project follows a consistent analysis workflow:

1. **Statistical Analysis** (`01_statistical_analysis`)
   - Descriptive statistics
   - Inferential statistics
   - Data quality assessment

2. **Univariate/Bivariate/Multivariate Analysis** (`02_univariate_bivariate_multivariate`)
   - Variable distributions
   - Correlation analysis
   - Feature relationships

3. **Comprehensive EDA** (`03_comprehensive_eda`)
   - Data visualization
   - Pattern identification
   - Outlier detection

4. **Machine Learning Analysis** (`04_ml_analysis`)
   - Model training and evaluation
   - Hyperparameter tuning
   - Performance metrics
   - Model comparison

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Contribution Guidelines

- Follow the existing code structure and documentation style
- Include comprehensive documentation for new features
- Ensure all analyses are reproducible
- Add appropriate citations for datasets and methodologies
- Test your code before submitting

---

## 📄 License

This repository is licensed under the MIT License. However, individual projects may have different licensing terms for datasets. Please refer to:

- Individual project README files for dataset-specific licensing information
- Original data source licenses (UCI ML Repository, Kaggle, CDC, etc.)
- Healthcare data compliance requirements (HIPAA, GDPR where applicable)

**Important**: Ensure compliance with data usage agreements and ethical guidelines when working with clinical and health data.

---

## 👤 Contact

**Nana Safo Duker**

- **Portfolio Website**: [https://nana-safo-duker.github.io/](https://nana-safo-duker.github.io/)
- **GitHub**: [@Nana-Safo-Duker](https://github.com/Nana-Safo-Duker)
- **Email**: freshsafoduker300@gmail.com

### Research Focus

AI/ML and Bioinformatics Researcher dedicated to advancing:
- 🧬 Cancer genomics and precision medicine
- 🦠 Infectious disease modeling
- 💊 Digital health innovation
- 🤖 Ethical AI in healthcare

---

## 📚 References & Citations

### Datasets

- **UCI Machine Learning Repository**: [https://archive.ics.uci.edu/ml/](https://archive.ics.uci.edu/ml/)
- **Kaggle**: [https://www.kaggle.com/](https://www.kaggle.com/)
- **CDC BRFSS**: [https://www.cdc.gov/brfss/](https://www.cdc.gov/brfss/)
- **SEER/NPCR**: National Cancer Institute Surveillance Programs

### Key Publications

Please refer to individual project README files for specific dataset citations and references.

---

## 🌟 Acknowledgments

- UCI Machine Learning Repository for providing open-access datasets
- Kaggle community for datasets and learning resources
- CDC and NCI for public health surveillance data
- Open-source community for excellent tools and libraries

---

**Built with ❤️ for advancing clinical data science and health analytics**

*Last Updated: 2025*

