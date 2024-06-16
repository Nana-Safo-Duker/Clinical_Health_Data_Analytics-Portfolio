# Install required R packages
# Run this script to install all necessary packages

packages <- c(
  "readr",
  "dplyr",
  "tidyr",
  "ggplot2",
  "gridExtra",
  "corrplot",
  "psych",
  "e1071",
  "VIM",
  "mice",
  "factoextra",
  "FactoMineR",
  "cluster",
  "caret",
  "randomForest",
  "xgboost",
  "glmnet",
  "Metrics"
)

# Install packages if not already installed
for (pkg in packages) {
  if (!require(pkg, character.only = TRUE)) {
    install.packages(pkg, dependencies = TRUE)
    library(pkg, character.only = TRUE)
  }
}

cat("All packages installed and loaded successfully!\n")

