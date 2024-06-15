# Comprehensive Exploratory Data Analysis Module
# R script for comprehensive EDA

library(ggplot2)
library(dplyr)
library(corrplot)
library(VIM)
library(mice)
source("data_loader.R")

# Function for comprehensive EDA
# Perform comprehensive exploratory data analysis
# Parameters: df_clean - cleaned dataset
comprehensive_eda <- function(df_clean) {
  cat("=== COMPREHENSIVE EXPLORATORY DATA ANALYSIS ===\n\n")
  
  # 1. Data Overview
  cat("1. DATA OVERVIEW\n")
  cat("=" , rep("=", 49), "\n", sep = "")
  cat("Dataset shape:", dim(df_clean), "\n")
  cat("Number of rows:", nrow(df_clean), "\n")
  cat("Number of columns:", ncol(df_clean), "\n")
  cat("Memory usage:", object.size(df_clean) / 1024^2, "MB\n")
  
  # 2. Data Types and Missing Values
  cat("\n2. DATA QUALITY\n")
  cat("=" , rep("=", 49), "\n", sep = "")
  cat("Data Types:\n")
  print(sapply(df_clean, class))
  
  cat("\nMissing Values:\n")
  missing <- colSums(is.na(df_clean))
  missing_pct <- (missing / nrow(df_clean)) * 100
  missing_df <- data.frame(
    Missing_Count = missing,
    Percentage = missing_pct
  )
  missing_df <- missing_df[missing_df$Missing_Count > 0, ]
  if (nrow(missing_df) > 0) {
    print(missing_df)
  } else {
    cat("No missing values found\n")
  }
  
  # 3. Summary Statistics
  cat("\n3. SUMMARY STATISTICS\n")
  cat("=" , rep("=", 49), "\n", sep = "")
  numeric_cols <- sapply(df_clean, is.numeric)
  print(summary(df_clean[, numeric_cols]))
  
  # 4. Distribution Analysis
  cat("\n4. DISTRIBUTION ANALYSIS\n")
  cat("=" , rep("=", 49), "\n", sep = "")
  numeric_cols_names <- names(df_clean)[numeric_cols]
  for (col in head(numeric_cols_names, 5)) {
    cat("\n", col, ":\n", sep = "")
    cat("  Skewness:", e1071::skewness(df_clean[[col]], na.rm = TRUE), "\n")
    cat("  Kurtosis:", e1071::kurtosis(df_clean[[col]], na.rm = TRUE), "\n")
    cat("  CV:", (sd(df_clean[[col]], na.rm = TRUE) / mean(df_clean[[col]], na.rm = TRUE) * 100), "%\n")
  }
  
  # 5. Create visualizations
  create_eda_visualizations(df_clean)
  
  # 6. Feature Engineering
  cat("\n5. FEATURE ENGINEERING OPPORTUNITIES\n")
  cat("=" , rep("=", 49), "\n", sep = "")
  if ("County" %in% colnames(df_clean)) {
    # Extract state from county name
    df_clean$State <- gsub(".*,\\s*(\\w+)\\(.*", "\\1", df_clean$County)
    cat("Extracted state information from county names\n")
  }
  
  if ("FIPS" %in% colnames(df_clean)) {
    # State FIPS code (first 2 digits)
    df_clean$State_FIPS <- floor(df_clean$FIPS / 1000)
    cat("Extracted state FIPS codes\n")
  }
  
  # 7. Outlier Analysis
  cat("\n6. OUTLIER ANALYSIS\n")
  cat("=" , rep("=", 49), "\n", sep = "")
  for (col in head(numeric_cols_names, 3)) {
    Q1 <- quantile(df_clean[[col]], 0.25, na.rm = TRUE)
    Q3 <- quantile(df_clean[[col]], 0.75, na.rm = TRUE)
    IQR <- Q3 - Q1
    lower_bound <- Q1 - 1.5 * IQR
    upper_bound <- Q3 + 1.5 * IQR
    outliers <- df_clean[[col]][df_clean[[col]] < lower_bound | df_clean[[col]] > upper_bound]
    cat(col, ":", length(outliers[!is.na(outliers)]), "outliers (", 
        length(outliers[!is.na(outliers)]) / length(df_clean[[col]][!is.na(df_clean[[col]])]) * 100, "%)\n")
  }
  
  return(df_clean)
}

# Function to create EDA visualizations
# Create comprehensive EDA visualizations
create_eda_visualizations <- function(df_clean) {
  
  numeric_cols <- sapply(df_clean, is.numeric)
  numeric_cols_names <- names(df_clean)[numeric_cols]
  
  # 1. Distribution plots for key variables
  if ("Incidence_Rate" %in% colnames(df_clean)) {
    png("eda_distributions.png", width = 1500, height = 1200, res = 300)
    
    p1 <- ggplot(df_clean, aes(x = Incidence_Rate)) +
      geom_histogram(bins = 50, fill = "steelblue", alpha = 0.7, color = "black") +
      labs(title = "Distribution of Incidence Rate", x = "Incidence Rate", y = "Frequency") +
      theme_minimal()
    
    p2 <- ggplot(df_clean, aes(y = Incidence_Rate)) +
      geom_boxplot(fill = "steelblue", alpha = 0.7) +
      labs(title = "Box Plot of Incidence Rate", y = "Incidence Rate") +
      theme_minimal()
    
    # Q-Q plot
    qq_data <- data.frame(
      theoretical = qqnorm(df_clean$Incidence_Rate, plot.it = FALSE)$x,
      sample = qqnorm(df_clean$Incidence_Rate, plot.it = FALSE)$y
    )
    p3 <- ggplot(qq_data, aes(x = theoretical, y = sample)) +
      geom_point(alpha = 0.5) +
      geom_abline(intercept = 0, slope = 1, color = "red") +
      labs(title = "Q-Q Plot", x = "Theoretical Quantiles", y = "Sample Quantiles") +
      theme_minimal()
    
    p4 <- ggplot(df_clean, aes(x = Incidence_Rate)) +
      geom_density(fill = "steelblue", alpha = 0.7) +
      labs(title = "Density Plot of Incidence Rate", x = "Incidence Rate", y = "Density") +
      theme_minimal()
    
    grid.arrange(p1, p2, p3, p4, ncol = 2, nrow = 2)
    dev.off()
  }
  
  # 2. Correlation heatmap
  if (length(numeric_cols_names) > 1) {
    png("eda_correlation.png", width = 1200, height = 1000, res = 300)
    corr_matrix <- cor(df_clean[, numeric_cols_names], use = "complete.obs")
    corrplot(corr_matrix, method = "color", type = "upper", 
             order = "hclust", tl.cex = 0.8, tl.col = "black")
    dev.off()
  }
  
  # 3. Pair plot for key variables
  key_vars <- c("Incidence_Rate", "Annual_Count", "Trend_5yr")
  key_vars <- key_vars[key_vars %in% colnames(df_clean)]
  if (length(key_vars) >= 2) {
    png("eda_pairplot.png", width = 1500, height = 1200, res = 300)
    pairs(df_clean[, key_vars], main = "Pair Plot of Key Variables")
    dev.off()
  }
  
  # 4. Trend analysis
  if ("Trend" %in% colnames(df_clean)) {
    png("eda_trend_analysis.png", width = 1500, height = 500, res = 300)
    
    p1 <- ggplot(df_clean, aes(x = Trend)) +
      geom_bar(fill = "steelblue", alpha = 0.7) +
      labs(title = "Count of Counties by Trend", x = "Trend", y = "Count") +
      theme_minimal() +
      theme(axis.text.x = element_text(angle = 45, hjust = 1))
    
    if ("Incidence_Rate" %in% colnames(df_clean)) {
      p2 <- ggplot(df_clean, aes(x = Trend, y = Incidence_Rate)) +
        geom_boxplot(fill = "steelblue", alpha = 0.7) +
        labs(title = "Incidence Rate by Trend", x = "Trend", y = "Incidence Rate") +
        theme_minimal() +
        theme(axis.text.x = element_text(angle = 45, hjust = 1))
      
      grid.arrange(p1, p2, ncol = 2)
    } else {
      print(p1)
    }
    dev.off()
  }
}

# Main execution
if (!interactive()) {
  df <- load_data()
  df_clean <- clean_data(df)
  df_enhanced <- comprehensive_eda(df_clean)
}

