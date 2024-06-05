#!/usr/bin/env Rscript
#
# edgeR Differential Gene Expression Analysis Pipeline
# 
# This script performs comprehensive differential gene expression analysis using edgeR
# Author: Differential Gene Expression Dashboard Project
# Date: 2025
#

# Load required libraries
suppressPackageStartupMessages({
  library(edgeR)
  library(ggplot2)
  library(ggrepel)
  library(dplyr)
  library(tibble)
  library(limma)
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

#' Create DGEList and perform differential expression analysis with edgeR
#'
#' @param counts Count matrix (genes x samples)
#' @param metadata Sample metadata with 'group' column
#' @return edgeR results
run_edger <- function(counts, metadata) {
  cat("\nRunning edgeR analysis...\n")
  
  # Create DGEList object
  dge <- DGEList(counts = counts, group = metadata$group)
  
  # Filter low count genes
  keep <- filterByExpr(dge)
  dge <- dge[keep, , keep.lib.sizes = FALSE]
  cat(sprintf("  - Retained %d genes after filtering\n", sum(keep)))
  
  # Calculate normalization factors
  dge <- calcNormFactors(dge)
  
  # Design matrix
  design <- model.matrix(~ 0 + group, data = metadata)
  colnames(design) <- levels(metadata$group)
  
  # Estimate dispersions
  dge <- estimateDisp(dge, design)
  
  cat(sprintf("  - Common dispersion: %.3f\n", dge$common.dispersion))
  cat(sprintf("  - Trended dispersion: %.3f\n", mean(dge$trended.dispersion)))
  
  # Fit GLM
  fit <- glmQLFit(dge, design)
  
  # Make contrast (assuming two groups)
  groups <- levels(metadata$group)
  contrast_name <- paste(groups[2], "vs", groups[1], sep = "_")
  contrast <- makeContrasts(
    contrasts = paste(groups[2], "-", groups[1]),
    levels = design
  )
  
  # Perform test
  qlf <- glmQLFTest(fit, contrast = contrast)
  
  # Get results
  res <- topTags(qlf, n = Inf, sort.by = "PValue")$table
  
  # Add regulation status
  res$regulation <- "Not Significant"
  res$regulation[which(res$FDR < FDR_THRESHOLD & res$logFC > LOG2FC_THRESHOLD)] <- "Upregulated"
  res$regulation[which(res$FDR < FDR_THRESHOLD & res$logFC < -LOG2FC_THRESHOLD)] <- "Downregulated"
  
  # Rename columns for consistency
  res <- res %>%
    rename(
      log2FoldChange = logFC,
      baseMean = logCPM,
      pvalue = PValue,
      padj = FDR
    )
  
  cat(sprintf("\nResults Summary:\n"))
  cat(sprintf("  - Total genes: %d\n", nrow(res)))
  cat(sprintf("  - Upregulated: %d\n", sum(res$regulation == "Upregulated")))
  cat(sprintf("  - Downregulated: %d\n", sum(res$regulation == "Downregulated")))
  cat(sprintf("  - Not significant: %d\n", sum(res$regulation == "Not Significant")))
  
  return(list(dge = dge, results = res, fit = fit))
}

#' Create MDS plot (multidimensional scaling)
#'
#' @param dge DGEList object
#' @param metadata Sample metadata
create_mds_plot <- function(dge, metadata) {
  # Calculate MDS
  mds <- plotMDS(dge, plot = FALSE)
  
  # Create data frame for plotting
  mds_df <- data.frame(
    Sample = colnames(dge),
    MDS1 = mds$x,
    MDS2 = mds$y,
    Group = metadata$group
  )
  
  # Create plot
  p <- ggplot(mds_df, aes(x = MDS1, y = MDS2, color = Group)) +
    geom_point(size = 4) +
    geom_text_repel(aes(label = Sample), size = 3) +
    labs(
      title = "MDS Plot - Sample Similarity",
      x = "MDS Dimension 1",
      y = "MDS Dimension 2"
    ) +
    theme_minimal() +
    theme(
      plot.title = element_text(hjust = 0.5, face = "bold", size = 14),
      legend.position = "bottom"
    )
  
  return(p)
}

#' Create volcano plot
#'
#' @param res edgeR results data frame
#' @param title Plot title
create_volcano_plot <- function(res, title = "Volcano Plot - edgeR") {
  res_df <- res %>%
    rownames_to_column("Gene") %>%
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
      y = "-log10 FDR",
      color = "Regulation Status"
    ) +
    theme_minimal() +
    theme(
      plot.title = element_text(hjust = 0.5, face = "bold", size = 14),
      legend.position = "bottom"
    )
  
  return(p)
}

#' Create BCV plot (biological coefficient of variation)
#'
#' @param dge DGEList object
create_bcv_plot <- function(dge) {
  png(file.path(PLOTS_DIR, "bcv_plot.png"), width = 800, height = 600, res = 150)
  plotBCV(dge, main = "Biological Coefficient of Variation")
  dev.off()
  
  cat("BCV plot saved to", file.path(PLOTS_DIR, "bcv_plot.png"), "\n")
}

#' Export results to CSV
#'
#' @param res edgeR results data frame
#' @param output_file Output file path
export_results <- function(res, output_file) {
  cat(sprintf("\nExporting results to %s...\n", output_file))
  
  res_df <- res %>%
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
  cat("edgeR Differential Expression Analysis\n")
  cat("===========================================\n\n")
  
  # Example usage - uncomment and modify with your data
  
  # data <- load_data(
  #   count_file = file.path(DATA_DIR, "counts.csv"),
  #   metadata_file = file.path(DATA_DIR, "metadata.csv")
  # )
  # 
  # edger_results <- run_edger(
  #   counts = data$counts,
  #   metadata = data$metadata
  # )
  # 
  # # Create and save plots
  # p_volcano <- create_volcano_plot(edger_results$results)
  # ggsave(file.path(PLOTS_DIR, "edger_volcano_plot.png"), p_volcano, width = 10, height = 8, dpi = 300)
  # 
  # p_mds <- create_mds_plot(edger_results$dge, data$metadata)
  # ggsave(file.path(PLOTS_DIR, "edger_mds_plot.png"), p_mds, width = 8, height = 6, dpi = 300)
  # 
  # create_bcv_plot(edger_results$dge)
  # 
  # # Export results
  # export_results(edger_results$results, file.path(OUTPUT_DIR, "edger_results.csv"))
  
  cat("\n===========================================\n")
  cat("Analysis completed successfully!\n")
  cat("===========================================\n")
  
  cat("\nNOTE: This is a template script. Please uncomment and modify\n")
  cat("the main() function with your actual data paths.\n\n")
  cat("Required input format:\n")
  cat("  - counts.csv: Gene expression count matrix (genes as rows, samples as columns)\n")
  cat("  - metadata.csv: Sample information (samples as rows, group column required)\n\n")
}

# Run main function if script is executed directly
if (!interactive()) {
  main()
}

