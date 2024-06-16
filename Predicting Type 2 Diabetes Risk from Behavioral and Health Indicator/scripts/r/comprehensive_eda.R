# Comprehensive Exploratory Data Analysis
# Diabetes Binary Health Indicators - BRFSS 2021

# Load required libraries
library(ggplot2)
library(dplyr)
library(corrplot)
library(VIM)
library(gridExtra)

# Set working directory
setwd("../../")

# Load data
df <- read.csv("data/diabetes_binary_health_indicators_BRFSS2021.csv")

# Data Overview
cat("=== DATA OVERVIEW ===\n")
cat("Dataset Shape:", dim(df), "\n")
cat("Number of features:", ncol(df), "\n")
cat("Number of records:", nrow(df), "\n")

cat("\n=== DATA TYPES ===\n")
str(df)

cat("\n=== MISSING VALUES ===\n")
missing <- colSums(is.na(df))
print(missing[missing > 0])

cat("\n=== DUPLICATE ROWS ===\n")
cat("Number of duplicate rows:", sum(duplicated(df)), "\n")

# Descriptive Statistics
cat("\n=== DESCRIPTIVE STATISTICS ===\n")
numerical_cols <- sapply(df, is.numeric)
desc_stats <- summary(df[, numerical_cols])
print(desc_stats)

# Target Variable Analysis
cat("\n=== TARGET VARIABLE ANALYSIS ===\n")
target_dist <- table(df$Diabetes_binary)
target_prop <- prop.table(target_dist)
print(target_dist)
print(target_prop)

# Visualization
png("results/figures/target_distribution_eda_r.png", width = 1200, height = 600, res = 300)
par(mfrow = c(1, 2))
barplot(target_dist, main = "Diabetes Distribution (Count)", 
        xlab = "Diabetes (0=No, 1=Yes)", ylab = "Frequency", 
        col = c("skyblue", "salmon"))
barplot(target_prop, main = "Diabetes Distribution (Proportion)", 
        xlab = "Diabetes (0=No, 1=Yes)", ylab = "Proportion", 
        col = c("skyblue", "salmon"))
dev.off()

# Feature Distributions
cat("\n=== FEATURE DISTRIBUTIONS ===\n")
key_vars <- c("BMI", "Age", "GenHlth", "MentHlth", "PhysHlth")

png("results/figures/feature_distributions_r.png", width = 1800, height = 1000, res = 300)
par(mfrow = c(2, 3))
for (var in key_vars) {
  if (var %in% colnames(df)) {
    hist(df[[var]], main = paste("Distribution of", var), 
         xlab = var, ylab = "Frequency",
         col = "steelblue", border = "black", breaks = 30)
    abline(v = mean(df[[var]], na.rm = TRUE), col = "red", lty = 2, lwd = 2)
    abline(v = median(df[[var]], na.rm = TRUE), col = "green", lty = 2, lwd = 2)
  }
}
dev.off()

# Correlation Analysis
cat("\n=== CORRELATION ANALYSIS ===\n")
numerical_df <- df[, numerical_cols]
correlation_matrix <- cor(numerical_df, use = "complete.obs")
diabetes_corr <- correlation_matrix[, "Diabetes_binary"]
diabetes_corr <- sort(diabetes_corr, decreasing = TRUE)
print(diabetes_corr)

# Correlation heatmap
png("results/figures/correlation_matrix_eda_r.png", width = 1400, height = 1000, res = 300)
corrplot(correlation_matrix, method = "color", type = "upper", 
         order = "hclust", tl.cex = 0.8, tl.col = "black")
dev.off()

# Categorical Variable Analysis
cat("\n=== CATEGORICAL VARIABLE ANALYSIS ===\n")
categorical_vars <- c("HighBP", "HighChol", "Smoker", "PhysActivity", "Sex", "HeartDiseaseorAttack")

png("results/figures/categorical_analysis_r.png", width = 1800, height = 1000, res = 300)
par(mfrow = c(2, 3))
for (var in categorical_vars) {
  if (var %in% colnames(df)) {
    crosstab <- prop.table(table(df[[var]], df$Diabetes_binary), margin = 1) * 100
    barplot(crosstab, main = paste("Diabetes Prevalence by", var),
            xlab = var, ylab = "Percentage (%)",
            col = c("skyblue", "salmon"),
            legend = rownames(crosstab))
  }
}
dev.off()

# Outlier Analysis
cat("\n=== OUTLIER ANALYSIS ===\n")
outlier_summary <- data.frame(
  Variable = character(),
  Lower_Bound = numeric(),
  Upper_Bound = numeric(),
  Number_of_Outliers = numeric(),
  Percentage = numeric(),
  stringsAsFactors = FALSE
)

for (var in key_vars) {
  if (var %in% colnames(df)) {
    Q1 <- quantile(df[[var]], 0.25, na.rm = TRUE)
    Q3 <- quantile(df[[var]], 0.75, na.rm = TRUE)
    IQR <- Q3 - Q1
    lower_bound <- Q1 - 1.5 * IQR
    upper_bound <- Q3 + 1.5 * IQR
    
    outliers <- sum(df[[var]] < lower_bound | df[[var]] > upper_bound, na.rm = TRUE)
    outlier_summary <- rbind(outlier_summary, data.frame(
      Variable = var,
      Lower_Bound = lower_bound,
      Upper_Bound = upper_bound,
      Number_of_Outliers = outliers,
      Percentage = (outliers / nrow(df)) * 100
    ))
  }
}
print(outlier_summary)

cat("\n=== COMPREHENSIVE EDA COMPLETE ===\n")

