# Statistical Analysis: Descriptive, Inferential, and Exploratory
# Comprehensive statistical analysis of health data

# Load libraries
library(ggplot2)
library(dplyr)
library(corrplot)
library(caret)
library(VIM)

# Set working directory (adjust as needed)
# setwd("path/to/your/project")

# Load data
df <- read.csv("../data/health_data.csv", stringsAsFactors = FALSE)

# Remove unnecessary columns
if ("Unnamed..0" %in% colnames(df)) {
  df <- df[, !colnames(df) %in% "Unnamed..0"]
}

# Data cleaning and preprocessing
df$age_years <- df$age / 365.25
df$bmi <- df$weight / ((df$height / 100) ^ 2)

# Clean blood pressure data
df <- df[df$ap_hi >= 80 & df$ap_hi <= 250, ]
df <- df[df$ap_lo >= 40 & df$ap_lo <= 150, ]
df <- df[df$ap_hi >= df$ap_lo, ]

# Clean height and weight
df <- df[df$height >= 100 & df$height <= 220, ]
df <- df[df$weight >= 30 & df$weight <= 200, ]
df <- df[df$bmi >= 10 & df$bmi <= 60, ]

cat("Dataset shape:", dim(df), "\n")
cat("Missing values:\n")
print(colSums(is.na(df)))

# ============================================================================
# 1. DESCRIPTIVE STATISTICS
# ============================================================================

cat("\n", "=", rep("=", 78), "\n", sep="")
cat("DESCRIPTIVE STATISTICS - NUMERICAL VARIABLES\n")
cat("=", rep("=", 78), "\n", sep="")

numerical_cols <- c("age_years", "height", "weight", "ap_hi", "ap_lo", "bmi")
print(summary(df[numerical_cols]))

# Additional statistics
cat("\n", "=", rep("=", 78), "\n", sep="")
cat("ADDITIONAL STATISTICS\n")
cat("=", rep("=", 78), "\n", sep="")

# Install moments package if not available
if (!require(moments)) {
  install.packages("moments")
  library(moments)
}

for (col in numerical_cols) {
  cat("\n", toupper(col), ":\n", sep="")
  if (require(moments, quietly = TRUE)) {
    cat("  Skewness:", skewness(df[[col]], na.rm = TRUE), "\n")
    cat("  Kurtosis:", kurtosis(df[[col]], na.rm = TRUE), "\n")
  }
  cat("  Median:", median(df[[col]], na.rm = TRUE), "\n")
  cat("  IQR:", IQR(df[[col]], na.rm = TRUE), "\n")
}

# Categorical variables
cat("\n", "=", rep("=", 78), "\n", sep="")
cat("DESCRIPTIVE STATISTICS - CATEGORICAL VARIABLES\n")
cat("=", rep("=", 78), "\n", sep="")

categorical_cols <- c("gender", "cholesterol", "gluc", "smoke", "alco", "active", "cardio")
for (col in categorical_cols) {
  cat("\n", toupper(col), ":\n", sep="")
  print(table(df[[col]]))
  print(prop.table(table(df[[col]])))
}

# ============================================================================
# 2. INFERENTIAL STATISTICS
# ============================================================================

cat("\n", "=", rep("=", 78), "\n", sep="")
cat("T-TEST: Age difference between cardio and non-cardio patients\n")
cat("=", rep("=", 78), "\n", sep="")

cardio_yes <- df$age_years[df$cardio == 1]
cardio_no <- df$age_years[df$cardio == 0]

t_test_result <- t.test(cardio_yes, cardio_no)
print(t_test_result)
cat("Mean age (Cardio=1):", mean(cardio_yes), "years\n")
cat("Mean age (Cardio=0):", mean(cardio_no), "years\n")

# Chi-square tests
cat("\n", "=", rep("=", 78), "\n", sep="")
cat("CHI-SQUARE TESTS: Association between categorical variables and cardio\n")
cat("=", rep("=", 78), "\n", sep="")

categorical_vars <- c("gender", "cholesterol", "gluc", "smoke", "alco", "active")
for (var in categorical_vars) {
  cat("\n", toupper(var), " vs Cardio:\n", sep="")
  contingency_table <- table(df[[var]], df$cardio)
  chi_test <- chisq.test(contingency_table)
  print(chi_test)
  cat("  Degrees of freedom:", chi_test$parameter, "\n")
  if (chi_test$p.value < 0.05) {
    cat("  Result: Significant association (p < 0.05)\n")
  } else {
    cat("  Result: No significant association (p >= 0.05)\n")
  }
}

# Correlation analysis
cat("\n", "=", rep("=", 78), "\n", sep="")
cat("CORRELATION ANALYSIS\n")
cat("=", rep("=", 78), "\n", sep="")

correlation_cols <- c("age_years", "height", "weight", "ap_hi", "ap_lo", "bmi", "cardio")
correlation_matrix <- cor(df[correlation_cols], use = "complete.obs")
print(correlation_matrix)

# Visualize correlation matrix
png("../figures/correlation_matrix.png", width = 1200, height = 1000, res = 300)
corrplot(correlation_matrix, method = "color", type = "upper", 
         order = "hclust", tl.cex = 0.8, tl.col = "black", 
         addCoef.col = "black", number.cex = 0.7)
dev.off()

# ============================================================================
# 3. EXPLORATORY DATA ANALYSIS
# ============================================================================

# Distribution of target variable
png("../figures/cardio_distribution.png", width = 1200, height = 800, res = 300)
cardio_counts <- table(df$cardio)
barplot(cardio_counts, names.arg = c("No (0)", "Yes (1)"), 
        col = c("skyblue", "salmon"), border = "black",
        main = "Distribution of Cardiovascular Disease",
        xlab = "Cardiovascular Disease", ylab = "Count")
text(barplot(cardio_counts, plot = FALSE), cardio_counts + 500, 
     labels = cardio_counts, pos = 3, font = 2)
dev.off()

# Distribution of numerical variables
png("../figures/numerical_distributions.png", width = 1800, height = 1200, res = 300)
par(mfrow = c(2, 3))
for (col in numerical_cols) {
  hist(df[[col]], breaks = 50, main = paste("Distribution of", toupper(col)),
       xlab = col, col = "steelblue", border = "black")
}
dev.off()

# Box plots by cardio status
png("../figures/boxplots_by_cardio.png", width = 1800, height = 1200, res = 300)
par(mfrow = c(2, 3))
for (col in numerical_cols) {
  boxplot(df[[col]] ~ df$cardio, main = paste(toupper(col), "by Cardio Status"),
          xlab = "Cardiovascular Disease", ylab = col,
          col = c("skyblue", "salmon"), border = "black")
}
dev.off()

# Summary statistics by cardio status
cat("\n", "=", rep("=", 78), "\n", sep="")
cat("SUMMARY STATISTICS BY CARDIO STATUS\n")
cat("=", rep("=", 78), "\n", sep="")
print(aggregate(df[numerical_cols], by = list(df$cardio), FUN = function(x) {
  c(mean = mean(x), median = median(x), sd = sd(x))
}))

cat("\nStatistical analysis completed successfully!\n")

