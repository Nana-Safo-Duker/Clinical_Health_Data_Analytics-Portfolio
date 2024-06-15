# Machine Learning Analysis
# Breast Cancer Diagnosis Dataset
# Classification Problem: Malignant (M) vs Benign (B)

# Load required libraries
library(caret)
library(randomForest)
library(e1071)
library(xgboost)
library(glmnet)
library(rpart)
library(ranger)
library(pROC)
library(ggplot2)
library(dplyr)

# Load data
df <- read.csv("../../data/breast_cancer.csv", stringsAsFactors = FALSE)

# Prepare data
# Remove ID column
df <- df[, !names(df) %in% c("id")]

# Encode target variable
df$diagnosis <- as.factor(df$diagnosis)
levels(df$diagnosis) <- c("Benign", "Malignant")  # B=Benign, M=Malignant

# Get features
features <- setdiff(names(df), "diagnosis")
X <- df[, features]
y <- df$diagnosis

# Create results directory
dir.create("../../results/ml", showWarnings = FALSE, recursive = TRUE)

# ==============================================================================
# Data Splitting
# ==============================================================================
set.seed(42)
trainIndex <- createDataPartition(y, p = 0.8, list = FALSE)
X_train <- X[trainIndex, ]
X_test <- X[-trainIndex, ]
y_train <- y[trainIndex]
y_test <- y[-trainIndex]

cat("Training set size:", nrow(X_train), "\n")
cat("Test set size:", nrow(X_test), "\n")
cat("Number of features:", ncol(X_train), "\n\n")

# ==============================================================================
# Model Training and Evaluation
# ==============================================================================
cat("=" , rep("=", 79), "\n", sep = "")
cat("MACHINE LEARNING MODEL COMPARISON\n")
cat("=" , rep("=", 79), "\n", sep = "")

# Train control for cross-validation
train_control <- trainControl(
  method = "cv",
  number = 5,
  classProbs = TRUE,
  summaryFunction = twoClassSummary
)

# Define models to compare
models <- list()

# 1. Logistic Regression
cat("Training Logistic Regression...\n")
model_lr <- train(
  x = X_train, y = y_train,
  method = "glm",
  family = "binomial",
  trControl = train_control,
  metric = "ROC"
)
models[["Logistic Regression"]] <- model_lr

# 2. Decision Tree
cat("Training Decision Tree...\n")
model_dt <- train(
  x = X_train, y = y_train,
  method = "rpart",
  trControl = train_control,
  metric = "ROC"
)
models[["Decision Tree"]] <- model_dt

# 3. Random Forest
cat("Training Random Forest...\n")
model_rf <- train(
  x = X_train, y = y_train,
  method = "rf",
  trControl = train_control,
  metric = "ROC",
  ntree = 100
)
models[["Random Forest"]] <- model_rf

# 4. Support Vector Machine
cat("Training SVM...\n")
model_svm <- train(
  x = X_train, y = y_train,
  method = "svmRadial",
  trControl = train_control,
  metric = "ROC"
)
models[["SVM"]] <- model_svm

# 5. K-Nearest Neighbors
cat("Training KNN...\n")
model_knn <- train(
  x = X_train, y = y_train,
  method = "knn",
  trControl = train_control,
  metric = "ROC"
)
models[["KNN"]] <- model_knn

# 6. Naive Bayes
cat("Training Naive Bayes...\n")
model_nb <- train(
  x = X_train, y = y_train,
  method = "nb",
  trControl = train_control,
  metric = "ROC"
)
models[["Naive Bayes"]] <- model_nb

# 7. Gradient Boosting
cat("Training Gradient Boosting...\n")
model_gbm <- train(
  x = X_train, y = y_train,
  method = "gbm",
  trControl = train_control,
  metric = "ROC",
  verbose = FALSE
)
models[["Gradient Boosting"]] <- model_gbm

# ==============================================================================
# Model Evaluation
# ==============================================================================
results_list <- list()

for (model_name in names(models)) {
  cat("\nEvaluating", model_name, "...\n")
  
  model <- models[[model_name]]
  
  # Predictions
  pred_train <- predict(model, X_train)
  pred_test <- predict(model, X_test)
  pred_test_proba <- predict(model, X_test, type = "prob")
  
  # Metrics
  train_accuracy <- mean(pred_train == y_train)
  test_accuracy <- mean(pred_test == y_test)
  
  # Confusion matrix
  cm <- confusionMatrix(pred_test, y_test)
  
  # ROC AUC
  roc_auc <- tryCatch({
    roc_obj <- roc(y_test, pred_test_proba$Malignant)
    as.numeric(auc(roc_obj))
  }, error = function(e) NA)
  
  results_list[[model_name]] <- list(
    model = model,
    train_accuracy = train_accuracy,
    test_accuracy = test_accuracy,
    precision = cm$byClass["Precision"],
    recall = cm$byClass["Recall"],
    f1_score = cm$byClass["F1"],
    roc_auc = roc_auc,
    confusion_matrix = cm$table,
    predictions = pred_test,
    probabilities = pred_test_proba
  )
  
  cat("  Test Accuracy:", test_accuracy, "\n")
  cat("  Precision:", cm$byClass["Precision"], "\n")
  cat("  Recall:", cm$byClass["Recall"], "\n")
  cat("  F1 Score:", cm$byClass["F1"], "\n")
  if (!is.na(roc_auc)) {
    cat("  ROC AUC:", roc_auc, "\n")
  }
}

# ==============================================================================
# Model Comparison
# ==============================================================================
cat("\n", rep("=", 80), "\n", sep = "")
cat("MODEL COMPARISON RESULTS\n")
cat(rep("=", 80), "\n", sep = "")

comparison_df <- data.frame(
  Model = names(results_list),
  Test_Accuracy = sapply(results_list, function(x) x$test_accuracy),
  Precision = sapply(results_list, function(x) x$precision),
  Recall = sapply(results_list, function(x) x$recall),
  F1_Score = sapply(results_list, function(x) x$f1_score),
  ROC_AUC = sapply(results_list, function(x) x$roc_auc)
)

comparison_df <- comparison_df[order(comparison_df$Test_Accuracy, decreasing = TRUE), ]
print(comparison_df)

# Save comparison
write.csv(comparison_df, "../../results/ml/model_comparison.csv", row.names = FALSE)

# Visualization
png("../../results/ml/model_comparison_accuracy.png", width = 1200, height = 800)
comparison_df_sorted <- comparison_df[order(comparison_df$Test_Accuracy), ]
barplot(comparison_df_sorted$Test_Accuracy, 
       names.arg = comparison_df_sorted$Model,
       horiz = TRUE, las = 1,
       main = "Model Comparison: Test Accuracy",
       xlab = "Test Accuracy", xlim = c(0.9, 1.0))
dev.off()

# ==============================================================================
# Detailed Analysis of Best Model
# ==============================================================================
best_model_name <- comparison_df$Model[1]
best_model_results <- results_list[[best_model_name]]

cat("\n", rep("=", 80), "\n", sep = "")
cat("DETAILED ANALYSIS:", best_model_name, "\n")
cat(rep("=", 80), "\n", sep = "")

# Classification report
cat("\nClassification Report:\n")
print(confusionMatrix(best_model_results$predictions, y_test))

# Confusion matrix visualization
png(paste0("../../results/ml/confusion_matrix_", 
          gsub(" ", "_", best_model_name), ".png"), 
    width = 800, height = 600)
cm_plot <- as.data.frame(best_model_results$confusion_matrix)
colnames(cm_plot) <- c("Predicted", "Actual", "Freq")
ggplot(cm_plot, aes(x = Predicted, y = Actual, fill = Freq)) +
  geom_tile() +
  geom_text(aes(label = Freq), color = "white", size = 10) +
  scale_fill_gradient(low = "lightblue", high = "darkblue") +
  theme_minimal() +
  labs(title = paste("Confusion Matrix:", best_model_name))
dev.off()

# ROC Curve
if (!is.na(best_model_results$roc_auc)) {
  roc_obj <- roc(y_test, best_model_results$probabilities$Malignant)
  
  png(paste0("../../results/ml/roc_curve_", 
            gsub(" ", "_", best_model_name), ".png"), 
      width = 800, height = 600)
  plot(roc_obj, main = paste("ROC Curve:", best_model_name),
      print.auc = TRUE, auc.polygon = TRUE, grid = TRUE)
  dev.off()
}

# Feature importance (if available)
if ("rf" %in% class(best_model_results$model$finalModel) || 
    "ranger" %in% class(best_model_results$model$finalModel)) {
  
  if ("rf" %in% class(best_model_results$model$finalModel)) {
    importance_df <- data.frame(
      Feature = names(best_model_results$model$finalModel$importance),
      Importance = as.numeric(best_model_results$model$finalModel$importance)
    )
  } else {
    importance_df <- data.frame(
      Feature = names(best_model_results$model$finalModel$variable.importance),
      Importance = as.numeric(best_model_results$model$finalModel$variable.importance)
    )
  }
  
  importance_df <- importance_df[order(importance_df$Importance, decreasing = TRUE), ]
  
  cat("\nTop 10 Most Important Features:\n")
  print(head(importance_df, 10))
  
  # Visualization
  png(paste0("../../results/ml/feature_importance_", 
            gsub(" ", "_", best_model_name), ".png"), 
      width = 1000, height = 800)
  top_features <- head(importance_df, 15)
  barplot(top_features$Importance, names.arg = top_features$Feature,
         horiz = TRUE, las = 1,
         main = paste("Top 15 Feature Importances:", best_model_name),
         xlab = "Importance")
  dev.off()
}

# ==============================================================================
# Hyperparameter Tuning (Random Forest)
# ==============================================================================
cat("\n", rep("=", 80), "\n", sep = "")
cat("HYPERPARAMETER TUNING\n")
cat(rep("=", 80), "\n", sep = "")

cat("\nTuning Random Forest...\n")
tuned_rf <- train(
  x = X_train, y = y_train,
  method = "rf",
  trControl = train_control,
  metric = "ROC",
  tuneGrid = expand.grid(mtry = c(5, 10, 15, 20)),
  ntree = 200
)

cat("Best parameters:", tuned_rf$bestTune, "\n")
cat("Best CV score:", max(tuned_rf$results$ROC), "\n")

# Evaluate tuned model
pred_tuned <- predict(tuned_rf, X_test)
accuracy_tuned <- mean(pred_tuned == y_test)
cat("Tuned Random Forest Test Accuracy:", accuracy_tuned, "\n")

cat("\n", rep("=", 80), "\n", sep = "")
cat("ML ANALYSIS COMPLETE\n")
cat("All results saved to results/ml/\n")
cat(rep("=", 80), "\n", sep = "")

