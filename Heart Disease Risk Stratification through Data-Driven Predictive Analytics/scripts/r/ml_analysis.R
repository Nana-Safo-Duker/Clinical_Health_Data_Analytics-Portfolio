# Heart Disease Dataset - Machine Learning Analysis (R)

# Load necessary libraries
library(tidyverse)
library(caret)
library(randomForest)
library(e1071)
library(rpart)
library(glmnet)
library(pROC)
library(ggplot2)
library(gridExtra)

# Load the dataset
df <- read.csv("../../data/heart-disease.csv")
cat("Dataset loaded successfully!\n")

# Preprocess data
df_processed <- df
df_processed$sex <- as.factor(df_processed$sex)
df_processed$heart_disease <- as.factor(df_processed$heart_disease)

# Separate features and target
X <- df_processed %>% select(-heart_disease)
y <- df_processed$heart_disease

cat("Features:", paste(names(X), collapse = ", "), "\n")
cat("Target distribution:\n")
print(table(y))

# Train-test split
set.seed(42)
trainIndex <- createDataPartition(y, p = 0.8, list = FALSE)
X_train <- X[trainIndex, ]
X_test <- X[-trainIndex, ]
y_train <- y[trainIndex]
y_test <- y[-trainIndex]

cat("\nTrain set:", nrow(X_train), "samples\n")
cat("Test set:", nrow(X_test), "samples\n")

# ============================================================================
# MODEL TRAINING
# ============================================================================

cat("\n=== TRAINING MODELS ===\n")

# Define models
models <- list()

# 1. Logistic Regression
cat("\nTraining Logistic Regression...\n")
model_lr <- train(X_train, y_train, method = "glm", family = "binomial", 
                  trControl = trainControl(method = "cv", number = 5))
models[["Logistic Regression"]] <- model_lr

# 2. Random Forest
cat("Training Random Forest...\n")
model_rf <- train(X_train, y_train, method = "rf", 
                  trControl = trainControl(method = "cv", number = 5),
                  ntree = 100)
models[["Random Forest"]] <- model_rf

# 3. Support Vector Machine
cat("Training SVM...\n")
model_svm <- train(X_train, y_train, method = "svmRadial", 
                   trControl = trainControl(method = "cv", number = 5))
models[["SVM"]] <- model_svm

# 4. Decision Tree
cat("Training Decision Tree...\n")
model_dt <- train(X_train, y_train, method = "rpart", 
                  trControl = trainControl(method = "cv", number = 5))
models[["Decision Tree"]] <- model_dt

# 5. Naive Bayes
cat("Training Naive Bayes...\n")
model_nb <- train(X_train, y_train, method = "nb", 
                  trControl = trainControl(method = "cv", number = 5))
models[["Naive Bayes"]] <- model_nb

# ============================================================================
# MODEL EVALUATION
# ============================================================================

cat("\n=== MODEL EVALUATION ===\n")

results <- data.frame()

for(name in names(models)) {
  model <- models[[name]]
  
  # Predictions
  y_pred <- predict(model, X_test)
  y_pred_proba <- predict(model, X_test, type = "prob")[, 2]
  
  # Metrics
  cm <- confusionMatrix(y_pred, y_test)
  accuracy <- cm$overall["Accuracy"]
  precision <- cm$byClass["Precision"]
  recall <- cm$byClass["Recall"]
  f1 <- cm$byClass["F1"]
  
  # ROC-AUC
  roc_obj <- roc(as.numeric(y_test), y_pred_proba)
  roc_auc <- auc(roc_obj)
  
  # Cross-validation results
  cv_results <- model$results
  
  results <- rbind(results, data.frame(
    Model = name,
    Accuracy = as.numeric(accuracy),
    Precision = as.numeric(precision),
    Recall = as.numeric(recall),
    F1 = as.numeric(f1),
    ROC_AUC = as.numeric(roc_auc),
    CV_Accuracy = max(cv_results$Accuracy, na.rm = TRUE)
  ))
  
  cat("\n", name, ":\n")
  cat("  Accuracy:", as.numeric(accuracy), "\n")
  cat("  Precision:", as.numeric(precision), "\n")
  cat("  Recall:", as.numeric(recall), "\n")
  cat("  F1-Score:", as.numeric(f1), "\n")
  cat("  ROC-AUC:", as.numeric(roc_auc), "\n")
}

# Sort by ROC-AUC
results <- results[order(results$ROC_AUC, decreasing = TRUE), ]
print(results)

# ============================================================================
# VISUALIZATIONS
# ============================================================================

# Create output directory
if(!dir.exists("../../results/figures")) {
  dir.create("../../results/figures", recursive = TRUE)
}

# Model comparison
png("../../results/figures/r_ml_model_comparison.png", width = 1800, height = 1000, res = 300)
p1 <- ggplot(results, aes(x = reorder(Model, Accuracy), y = Accuracy)) +
  geom_bar(stat = "identity", fill = "steelblue", alpha = 0.7) +
  coord_flip() +
  labs(title = "Model Accuracy Comparison", x = "Model", y = "Accuracy") +
  theme_minimal()

p2 <- ggplot(results, aes(x = reorder(Model, ROC_AUC), y = ROC_AUC)) +
  geom_bar(stat = "identity", fill = "darkgreen", alpha = 0.7) +
  coord_flip() +
  labs(title = "Model ROC-AUC Comparison", x = "Model", y = "ROC-AUC") +
  theme_minimal()

grid.arrange(p1, p2, ncol = 2)
dev.off()

# ROC Curves
png("../../results/figures/r_ml_roc_curves.png", width = 1000, height = 800, res = 300)
plot(roc(as.numeric(y_test), predict(models[["Logistic Regression"]], X_test, type = "prob")[, 2]),
     main = "ROC Curves Comparison", col = "blue", lwd = 2)
for(i in 2:length(models)) {
  model <- models[[i]]
  y_pred_proba <- predict(model, X_test, type = "prob")[, 2]
  roc_obj <- roc(as.numeric(y_test), y_pred_proba)
  lines(roc_obj, col = i, lwd = 2)
}
legend("bottomright", legend = names(models), col = 1:length(models), lwd = 2)
dev.off()

# Confusion matrices
png("../../results/figures/r_ml_confusion_matrices.png", width = 1600, height = 1200, res = 300)
plots <- list()
for(i in 1:min(4, length(models))) {
  name <- names(models)[i]
  model <- models[[name]]
  y_pred <- predict(model, X_test)
  cm <- confusionMatrix(y_pred, y_test)
  
  cm_df <- as.data.frame(cm$table)
  p <- ggplot(cm_df, aes(x = Reference, y = Prediction, fill = Freq)) +
    geom_tile() +
    geom_text(aes(label = Freq), color = "white", size = 5) +
    scale_fill_gradient(low = "lightblue", high = "darkblue") +
    labs(title = paste(name, "\nAccuracy:", round(cm$overall["Accuracy"], 3))) +
    theme_minimal()
  plots[[i]] <- p
}
grid.arrange(grobs = plots, ncol = 2)
dev.off()

# Feature importance (for Random Forest)
if("Random Forest" %in% names(models)) {
  png("../../results/figures/r_ml_feature_importance.png", width = 1000, height = 600, res = 300)
  importance_df <- data.frame(
    Feature = rownames(varImp(models[["Random Forest"]])$importance),
    Importance = varImp(models[["Random Forest"]])$importance$Overall
  )
  importance_df <- importance_df[order(importance_df$Importance, decreasing = TRUE), ]
  
  ggplot(importance_df, aes(x = reorder(Feature, Importance), y = Importance)) +
    geom_bar(stat = "identity", fill = "steelblue", alpha = 0.7) +
    coord_flip() +
    labs(title = "Random Forest - Feature Importance", x = "Feature", y = "Importance") +
    theme_minimal()
  dev.off()
}

# Save best model
best_model_name <- results$Model[1]
best_model <- models[[best_model_name]]
saveRDS(best_model, "../../results/models/best_model_r.rds")
cat("\nBest model (", best_model_name, ") saved to ../../results/models/best_model_r.rds\n")

# Save results
write.csv(results, "../../results/model_results_r.csv", row.names = FALSE)
cat("Results saved to ../../results/model_results_r.csv\n")

cat("\n=== ML Analysis Complete! ===\n")

