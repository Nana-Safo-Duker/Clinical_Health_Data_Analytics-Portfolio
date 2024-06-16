# Statistical Analysis: Descriptive, Inferential, and Exploratory
#
# This script performs comprehensive statistical analysis of the Cardiovascular Disease Dataset,
# including descriptive statistics, inferential statistics, and exploratory data analysis.

# Load necessary libraries
library(tidyverse)
library(ggplot2)
library(dplyr)
library(corrplot)
if (!require(psych)) install.packages("psych")
if (!require(Hmisc)) install.packages("Hmisc")
library(psych)
library(Hmisc)

# Set theme for plots
theme_set(theme_minimal() + theme(plot.title = element_text(size = 14, face = "bold")))

# Load the dataset
df <- read.csv("../../data/Cardiovascular_Disease_Dataset.csv", stringsAsFactors = FALSE)

cat("Dataset loaded successfully!\n")
cat("Shape:", nrow(df), "rows,", ncol(df), "columns\n")

# Descriptive Statistics
cat(paste(rep("=", 80), collapse = ""), "\n")
cat("DESCRIPTIVE STATISTICS\n")
cat(paste(rep("=", 80), collapse = ""), "\n")

numerical_cols <- c("age", "restingBP", "serumcholestrol", "maxheartrate", "oldpeak")
categorical_cols <- c("gender", "chestpain", "fastingbloodsugar", "restingrelectro", 
                     "exerciseangia", "slope", "noofmajorvessels", "target")

cat("\nNumerical Variables Summary:\n")
print(summary(df[numerical_cols]))

cat("\n\nCategorical Variables Summary:\n")
for (col in categorical_cols) {
  if (col %in% names(df)) {
    cat("\n", toupper(col), ":\n")
    print(table(df[[col]]))
    cat("Percentage:\n")
    print(prop.table(table(df[[col]])) * 100)
  }
}

# Inferential Statistics
cat("\n\n", paste(rep("=", 80), collapse = ""), "\n")
cat("INFERENTIAL STATISTICS\n")
cat(paste(rep("=", 80), collapse = ""), "\n")

disease_0 <- df[df$target == 0, ]
disease_1 <- df[df$target == 1, ]

cat("\nT-Test: Comparing means between disease and no-disease groups\n")
for (col in numerical_cols) {
  if (col %in% names(df)) {
    group_0 <- disease_0[[col]]
    group_1 <- disease_1[[col]]
    
    if (length(group_0) > 0 && length(group_1) > 0) {
      test_result <- t.test(group_0, group_1)
      
      cat("\n", toupper(col), ":\n")
      cat("  t-statistic:", test_result$statistic, "\n")
      cat("  p-value:", test_result$p.value, "\n")
      cat("  Significant:", ifelse(test_result$p.value < 0.05, "Yes", "No"), "\n")
    }
  }
}

# Exploratory Analysis
cat("\n\n", paste(rep("=", 80), collapse = ""), "\n")
cat("EXPLORATORY DATA ANALYSIS\n")
cat(paste(rep("=", 80), collapse = ""), "\n")

# Correlation matrix
numerical_cols_with_target <- c(numerical_cols, "target")
correlation_matrix <- cor(df[numerical_cols_with_target], use = "complete.obs")

cat("\nCorrelation with Target:\n")
target_corr <- correlation_matrix[, "target"]
target_corr <- target_corr[names(target_corr) != "target"]
print(sort(target_corr, decreasing = TRUE))

# Save correlation plot
png("../../results/correlation_matrix.png", width = 800, height = 600)
corrplot(correlation_matrix, method = "color", type = "upper", 
         order = "hclust", tl.cex = 0.8, tl.col = "black",
         addCoef.col = "black", number.cex = 0.7)
dev.off()

cat("\nAnalysis complete!\n")

