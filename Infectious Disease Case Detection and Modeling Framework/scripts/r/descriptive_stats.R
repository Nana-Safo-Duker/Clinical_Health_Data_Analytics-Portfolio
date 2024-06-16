# Descriptive Statistics Module
# R script for descriptive statistical analysis

library(dplyr)
library(psych)
source("data_loader.R")

# Function to calculate descriptive statistics
# Calculate comprehensive descriptive statistics
# Parameters: data - numeric vector, col_name - variable name
# Returns: data.frame with descriptive statistics
descriptive_stats <- function(data, col_name) {
  stats <- data.frame(
    Variable = col_name,
    Mean = mean(data, na.rm = TRUE),
    Median = median(data, na.rm = TRUE),
    Mode = as.numeric(names(sort(table(data), decreasing = TRUE)[1])),
    SD = sd(data, na.rm = TRUE),
    Variance = var(data, na.rm = TRUE),
    Min = min(data, na.rm = TRUE),
    Max = max(data, na.rm = TRUE),
    Range = max(data, na.rm = TRUE) - min(data, na.rm = TRUE),
    Q1 = quantile(data, 0.25, na.rm = TRUE),
    Q3 = quantile(data, 0.75, na.rm = TRUE),
    IQR = IQR(data, na.rm = TRUE),
    Skewness = skew(data, na.rm = TRUE),
    Kurtosis = kurtosi(data, na.rm = TRUE),
    CV = (sd(data, na.rm = TRUE) / mean(data, na.rm = TRUE)) * 100
  )
  
  return(stats)
}

# Function to calculate and display descriptive statistics
calculate_descriptive_stats <- function(df_clean) {
  cat("=== DESCRIPTIVE STATISTICS ===\n\n")
  
  # Basic statistics
  cat("1. Summary Statistics for Incidence Rate:\n")
  print(summary(df_clean$Incidence_Rate))
  
  cat("\n2. Summary Statistics for Annual Count:\n")
  print(summary(df_clean$Annual_Count))
  
  # Comprehensive statistics
  cat("\n3. Comprehensive Descriptive Statistics for Incidence Rate:\n")
  incidence_stats <- descriptive_stats(df_clean$Incidence_Rate, "Incidence_Rate")
  print(incidence_stats)
  
  # Statistics by Trend
  if ("Trend" %in% colnames(df_clean)) {
    cat("\n4. Descriptive Statistics by Trend Category:\n")
    trend_stats <- df_clean %>%
      group_by(Trend) %>%
      summarise(
        count = n(),
        mean = mean(Incidence_Rate, na.rm = TRUE),
        median = median(Incidence_Rate, na.rm = TRUE),
        sd = sd(Incidence_Rate, na.rm = TRUE),
        min = min(Incidence_Rate, na.rm = TRUE),
        max = max(Incidence_Rate, na.rm = TRUE),
        .groups = "drop"
      )
    print(trend_stats)
  }
  
  return(incidence_stats)
}

# Main execution
if (!interactive()) {
  df <- load_data()
  df_clean <- clean_data(df)
  stats <- calculate_descriptive_stats(df_clean)
}

