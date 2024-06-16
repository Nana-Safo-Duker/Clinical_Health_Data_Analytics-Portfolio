# Comprehensive Exploratory Data Analysis
# Deep dive into the health dataset

# Load libraries
library(ggplot2)
library(dplyr)
library(corrplot)
library(VIM)
library(psych)

# Install moments package if not available
if (!require(moments)) {
  install.packages("moments")
  library(moments)
}

# Load data
df <- read.csv("../data/health_data.csv", stringsAsFactors = FALSE)

# Data cleaning
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

# ============================================================================
# DATA OVERVIEW
# ============================================================================

cat("=", rep("=", 78), "\n", sep="")
cat("DATA OVERVIEW\n")
cat("=", rep("=", 78), "\n", sep="")
cat("Dataset shape:", dim(df), "\n")
cat("\nColumn names:", colnames(df), "\n")
cat("\nData types:\n")
print(sapply(df, class))
cat("\nMissing values:\n")
print(colSums(is.na(df)))
cat("\nDuplicate rows:", sum(duplicated(df)), "\n")
cat("\nFirst few rows:\n")
print(head(df))
cat("\nSummary statistics:\n")
print(summary(df))

# Missing data visualization
if (sum(is.na(df)) > 0) {
  png("../figures/missing_data.png", width = 1200, height = 800, res = 300)
  aggr(df, col = c('steelblue', 'red'), numbers = TRUE, sortVars = TRUE,
       labels = names(df), cex.axis = 0.7, gap = 3,
       ylab = c("Missing data", "Pattern"))
  dev.off()
}

# ============================================================================
# OUTLIER ANALYSIS
# ============================================================================

cat("\n", "=", rep("=", 78), "\n", sep="")
cat("OUTLIER ANALYSIS\n")
cat("=", rep("=", 78), "\n", sep="")

numerical_cols <- c("age_years", "height", "weight", "ap_hi", "ap_lo", "bmi")

png("../figures/outlier_analysis.png", width = 1800, height = 1200, res = 300)
par(mfrow = c(2, 3))
for (col in numerical_cols) {
  Q1 <- quantile(df[[col]], 0.25, na.rm = TRUE)
  Q3 <- quantile(df[[col]], 0.75, na.rm = TRUE)
  IQR <- Q3 - Q1
  lower_bound <- Q1 - 1.5 * IQR
  upper_bound <- Q3 + 1.5 * IQR
  
  outliers <- sum(df[[col]] < lower_bound | df[[col]] > upper_bound, na.rm = TRUE)
  cat("\n", toupper(col), ":\n", sep="")
  cat("  Outliers:", outliers, "(", round(outliers/nrow(df)*100, 2), "%)\n")
  cat("  Lower bound:", lower_bound, "\n")
  cat("  Upper bound:", upper_bound, "\n")
  
  boxplot(df[[col]], main = paste(toupper(col), "- Box Plot"),
          ylab = col, col = "steelblue", border = "black")
  grid(nx = NA, ny = NULL)
}
dev.off()

# ============================================================================
# DISTRIBUTION ANALYSIS
# ============================================================================

cat("\n", "=", rep("=", 78), "\n", sep="")
cat("DISTRIBUTION ANALYSIS\n")
cat("=", rep("=", 78), "\n", sep="")

png("../figures/distribution_analysis.png", width = 1800, height = 1200, res = 300)
par(mfrow = c(2, 3))
for (col in numerical_cols) {
  hist(df[[col]], breaks = 50, probability = TRUE,
       main = paste(toupper(col), "Distribution"),
       xlab = col, col = "steelblue", border = "black")
  
  # Normal distribution overlay
  x <- seq(min(df[[col]], na.rm = TRUE), max(df[[col]], na.rm = TRUE), length = 100)
  lines(x, dnorm(x, mean = mean(df[[col]], na.rm = TRUE), 
                 sd = sd(df[[col]], na.rm = TRUE)), col = "red", lwd = 2)
  
  # Statistics
  if (require(moments, quietly = TRUE)) {
    skewness_val <- skewness(df[[col]], na.rm = TRUE)
    kurtosis_val <- kurtosis(df[[col]], na.rm = TRUE)
  } else {
    skewness_val <- NA
    kurtosis_val <- NA
  }
  legend("topright", 
         legend = c(paste("Skew:", round(skewness_val, 2)),
                   paste("Kurtosis:", round(kurtosis_val, 2))),
         bty = "n", bg = "wheat")
  grid()
}
dev.off()

# ============================================================================
# RELATIONSHIP ANALYSIS
# ============================================================================

cat("\n", "=", rep("=", 78), "\n", sep="")
cat("RELATIONSHIP ANALYSIS\n")
cat("=", rep("=", 78), "\n", sep="")

correlation_cols <- c("age_years", "height", "weight", "ap_hi", "ap_lo", "bmi", "cardio")
correlation_matrix <- cor(df[correlation_cols], use = "complete.obs")

png("../figures/relationship_correlation.png", width = 1200, height = 1000, res = 300)
corrplot(correlation_matrix, method = "color", type = "upper",
         order = "hclust", tl.cex = 0.8, tl.col = "black",
         addCoef.col = "black", number.cex = 0.7,
         title = "Correlation Matrix")
dev.off()

cat("\nCorrelation with target variable (cardio):\n")
cardio_corr <- sort(correlation_matrix["cardio", ], decreasing = TRUE)
print(cardio_corr)

# ============================================================================
# TARGET VARIABLE ANALYSIS
# ============================================================================

cat("\n", "=", rep("=", 78), "\n", sep="")
cat("TARGET VARIABLE ANALYSIS\n")
cat("=", rep("=", 78), "\n", sep="")

# Distribution
png("../figures/target_distribution.png", width = 1000, height = 600, res = 300)
cardio_counts <- table(df$cardio)
barplot(cardio_counts, names.arg = c("No (0)", "Yes (1)"),
        col = c("skyblue", "salmon"), border = "black",
        main = "Distribution of Target Variable (Cardio)",
        xlab = "Cardiovascular Disease", ylab = "Count")
text(barplot(cardio_counts, plot = FALSE), cardio_counts + 500,
     labels = paste0(cardio_counts, "\n(", round(cardio_counts/nrow(df)*100, 2), "%)"),
     pos = 3, font = 2)
grid(nx = NA, ny = NULL)
dev.off()

# Comparison by target variable
png("../figures/target_comparison.png", width = 1800, height = 1200, res = 300)
par(mfrow = c(2, 3))
for (col in numerical_cols) {
  boxplot(df[[col]] ~ df$cardio,
          main = paste(toupper(col), "by Cardio Status"),
          xlab = "Cardiovascular Disease", ylab = col,
          col = c("skyblue", "salmon"), border = "black")
  grid(nx = NA, ny = NULL)
}
dev.off()

# ============================================================================
# FEATURE ENGINEERING INSIGHTS
# ============================================================================

cat("\n", "=", rep("=", 78), "\n", sep="")
cat("FEATURE ENGINEERING INSIGHTS\n")
cat("=", rep("=", 78), "\n", sep="")

# Blood pressure categories
df$bp_category <- cut(df$ap_hi, breaks = c(0, 120, 140, 160, 300),
                      labels = c("Normal", "Elevated", "High Stage 1", "High Stage 2"))
cat("\nBlood Pressure Categories:\n")
print(table(df$bp_category))

# BMI categories
df$bmi_category <- cut(df$bmi, breaks = c(0, 18.5, 25, 30, 100),
                       labels = c("Underweight", "Normal", "Overweight", "Obese"))
cat("\nBMI Categories:\n")
print(table(df$bmi_category))

# Age groups
df$age_group <- cut(df$age_years, breaks = c(0, 30, 40, 50, 60, 100),
                    labels = c("<30", "30-40", "40-50", "50-60", "60+"))
cat("\nAge Groups:\n")
print(table(df$age_group))

cat("\nComprehensive EDA completed successfully!\n")

