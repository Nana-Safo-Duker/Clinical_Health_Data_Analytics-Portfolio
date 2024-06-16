# Data Loading and Preprocessing Module
# R script for loading and cleaning cancer incidence data

# Load required libraries
library(readr)
library(dplyr)
library(tidyr)

# Function to load data
# Load the cancer incidence dataset
# Parameters: file_path - Path to the CSV file
# Returns: data.frame with loaded dataset
load_data <- function(file_path = "../data/incd.csv") {
  # Try reading with different encodings
  tryCatch({
    df <- read_csv(file_path, locale = locale(encoding = "UTF-8"))
  }, error = function(e) {
    df <- read_csv(file_path, locale = locale(encoding = "Latin1"))
  })
  
  return(df)
}

# Function to clean data
# Clean and preprocess the dataset
# Parameters: df - Raw dataset
# Returns: data.frame with cleaned dataset
clean_data <- function(df) {
  # Clean column names
  colnames(df) <- gsub(" ", "_", colnames(df))
  colnames(df) <- gsub("\\(", "", colnames(df))
  colnames(df) <- gsub("\\)", "", colnames(df))
  colnames(df) <- gsub("-", "_", colnames(df))
  colnames(df) <- gsub("%", "pct", colnames(df))
  
  # Rename columns for easier access
  colnames(df) <- gsub("Age_Adjusted_Incidence_Rate.*cases_per_100,000", "Incidence_Rate", colnames(df))
  colnames(df) <- gsub("Lower_95pct_Confidence_Interval$", "CI_Lower", colnames(df))
  colnames(df) <- gsub("Upper_95pct_Confidence_Interval$", "CI_Upper", colnames(df))
  colnames(df) <- gsub("Average_Annual_Count", "Annual_Count", colnames(df))
  colnames(df) <- gsub("Recent_Trend", "Trend", colnames(df))
  colnames(df) <- gsub("Recent_5_Year_Trend.*in_Incidence_Rates", "Trend_5yr", colnames(df))
  
  # Convert numeric columns
  numeric_cols <- c("Incidence_Rate", "CI_Lower", "CI_Upper", "Annual_Count", 
                    "Trend_5yr", "FIPS")
  
  for (col in numeric_cols) {
    if (col %in% colnames(df)) {
      df[[col]] <- as.numeric(df[[col]])
    }
  }
  
  # Remove rows with missing key variables
  df_clean <- df %>% filter(!is.na(Incidence_Rate))
  
  return(df_clean)
}

# Main execution
if (!interactive()) {
  df <- load_data()
  df_clean <- clean_data(df)
  cat("Dataset loaded:", dim(df_clean), "\n")
  cat("Columns:", colnames(df_clean), "\n")
}

