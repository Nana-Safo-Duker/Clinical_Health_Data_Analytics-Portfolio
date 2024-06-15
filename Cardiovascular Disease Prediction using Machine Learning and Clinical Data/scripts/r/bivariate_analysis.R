# Bivariate Analysis
#
# This script performs bivariate analysis on the Cardiovascular Disease Dataset.

# Load necessary libraries
library(tidyverse)
library(ggplot2)
library(dplyr)
library(corrplot)
library(gridExtra)

# Set theme for plots
theme_set(theme_minimal() + theme(plot.title = element_text(size = 14, face = "bold")))

# Load the dataset
df <- read.csv("../../data/Cardiovascular_Disease_Dataset.csv", stringsAsFactors = FALSE)

# Correlation Analysis
cat(paste(rep("=", 80), collapse = ""), "\n")
cat("CORRELATION ANALYSIS\n")
cat(paste(rep("=", 80), collapse = ""), "\n")

numerical_cols <- c("age", "restingBP", "serumcholestrol", "maxheartrate", "oldpeak")
correlation_matrix <- cor(df[numerical_cols], use = "complete.obs")

cat("\nCorrelation Matrix:\n")
print(round(correlation_matrix, 3))

# Save correlation plot
png("../../results/correlation_matrix.png", width = 800, height = 600)
corrplot(correlation_matrix, method = "color", type = "upper", 
         order = "hclust", tl.cex = 0.8, tl.col = "black",
         addCoef.col = "black", number.cex = 0.7)
dev.off()

# Numerical vs Target
cat("\n\n", paste(rep("=", 80), collapse = ""), "\n")
cat("NUMERICAL VARIABLES VS TARGET\n")
cat(paste(rep("=", 80), collapse = ""), "\n")

for (col in numerical_cols) {
  if (col %in% names(df)) {
    cat("\n", toupper(col), "by Target:\n")
    grouped <- df %>%
      group_by(target) %>%
      summarise(
        mean = mean(.data[[col]], na.rm = TRUE),
        median = median(.data[[col]], na.rm = TRUE),
        sd = sd(.data[[col]], na.rm = TRUE)
      )
    print(grouped)
    
    # Statistical test
    group_0 <- df[df$target == 0, col]
    group_1 <- df[df$target == 1, col]
    test_result <- t.test(group_0, group_1)
    cat("  t-test p-value:", test_result$p.value, 
        ifelse(test_result$p.value < 0.05, "(Significant)", "(Not significant)"), "\n")
  }
}

# Categorical vs Target
cat("\n\n", paste(rep("=", 80), collapse = ""), "\n")
cat("CATEGORICAL VARIABLES VS TARGET\n")
cat(paste(rep("=", 80), collapse = ""), "\n")

categorical_vars <- c("gender", "chestpain", "fastingbloodsugar", "restingrelectro", 
                     "exerciseangia", "slope", "noofmajorvessels")

for (var in categorical_vars) {
  if (var %in% names(df)) {
    cat("\n", toupper(var), "vs TARGET:\n")
    crosstab <- table(df[[var]], df$target)
    print(crosstab)
    
    # Chi-square test
    test_result <- chisq.test(crosstab)
    cat("  Chi-square p-value:", test_result$p.value, 
        ifelse(test_result$p.value < 0.05, "(Significant)", "(Not significant)"), "\n")
  }
}

# Visualize relationships
plots_list <- list()
for (col in numerical_cols) {
  if (col %in% names(df)) {
    p <- ggplot(df, aes_string(x = "factor(target)", y = col, fill = "factor(target)")) +
      geom_violin(alpha = 0.7) +
      scale_fill_manual(values = c("skyblue", "coral"), labels = c("No Disease", "Disease")) +
      labs(title = paste(col, "by Target"),
           x = "Target",
           y = col,
           fill = "Target") +
      theme_minimal() +
      theme(legend.position = "none")
    plots_list[[col]] <- p
  }
}

# Save plots
png("../../results/bivariate_analysis.png", width = 1200, height = 800)
do.call(grid.arrange, c(plots_list, ncol = 2))
dev.off()

cat("\nBivariate analysis complete!\n")

