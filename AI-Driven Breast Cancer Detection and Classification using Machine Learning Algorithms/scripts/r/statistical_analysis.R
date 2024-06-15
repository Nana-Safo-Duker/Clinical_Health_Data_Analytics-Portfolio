# Statistical Analysis: Descriptive, Inferential, and Exploratory
# Breast Cancer Diagnosis Dataset

# Load required libraries
library(dplyr)
library(tidyr)
library(ggplot2)
library(corrplot)
library(psych)
library(car)

# Set working directory (adjust path as needed)
# setwd("path/to/project")

# Load data
df <- read.csv("../../data/breast_cancer.csv", stringsAsFactors = FALSE)

# Basic information
cat("=== DATASET INFORMATION ===\n")
cat("Dataset shape:", nrow(df), "rows,", ncol(df), "columns\n")
cat("Missing values:", sum(is.na(df)), "\n")
cat("Duplicate rows:", sum(duplicated(df)), "\n\n")

# Get numerical columns
numerical_cols <- setdiff(names(df), c("id", "diagnosis"))

# ==============================================================================
# 1. DESCRIPTIVE STATISTICS
# ==============================================================================
cat("=== DESCRIPTIVE STATISTICS ===\n")

# Basic descriptive statistics
desc_stats <- describe(df[numerical_cols])
print(desc_stats)

# Additional statistics
cat("\n=== ADDITIONAL STATISTICS ===\n")
additional_stats <- df[numerical_cols] %>%
  summarise_all(list(
    mean = ~mean(., na.rm = TRUE),
    median = ~median(., na.rm = TRUE),
    sd = ~sd(., na.rm = TRUE),
    min = ~min(., na.rm = TRUE),
    max = ~max(., na.rm = TRUE),
    skewness = ~skew(., na.rm = TRUE),
    kurtosis = ~kurtosi(., na.rm = TRUE)
  ))

# Diagnosis distribution
cat("\n=== DIAGNOSIS DISTRIBUTION ===\n")
diagnosis_counts <- table(df$diagnosis)
diagnosis_props <- prop.table(diagnosis_counts) * 100
print(diagnosis_counts)
print(diagnosis_props)

# Visualization: Diagnosis distribution
png("../../results/diagnosis_distribution.png", width = 1200, height = 600)
par(mfrow = c(1, 2))
barplot(diagnosis_counts, main = "Diagnosis Count", col = c("#3498db", "#e74c3c"))
pie(diagnosis_counts, main = "Diagnosis Proportion", col = c("#3498db", "#e74c3c"),
    labels = paste0(names(diagnosis_counts), "\n", round(diagnosis_props, 1), "%"))
dev.off()

# ==============================================================================
# 2. INFERENTIAL STATISTICS
# ==============================================================================
cat("\n=== INFERENTIAL STATISTICS ===\n")

# Separate data by diagnosis
malignant <- df[df$diagnosis == "M", ]
benign <- df[df$diagnosis == "B", ]

cat("Malignant samples:", nrow(malignant), "\n")
cat("Benign samples:", nrow(benign), "\n\n")

# Normality tests
cat("=== NORMALITY TESTS (Shapiro-Wilk Test) ===\n")
key_features <- c("radius_mean", "texture_mean", "perimeter_mean", 
                 "area_mean", "smoothness_mean")

normality_results <- list()
for (feature in key_features) {
  # Test for malignant (sample if too large)
  if (nrow(malignant) > 5000) {
    sample_m <- sample(malignant[[feature]], 5000)
  } else {
    sample_m <- malignant[[feature]]
  }
  
  # Test for benign (sample if too large)
  if (nrow(benign) > 5000) {
    sample_b <- sample(benign[[feature]], 5000)
  } else {
    sample_b <- benign[[feature]]
  }
  
  test_m <- shapiro.test(sample_m)
  test_b <- shapiro.test(sample_b)
  
  cat(feature, ":\n")
  cat("  Malignant: statistic =", test_m$statistic, ", p-value =", test_m$p.value, 
      ", normal =", test_m$p.value > 0.05, "\n")
  cat("  Benign: statistic =", test_b$statistic, ", p-value =", test_b$p.value, 
      ", normal =", test_b$p.value > 0.05, "\n\n")
  
  normality_results[[feature]] <- list(
    malignant = test_m,
    benign = test_b
  )
}

# T-tests
cat("=== INDEPENDENT T-TESTS ===\n")
ttest_results <- list()

for (feature in numerical_cols[1:10]) {
  test_result <- t.test(malignant[[feature]], benign[[feature]])
  
  mean_m <- mean(malignant[[feature]])
  mean_b <- mean(benign[[feature]])
  
  significance <- ifelse(test_result$p.value < 0.001, "***",
                        ifelse(test_result$p.value < 0.01, "**",
                              ifelse(test_result$p.value < 0.05, "*", "")))
  
  cat(feature, ": t =", test_result$statistic, ", p =", test_result$p.value, 
      significance, "\n")
  cat("  Malignant mean:", mean_m, ", Benign mean:", mean_b, "\n")
  
  ttest_results[[feature]] <- list(
    t_statistic = as.numeric(test_result$statistic),
    p_value = test_result$p.value,
    mean_malignant = mean_m,
    mean_benign = mean_b,
    significant = test_result$p.value < 0.05
  )
}

# Mann-Whitney U test (non-parametric)
cat("\n=== MANN-WHITNEY U TESTS (Non-parametric) ===\n")
for (feature in numerical_cols[1:10]) {
  test_result <- wilcox.test(malignant[[feature]], benign[[feature]])
  
  significance <- ifelse(test_result$p.value < 0.001, "***",
                        ifelse(test_result$p.value < 0.01, "**",
                              ifelse(test_result$p.value < 0.05, "*", "")))
  
  cat(feature, ": W =", test_result$statistic, ", p =", test_result$p.value, 
      significance, "\n")
}

# Effect size (Cohen's d)
cat("\n=== EFFECT SIZE (Cohen's d) ===\n")
cohens_d <- function(group1, group2) {
  n1 <- length(group1)
  n2 <- length(group2)
  var1 <- var(group1)
  var2 <- var(group2)
  pooled_sd <- sqrt(((n1 - 1) * var1 + (n2 - 1) * var2) / (n1 + n2 - 2))
  d <- (mean(group1) - mean(group2)) / pooled_sd
  return(d)
}

effect_sizes <- list()
for (feature in numerical_cols[1:10]) {
  d <- cohens_d(malignant[[feature]], benign[[feature]])
  effect_sizes[[feature]] <- d
  
  interpretation <- ifelse(abs(d) < 0.2, "negligible",
                          ifelse(abs(d) < 0.5, "small",
                                ifelse(abs(d) < 0.8, "medium", "large")))
  
  cat(feature, ": Cohen's d =", d, "(", interpretation, "effect)\n")
}

# Confidence intervals
cat("\n=== 95% CONFIDENCE INTERVALS ===\n")
for (feature in key_features) {
  ci_m <- t.test(malignant[[feature]])$conf.int
  ci_b <- t.test(benign[[feature]])$conf.int
  
  cat(feature, ":\n")
  cat("  Malignant 95% CI: [", ci_m[1], ",", ci_m[2], "]\n")
  cat("  Benign 95% CI: [", ci_b[1], ",", ci_b[2], "]\n\n")
}

# ==============================================================================
# 3. EXPLORATORY STATISTICAL ANALYSIS
# ==============================================================================
cat("=== EXPLORATORY STATISTICAL ANALYSIS ===\n")

# Correlation matrix
correlation_matrix <- cor(df[numerical_cols], use = "complete.obs")

# Visualization
png("../../results/correlation_matrix.png", width = 2000, height = 1600)
corrplot(correlation_matrix, method = "color", type = "upper", 
         order = "hclust", tl.cex = 0.6, tl.col = "black")
dev.off()

# Highly correlated features
cat("\n=== HIGHLY CORRELATED FEATURES (|r| > 0.9) ===\n")
high_corr_pairs <- list()
for (i in 1:(ncol(correlation_matrix) - 1)) {
  for (j in (i + 1):ncol(correlation_matrix)) {
    corr_val <- correlation_matrix[i, j]
    if (abs(corr_val) > 0.9) {
      pair_name <- paste0(colnames(correlation_matrix)[i], " <-> ", 
                         colnames(correlation_matrix)[j])
      cat(pair_name, ":", corr_val, "\n")
      high_corr_pairs[[pair_name]] <- corr_val
    }
  }
}

# Statistical summary by diagnosis
cat("\n=== STATISTICAL SUMMARY BY DIAGNOSIS ===\n")
summary_by_diagnosis <- df %>%
  group_by(diagnosis) %>%
  summarise_at(vars(numerical_cols[1:10]), 
              list(mean = mean, sd = sd, median = median))
print(summary_by_diagnosis)

# Box plots
png("../../results/feature_distributions_by_diagnosis.png", width = 1800, height = 1200)
par(mfrow = c(2, 3))
for (feature in key_features) {
  boxplot(df[[feature]] ~ df$diagnosis, 
         main = paste(feature, "by Diagnosis"),
         xlab = "Diagnosis", ylab = feature,
         col = c("#3498db", "#e74c3c"))
}
dev.off()

# Outlier detection
cat("\n=== OUTLIER DETECTION (IQR Method) ===\n")
outlier_counts <- list()
for (feature in numerical_cols[1:10]) {
  Q1 <- quantile(df[[feature]], 0.25)
  Q3 <- quantile(df[[feature]], 0.75)
  IQR <- Q3 - Q1
  lower_bound <- Q1 - 1.5 * IQR
  upper_bound <- Q3 + 1.5 * IQR
  
  outliers <- sum(df[[feature]] < lower_bound | df[[feature]] > upper_bound)
  outlier_counts[[feature]] <- outliers
  
  if (outliers > 0) {
    cat(feature, ":", outliers, "outliers (", 
        round(outliers / nrow(df) * 100, 2), "%)\n")
  }
}

cat("\n=== ANALYSIS COMPLETE ===\n")
cat("All results saved to results/ directory\n")

