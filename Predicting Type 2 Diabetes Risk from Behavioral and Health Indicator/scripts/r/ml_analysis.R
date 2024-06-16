# Machine Learning Analysis
# Diabetes Binary Health Indicators - BRFSS 2021

# Load required libraries
library(caret)
library(randomForest)
library(e1071)
library(pROC)
library(ggplot2)
library(dplyr)

# Set working directory
setwd("../../")

# Load data
df <- read.csv("data/diabetes_binary_health_indicators_BRFSS2021.csv")

cat("Dataset shape:", dim(df), "\n")

# Prepare data
set.seed(42)
trainIndex <- createDataPartition(df$Diabetes_binary, p = 0.8, list = FALSE)
train_data <- df[trainIndex, ]
test_data <- df[-trainIndex, ]

# Separate features and target
X_train <- train_data[, !colnames(train_data) %in% "Diabetes_binary"]
y_train <- train_data$Diabetes_binary
X_test <- test_data[, !colnames(test_data) %in% "Diabetes_binary"]
y_test <- test_data$Diabetes_binary

cat("Training set size:", dim(train_data), "\n")
cat("Test set size:", dim(test_data), "\n")

# Scale features
preProc <- preProcess(X_train, method = c("center", "scale"))
X_train_scaled <- predict(preProc, X_train)
X_test_scaled <- predict(preProc, X_test)

# Train models
cat("\n=== TRAINING MODELS ===\n")

# Logistic Regression
cat("\nTraining Logistic Regression...\n")
log_model <- glm(Diabetes_binary ~ ., data = train_data, family = binomial)
log_pred <- predict(log_model, newdata = test_data, type = "response")
log_pred_class <- ifelse(log_pred > 0.5, 1, 0)

log_accuracy <- mean(log_pred_class == y_test)
log_precision <- sum(log_pred_class == 1 & y_test == 1) / sum(log_pred_class == 1)
log_recall <- sum(log_pred_class == 1 & y_test == 1) / sum(y_test == 1)
log_f1 <- 2 * (log_precision * log_recall) / (log_precision + log_recall)
log_auc <- auc(roc(y_test, log_pred))

cat("Logistic Regression - Accuracy:", log_accuracy, "AUC:", log_auc, "\n")

# Random Forest
cat("\nTraining Random Forest...\n")
rf_model <- randomForest(as.factor(Diabetes_binary) ~ ., data = train_data, ntree = 100, mtry = sqrt(ncol(X_train)))
rf_pred <- predict(rf_model, newdata = test_data, type = "prob")[, 2]
rf_pred_class <- predict(rf_model, newdata = test_data)

rf_accuracy <- mean(rf_pred_class == y_test)
rf_precision <- sum(rf_pred_class == 1 & y_test == 1) / sum(rf_pred_class == 1)
rf_recall <- sum(rf_pred_class == 1 & y_test == 1) / sum(y_test == 1)
rf_f1 <- 2 * (rf_precision * rf_recall) / (rf_precision + rf_recall)
rf_auc <- auc(roc(y_test, rf_pred))

cat("Random Forest - Accuracy:", rf_accuracy, "AUC:", rf_auc, "\n")

# SVM
cat("\nTraining SVM...\n")
svm_model <- svm(as.factor(Diabetes_binary) ~ ., data = train_data, probability = TRUE)
svm_pred <- attr(predict(svm_model, newdata = test_data, probability = TRUE), "probabilities")[, 2]
svm_pred_class <- predict(svm_model, newdata = test_data)

svm_accuracy <- mean(svm_pred_class == y_test)
svm_precision <- sum(svm_pred_class == 1 & y_test == 1) / sum(svm_pred_class == 1)
svm_recall <- sum(svm_pred_class == 1 & y_test == 1) / sum(y_test == 1)
svm_f1 <- 2 * (svm_precision * svm_recall) / (svm_precision + svm_recall)
svm_auc <- auc(roc(y_test, svm_pred))

cat("SVM - Accuracy:", svm_accuracy, "AUC:", svm_auc, "\n")

# Model Comparison
results <- data.frame(
  Model = c("Logistic Regression", "Random Forest", "SVM"),
  Accuracy = c(log_accuracy, rf_accuracy, svm_accuracy),
  Precision = c(log_precision, rf_precision, svm_precision),
  Recall = c(log_recall, rf_recall, svm_recall),
  F1_Score = c(log_f1, rf_f1, svm_f1),
  AUC = c(log_auc, rf_auc, svm_auc)
)

print(results)

# Save results
write.csv(results, "results/models/model_performance_r.csv", row.names = FALSE)

# ROC Curves
png("results/figures/roc_curves_r.png", width = 1000, height = 800, res = 300)
plot(roc(y_test, log_pred), col = "blue", main = "ROC Curves - Model Comparison")
lines(roc(y_test, rf_pred), col = "red")
lines(roc(y_test, svm_pred), col = "green")
legend("bottomright", legend = c("Logistic Regression", "Random Forest", "SVM"),
       col = c("blue", "red", "green"), lty = 1)
dev.off()

# Feature Importance (Random Forest)
if (exists("rf_model")) {
  feature_importance <- importance(rf_model)
  feature_importance_df <- data.frame(
    Feature = rownames(feature_importance),
    Importance = feature_importance[, 1]
  )
  feature_importance_df <- feature_importance_df[order(-feature_importance_df$Importance), ]
  
  cat("\nTop 10 Most Important Features (Random Forest):\n")
  print(head(feature_importance_df, 10))
  
  # Visualization
  png("results/figures/feature_importance_rf_r.png", width = 1000, height = 800, res = 300)
  barplot(head(feature_importance_df$Importance, 15), 
          names.arg = head(feature_importance_df$Feature, 15),
          main = "Top 15 Feature Importance (Random Forest)",
          xlab = "Importance", las = 2, col = "steelblue")
  dev.off()
}

cat("\n=== MACHINE LEARNING ANALYSIS COMPLETE ===\n")
cat("Best Model (by AUC):", results$Model[which.max(results$AUC)], "\n")

