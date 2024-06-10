# ==============================================================================
# AI-Driven Cancer Drug Discovery and Target Identification
# Comprehensive R Script for Statistical Analysis and Visualization
#
# Author: Research Paper Review Project
# Reference: Signal Transduction and Targeted Therapy
#            https://www.nature.com/articles/s41392-022-00994-0
# ==============================================================================

# ------------------------------------------------------------------------------
# 1. SETUP AND LIBRARIES
# ------------------------------------------------------------------------------

# Install packages if needed (uncomment as needed)
# install.packages(c("tidyverse", "ggplot2", "dplyr", "readr", "tidyr",
#                    "reshape2", "viridis", "RColorBrewer", "pheatmap",
#                    "stats", "ggplot2", "corrplot", "factoextra"))

# Load required libraries
library(tidyverse)
library(ggplot2)
library(dplyr)
library(readr)
library(tidyr)
library(reshape2)
library(viridis)
library(RColorBrewer)
library(pheatmap)
library(stats)
library(corrplot)
library(factoextra)
library(here)

# Set theme for ggplot2
theme_set(theme_minimal(base_size = 12) +
          theme(plot.title = element_text(face = "bold", size = 14),
                axis.title = element_text(face = "bold"),
                legend.position = "right"))

# Set random seed for reproducibility
set.seed(42)

# ------------------------------------------------------------------------------
# 2. GENERATE SYNTHETIC GENE EXPRESSION DATA
# ------------------------------------------------------------------------------

#' Generate synthetic gene expression data
#'
#' @param n_genes Number of genes
#' @param n_normal_samples Number of normal samples
#' @param n_cancer_samples Number of cancer samples
#' @param n_differential_genes Number of differentially expressed genes
#' @return List containing data frame and gene names
generate_synthetic_data <- function(n_genes = 200,
                                    n_normal_samples = 100,
                                    n_cancer_samples = 100,
                                    n_differential_genes = 50) {
  
  # Generate gene names
  gene_names <- paste0("Gene_", 1:n_genes)
  
  # Generate normal samples
  normal_data <- matrix(rnorm(n_normal_samples * n_genes, mean = 5, sd = 1.5),
                        nrow = n_normal_samples,
                        ncol = n_genes)
  
  # Generate cancer samples
  cancer_data <- matrix(rnorm(n_cancer_samples * n_genes, mean = 5, sd = 1.5),
                        nrow = n_cancer_samples,
                        ncol = n_genes)
  
  # Create differential expression
  differential_indices <- sample(n_genes, n_differential_genes, replace = FALSE)
  
  # Upregulate half of differential genes
  n_upregulated <- n_differential_genes %/% 2
  upregulated_indices <- differential_indices[1:n_upregulated]
  cancer_data[, upregulated_indices] <- matrix(
    rnorm(n_cancer_samples * length(upregulated_indices), mean = 8, sd = 2),
    nrow = n_cancer_samples,
    ncol = length(upregulated_indices)
  )
  
  # Downregulate remaining differential genes
  downregulated_indices <- differential_indices[(n_upregulated + 1):n_differential_genes]
  cancer_data[, downregulated_indices] <- matrix(
    rnorm(n_cancer_samples * length(downregulated_indices), mean = 2, sd = 1),
    nrow = n_cancer_samples,
    ncol = length(downregulated_indices)
  )
  
  # Combine data
  data <- rbind(normal_data, cancer_data)
  
  # Create data frame
  df <- as.data.frame(data)
  colnames(df) <- gene_names
  df$Sample_Type <- c(rep("Normal", n_normal_samples),
                      rep("Cancer", n_cancer_samples))
  
  return(list(data = df, gene_names = gene_names))
}

# Generate data
data_result <- generate_synthetic_data(
  n_genes = 200,
  n_normal_samples = 100,
  n_cancer_samples = 100,
  n_differential_genes = 50
)

df_gene_exp <- data_result$data
gene_names <- data_result$gene_names

cat("\nGenerated synthetic data:\n")
cat(sprintf("  - Total samples: %d\n", nrow(df_gene_exp)))
cat(sprintf("  - Normal samples: %d\n", sum(df_gene_exp$Sample_Type == "Normal")))
cat(sprintf("  - Cancer samples: %d\n", sum(df_gene_exp$Sample_Type == "Cancer")))
cat(sprintf("  - Genes analyzed: %d\n", length(gene_names)))

# ------------------------------------------------------------------------------
# 3. STATISTICAL ANALYSIS: T-TESTS FOR DIFFERENTIAL EXPRESSION
# ------------------------------------------------------------------------------

#' Perform differential expression analysis using t-tests
#'
#' @param df Data frame with gene expression data
#' @param gene_names Vector of gene names
#' @param control_group Control group name
#' @param treatment_group Treatment group name
#' @return Data frame with test results
perform_differential_expression <- function(df, gene_names,
                                            control_group = "Normal",
                                            treatment_group = "Cancer") {
  
  results <- data.frame(
    Gene = character(),
    Mean_Control = numeric(),
    Mean_Treatment = numeric(),
    Mean_Difference = numeric(),
    T_Statistic = numeric(),
    P_Value = numeric(),
    Cohen_D = numeric(),
    Std_Control = numeric(),
    Std_Treatment = numeric(),
    stringsAsFactors = FALSE
  )
  
  for (gene in gene_names) {
    # Extract data for each group
    control_data <- df %>% filter(Sample_Type == control_group) %>% pull(gene)
    treatment_data <- df %>% filter(Sample_Type == treatment_group) %>% pull(gene)
    
    # Perform t-test
    t_test <- t.test(control_data, treatment_data)
    
    # Calculate effect size (Cohen's d)
    mean_diff <- mean(treatment_data) - mean(control_data)
    pooled_sd <- sqrt((var(control_data) + var(treatment_data)) / 2)
    cohens_d <- mean_diff / pooled_sd
    
    results <- rbind(results, data.frame(
      Gene = gene,
      Mean_Control = mean(control_data),
      Mean_Treatment = mean(treatment_data),
      Mean_Difference = mean_diff,
      T_Statistic = t_test$statistic,
      P_Value = t_test$p.value,
      Cohen_D = cohens_d,
      Std_Control = sd(control_data),
      Std_Treatment = sd(treatment_data),
      stringsAsFactors = FALSE
    ))
  }
  
  # Add significance markers
  results$Significant <- results$P_Value < 0.05
  
  # Bonferroni correction
  num_comparisons <- nrow(results)
  results$FDR_Corrected <- results$P_Value < (0.05 / num_comparisons)
  
  # Sort by P-value
  results <- results %>% arrange(P_Value)
  
  return(results)
}

# Perform analysis
df_tests <- perform_differential_expression(df_gene_exp, gene_names)

cat("\n\nT-test Results Summary:\n")
cat(sprintf("Significant genes (p < 0.05): %d out of %d\n",
            sum(df_tests$Significant), nrow(df_tests)))
cat(sprintf("Significant after Bonferroni correction: %d\n",
            sum(df_tests$FDR_Corrected)))

cat("\nTop 10 Most Significantly Differentially Expressed Genes:\n")
print(df_tests %>% 
      head(10) %>%
      select(Gene, Mean_Control, Mean_Treatment, Mean_Difference, 
             P_Value, Cohen_D, Significant))

# ------------------------------------------------------------------------------
# 4. VISUALIZATIONS: T-TEST RESULTS
# ------------------------------------------------------------------------------

# Create comprehensive visualization
pdf("statistical_analysis_results.pdf", width = 12, height = 10)

# Layout: 2x2 grid
par(mfrow = c(2, 2))

# 1. P-value distribution
hist(df_tests$P_Value, breaks = 50, col = "steelblue", 
     border = "black", main = "Distribution of P-Values",
     xlab = "P-Value", ylab = "Frequency")
abline(v = 0.05, col = "red", lty = 2, lwd = 2)
legend("topright", legend = "p = 0.05 threshold", 
       col = "red", lty = 2, lwd = 2)

# 2. Volcano plot
log_p_values <- -log10(df_tests$P_Value + 1e-300)  # Add small value to avoid log(0)
sig_threshold <- 0.05

colors <- ifelse(df_tests$P_Value < sig_threshold & abs(df_tests$Mean_Difference) > 1,
                 "red", "gray")

plot(df_tests$Mean_Difference, log_p_values,
     col = colors, pch = 19, alpha = 0.6,
     xlab = "Mean Difference (Cancer - Normal)",
     ylab = "-log10(P-Value)",
     main = "Volcano Plot: Differential Gene Expression")
abline(h = -log10(sig_threshold), col = "red", lty = 2, lwd = 2)
abline(v = -1, col = "blue", lty = 2, alpha = 0.5)
abline(v = 1, col = "blue", lty = 2, alpha = 0.5)
grid(alpha = 0.3)

# 3. Top genes by effect size
sig_genes <- df_tests %>% filter(Significant)
if (nrow(sig_genes) > 0) {
  top_genes <- sig_genes %>% arrange(Cohen_D) %>% head(20)
  
  barplot(height = top_genes$Cohen_D,
          names.arg = top_genes$Gene,
          horiz = TRUE, las = 2,
          col = "coral", border = "black",
          xlab = "Cohen's d (Effect Size)",
          main = "Top 20 Genes by Effect Size")
  abline(v = 0, col = "black", lty = 1)
}

# 4. Summary statistics table
summary_stats <- data.frame(
  Statistic = c("Mean", "Median", "Std", "Min", "Max"),
  P_Value = c(mean(df_tests$P_Value),
              median(df_tests$P_Value),
              sd(df_tests$P_Value),
              min(df_tests$P_Value),
              max(df_tests$P_Value))
)

plot.new()
text(x = 0.5, y = 0.5, 
     paste(capture.output(print(summary_stats, row.names = FALSE)), 
           collapse = "\n"),
     family = "monospace", cex = 1.2)
title("P-Value Summary Statistics")

par(mfrow = c(1, 1))

dev.off()
cat("\nSaved statistical_analysis_results.pdf\n")

# ------------------------------------------------------------------------------
# 5. DIMENSIONALITY REDUCTION: PCA
# ------------------------------------------------------------------------------

# Prepare data for PCA
X <- df_gene_exp %>% select(-Sample_Type) %>% as.matrix()

# Standardize data
X_scaled <- scale(X)

# Perform PCA
pca_result <- prcomp(X_scaled, center = FALSE, scale. = FALSE)  # Already scaled

# Calculate explained variance
explained_variance <- summary(pca_result)$importance[2, ]
cumulative_variance <- summary(pca_result)$importance[3, ]

cat("\n\nPCA Results:\n")
cat(sprintf("First 10 components explain %.2f%% of variance\n",
            cumulative_variance[10] * 100))
cat(sprintf("First 20 components explain %.2f%% of variance\n",
            cumulative_variance[20] * 100))

# Visualize PCA
pdf("pca_visualization.pdf", width = 14, height = 10)

# Layout: 2x2 grid
par(mfrow = c(2, 2))

# 1. Scree plot (explained variance)
barplot(explained_variance[1:20], col = "teal", border = "black",
        main = "PCA: Explained Variance by Component",
        xlab = "Principal Component",
        ylab = "Explained Variance Ratio")
lines(cumulative_variance[1:20], col = "red", lwd = 2, type = "o", pch = 19)
abline(h = 0.95, col = "red", lty = 2, alpha = 0.5)
legend("right", legend = "Cumulative", col = "red", lty = 1, lwd = 2)

# 2. PCA scatter plot (PC1 vs PC2)
sample_types <- df_gene_exp$Sample_Type
colors_pca <- ifelse(sample_types == "Normal", "steelblue", "crimson")

plot(pca_result$x[, 1], pca_result$x[, 2],
     col = colors_pca, pch = 19, alpha = 0.6,
     xlab = paste0("PC1 (", round(explained_variance[1] * 100, 2), "% variance)"),
     ylab = paste0("PC2 (", round(explained_variance[2] * 100, 2), "% variance)"),
     main = "PCA: First Two Components")
legend("topright", legend = c("Normal", "Cancer"),
       col = c("steelblue", "crimson"), pch = 19)
grid(alpha = 0.3)

# 3. PCA scatter plot (PC3 vs PC4)
plot(pca_result$x[, 3], pca_result$x[, 4],
     col = colors_pca, pch = 19, alpha = 0.6,
     xlab = paste0("PC3 (", round(explained_variance[3] * 100, 2), "% variance)"),
     ylab = paste0("PC4 (", round(explained_variance[4] * 100, 2), "% variance)"),
     main = "PCA: Components 3 and 4")
legend("topright", legend = c("Normal", "Cancer"),
       col = c("steelblue", "crimson"), pch = 19)
grid(alpha = 0.3)

# 4. Biplot of top features
biplot(pca_result, cex = 0.6, main = "PCA Biplot")

par(mfrow = c(1, 1))

dev.off()
cat("Saved pca_visualization.pdf\n")

# ------------------------------------------------------------------------------
# 6. CORRELATION ANALYSIS
# ------------------------------------------------------------------------------

# Calculate correlation matrix for top differentially expressed genes
top_sig_genes <- df_tests %>% 
  filter(Significant) %>% 
  arrange(P_Value) %>% 
  head(30) %>%
  pull(Gene)

cor_matrix <- cor(df_gene_exp[, top_sig_genes])

# Visualize correlation matrix
pdf("correlation_heatmap.pdf", width = 10, height = 10)

pheatmap(cor_matrix,
         color = colorRampPalette(c("navy", "white", "firebrick3"))(100),
         main = "Correlation Matrix of Top Differentially Expressed Genes",
         clustering_distance_rows = "correlation",
         clustering_distance_cols = "correlation",
         fontsize = 6)

dev.off()
cat("Saved correlation_heatmap.pdf\n")

# ------------------------------------------------------------------------------
# 7. ANOVA ANALYSIS ACROSS MULTIPLE GROUPS (IF APPLICABLE)
# ------------------------------------------------------------------------------

# Demonstration of ANOVA for multi-group comparison
# (In this case, we only have 2 groups, but code shows how to extend)

if (length(unique(df_gene_exp$Sample_Type)) > 2) {
  cat("\nPerforming ANOVA for multi-group comparison...\n")
  
  # ANOVA for first gene (example)
  gene <- gene_names[1]
  
  # Prepare data
  anova_data <- df_gene_exp %>%
    select(Sample_Type, all_of(gene)) %>%
    mutate(Sample_Type = as.factor(Sample_Type))
  
  # Perform ANOVA
  anova_result <- aov(as.formula(paste(gene, "~ Sample_Type")), data = anova_data)
  summary_anova <- summary(anova_result)
  
  cat("\nANOVA Results for", gene, ":\n")
  print(summary_anova)
}

# ------------------------------------------------------------------------------
# 8. SUMMARY STATISTICS
# ------------------------------------------------------------------------------

cat("\n\n" , "="*80, "\n")
cat("Analysis Complete!\n")
cat("="*80, "\n\n")

cat("Summary:\n")
cat(sprintf("  - Total samples analyzed: %d\n", nrow(df_gene_exp)))
cat(sprintf("  - Total genes analyzed: %d\n", length(gene_names)))
cat(sprintf("  - Significantly differentially expressed genes: %d\n",
            sum(df_tests$Significant)))
cat(sprintf("  - After Bonferroni correction: %d\n", sum(df_tests$FDR_Corrected)))

cat("\nFiles generated:\n")
cat("  - statistical_analysis_results.pdf\n")
cat("  - pca_visualization.pdf\n")
cat("  - correlation_heatmap.pdf\n")

cat("\nTop 5 most significant genes:\n")
print(df_tests %>% head(5) %>% select(Gene, P_Value, Cohen_D))

cat("\n", "="*80, "\n\n")

# Save results to CSV
write.csv(df_tests, "differential_expression_results.csv", row.names = FALSE)
cat("Saved differential_expression_results.csv\n")

