# R Package Requirements
# List of required R packages for this project

required_packages <- c(
  "readr",        # Data reading
  "dplyr",        # Data manipulation
  "tidyr",        # Data tidying
  "ggplot2",      # Visualization
  "gridExtra",    # Plot arrangement
  "corrplot",     # Correlation plots
  "psych",        # Psychological and statistical functions
  "e1071",        # Statistical functions (skewness, kurtosis)
  "VIM",          # Visualization and imputation of missing values
  "mice",         # Multiple imputation
  "factoextra",   # Extract and visualize results of multivariate data analyses
  "FactoMineR",   # Multivariate data analysis
  "cluster",      # Cluster analysis
  "caret",        # Classification and regression training
  "randomForest", # Random forest
  "xgboost",      # XGBoost
  "glmnet",       # Lasso and elastic-net regularized generalized linear models
  "Metrics",      # Evaluation metrics
  "rlang"         # Advanced programming tools for R
)

cat("Required R packages:\n")
for (pkg in required_packages) {
  cat("  -", pkg, "\n")
}

cat("\nTo install all packages, run:\n")
cat("install.packages(c(", paste0('"', required_packages, '"', collapse = ", "), "))\n")

