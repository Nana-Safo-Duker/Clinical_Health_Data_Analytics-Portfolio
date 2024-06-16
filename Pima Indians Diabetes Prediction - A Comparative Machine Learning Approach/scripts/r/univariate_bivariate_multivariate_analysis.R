# Pima Indians Diabetes Dataset - Univariate, Bivariate, and Multivariate Analysis
# R Script for Comprehensive Analysis

# Load necessary libraries
library(dplyr)
library(tidyverse)
library(ggplot2)
library(GGally)
library(corrplot)
library(gridExtra)
library(stats)

# Set output directory
output_dir <- "../../outputs/"
dir.create(output_dir, showWarnings = FALSE, recursive = TRUE)

# Function to load data
load_data <- function() {
  data <- read.csv("../../data/pima-indians-diabetes.csv", skip = 9, header = FALSE)
  colnames(data) <- c(
    "Pregnancies",
    "Glucose",
    "BloodPressure",
    "SkinThickness",
    "Insulin",
    "BMI",
    "DiabetesPedigreeFunction",
    "Age",
    "Outcome"
  )
  data$Outcome <- as.factor(data$Outcome)
  levels(data$Outcome) <- c("No Diabetes", "Diabetes")
  return(data)
}

# Univariate Analysis
univariate_analysis <- function(data, output_dir) {
  cat(paste(rep("=", 80), collapse = ""), "\n")
  cat("UNIVARIATE ANALYSIS\n")
  cat(paste(rep("=", 80), collapse = ""), "\n\n")
  
  numeric_features <- c("Pregnancies", "Glucose", "BloodPressure", "SkinThickness",
                       "Insulin", "BMI", "DiabetesPedigreeFunction", "Age")
  
  # Summary statistics
  univariate_stats <- data.frame(
    Feature = numeric_features,
    Mean = sapply(numeric_features, function(x) mean(data[[x]], na.rm = TRUE)),
    Median = sapply(numeric_features, function(x) median(data[[x]], na.rm = TRUE)),
    Std = sapply(numeric_features, function(x) sd(data[[x]], na.rm = TRUE)),
    Variance = sapply(numeric_features, function(x) var(data[[x]], na.rm = TRUE)),
    Skewness = sapply(numeric_features, function(x) {
      mean_val <- mean(data[[x]], na.rm = TRUE)
      sd_val <- sd(data[[x]], na.rm = TRUE)
      n <- sum(!is.na(data[[x]]))
      sum((data[[x]] - mean_val)^3, na.rm = TRUE) / (n * sd_val^3)
    }),
    Kurtosis = sapply(numeric_features, function(x) {
      mean_val <- mean(data[[x]], na.rm = TRUE)
      sd_val <- sd(data[[x]], na.rm = TRUE)
      n <- sum(!is.na(data[[x]]))
      sum((data[[x]] - mean_val)^4, na.rm = TRUE) / (n * sd_val^4) - 3
    }),
    Min = sapply(numeric_features, function(x) min(data[[x]], na.rm = TRUE)),
    Max = sapply(numeric_features, function(x) max(data[[x]], na.rm = TRUE)),
    Q1 = sapply(numeric_features, function(x) quantile(data[[x]], 0.25, na.rm = TRUE)),
    Q3 = sapply(numeric_features, function(x) quantile(data[[x]], 0.75, na.rm = TRUE)),
    IQR = sapply(numeric_features, function(x) IQR(data[[x]], na.rm = TRUE))
  )
  
  cat("Univariate Statistics:\n")
  print(univariate_stats, digits = 3)
  
  # Distribution plots
  plots <- list()
  for (i in 1:length(numeric_features)) {
    feature <- numeric_features[i]
    plots[[i]] <- ggplot(data, aes_string(x = feature)) +
      geom_histogram(bins = 30, fill = "steelblue", alpha = 0.7, color = "black") +
      geom_vline(aes_string(xintercept = mean(data[[feature]], na.rm = TRUE)),
                 color = "red", linetype = "dashed", size = 1) +
      geom_vline(aes_string(xintercept = median(data[[feature]], na.rm = TRUE)),
                 color = "green", linetype = "dashed", size = 1) +
      labs(title = paste("Distribution of", feature),
           x = feature, y = "Frequency") +
      theme_minimal()
  }
  
  pdf(paste0(output_dir, "univariate_distributions.pdf"), width = 20, height = 10)
  do.call(grid.arrange, c(plots, ncol = 4))
  dev.off()
  
  # Box plots
  plots <- list()
  for (i in 1:length(numeric_features)) {
    feature <- numeric_features[i]
    plots[[i]] <- ggplot(data, aes_string(y = feature)) +
      geom_boxplot(fill = "lightblue", alpha = 0.7) +
      labs(title = paste("Box Plot of", feature),
           y = feature) +
      theme_minimal()
  }
  
  pdf(paste0(output_dir, "univariate_boxplots.pdf"), width = 20, height = 10)
  do.call(grid.arrange, c(plots, ncol = 4))
  dev.off()
  
  # Normality tests
  cat("\n", paste(rep("=", 80), collapse = ""), "\n")
  cat("NORMALITY TESTS (Shapiro-Wilk Test)\n")
  cat(paste(rep("=", 80), collapse = ""), "\n\n")
  
  normality_results <- list()
  for (feature in numeric_features) {
    sample_size <- min(5000, nrow(data))
    sample_data <- sample(data[[feature]], sample_size)
    test_result <- shapiro.test(sample_data)
    normality_results[[feature]] <- data.frame(
      Feature = feature,
      W_statistic = test_result$statistic,
      P_value = test_result$p.value,
      Normal = ifelse(test_result$p.value > 0.05, "Yes", "No")
    )
  }
  
  normality_df <- do.call(rbind, normality_results)
  print(normality_df)
  
  return(list(univariate_stats = univariate_stats, normality_df = normality_df))
}

# Bivariate Analysis
bivariate_analysis <- function(data, output_dir) {
  cat("\n", paste(rep("=", 80), collapse = ""), "\n")
  cat("BIVARIATE ANALYSIS\n")
  cat(paste(rep("=", 80), collapse = ""), "\n\n")
  
  numeric_features <- c("Pregnancies", "Glucose", "BloodPressure", "SkinThickness",
                       "Insulin", "BMI", "DiabetesPedigreeFunction", "Age")
  
  # Feature vs Outcome box plots
  plots <- list()
  for (i in 1:length(numeric_features)) {
    feature <- numeric_features[i]
    plots[[i]] <- ggplot(data, aes_string(x = "Outcome", y = feature, fill = "Outcome")) +
      geom_boxplot(alpha = 0.7) +
      scale_fill_manual(values = c("skyblue", "salmon")) +
      labs(title = paste(feature, "by Outcome"),
           x = "Outcome", y = feature) +
      theme_minimal() +
      theme(legend.position = "none")
  }
  
  pdf(paste0(output_dir, "bivariate_boxplots.pdf"), width = 20, height = 10)
  do.call(grid.arrange, c(plots, ncol = 4))
  dev.off()
  
  # Density plots by outcome
  plots <- list()
  for (i in 1:length(numeric_features)) {
    feature <- numeric_features[i]
    plots[[i]] <- ggplot(data, aes_string(x = feature, fill = "Outcome")) +
      geom_density(alpha = 0.7) +
      scale_fill_manual(values = c("skyblue", "salmon"),
                       labels = c("No Diabetes", "Diabetes")) +
      labs(title = paste(feature, "Distribution by Outcome"),
           x = feature, y = "Density") +
      theme_minimal()
  }
  
  pdf(paste0(output_dir, "bivariate_densities.pdf"), width = 20, height = 10)
  do.call(grid.arrange, c(plots, ncol = 4))
  dev.off()
  
  # Correlation analysis
  data_numeric <- data
  data_numeric$Outcome <- as.numeric(data_numeric$Outcome) - 1
  
  correlation_matrix <- cor(data_numeric[, c(numeric_features, "Outcome")], use = "complete.obs")
  outcome_correlations <- correlation_matrix[, "Outcome"]
  outcome_correlations <- outcome_correlations[names(outcome_correlations) != "Outcome"]
  outcome_correlations <- sort(outcome_correlations, decreasing = TRUE)
  
  cat("Correlation with Outcome:\n")
  print(outcome_correlations, digits = 3)
  
  # Visualize correlations
  correlation_df <- data.frame(
    Feature = names(outcome_correlations),
    Correlation = as.numeric(outcome_correlations)
  )
  
  png(paste0(output_dir, "bivariate_correlations.png"), width = 800, height = 600)
  ggplot(correlation_df, aes(x = reorder(Feature, Correlation), y = Correlation)) +
    geom_bar(stat = "identity", fill = "steelblue", alpha = 0.7) +
    coord_flip() +
    labs(title = "Feature Correlations with Outcome",
         x = "Feature", y = "Correlation Coefficient") +
    theme_minimal()
  dev.off()
  
  # Statistical tests (T-tests)
  cat("\n", paste(rep("=", 80), collapse = ""), "\n")
  cat("STATISTICAL TESTS (Independent T-tests)\n")
  cat(paste(rep("=", 80), collapse = ""), "\n\n")
  
  diabetic <- data[data$Outcome == "Diabetes", ]
  non_diabetic <- data[data$Outcome == "No Diabetes", ]
  
  ttest_results <- list()
  for (feature in numeric_features) {
    test_result <- t.test(diabetic[[feature]], non_diabetic[[feature]])
    ttest_results[[feature]] <- data.frame(
      Feature = feature,
      T_statistic = test_result$statistic,
      P_value = test_result$p.value,
      Significant = ifelse(test_result$p.value < 0.05, "Yes", "No"),
      Diabetic_Mean = mean(diabetic[[feature]], na.rm = TRUE),
      Non_Diabetic_Mean = mean(non_diabetic[[feature]], na.rm = TRUE),
      Difference = mean(diabetic[[feature]], na.rm = TRUE) - mean(non_diabetic[[feature]], na.rm = TRUE)
    )
  }
  
  ttest_df <- do.call(rbind, ttest_results)
  print(ttest_df, digits = 4)
  
  return(list(correlations = outcome_correlations, ttest_df = ttest_df))
}

# Multivariate Analysis
multivariate_analysis <- function(data, output_dir) {
  cat("\n", paste(rep("=", 80), collapse = ""), "\n")
  cat("MULTIVARIATE ANALYSIS\n")
  cat(paste(rep("=", 80), collapse = ""), "\n\n")
  
  numeric_features <- c("Pregnancies", "Glucose", "BloodPressure", "SkinThickness",
                       "Insulin", "BMI", "DiabetesPedigreeFunction", "Age")
  
  # Correlation heatmap
  data_numeric <- data
  data_numeric$Outcome <- as.numeric(data_numeric$Outcome) - 1
  
  correlation_matrix <- cor(data_numeric[, c(numeric_features, "Outcome")], use = "complete.obs")
  
  png(paste0(output_dir, "multivariate_correlation_heatmap.png"), width = 1200, height = 1000)
  corrplot(correlation_matrix, method = "color", type = "upper", order = "hclust",
           tl.cex = 0.8, tl.col = "black", tl.srt = 45,
           addCoef.col = "black", number.cex = 0.7,
           col = colorRampPalette(c("blue", "white", "red"))(200),
           title = "Multivariate Analysis: Feature Correlation Heatmap", mar = c(0,0,2,0))
  dev.off()
  
  # PCA Analysis
  cat("\n", paste(rep("=", 80), collapse = ""), "\n")
  cat("PRINCIPAL COMPONENT ANALYSIS (PCA)\n")
  cat(paste(rep("=", 80), collapse = ""), "\n\n")
  
  # Prepare data (handle zeros)
  data_clean <- data_numeric[, numeric_features]
  data_clean[data_clean == 0] <- NA
  for (col in numeric_features) {
    data_clean[is.na(data_clean[[col]]), col] <- median(data_clean[[col]], na.rm = TRUE)
  }
  
  # Standardize
  data_scaled <- scale(data_clean)
  
  # Apply PCA
  pca <- prcomp(data_scaled, center = FALSE, scale. = FALSE)
  
  # Explained variance
  explained_variance <- pca$sdev^2 / sum(pca$sdev^2)
  cumulative_variance <- cumsum(explained_variance)
  
  cat("Explained Variance by Component:\n")
  for (i in 1:length(explained_variance)) {
    cat(sprintf("PC%d: %.4f (%.2f%%) - Cumulative: %.4f (%.2f%%)\n",
                i, explained_variance[i], explained_variance[i]*100,
                cumulative_variance[i], cumulative_variance[i]*100))
  }
  
  # Scree plot
  scree_df <- data.frame(
    PC = 1:length(explained_variance),
    Individual = explained_variance,
    Cumulative = cumulative_variance
  )
  
  png(paste0(output_dir, "multivariate_pca_scree.png"), width = 1000, height = 600)
  ggplot(scree_df, aes(x = PC)) +
    geom_bar(aes(y = Individual), stat = "identity", fill = "steelblue", alpha = 0.7) +
    geom_line(aes(y = Cumulative), color = "red", size = 1) +
    geom_point(aes(y = Cumulative), color = "red", size = 2) +
    labs(title = "PCA Scree Plot",
         x = "Principal Component", y = "Explained Variance Ratio") +
    theme_minimal()
  dev.off()
  
  # PCA visualization (2D)
  pca_2d <- data.frame(
    PC1 = pca$x[, 1],
    PC2 = pca$x[, 2],
    Outcome = data$Outcome
  )
  
  png(paste0(output_dir, "multivariate_pca_2d.png"), width = 1200, height = 800)
  ggplot(pca_2d, aes(x = PC1, y = PC2, color = Outcome)) +
    geom_point(alpha = 0.6, size = 2) +
    scale_color_manual(values = c("skyblue", "salmon"),
                      labels = c("No Diabetes", "Diabetes")) +
    labs(title = "PCA 2D Visualization",
         x = paste0("First Principal Component (Explained Variance: ",
                   round(explained_variance[1]*100, 2), "%)"),
         y = paste0("Second Principal Component (Explained Variance: ",
                   round(explained_variance[2]*100, 2), "%)")) +
    theme_minimal()
  dev.off()
  
  cat(sprintf("\nTotal Explained Variance (First 2 PCs): %.2f%%\n",
              sum(explained_variance[1:2])*100))
  
  # PCA component loadings
  pca_loadings <- data.frame(
    pca$rotation[, 1:2],
    Feature = numeric_features
  )
  colnames(pca_loadings) <- c("PC1", "PC2", "Feature")
  
  cat("\nPCA Component Loadings (First 2 Components):\n")
  print(pca_loadings, digits = 3)
  
  return(list(pca = pca, pca_loadings = pca_loadings))
}

# Main function
main <- function() {
  cat("Pima Indians Diabetes Dataset - Univariate, Bivariate, Multivariate Analysis\n")
  cat(paste(rep("=", 80), collapse = ""), "\n\n")
  
  # Load data
  data <- load_data()
  cat("Dataset loaded:", dim(data), "\n")
  cat("Features:", colnames(data), "\n\n")
  
  # Univariate analysis
  univariate_results <- univariate_analysis(data, output_dir)
  
  # Bivariate analysis
  bivariate_results <- bivariate_analysis(data, output_dir)
  
  # Multivariate analysis
  multivariate_results <- multivariate_analysis(data, output_dir)
  
  cat("\n", paste(rep("=", 80), collapse = ""), "\n")
  cat("ANALYSIS COMPLETE\n")
  cat(paste(rep("=", 80), collapse = ""), "\n\n")
  cat("Key Findings:\n")
  cat("1. Univariate: Features show varying distributions and normality\n")
  cat("2. Bivariate: Strong correlations between Glucose, BMI, Age and Outcome\n")
  cat("3. Multivariate: PCA reveals patterns in high-dimensional space\n")
  cat(paste(rep("=", 80), collapse = ""), "\n")
}

# Run main function
if (!interactive()) {
  main()
}


