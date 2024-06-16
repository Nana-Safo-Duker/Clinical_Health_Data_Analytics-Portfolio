# Descriptive, Inferential, and Exploratory Statistical Analysis
# Diabetes Binary Health Indicators - BRFSS 2021

# Load required libraries
library(ggplot2)
library(dplyr)
library(corrplot)
library(caret)
library(VIM)

# Set working directory (adjust path as needed)
setwd("../../")

# Load data
df <- read.csv("data/diabetes_binary_health_indicators_BRFSS2021.csv")

# Basic information
cat("Dataset shape:", dim(df), "\n")
cat("Columns:", colnames(df), "\n")

# Data overview
cat("\n=== DATASET INFORMATION ===\n")
str(df)
summary(df)

# Missing values
cat("\n=== MISSING VALUES ===\n")
missing_values <- colSums(is.na(df))
print(missing_values[missing_values > 0])

# Duplicate rows
cat("\n=== DUPLICATE ROWS ===\n")
cat("Number of duplicate rows:", sum(duplicated(df)), "\n")

# Descriptive statistics
cat("\n=== DESCRIPTIVE STATISTICS ===\n")
numerical_cols <- sapply(df, is.numeric)
desc_stats <- summary(df[, numerical_cols])
print(desc_stats)

# Additional statistics
cat("\n=== ADDITIONAL STATISTICS ===\n")
additional_stats <- data.frame(
  Variable = names(df)[numerical_cols],
  Mean = sapply(df[, numerical_cols], mean, na.rm = TRUE),
  Median = sapply(df[, numerical_cols], median, na.rm = TRUE),
  SD = sapply(df[, numerical_cols], sd, na.rm = TRUE),
  Min = sapply(df[, numerical_cols], min, na.rm = TRUE),
  Max = sapply(df[, numerical_cols], max, na.rm = TRUE),
  Skewness = sapply(df[, numerical_cols], function(x) {
    if(length(x) > 0) {
      moments::skewness(x, na.rm = TRUE)
    } else NA
  })
)
print(additional_stats)

# Target variable distribution
cat("\n=== TARGET VARIABLE DISTRIBUTION ===\n")
target_dist <- table(df$Diabetes_binary)
print(target_dist)
print(prop.table(target_dist))

# Visualization
png("results/figures/target_distribution_r.png", width = 1200, height = 600, res = 300)
par(mfrow = c(1, 2))
barplot(target_dist, main = "Diabetes Distribution (Count)", 
        xlab = "Diabetes (0=No, 1=Yes)", ylab = "Frequency", 
        col = c("skyblue", "salmon"))
barplot(prop.table(target_dist), main = "Diabetes Distribution (Proportion)", 
        xlab = "Diabetes (0=No, 1=Yes)", ylab = "Proportion", 
        col = c("skyblue", "salmon"))
dev.off()

# Chi-square tests for categorical variables
cat("\n=== CHI-SQUARE TESTS ===\n")
categorical_cols <- c("HighBP", "HighChol", "CholCheck", "Smoker", "Stroke", 
                      "HeartDiseaseorAttack", "PhysActivity", "Fruits", "Veggies",
                      "HvyAlcoholConsump", "AnyHealthcare", "NoDocbcCost", "DiffWalk", "Sex")

chi2_results <- data.frame(
  Variable = character(),
  Chi_square = numeric(),
  p_value = numeric(),
  Significant = character(),
  stringsAsFactors = FALSE
)

for (col in categorical_cols) {
  if (col %in% colnames(df)) {
    contingency_table <- table(df[[col]], df$Diabetes_binary)
    chi2_test <- chisq.test(contingency_table)
    chi2_results <- rbind(chi2_results, data.frame(
      Variable = col,
      Chi_square = chi2_test$statistic,
      p_value = chi2_test$p.value,
      Significant = ifelse(chi2_test$p.value < 0.05, "Yes", "No")
    ))
  }
}
print(chi2_results)

# T-tests for numerical variables
cat("\n=== T-TESTS ===\n")
numerical_vars <- c("BMI", "GenHlth", "MentHlth", "PhysHlth", "Age", "Education", "Income")

t_test_results <- data.frame(
  Variable = character(),
  t_statistic = numeric(),
  p_value = numeric(),
  Significant = character(),
  stringsAsFactors = FALSE
)

for (var in numerical_vars) {
  if (var %in% colnames(df)) {
    no_diabetes <- df[df$Diabetes_binary == 0, var]
    yes_diabetes <- df[df$Diabetes_binary == 1, var]
    t_test <- t.test(no_diabetes, yes_diabetes)
    t_test_results <- rbind(t_test_results, data.frame(
      Variable = var,
      t_statistic = t_test$statistic,
      p_value = t_test$p.value,
      Significant = ifelse(t_test$p.value < 0.05, "Yes", "No")
    ))
  }
}
print(t_test_results)

# Correlation analysis
cat("\n=== CORRELATION ANALYSIS ===\n")
numerical_df <- df[, numerical_cols]
correlation_matrix <- cor(numerical_df, use = "complete.obs")
diabetes_corr <- correlation_matrix[, "Diabetes_binary"]
diabetes_corr <- sort(diabetes_corr, decreasing = TRUE)
print(diabetes_corr)

# Correlation heatmap
png("results/figures/correlation_matrix_r.png", width = 1400, height = 1000, res = 300)
corrplot(correlation_matrix, method = "color", type = "upper", 
         order = "hclust", tl.cex = 0.8, tl.col = "black")
dev.off()

cat("\n=== ANALYSIS COMPLETE ===\n")

