# Machine Learning Analysis
# Predicting cardiovascular disease using various ML algorithms

# Load libraries
library(caret)
library(randomForest)
library(e1071)
library(pROC)
library(xgboost)
library(lightgbm)
library(ggplot2)
library(dplyr)

# Load data
df <- read.csv("../data/health_data.csv", stringsAsFactors = FALSE)

# Data cleaning and preprocessing
if ("Unnamed..0" %in% colnames(df)) {
  df <- df[, !colnames(df) %in% "Unnamed..0"]
}

df$age_years <- df$age / 365.25
df$bmi <- df$weight / ((df$height / 100) ^ 2)
df <- df[df$ap_hi >= 80 & df$ap_hi <= 250, ]
df <- df[df$ap_lo >= 40 & df$ap_lo <= 150, ]
df <- df[df$ap_hi >= df$ap_lo, ]
df <- df[df$height >= 100 & df$height <= 220, ]
df <- df[df$weight >= 30 & df$weight <= 200, ]
df <- df[df$bmi >= 10 & df$bmi <= 60, ]

# Prepare data
feature_cols <- c("age_years", "gender", "height", "weight", "ap_hi", "ap_lo",
                  "cholesterol", "gluc", "smoke", "alco", "active", "bmi")
X <- df[feature_cols]
y <- as.factor(df$cardio)

# Split data
set.seed(42)
train_index <- createDataPartition(y, p = 0.8, list = FALSE)
X_train <- X[train_index, ]
X_test <- X[-train_index, ]
y_train <- y[train_index]
y_test <- y[-train_index]

cat("Training set size:", dim(X_train), "\n")
cat("Test set size:", dim(X_test), "\n")
cat("Features:", feature_cols, "\n")

# ============================================================================
# MODEL TRAINING
# ============================================================================

cat("\n", "=", rep("=", 78), "\n", sep="")
cat("MACHINE LEARNING MODEL TRAINING\n")
cat("=", rep("=", 78), "\n", sep="")

# Control parameters
ctrl <- trainControl(method = "cv", number = 5, 
                     classProbs = TRUE, summaryFunction = twoClassSummary,
                     verboseIter = FALSE)

# Train models
models <- list()

# Logistic Regression
cat("\nTraining Logistic Regression...\n")
models[["Logistic Regression"]] <- train(X_train, y_train,
                                          method = "glm",
                                          family = "binomial",
                                          trControl = ctrl,
                                          metric = "ROC")

# Random Forest
cat("Training Random Forest...\n")
models[["Random Forest"]] <- train(X_train, y_train,
                                    method = "rf",
                                    ntree = 100,
                                    trControl = ctrl,
                                    metric = "ROC",
                                    verbose = FALSE)

# Gradient Boosting
cat("Training Gradient Boosting...\n")
models[["Gradient Boosting"]] <- train(X_train, y_train,
                                        method = "gbm",
                                        trControl = ctrl,
                                        metric = "ROC",
                                        verbose = FALSE)

# SVM
cat("Training SVM...\n")
models[["SVM"]] <- train(X_train, y_train,
                         method = "svmRadial",
                         trControl = ctrl,
                         metric = "ROC")

# XGBoost
cat("Training XGBoost...\n")
xgb_grid <- expand.grid(nrounds = 100,
                        max_depth = 6,
                        eta = 0.3,
                        gamma = 0,
                        colsample_bytree = 1,
                        min_child_weight = 1,
                        subsample = 1)
models[["XGBoost"]] <- train(X_train, y_train,
                              method = "xgbTree",
                              tuneGrid = xgb_grid,
                              trControl = ctrl,
                              metric = "ROC",
                              verbose = FALSE)

# ============================================================================
# MODEL EVALUATION
# ============================================================================

cat("\n", "=", rep("=", 78), "\n", sep="")
cat("MODEL EVALUATION\n")
cat("=", rep("=", 78), "\n", sep="")

results <- data.frame(Model = character(), ROC_AUC = numeric(), 
                      stringsAsFactors = FALSE)

# Predictions and evaluation
predictions <- list()
roc_curves <- list()

for (name in names(models)) {
  cat("\n", name, ":\n", sep="")
  
  # Predictions
  pred <- predict(models[[name]], X_test)
  pred_proba <- predict(models[[name]], X_test, type = "prob")[, 2]
  
  predictions[[name]] <- list(pred = pred, pred_proba = pred_proba)
  
  # Classification report
  cat("Classification Report:\n")
  print(confusionMatrix(pred, y_test))
  
  # ROC-AUC
  roc_obj <- roc(y_test, pred_proba)
  roc_auc <- auc(roc_obj)
  results <- rbind(results, data.frame(Model = name, ROC_AUC = as.numeric(roc_auc)))
  roc_curves[[name]] <- roc_obj
  
  cat("ROC-AUC:", roc_auc, "\n")
}

# Sort results
results <- results[order(-results$ROC_AUC), ]
print(results)

# ROC curves
png("../figures/roc_curves.png", width = 1200, height = 800, res = 300)
plot(roc_curves[[1]], main = "ROC Curves - Model Comparison",
     col = 1, lwd = 2)
for (i in 2:length(roc_curves)) {
  lines(roc_curves[[i]], col = i, lwd = 2)
}
legend("bottomright", legend = names(roc_curves),
       col = 1:length(roc_curves), lwd = 2)
abline(a = 0, b = 1, lty = 2, col = "gray")
dev.off()

# Confusion matrices
png("../figures/confusion_matrices.png", width = 1800, height = 1200, res = 300)
par(mfrow = c(2, 3))
for (name in names(models)) {
  cm <- confusionMatrix(predictions[[name]]$pred, y_test)$table
  heatmap(cm, main = paste(name, "\nROC-AUC:", 
                           round(results[results$Model == name, "ROC_AUC"], 4)),
          col = heat.colors(256), Rowv = NA, Colv = NA,
          xlab = "Predicted", ylab = "Actual")
}
dev.off()

# Model comparison
png("../figures/model_comparison.png", width = 1200, height = 600, res = 300)
barplot(results$ROC_AUC, names.arg = results$Model, horiz = TRUE,
        main = "Model Performance Comparison",
        xlab = "ROC-AUC Score", col = "steelblue", border = "black")
abline(v = 0.5, lty = 2, col = "red")
text(results$ROC_AUC + 0.01, 1:nrow(results), 
     labels = round(results$ROC_AUC, 4), pos = 4)
grid(nx = NA, ny = NULL)
dev.off()

# ============================================================================
# FEATURE IMPORTANCE
# ============================================================================

cat("\n", "=", rep("=", 78), "\n", sep="")
cat("FEATURE IMPORTANCE ANALYSIS\n")
cat("=", rep("=", 78), "\n", sep="")

# Get feature importance from Random Forest
rf_model <- models[["Random Forest"]]
if (!is.null(rf_model$finalModel$importance)) {
  importance <- importance(rf_model$finalModel)
  importance_df <- data.frame(
    Feature = rownames(importance),
    Importance = importance[, "MeanDecreaseGini"]
  )
  importance_df <- importance_df[order(-importance_df$Importance), ]
  
  png("../figures/feature_importance.png", width = 1200, height = 800, res = 300)
  barplot(importance_df$Importance, names.arg = importance_df$Feature,
          main = "Random Forest - Feature Importance",
          xlab = "Importance", col = "steelblue", border = "black",
          las = 2, horiz = TRUE)
  grid(nx = NA, ny = NULL)
  dev.off()
  
  print(importance_df)
}

cat("\nMachine Learning Analysis completed successfully!\n")

