###############################################################################
# Radiomics Statistical Analysis in R
# 
# This script provides comprehensive statistical analysis functions for
# radiomics data, including descriptive statistics, hypothesis testing,
# correlation analysis, and survival analysis.
#
# Author: Research Team
# Date: 2025
###############################################################################

# Load required libraries
suppressPackageStartupMessages({
  library(dplyr)
  library(tidyr)
  library(ggplot2)
  library(gridExtra)
  library(corrplot)
  library(pheatmap)
  library(survival)
  library(survminer)
  library(randomForest)
  library(caret)
  library(VIM)
  library(car)
})

# Set random seed for reproducibility
set.seed(42)

###############################################################################
# Data Loading and Preprocessing
###############################################################################

#' Load and preprocess radiomics data
#'
#' @param file_path Path to CSV file containing radiomics features
#' @param outcome_col Name of outcome column
#' @return Preprocessed data frame
load_radiomics_data <- function(file_path, outcome_col = "outcome") {
  cat("Loading radiomics data from:", file_path, "\n")
  
  # Read data
  data <- read.csv(file_path, stringsAsFactors = FALSE)
  
  # Basic data quality checks
  cat("Data dimensions:", nrow(data), "samples x", ncol(data), "features\n")
  cat("Missing values:", sum(is.na(data)), "\n")
  
  # Identify feature columns (exclude metadata columns)
  feature_cols <- setdiff(colnames(data), 
                         c("patient_id", "image_id", outcome_col, 
                           "survival_time", "survival_status"))
  
  # Convert features to numeric
  data[feature_cols] <- lapply(data[feature_cols], as.numeric)
  
  # Handle missing values (median imputation for features)
  if (sum(is.na(data[feature_cols])) > 0) {
    cat("Imputing missing values with median...\n")
    for (col in feature_cols) {
      if (sum(is.na(data[[col]])) > 0) {
        data[[col]][is.na(data[[col]])] <- median(data[[col]], na.rm = TRUE)
      }
    }
  }
  
  return(list(data = data, feature_cols = feature_cols))
}


###############################################################################
# Descriptive Statistics
###############################################################################

#' Calculate descriptive statistics for radiomic features
#'
#' @param data Data frame with radiomics features
#' @param feature_cols Vector of feature column names
#' @param group_col Optional grouping column name
#' @return Data frame with descriptive statistics
calculate_descriptive_stats <- function(data, feature_cols, group_col = NULL) {
  cat("Calculating descriptive statistics...\n")
  
  if (is.null(group_col)) {
    # Overall statistics
    stats <- data %>%
      select(all_of(feature_cols)) %>%
      summarise_all(list(
        mean = mean,
        median = median,
        sd = sd,
        min = min,
        max = max,
        q25 = ~quantile(.x, 0.25, na.rm = TRUE),
        q75 = ~quantile(.x, 0.75, na.rm = TRUE)
      ))
    
    stats_long <- stats %>%
      gather(key = "stat_feature", value = "value") %>%
      separate(stat_feature, into = c("stat", "feature"), sep = "_") %>%
      spread(key = stat, value = value)
    
    return(stats_long)
  } else {
    # Grouped statistics
    stats <- data %>%
      group_by(!!sym(group_col)) %>%
      select(all_of(feature_cols)) %>%
      summarise_all(list(
        mean = mean,
        median = median,
        sd = sd,
        n = length
      ), na.rm = TRUE)
    
    return(stats)
  }
}


###############################################################################
# Hypothesis Testing
###############################################################################

#' Compare radiomic features between two groups using t-test
#'
#' T-test is appropriate here because it allows for straightforward hypothesis
#' testing on differences of means between two independent groups.
#'
#' @param data Data frame with features and group labels
#' @param feature_cols Vector of feature column names
#' @param group_col Name of grouping column
#' @param group1 Name of first group
#' @param group2 Name of second group
#' @return Data frame with test results
compare_groups_ttest <- function(data, feature_cols, group_col, 
                                  group1, group2) {
  cat("Comparing", group1, "vs", group2, "using t-test...\n")
  
  group1_data <- data[data[[group_col]] == group1, ]
  group2_data <- data[data[[group_col]] == group2, ]
  
  results <- data.frame(
    feature = character(),
    group1_mean = numeric(),
    group1_sd = numeric(),
    group2_mean = numeric(),
    group2_sd = numeric(),
    mean_difference = numeric(),
    t_statistic = numeric(),
    p_value = numeric(),
    stringsAsFactors = FALSE
  )
  
  for (feature in feature_cols) {
    values1 <- group1_data[[feature]]
    values2 <- group2_data[[feature]]
    
    # Remove NA values
    values1 <- values1[!is.na(values1)]
    values2 <- values2[!is.na(values2)]
    
    if (length(values1) >= 3 && length(values2) >= 3) {
      # Perform t-test
      test_result <- t.test(values1, values2)
      
      # Check normality (Shapiro-Wilk test for small samples)
      if (length(values1) <= 50 && length(values2) <= 50) {
        norm1 <- shapiro.test(values1)
        norm2 <- shapiro.test(values2)
      }
      
      results <- rbind(results, data.frame(
        feature = feature,
        group1_mean = mean(values1),
        group1_sd = sd(values1),
        group2_mean = mean(values2),
        group2_sd = sd(values2),
        mean_difference = mean(values1) - mean(values2),
        t_statistic = test_result$statistic,
        p_value = test_result$p.value,
        stringsAsFactors = FALSE
      ))
    }
  }
  
  # Add significance flag and adjust for multiple comparisons (Bonferroni)
  results$significant <- results$p_value < 0.05
  results$p_value_adjusted <- p.adjust(results$p_value, method = "bonferroni")
  results$significant_adjusted <- results$p_value_adjusted < 0.05
  
  # Calculate effect size (Cohen's d)
  results$cohens_d <- (results$group1_mean - results$group2_mean) / 
    sqrt((results$group1_sd^2 + results$group2_sd^2) / 2)
  
  results <- results[order(results$p_value), ]
  
  return(results)
}


#' Non-parametric comparison using Mann-Whitney U test
#'
#' @param data Data frame with features and group labels
#' @param feature_cols Vector of feature column names
#' @param group_col Name of grouping column
#' @param group1 Name of first group
#' @param group2 Name of second group
#' @return Data frame with test results
compare_groups_mannwhitney <- function(data, feature_cols, group_col,
                                       group1, group2) {
  cat("Comparing", group1, "vs", group2, "using Mann-Whitney U test...\n")
  
  group1_data <- data[data[[group_col]] == group1, ]
  group2_data <- data[data[[group_col]] == group2, ]
  
  results <- data.frame(
    feature = character(),
    group1_median = numeric(),
    group2_median = numeric(),
    u_statistic = numeric(),
    p_value = numeric(),
    stringsAsFactors = FALSE
  )
  
  for (feature in feature_cols) {
    values1 <- group1_data[[feature]][!is.na(group1_data[[feature]])]
    values2 <- group2_data[[feature]][!is.na(group2_data[[feature]])]
    
    if (length(values1) >= 3 && length(values2) >= 3) {
      test_result <- wilcox.test(values1, values2)
      
      results <- rbind(results, data.frame(
        feature = feature,
        group1_median = median(values1),
        group2_median = median(values2),
        u_statistic = test_result$statistic,
        p_value = test_result$p.value,
        stringsAsFactors = FALSE
      ))
    }
  }
  
  results$significant <- results$p_value < 0.05
  results$p_value_adjusted <- p.adjust(results$p_value, method = "bonferroni")
  results <- results[order(results$p_value), ]
  
  return(results)
}


###############################################################################
# Correlation Analysis
###############################################################################

#' Calculate correlations between features and outcome
#'
#' @param data Data frame with features and outcome
#' @param feature_cols Vector of feature column names
#' @param outcome_col Name of outcome column
#' @param method Correlation method ("pearson" or "spearman")
#' @return Data frame with correlation results
calculate_correlations <- function(data, feature_cols, outcome_col, 
                                   method = "pearson") {
  cat("Calculating", method, "correlations...\n")
  
  correlations <- data.frame(
    feature = character(),
    correlation = numeric(),
    p_value = numeric(),
    stringsAsFactors = FALSE
  )
  
  for (feature in feature_cols) {
    if (feature %in% colnames(data) && outcome_col %in% colnames(data)) {
      complete_data <- data[c(feature, outcome_col)]
      complete_data <- complete_data[complete.cases(complete_data), ]
      
      if (nrow(complete_data) > 3) {
        if (method == "pearson") {
          cor_test <- cor.test(complete_data[[feature]], 
                              complete_data[[outcome_col]], 
                              method = "pearson")
        } else {
          cor_test <- cor.test(complete_data[[feature]], 
                              complete_data[[outcome_col]], 
                              method = "spearman")
        }
        
        correlations <- rbind(correlations, data.frame(
          feature = feature,
          correlation = cor_test$estimate,
          p_value = cor_test$p.value,
          stringsAsFactors = FALSE
        ))
      }
    }
  }
  
  correlations$abs_correlation <- abs(correlations$correlation)
  correlations$significant <- correlations$p_value < 0.05
  correlations <- correlations[order(correlations$abs_correlation, 
                                     decreasing = TRUE), ]
  
  return(correlations)
}


###############################################################################
# Principal Component Analysis (PCA)
###############################################################################

#' Perform PCA on radiomic features
#'
#' PCA was chosen for dimensionality reduction due to its interpretability
#' and linear assumptions, which align well with radiomic datasets that
#' often exhibit linear relationships between features.
#'
#' @param data Data frame with features
#' @param feature_cols Vector of feature column names
#' @param n_components Number of principal components to return
#' @param scale_features Whether to scale features before PCA
#' @return List with PCA results
perform_pca <- function(data, feature_cols, n_components = NULL, 
                        scale_features = TRUE) {
  cat("Performing PCA...\n")
  
  # Extract feature matrix
  feature_matrix <- data[, feature_cols, drop = FALSE]
  
  # Remove rows with missing values
  complete_cases <- complete.cases(feature_matrix)
  feature_matrix <- feature_matrix[complete_cases, ]
  
  if (scale_features) {
    feature_matrix <- scale(feature_matrix)
  }
  
  # Perform PCA
  pca_result <- prcomp(feature_matrix, center = FALSE, scale. = FALSE)
  
  # Determine number of components (explain 95% variance if not specified)
  if (is.null(n_components)) {
    variance_explained <- cumsum(pca_result$sdev^2 / sum(pca_result$sdev^2))
    n_components <- which(variance_explained >= 0.95)[1]
    if (is.na(n_components)) {
      n_components <- min(50, ncol(feature_matrix))
    }
  }
  
  # Extract components
  pca_data <- as.data.frame(pca_result$x[, 1:n_components])
  
  # Calculate variance explained
  variance_explained <- pca_result$sdev^2 / sum(pca_result$sdev^2)
  
  cat(sprintf("PCA: %d components explain %.2f%% of variance\n",
              n_components, sum(variance_explained[1:n_components]) * 100))
  
  return(list(
    pca_data = pca_data,
    pca_object = pca_result,
    variance_explained = variance_explained,
    n_components = n_components
  ))
}


###############################################################################
# Survival Analysis
###############################################################################

#' Perform survival analysis using radiomic features
#'
#' @param data Data frame with features, survival time, and survival status
#' @param feature_cols Vector of feature column names
#' @param time_col Name of survival time column
#' @param status_col Name of survival status column (1 = event, 0 = censored)
#' @param cutoff_method Method for determining high/low risk cutoff ("median" or "optimal")
#' @return List with survival analysis results
perform_survival_analysis <- function(data, feature_cols, time_col, status_col,
                                     cutoff_method = "median") {
  cat("Performing survival analysis...\n")
  
  survival_results <- data.frame(
    feature = character(),
    hr = numeric(),
    hr_lower = numeric(),
    hr_upper = numeric(),
    p_value = numeric(),
    stringsAsFactors = FALSE
  )
  
  for (feature in feature_cols) {
    if (feature %in% colnames(data)) {
      # Create survival object
      surv_obj <- Surv(data[[time_col]], data[[status_col]])
      
      # Determine cutoff
      if (cutoff_method == "median") {
        cutoff <- median(data[[feature]], na.rm = TRUE)
      } else {
        # Find optimal cutoff (survminer)
        cutoff_result <- surv_cutpoint(data, 
                                      time = time_col, 
                                      event = status_col, 
                                      variables = feature)
        cutoff <- cutoff_result$cutpoint$cutpoint
      }
      
      # Create risk groups
      risk_group <- ifelse(data[[feature]] > cutoff, "High", "Low")
      
      # Fit Cox model
      cox_fit <- coxph(surv_obj ~ risk_group, data = data)
      cox_summary <- summary(cox_fit)
      
      survival_results <- rbind(survival_results, data.frame(
        feature = feature,
        hr = cox_summary$conf.int[1, "exp(coef)"],
        hr_lower = cox_summary$conf.int[1, "lower .95"],
        hr_upper = cox_summary$conf.int[1, "upper .95"],
        p_value = cox_summary$coef[1, "Pr(>|z|)"],
        stringsAsFactors = FALSE
      ))
    }
  }
  
  survival_results$significant <- survival_results$p_value < 0.05
  survival_results <- survival_results[order(survival_results$p_value), ]
  
  return(survival_results)
}


###############################################################################
# Visualization Functions
###############################################################################

#' Create box plots comparing features between groups
#'
#' @param data Data frame with features and group labels
#' @param feature_cols Vector of feature column names
#' @param group_col Name of grouping column
#' @param n_features Number of top features to plot
#' @param output_file Optional file path to save plot
plot_feature_comparison <- function(data, feature_cols, group_col, 
                                    n_features = 6, output_file = NULL) {
  # Select top variable features
  feature_variance <- sapply(feature_cols, function(x) var(data[[x]], na.rm = TRUE))
  top_features <- names(sort(feature_variance, decreasing = TRUE))[1:n_features]
  
  plots <- list()
  for (feature in top_features) {
    p <- ggplot(data, aes_string(x = group_col, y = feature, fill = group_col)) +
      geom_boxplot(alpha = 0.7) +
      geom_jitter(width = 0.2, alpha = 0.3) +
      labs(title = feature, x = "Group", y = "Feature Value") +
      theme_minimal() +
      theme(legend.position = "none")
    plots[[feature]] <- p
  }
  
  combined_plot <- grid.arrange(grobs = plots, ncol = 3)
  
  if (!is.null(output_file)) {
    ggsave(output_file, combined_plot, width = 15, height = 10, dpi = 300)
  }
  
  return(combined_plot)
}


#' Create correlation heatmap
#'
#' @param data Data frame with features
#' @param feature_cols Vector of feature column names
#' @param method Correlation method
#' @param output_file Optional file path to save plot
plot_correlation_heatmap <- function(data, feature_cols, method = "pearson",
                                     output_file = NULL) {
  # Calculate correlation matrix
  feature_matrix <- data[, feature_cols, drop = FALSE]
  cor_matrix <- cor(feature_matrix, use = "complete.obs", method = method)
  
  # Plot
  pheatmap(cor_matrix,
           clustering_distance_rows = "correlation",
           clustering_distance_cols = "correlation",
           color = colorRampPalette(c("blue", "white", "red"))(100),
           main = paste("Feature Correlation Matrix (", method, ")"),
           filename = output_file,
           width = 12,
           height = 10)
  
  return(cor_matrix)
}


###############################################################################
# Machine Learning (Random Forest)
###############################################################################

#' Build random forest model for outcome prediction
#'
#' @param data Data frame with features and outcome
#' @param feature_cols Vector of feature column names
#' @param outcome_col Name of outcome column
#' @param n_trees Number of trees in random forest
#' @param n_features_selected Number of features to select
#' @return Trained random forest model
build_random_forest <- function(data, feature_cols, outcome_col,
                                n_trees = 500, n_features_selected = 50) {
  cat("Building random forest model...\n")
  
  # Prepare data
  feature_data <- data[, feature_cols, drop = FALSE]
  outcome_data <- data[[outcome_col]]
  
  # Remove rows with missing values
  complete_cases <- complete.cases(feature_data) & !is.na(outcome_data)
  feature_data <- feature_data[complete_cases, ]
  outcome_data <- outcome_data[complete_cases]
  
  # Feature selection (if needed)
  if (length(feature_cols) > n_features_selected) {
    # Use random forest importance for feature selection
    temp_rf <- randomForest(x = feature_data, y = outcome_data, ntree = 100)
    importance_scores <- importance(temp_rf)
    top_features <- rownames(importance_scores)[
      order(importance_scores, decreasing = TRUE)[1:n_features_selected]
    ]
    feature_data <- feature_data[, top_features]
  }
  
  # Train model
  rf_model <- randomForest(
    x = feature_data,
    y = outcome_data,
    ntree = n_trees,
    importance = TRUE,
    proximity = TRUE
  )
  
  cat("Model trained with", n_trees, "trees\n")
  cat("Out-of-bag error:", rf_model$err.rate[n_trees, "OOB"], "\n")
  
  return(rf_model)
}


###############################################################################
# Main Analysis Pipeline
###############################################################################

main <- function() {
  cat("=" %&% paste(rep("=", 59), collapse = "") %&% "\n")
  cat("Radiomics Statistical Analysis Pipeline\n")
  cat("=" %&% paste(rep("=", 59), collapse = "") %&% "\n\n")
  
  # Example: Create synthetic data for demonstration
  cat("1. Generating synthetic radiomics data...\n")
  n_samples <- 100
  feature_data <- data.frame(
    firstorder_Mean = rnorm(n_samples, 100, 20),
    firstorder_StdDev = rnorm(n_samples, 15, 5),
    firstorder_Entropy = rnorm(n_samples, 3.5, 0.5),
    glcm_Correlation = rnorm(n_samples, 0.7, 0.1),
    glcm_Contrast = rnorm(n_samples, 5, 2),
    shape_Volume = rnorm(n_samples, 50, 15),
    shape_Sphericity = rnorm(n_samples, 0.7, 0.1)
  )
  
  # Create binary outcome
  outcome <- ifelse(feature_data$firstorder_Entropy > 3.5, 1, 0)
  feature_data$outcome <- outcome
  feature_data$group <- ifelse(outcome == 0, "Poor_Outcome", "Good_Outcome")
  
  feature_cols <- setdiff(colnames(feature_data), c("outcome", "group"))
  
  cat("   Data: ", nrow(feature_data), "samples x", length(feature_cols), "features\n\n")
  
  # Descriptive statistics
  cat("2. Descriptive statistics...\n")
  desc_stats <- calculate_descriptive_stats(feature_data, feature_cols)
  print(head(desc_stats, 10))
  cat("\n")
  
  # Group comparison
  cat("3. Comparing groups (t-test)...\n")
  comparison_results <- compare_groups_ttest(
    feature_data, feature_cols, "group", "Poor_Outcome", "Good_Outcome"
  )
  cat("Top significant features:\n")
  print(head(comparison_results[comparison_results$significant, 
                                c("feature", "p_value", "mean_difference")], 5))
  cat("\n")
  
  # Correlation analysis
  cat("4. Correlation analysis...\n")
  corr_results <- calculate_correlations(feature_data, feature_cols, "outcome")
  cat("Top correlated features:\n")
  print(head(corr_results[, c("feature", "correlation", "p_value")], 5))
  cat("\n")
  
  # PCA
  cat("5. Principal Component Analysis...\n")
  pca_result <- perform_pca(feature_data, feature_cols, n_components = 3)
  cat("Variance explained by first 3 components:\n")
  for (i in 1:3) {
    cat(sprintf("  PC%d: %.2f%%\n", i, pca_result$variance_explained[i] * 100))
  }
  cat("\n")
  
  # Random Forest
  cat("6. Building Random Forest model...\n")
  rf_model <- build_random_forest(feature_data, feature_cols, "outcome")
  cat("\nTop 5 most important features:\n")
  importance_df <- as.data.frame(importance(rf_model))
  importance_df <- importance_df[order(importance_df$MeanDecreaseGini, 
                                      decreasing = TRUE), ]
  print(head(importance_df, 5))
  cat("\n")
  
  # Visualization
  cat("7. Creating visualizations...\n")
  plot_feature_comparison(feature_data, feature_cols, "group", n_features = 6)
  
  cat("\n" %&% paste(rep("=", 60), collapse = "") %&% "\n")
  cat("Analysis complete!\n")
}

# Helper function for string concatenation
`%&%` <- function(a, b) paste0(a, b)

# Run main analysis if script is executed directly
if (!interactive()) {
  main()
}

