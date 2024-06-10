# Predicting Cancer Outcomes with Radiomics and Artificial Intelligence

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![R 4.0+](https://img.shields.io/badge/R-4.0+-blue.svg)](https://www.r-project.org/)

A comprehensive research project exploring the application of radiomics and machine learning techniques for predicting cancer outcomes from medical imaging data. This repository provides a complete workflow including data analysis, statistical methods, machine learning models, and detailed documentation.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Project Structure](#project-structure)
- [Usage](#usage)
- [Methodology](#methodology)
- [Results](#results)
- [Contributing](#contributing)
- [License](#license)
- [References](#references)

## 🎯 Overview

This project investigates how quantitative image features (radiomics) extracted from medical images can be combined with artificial intelligence to predict cancer patient outcomes. The research addresses a fundamental question in precision oncology: *Can quantitative image analysis improve our ability to predict cancer outcomes beyond conventional clinical methods?*

### Key Objectives

- Extract and analyze radiomic features from medical images
- Identify statistically significant features associated with patient outcomes
- Develop and evaluate machine learning models for outcome prediction
- Provide reproducible analysis workflows in both Python and R
- Create comprehensive documentation and visualizations

## ✨ Features

### Analysis Components

- **Radiomic Feature Extraction**: First-order statistics, texture features (GLCM, GLRLM), and shape features
- **Statistical Analysis**: 
  - T-tests for group comparisons
  - Correlation analysis
  - Principal Component Analysis (PCA)
  - Effect size calculations (Cohen's d)
- **Machine Learning Models**:
  - Random Forest Classifier
  - Support Vector Machine (SVM)
  - Feature selection and dimensionality reduction
  - Cross-validation for model assessment
- **Visualizations**: 
  - Feature distribution plots
  - Correlation heatmaps
  - ROC curves
  - Confusion matrices
  - Feature importance rankings

### Code Implementations

- **Python**: Complete analysis pipeline with object-oriented design
- **R**: Statistical analysis functions and survival analysis capabilities
- **Jupyter Notebook**: Interactive exploration and step-by-step analysis

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- R 4.0 or higher (optional, for R scripts)
- Git

### Python Environment Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/radiomics-cancer-prediction.git
cd radiomics-cancer-prediction
```

2. Create a virtual environment (recommended):
```bash
# Using venv
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

3. Install Python dependencies:
```bash
pip install -r requirements.txt
```

### R Environment Setup (Optional)

If you plan to use the R scripts:

1. Install R packages:
```r
install.packages(c("dplyr", "tidyr", "ggplot2", "gridExtra", "corrplot", 
                   "pheatmap", "survival", "survminer", "randomForest", 
                   "caret", "VIM", "car"))
```

2. Run R scripts:
```bash
Rscript radiomics_statistical_analysis.R
```

## 📁 Project Structure

```
.
├── README.md                           # This file
├── LICENSE                              # MIT License
├── requirements.txt                     # Python dependencies
├── .gitignore                          # Git ignore rules
├── .gitattributes                       # Git attributes for line endings
│
├── Guidelines_Research_Paper_Review.txt # Review guidelines
│
├── radiomics_analysis.ipynb            # Jupyter notebook (complete workflow)
├── radiomics_analysis.py               # Python analysis pipeline
├── radiomics_statistical_analysis.R    # R statistical analysis script
│
├── data/                               # Data directory (gitignored)
│   └── example/                        # Example data files
│
├── output/                             # Output directory (gitignored)
│   ├── figures/                        # Generated plots and visualizations
│   └── results/                        # Analysis results
│
└── docs/                               # Additional documentation
    └── methodology.md                  # Detailed methodology notes
```

## 💻 Usage

### Jupyter Notebook (Recommended for Exploration)

1. Start Jupyter Notebook:
```bash
jupyter notebook
```

2. Open `radiomics_analysis.ipynb` and run cells sequentially

The notebook provides:
- Step-by-step analysis with explanations
- Interactive visualizations
- Code comments and methodology notes

### Python Script

Run the complete analysis pipeline:

```bash
python radiomics_analysis.py
```

This will:
1. Load or generate synthetic radiomic data
2. Perform statistical analysis
3. Build and evaluate ML models
4. Generate visualizations

### R Script

For R-based statistical analysis:

```bash
Rscript radiomics_statistical_analysis.R
```

The R script provides:
- Descriptive statistics
- Hypothesis testing (t-tests, Mann-Whitney U)
- Correlation analysis
- PCA
- Survival analysis (if survival data available)
- Random Forest modeling

## 📊 Methodology

### Radiomic Feature Extraction

Radiomic features are categorized into:

1. **First-order Statistics**: Intensity distribution measures
   - Mean, median, standard deviation
   - Entropy, energy, skewness, kurtosis

2. **Texture Features**: Spatial relationship patterns
   - Gray Level Co-occurrence Matrix (GLCM)
   - Gray Level Run Length Matrix (GLRLM)
   - Gray Level Size Zone Matrix (GLSZM)

3. **Shape Features**: Geometric characteristics
   - Volume, surface area, sphericity, compactness

### Statistical Methods

#### Hypothesis Testing

- **T-test**: Used to compare mean feature values between outcome groups
  - Appropriate for normally distributed data
  - Enables straightforward hypothesis testing on differences of means
  - Assumptions: Independence, normality, equal variances

- **Effect Size**: Cohen's d calculated to assess practical significance

#### Dimensionality Reduction

- **Principal Component Analysis (PCA)**: 
  - Chosen for interpretability and linear assumptions
  - Aligns well with radiomic datasets showing linear relationships
  - Reduces feature space while preserving variance

### Machine Learning Pipeline

1. **Data Preprocessing**:
   - Missing value imputation (median)
   - Feature scaling (StandardScaler)
   
2. **Feature Selection**:
   - SelectKBest with F-classification score
   - Selects top features based on statistical significance

3. **Model Training**:
   - Random Forest: Handles non-linear relationships and feature interactions
   - SVM: Effective for high-dimensional data with complex decision boundaries

4. **Model Evaluation**:
   - Train-test split (80-20)
   - 5-fold stratified cross-validation
   - Metrics: Accuracy, Precision, Recall, F1-score, ROC-AUC

5. **Visualization**:
   - ROC curves
   - Confusion matrices
   - Feature importance plots

## 📈 Results

### Key Findings

1. **Feature Significance**: Multiple radiomic features show significant associations with patient outcomes, particularly:
   - First-order entropy (higher entropy → worse outcomes)
   - GLCM correlation (lower correlation → worse outcomes)

2. **Model Performance**: 
   - Random Forest typically achieves superior performance
   - ROC-AUC scores often exceed 0.75
   - Models generalize well with proper cross-validation

3. **Clinical Implications**:
   - Quantitative image features provide prognostic information
   - Radiomics can complement traditional clinical factors
   - Potential for non-invasive biomarker development

### Limitations

- **Data**: Current analysis uses synthetic data; real-world validation needed
- **Reproducibility**: Feature extraction parameters must be standardized
- **Generalizability**: Models require validation on independent cohorts
- **Interpretability**: Balance needed between accuracy and clinical interpretability

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Contribution Guidelines

- Follow PEP 8 style guide for Python code
- Add docstrings to functions and classes
- Include tests for new features
- Update documentation as needed
- Ensure code is compatible with Python 3.8+

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📚 References

### Scientific Literature

1. Lambin, P., et al. (2017). Radiomics: the bridge between medical imaging and personalized medicine. *Nature Reviews Clinical Oncology*, 14(12), 749-762.

2. Aerts, H. J., et al. (2014). Decoding tumour phenotype by noninvasive imaging using a quantitative radiomics approach. *Nature Communications*, 5, 4006.

3. Gillies, R. J., Kinahan, P. E., & Hricak, H. (2016). Radiomics: Images Are More than Pictures, They Are Data. *Radiology*, 278(2), 563-577.

4. Liu, Z., et al. (2017). The Applications of Radiomics in Precision Diagnosis and Treatment of Oncology: Opportunities and Challenges. *Theranostics*, 7(16), 3203-3209.

5. van Timmeren, J. E., et al. (2020). Radiomics in medical imaging—"how-to" guide and critical reflection. *Insights into Imaging*, 11(1), 91.

### Tools and Libraries

- **PyRadiomics**: Open-source Python package for radiomic feature extraction
- **scikit-learn**: Machine learning library for Python
- **pandas**: Data manipulation and analysis
- **numpy**: Numerical computing
- **matplotlib/seaborn**: Data visualization

### Related Resources

- [The Cancer Imaging Archive (TCIA)](https://www.cancerimagingarchive.net/)
- [Image Biomarker Standardization Initiative (IBSI)](https://ibsi.readthedocs.io/)
- [Radiomics.org](https://www.radiomics.org/)

## 📧 Contact

For questions, suggestions, or collaboration inquiries, please open an issue on GitHub.

## 🙏 Acknowledgments

- The radiomics and medical imaging research community
- Developers of open-source tools (PyRadiomics, scikit-learn, etc.)
- Researchers whose work has advanced the field of precision oncology

---

**Note**: This project is for educational and research purposes. Clinical applications require proper validation, regulatory approval, and ethical considerations. Always consult with medical professionals for clinical decision-making.

