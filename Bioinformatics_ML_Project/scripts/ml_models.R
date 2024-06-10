# Machine Learning Models Module in R
# Implementations of various ML algorithms for clinical diagnosis

# Load required libraries
library(randomForest)
library(e1071)        # For SVM
library(gbm)          # For Gradient Boosting
library(nnet)         # For Neural Networks
library(caret)
library(pROC)

# =============================================================================
# FUNCTION: Train Random Forest
# =============================================================================
train_random_forest <- function(X_train, y_train, ntree = 100, 
                               mtry = NULL, ...) {
  #' Train a Random Forest classifier
  #'
  #' @param X_train Training features
  #' @param y_train Training labels
  #' @param ntree Number of trees
  #' @param mtry Number of variables to try at each split
  #' @return Trained Random Forest model
  #' @examples
  #' model <- train_random_forest(X_train, y_train, ntree = 100)
  
  cat("\n--- Training Random Forest ---\n")
  cat(sprintf("Parameters: ntree=%d\n", ntree))
  
  # Convert to factor for classification
  y_train <- as.factor(y_train)
  
  # Default mtry if not specified
  if (is.null(mtry)) {
    mtry <- floor(sqrt(ncol(X_train)))
  }
  
  # Train model
  model <- randomForest(
    x = X_train,
    y = y_train,
    ntree = ntree,
    mtry = mtry,
    importance = TRUE,
    ...
  )
  
  # Calculate training accuracy
  train_pred <- predict(model, X_train)
  train_accuracy <- mean(train_pred == y_train)
  
  cat("✓ Random Forest trained successfully\n")
  cat(sprintf("  Training accuracy: %.4f\n", train_accuracy))
  cat(sprintf("  Out-of-bag error: %.4f\n", model$err.rate[ntree, "OOB"]))
  
  return(model)
}

# =============================================================================
# FUNCTION: Train SVM
# =============================================================================
train_svm <- function(X_train, y_train, kernel = "radial", 
                     cost = 1, ...) {
  #' Train a Support Vector Machine classifier
  #'
  #' @param X_train Training features
  #' @param y_train Training labels
  #' @param kernel Kernel type ('linear', 'polynomial', 'radial', 'sigmoid')
  #' @param cost Cost parameter
  #' @return Trained SVM model
  #' @examples
  #' model <- train_svm(X_train, y_train, kernel = "radial")
  
  cat("\n--- Training SVM ---\n")
  cat(sprintf("Parameters: kernel=%s, cost=%.2f\n", kernel, cost))
  
  # Convert to factor
  y_train <- as.factor(y_train)
  
  # Train model
  model <- svm(
    x = X_train,
    y = y_train,
    kernel = kernel,
    cost = cost,
    probability = TRUE,
    ...
  )
  
  # Calculate training accuracy
  train_pred <- predict(model, X_train)
  train_accuracy <- mean(train_pred == y_train)
  
  cat("✓ SVM trained successfully\n")
  cat(sprintf("  Training accuracy: %.4f\n", train_accuracy))
  cat(sprintf("  Number of support vectors: %d\n", model$tot.nSV))
  
  return(model)
}

# =============================================================================
# FUNCTION: Train Gradient Boosting
# =============================================================================
train_gradient_boosting <- function(X_train, y_train, n_trees = 100,
                                   interaction_depth = 3, 
                                   shrinkage = 0.1, ...) {
  #' Train a Gradient Boosting classifier
  #'
  #' @param X_train Training features
  #' @param y_train Training labels
  #' @param n_trees Number of boosting iterations
  #' @param interaction_depth Maximum depth of trees
  #' @param shrinkage Learning rate
  #' @return Trained Gradient Boosting model
  #' @examples
  #' model <- train_gradient_boosting(X_train, y_train, n_trees = 100)
  
  cat("\n--- Training Gradient Boosting ---\n")
  cat(sprintf("Parameters: n.trees=%d, interaction.depth=%d, shrinkage=%.2f\n",
              n_trees, interaction_depth, shrinkage))
  
  # Prepare data
  train_data <- as.data.frame(X_train)
  train_data$diagnosis <- as.numeric(as.character(y_train))
  
  # Train model
  model <- gbm(
    diagnosis ~ .,
    data = train_data,
    distribution = "bernoulli",
    n.trees = n_trees,
    interaction.depth = interaction_depth,
    shrinkage = shrinkage,
    verbose = FALSE,
    ...
  )
  
  # Calculate training accuracy
  train_pred_prob <- predict(model, newdata = X_train, 
                              n.trees = n_trees, type = "response")
  train_pred <- ifelse(train_pred_prob > 0.5, 1, 0)
  train_accuracy <- mean(train_pred == as.numeric(as.character(y_train)))
  
  cat("✓ Gradient Boosting trained successfully\n")
  cat(sprintf("  Training accuracy: %.4f\n", train_accuracy))
  
  return(model)
}

# =============================================================================
# FUNCTION: Train Neural Network
# =============================================================================
train_neural_network <- function(X_train, y_train, size = c(10, 5),
                                maxit = 500, ...) {
  #' Train a Neural Network classifier
  #'
  #' @param X_train Training features
  #' @param y_train Training labels
  #' @param size Number of units in hidden layers
  #' @param maxit Maximum number of iterations
  #' @return Trained Neural Network model
  #' @examples
  #' model <- train_neural_network(X_train, y_train, size = c(10, 5))
  
  cat("\n--- Training Neural Network ---\n")
  cat(sprintf("Parameters: hidden layers=%s, maxit=%d\n",
              paste(size, collapse=", "), maxit))
  
  # Prepare data
  train_data <- as.data.frame(X_train)
  train_data$diagnosis <- as.factor(y_train)
  
  # Train model (single hidden layer with nnet)
  model <- nnet(
    diagnosis ~ .,
    data = train_data,
    size = size[1],
    maxit = maxit,
    trace = FALSE,
    ...
  )
  
  # Calculate training accuracy
  train_pred <- predict(model, X_train, type = "class")
  train_accuracy <- mean(train_pred == y_train)
  
  cat("✓ Neural Network trained successfully\n")
  cat(sprintf("  Training accuracy: %.4f\n", train_accuracy))
  
  return(model)
}

# =============================================================================
# FUNCTION: Cross-Validate Model
# =============================================================================
cross_validate_model <- function(X, y, model_type = "rf", k = 5, ...) {
  #' Perform k-fold cross-validation
  #'
  #' @param X Feature matrix
  #' @param y Labels
  #' @param model_type Type of model ('rf', 'svm', 'gbm')
  #' @param k Number of folds
  #' @return List with CV results
  #' @examples
  #' cv_results <- cross_validate_model(X_train, y_train, model_type = "rf", k = 5)
  
  cat(sprintf("\n--- Performing %d-fold Cross-Validation ---\n", k))
  
  set.seed(42)
  y <- as.factor(y)
  folds <- createFolds(y, k = k, list = TRUE, returnTrain = FALSE)
  
  accuracies <- numeric(k)
  
  for (i in 1:k) {
    # Split data
    test_idx <- folds[[i]]
    X_train_cv <- X[-test_idx, ]
    X_test_cv <- X[test_idx, ]
    y_train_cv <- y[-test_idx]
    y_test_cv <- y[test_idx]
    
    # Train model
    if (model_type == "rf") {
      model <- randomForest(x = X_train_cv, y = y_train_cv, ntree = 100)
    } else if (model_type == "svm") {
      model <- svm(x = X_train_cv, y = y_train_cv, kernel = "radial")
    } else if (model_type == "gbm") {
      train_data <- as.data.frame(X_train_cv)
      train_data$diagnosis <- as.numeric(as.character(y_train_cv))
      model <- gbm(diagnosis ~ ., data = train_data, 
                   distribution = "bernoulli", n.trees = 100, verbose = FALSE)
    }
    
    # Predict
    if (model_type == "gbm") {
      pred_prob <- predict(model, newdata = X_test_cv, 
                          n.trees = 100, type = "response")
      pred <- ifelse(pred_prob > 0.5, 1, 0)
    } else {
      pred <- predict(model, X_test_cv)
    }
    
    # Calculate accuracy
    accuracies[i] <- mean(pred == y_test_cv)
  }
  
  cat("✓ Cross-validation complete\n")
  cat(sprintf("  Mean accuracy: %.4f ± %.4f\n", 
              mean(accuracies), sd(accuracies)))
  cat(sprintf("  Individual scores: %s\n", 
              paste(sprintf("%.4f", accuracies), collapse = ", ")))
  
  return(list(
    mean = mean(accuracies),
    sd = sd(accuracies),
    scores = accuracies
  ))
}

# =============================================================================
# FUNCTION: Get Feature Importance
# =============================================================================
get_feature_importance <- function(model, feature_names = NULL, top_n = 10) {
  #' Extract and display feature importance
  #'
  #' @param model Trained model
  #' @param feature_names Names of features
  #' @param top_n Number of top features to display
  #' @return Dataframe with feature importances
  #' @examples
  #' importance <- get_feature_importance(model, feature_names, top_n = 10)
  
  if (inherits(model, "randomForest")) {
    importance_values <- importance(model)[, "MeanDecreaseGini"]
  } else if (inherits(model, "gbm")) {
    importance_values <- summary(model, plotit = FALSE)$rel.inf
    names(importance_values) <- summary(model, plotit = FALSE)$var
  } else {
    cat("✗ Model does not have feature importance\n")
    return(NULL)
  }
  
  if (is.null(feature_names)) {
    feature_names <- names(importance_values)
  }
  
  importance_df <- data.frame(
    Feature = feature_names,
    Importance = importance_values,
    stringsAsFactors = FALSE
  )
  
  importance_df <- importance_df[order(-importance_df$Importance), ]
  
  cat(sprintf("\nTop %d most important features:\n", top_n))
  cat("==================================================\n")
  print(head(importance_df, top_n), row.names = FALSE)
  
  return(importance_df)
}

# =============================================================================
# FUNCTION: Save Model
# =============================================================================
save_model <- function(model, filepath) {
  #' Save a trained model to disk
  #'
  #' @param model Trained model
  #' @param filepath Path to save the model
  #' @examples
  #' save_model(model, 'results/models/rf_model.rds')
  
  saveRDS(model, filepath)
  cat(sprintf("✓ Model saved to %s\n", filepath))
}

# =============================================================================
# FUNCTION: Load Model
# =============================================================================
load_model <- function(filepath) {
  #' Load a trained model from disk
  #'
  #' @param filepath Path to the saved model
  #' @return Loaded model
  #' @examples
  #' model <- load_model('results/models/rf_model.rds')
  
  model <- readRDS(filepath)
  cat(sprintf("✓ Model loaded from %s\n", filepath))
  return(model)
}

# =============================================================================
# MAIN EXECUTION (Example Usage)
# =============================================================================
if (interactive()) {
  cat("\n=============================================================\n")
  cat("Machine Learning Models Module - Example Usage\n")
  cat("=============================================================\n\n")
  
  # Source data processing
  source("data_processing.R")
  
  # Generate and preprocess data
  df <- generate_synthetic_data(n_samples = 1000)
  result <- preprocess_data(df)
  
  # Train Random Forest
  cat("\n" + paste(rep("=", 60), collapse="") + "\n")
  rf_model <- train_random_forest(result$X_train, result$y_train, ntree = 50)
  
  # Cross-validate
  rf_cv <- cross_validate_model(result$X_train, result$y_train, 
                                 model_type = "rf", k = 5)
  
  # Get feature importance
  feature_names <- c('age', 'bmi', 'blood_pressure_sys', 'blood_pressure_dia',
                     'glucose', 'cholesterol', 'heart_rate', 
                     'biomarker_a', 'biomarker_b')
  importance <- get_feature_importance(rf_model, feature_names, top_n = 5)
}


