# Setup Guide

This guide will help you set up the environment to run the health data analysis project.

## Prerequisites

- Python 3.8 or higher
- R 4.0 or higher (optional, for R analysis)
- Git
- Jupyter Notebook or JupyterLab (for running notebooks)

## Python Setup

### Option 1: Using pip

1. Create a virtual environment (recommended):
```bash
python -m venv venv
```

2. Activate the virtual environment:
   - On Windows:
   ```bash
   venv\Scripts\activate
   ```
   - On macOS/Linux:
   ```bash
   source venv/bin/activate
   ```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

### Option 2: Using conda

1. Create conda environment:
```bash
conda env create -f environment.yml
```

2. Activate the environment:
```bash
conda activate health_data_analysis
```

## R Setup

1. Install required R packages:
```r
install.packages(c("ggplot2", "dplyr", "corrplot", "caret", "VIM", 
                   "psych", "randomForest", "e1071", "pROC", "xgboost",
                   "lightgbm", "GGally", "moments"))
```

2. (Optional) Setup R kernel for Jupyter:
```r
install.packages('IRkernel')
IRkernel::installspec()
```

## Running the Analysis

### Python Notebooks

1. Start Jupyter Notebook:
```bash
jupyter notebook
```

2. Navigate to `python_notebooks/` and open the desired notebook:
   - `01_statistical_analysis.ipynb`
   - `02_univariate_bivariate_multivariate.ipynb`
   - `03_comprehensive_eda.ipynb`
   - `04_ml_analysis.ipynb`

### Python Scripts

Run scripts directly from the command line:
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

### R Scripts

Run R scripts from the command line:
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

### R Notebooks

1. Open RStudio
2. Open the `.Rmd` file in `r_notebooks/`
3. Click "Knit" to generate the HTML report

## Project Structure

```
health_data/
├── data/                          # Dataset
│   └── health_data.csv
├── python_notebooks/              # Python Jupyter notebooks
├── python_scripts/                # Python scripts
├── r_notebooks/                   # R notebooks (.Rmd)
├── r_scripts/                     # R scripts
├── results/                       # Analysis results
├── figures/                       # Generated visualizations
├── docs/                          # Documentation
├── requirements.txt               # Python dependencies
├── environment.yml                # Conda environment
└── README.md                      # Project documentation
```

## Troubleshooting

### Common Issues

1. **Module not found error**: Make sure you've installed all requirements and activated the virtual environment.

2. **R package installation issues**: Try installing packages one at a time, or use `install.packages()` with `dependencies = TRUE`.

3. **Figure generation errors**: Make sure the `figures/` directory exists. Create it if necessary:
   ```bash
   mkdir figures
   ```

4. **Memory issues with large datasets**: Consider sampling the data or using a machine with more RAM.

## Next Steps

1. Review the README.md for project overview
2. Start with `01_statistical_analysis.ipynb` for basic analysis
3. Proceed through the notebooks in order
4. Review generated figures in the `figures/` directory
5. Check results in the `results/` directory

## Support

If you encounter any issues, please:
1. Check the error messages carefully
2. Verify that all dependencies are installed
3. Ensure the data file is in the correct location
4. Review the project structure

For additional help, please open an issue on the GitHub repository.

