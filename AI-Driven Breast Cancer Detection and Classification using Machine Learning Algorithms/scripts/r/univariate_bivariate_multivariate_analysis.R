# Univariate, Bivariate, and Multivariate Analysis
# Breast Cancer Diagnosis Dataset

# Load required libraries
library(dplyr)
library(ggplot2)
library(corrplot)
library(psych)
library(FactoMineR)
library(factoextra)

# Load data
df <- read.csv("../../data/breast_cancer.csv", stringsAsFactors = FALSE)

# Get numerical columns
numerical_cols <- setdiff(names(df), c("id", "diagnosis"))

# Create results directories
dir.create("../../results/univariate", showWarnings = FALSE, recursive = TRUE)
dir.create("../../results/bivariate", showWarnings = FALSE, recursive = TRUE)
dir.create("../../results/multivariate", showWarnings = FALSE, recursive = TRUE)

# ==============================================================================
# UNIVARIATE ANALYSIS
# ==============================================================================
cat("=== UNIVARIATE ANALYSIS ===\n")

key_features <- c("radius_mean", "texture_mean", "perimeter_mean", 
                 "area_mean", "smoothness_mean", "compactness_mean")

# Distribution analysis
png("../../results/univariate/distributions.png", width = 1800, height = 1200)
par(mfrow = c(2, 3))
for (feature in key_features) {
  hist(df[[feature]], breaks = 30, main = paste("Distribution of", feature),
      xlab = feature, ylab = "Frequency", col = "steelblue", border = "black")
  abline(v = mean(df[[feature]]), col = "red", lty = 2, lwd = 2)
  abline(v = median(df[[feature]]), col = "green", lty = 2, lwd = 2)
  legend("topright", legend = c(paste("Mean:", round(mean(df[[feature]]), 2)),
                               paste("Median:", round(median(df[[feature]]), 2))),
        col = c("red", "green"), lty = 2, lwd = 2)
}
dev.off()

# Box plots
png("../../results/univariate/boxplots.png", width = 1800, height = 1200)
par(mfrow = c(2, 3))
for (feature in key_features) {
  boxplot(df[[feature]], main = paste("Box Plot of", feature),
         ylab = feature, col = "lightblue")
}
dev.off()

# Statistical summary
cat("\nUnivariate Statistics:\n")
univariate_stats <- describe(df[key_features])
print(univariate_stats)

# Normality tests
cat("\n=== NORMALITY TESTS ===\n")
for (feature in key_features) {
  test_result <- shapiro.test(df[[feature]])
  is_normal <- test_result$p.value > 0.05
  cat(feature, ": Shapiro-Wilk statistic =", test_result$statistic, 
     ", p-value =", test_result$p.value, ", Normal =", is_normal, "\n")
}

# ==============================================================================
# BIVARIATE ANALYSIS
# ==============================================================================
cat("\n=== BIVARIATE ANALYSIS ===\n")

# Scatter plots for highly correlated pairs
highly_corr_pairs <- list(
  c("radius_mean", "perimeter_mean"),
  c("radius_mean", "area_mean"),
  c("perimeter_mean", "area_mean"),
  c("radius_mean", "radius_worst"),
  c("texture_mean", "texture_worst"),
  c("smoothness_mean", "smoothness_worst")
)

png("../../results/bivariate/scatter_plots.png", width = 1800, height = 1200)
par(mfrow = c(2, 3))
for (pair in highly_corr_pairs) {
  feat1 <- pair[1]
  feat2 <- pair[2]
  
  # Color by diagnosis
  plot(df[[feat1]], df[[feat2]], 
      col = ifelse(df$diagnosis == "M", "red", "blue"),
      pch = 19, alpha = 0.6,
      xlab = feat1, ylab = feat2,
      main = paste(feat1, "vs", feat2))
  
  # Calculate correlation
  corr_coef <- cor(df[[feat1]], df[[feat2]])
  p_value <- cor.test(df[[feat1]], df[[feat2]])$p.value
  
  legend("topright", 
        legend = c(paste("r =", round(corr_coef, 3)),
                  paste("p =", format(p_value, scientific = TRUE, digits = 3)),
                  "Malignant", "Benign"),
        col = c("black", "black", "red", "blue"),
        pch = c(NA, NA, 19, 19))
  
  grid()
}
dev.off()

# Correlation heatmap for key features
png("../../results/bivariate/correlation_heatmap.png", width = 1200, height = 1000)
key_corr <- cor(df[key_features])
corrplot(key_corr, method = "color", type = "upper", order = "hclust",
        tl.cex = 0.8, tl.col = "black", addCoef.col = "black")
dev.off()

# Feature vs Diagnosis analysis
png("../../results/bivariate/features_by_diagnosis.png", width = 1800, height = 1200)
par(mfrow = c(2, 3))
for (feature in key_features) {
  boxplot(df[[feature]] ~ df$diagnosis, 
         main = paste(feature, "by Diagnosis"),
         xlab = "Diagnosis", ylab = feature,
         col = c("#3498db", "#e74c3c"))
  
  # Statistical test
  malignant <- df[df$diagnosis == "M",][[feature]]
  benign <- df[df$diagnosis == "B",][[feature]]
  test_result <- t.test(malignant, benign)
  
  text(1.5, max(df[[feature]]), 
      paste("p-value:", format(test_result$p.value, scientific = TRUE, digits = 3)),
      cex = 0.8)
}
dev.off()

cat("\nBivariate analysis visualizations saved to results/bivariate/\n")

# ==============================================================================
# MULTIVARIATE ANALYSIS
# ==============================================================================
cat("\n=== MULTIVARIATE ANALYSIS ===\n")

# Prepare data for PCA
X <- df[numerical_cols]
X_scaled <- scale(X)

# Principal Component Analysis
pca_result <- prcomp(X_scaled, center = TRUE, scale. = TRUE)

# Explained variance
explained_variance <- pca_result$sdev^2 / sum(pca_result$sdev^2)
cumulative_variance <- cumsum(explained_variance)

# Scree plot
png("../../results/multivariate/pca_analysis.png", width = 1600, height = 600)
par(mfrow = c(1, 2))
barplot(explained_variance[1:20], 
       main = "Scree Plot: Explained Variance by Component",
       xlab = "Principal Component", ylab = "Explained Variance Ratio",
       col = "steelblue")
plot(cumulative_variance[1:20], type = "o", 
    main = "Cumulative Explained Variance",
    xlab = "Number of Components", ylab = "Cumulative Explained Variance",
    col = "steelblue", lwd = 2)
abline(h = 0.95, col = "red", lty = 2, lwd = 2)
legend("bottomright", legend = "95% Variance", col = "red", lty = 2, lwd = 2)
dev.off()

# Number of components for 95% variance
n_components_95 <- which(cumulative_variance >= 0.95)[1]
cat("Number of components explaining 95% variance:", n_components_95, "\n")
cat("First 5 components explain", round(cumulative_variance[5] * 100, 2), "% of variance\n")

# PCA biplot (first 2 components)
X_pca <- pca_result$x[, 1:2]

png("../../results/multivariate/pca_biplot.png", width = 1200, height = 1000)
plot(X_pca, col = ifelse(df$diagnosis == "M", "red", "blue"),
    pch = 19, alpha = 0.6,
    xlab = paste("First Principal Component (", 
                round(explained_variance[1] * 100, 2), "% variance)"),
    ylab = paste("Second Principal Component (", 
                round(explained_variance[2] * 100, 2), "% variance)"),
    main = "PCA: First Two Principal Components")
legend("topright", legend = c("Malignant", "Benign"),
      col = c("red", "blue"), pch = 19)
grid()
dev.off()

# Feature importance from PCA
feature_importance <- data.frame(
  Feature = numerical_cols,
  PC1 = pca_result$rotation[, 1],
  PC2 = pca_result$rotation[, 2]
)
feature_importance$PC1_abs <- abs(feature_importance$PC1)
feature_importance$PC2_abs <- abs(feature_importance$PC2)

# Top features for PC1
top_pc1 <- feature_importance[order(feature_importance$PC1_abs, decreasing = TRUE), ][1:10, ]
cat("\nTop 10 features for PC1:\n")
print(top_pc1[, c("Feature", "PC1")])

# Correlation matrix visualization
key_features_extended <- c(key_features, "concavity_mean", "symmetry_mean", 
                          "fractal_dimension_mean")

png("../../results/multivariate/correlation_matrix.png", width = 1400, height = 1200)
corr_matrix <- cor(df[key_features_extended])
corrplot(corr_matrix, method = "color", type = "upper", order = "hclust",
        tl.cex = 0.8, tl.col = "black", addCoef.col = "black")
dev.off()

# Pair plot for key features (sample if too many points)
sample_size <- min(200, nrow(df))
sample_df <- df[sample(1:nrow(df), sample_size), ]

png("../../results/multivariate/pair_plot.png", width = 2000, height = 2000)
pairs(sample_df[key_features], 
     col = ifelse(sample_df$diagnosis == "M", "red", "blue"),
     pch = 19, cex = 0.5,
     main = "Multivariate Analysis: Pair Plot of Key Features")
dev.off()

cat("\nMultivariate analysis visualizations saved to results/multivariate/\n")

cat("\n=== ANALYSIS COMPLETE ===\n")
cat("All visualizations and results saved to results/ directory\n")

