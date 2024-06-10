# R Scripts for Differential Gene Expression Analysis

This directory contains comprehensive R scripts for performing differential gene expression analysis using popular Bioconductor packages.

## 📁 Contents

- **`deseq2_analysis.R`** - Complete pipeline for DESeq2 analysis
- **`edger_analysis.R`** - Complete pipeline for edgeR analysis
- **`limma_analysis.R`** - Complete pipeline for limma-voom analysis

## 🔧 Installation

### Required R Packages

```r
# Install Bioconductor if not already installed
if (!requireNamespace("BiocManager", quietly = TRUE))
    install.packages("BiocManager")

# Install required Bioconductor packages
BiocManager::install(c(
    "DESeq2",
    "edgeR",
    "limma"
))

# Install CRAN packages
install.packages(c(
    "ggplot2",
    "pheatmap",
    "RColorBrewer",
    "ggrepel",
    "dplyr",
    "tibble"
))
```

## 📊 Usage

### 1. Prepare Your Data

You need two input files:

**counts.csv** - Gene expression count matrix
```
,Sample1,Sample2,Sample3,Sample4
GENE1,1523,1832,234,189
GENE2,45,67,2341,2567
GENE3,789,654,432,567
```

**metadata.csv** - Sample information
```
,condition,group
Sample1,control,A
Sample2,control,A
Sample3,treated,B
Sample4,treated,B
```

### 2. Run Analysis

#### DESeq2 Analysis

```bash
Rscript R/deseq2_analysis.R
```

Or from R console:
```r
source("R/deseq2_analysis.R")

# Load your data
data <- load_data(
  count_file = "data/raw/counts.csv",
  metadata_file = "data/raw/metadata.csv"
)

# Run DESeq2
results <- run_deseq2(
  counts = data$counts,
  metadata = data$metadata,
  design_formula = ~ condition
)

# Create visualizations
p_volcano <- create_volcano_plot(results$results)
p_ma <- create_ma_plot(results$results)
p_pca <- create_pca_plot(results$dds)

# Export results
export_results(results$results, "data/processed/deseq2_results.csv")
```

#### edgeR Analysis

```bash
Rscript R/edger_analysis.R
```

Or from R console:
```r
source("R/edger_analysis.R")

# Load and analyze
data <- load_data(
  count_file = "data/raw/counts.csv",
  metadata_file = "data/raw/metadata.csv"
)

results <- run_edger(
  counts = data$counts,
  metadata = data$metadata
)

# Visualize and export
p_volcano <- create_volcano_plot(results$results)
p_mds <- create_mds_plot(results$dge, data$metadata)
export_results(results$results, "data/processed/edger_results.csv")
```

#### limma-voom Analysis

```bash
Rscript R/limma_analysis.R
```

Or from R console:
```r
source("R/limma_analysis.R")

# Load and analyze
data <- load_data(
  count_file = "data/raw/counts.csv",
  metadata_file = "data/raw/metadata.csv"
)

results <- run_limma_voom(
  counts = data$counts,
  metadata = data$metadata
)

# Visualize and export
p_volcano <- create_volcano_plot(results$results)
p_ma <- create_ma_plot(results$results)
export_results(results$results, "data/processed/limma_results.csv")
```

## 📈 Output

Each script generates:

1. **Results CSV files**:
   - `*_results.csv` - All genes with statistics
   - `*_results_significant.csv` - Only significant genes

2. **Visualization plots**:
   - Volcano plots
   - MA plots
   - PCA/MDS plots
   - Heatmaps
   - Quality control plots

3. **Statistics summary** in console output

## 🎯 Method Comparison

| Method | Best For | Advantages | Considerations |
|--------|----------|------------|----------------|
| **DESeq2** | Most RNA-seq experiments | Robust, well-documented, handles small samples well | Can be slower for very large datasets |
| **edgeR** | Large datasets, time-series | Fast, flexible, good for complex designs | Requires more parameter tuning |
| **limma-voom** | Microarrays & RNA-seq | Very fast, handles batch effects well | Assumes data is approximately normal after transformation |

## 📚 References

- **DESeq2**: Love, M.I., Huber, W., Anders, S. (2014) Genome Biology
- **edgeR**: Robinson, M.D., McCarthy, D.J., Smyth, G.K. (2010) Bioinformatics
- **limma**: Ritchie, M.E., et al. (2015) Nucleic Acids Research

## 💡 Tips

1. **Sample size**: DESeq2 works well with small samples (n=3), edgeR and limma-voom need n≥3 per group
2. **Filtering**: All scripts include automatic low-count gene filtering
3. **Normalization**: Each method uses its own normalization approach
4. **Batch effects**: Use design formulas to account for batch effects
5. **Multiple comparisons**: Results include FDR/adjusted p-values

## 🐛 Troubleshooting

**Error: Package not found**
```r
# Reinstall BiocManager and packages
install.packages("BiocManager")
BiocManager::install(c("DESeq2", "edgeR", "limma"))
```

**Error: Design matrix not full rank**
- Check your metadata for redundant columns
- Ensure you have replicates for each condition

**Memory issues with large datasets**
- Use edgeR for better memory efficiency
- Filter more aggressively for low-count genes

## 📞 Support

For issues specific to:
- **Script usage**: Open an issue on GitHub
- **Method questions**: Refer to Bioconductor support forums
- **Statistical interpretation**: Consult with a biostatistician

