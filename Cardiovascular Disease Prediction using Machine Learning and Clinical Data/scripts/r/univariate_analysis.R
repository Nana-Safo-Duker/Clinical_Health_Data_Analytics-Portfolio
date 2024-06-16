# Univariate Analysis
#
# This script performs univariate analysis on the Cardiovascular Disease Dataset.

# Load necessary libraries
library(tidyverse)
library(ggplot2)
library(dplyr)
library(psych)
library(gridExtra)

# Set theme for plots
theme_set(theme_minimal() + theme(plot.title = element_text(size = 14, face = "bold")))

# Load the dataset
df <- read.csv("../../data/Cardiovascular_Disease_Dataset.csv", stringsAsFactors = FALSE)

# Univariate Analysis for Numerical Variables
cat(paste(rep("=", 80), collapse = ""), "\n")
cat("UNIVARIATE ANALYSIS - NUMERICAL VARIABLES\n")
cat(paste(rep("=", 80), collapse = ""), "\n")

numerical_cols <- c("age", "restingBP", "serumcholestrol", "maxheartrate", "oldpeak")

for (col in numerical_cols) {
  if (col %in% names(df)) {
    cat("\n", toupper(col), ":\n")
    cat("  Mean:", mean(df[[col]], na.rm = TRUE), "\n")
    cat("  Median:", median(df[[col]], na.rm = TRUE), "\n")
    cat("  Std Dev:", sd(df[[col]], na.rm = TRUE), "\n")
    cat("  Min:", min(df[[col]], na.rm = TRUE), "\n")
    cat("  Max:", max(df[[col]], na.rm = TRUE), "\n")
    cat("  Skewness:", psych::skew(df[[col]], na.rm = TRUE), "\n")
    cat("  Kurtosis:", psych::kurtosi(df[[col]], na.rm = TRUE), "\n")
    
    # Outlier detection
    Q1 <- quantile(df[[col]], 0.25, na.rm = TRUE)
    Q3 <- quantile(df[[col]], 0.75, na.rm = TRUE)
    IQR_val <- Q3 - Q1
    outliers <- df[df[[col]] < Q1 - 1.5 * IQR_val | df[[col]] > Q3 + 1.5 * IQR_val, ]
    cat("  Outliers:", nrow(outliers), "(", round(nrow(outliers)/nrow(df)*100, 2), "%)\n")
  }
}

# Univariate Analysis for Categorical Variables
cat("\n\n", paste(rep("=", 80), collapse = ""), "\n")
cat("UNIVARIATE ANALYSIS - CATEGORICAL VARIABLES\n")
cat(paste(rep("=", 80), collapse = ""), "\n")

categorical_cols <- c("gender", "chestpain", "fastingbloodsugar", "restingrelectro", 
                     "exerciseangia", "slope", "noofmajorvessels", "target")

for (col in categorical_cols) {
  if (col %in% names(df)) {
    cat("\n", toupper(col), ":\n")
    value_counts <- table(df[[col]])
    print(value_counts)
    cat("Percentage:\n")
    print(prop.table(value_counts) * 100)
  }
}

# Visualize distributions
plots_list <- list()
for (col in numerical_cols) {
  if (col %in% names(df)) {
    p <- ggplot(df, aes_string(x = col)) +
      geom_histogram(bins = 30, fill = "steelblue", alpha = 0.7, color = "black") +
      labs(title = paste("Histogram:", col),
           x = col,
           y = "Frequency") +
      theme_minimal()
    plots_list[[col]] <- p
  }
}

# Save plots
png("../../results/univariate_analysis.png", width = 1200, height = 800)
do.call(grid.arrange, c(plots_list, ncol = 2))
dev.off()

cat("\nUnivariate analysis complete!\n")

