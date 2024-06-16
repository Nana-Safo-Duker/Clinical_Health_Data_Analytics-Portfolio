# Comprehensive Exploratory Data Analysis Script
# This script performs thorough exploratory data analysis of the treatment starts dataset.

# Load libraries
library(dplyr)
library(ggplot2)
library(tidyr)
library(lubridate)
library(gridExtra)
library(moments)
library(VIM)

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
  df$Quarter <- quarter(df$TreatmentStart)
  return(df)
}

# Data quality assessment
data_quality_assessment <- function(df) {
  cat("=" %+% rep("=", 59), "\n")
  cat("DATA QUALITY ASSESSMENT\n")
  cat("=" %+% rep("=", 59), "\n")
  
  cat("\nDataset shape:", dim(df), "\n")
  cat("Missing values:\n")
  print(colSums(is.na(df)))
  cat("Date range:", min(df$TreatmentStart), "to", max(df$TreatmentStart), "\n")
  
  # Outlier detection
  Q1 <- quantile(df$Dosage, 0.25)
  Q3 <- quantile(df$Dosage, 0.75)
  IQR_val <- IQR(df$Dosage)
  outliers <- df[df$Dosage < (Q1 - 1.5*IQR_val) | df$Dosage > (Q3 + 1.5*IQR_val), ]
  cat("\nOutliers detected:", nrow(outliers), "\n")
  if (nrow(outliers) > 0) {
    cat("Outlier details:\n")
    print(outliers[, c("PatientID", "Drug", "Dosage")])
  }
  
  return(outliers)
}

# Descriptive statistics
descriptive_statistics <- function(df) {
  cat("\n" %+% "=" %+% rep("=", 59), "\n")
  cat("DESCRIPTIVE STATISTICS\n")
  cat("=" %+% rep("=", 59), "\n")
  
  cat("\nNumerical variables:\n")
  print(summary(df$Dosage))
  cat("Skewness:", skewness(df$Dosage), "\n")
  cat("Kurtosis:", kurtosis(df$Dosage), "\n")
  
  cat("\nCategorical variables:\n")
  cat("Drug distribution:\n")
  print(table(df$Drug))
  cat("Proportions:\n")
  print(prop.table(table(df$Drug)) * 100)
}

# Temporal analysis
temporal_analysis <- function(df, output_dir = "outputs") {
  cat("\n" %+% "=" %+% rep("=", 59), "\n")
  cat("TEMPORAL ANALYSIS\n")
  cat("=" %+% rep("=", 59), "\n")
  
  month_order <- month.name[1:6]
  monthly_counts <- df %>%
    group_by(MonthName) %>%
    summarise(Count = n()) %>%
    arrange(match(MonthName, month_order))
  
  cat("\nTreatment starts by month:\n")
  print(monthly_counts)
  
  cat("\nMean dosage by month:\n")
  mean_dosage_month <- df %>%
    group_by(MonthName) %>%
    summarise(Mean_Dosage = mean(Dosage)) %>%
    arrange(match(MonthName, month_order))
  print(mean_dosage_month)
  
  # Visualizations
  png(paste0(output_dir, "/temporal_analysis.png"), width = 1200, height = 800)
  
  p1 <- ggplot(monthly_counts, aes(x = MonthName, y = Count)) +
    geom_bar(stat = "identity", fill = "steelblue") +
    labs(title = "Treatment Starts by Month", x = "Month", y = "Count") +
    theme_minimal() +
    theme(axis.text.x = element_text(angle = 45, hjust = 1))
  
  p2 <- ggplot(mean_dosage_month, aes(x = MonthName, y = Mean_Dosage)) +
    geom_line(group = 1, color = "teal", size = 1) +
    geom_point(color = "teal", size = 3) +
    labs(title = "Mean Dosage by Month", x = "Month", y = "Mean Dosage") +
    theme_minimal() +
    theme(axis.text.x = element_text(angle = 45, hjust = 1))
  
  df_sorted <- df[order(df$TreatmentStart), ]
  df_sorted$Cumulative <- 1:nrow(df_sorted)
  p3 <- ggplot(df_sorted, aes(x = TreatmentStart, y = Cumulative)) +
    geom_line() +
    geom_point(size = 2) +
    labs(title = "Treatment Starts Timeline", x = "Date", y = "Cumulative Count") +
    theme_minimal() +
    theme(axis.text.x = element_text(angle = 45, hjust = 1))
  
  drug_month <- table(df$MonthName, df$Drug)
  p4 <- ggplot(as.data.frame(drug_month), aes(x = Var1, y = Var2, fill = Freq)) +
    geom_tile() +
    scale_fill_gradient(low = "white", high = "red") +
    labs(title = "Drug Usage by Month", x = "Month", y = "Drug", fill = "Count") +
    theme_minimal() +
    theme(axis.text.x = element_text(angle = 45, hjust = 1))
  
  grid.arrange(p1, p2, p3, p4, nrow = 2, ncol = 2)
  dev.off()
}

# Relationship analysis
relationship_analysis <- function(df, output_dir = "outputs") {
  cat("\n" %+% "=" %+% rep("=", 59), "\n")
  cat("RELATIONSHIP ANALYSIS\n")
  cat("=" %+% rep("=", 59), "\n")
  
  # Correlation
  df_encoded <- df
  df_encoded$Drug_encoded <- ifelse(df_encoded$Drug == "Cisplatin", 0, 1)
  corr_matrix <- cor(df_encoded[, c("Dosage", "Drug_encoded", "Month")])
  
  cat("\nCorrelation matrix:\n")
  print(corr_matrix)
  
  # Visualizations
  png(paste0(output_dir, "/relationship_analysis.png"), width = 1200, height = 800)
  
  p1 <- ggplot(df, aes(x = Drug, y = Dosage)) +
    geom_boxplot() +
    labs(title = "Dosage Distribution by Drug") + theme_minimal()
  
  library(corrplot)
  corrplot(corr_matrix, method = "color", type = "upper",
           addCoef.col = "black", tl.col = "black", tl.srt = 45)
  
  p3 <- ggplot(df_encoded, aes(x = Month, y = Dosage, color = factor(Drug_encoded))) +
    geom_point(alpha = 0.6, size = 3) +
    scale_color_manual(values = c("0" = "blue", "1" = "red"),
                       labels = c("0" = "Cisplatin", "1" = "Nivolumab")) +
    labs(title = "Month vs Dosage (colored by Drug)",
         x = "Month", y = "Dosage", color = "Drug") + theme_minimal()
  
  p4 <- ggplot(df, aes(x = Dosage, fill = Drug)) +
    geom_histogram(alpha = 0.6, bins = 10, position = "identity") +
    labs(title = "Dosage Distribution by Drug", x = "Dosage", y = "Frequency") +
    theme_minimal()
  
  grid.arrange(p1, p3, p4, nrow = 2, ncol = 2)
  dev.off()
}

# Patient analysis
patient_analysis <- function(df) {
  cat("\n" %+% "=" %+% rep("=", 59), "\n")
  cat("PATIENT ANALYSIS\n")
  cat("=" %+% rep("=", 59), "\n")
  
  patient_stats <- df %>%
    group_by(PatientID) %>%
    summarise(
      Treatment_Count = n(),
      Mean_Dosage = mean(Dosage),
      Total_Dosage = sum(Dosage),
      Min_Dosage = min(Dosage),
      Max_Dosage = max(Dosage)
    )
  
  cat("\nNumber of unique patients:", length(unique(df$PatientID)), "\n")
  cat("Patients with multiple treatments:", 
      sum(patient_stats$Treatment_Count > 1), "\n")
  cat("\nPatient Statistics (top 10):\n")
  print(head(patient_stats[order(patient_stats$Treatment_Count, decreasing = TRUE), ], 10))
}

# Generate summary
generate_summary <- function(df, outliers) {
  cat("\n" %+% "=" %+% rep("=", 59), "\n")
  cat("EDA SUMMARY\n")
  cat("=" %+% rep("=", 59), "\n")
  
  cat("\n1. Dataset Overview:\n")
  cat("   - Total records:", nrow(df), "\n")
  cat("   - Unique patients:", length(unique(df$PatientID)), "\n")
  cat("   - Date range:", min(df$TreatmentStart), "to", max(df$TreatmentStart), "\n")
  
  cat("\n2. Drug Distribution:\n")
  drug_counts <- table(df$Drug)
  for (i in 1:length(drug_counts)) {
    cat("   -", names(drug_counts)[i], ":", drug_counts[i],
        "treatments (", round(drug_counts[i]/nrow(df)*100, 1), "%)\n")
  }
  
  cat("\n3. Dosage Statistics:\n")
  cat("   - Mean:", mean(df$Dosage), "\n")
  cat("   - Median:", median(df$Dosage), "\n")
  cat("   - Std Dev:", sd(df$Dosage), "\n")
  cat("   - Range:", min(df$Dosage), "-", max(df$Dosage), "\n")
  
  cat("\n4. Data Quality:\n")
  cat("   - Missing values:", sum(is.na(df)), "\n")
  cat("   - Outliers detected:", nrow(outliers), "\n")
  
  cat("\n5. Key Findings:\n")
  cat("   - Dataset contains treatment starts for two drugs: Cisplatin and Nivolumab\n")
  cat("   - Some patients have multiple treatment records\n")
  cat("   - Dosage varies significantly between drugs\n")
  cat("   - Treatment patterns show temporal variations\n")
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
  outliers <- data_quality_assessment(df)
  descriptive_statistics(df)
  temporal_analysis(df)
  relationship_analysis(df)
  patient_analysis(df)
  generate_summary(df, outliers)
  
  cat("\n" %+% "=" %+% rep("=", 59), "\n")
  cat("EDA COMPLETE\n")
  cat("=" %+% rep("=", 59), "\n")
}

# Run main function
if (!interactive()) {
  main()
}


