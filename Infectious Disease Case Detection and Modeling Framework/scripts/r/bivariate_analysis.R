# Bivariate Analysis Module
# R script for bivariate statistical analysis

library(ggplot2)
library(dplyr)
library(corrplot)
library(gridExtra)
library(rlang)
source("data_loader.R")

# Function for bivariate analysis (numerical vs numerical)
# Perform bivariate analysis between two variables
# Parameters: df_clean - cleaned dataset, var1/var2 - variables to analyze
bivariate_analysis <- function(df_clean, var1 = "Incidence_Rate", var2 = "Annual_Count") {
  cat("=== BIVARIATE ANALYSIS:", var1, "vs", var2, "===\n\n")
  
  # Remove missing values
  data <- df_clean %>%
    select(all_of(c(var1, var2))) %>%
    filter(!is.na(.data[[var1]]) & !is.na(.data[[var2]]))
  
  # Correlation analysis
  correlation <- cor(data[[var1]], data[[var2]])
  cat("1. Correlation Coefficient:", correlation, "\n")
  
  # Pearson correlation test
  pearson_test <- cor.test(data[[var1]], data[[var2]], method = "pearson")
  cat("   Pearson correlation: r =", pearson_test$estimate, 
      ", p-value =", pearson_test$p.value, "\n")
  
  # Spearman correlation
  spearman_test <- cor.test(data[[var1]], data[[var2]], method = "spearman")
  cat("   Spearman correlation: rho =", spearman_test$estimate, 
      ", p-value =", spearman_test$p.value, "\n")
  
  # Create visualizations
  p1 <- ggplot(data, aes_string(x = var1, y = var2)) +
    geom_point(alpha = 0.5) +
    geom_smooth(method = "lm", se = TRUE, color = "red") +
    labs(title = paste("Scatter Plot:", var1, "vs", var2),
         x = var1, y = var2) +
    theme_minimal()
  
  p2 <- ggplot(data, aes_string(x = var1, y = var2)) +
    geom_hex(bins = 30) +
    scale_fill_gradient(low = "white", high = "steelblue") +
    labs(title = paste("Hexbin Plot:", var1, "vs", var2),
         x = var1, y = var2) +
    theme_minimal()
  
  # Combine plots
  grid.arrange(p1, p2, ncol = 2)
  
  return(list(
    correlation = correlation,
    pearson_r = pearson_test$estimate,
    pearson_p = pearson_test$p.value,
    spearman_r = spearman_test$estimate,
    spearman_p = spearman_test$p.value
  ))
}

# Function for categorical vs numerical analysis
# Analyze relationship between categorical and numerical variables
# Parameters: df_clean - cleaned dataset, cat_var - categorical variable, num_var - numerical variable
categorical_bivariate_analysis <- function(df_clean, cat_var = "Trend", num_var = "Incidence_Rate") {
  cat("=== BIVARIATE ANALYSIS:", cat_var, "vs", num_var, "===\n\n")
  
  if (!cat_var %in% colnames(df_clean)) {
    cat("Variable", cat_var, "not found in dataset\n")
    return(NULL)
  }
  
  data <- df_clean %>%
    select(all_of(c(cat_var, num_var))) %>%
    filter(!is.na(.data[[cat_var]]) & !is.na(.data[[num_var]]))
  
  # Group statistics
  group_stats <- data %>%
    group_by(.data[[cat_var]]) %>%
    summarise(
      count = n(),
      mean = mean(.data[[num_var]], na.rm = TRUE),
      median = median(.data[[num_var]], na.rm = TRUE),
      sd = sd(.data[[num_var]], na.rm = TRUE),
      .groups = "drop"
    )
  
  cat("1. Group Statistics:\n")
  print(group_stats)
  
  # Create visualizations
  p1 <- ggplot(data, aes_string(x = cat_var, y = num_var)) +
    geom_boxplot(fill = "steelblue", alpha = 0.7) +
    labs(title = paste("Box Plot:", num_var, "by", cat_var),
         x = cat_var, y = num_var) +
    theme_minimal() +
    theme(axis.text.x = element_text(angle = 45, hjust = 1))
  
  p2 <- ggplot(data, aes_string(x = cat_var, y = num_var)) +
    geom_violin(fill = "steelblue", alpha = 0.7) +
    labs(title = paste("Violin Plot:", num_var, "by", cat_var),
         x = cat_var, y = num_var) +
    theme_minimal() +
    theme(axis.text.x = element_text(angle = 45, hjust = 1))
  
  p3 <- ggplot(group_stats, aes_string(x = cat_var, y = "mean")) +
    geom_bar(stat = "identity", fill = "steelblue", alpha = 0.7) +
    labs(title = paste("Mean", num_var, "by", cat_var),
         x = cat_var, y = paste("Mean", num_var)) +
    theme_minimal() +
    theme(axis.text.x = element_text(angle = 45, hjust = 1))
  
  p4 <- ggplot(data, aes_string(x = cat_var, y = num_var)) +
    geom_jitter(alpha = 0.5, width = 0.2) +
    labs(title = paste("Strip Plot:", num_var, "by", cat_var),
         x = cat_var, y = num_var) +
    theme_minimal() +
    theme(axis.text.x = element_text(angle = 45, hjust = 1))
  
  # Combine plots
  grid.arrange(p1, p2, p3, p4, ncol = 2, nrow = 2)
  
  # ANOVA test
  if (length(unique(data[[cat_var]])) > 2) {
    anova_result <- aov(data[[num_var]] ~ data[[cat_var]])
    anova_summary <- summary(anova_result)
    
    cat("\n2. ANOVA Test:\n")
    print(anova_summary)
  }
  
  return(group_stats)
}

# Main execution
if (!interactive()) {
  df <- load_data()
  df_clean <- clean_data(df)
  
  # Numerical vs Numerical
  result1 <- bivariate_analysis(df_clean, "Incidence_Rate", "Annual_Count")
  
  # Categorical vs Numerical
  if ("Trend" %in% colnames(df_clean)) {
    result2 <- categorical_bivariate_analysis(df_clean, "Trend", "Incidence_Rate")
  }
}

