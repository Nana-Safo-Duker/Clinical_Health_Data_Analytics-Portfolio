#!/usr/bin/env Rscript
# Complete ML Pipeline Script in R
# This script runs the entire machine learning pipeline from data loading
# to model training and evaluation

# Load required libraries
suppressPackageStartupMessages({
  library(tidyverse)
  library(randomForest)
  library(e1071)
  library(gbm)
  library(caret)
  library(pROC)
  library(ggplot2)
  library(gridExtra)
})

# Source required scripts
script_dir <- dirname(sys.frame(1)$ofile)
source(file.path(script_dir, "data_processing.R"))
source(file.path(script_dir, "ml_models.R"))

# =============================================================================
# MAIN PIPELINE FUNCTION
# =============================================================================
run_pipeline <- function(data_path = NULL, n_samples = 1000, 
                        models = c("rf", "svm", "gbm"),
                        output_dir = "results") {
  #' Run complete ML pipeline
  #'
  #' @param data_path Path to data file (optional)
  #' @param n_samples Number of synthetic samples if no data provided
  #' @param models Models to train (c("rf", "svm", "gbm", "nn"))
  #' @param output_dir Output directory for results
  
  cat("================================================================================\n")
  cat("MACHINE LEARNING PIPELINE FOR CLINICAL DIAGNOSIS\n")
  cat("================================================================================\n\n")
  
  # ============================================================
  # STEP 1: DATA LOADING
  # ============================================================
  cat("================================================================================\n")
  cat("STEP 1: DATA LOADING\n")
  cat("================================================================================\n\n")
  
  if (!is.null(data_path)) {
    df <- load_clinical_data(data_path)
  } else {
    cat(sprintf("Generating synthetic data with %d samples...\n", n_samples))
    df <- generate_synthetic_data(n_samples = n_samples)
  }
  
  cat(sprintf("Dataset shape: %d rows, %d columns\n", nrow(df), ncol(df)))
  
  # ============================================================
  # STEP 2: DATA PREPROCESSING
  # ============================================================
  cat("\n================================================================================\n")
  cat("STEP 2: DATA PREPROCESSING\n")
  cat("================================================================================\n\n")
  
  result <- preprocess_data(
    df,
    target_column = "diagnosis",
    test_size = 0.2,
    scale = TRUE
  )
  
  X_train <- result$X_train
  X_test <- result$X_test
  y_train <- result$y_train
  y_test <- result$y_test
  scaler <- result$scaler
  
  # ============================================================
  # STEP 3: MODEL TRAINING
  # ============================================================
  cat("\n================================================================================\n")
  cat("STEP 3: MODEL TRAINING\n")
  cat("================================================================================\n")
  
  trained_models <- list()
  
  if ("rf" %in% models) {
    cat("\n--- Training Random Forest ---\n")
    trained_models$RandomForest <- train_random_forest(
      X_train, y_train,
      ntree = 100
    )
  }
  
  if ("svm" %in% models) {
    cat("\n--- Training SVM ---\n")
    trained_models$SVM <- train_svm(
      X_train, y_train,
      kernel = "radial",
      cost = 1.0
    )
  }
  
  if ("gbm" %in% models) {
    cat("\n--- Training Gradient Boosting ---\n")
    trained_models$GradientBoosting <- train_gradient_boosting(
      X_train, y_train,
      n_trees = 100
    )
  }
  
  if ("nn" %in% models) {
    cat("\n--- Training Neural Network ---\n")
    trained_models$NeuralNetwork <- train_neural_network(
      X_train, y_train,
      size = c(100, 50)
    )
  }
  
  # ============================================================
  # STEP 4: MODEL EVALUATION
  # ============================================================
  cat("\n================================================================================\n")
  cat("STEP 4: MODEL EVALUATION\n")
  cat("================================================================================\n\n")
  
  evaluation_results <- list()
  
  for (model_name in names(trained_models)) {
    cat(sprintf("\n=== Evaluating %s ===\n", model_name))
    model <- trained_models[[model_name]]
    
    # Make predictions
    if (inherits(model, "gbm")) {
      y_pred_prob <- predict(model, newdata = X_test, 
                            n.trees = 100, type = "response")
      y_pred <- ifelse(y_pred_prob > 0.5, 1, 0)
    } else if (inherits(model, "svm")) {
      y_pred <- predict(model, X_test)
      y_pred_prob <- attr(predict(model, X_test, probability = TRUE), 
                         "probabilities")[, "1"]
    } else {
      y_pred <- predict(model, X_test)
      y_pred_prob <- predict(model, X_test, type = "prob")[, 2]
    }
    
    # Calculate metrics
    y_test_numeric <- as.numeric(as.character(y_test))
    y_pred_numeric <- as.numeric(as.character(y_pred))
    
    accuracy <- mean(y_pred_numeric == y_test_numeric)
    
    # Confusion matrix
    cm <- table(Actual = y_test_numeric, Predicted = y_pred_numeric)
    
    if (nrow(cm) == 2 && ncol(cm) == 2) {
      precision <- cm[2, 2] / sum(cm[, 2])
      recall <- cm[2, 2] / sum(cm[2, ])
      f1_score <- 2 * (precision * recall) / (precision + recall)
      
      # ROC-AUC
      roc_obj <- roc(y_test_numeric, y_pred_prob, quiet = TRUE)
      auc_score <- auc(roc_obj)
    } else {
      precision <- recall <- f1_score <- auc_score <- NA
    }
    
    # Store results
    evaluation_results[[model_name]] <- list(
      accuracy = accuracy,
      precision = precision,
      recall = recall,
      f1_score = f1_score,
      auc = auc_score,
      confusion_matrix = cm,
      predictions = y_pred,
      probabilities = y_pred_prob,
      roc = roc_obj
    )
    
    # Print results
    cat("\nPerformance Metrics:\n")
    cat("------------------------------------------------------------\n")
    cat(sprintf("  Accuracy          : %.4f\n", accuracy))
    cat(sprintf("  Precision         : %.4f\n", precision))
    cat(sprintf("  Recall            : %.4f\n", recall))
    cat(sprintf("  F1-Score          : %.4f\n", f1_score))
    cat(sprintf("  ROC-AUC           : %.4f\n", auc_score))
    
    cat("\nConfusion Matrix:\n")
    cat("------------------------------------------------------------\n")
    print(cm)
    
    # Cross-validation
    cat("\n--- Cross-Validation ---\n")
    model_type <- tolower(substr(model_name, 1, 3))
    if (model_type == "ran") model_type <- "rf"
    if (model_type == "gra") model_type <- "gbm"
    
    cv_results <- cross_validate_model(X_train, y_train, 
                                       model_type = model_type, k = 5)
  }
  
  # ============================================================
  # STEP 5: MODEL COMPARISON
  # ============================================================
  if (length(trained_models) > 1) {
    cat("\n================================================================================\n")
    cat("STEP 5: MODEL COMPARISON\n")
    cat("================================================================================\n\n")
    
    comparison_df <- data.frame(
      Model = names(evaluation_results),
      Accuracy = sapply(evaluation_results, function(x) x$accuracy),
      Precision = sapply(evaluation_results, function(x) x$precision),
      Recall = sapply(evaluation_results, function(x) x$recall),
      F1_Score = sapply(evaluation_results, function(x) x$f1_score),
      AUC = sapply(evaluation_results, function(x) x$auc)
    )
    
    comparison_df <- comparison_df[order(-comparison_df$F1_Score), ]
    
    cat("Model Comparison Results:\n")
    cat("================================================================================\n")
    print(comparison_df, row.names = FALSE, digits = 4)
    cat("================================================================================\n")
  }
  
  # ============================================================
  # STEP 6: VISUALIZATION
  # ============================================================
  cat("\n================================================================================\n")
  cat("STEP 6: VISUALIZATION\n")
  cat("================================================================================\n\n")
  
  # Create output directories
  dir.create(file.path(output_dir, "figures"), recursive = TRUE, showWarnings = FALSE)
  dir.create(file.path(output_dir, "models"), recursive = TRUE, showWarnings = FALSE)
  
  # Plot ROC curves
  cat("Generating ROC curve plot...\n")
  
  png(file.path(output_dir, "figures", "roc_curves.png"), 
      width = 800, height = 600, res = 100)
  
  plot(0, 0, type = "n", xlim = c(0, 1), ylim = c(0, 1),
       xlab = "False Positive Rate", ylab = "True Positive Rate",
       main = "ROC Curves Comparison")
  abline(0, 1, lty = 2, col = "gray")
  
  colors <- rainbow(length(evaluation_results))
  for (i in seq_along(evaluation_results)) {
    model_name <- names(evaluation_results)[i]
    roc_obj <- evaluation_results[[model_name]]$roc
    lines(roc_obj$specificities, roc_obj$sensitivities, 
          col = colors[i], lwd = 2)
  }
  
  legend("bottomright", 
         legend = sprintf("%s (AUC=%.3f)", 
                         names(evaluation_results),
                         sapply(evaluation_results, function(x) x$auc)),
         col = colors, lwd = 2)
  
  dev.off()
  cat("✓ ROC curves saved\n")
  
  # Plot feature importance (for first model if available)
  first_model <- trained_models[[1]]
  if (inherits(first_model, "randomForest") || inherits(first_model, "gbm")) {
    cat("Generating feature importance plot...\n")
    
    feature_names <- c('age', 'bmi', 'blood_pressure_sys', 'blood_pressure_dia',
                       'glucose', 'cholesterol', 'heart_rate', 
                       'biomarker_a', 'biomarker_b')
    
    importance_df <- get_feature_importance(first_model, feature_names, top_n = 9)
    
    png(file.path(output_dir, "figures", "feature_importance.png"),
        width = 800, height = 600, res = 100)
    
    par(mar = c(5, 10, 4, 2))
    barplot(rev(importance_df$Importance[1:9]), 
            names.arg = rev(importance_df$Feature[1:9]),
            horiz = TRUE, las = 1,
            col = rainbow(9),
            main = "Top 9 Feature Importances",
            xlab = "Importance")
    
    dev.off()
    cat("✓ Feature importance plot saved\n")
  }
  
  # ============================================================
  # STEP 7: SAVE MODELS
  # ============================================================
  cat("\n================================================================================\n")
  cat("STEP 7: SAVING MODELS\n")
  cat("================================================================================\n\n")
  
  for (model_name in names(trained_models)) {
    model_filename <- file.path(output_dir, "models", 
                                sprintf("%s_model.rds", 
                                       tolower(gsub(" ", "_", model_name))))
    save_model(trained_models[[model_name]], model_filename)
  }
  
  # Save scaler
  scaler_path <- file.path(output_dir, "models", "scaler.rds")
  saveRDS(scaler, scaler_path)
  cat(sprintf("✓ Scaler saved to %s\n", scaler_path))
  
  # ============================================================
  # FINAL SUMMARY
  # ============================================================
  cat("\n================================================================================\n")
  cat("PIPELINE COMPLETE!\n")
  cat("================================================================================\n\n")
  cat(sprintf("✓ Trained %d model(s)\n", length(trained_models)))
  cat(sprintf("✓ Results saved to %s/\n", output_dir))
  cat(sprintf("✓ Models saved to %s/models/\n", output_dir))
  cat(sprintf("✓ Figures saved to %s/figures/\n", output_dir))
  cat("\n================================================================================\n")
  
  return(list(
    models = trained_models,
    evaluations = evaluation_results,
    comparison = if(length(trained_models) > 1) comparison_df else NULL
  ))
}

# =============================================================================
# COMMAND LINE EXECUTION
# =============================================================================
if (!interactive()) {
  # Parse command line arguments
  args <- commandArgs(trailingOnly = TRUE)
  
  # Default values
  n_samples <- 1000
  models_to_train <- c("rf", "svm", "gbm")
  output_dir <- "results"
  
  # Run pipeline
  results <- run_pipeline(
    data_path = NULL,
    n_samples = n_samples,
    models = models_to_train,
    output_dir = output_dir
  )
}

# =============================================================================
# INTERACTIVE USAGE
# =============================================================================
if (interactive()) {
  cat("\n=============================================================\n")
  cat("ML Pipeline Script - Example Usage\n")
  cat("=============================================================\n\n")
  cat("To run the pipeline:\n")
  cat("  results <- run_pipeline(n_samples = 1000, models = c('rf', 'svm'))\n\n")
  cat("To run from command line:\n")
  cat("  Rscript run_pipeline.R\n\n")
}


