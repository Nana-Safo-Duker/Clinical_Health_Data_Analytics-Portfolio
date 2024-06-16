# Univariate, Bivariate, and Multivariate Analysis Script
# This script performs comprehensive analysis at different variable levels.

# Load libraries
library(dplyr)
library(ggplot2)
library(tidyr)
library(lubridate)
library(corrplot)
library(gridExtra)
library(moments)

# Helper function
`%+%` <- function(a, b) paste0(a, b)

# Load and preprocess data
load_and_preprocess_data <- function(file_path) {
  df <- read.csv(file_path, stringsAsFactors = FALSE)
  df$TreatmentStart <- as.Date(df$TreatmentStart, format = "%m/%d/%y")
  df$Year <- year(df$TreatmentStart)
  df$Month <- month(df$TreatmentStart)
  df$Day <- day(df$TreatmentStart)
  df$MonthName <- month.name[df$Month]
  df$Weekday <- weekdays(df$TreatmentStart)
  return(df)
}

# Univariate Analysis
univariate_analysis <- function(df, output_dir = "outputs") {
  cat("=" %+% rep("=", 59), "\n")
  cat("UNIVARIATE ANALYSIS\n")
  cat("=" %+% rep("=", 59), "\n")
  
  # Numerical variable analysis
  cat("\n1. Dosage (Numerical Variable):\n")
  print(summary(df$Dosage))
  cat("Skewness:", skewness(df$Dosage), "\n")
  cat("Kurtosis:", kurtosis(df$Dosage), "\n")
  
  # Categorical variable analysis
  cat("\n2. Drug (Categorical Variable):\n")
  print(table(df$Drug))
  cat("Proportions:\n")
  print(prop.table(table(df$Drug)) * 100)
  
  # Visualizations
  png(paste0(output_dir, "/univariate_analysis.png"), width = 1200, height = 800)
  
  p1 <- ggplot(df, aes(x = Dosage)) +
    geom_histogram(bins = 15, fill = "steelblue", alpha = 0.7, color = "black") +
    geom_vline(aes(xintercept = mean(Dosage)), color = "red", linetype = "dashed") +
    geom_vline(aes(xintercept = median(Dosage)), color = "green", linetype = "dashed") +
    labs(title = "Dosage Distribution", x = "Dosage", y = "Frequency") + theme_minimal()
  
  p2 <- ggplot(df, aes(y = Dosage)) +
    geom_boxplot() +
    labs(title = "Box Plot: Dosage", y = "Dosage") + theme_minimal()
  
  drug_counts <- table(df$Drug)
  p3 <- ggplot(data.frame(Drug = names(drug_counts), Count = as.numeric(drug_counts)),
               aes(x = Drug, y = Count)) +
    geom_bar(stat = "identity", fill = c("steelblue", "coral")) +
    labs(title = "Drug Distribution", x = "Drug", y = "Count") + theme_minimal()
  
  p4 <- ggplot(df, aes(sample = Dosage)) +
    stat_qq() + stat_qq_line() +
    labs(title = "Q-Q Plot: Normality Check") + theme_minimal()
  
  grid.arrange(p1, p2, p3, p4, nrow = 2, ncol = 2)
  dev.off()
  
  cat("\nVisualizations saved to", paste0(output_dir, "/univariate_analysis.png"), "\n")
}

# Bivariate Analysis
bivariate_analysis <- function(df, output_dir = "outputs") {
  cat("\n" %+% "=" %+% rep("=", 59), "\n")
  cat("BIVARIATE ANALYSIS\n")
  cat("=" %+% rep("=", 59), "\n")
  
  # Dosage vs Drug
  cat("\n1. Dosage vs Drug:\n")
  print(df %>% group_by(Drug) %>% summarise(
    Mean = mean(Dosage),
    Median = median(Dosage),
    SD = sd(Dosage),
    Min = min(Dosage),
    Max = max(Dosage)
  ))
  
  # Correlation analysis
  df_encoded <- df
  df_encoded$Drug_encoded <- ifelse(df_encoded$Drug == "Cisplatin", 0, 1)
  corr_matrix <- cor(df_encoded[, c("Dosage", "Drug_encoded", "Month")])
  cat("\n2. Correlation Matrix:\n")
  print(corr_matrix)
  
  # Chi-square test
  contingency_table <- table(df$Drug, df$MonthName)
  chi2_test <- chisq.test(contingency_table)
  cat("\n3. Chi-square test for Drug-Month association:\n")
  cat("   Chi-square:", chi2_test$statistic, ", p-value:", chi2_test$p.value, "\n")
  
  # Visualizations
  png(paste0(output_dir, "/bivariate_analysis.png"), width = 1200, height = 800)
  
  p1 <- ggplot(df, aes(x = Drug, y = Dosage)) +
    geom_boxplot() +
    labs(title = "Dosage by Drug") + theme_minimal()
  
  p2 <- corrplot(corr_matrix, method = "color", type = "upper",
                 addCoef.col = "black", tl.col = "black", tl.srt = 45)
  
  p3 <- ggplot(df_encoded, aes(x = Month, y = Dosage, color = factor(Drug_encoded))) +
    geom_point(alpha = 0.6, size = 3) +
    scale_color_manual(values = c("0" = "blue", "1" = "red"),
                       labels = c("0" = "Cisplatin", "1" = "Nivolumab")) +
    labs(title = "Month vs Dosage (colored by Drug)",
         x = "Month", y = "Dosage", color = "Drug") + theme_minimal()
  
  month_order <- month.name[1:6]
  drug_month <- table(df$MonthName, df$Drug)
  p4 <- ggplot(as.data.frame(drug_month), aes(x = Var1, y = Var2, fill = Freq)) +
    geom_tile() +
    scale_fill_gradient(low = "white", high = "red") +
    labs(title = "Drug Usage by Month", x = "Month", y = "Drug", fill = "Count") +
    theme_minimal() +
    theme(axis.text.x = element_text(angle = 45, hjust = 1))
  
  grid.arrange(p1, p3, p4, nrow = 2, ncol = 2)
  dev.off()
  
  cat("\nVisualizations saved to", paste0(output_dir, "/bivariate_analysis.png"), "\n")
}

# Multivariate Analysis
multivariate_analysis <- function(df, output_dir = "outputs") {
  cat("\n" %+% "=" %+% rep("=", 59), "\n")
  cat("MULTIVARIATE ANALYSIS\n")
  cat("=" %+% rep("=", 59), "\n")
  
  # Mean dosage by Drug and Month
  month_order <- month.name[1:6]
  drug_month_mean <- df %>%
    group_by(Drug, MonthName) %>%
    summarise(Mean_Dosage = mean(Dosage)) %>%
    pivot_wider(names_from = MonthName, values_from = Mean_Dosage) %>%
    select(Drug, all_of(month_order))
  
  cat("\n1. Mean Dosage by Drug and Month:\n")
  print(drug_month_mean)
  
  cat("\n2. Summary Statistics by Drug and Month:\n")
  print(df %>% group_by(Drug, MonthName) %>%
    summarise(
      Mean = mean(Dosage),
      Median = median(Dosage),
      SD = sd(Dosage),
      Count = n()
    ))
  
  # Visualizations
  png(paste0(output_dir, "/multivariate_analysis.png"), width = 1200, height = 800)
  
  drug_month_long <- df %>%
    group_by(Drug, MonthName) %>%
    summarise(Mean_Dosage = mean(Dosage))
  
  p1 <- ggplot(drug_month_long, aes(x = Drug, y = Mean_Dosage, fill = MonthName)) +
    geom_bar(stat = "identity", position = "dodge") +
    labs(title = "Mean Dosage by Drug and Month", x = "Drug", y = "Mean Dosage") +
    theme_minimal()
  
  drug_month_matrix <- as.matrix(drug_month_mean[, -1])
  rownames(drug_month_matrix) <- drug_month_mean$Drug
  
  p2 <- corrplot(drug_month_matrix, is.corr = FALSE, method = "color",
                 tl.col = "black", tl.srt = 45, title = "Mean Dosage Heatmap")
  
  p3 <- ggplot(df, aes(x = Dosage, fill = Drug)) +
    geom_histogram(alpha = 0.6, bins = 10, position = "identity") +
    labs(title = "Dosage Distribution by Drug", x = "Dosage", y = "Frequency") +
    theme_minimal()
  
  df_encoded <- df
  df_encoded$Drug_encoded <- ifelse(df_encoded$Drug == "Cisplatin", 0, 1)
  p4 <- ggplot(df_encoded, aes(x = Month, y = Dosage, color = factor(Drug_encoded),
                               size = Dosage)) +
    geom_point(alpha = 0.6) +
    scale_color_manual(values = c("0" = "blue", "1" = "red"),
                       labels = c("0" = "Cisplatin", "1" = "Nivolumab")) +
    labs(title = "Multivariate View: Month vs Dosage",
         x = "Month", y = "Dosage", color = "Drug") + theme_minimal()
  
  grid.arrange(p1, p3, p4, nrow = 2, ncol = 2)
  dev.off()
  
  cat("\nVisualizations saved to", paste0(output_dir, "/multivariate_analysis.png"), "\n")
}

# Main function
main <- function() {
  # Create output directory
  if (!dir.exists("outputs")) {
    dir.create("outputs")
  }
  
  # Load data
  file_path <- "../../data/mock_treatment_starts_2016.csv"
  df <- load_and_preprocess_data(file_path)
  
  # Perform analyses
  univariate_analysis(df)
  bivariate_analysis(df)
  multivariate_analysis(df)
  
  cat("\n" %+% "=" %+% rep("=", 59), "\n")
  cat("ANALYSIS COMPLETE\n")
  cat("=" %+% rep("=", 59), "\n")
}

# Run main function
if (!interactive()) {
  main()
}


