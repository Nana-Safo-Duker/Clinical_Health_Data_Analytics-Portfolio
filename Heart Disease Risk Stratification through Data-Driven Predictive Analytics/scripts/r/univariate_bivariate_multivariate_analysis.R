# Heart Disease Dataset - Univariate, Bivariate, and Multivariate Analysis (R)

# Load necessary libraries
library(tidyverse)
library(ggplot2)
library(corrplot)
library(gridExtra)
library(Hmisc)

# Load the dataset
df <- read.csv("../../data/heart-disease.csv")
cat("Dataset loaded successfully!\n")

# Define variable types
numerical_cols <- c("age", "rest_bp", "chol", "max_hr", "st_depr")
categorical_cols <- c("sex", "chest_pain", "heart_disease")

# Create output directory
if(!dir.exists("../../results/figures")) {
  dir.create("../../results/figures", recursive = TRUE)
}

# ============================================================================
# 1. UNIVARIATE ANALYSIS
# ============================================================================

cat("\n=== UNIVARIATE ANALYSIS ===\n")

# Numerical variables - distributions
png("../../results/figures/r_univariate_numerical.png", width = 1800, height = 1000, res = 300)
plots <- list()
for(i in 1:length(numerical_cols)) {
  col <- numerical_cols[i]
  p <- ggplot(df, aes_string(x = col)) +
    geom_histogram(aes(y = ..density..), bins = 30, fill = "steelblue", alpha = 0.7, color = "black") +
    geom_density(color = "red", size = 1) +
    geom_vline(aes_string(xintercept = mean(df[[col]])), color = "green", linetype = "dashed", size = 1) +
    geom_vline(aes_string(xintercept = median(df[[col]])), color = "blue", linetype = "dashed", size = 1) +
    labs(title = paste("Distribution of", col)) +
    theme_minimal()
  plots[[i]] <- p
}
grid.arrange(grobs = plots, ncol = 3)
dev.off()

# Categorical variables
png("../../results/figures/r_univariate_categorical.png", width = 1800, height = 500, res = 300)
plots <- list()
for(i in 1:length(categorical_cols)) {
  col <- categorical_cols[i]
  value_counts <- table(df[[col]])
  p <- ggplot(data.frame(x = names(value_counts), y = as.numeric(value_counts)), 
              aes(x = x, y = y)) +
    geom_bar(stat = "identity", fill = "steelblue", alpha = 0.7, color = "black") +
    labs(title = paste("Distribution of", col), x = col, y = "Frequency") +
    theme_minimal()
  plots[[i]] <- p
}
grid.arrange(grobs = plots, ncol = 3)
dev.off()

# ============================================================================
# 2. BIVARIATE ANALYSIS
# ============================================================================

cat("\n=== BIVARIATE ANALYSIS ===\n")

# Numerical vs Target
png("../../results/figures/r_bivariate_numerical.png", width = 1800, height = 1000, res = 300)
plots <- list()
for(i in 1:length(numerical_cols)) {
  col <- numerical_cols[i]
  p <- ggplot(df, aes_string(x = "factor(heart_disease)", y = col, fill = "factor(heart_disease)")) +
    geom_violin(alpha = 0.7) +
    geom_boxplot(width = 0.2, alpha = 0.5) +
    scale_fill_manual(values = c("0" = "#FF6B6B", "1" = "#4ECDC4"), 
                     labels = c("No Heart Disease", "Heart Disease")) +
    labs(title = paste(col, "vs Heart Disease"), x = "Heart Disease", y = col) +
    theme_minimal() +
    theme(legend.position = "none")
  plots[[i]] <- p
}
grid.arrange(grobs = plots, ncol = 3)
dev.off()

# Categorical vs Target
png("../../results/figures/r_bivariate_categorical.png", width = 1500, height = 500, res = 300)
p1 <- ggplot(df, aes(x = sex, fill = factor(heart_disease))) +
  geom_bar(position = "fill", alpha = 0.7) +
  scale_fill_manual(values = c("0" = "#FF6B6B", "1" = "#4ECDC4"), 
                   labels = c("No Heart Disease", "Heart Disease")) +
  labs(title = "Sex vs Heart Disease", x = "Sex", y = "Percentage", fill = "Heart Disease") +
  theme_minimal()

p2 <- ggplot(df, aes(x = factor(chest_pain), fill = factor(heart_disease))) +
  geom_bar(position = "fill", alpha = 0.7) +
  scale_fill_manual(values = c("0" = "#FF6B6B", "1" = "#4ECDC4"), 
                   labels = c("No Heart Disease", "Heart Disease")) +
  labs(title = "Chest Pain vs Heart Disease", x = "Chest Pain Type", y = "Percentage", fill = "Heart Disease") +
  theme_minimal()

grid.arrange(p1, p2, ncol = 2)
dev.off()

# Correlation matrix
png("../../results/figures/r_bivariate_correlation.png", width = 1000, height = 800, res = 300)
correlation_matrix <- cor(df[numerical_cols])
corrplot(correlation_matrix, method = "color", type = "upper", 
         order = "hclust", tl.cex = 0.8, tl.col = "black", 
         addCoef.col = "black", number.cex = 0.7)
dev.off()

# ============================================================================
# 3. MULTIVARIATE ANALYSIS
# ============================================================================

cat("\n=== MULTIVARIATE ANALYSIS ===\n")

# Comprehensive correlation heatmap
png("../../results/figures/r_multivariate_heatmap.png", width = 1000, height = 800, res = 300)
correlation_matrix_full <- cor(df[c(numerical_cols, "heart_disease")])
corrplot(correlation_matrix_full, method = "color", type = "upper", 
         order = "hclust", tl.cex = 0.8, tl.col = "black", 
         addCoef.col = "black", number.cex = 0.7)
dev.off()

# Grouped statistics
cat("\nGrouped Statistics by Sex and Heart Disease:\n")
print(df %>% 
  group_by(sex, heart_disease) %>% 
  summarise_at(vars(numerical_cols), list(mean = mean, sd = sd), .groups = "drop"))

cat("\nGrouped Statistics by Chest Pain and Heart Disease:\n")
print(df %>% 
  group_by(chest_pain, heart_disease) %>% 
  summarise_at(vars(numerical_cols), list(mean = mean, sd = sd), .groups = "drop"))

cat("\n=== Analysis Complete! ===\n")
cat("Figures saved to ../../results/figures/\n")

