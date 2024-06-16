# Univariate, Bivariate, and Multivariate Analysis
# Comprehensive analysis of health data

# Load libraries
library(ggplot2)
library(dplyr)
library(corrplot)
library(GGally)

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
# 1. UNIVARIATE ANALYSIS
# ============================================================================

cat("=", rep("=", 78), "\n", sep="")
cat("UNIVARIATE ANALYSIS\n")
cat("=", rep("=", 78), "\n", sep="")

numerical_cols <- c("age_years", "height", "weight", "ap_hi", "ap_lo", "bmi")

# Histograms and density plots
png("../figures/univariate_numerical.png", width = 1800, height = 1200, res = 300)
par(mfrow = c(2, 3))
for (col in numerical_cols) {
  hist(df[[col]], breaks = 50, probability = TRUE, 
       main = paste(toupper(col), "Distribution"),
       xlab = col, col = "steelblue", border = "black")
  lines(density(df[[col]]), col = "red", lwd = 2)
}
dev.off()

# Categorical variables
categorical_cols <- c("gender", "cholesterol", "gluc", "smoke", "alco", "active", "cardio")

png("../figures/univariate_categorical.png", width = 1800, height = 1500, res = 300)
par(mfrow = c(3, 3))
for (col in categorical_cols) {
  value_counts <- table(df[[col]])
  barplot(value_counts, main = paste(toupper(col), "Distribution"),
          xlab = col, ylab = "Count", col = "steelblue", border = "black")
}
dev.off()

# ============================================================================
# 2. BIVARIATE ANALYSIS
# ============================================================================

cat("=", rep("=", 78), "\n", sep="")
cat("BIVARIATE ANALYSIS\n")
cat("=", rep("=", 78), "\n", sep="")

# Scatter plots
pairs_list <- list(
  c("age_years", "bmi"),
  c("ap_hi", "ap_lo"),
  c("weight", "height"),
  c("ap_hi", "bmi")
)

png("../figures/bivariate_scatter.png", width = 1600, height = 1200, res = 300)
par(mfrow = c(2, 2))
for (pair in pairs_list) {
  x <- pair[1]
  y <- pair[2]
  plot(df[[x]], df[[y]], pch = 19, cex = 0.3, alpha = 0.5,
       main = paste(toupper(x), "vs", toupper(y)),
       xlab = x, ylab = y)
  corr_val <- cor(df[[x]], df[[y]], use = "complete.obs")
  legend("topright", legend = paste("r =", round(corr_val, 3)), 
         bty = "n", bg = "wheat")
  grid()
}
dev.off()

# Box plots
comparisons <- list(
  c("bmi", "cardio"),
  c("age_years", "cardio"),
  c("ap_hi", "cardio"),
  c("bmi", "gender"),
  c("ap_hi", "cholesterol"),
  c("bmi", "smoke")
)

png("../figures/bivariate_boxplots.png", width = 1800, height = 1200, res = 300)
par(mfrow = c(2, 3))
for (comp in comparisons) {
  numerical <- comp[1]
  categorical <- comp[2]
  boxplot(df[[numerical]] ~ df[[categorical]],
          main = paste(toupper(numerical), "by", toupper(categorical)),
          xlab = categorical, ylab = numerical,
          col = "steelblue", border = "black")
  grid(nx = NA, ny = NULL)
}
dev.off()

# Heatmaps
categorical_vars <- c("gender", "cholesterol", "gluc", "smoke", "alco", "active")

png("../figures/bivariate_heatmaps.png", width = 1800, height = 1200, res = 300)
par(mfrow = c(2, 3))
for (var in categorical_vars) {
  crosstab <- prop.table(table(df[[var]], df$cardio), margin = 1) * 100
  heatmap(crosstab, main = paste(toupper(var), "vs Cardio"),
          xlab = "Cardio", ylab = var, col = heat.colors(256),
          Rowv = NA, Colv = NA)
}
dev.off()

# ============================================================================
# 3. MULTIVARIATE ANALYSIS
# ============================================================================

cat("=", rep("=", 78), "\n", sep="")
cat("MULTIVARIATE ANALYSIS\n")
cat("=", rep("=", 78), "\n", sep="")

# Correlation matrix
numerical_cols <- c("age_years", "height", "weight", "ap_hi", "ap_lo", "bmi", "cardio")
correlation_matrix <- cor(df[numerical_cols], use = "complete.obs")

png("../figures/multivariate_correlation.png", width = 1200, height = 1000, res = 300)
corrplot(correlation_matrix, method = "color", type = "upper",
         order = "hclust", tl.cex = 0.8, tl.col = "black",
         addCoef.col = "black", number.cex = 0.7,
         title = "Multivariate Correlation Matrix")
dev.off()

# Pair plot
key_vars <- c("age_years", "bmi", "ap_hi", "ap_lo", "cardio")
pair_df <- df[sample(nrow(df), min(5000, nrow(df))), key_vars]
pair_df$cardio <- as.factor(pair_df$cardio)

png("../figures/multivariate_pairplot.png", width = 2000, height = 2000, res = 300)
ggpairs(pair_df, aes(color = cardio, alpha = 0.7),
        lower = list(continuous = "points"),
        upper = list(continuous = "cor"),
        diag = list(continuous = "densityDiag"))
dev.off()

cat("\nUnivariate, bivariate, and multivariate analysis completed successfully!\n")

