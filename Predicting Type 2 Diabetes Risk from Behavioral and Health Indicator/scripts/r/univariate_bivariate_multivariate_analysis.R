# Univariate, Bivariate, and Multivariate Analysis
# Diabetes Binary Health Indicators - BRFSS 2021

# Load required libraries
library(ggplot2)
library(dplyr)
library(corrplot)
library(gridExtra)

# Set working directory
setwd("../../")

# Load data
df <- read.csv("data/diabetes_binary_health_indicators_BRFSS2021.csv")

cat("Dataset shape:", dim(df), "\n")

# Univariate Analysis
cat("\n=== UNIVARIATE ANALYSIS ===\n")
numerical_cols <- c("BMI", "GenHlth", "MentHlth", "PhysHlth", "Age", "Education", "Income")

univariate_summary <- data.frame(
  Variable = character(),
  Mean = numeric(),
  Median = numeric(),
  SD = numeric(),
  Skewness = numeric(),
  Min = numeric(),
  Max = numeric(),
  IQR = numeric(),
  stringsAsFactors = FALSE
)

for (col in numerical_cols) {
  if (col %in% colnames(df)) {
    data <- df[[col]]
    univariate_summary <- rbind(univariate_summary, data.frame(
      Variable = col,
      Mean = mean(data, na.rm = TRUE),
      Median = median(data, na.rm = TRUE),
      SD = sd(data, na.rm = TRUE),
      Skewness = moments::skewness(data, na.rm = TRUE),
      Min = min(data, na.rm = TRUE),
      Max = max(data, na.rm = TRUE),
      IQR = IQR(data, na.rm = TRUE)
    ))
  }
}
print(univariate_summary)

# Univariate visualizations
png("results/figures/univariate_numerical_r.png", width = 1800, height = 1500, res = 300)
par(mfrow = c(3, 3))
for (col in numerical_cols[1:min(9, length(numerical_cols))]) {
  if (col %in% colnames(df)) {
    hist(df[[col]], main = paste(col, "- Distribution"), xlab = col, 
         col = "steelblue", border = "black", breaks = 30)
    abline(v = mean(df[[col]], na.rm = TRUE), col = "red", lty = 2, lwd = 2)
  }
}
dev.off()

# Bivariate Analysis
cat("\n=== BIVARIATE ANALYSIS ===\n")
correlation_results <- data.frame(
  Variable = character(),
  Pearson_r = numeric(),
  p_value = numeric(),
  Significant = character(),
  stringsAsFactors = FALSE
)

for (col in numerical_cols) {
  if (col %in% colnames(df) && col != "Diabetes_binary") {
    cor_test <- cor.test(df[[col]], df$Diabetes_binary, use = "complete.obs")
    correlation_results <- rbind(correlation_results, data.frame(
      Variable = col,
      Pearson_r = cor_test$estimate,
      p_value = cor_test$p.value,
      Significant = ifelse(cor_test$p.value < 0.05, "Yes", "No")
    ))
  }
}
print(correlation_results)

# Box plots
png("results/figures/bivariate_numerical_vs_target_r.png", width = 1800, height = 1500, res = 300)
par(mfrow = c(3, 3))
for (col in numerical_cols[1:min(9, length(numerical_cols))]) {
  if (col %in% colnames(df) && col != "Diabetes_binary") {
    boxplot(df[[col]] ~ df$Diabetes_binary, 
            main = paste(col, "by Diabetes Status"),
            xlab = "Diabetes (0=No, 1=Yes)",
            ylab = col,
            col = c("skyblue", "salmon"))
  }
}
dev.off()

# Multivariate Analysis
cat("\n=== MULTIVARIATE ANALYSIS ===\n")
numerical_df <- df[, sapply(df, is.numeric)]
correlation_matrix <- cor(numerical_df, use = "complete.obs")

# Correlation heatmap
png("results/figures/multivariate_correlation_heatmap_r.png", width = 1600, height = 1200, res = 300)
corrplot(correlation_matrix, method = "color", type = "upper", 
         order = "hclust", tl.cex = 0.7, tl.col = "black")
dev.off()

# Multivariate group analysis
df$BMI_Category <- cut(df$BMI, breaks = c(0, 18.5, 25, 30, 100),
                       labels = c("Underweight", "Normal", "Overweight", "Obese"))

multi_group <- df %>%
  group_by(HighBP, HighChol) %>%
  summarise(
    Diabetes_Rate = mean(Diabetes_binary, na.rm = TRUE) * 100,
    Count = n(),
    .groups = "drop"
  )
print(multi_group)

# Heatmap for multivariate categorical analysis
pivot_table <- df %>%
  group_by(HighBP, HighChol) %>%
  summarise(Diabetes_Rate = mean(Diabetes_binary, na.rm = TRUE) * 100, .groups = "drop") %>%
  pivot_wider(names_from = HighChol, values_from = Diabetes_Rate)

png("results/figures/multivariate_heatmap_bp_chol_r.png", width = 1000, height = 600, res = 300)
heatmap(as.matrix(pivot_table[, -1]), 
        main = "Diabetes Prevalence by HighBP and HighChol",
        xlab = "HighChol (0=No, 1=Yes)",
        ylab = "HighBP (0=No, 1=Yes)",
        col = heat.colors(100))
dev.off()

cat("\n=== ANALYSIS COMPLETE ===\n")

