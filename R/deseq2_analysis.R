#!/usr/bin/env Rscript
#
# DESeq2 Differential Gene Expression Analysis Pipeline
# 
# This script performs comprehensive differential gene expression analysis using DESeq2
# Author: Differential Gene Expression Dashboard Project
# Date: 2025
#

# Load required libraries
suppressPackageStartupMessages({
  library(DESeq2)
  library(ggplot2)
  library(pheatmap)
  library(RColorBrewer)
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
PADJ_THRESHOLD <- 0.05
LOG2FC_THRESHOLD <- 1.0
TOP_N_GENES <- 50

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
  
  # Ensure samples match between counts and metadata
  common_samples <- intersect(colnames(counts), rownames(metadata))
  counts <- counts[, common_samples]
  metadata <- metadata[common_samples, , drop = FALSE]
  
  cat(sprintf("  - %d genes\n", nrow(counts)))
  cat(sprintf("  - %d samples\n", ncol(counts)))
  
  return(list(counts = counts, metadata = metadata))
}

#' Create DESeq2 dataset and perform differential expression analysis
#'
#' @param counts Count matrix (genes x samples)
#' @param metadata Sample metadata
#' @param design_formula Design formula for DESeq2
#' @return DESeq2 results object
run_deseq2 <- function(counts, metadata, design_formula = ~ condition) {
  cat("\nRunning DESeq2 analysis...\n")
  
  # Create DESeq2 dataset
  dds <- DESeqDataSetFromMatrix(
    countData = counts,
    colData = metadata,
    design = design_formula
  )
  
  # Filter low count genes
  keep <- rowSums(counts(dds)) >= 10
  dds <- dds[keep, ]
  cat(sprintf("  - Retained %d genes after filtering\n", sum(keep)))
  
  # Run DESeq2
  dds <- DESeq(dds)
  
  # Get results
  res <- results(dds, alpha = PADJ_THRESHOLD)
  
  # Add regulation status
  res$regulation <- "Not Significant"
  res$regulation[which(res$padj < PADJ_THRESHOLD & res$log2FoldChange > LOG2FC_THRESHOLD)] <- "Upregulated"
  res$regulation[which(res$padj < PADJ_THRESHOLD & res$log2FoldChange < -LOG2FC_THRESHOLD)] <- "Downregulated"
  
  cat(sprintf("\nResults Summary:\n"))
  cat(sprintf("  - Total genes: %d\n", nrow(res)))
  cat(sprintf("  - Upregulated: %d\n", sum(res$regulation == "Upregulated", na.rm = TRUE)))
  cat(sprintf("  - Downregulated: %d\n", sum(res$regulation == "Downregulated", na.rm = TRUE)))
  cat(sprintf("  - Not significant: %d\n", sum(res$regulation == "Not Significant", na.rm = TRUE)))
  
  return(list(dds = dds, results = res))
}

#' Create volcano plot
#'
#' @param res DESeq2 results object
#' @param title Plot title
create_volcano_plot <- function(res, title = "Volcano Plot") {
  # Prepare data
  res_df <- as.data.frame(res) %>%
    rownames_to_column("Gene") %>%
    filter(!is.na(padj) & !is.na(log2FoldChange)) %>%
    mutate(
      neg_log10_padj = -log10(padj),
      regulation = factor(regulation, levels = c("Upregulated", "Downregulated", "Not Significant"))
    )
  
  # Add labels for top genes
  top_genes <- res_df %>%
    filter(regulation != "Not Significant") %>%
    arrange(padj) %>%
    head(20)
  
  # Create plot
  p <- ggplot(res_df, aes(x = log2FoldChange, y = neg_log10_padj, color = regulation)) +
    geom_point(alpha = 0.6, size = 1.5) +
    scale_color_manual(
      values = c("Upregulated" = "#d62728", "Downregulated" = "#2ca02c", "Not Significant" = "#7f7f7f")
    ) +
    geom_hline(yintercept = -log10(PADJ_THRESHOLD), linetype = "dashed", alpha = 0.5) +
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
#' @param res DESeq2 results object
#' @param title Plot title
create_ma_plot <- function(res, title = "MA Plot") {
  res_df <- as.data.frame(res) %>%
    rownames_to_column("Gene") %>%
    filter(!is.na(padj) & !is.na(baseMean) & !is.na(log2FoldChange)) %>%
    mutate(
      log10_baseMean = log10(baseMean + 1),
      regulation = factor(regulation, levels = c("Upregulated", "Downregulated", "Not Significant"))
    )
  
  p <- ggplot(res_df, aes(x = log10_baseMean, y = log2FoldChange, color = regulation)) +
    geom_point(alpha = 0.5, size = 1) +
    scale_color_manual(
      values = c("Upregulated" = "#d62728", "Downregulated" = "#2ca02c", "Not Significant" = "#7f7f7f")
    ) +
    geom_hline(yintercept = 0, linetype = "solid", color = "black", alpha = 0.5) +
    labs(
      title = title,
      x = "log10 Mean Expression",
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

#' Create PCA plot
#'
#' @param dds DESeq2 dataset
#' @param title Plot title
create_pca_plot <- function(dds, title = "PCA Plot") {
  vsd <- vst(dds, blind = FALSE)
  pcaData <- plotPCA(vsd, intgroup = "condition", returnData = TRUE)
  percentVar <- round(100 * attr(pcaData, "percentVar"))
  
  p <- ggplot(pcaData, aes(x = PC1, y = PC2, color = condition)) +
    geom_point(size = 4) +
    labs(
      title = title,
      x = paste0("PC1: ", percentVar[1], "% variance"),
      y = paste0("PC2: ", percentVar[2], "% variance")
    ) +
    theme_minimal() +
    theme(
      plot.title = element_text(hjust = 0.5, face = "bold", size = 14),
      legend.position = "bottom"
    )
  
  return(p)
}

#' Create heatmap of top genes
#'
#' @param dds DESeq2 dataset
#' @param res DESeq2 results
#' @param n_genes Number of top genes to plot
create_heatmap <- function(dds, res, n_genes = 50) {
  vsd <- vst(dds, blind = FALSE)
  
  # Get top genes
  top_genes <- res[order(res$padj), ] %>%
    head(n_genes) %>%
    rownames()
  
  # Extract normalized counts
  mat <- assay(vsd)[top_genes, ]
  mat <- t(scale(t(mat)))
  
  # Create annotation
  annotation_col <- as.data.frame(colData(dds)[, c("condition"), drop = FALSE])
  
  # Create heatmap
  pheatmap(
    mat,
    cluster_rows = TRUE,
    cluster_cols = TRUE,
    show_rownames = TRUE,
    show_colnames = TRUE,
    annotation_col = annotation_col,
    color = colorRampPalette(rev(brewer.pal(n = 7, name = "RdYlBu")))(100),
    main = paste0("Top ", n_genes, " Differentially Expressed Genes")
  )
}

#' Export results to CSV
#'
#' @param res DESeq2 results object
#' @param output_file Output file path
export_results <- function(res, output_file) {
  cat(sprintf("\nExporting results to %s...\n", output_file))
  
  res_df <- as.data.frame(res) %>%
    rownames_to_column("Gene") %>%
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
  cat("DESeq2 Differential Expression Analysis\n")
  cat("===========================================\n\n")
  
  # Example usage - adjust paths as needed
  # Uncomment and modify these lines when you have real data
  
  # data <- load_data(
  #   count_file = file.path(DATA_DIR, "counts.csv"),
  #   metadata_file = file.path(DATA_DIR, "metadata.csv")
  # )
  # 
  # deseq_results <- run_deseq2(
  #   counts = data$counts,
  #   metadata = data$metadata,
  #   design_formula = ~ condition
  # )
  # 
  # # Create and save plots
  # p_volcano <- create_volcano_plot(deseq_results$results)
  # ggsave(file.path(PLOTS_DIR, "volcano_plot.png"), p_volcano, width = 10, height = 8, dpi = 300)
  # 
  # p_ma <- create_ma_plot(deseq_results$results)
  # ggsave(file.path(PLOTS_DIR, "ma_plot.png"), p_ma, width = 10, height = 8, dpi = 300)
  # 
  # p_pca <- create_pca_plot(deseq_results$dds)
  # ggsave(file.path(PLOTS_DIR, "pca_plot.png"), p_pca, width = 8, height = 6, dpi = 300)
  # 
  # png(file.path(PLOTS_DIR, "heatmap.png"), width = 800, height = 1000, res = 150)
  # create_heatmap(deseq_results$dds, deseq_results$results, n_genes = TOP_N_GENES)
  # dev.off()
  # 
  # # Export results
  # export_results(deseq_results$results, file.path(OUTPUT_DIR, "deseq2_results.csv"))
  
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

