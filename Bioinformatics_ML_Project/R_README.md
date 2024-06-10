# R Scripts for Bioinformatics ML Project

This directory contains R implementations of the machine learning pipeline for clinical diagnosis.

## 📋 R Scripts Overview

### 1. `data_processing.R`
Complete data processing pipeline including:
- Data loading and validation
- Missing value imputation (mean, median, MICE)
- Outlier detection and removal
- Feature scaling (standard, min-max, robust)
- Train/test splitting
- Synthetic data generation

**Key Functions:**
- `load_clinical_data()` - Load data from CSV
- `handle_missing_values()` - Impute missing values
- `remove_outliers()` - Detect and remove outliers
- `scale_features()` - Scale numerical features
- `preprocess_data()` - Complete preprocessing pipeline
- `generate_synthetic_data()` - Create synthetic datasets

### 2. `ml_models.R`
Machine learning model implementations:
- Random Forest
- Support Vector Machine (SVM)
- Gradient Boosting Machine (GBM)
- Neural Network

**Key Functions:**
- `train_random_forest()` - Train Random Forest classifier
- `train_svm()` - Train SVM classifier
- `train_gradient_boosting()` - Train GBM classifier
- `train_neural_network()` - Train Neural Network
- `cross_validate_model()` - K-fold cross-validation
- `get_feature_importance()` - Extract feature importance
- `save_model()` / `load_model()` - Model persistence

### 3. `run_pipeline.R`
Complete end-to-end ML pipeline that:
1. Loads or generates data
2. Preprocesses data
3. Trains multiple models
4. Evaluates performance
5. Generates visualizations
6. Saves models and results

## 🚀 Installation

### Required R Packages

```r
# Install required packages
install.packages(c(
  "tidyverse",       # Data manipulation
  "caret",           # Machine learning framework
  "randomForest",    # Random Forest
  "e1071",           # SVM
  "gbm",             # Gradient Boosting
  "nnet",            # Neural Networks
  "pROC",            # ROC analysis
  "mice",            # Missing value imputation
  "ggplot2",         # Visualization
  "scales"           # Scaling utilities
))
```

Or use the provided installation script:

```r
source("install_packages.R")
```

## 💻 Usage Examples

### Quick Start: Run Complete Pipeline

```r
# Source the pipeline script
source("scripts/run_pipeline.R")

# Run with default settings
results <- run_pipeline(
  n_samples = 1000,
  models = c("rf", "svm", "gbm"),
  output_dir = "results"
)
```

### Command Line Execution

```bash
# Run from terminal
Rscript scripts/run_pipeline.R
```

### Step-by-Step Usage

#### 1. Data Processing

```r
# Source data processing module
source("scripts/data_processing.R")

# Generate synthetic data
df <- generate_synthetic_data(n_samples = 1000)

# Or load real data
df <- load_clinical_data("data/raw/clinical_data.csv")

# Preprocess data
result <- preprocess_data(
  df,
  target_column = "diagnosis",
  test_size = 0.2,
  scale = TRUE
)

# Extract components
X_train <- result$X_train
X_test <- result$X_test
y_train <- result$y_train
y_test <- result$y_test
```

#### 2. Model Training

```r
# Source model module
source("scripts/ml_models.R")

# Train Random Forest
rf_model <- train_random_forest(
  X_train, y_train,
  ntree = 100,
  mtry = 3
)

# Train SVM
svm_model <- train_svm(
  X_train, y_train,
  kernel = "radial",
  cost = 1.0
)

# Train Gradient Boosting
gbm_model <- train_gradient_boosting(
  X_train, y_train,
  n_trees = 100,
  interaction_depth = 3,
  shrinkage = 0.1
)
```

#### 3. Model Evaluation

```r
# Make predictions
predictions <- predict(rf_model, X_test)

# Calculate accuracy
accuracy <- mean(predictions == y_test)
cat(sprintf("Accuracy: %.4f\n", accuracy))

# Confusion matrix
cm <- table(Actual = y_test, Predicted = predictions)
print(cm)

# Cross-validation
cv_results <- cross_validate_model(
  X_train, y_train,
  model_type = "rf",
  k = 5
)
```

#### 4. Feature Importance

```r
# Get feature importance
feature_names <- c(
  'age', 'bmi', 'blood_pressure_sys', 'blood_pressure_dia',
  'glucose', 'cholesterol', 'heart_rate', 
  'biomarker_a', 'biomarker_b'
)

importance <- get_feature_importance(
  rf_model,
  feature_names,
  top_n = 10
)

# Visualize
barplot(
  importance$Importance[1:10],
  names.arg = importance$Feature[1:10],
  horiz = TRUE,
  las = 1,
  main = "Top 10 Feature Importances"
)
```

#### 5. ROC Curve Analysis

```r
library(pROC)

# Get predicted probabilities
pred_prob <- predict(rf_model, X_test, type = "prob")[, 2]

# Calculate ROC
roc_obj <- roc(y_test, pred_prob)
auc_score <- auc(roc_obj)

# Plot ROC curve
plot(roc_obj, main = sprintf("ROC Curve (AUC = %.3f)", auc_score))
```

#### 6. Save and Load Models

```r
# Save model
save_model(rf_model, "results/models/rf_model.rds")

# Load model
loaded_model <- load_model("results/models/rf_model.rds")

# Make predictions with loaded model
new_predictions <- predict(loaded_model, X_test)
```

## 📊 Complete Example

```r
#!/usr/bin/env Rscript

# Load libraries
library(tidyverse)
library(randomForest)
library(caret)

# Source modules
source("scripts/data_processing.R")
source("scripts/ml_models.R")

# =====================================================
# 1. DATA PREPARATION
# =====================================================
cat("Generating data...\n")
df <- generate_synthetic_data(n_samples = 1000)

cat("Preprocessing data...\n")
result <- preprocess_data(df)

# =====================================================
# 2. MODEL TRAINING
# =====================================================
cat("\nTraining Random Forest...\n")
rf_model <- train_random_forest(
  result$X_train,
  result$y_train,
  ntree = 100
)

cat("\nTraining SVM...\n")
svm_model <- train_svm(
  result$X_train,
  result$y_train,
  kernel = "radial"
)

# =====================================================
# 3. MODEL EVALUATION
# =====================================================
cat("\n=== Random Forest Evaluation ===\n")
rf_pred <- predict(rf_model, result$X_test)
rf_accuracy <- mean(rf_pred == result$y_test)
cat(sprintf("Accuracy: %.4f\n", rf_accuracy))

cat("\n=== SVM Evaluation ===\n")
svm_pred <- predict(svm_model, result$X_test)
svm_accuracy <- mean(svm_pred == result$y_test)
cat(sprintf("Accuracy: %.4f\n", svm_accuracy))

# =====================================================
# 4. CROSS-VALIDATION
# =====================================================
cat("\n=== Cross-Validation ===\n")
cv_rf <- cross_validate_model(
  result$X_train,
  result$y_train,
  model_type = "rf",
  k = 5
)

# =====================================================
# 5. FEATURE IMPORTANCE
# =====================================================
cat("\n=== Feature Importance ===\n")
feature_names <- c(
  'age', 'bmi', 'blood_pressure_sys', 'blood_pressure_dia',
  'glucose', 'cholesterol', 'heart_rate',
  'biomarker_a', 'biomarker_b'
)

importance <- get_feature_importance(rf_model, feature_names, top_n = 5)

# =====================================================
# 6. SAVE MODELS
# =====================================================
cat("\nSaving models...\n")
dir.create("results/models", recursive = TRUE, showWarnings = FALSE)
save_model(rf_model, "results/models/rf_model.rds")
save_model(svm_model, "results/models/svm_model.rds")

cat("\n✓ Analysis complete!\n")
```

## 🎯 Model Parameters

### Random Forest
```r
train_random_forest(
  X_train, y_train,
  ntree = 100,           # Number of trees
  mtry = NULL,           # Variables per split (default: sqrt(p))
  importance = TRUE      # Calculate feature importance
)
```

### SVM
```r
train_svm(
  X_train, y_train,
  kernel = "radial",     # Kernel: linear, polynomial, radial, sigmoid
  cost = 1.0,            # Regularization parameter
  probability = TRUE     # Enable probability estimates
)
```

### Gradient Boosting
```r
train_gradient_boosting(
  X_train, y_train,
  n_trees = 100,         # Number of boosting iterations
  interaction_depth = 3, # Maximum tree depth
  shrinkage = 0.1        # Learning rate
)
```

### Neural Network
```r
train_neural_network(
  X_train, y_train,
  size = c(10, 5),       # Hidden layer sizes
  maxit = 500            # Maximum iterations
)
```

## 📈 Output Structure

After running the pipeline, results are saved in:

```
results/
├── figures/
│   ├── roc_curves.png          # ROC curves for all models
│   └── feature_importance.png  # Feature importance plot
└── models/
    ├── randomforest_model.rds  # Trained RF model
    ├── svm_model.rds           # Trained SVM model
    ├── gradientboosting_model.rds  # Trained GBM model
    └── scaler.rds              # Scaler parameters
```

## 🔍 Troubleshooting

### Common Issues

1. **Package Installation Errors**
   ```r
   # Try installing from source
   install.packages("package_name", type = "source")
   ```

2. **Memory Issues with Large Datasets**
   ```r
   # Reduce ntree for Random Forest
   rf_model <- train_random_forest(X_train, y_train, ntree = 50)
   ```

3. **Convergence Issues with Neural Networks**
   ```r
   # Increase max iterations
   nn_model <- train_neural_network(X_train, y_train, maxit = 1000)
   ```

## 📚 Additional Resources

- [R Caret Package Documentation](https://topepo.github.io/caret/)
- [Random Forest in R](https://www.rdocumentation.org/packages/randomForest)
- [SVM with e1071](https://cran.r-project.org/web/packages/e1071/)
- [Gradient Boosting Machine](https://cran.r-project.org/web/packages/gbm/)

## 🤝 Integration with Python

The R scripts produce compatible outputs with the Python implementation:
- Models can be evaluated using the same metrics
- Data format is consistent (CSV)
- Visualization outputs are in standard formats (PNG, PDF)

## 📝 Notes

- All functions include comprehensive documentation
- Random seeds are set for reproducibility (seed = 42)
- Error handling is implemented for robust execution
- Progress messages guide users through execution
- Models are saved in `.rds` format for R compatibility

---

**For Python implementation, see:** `src/` directory

**For complete pipeline:** Run `Rscript scripts/run_pipeline.R`

*Last Updated: October 27, 2025*


