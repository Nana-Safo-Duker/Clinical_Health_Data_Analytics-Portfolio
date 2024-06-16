# Multivariate Analysis
#
# This script performs multivariate analysis on the Cardiovascular Disease Dataset.

# Load necessary libraries
library(tidyverse)
library(ggplot2)
library(dplyr)
library(factoextra)
library(FactoMineR)
library(corrplot)

# Set theme for plots
theme_set(theme_minimal() + theme(plot.title = element_text(size = 14, face = "bold")))

# Load the dataset
df <- read.csv("../../data/Cardiovascular_Disease_Dataset.csv", stringsAsFactors = FALSE)

# PCA Analysis
cat(paste(rep("=", 80), collapse = ""), "\n")
cat("PRINCIPAL COMPONENT ANALYSIS (PCA)\n")
cat(paste(rep("=", 80), collapse = ""), "\n")

numerical_cols <- c("age", "restingBP", "serumcholestrol", "maxheartrate", "oldpeak")
X <- df[numerical_cols]
X <- X[complete.cases(X), ]
X_scaled <- scale(X)

# Perform PCA
pca_result <- prcomp(X_scaled, center = FALSE, scale. = FALSE)

# Explained variance
explained_variance <- summary(pca_result)$importance[2, ]
cumulative_variance <- summary(pca_result)$importance[3, ]

cat("\nExplained Variance by Component:\n")
for (i in 1:length(explained_variance)) {
  cat("  PC", i, ":", explained_variance[i], "(", explained_variance[i]*100, "%) - Cumulative:", 
      cumulative_variance[i], "(", cumulative_variance[i]*100, "%)\n")
}

# Plot PCA
X_pca <- as.data.frame(pca_result$x[, 1:2])
X_pca$target <- df[complete.cases(df[numerical_cols]), "target"]

p <- ggplot(X_pca, aes(x = PC1, y = PC2, color = factor(target))) +
  geom_point(alpha = 0.6) +
  scale_color_manual(values = c("skyblue", "coral"), labels = c("No Disease", "Disease")) +
  labs(title = "PCA: First Two Principal Components",
       x = paste0("PC1 (", round(explained_variance[1]*100, 2), "% variance)"),
       y = paste0("PC2 (", round(explained_variance[2]*100, 2), "% variance)"),
       color = "Target") +
  theme_minimal()

ggsave("../../results/pca_analysis.png", plot = p, width = 10, height = 8)

cat("\nFirst two principal components explain", cumulative_variance[2]*100, "% of variance\n")

# Feature Importance
cat("\n\n", paste(rep("=", 80), collapse = ""), "\n")
cat("FEATURE IMPORTANCE\n")
cat(paste(rep("=", 80), collapse = ""), "\n")

feature_importance <- data.frame(
  Feature = character(),
  Importance = numeric(),
  stringsAsFactors = FALSE
)

for (col in numerical_cols) {
  if (col %in% names(df)) {
    correlation <- cor(df[[col]], df$target, use = "complete.obs")
    feature_importance <- rbind(feature_importance, 
                               data.frame(Feature = col, Importance = abs(correlation)))
  }
}

# Sort by importance
feature_importance <- feature_importance[order(-feature_importance$Importance), ]

cat("\nFeature Importance (absolute correlation with target):\n")
print(feature_importance)

# Visualize feature importance
p <- ggplot(feature_importance, aes(x = reorder(Feature, Importance), y = Importance)) +
  geom_bar(stat = "identity", fill = "steelblue", alpha = 0.7) +
  coord_flip() +
  labs(title = "Feature Importance Based on Correlation with Target",
       x = "Feature",
       y = "Absolute Correlation with Target") +
  theme_minimal()

ggsave("../../results/feature_importance.png", plot = p, width = 10, height = 6)

# Multivariate Correlation
numerical_cols_with_target <- c(numerical_cols, "target")
correlation_matrix <- cor(df[numerical_cols_with_target], use = "complete.obs")

png("../../results/multivariate_correlation.png", width = 1000, height = 800)
corrplot(correlation_matrix, method = "color", type = "upper", 
         order = "hclust", tl.cex = 0.8, tl.col = "black",
         addCoef.col = "black", number.cex = 0.7)
dev.off()

cat("\nMultivariate analysis complete!\n")

