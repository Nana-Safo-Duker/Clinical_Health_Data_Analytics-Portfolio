# Comprehensive Exploratory Data Analysis (EDA)
# Breast Cancer Diagnosis Dataset

# Load required libraries
library(dplyr)
library(tidyr)
library(ggplot2)
library(corrplot)
library(VIM)
library(naniar)
library(psych)

# Load data
df <- read.csv("../../data/breast_cancer.csv", stringsAsFactors = FALSE)

# Create results directory
dir.create("../../results/eda", showWarnings = FALSE, recursive = TRUE)

# ==============================================================================
# 1. DATA OVERVIEW
# ==============================================================================
cat("=" , rep("=", 79), "\n", sep = "")
cat("COMPREHENSIVE EXPLORATORY DATA ANALYSIS\n")
cat("=" , rep("=", 79), "\n", sep = "")

cat("\n1. DATA OVERVIEW\n")
cat(rep("-", 80), "\n")
cat("Dataset shape:", nrow(df), "rows,", ncol(df), "columns\n")
cat("Number of rows:", nrow(df), "\n")
cat("Number of columns:", ncol(df), "\n")

# Get numerical columns
numerical_cols <- setdiff(names(df), c("id", "diagnosis"))

cat("\n2. DATA TYPES\n")
cat(rep("-", 80), "\n")
print(str(df))

cat("\n3. MISSING VALUES\n")
cat(rep("-", 80), "\n")
missing <- colSums(is.na(df))
if (sum(missing) > 0) {
  missing_df <- data.frame(
    Column = names(missing),
    Missing_Count = missing,
    Missing_Percentage = round(missing / nrow(df) * 100, 2)
  )
  missing_df <- missing_df[missing_df$Missing_Count > 0, ]
  print(missing_df)
} else {
  cat("No missing values found!\n")
}

cat("\n4. DUPLICATE ROWS\n")
cat(rep("-", 80), "\n")
duplicates <- sum(duplicated(df))
cat("Number of duplicate rows:", duplicates, "\n")

cat("\n5. BASIC STATISTICS\n")
cat(rep("-", 80), "\n")
print(summary(df[numerical_cols]))

# ==============================================================================
# 2. TARGET VARIABLE ANALYSIS
# ==============================================================================
cat("\n6. TARGET VARIABLE ANALYSIS\n")
cat(rep("-", 80), "\n")

diagnosis_counts <- table(df$diagnosis)
diagnosis_props <- prop.table(diagnosis_counts) * 100

cat("Diagnosis distribution:\n")
for (diagnosis in names(diagnosis_counts)) {
  cat(" ", diagnosis, ":", diagnosis_counts[diagnosis], 
      "(", round(diagnosis_props[diagnosis], 2), "%)\n")
}

# Visualization
png("../../results/eda/target_distribution.png", width = 1400, height = 600)
par(mfrow = c(1, 2))
barplot(diagnosis_counts, main = "Diagnosis Count Distribution", 
       col = c("#3498db", "#e74c3c"), xlab = "Diagnosis", ylab = "Count")
pie(diagnosis_counts, main = "Diagnosis Proportion", 
   col = c("#3498db", "#e74c3c"),
   labels = paste0(names(diagnosis_counts), "\n", 
                  round(diagnosis_props, 1), "%"))
dev.off()

# ==============================================================================
# 3. FEATURE ANALYSIS
# ==============================================================================
cat("\n7. FEATURE ANALYSIS\n")
cat(rep("-", 80), "\n")

# Separate features by type
mean_features <- numerical_cols[grepl("_mean", numerical_cols)]
se_features <- numerical_cols[grepl("_se", numerical_cols)]
worst_features <- numerical_cols[grepl("_worst", numerical_cols)]

cat("Mean features:", length(mean_features), "\n")
cat("Standard error features:", length(se_features), "\n")
cat("Worst features:", length(worst_features), "\n")

# Statistical summary by diagnosis
cat("\n8. STATISTICAL SUMMARY BY DIAGNOSIS\n")
cat(rep("-", 80), "\n")

key_features <- c("radius_mean", "texture_mean", "perimeter_mean", 
                 "area_mean", "smoothness_mean", "compactness_mean")

summary_by_diagnosis <- df %>%
  group_by(diagnosis) %>%
  summarise_at(vars(key_features), 
              list(mean = mean, sd = sd, median = median, 
                   min = min, max = max))
print(summary_by_diagnosis)

# Distribution plots
png("../../results/eda/feature_distributions.png", width = 1800, height = 1200)
par(mfrow = c(2, 3))
for (feature in key_features) {
  hist(df[df$diagnosis == "M",][[feature]], breaks = 30, 
      col = rgb(1, 0, 0, 0.5), main = paste("Distribution of", feature),
      xlab = feature, ylab = "Frequency")
  hist(df[df$diagnosis == "B",][[feature]], breaks = 30, 
      col = rgb(0, 0, 1, 0.5), add = TRUE)
  legend("topright", legend = c("Malignant", "Benign"), 
        fill = c(rgb(1, 0, 0, 0.5), rgb(0, 0, 1, 0.5)))
}
dev.off()

# Box plots
png("../../results/eda/boxplots_by_diagnosis.png", width = 1800, height = 1200)
par(mfrow = c(2, 3))
for (feature in key_features) {
  boxplot(df[[feature]] ~ df$diagnosis, 
         main = paste(feature, "by Diagnosis"),
         xlab = "Diagnosis", ylab = feature,
         col = c("#3498db", "#e74c3c"))
}
dev.off()

# ==============================================================================
# 4. CORRELATION ANALYSIS
# ==============================================================================
cat("\n9. CORRELATION ANALYSIS\n")
cat(rep("-", 80), "\n")

# Full correlation matrix
correlation_matrix <- cor(df[numerical_cols], use = "complete.obs")

# Visualization
png("../../results/eda/correlation_matrix_full.png", width = 2000, height = 1600)
corrplot(correlation_matrix, method = "color", type = "upper", 
         order = "hclust", tl.cex = 0.5, tl.col = "black")
dev.off()

# Highly correlated pairs
high_corr_pairs <- list()
for (i in 1:(ncol(correlation_matrix) - 1)) {
  for (j in (i + 1):ncol(correlation_matrix)) {
    corr_val <- correlation_matrix[i, j]
    if (abs(corr_val) > 0.9) {
      pair_name <- paste0(colnames(correlation_matrix)[i], " <-> ", 
                         colnames(correlation_matrix)[j])
      high_corr_pairs[[pair_name]] <- corr_val
    }
  }
}

cat("Number of highly correlated pairs (|r| > 0.9):", length(high_corr_pairs), "\n")
if (length(high_corr_pairs) > 0) {
  cat("Top 10 highly correlated pairs:\n")
  sorted_pairs <- sort(unlist(high_corr_pairs), decreasing = TRUE)
  for (i in 1:min(10, length(sorted_pairs))) {
    cat(" ", names(sorted_pairs)[i], ":", sorted_pairs[i], "\n")
  }
}

# Correlation with target
df_encoded <- df
df_encoded$diagnosis_encoded <- ifelse(df_encoded$diagnosis == "M", 1, 0)

target_corr <- cor(df_encoded[numerical_cols], df_encoded$diagnosis_encoded)
target_corr_sorted <- sort(abs(target_corr[, 1]), decreasing = TRUE)

cat("\nTop 10 features most correlated with diagnosis:\n")
print(head(target_corr_sorted, 10))

# Visualization
png("../../results/eda/target_correlation.png", width = 1200, height = 800)
barplot(head(target_corr_sorted, 15), horiz = TRUE, 
       main = "Top 15 Features Most Correlated with Diagnosis",
       xlab = "Correlation Coefficient", las = 1)
dev.off()

# ==============================================================================
# 5. OUTLIER ANALYSIS
# ==============================================================================
cat("\n10. OUTLIER ANALYSIS\n")
cat(rep("-", 80), "\n")

# IQR method
outlier_counts_iqr <- list()
for (feature in key_features) {
  Q1 <- quantile(df[[feature]], 0.25)
  Q3 <- quantile(df[[feature]], 0.75)
  IQR <- Q3 - Q1
  lower_bound <- Q1 - 1.5 * IQR
  upper_bound <- Q3 + 1.5 * IQR
  
  outliers <- sum(df[[feature]] < lower_bound | df[[feature]] > upper_bound)
  outlier_counts_iqr[[feature]] <- outliers
  
  if (outliers > 0) {
    cat(feature, ":", outliers, "outliers (", 
        round(outliers / nrow(df) * 100, 2), "%)\n")
  }
}

# Z-score method
outlier_counts_zscore <- list()
for (feature in key_features) {
  z_scores <- abs(scale(df[[feature]]))
  outliers <- sum(z_scores > 3, na.rm = TRUE)
  outlier_counts_zscore[[feature]] <- outliers
  
  if (outliers > 0) {
    cat(feature, "(Z-score):", outliers, "outliers (", 
        round(outliers / nrow(df) * 100, 2), "%)\n")
  }
}

# ==============================================================================
# 6. SUMMARY INSIGHTS
# ==============================================================================
cat("\n12. SUMMARY INSIGHTS\n")
cat(rep("-", 80), "\n")

# Dataset balance
diagnosis_counts <- table(df$diagnosis)
balance_ratio <- min(diagnosis_counts) / max(diagnosis_counts)
cat("Dataset balance ratio:", round(balance_ratio, 3), 
   ifelse(balance_ratio > 0.8, "(Balanced)", "(Imbalanced)"), "\n")

# Feature count
cat("Total features:", length(numerical_cols), "\n")

# Missing values
missing_count <- sum(is.na(df))
cat("Missing values:", missing_count, 
   ifelse(missing_count == 0, "(None)", "(Present)"), "\n")

# Correlation insights
high_corr_count <- length(high_corr_pairs)
cat("Highly correlated feature pairs (|r| > 0.9):", high_corr_count, "\n")

cat("\n", rep("=", 80), "\n", sep = "")
cat("EDA COMPLETE - All visualizations saved to results/eda/\n")
cat(rep("=", 80), "\n", sep = "")

