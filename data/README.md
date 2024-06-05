# 📊 Data Directory

This directory contains all data files for the Differential Gene Expression Analysis project.

## 📁 Directory Structure

```
data/
├── raw/              # Raw input data (count matrices, metadata)
├── processed/        # Processed results from analyses
└── examples/         # Example datasets for tutorials
```

## 📂 Subdirectories

### `raw/`
Place your raw input files here:
- **Count matrices**: Gene expression counts (genes × samples)
- **Metadata files**: Sample information and experimental design
- **Annotation files**: Gene annotations, IDs, descriptions

**Recommended format**:
```csv
# counts.csv - Count matrix
,Sample1,Sample2,Sample3,Sample4
GENE1,1523,1832,234,189
GENE2,45,67,2341,2567

# metadata.csv - Sample metadata
,condition,batch,replicate
Sample1,control,batch1,rep1
Sample2,control,batch1,rep2
Sample3,treated,batch2,rep1
Sample4,treated,batch2,rep2
```

### `processed/`
Output files from R scripts and analyses will be saved here:
- `deseq2_results.csv` - DESeq2 analysis results
- `edger_results.csv` - edgeR analysis results
- `limma_results.csv` - limma-voom analysis results
- `*_significant.csv` - Filtered significant genes only

### `examples/`
Sample datasets for tutorials and testing:
- `sample_data.csv` - Example differential expression results
- Includes realistic gene expression data
- Pre-computed statistics for immediate use

## 📥 Input Data Format

### For R Scripts (DESeq2, edgeR, limma)

**Count Matrix** (`counts.csv`):
- Rows = genes
- Columns = samples
- Values = raw read counts (integers)
- First column = gene IDs

**Metadata** (`metadata.csv`):
- Rows = samples (matching count matrix columns)
- Columns = experimental factors
- Must include 'condition' or 'group' column
- Additional columns for batch effects, replicates, etc.

### For Python Dashboard

**Results File** (any CSV with these columns):
- `Gene` - Gene identifier
- `log2FoldChange` - Log2 fold change value
- `padj` - Adjusted p-value
- `baseMean` - Mean expression (optional)
- `pvalue` - Raw p-value (optional)
- `regulation` - Up/Down/Not Significant (optional)

## 📊 Example Usage

### Preparing Your Data

1. **Export from DESeq2**:
```r
results_df <- as.data.frame(results(dds))
results_df$Gene <- rownames(results_df)
write.csv(results_df, "data/processed/my_results.csv", row.names=FALSE)
```

2. **Export from edgeR**:
```r
results <- topTags(qlf, n=Inf)$table
results$Gene <- rownames(results)
write.csv(results, "data/processed/my_results.csv", row.names=FALSE)
```

3. **Export from limma**:
```r
results <- topTable(fit2, number=Inf)
results$Gene <- rownames(results)
write.csv(results, "data/processed/my_results.csv", row.names=FALSE)
```

## 🔒 Data Security

⚠️ **Important Notes**:

1. **Git Ignore**: Large data files are automatically excluded from git (see `.gitignore`)
2. **Sensitive Data**: Never commit patient data or sensitive information
3. **File Size**: Keep individual files under 100MB for git compatibility
4. **Backups**: Maintain backups of raw data separately

## 💾 Storage Guidelines

### What TO commit to git:
- ✅ Small example datasets (< 1MB)
- ✅ README files
- ✅ Data dictionaries
- ✅ Sample metadata templates

### What NOT to commit:
- ❌ Large count matrices (> 10MB)
- ❌ Raw sequencing data
- ❌ Sensitive/protected data
- ❌ Temporary analysis files

## 📝 Data Documentation

For each dataset, document:
- **Source**: Where did the data come from?
- **Processing**: How was it preprocessed?
- **Date**: When was it generated?
- **Format**: File format and column descriptions
- **Conditions**: Experimental conditions and design

Example documentation in `DATASET_INFO.txt`:
```
Dataset: Mouse liver RNA-seq
Source: GEO accession GSE12345
Date: 2025-01-15
Samples: 12 (6 control, 6 treated)
Conditions: Control vs. Drug Treatment
Sequencing: Illumina HiSeq 2500, paired-end 100bp
Processing: STAR alignment, featureCounts quantification
```

## 🔄 Data Versioning

For reproducibility:
1. Version your analysis scripts
2. Document data processing steps
3. Keep original raw data unchanged
4. Use dated folders for processed results

## 📞 Need Help?

- **File format questions**: See project documentation
- **Large datasets**: Consider data compression or external storage
- **Data privacy**: Consult your institution's IRB/ethics board

---

## 🗂️ Quick Reference

| Directory | Purpose | Git Tracked |
|-----------|---------|-------------|
| `raw/` | Original input data | No (too large) |
| `processed/` | Analysis outputs | No (regenerable) |
| `examples/` | Tutorial samples | Yes (small files) |

---

*Organize your data, organize your research! 📊*

