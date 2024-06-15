# Machine Learning Analysis Module
# R script for machine learning analysis

library(caret)
library(randomForest)
library(xgboost)
library(glmnet)
library(Metrics)
library(dplyr)
source("data_loader.R")

# Function to prepare ML data
# Prepare data for machine learning
# Parameters: df_clean - cleaned dataset, target - target variable name
prepare_ml_data <- function(df_clean, target = "Incidence_Rate") {
  # Select features
  feature_cols <- c("CI_Lower", "CI_Upper", "Annual_Count", "Trend_5yr", "FIPS")
  feature_cols <- feature_cols[feature_cols %in% colnames(df_clean)]
  
  # Handle categorical variables
  if ("Trend" %in% colnames(df_clean)) {
    df_clean$Trend_encoded <- as.numeric(as.factor(df_clean$Trend))
    feature_cols <- c(feature_cols, "Trend_encoded")
  }
  
  # Create feature matrix and target vector
  X <- df_clean[, feature_cols, drop = FALSE]
  y <- df_clean[[target]]
  
  # Remove rows with missing values
  complete_cases <- complete.cases(X, y)
  X <- X[complete_cases, , drop = FALSE]
  y <- y[complete_cases]
  
  # Split data
  set.seed(42)
  train_index <- createDataPartition(y, p = 0.8, list = FALSE)
  X_train <- X[train_index, , drop = FALSE]
  X_test <- X[-train_index, , drop = FALSE]
  y_train <- y[train_index]
  y_test <- y[-train_index]
  
  # Scale features
  preProc <- preProcess(X_train, method = c("center", "scale"))
  X_train_scaled <- predict(preProc, X_train)
  X_test_scaled <- predict(preProc, X_test)
  
  return(list(
    X_train = X_train_scaled,
    X_test = X_test_scaled,
    y_train = y_train,
    y_test = y_test,
    preProc = preProc,
    feature_cols = feature_cols
  ))
}

# Function to train and evaluate models
# Train and evaluate multiple ML models
# Parameters: X_train/X_test - training/test features, y_train/y_test - training/test targets
train_and_evaluate_models <- function(X_train, X_test, y_train, y_test) {
  models <- list()
  results <- data.frame()
  
  cat("=== MACHINE LEARNING MODEL EVALUATION ===\n\n")
  
  # Linear Regression
  cat("Training Linear Regression...\n")
  lm_model <- lm(y_train ~ ., data = data.frame(X_train, y_train = y_train))
  lm_pred_train <- predict(lm_model, newdata = data.frame(X_train))
  lm_pred_test <- predict(lm_model, newdata = data.frame(X_test))
  
  results <- rbind(results, data.frame(
    Model = "Linear Regression",
    Train_RMSE = rmse(y_train, lm_pred_train),
    Test_RMSE = rmse(y_test, lm_pred_test),
    Train_MAE = mae(y_train, lm_pred_train),
    Test_MAE = mae(y_test, lm_pred_test),
    Train_R2 = R2(lm_pred_train, y_train),
    Test_R2 = R2(lm_pred_test, y_test)
  ))
  models[["Linear Regression"]] <- lm_model
  
  # Ridge Regression
  cat("Training Ridge Regression...\n")
  ridge_model <- train(
    x = X_train, y = y_train,
    method = "ridge",
    trControl = trainControl(method = "cv", number = 5),
    tuneGrid = expand.grid(lambda = seq(0.001, 1, length = 10))
  )
  ridge_pred_train <- predict(ridge_model, newdata = X_train)
  ridge_pred_test <- predict(ridge_model, newdata = X_test)
  
  results <- rbind(results, data.frame(
    Model = "Ridge Regression",
    Train_RMSE = rmse(y_train, ridge_pred_train),
    Test_RMSE = rmse(y_test, ridge_pred_test),
    Train_MAE = mae(y_train, ridge_pred_train),
    Test_MAE = mae(y_test, ridge_pred_test),
    Train_R2 = R2(ridge_pred_train, y_train),
    Test_R2 = R2(ridge_pred_test, y_test)
  ))
  models[["Ridge Regression"]] <- ridge_model
  
  # Lasso Regression
  cat("Training Lasso Regression...\n")
  lasso_model <- train(
    x = X_train, y = y_train,
    method = "lasso",
    trControl = trainControl(method = "cv", number = 5),
    tuneGrid = expand.grid(fraction = seq(0.1, 1, length = 10))
  )
  lasso_pred_train <- predict(lasso_model, newdata = X_train)
  lasso_pred_test <- predict(lasso_model, newdata = X_test)
  
  results <- rbind(results, data.frame(
    Model = "Lasso Regression",
    Train_RMSE = rmse(y_train, lasso_pred_train),
    Test_RMSE = rmse(y_test, lasso_pred_test),
    Train_MAE = mae(y_train, lasso_pred_train),
    Test_MAE = mae(y_test, lasso_pred_test),
    Train_R2 = R2(lasso_pred_train, y_train),
    Test_R2 = R2(lasso_pred_test, y_test)
  ))
  models[["Lasso Regression"]] <- lasso_model
  
  # Random Forest
  cat("Training Random Forest...\n")
  rf_model <- randomForest(
    x = X_train, y = y_train,
    ntree = 100, mtry = sqrt(ncol(X_train)),
    importance = TRUE
  )
  rf_pred_train <- predict(rf_model, newdata = X_train)
  rf_pred_test <- predict(rf_model, newdata = X_test)
  
  results <- rbind(results, data.frame(
    Model = "Random Forest",
    Train_RMSE = rmse(y_train, rf_pred_train),
    Test_RMSE = rmse(y_test, rf_pred_test),
    Train_MAE = mae(y_train, rf_pred_train),
    Test_MAE = mae(y_test, rf_pred_test),
    Train_R2 = R2(rf_pred_train, y_train),
    Test_R2 = R2(rf_pred_test, y_test)
  ))
  models[["Random Forest"]] <- rf_model
  
  # Gradient Boosting
  cat("Training Gradient Boosting...\n")
  gbm_model <- train(
    x = X_train, y = y_train,
    method = "gbm",
    trControl = trainControl(method = "cv", number = 5),
    verbose = FALSE
  )
  gbm_pred_train <- predict(gbm_model, newdata = X_train)
  gbm_pred_test <- predict(gbm_model, newdata = X_test)
  
  results <- rbind(results, data.frame(
    Model = "Gradient Boosting",
    Train_RMSE = rmse(y_train, gbm_pred_train),
    Test_RMSE = rmse(y_test, gbm_pred_test),
    Train_MAE = mae(y_train, gbm_pred_train),
    Test_MAE = mae(y_test, gbm_pred_test),
    Train_R2 = R2(gbm_pred_train, y_train),
    Test_R2 = R2(gbm_pred_test, y_test)
  ))
  models[["Gradient Boosting"]] <- gbm_model
  
  # Print results
  print(results)
  
  return(list(
    models = models,
    results = results
  ))
}

# Function to plot model comparison
# Plot model comparison
plot_model_comparison <- function(results) {
  library(ggplot2)
  library(gridExtra)
  
  p1 <- ggplot(results, aes(x = reorder(Model, Test_R2), y = Test_R2)) +
    geom_bar(stat = "identity", fill = "steelblue", alpha = 0.7) +
    coord_flip() +
    labs(title = "Model Comparison: R² Score", x = "Model", y = "R² Score") +
    theme_minimal()
  
  p2 <- ggplot(results, aes(x = reorder(Model, -Test_RMSE), y = Test_RMSE)) +
    geom_bar(stat = "identity", fill = "steelblue", alpha = 0.7) +
    coord_flip() +
    labs(title = "Model Comparison: RMSE", x = "Model", y = "RMSE") +
    theme_minimal()
  
  png("ml_model_comparison.png", width = 1500, height = 600, res = 300)
  grid.arrange(p1, p2, ncol = 2)
  dev.off()
}

# Function for feature importance analysis
# Analyze feature importance
feature_importance_analysis <- function(model, feature_names) {
  if (class(model)[1] == "randomForest") {
    importance <- importance(model)
    importance_df <- data.frame(
      Feature = rownames(importance),
      Importance = importance[, "%IncMSE"]
    )
  } else if (class(model)[1] == "train" && model$method == "gbm") {
    importance <- varImp(model)
    importance_df <- data.frame(
      Feature = rownames(importance$importance),
      Importance = importance$importance$Overall
    )
  } else {
    cat("Model does not support feature importance\n")
    return(NULL)
  }
  
  importance_df <- importance_df[order(-importance_df$Importance), ]
  
  # Plot
  png("ml_feature_importance.png", width = 1000, height = 600, res = 300)
  ggplot(importance_df, aes(x = reorder(Feature, Importance), y = Importance)) +
    geom_bar(stat = "identity", fill = "steelblue", alpha = 0.7) +
    coord_flip() +
    labs(title = "Feature Importance", x = "Feature", y = "Importance") +
    theme_minimal()
  dev.off()
  
  return(importance_df)
}

# Main execution
if (!interactive()) {
  # Load and prepare data
  df <- load_data()
  df_clean <- clean_data(df)
  
  ml_data <- prepare_ml_data(df_clean)
  
  cat("Training set size:", nrow(ml_data$X_train), "\n")
  cat("Test set size:", nrow(ml_data$X_test), "\n")
  cat("Features:", ml_data$feature_cols, "\n\n")
  
  # Train and evaluate models
  results_list <- train_and_evaluate_models(
    ml_data$X_train, ml_data$X_test,
    ml_data$y_train, ml_data$y_test
  )
  
  # Plot comparison
  plot_model_comparison(results_list$results)
  
  # Feature importance for best model
  best_model_name <- results_list$results$Model[which.max(results_list$results$Test_R2)]
  best_model <- results_list$models[[best_model_name]]
  cat("\nBest Model:", best_model_name, "\n")
  importance_df <- feature_importance_analysis(best_model, ml_data$feature_cols)
  if (!is.null(importance_df)) {
    cat("\nFeature Importance:\n")
    print(importance_df)
  }
}

