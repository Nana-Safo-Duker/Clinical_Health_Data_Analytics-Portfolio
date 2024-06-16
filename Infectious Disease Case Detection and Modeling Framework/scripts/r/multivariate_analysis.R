# Multivariate Analysis Module
# R script for multivariate statistical analysis

library(ggplot2)
library(dplyr)
library(corrplot)
library(factoextra)
library(FactoMineR)
library(cluster)
source("data_loader.R")

# Function for multivariate analysis
# Perform multivariate analysis
# Parameters: df_clean - cleaned dataset
multivariate_analysis <- function(df_clean) {
  cat("=== MULTIVARIATE ANALYSIS ===\n\n")
  
  # Select numeric columns
  numeric_cols <- c("Incidence_Rate", "CI_Lower", "CI_Upper", "Annual_Count", "Trend_5yr")
  numeric_cols <- numeric_cols[numeric_cols %in% colnames(df_clean)]
  data <- df_clean %>%
    select(all_of(numeric_cols)) %>%
    na.omit()
  
  # Correlation matrix
  cat("1. Correlation Matrix:\n")
  corr_matrix <- cor(data)
  print(corr_matrix)
  
  # Visualize correlation matrix
  png("correlation_matrix.png", width = 1200, height = 1000, res = 300)
  corrplot(corr_matrix, method = "color", type = "upper", 
           order = "hclust", tl.cex = 0.8, tl.col = "black")
  dev.off()
  
  # Principal Component Analysis (PCA)
  cat("\n2. Principal Component Analysis (PCA):\n")
  
  # Scale data
  data_scaled <- scale(data)
  
  # Perform PCA
  pca_result <- PCA(data_scaled, graph = FALSE)
  
  # Explained variance
  eig_values <- get_eigenvalue(pca_result)
  cat("Explained Variance:\n")
  print(eig_values)
  
  # Scree plot
  png("pca_scree_plot.png", width = 1200, height = 600, res = 300)
  fviz_eig(pca_result, addlabels = TRUE, ylim = c(0, 50))
  dev.off()
  
  # Biplot
  png("pca_biplot.png", width = 1200, height = 1000, res = 300)
  fviz_pca_biplot(pca_result, repel = TRUE, col.var = "contrib", 
                  gradient.cols = c("#00AFBB", "#E7B800", "#FC4E07"))
  dev.off()
  
  # Variable contributions
  var_contrib <- get_pca_var(pca_result)
  cat("\n3. Variable Contributions to Principal Components:\n")
  print(var_contrib$contrib)
  
  return(list(
    correlation_matrix = corr_matrix,
    pca_result = pca_result,
    explained_variance = eig_values
  ))
}

# Function for cluster analysis
# Perform cluster analysis using K-means
# Parameters: df_clean - cleaned dataset, n_clusters - number of clusters
cluster_analysis <- function(df_clean, n_clusters = 3) {
  cat("\n4. Cluster Analysis (K-means, k =", n_clusters, "):\n")
  
  # Select numeric columns
  numeric_cols <- c("Incidence_Rate", "Annual_Count", "Trend_5yr")
  numeric_cols <- numeric_cols[numeric_cols %in% colnames(df_clean)]
  data <- df_clean %>%
    select(all_of(numeric_cols)) %>%
    na.omit()
  
  # Scale data
  data_scaled <- scale(data)
  
  # K-means clustering
  set.seed(42)
  kmeans_result <- kmeans(data_scaled, centers = n_clusters, nstart = 25)
  
  # Add cluster labels
  data_with_clusters <- data
  data_with_clusters$Cluster <- as.factor(kmeans_result$cluster)
  
  # Cluster statistics
  cat("Cluster Statistics:\n")
  cluster_stats <- data_with_clusters %>%
    group_by(Cluster) %>%
    summarise_all(mean, na.rm = TRUE)
  print(cluster_stats)
  
  # Visualize clusters
  if (length(numeric_cols) >= 2) {
    png("cluster_analysis.png", width = 1000, height = 800, res = 300)
    plot(data[[numeric_cols[1]]], data[[numeric_cols[2]]], 
         col = kmeans_result$cluster, pch = 19, alpha = 0.6,
         xlab = numeric_cols[1], ylab = numeric_cols[2],
         main = paste("K-means Clustering (k =", n_clusters, ")"))
    points(kmeans_result$centers[, 1], kmeans_result$centers[, 2], 
           col = 1:n_clusters, pch = 8, cex = 2, lwd = 2)
    dev.off()
  }
  
  return(list(
    kmeans_result = kmeans_result,
    clusters = kmeans_result$cluster,
    data_with_clusters = data_with_clusters
  ))
}

# Main execution
if (!interactive()) {
  df <- load_data()
  df_clean <- clean_data(df)
  
  # Multivariate analysis
  result <- multivariate_analysis(df_clean)
  
  # Cluster analysis
  cluster_result <- cluster_analysis(df_clean, n_clusters = 3)
}

