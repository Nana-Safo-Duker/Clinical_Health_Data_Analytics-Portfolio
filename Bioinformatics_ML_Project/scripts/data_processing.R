# Data Processing Module in R
# Functions for loading, cleaning, and preprocessing clinical data

# Load required libraries
library(tidyverse)
library(caret)
library(mice)      # For missing value imputation
library(scales)    # For data scaling

# =============================================================================
# FUNCTION: Load Clinical Data
# =============================================================================
load_clinical_data <- function(filepath) {
  #' Load clinical data from CSV file
  #'
  #' @param filepath Path to the CSV file
  #' @return Dataframe with clinical data
  #' @examples
  #' df <- load_clinical_data('data/raw/clinical_data.csv')
  
  tryCatch({
    df <- read.csv(filepath, stringsAsFactors = FALSE)
    cat(sprintf("✓ Data loaded successfully: %d rows, %d columns\n", 
                nrow(df), ncol(df)))
    return(df)
  }, error = function(e) {
    cat(sprintf("✗ Error loading data: %s\n", e$message))
    stop(e)
  })
}

# =============================================================================
# FUNCTION: Handle Missing Values
# =============================================================================
handle_missing_values <- function(df, method = "mean") {
  #' Handle missing values in the dataset
  #'
  #' @param df Input dataframe
  #' @param method Imputation method ('mean', 'median', 'mode', 'mice')
  #' @return Dataframe with imputed values
  #' @examples
  #' df_clean <- handle_missing_values(df, method = "median")
  
  cat("\n--- Handling Missing Values ---\n")
  
  # Check for missing values
  missing_count <- sum(is.na(df))
  if (missing_count == 0) {
    cat("✓ No missing values found\n")
    return(df)
  }
  
  cat(sprintf("Found %d missing values\n", missing_count))
  
  # Separate numeric and categorical columns
  numeric_cols <- names(df)[sapply(df, is.numeric)]
  categorical_cols <- names(df)[sapply(df, function(x) is.character(x) | is.factor(x))]
  
  if (method == "mice") {
    # Multiple Imputation by Chained Equations
    imputed <- mice(df, m = 5, method = 'pmm', seed = 42, printFlag = FALSE)
    df_imputed <- complete(imputed, 1)
  } else {
    df_imputed <- df
    
    # Impute numeric columns
    for (col in numeric_cols) {
      if (any(is.na(df_imputed[[col]]))) {
        if (method == "mean") {
          df_imputed[[col]][is.na(df_imputed[[col]])] <- mean(df_imputed[[col]], na.rm = TRUE)
        } else if (method == "median") {
          df_imputed[[col]][is.na(df_imputed[[col]])] <- median(df_imputed[[col]], na.rm = TRUE)
        }
      }
    }
    
    # Impute categorical columns with mode
    for (col in categorical_cols) {
      if (any(is.na(df_imputed[[col]]))) {
        mode_val <- names(sort(table(df_imputed[[col]]), decreasing = TRUE))[1]
        df_imputed[[col]][is.na(df_imputed[[col]])] <- mode_val
      }
    }
  }
  
  cat(sprintf("✓ Imputed missing values using '%s' method\n", method))
  return(df_imputed)
}

# =============================================================================
# FUNCTION: Remove Outliers
# =============================================================================
remove_outliers <- function(df, columns, method = "iqr", threshold = 1.5) {
  #' Remove outliers from specified columns
  #'
  #' @param df Input dataframe
  #' @param columns Columns to check for outliers
  #' @param method Method for outlier detection ('iqr' or 'zscore')
  #' @param threshold Threshold for outlier detection
  #' @return List with cleaned dataframe and number of rows removed
  #' @examples
  #' result <- remove_outliers(df, c('age', 'glucose'), method = 'iqr')
  
  initial_rows <- nrow(df)
  df_clean <- df
  
  if (method == "iqr") {
    for (col in columns) {
      Q1 <- quantile(df_clean[[col]], 0.25, na.rm = TRUE)
      Q3 <- quantile(df_clean[[col]], 0.75, na.rm = TRUE)
      IQR <- Q3 - Q1
      lower_bound <- Q1 - threshold * IQR
      upper_bound <- Q3 + threshold * IQR
      
      df_clean <- df_clean[df_clean[[col]] >= lower_bound & 
                           df_clean[[col]] <= upper_bound, ]
    }
  } else if (method == "zscore") {
    for (col in columns) {
      z_scores <- abs(scale(df_clean[[col]]))
      df_clean <- df_clean[z_scores < threshold, ]
    }
  }
  
  removed <- initial_rows - nrow(df_clean)
  cat(sprintf("✓ Removed %d outlier rows (%.2f%%)\n", 
              removed, removed/initial_rows*100))
  
  return(list(data = df_clean, removed = removed))
}

# =============================================================================
# FUNCTION: Scale Features
# =============================================================================
scale_features <- function(X, method = "standard") {
  #' Scale numerical features
  #'
  #' @param X Feature matrix or dataframe
  #' @param method Scaling method ('standard', 'minmax', 'robust')
  #' @return List with scaled data and scaler parameters
  #' @examples
  #' result <- scale_features(X_train, method = "standard")
  
  if (method == "standard") {
    # Z-score normalization
    means <- apply(X, 2, mean, na.rm = TRUE)
    sds <- apply(X, 2, sd, na.rm = TRUE)
    X_scaled <- scale(X, center = means, scale = sds)
    scaler <- list(means = means, sds = sds, method = "standard")
  } else if (method == "minmax") {
    # Min-Max scaling to [0, 1]
    mins <- apply(X, 2, min, na.rm = TRUE)
    maxs <- apply(X, 2, max, na.rm = TRUE)
    X_scaled <- as.data.frame(lapply(1:ncol(X), function(i) {
      (X[, i] - mins[i]) / (maxs[i] - mins[i])
    }))
    names(X_scaled) <- names(X)
    scaler <- list(mins = mins, maxs = maxs, method = "minmax")
  } else if (method == "robust") {
    # Robust scaling using median and IQR
    medians <- apply(X, 2, median, na.rm = TRUE)
    q1 <- apply(X, 2, quantile, probs = 0.25, na.rm = TRUE)
    q3 <- apply(X, 2, quantile, probs = 0.75, na.rm = TRUE)
    iqr <- q3 - q1
    X_scaled <- as.data.frame(lapply(1:ncol(X), function(i) {
      (X[, i] - medians[i]) / iqr[i]
    }))
    names(X_scaled) <- names(X)
    scaler <- list(medians = medians, iqr = iqr, method = "robust")
  } else {
    stop("Method must be 'standard', 'minmax', or 'robust'")
  }
  
  cat(sprintf("✓ Features scaled using '%s' method\n", method))
  return(list(data = X_scaled, scaler = scaler))
}

# =============================================================================
# FUNCTION: Preprocess Data (Complete Pipeline)
# =============================================================================
preprocess_data <- function(df, target_column = "diagnosis", test_size = 0.2,
                           random_seed = 42, scale = TRUE, 
                           handle_outliers = FALSE) {
  #' Complete preprocessing pipeline for clinical data
  #'
  #' @param df Input dataframe
  #' @param target_column Name of the target column
  #' @param test_size Proportion of data for testing
  #' @param random_seed Random seed for reproducibility
  #' @param scale Whether to scale features
  #' @param handle_outliers Whether to remove outliers
  #' @return List with train/test splits and scaler
  #' @examples
  #' result <- preprocess_data(df, target_column = "diagnosis")
  
  cat("=============================================================\n")
  cat("PREPROCESSING PIPELINE\n")
  cat("=============================================================\n")
  
  set.seed(random_seed)
  df_processed <- df
  
  # Remove ID columns
  id_cols <- c("patient_id", "id", "ID")
  id_cols_present <- intersect(id_cols, names(df_processed))
  if (length(id_cols_present) > 0) {
    df_processed <- df_processed[, !(names(df_processed) %in% id_cols_present)]
    cat(sprintf("✓ Removed ID columns: %s\n", paste(id_cols_present, collapse = ", ")))
  }
  
  # Handle missing values
  if (sum(is.na(df_processed)) > 0) {
    df_processed <- handle_missing_values(df_processed, method = "median")
  }
  
  # Encode categorical features (except target)
  categorical_cols <- names(df_processed)[sapply(df_processed, function(x) 
    is.character(x) | is.factor(x))]
  categorical_cols <- setdiff(categorical_cols, target_column)
  
  if (length(categorical_cols) > 0) {
    # One-hot encoding
    dummies <- dummyVars(~ ., data = df_processed[, categorical_cols, drop = FALSE])
    encoded <- predict(dummies, newdata = df_processed)
    df_processed <- cbind(df_processed[, !(names(df_processed) %in% categorical_cols)], 
                          encoded)
    cat(sprintf("✓ Encoded %d categorical columns\n", length(categorical_cols)))
  }
  
  # Separate features and target
  if (!(target_column %in% names(df_processed))) {
    stop(sprintf("Target column '%s' not found in dataframe", target_column))
  }
  
  X <- df_processed[, !(names(df_processed) %in% target_column)]
  y <- df_processed[[target_column]]
  
  cat(sprintf("✓ Separated features (n=%d) and target\n", ncol(X)))
  
  # Handle outliers if requested
  if (handle_outliers) {
    numeric_cols <- names(X)[sapply(X, is.numeric)]
    combined <- cbind(X, diagnosis = y)
    outlier_result <- remove_outliers(combined, numeric_cols)
    combined <- outlier_result$data
    X <- combined[, !(names(combined) %in% "diagnosis")]
    y <- combined$diagnosis
  }
  
  # Split data
  n <- nrow(X)
  train_indices <- createDataPartition(y, p = 1 - test_size, list = FALSE)
  
  X_train <- X[train_indices, ]
  X_test <- X[-train_indices, ]
  y_train <- y[train_indices]
  y_test <- y[-train_indices]
  
  cat(sprintf("✓ Split data: Train=%d, Test=%d\n", 
              length(train_indices), nrow(X_test)))
  
  # Scale features
  scaler <- NULL
  if (scale) {
    scale_result <- scale_features(X_train, method = "standard")
    X_train <- scale_result$data
    scaler <- scale_result$scaler
    
    # Apply same scaling to test set
    if (scaler$method == "standard") {
      X_test <- scale(X_test, center = scaler$means, scale = scaler$sds)
    } else if (scaler$method == "minmax") {
      X_test <- as.data.frame(lapply(1:ncol(X_test), function(i) {
        (X_test[, i] - scaler$mins[i]) / (scaler$maxs[i] - scaler$mins[i])
      }))
      names(X_test) <- names(X_train)
    }
  }
  
  cat("=============================================================\n")
  cat("PREPROCESSING COMPLETE\n")
  cat("=============================================================\n")
  
  return(list(
    X_train = X_train,
    X_test = X_test,
    y_train = y_train,
    y_test = y_test,
    scaler = scaler
  ))
}

# =============================================================================
# FUNCTION: Generate Synthetic Data
# =============================================================================
generate_synthetic_data <- function(n_samples = 1000, random_seed = 42) {
  #' Generate synthetic clinical data for testing
  #'
  #' @param n_samples Number of samples to generate
  #' @param random_seed Random seed for reproducibility
  #' @return Dataframe with synthetic clinical data
  #' @examples
  #' df <- generate_synthetic_data(n_samples = 500)
  
  set.seed(random_seed)
  
  # Generate synthetic data
  df <- data.frame(
    patient_id = sprintf("PT%04d", 1:n_samples),
    age = sample(18:85, n_samples, replace = TRUE),
    gender = sample(c("M", "F"), n_samples, replace = TRUE),
    bmi = rnorm(n_samples, mean = 27, sd = 5),
    blood_pressure_sys = rnorm(n_samples, mean = 130, sd = 20),
    blood_pressure_dia = rnorm(n_samples, mean = 85, sd = 12),
    glucose = rnorm(n_samples, mean = 100, sd = 25),
    cholesterol = rnorm(n_samples, mean = 200, sd = 40),
    heart_rate = rnorm(n_samples, mean = 75, sd = 10),
    biomarker_a = rgamma(n_samples, shape = 2, scale = 2),
    biomarker_b = rexp(n_samples, rate = 1/1.5),
    diagnosis = sample(c(0, 1), n_samples, replace = TRUE, prob = c(0.7, 0.3))
  )
  
  # Introduce missing values
  missing_indices <- sample(1:n_samples, size = floor(n_samples * 0.05))
  df$biomarker_a[missing_indices] <- NA
  
  cat(sprintf("✓ Generated synthetic data: %d rows, %d columns\n", 
              nrow(df), ncol(df)))
  
  return(df)
}

# =============================================================================
# MAIN EXECUTION (Example Usage)
# =============================================================================
if (interactive()) {
  cat("\n=============================================================\n")
  cat("Data Processing Module - Example Usage\n")
  cat("=============================================================\n\n")
  
  # Generate synthetic data
  df <- generate_synthetic_data(n_samples = 1000)
  cat(sprintf("\nDataset shape: %d rows, %d columns\n", nrow(df), ncol(df)))
  cat(sprintf("Missing values: %d\n", sum(is.na(df))))
  
  # Preprocess
  result <- preprocess_data(df, target_column = "diagnosis", scale = TRUE)
  
  cat("\nFinal shapes:\n")
  cat(sprintf("  X_train: %d rows, %d columns\n", 
              nrow(result$X_train), ncol(result$X_train)))
  cat(sprintf("  X_test: %d rows, %d columns\n", 
              nrow(result$X_test), ncol(result$X_test)))
  cat(sprintf("  y_train: %d observations\n", length(result$y_train)))
  cat(sprintf("  y_test: %d observations\n", length(result$y_test)))
}


