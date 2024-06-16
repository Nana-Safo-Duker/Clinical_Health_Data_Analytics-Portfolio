# Univariate Analysis Module
# R script for univariate statistical analysis

library(ggplot2)
library(dplyr)
library(gridExtra)
source("data_loader.R")

# Function for univariate analysis
# Perform univariate analysis on a single variable
# Parameters: df_clean - cleaned dataset, variable - variable to analyze
univariate_analysis <- function(df_clean, variable = "Incidence_Rate") {
  data <- df_clean[[variable]]
  data <- data[!is.na(data)]
  
  cat("=== UNIVARIATE ANALYSIS:", variable, "===\n\n")
  
  # Descriptive statistics
  cat("1. Descriptive Statistics:\n")
  print(summary(data))
  
  # Distribution characteristics
  cat("\n2. Distribution Characteristics:\n")
  cat("   Skewness:", e1071::skewness(data), "\n")
  cat("   Kurtosis:", e1071::kurtosis(data), "\n")
  cat("   Coefficient of Variation:", (sd(data) / mean(data) * 100), "%\n")
  
  # Create visualizations
  p1 <- ggplot(data.frame(x = data), aes(x = x)) +
    geom_histogram(bins = 50, fill = "steelblue", alpha = 0.7, color = "black") +
    geom_vline(aes(xintercept = mean(data)), color = "red", linetype = "dashed") +
    geom_vline(aes(xintercept = median(data)), color = "green", linetype = "dashed") +
    labs(title = paste("Histogram of", variable),
         x = variable, y = "Frequency") +
    theme_minimal()
  
  p2 <- ggplot(data.frame(x = data), aes(y = x)) +
    geom_boxplot(fill = "steelblue", alpha = 0.7) +
    labs(title = paste("Box Plot of", variable),
         y = variable) +
    theme_minimal()
  
  p3 <- ggplot(data.frame(x = data), aes(x = x)) +
    geom_density(fill = "steelblue", alpha = 0.7) +
    labs(title = paste("Density Plot of", variable),
         x = variable, y = "Density") +
    theme_minimal()
  
  # Q-Q plot
  qq_data <- data.frame(
    theoretical = qqnorm(data, plot.it = FALSE)$x,
    sample = qqnorm(data, plot.it = FALSE)$y
  )
  
  p4 <- ggplot(qq_data, aes(x = theoretical, y = sample)) +
    geom_point(alpha = 0.5) +
    geom_abline(intercept = 0, slope = 1, color = "red") +
    labs(title = paste("Q-Q Plot of", variable),
         x = "Theoretical Quantiles", y = "Sample Quantiles") +
    theme_minimal()
  
  # Violin plot
  p5 <- ggplot(data.frame(x = data), aes(x = "", y = x)) +
    geom_violin(fill = "steelblue", alpha = 0.7) +
    labs(title = paste("Violin Plot of", variable),
         x = "", y = variable) +
    theme_minimal()
  
  # Cumulative distribution
  sorted_data <- sort(data)
  y <- seq(1, length(sorted_data)) / length(sorted_data)
  p6 <- ggplot(data.frame(x = sorted_data, y = y), aes(x = x, y = y)) +
    geom_line(color = "steelblue") +
    labs(title = paste("Cumulative Distribution of", variable),
         x = variable, y = "Cumulative Probability") +
    theme_minimal()
  
  # Combine plots
  grid.arrange(p1, p2, p3, p4, p5, p6, ncol = 3, nrow = 2)
  
  # Outlier detection
  Q1 <- quantile(data, 0.25)
  Q3 <- quantile(data, 0.75)
  IQR <- Q3 - Q1
  lower_bound <- Q1 - 1.5 * IQR
  upper_bound <- Q3 + 1.5 * IQR
  
  outliers <- data[data < lower_bound | data > upper_bound]
  
  cat("\n3. Outlier Detection (IQR Method):\n")
  cat("   Lower bound:", lower_bound, "\n")
  cat("   Upper bound:", upper_bound, "\n")
  cat("   Number of outliers:", length(outliers), "\n")
  cat("   Percentage:", (length(outliers) / length(data) * 100), "%\n")
  
  return(list(
    data = data,
    outliers = outliers,
    stats = summary(data)
  ))
}

# Main execution
if (!interactive()) {
  df <- load_data()
  df_clean <- clean_data(df)
  result <- univariate_analysis(df_clean, "Incidence_Rate")
}

