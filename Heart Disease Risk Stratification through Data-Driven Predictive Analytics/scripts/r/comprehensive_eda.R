# Heart Disease Dataset - Comprehensive Exploratory Data Analysis (R)

# Load necessary libraries
library(tidyverse)
library(ggplot2)
library(corrplot)
library(gridExtra)
library(Hmisc)
library(psych)

# Load the dataset
df <- read.csv("../../data/heart-disease.csv")
cat("Dataset loaded successfully!\n")
cat("Shape:", nrow(df), "rows,", ncol(df), "columns\n")

# Define variable types
numerical_cols <- c("age", "rest_bp", "chol", "max_hr", "st_depr")
categorical_cols <- c("sex", "chest_pain", "heart_disease")

# Create output directory
if(!dir.exists("../../results/figures")) {
  dir.create("../../results/figures", recursive = TRUE)
}

# ============================================================================
# 1. DATA OVERVIEW
# ============================================================================

cat("\n=== DATA OVERVIEW ===\n")
cat("Dataset shape:", nrow(df), "x", ncol(df), "\n")
cat("Missing values:\n")
print(colSums(is.na(df)))
cat("Duplicate rows:", sum(duplicated(df)), "\n")
cat("\nSummary statistics:\n")
print(summary(df))

# ============================================================================
# 2. UNIVARIATE ANALYSIS
# ============================================================================

cat("\n=== UNIVARIATE ANALYSIS ===\n")

# Numerical distributions
png("../../results/figures/r_eda_univariate_numerical.png", width = 1800, height = 1000, res = 300)
plots <- list()
for(i in 1:length(numerical_cols)) {
  col <- numerical_cols[i]
  p <- ggplot(df, aes_string(x = col)) +
    geom_histogram(aes(y = ..density..), bins = 30, fill = "steelblue", alpha = 0.7, color = "black") +
    geom_density(color = "red", size = 1) +
    geom_vline(aes_string(xintercept = mean(df[[col]])), color = "green", linetype = "dashed") +
    geom_vline(aes_string(xintercept = median(df[[col]])), color = "blue", linetype = "dashed") +
    labs(title = paste("Distribution of", col)) +
    theme_minimal()
  plots[[i]] <- p
}
grid.arrange(grobs = plots, ncol = 3)
dev.off()

# ============================================================================
# 3. BIVARIATE ANALYSIS
# ============================================================================

cat("\n=== BIVARIATE ANALYSIS ===\n")

# Numerical vs Target
png("../../results/figures/r_eda_bivariate_numerical.png", width = 1800, height = 1000, res = 300)
plots <- list()
for(i in 1:length(numerical_cols)) {
  col <- numerical_cols[i]
  p <- ggplot(df, aes_string(x = "factor(heart_disease)", y = col, fill = "factor(heart_disease)")) +
    geom_boxplot(alpha = 0.7) +
    scale_fill_manual(values = c("0" = "#FF6B6B", "1" = "#4ECDC4")) +
    labs(title = paste(col, "vs Heart Disease"), x = "Heart Disease", y = col) +
    theme_minimal() +
    theme(legend.position = "none")
  plots[[i]] <- p
}
grid.arrange(grobs = plots, ncol = 3)
dev.off()

# Correlation heatmap
png("../../results/figures/r_eda_correlation_heatmap.png", width = 1000, height = 800, res = 300)
correlation_matrix <- cor(df[c(numerical_cols, "heart_disease")])
corrplot(correlation_matrix, method = "color", type = "upper", 
         order = "hclust", tl.cex = 0.8, tl.col = "black", 
         addCoef.col = "black", number.cex = 0.7)
dev.off()

# ============================================================================
# 4. MULTIVARIATE ANALYSIS
# ============================================================================

cat("\n=== MULTIVARIATE ANALYSIS ===\n")

# Pairwise relationships (sample)
png("../../results/figures/r_eda_multivariate_scatter.png", width = 1600, height = 1200, res = 300)
p1 <- ggplot(df, aes(x = age, y = chol, color = factor(heart_disease))) +
  geom_point(alpha = 0.6) +
  scale_color_manual(values = c("0" = "#FF6B6B", "1" = "#4ECDC4"), 
                    labels = c("No Heart Disease", "Heart Disease")) +
  labs(title = "Age vs Cholesterol", color = "Heart Disease") +
  theme_minimal()

p2 <- ggplot(df, aes(x = age, y = max_hr, color = factor(heart_disease))) +
  geom_point(alpha = 0.6) +
  scale_color_manual(values = c("0" = "#FF6B6B", "1" = "#4ECDC4"), 
                    labels = c("No Heart Disease", "Heart Disease")) +
  labs(title = "Age vs Max Heart Rate", color = "Heart Disease") +
  theme_minimal()

p3 <- ggplot(df, aes(x = chol, y = max_hr, color = factor(heart_disease))) +
  geom_point(alpha = 0.6) +
  scale_color_manual(values = c("0" = "#FF6B6B", "1" = "#4ECDC4"), 
                    labels = c("No Heart Disease", "Heart Disease")) +
  labs(title = "Cholesterol vs Max Heart Rate", color = "Heart Disease") +
  theme_minimal()

p4 <- ggplot(df, aes(x = rest_bp, y = st_depr, color = factor(heart_disease))) +
  geom_point(alpha = 0.6) +
  scale_color_manual(values = c("0" = "#FF6B6B", "1" = "#4ECDC4"), 
                    labels = c("No Heart Disease", "Heart Disease")) +
  labs(title = "Rest BP vs ST Depression", color = "Heart Disease") +
  theme_minimal()

grid.arrange(p1, p2, p3, p4, ncol = 2)
dev.off()

# ============================================================================
# 5. SUMMARY
# ============================================================================

cat("\n=== EDA SUMMARY ===\n")
cat("1. Data Quality: Clean dataset with no missing values\n")
cat("2. Target Distribution:\n")
print(table(df$heart_disease))
cat("\n3. Key Correlations with Heart Disease:\n")
correlations <- cor(df[numerical_cols], df$heart_disease)
print(sort(abs(correlations), decreasing = TRUE))

cat("\n=== EDA Complete! ===\n")
cat("Figures saved to ../../results/figures/\n")

