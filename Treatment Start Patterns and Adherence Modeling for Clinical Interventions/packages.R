# R Package Dependencies
# This script installs all required R packages for the analysis

# List of required packages
required_packages <- c(
  "dplyr",        # Data manipulation
  "ggplot2",      # Data visualization
  "tidyr",        # Data tidying
  "lubridate",    # Date/time manipulation
  "corrplot",     # Correlation plots
  "gridExtra",    # Grid arrangements for plots
  "moments",      # Moments, skewness, kurtosis
  "caret",        # Classification and regression training
  "randomForest", # Random forest algorithm
  "gbm",          # Gradient boosting machine
  "xgboost",      # Extreme gradient boosting
  "VIM",          # Visualization and imputation of missing values
  "car",          # Companion to applied regression
  "knitr",        # Dynamic report generation
  "rmarkdown"     # R Markdown document generation
)

# Function to install packages if not already installed
install_if_missing <- function(package) {
  if (!require(package, character.only = TRUE)) {
    install.packages(package, dependencies = TRUE)
    library(package, character.only = TRUE)
  }
}

# Install all required packages
cat("Installing required R packages...\n")
for (package in required_packages) {
  install_if_missing(package)
}

cat("All required packages have been installed!\n")
cat("Installed packages:\n")
print(required_packages)


