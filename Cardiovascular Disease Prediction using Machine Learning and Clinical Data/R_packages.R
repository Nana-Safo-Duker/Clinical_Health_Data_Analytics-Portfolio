# R Package Installation Script
# This script installs all required R packages for the Cardiovascular Disease Analysis project

# List of required packages
required_packages <- c(
  # Core data manipulation and visualization
  "tidyverse",
  "ggplot2",
  "dplyr",
  "gridExtra",
  
  # Statistical analysis
  "psych",
  "Hmisc",
  "car",
  "vcd",
  
  # Visualization
  "corrplot",
  "VIM",
  "ggcorrplot",
  "GGally",
  
  # Machine learning
  "caret",
  "randomForest",
  "e1071",
  "rpart",
  "xgboost",
  "pROC",
  "pander",
  
  # Multivariate analysis
  "factoextra",
  "FactoMineR",
  
  # R Markdown
  "rmarkdown",
  "knitr"
)

# Function to install packages if not already installed
install_if_missing <- function(packages) {
  new_packages <- packages[!(packages %in% installed.packages()[,"Package"])]
  if(length(new_packages)) {
    install.packages(new_packages, dependencies = TRUE)
  }
  # Load all packages
  for(package in packages) {
    if(!require(package, character.only = TRUE)) {
      stop(paste("Failed to load package:", package))
    }
  }
}

# Install and load all required packages
cat("Installing and loading required R packages...\n")
install_if_missing(required_packages)
cat("All packages installed and loaded successfully!\n")

# Verify installation
cat("\nInstalled packages:\n")
print(installed.packages()[required_packages, c("Package", "Version")])

