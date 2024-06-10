#!/usr/bin/env Rscript
#
# limma-voom Differential Gene Expression Analysis Pipeline
# 
# This script performs comprehensive differential gene expression analysis using limma-voom
# Author: Differential Gene Expression Dashboard Project
# Date: 2025
#

# Load required libraries
suppressPackageStartupMessages({
  library(limma)
  library(edgeR)
  library(ggplot2)
  library(ggrepel)
  library(dplyr)
  library(tibble)
})

# ============================================================================
# CONFIGURATION
# ============================================================================

# Set paths
DATA_DIR <- "data/raw"
OUTPUT_DIR <- "data/processed"
PLOTS_DIR <- "docs/images"

# Create output directories if they don't exist
dir.create(OUTPUT_DIR, showWarnings = FALSE, recursive = TRUE)
dir.create(PLOTS_DIR, showWarnings = FALSE, recursive = TRUE)

# Analysis parameters
FDR_THRESHOLD <- 0.05
LOG2FC_THRESHOLD <- 1.0

# ============================================================================
# FUNCTIONS
# ============================================================================

#' Load count matrix and metadata
#'
#' @param count_file Path to count matrix CSV file (genes x samples)
#' @param metadata_file Path to sample metadata CSV file
#' @return List containing count matrix and metadata
load_data <- function(count_file, metadata_file) {
  cat("Loading data...\n")
  
  # Load count matrix
  counts <- read.csv(count_file, row.names = 1, check.names = FALSE)
  counts <- as.matrix(counts)
  
  # Load metadata
  metadata <- read.csv(metadata_file, row.names = 1, stringsAsFactors = TRUE)
  
  # Ensure samples match
  common_samples <- intersect(colnames(counts), rownames(metadata))
  counts <- counts[, common_samples]
  metadata <- metadata[common_samples, , drop = FALSE]
  
  cat(sprintf("  - %d genes\n", nrow(counts)))
  cat(sprintf("  - %d samples\n", ncol(counts)))
  
  return(list(counts = counts, metadata = metadata))
}

#' Perform limma-voom differential expression analysis
#'
#' @param counts Count matrix (genes x samples)
#' @param metadata Sample metadata with 'condition' column
#' @return limma results
run_limma_voom <- function(counts, metadata) {
  cat("\nRunning limma-voom analysis...\n")
  
  # Create DGEList object for filtering
  dge <- DGEList(counts = counts)
  
  # Filter low count genes
  keep <- filterByExpr(dge, group = metadata$condition)
  dge <- dge[keep, , keep.lib.sizes = FALSE]
  cat(sprintf("  - Retained %d genes after filtering\n", sum(keep)))
  
  # Calculate normalization factors
  dge <- calcNormFactors(dge)
  
  # Design matrix
  design <- model.matrix(~ 0 + condition, data = metadata)
  colnames(design) <- levels(metadata$condition)
  
  # Apply voom transformation
  cat("  - Applying voom transformation...\n")
  v <- voom(dge, design, plot = FALSE)
  
  # Fit linear model
  cat("  - Fitting linear model...\n")
  fit <- lmFit(v, design)
  
  # Make contrast (assuming two conditions)
  conditions <- levels(metadata$condition)
  contrast_name <- paste(conditions[2], "vs", conditions[1], sep = "_")
  contrast <- makeContrasts(
    contrasts = paste(conditions[2], "-", conditions[1]),
    levels = design
  )
  
  # Fit contrasts
  fit2 <- contrasts.fit(fit, contrast)
  
  # Apply empirical Bayes smoothing
  fit2 <- eBayes(fit2)
  
  # Get results
  res <- topTable(fit2, number = Inf, sort.by = "P")
  
  # Add additional columns
  res$Gene <- rownames(res)
  
  # Add regulation status
  res$regulation <- "Not Significant"
  res$regulation[which(res$adj.P.Val < FDR_THRESHOLD & res$logFC > LOG2FC_THRESHOLD)] <- "Upregulated"
  res$regulation[which(res$adj.P.Val < FDR_THRESHOLD & res$logFC < -LOG2FC_THRESHOLD)] <- "Downregulated"
  
  # Rename columns for consistency
  res <- res %>%
    rename(
      log2FoldChange = logFC,
      baseMean = AveExpr,
      pvalue = P.Value,
      padj = adj.P.Val
    )
  
  cat(sprintf("\nResults Summary:\n"))
  cat(sprintf("  - Total genes: %d\n", nrow(res)))
  cat(sprintf("  - Upregulated: %d\n", sum(res$regulation == "Upregulated")))
  cat(sprintf("  - Downregulated: %d\n", sum(res$regulation == "Downregulated")))
  cat(sprintf("  - Not significant: %d\n", sum(res$regulation == "Not Significant")))
  
  return(list(voom = v, fit = fit2, results = res))
}

#' Create voom mean-variance plot
#'
#' @param counts Count matrix
#' @param metadata Sample metadata
#' @param design Design matrix
create_voom_plot <- function(counts, metadata, design) {
  dge <- DGEList(counts = counts)
  keep <- filterByExpr(dge, group = metadata$condition)
  dge <- dge[keep, , keep.lib.sizes = FALSE]
  dge <- calcNormFactors(dge)
  
  png(file.path(PLOTS_DIR, "voom_mean_variance.png"), width = 800, height = 600, res = 150)
  v <- voom(dge, design, plot = TRUE)
  dev.off()
  
  cat("Voom mean-variance plot saved to", file.path(PLOTS_DIR, "voom_mean_variance.png"), "\n")
}

#' Create volcano plot
#'
#' @param res limma results data frame
#' @param title Plot title
create_volcano_plot <- function(res, title = "Volcano Plot - limma-voom") {
  res_df <- res %>%
    filter(!is.na(padj) & !is.na(log2FoldChange)) %>%
    mutate(
      neg_log10_padj = -log10(padj),
      regulation = factor(regulation, levels = c("Upregulated", "Downregulated", "Not Significant"))
    )
  
  # Top genes for labeling
  top_genes <- res_df %>%
    filter(regulation != "Not Significant") %>%
    arrange(padj) %>%
    head(20)
  
  p <- ggplot(res_df, aes(x = log2FoldChange, y = neg_log10_padj, color = regulation)) +
    geom_point(alpha = 0.6, size = 1.5) +
    scale_color_manual(
      values = c("Upregulated" = "#d62728", "Downregulated" = "#2ca02c", "Not Significant" = "#7f7f7f")
    ) +
    geom_hline(yintercept = -log10(FDR_THRESHOLD), linetype = "dashed", alpha = 0.5) +
    geom_vline(xintercept = c(-LOG2FC_THRESHOLD, LOG2FC_THRESHOLD), linetype = "dashed", alpha = 0.5) +
    geom_text_repel(
      data = top_genes,
      aes(label = Gene),
      size = 3,
      max.overlaps = 15,
      box.padding = 0.5
    ) +
    labs(
      title = title,
      x = "log2 Fold Change",
      y = "-log10 Adjusted P-value",
      color = "Regulation Status"
    ) +
    theme_minimal() +
    theme(
      plot.title = element_text(hjust = 0.5, face = "bold", size = 14),
      legend.position = "bottom"
    )
  
  return(p)
}

#' Create MA plot
#'
#' @param res limma results data frame
#' @param title Plot title
create_ma_plot <- function(res, title = "MA Plot - limma-voom") {
  res_df <- res %>%
    filter(!is.na(padj) & !is.na(baseMean) & !is.na(log2FoldChange)) %>%
    mutate(
      regulation = factor(regulation, levels = c("Upregulated", "Downregulated", "Not Significant"))
    )
  
  p <- ggplot(res_df, aes(x = baseMean, y = log2FoldChange, color = regulation)) +
    geom_point(alpha = 0.5, size = 1) +
    scale_color_manual(
      values = c("Upregulated" = "#d62728", "Downregulated" = "#2ca02c", "Not Significant" = "#7f7f7f")
    ) +
    scale_x_log10() +
    geom_hline(yintercept = 0, linetype = "solid", color = "black", alpha = 0.5) +
    labs(
      title = title,
      x = "Average Expression (log scale)",
      y = "log2 Fold Change",
      color = "Regulation Status"
    ) +
    theme_minimal() +
    theme(
      plot.title = element_text(hjust = 0.5, face = "bold", size = 14),
      legend.position = "bottom"
    )
  
  return(p)
}

#' Export results to CSV
#'
#' @param res limma results data frame
#' @param output_file Output file path
export_results <- function(res, output_file) {
  cat(sprintf("\nExporting results to %s...\n", output_file))
  
  res_df <- res %>%
    arrange(padj)
  
  write.csv(res_df, output_file, row.names = FALSE)
  
  # Also export significant genes only
  sig_file <- gsub("\\.csv$", "_significant.csv", output_file)
  sig_df <- res_df %>%
    filter(regulation != "Not Significant")
  
  write.csv(sig_df, sig_file, row.names = FALSE)
  
  cat(sprintf("  - All results: %s\n", output_file))
  cat(sprintf("  - Significant genes: %s\n", sig_file))
}

# ============================================================================
# MAIN ANALYSIS PIPELINE
# ============================================================================

main <- function() {
  cat("===========================================\n")
  cat("limma-voom Differential Expression Analysis\n")
  cat("===========================================\n\n")
  
  # Example usage - uncomment and modify with your data
  
  # data <- load_data(
  #   count_file = file.path(DATA_DIR, "counts.csv"),
  #   metadata_file = file.path(DATA_DIR, "metadata.csv")
  # )
  # 
  # design <- model.matrix(~ 0 + condition, data = data$metadata)
  # colnames(design) <- levels(data$metadata$condition)
  # 
  # # Create voom plot
  # create_voom_plot(data$counts, data$metadata, design)
  # 
  # limma_results <- run_limma_voom(
  #   counts = data$counts,
  #   metadata = data$metadata
  # )
  # 
  # # Create and save plots
  # p_volcano <- create_volcano_plot(limma_results$results)
  # ggsave(file.path(PLOTS_DIR, "limma_volcano_plot.png"), p_volcano, width = 10, height = 8, dpi = 300)
  # 
  # p_ma <- create_ma_plot(limma_results$results)
  # ggsave(file.path(PLOTS_DIR, "limma_ma_plot.png"), p_ma, width = 10, height = 8, dpi = 300)
  # 
  # # Export results
  # export_results(limma_results$results, file.path(OUTPUT_DIR, "limma_results.csv"))
  
  cat("\n===========================================\n")
  cat("Analysis completed successfully!\n")
  cat("===========================================\n")
  
  cat("\nNOTE: This is a template script. Please uncomment and modify\n")
  cat("the main() function with your actual data paths.\n\n")
  cat("Required input format:\n")
  cat("  - counts.csv: Gene expression count matrix (genes as rows, samples as columns)\n")
  cat("  - metadata.csv: Sample information (samples as rows, condition column required)\n\n")
}

# Run main function if script is executed directly
if (!interactive()) {
  main()
}

