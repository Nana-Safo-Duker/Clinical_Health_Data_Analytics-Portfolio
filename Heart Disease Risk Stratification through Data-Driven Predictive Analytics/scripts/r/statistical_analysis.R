# Heart Disease Dataset - Statistical Analysis (R)
# Descriptive, Inferential, and Exploratory Statistical Analysis

# Load necessary libraries
library(tidyverse)
library(ggplot2)
library(corrplot)
library(Hmisc)
library(psych)
library(gridExtra)

# Load the dataset
df <- read.csv("../../data/heart-disease.csv")
cat("Dataset loaded successfully!\n")
cat("Shape:", nrow(df), "rows,", ncol(df), "columns\n")

# Define variable types
numerical_cols <- c("age", "rest_bp", "chol", "max_hr", "st_depr")
categorical_cols <- c("sex", "chest_pain", "heart_disease")

# ============================================================================
# 1. DESCRIPTIVE STATISTICS
# ============================================================================

cat("\n=== DATASET INFORMATION ===\n")
cat("Total records:", nrow(df), "\n")
cat("Total features:", ncol(df), "\n")
cat("Missing values:\n")
print(colSums(is.na(df)))
cat("Duplicate rows:", sum(duplicated(df)), "\n")

cat("\n=== DESCRIPTIVE STATISTICS - NUMERICAL VARIABLES ===\n")
print(summary(df[numerical_cols]))
cat("\nAdditional Statistics:\n")
print(describe(df[numerical_cols]))

cat("\n=== DESCRIPTIVE STATISTICS - CATEGORICAL VARIABLES ===\n")
for(col in categorical_cols) {
  cat("\n", toupper(col), ":\n")
  print(table(df[[col]]))
  cat("Proportions:\n")
  print(prop.table(table(df[[col]])) * 100)
}

# ============================================================================
# 2. INFERENTIAL STATISTICS
# ============================================================================

cat("\n=== HYPOTHESIS TESTING: T-TESTS ===\n")
heart_disease <- df[df$heart_disease == 1, ]
no_heart_disease <- df[df$heart_disease == 0, ]

for(col in numerical_cols) {
  test_result <- t.test(heart_disease[[col]], no_heart_disease[[col]])
  cat("\n", toupper(col), ":\n")
  cat("  Mean (Heart Disease):", mean(heart_disease[[col]]), "\n")
  cat("  Mean (No Heart Disease):", mean(no_heart_disease[[col]]), "\n")
  cat("  P-value:", test_result$p.value, "\n")
  if(test_result$p.value < 0.05) {
    cat("  Result: Significant difference (p < 0.05)\n")
  }
}

cat("\n=== CHI-SQUARE TESTS ===\n")
# Sex vs Heart Disease
contingency1 <- table(df$sex, df$heart_disease)
chi2_test1 <- chisq.test(contingency1)
cat("\nSex vs Heart Disease:\n")
print(contingency1)
cat("P-value:", chi2_test1$p.value, "\n")

# Chest Pain vs Heart Disease
contingency2 <- table(df$chest_pain, df$heart_disease)
chi2_test2 <- chisq.test(contingency2)
cat("\nChest Pain vs Heart Disease:\n")
print(contingency2)
cat("P-value:", chi2_test2$p.value, "\n")

# Correlation analysis
cat("\n=== CORRELATION ANALYSIS ===\n")
correlation_matrix <- cor(df[c(numerical_cols, "heart_disease")])
print(correlation_matrix)

# ============================================================================
# 3. EXPLORATORY STATISTICAL ANALYSIS - VISUALIZATIONS
# ============================================================================

# Create output directory
if(!dir.exists("../../results/figures")) {
  dir.create("../../results/figures", recursive = TRUE)
}

# Distribution plots
png("../../results/figures/r_univariate_distributions.png", width = 1800, height = 1000, res = 300)
plots <- list()
for(i in 1:length(numerical_cols)) {
  col <- numerical_cols[i]
  p <- ggplot(df, aes_string(x = col)) +
    geom_histogram(bins = 30, fill = "steelblue", alpha = 0.7, color = "black") +
    geom_vline(aes_string(xintercept = mean(df[[col]])), color = "red", linetype = "dashed", size = 1) +
    geom_vline(aes_string(xintercept = median(df[[col]])), color = "green", linetype = "dashed", size = 1) +
    labs(title = paste("Distribution of", col)) +
    theme_minimal()
  plots[[i]] <- p
}
grid.arrange(grobs = plots, ncol = 3)
dev.off()

# Box plots
png("../../results/figures/r_boxplots.png", width = 1800, height = 1000, res = 300)
plots <- list()
for(i in 1:length(numerical_cols)) {
  col <- numerical_cols[i]
  p <- ggplot(df, aes_string(x = "factor(heart_disease)", y = col, fill = "factor(heart_disease)")) +
    geom_boxplot(alpha = 0.7) +
    scale_fill_manual(values = c("0" = "#FF6B6B", "1" = "#4ECDC4")) +
    labs(title = paste(col, "by Heart Disease Status"), x = "Heart Disease") +
    theme_minimal() +
    theme(legend.position = "none")
  plots[[i]] <- p
}
grid.arrange(grobs = plots, ncol = 3)
dev.off()

# Correlation heatmap
png("../../results/figures/r_correlation_heatmap.png", width = 1000, height = 800, res = 300)
corrplot(correlation_matrix, method = "color", type = "upper", 
         order = "hclust", tl.cex = 0.8, tl.col = "black", 
         addCoef.col = "black", number.cex = 0.7)
dev.off()

cat("\n=== Analysis Complete! ===\n")
cat("Figures saved to ../../results/figures/\n")

