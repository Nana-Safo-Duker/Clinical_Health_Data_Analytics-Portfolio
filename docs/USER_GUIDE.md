# 🧬 User Guide: Advanced Differential Gene Expression Dashboard

## Table of Contents
1. [Getting Started](#getting-started)
2. [Step-by-Step Tutorial](#step-by-step-tutorial)
3. [Feature Guide](#feature-guide)
4. [Tips & Best Practices](#tips--best-practices)
5. [FAQ](#faq)
6. [Troubleshooting](#troubleshooting)

---

## Getting Started

### Prerequisites
- Python 3.8 or higher
- Web browser (Chrome, Firefox, Safari, or Edge)
- Gene expression data in CSV format

### Installation

**Quick Start:**
```bash
# Navigate to project directory
cd Differential-Gene-Expression

# Install dependencies
pip install -r requirements.txt

# Launch dashboard
python quick_start.py
```

**Manual Start:**
```bash
streamlit run Differential_Gene_Dashboard_Enhanced.py
```

The dashboard will automatically open in your browser at `http://localhost:8501`

---

## Step-by-Step Tutorial

### Tutorial 1: Basic Analysis with Sample Data

#### Step 1: Launch the Dashboard
```bash
python quick_start.py
```

#### Step 2: Upload Data
1. Click "**Browse files**" in the sidebar
2. Select `sample_data.csv` (included in this repository)
3. Wait for upload confirmation ✅

#### Step 3: Map Your Columns
The dashboard will display your data preview. Now map the columns:

| Field | Sample Data Column |
|-------|-------------------|
| Gene Name Column | `Gene` |
| Log2 Fold Change | `log2FoldChange` |
| Adjusted P-value | `padj` |
| Regulation Column | `regulation` |

For optional columns:
- Mean Expression: `baseMean`
- Raw P-value: `pvalue`

#### Step 4: Set Thresholds
Use the sliders to adjust significance criteria:
- **Log2 Fold Change**: `1.0` (genes with ≥2-fold change)
- **Adjusted P-value**: `0.05` (5% FDR)

💡 **Tip**: Start with standard thresholds, then adjust based on your results

#### Step 5: View Statistics
The metrics dashboard shows:
- 📊 **Total Genes**: 50
- 📈 **Significant**: ~30 (60%)
- 🔺 **Upregulated**: ~16 (53%)
- 🔻 **Downregulated**: ~14 (47%)

#### Step 6: Explore Visualizations

**Tab 1: Volcano Plot**
- Red dots = Upregulated genes
- Green dots = Downregulated genes
- Gray dots = Not significant
- **Hover** over points to see gene details
- **Zoom** by clicking and dragging
- **Pan** by holding Shift + drag

**Tab 2: Top Genes**
- Shows most differentially expressed genes
- Adjust slider to show more/fewer genes
- Colors indicate up (red) or down (green) regulation

**Tab 3: Distributions**
- Left: log2 Fold Change distribution
- Right: P-value distribution
- Helps identify overall trends

**Tab 4: MA Plot** (if baseMean available)
- Shows relationship between expression level and fold change
- Identifies expression-dependent bias

**Tab 5: Data Table**
- Sortable, searchable table
- Shows all significant genes
- Export-ready format

#### Step 7: Search for Specific Genes
In the "Search Specific Genes" box, enter:
```
TP53, BRCA1, EGFR
```

The dashboard will highlight and display these genes if found.

#### Step 8: Export Results
Choose your preferred format:
- 📥 **CSV**: Lightweight, universal format
- 📥 **Excel**: Formatted, ready for presentations
- 📥 **All Data**: Complete filtered dataset

---

### Tutorial 2: Analyzing Your Own Data

#### Preparing Your Data

Your CSV should look like this:

```csv
Gene,log2FoldChange,padj
GENE1,2.5,0.001
GENE2,-1.8,0.01
GENE3,3.2,0.0001
...
```

**Required columns:**
- Gene identifiers (any naming convention)
- Numeric log2 fold change values
- Numeric adjusted p-values (0-1)

**Optional columns:**
- Regulation status (Upregulated/Downregulated/Not Significant)
- Base mean expression
- Raw p-values
- Any other metadata

#### Step-by-Step with Your Data

1. **Export from your analysis tool**

   **From DESeq2 (R):**
   ```R
   results_df <- as.data.frame(results(dds))
   results_df$Gene <- rownames(results_df)
   write.csv(results_df, "my_deseq2_results.csv", row.names=FALSE)
   ```

   **From edgeR (R):**
   ```R
   results_df <- topTags(lrt, n=Inf)$table
   results_df$Gene <- rownames(results_df)
   write.csv(results_df, "my_edger_results.csv", row.names=FALSE)
   ```

   **From limma (R):**
   ```R
   results_df <- topTable(fit, number=Inf)
   results_df$Gene <- rownames(results_df)
   write.csv(results_df, "my_limma_results.csv", row.names=FALSE)
   ```

2. **Upload to dashboard**
   - Click Browse files
   - Select your CSV

3. **Map columns** (they may have different names)
   
   Common column name mappings:

   | Your Column | Dashboard Field |
   |-------------|----------------|
   | `gene_id`, `GeneID`, `symbol` | Gene Name |
   | `logFC`, `log2FC`, `log2FoldChange` | Log2 Fold Change |
   | `FDR`, `adj.P.Val`, `padj` | Adjusted P-value |

4. **Analyze and export**

---

## Feature Guide

### 🌋 Volcano Plot

**Purpose**: Visualize fold change vs statistical significance

**How to Read**:
- **X-axis**: log2 fold change (left = downregulated, right = upregulated)
- **Y-axis**: -log10 p-value (higher = more significant)
- **Top-right**: Significantly upregulated
- **Top-left**: Significantly downregulated
- **Bottom**: Not statistically significant

**Interactions**:
- Hover to see gene names and exact values
- Click and drag to zoom into regions
- Double-click to reset zoom
- Switch between Plotly and Altair engines

**Best For**:
- Quick overview of DE genes
- Identifying most changed genes
- Publication figures

### 📊 Top Genes Chart

**Purpose**: Highlight most differentially expressed genes

**Features**:
- Automatically selects top up/down genes
- Adjustable number of genes shown
- Sorted by fold change magnitude
- Color-coded by direction

**Best For**:
- Identifying candidate genes
- Quick reporting
- Presentations

### 📉 Distribution Plots

**Purpose**: Understand overall expression patterns

**Log2FC Distribution**:
- Shows how many genes are up vs down
- Centered at zero = balanced
- Skewed = overall trend in one direction

**P-value Distribution**:
- Should show enrichment at low p-values if DE present
- Uniform = possibly no true differences
- Peak at low p-values = strong signal

**Best For**:
- Quality control
- Understanding experiment quality
- Identifying biases

### 🔬 MA Plot

**Purpose**: Detect expression-level dependent bias

**How to Read**:
- **X-axis**: Mean expression level
- **Y-axis**: Log2 fold change
- Should see even spread across expression levels
- Funnel shape at low expression = normal

**Red Flag**:
- Systematic trends (curve) = bias
- All high-FC genes at one expression level = problem

**Best For**:
- Quality control
- Normalization validation
- Bias detection

### 🔍 Gene Search

**Purpose**: Find specific genes of interest

**How to Use**:
1. Enter gene names (comma-separated)
2. Case-insensitive matching
3. Results show immediately

**Example**:
```
TP53, BRCA1, egfr
```

**Best For**:
- Validating known genes
- Checking specific pathways
- Follow-up analysis

### 📋 Data Table

**Purpose**: Detailed view of significant genes

**Features**:
- Sortable by any column
- Formatted numbers (3 decimals for FC, scientific for p-values)
- Shows only significant genes by default
- Ready for export

**Sorting Options**:
- **By padj**: Find most significant
- **By log2FoldChange**: Find most changed
- **By Gene**: Alphabetical

**Best For**:
- Detailed examination
- Preparing supplementary tables
- Gene list generation

### 💾 Export Functions

**CSV Export**:
- Universal format
- Opens in Excel, R, Python
- Smallest file size

**Excel Export**:
- Formatted for readability
- Multiple sheets possible
- Best for sharing

**All Data Export**:
- Includes non-significant genes
- Complete filtered dataset
- Best for further analysis

---

## Tips & Best Practices

### Choosing Thresholds

**Conservative (strict)**:
```
Log2 FC: ±1.5 (3-fold change)
P-adj: 0.01 (1% FDR)
```
Use when: High false discovery cost, large sample size

**Standard**:
```
Log2 FC: ±1.0 (2-fold change)
P-adj: 0.05 (5% FDR)
```
Use when: Typical RNA-seq analysis

**Exploratory (permissive)**:
```
Log2 FC: ±0.5 (1.4-fold change)
P-adj: 0.1 (10% FDR)
```
Use when: Small sample size, hypothesis generation

### Data Quality Checks

✅ **Good Signs**:
- Clear separation in volcano plot
- Enrichment of low p-values
- Reasonable number of DE genes (10-30% typical)
- Balanced up/down (if no biological bias expected)

⚠️ **Warning Signs**:
- All genes significant (check thresholds)
- No significant genes (check data quality)
- Only upregulated or only downregulated
- P-value distribution uniform

### Interpretation Guidelines

**Fold Change Interpretation**:
- **±0.5**: Subtle change, may not be biologically meaningful
- **±1.0**: 2-fold change, standard cutoff
- **±2.0**: 4-fold change, strong effect
- **±3.0+**: 8+ fold change, very strong effect

**P-value Interpretation**:
- **0.05**: Standard significance
- **0.01**: Strong significance
- **0.001**: Very strong significance
- **< 1e-10**: Extremely significant (check for outliers)

### Workflow Recommendations

1. **Initial Analysis**:
   - Use standard thresholds
   - Review all visualizations
   - Check data quality

2. **Exploration**:
   - Adjust thresholds
   - Search known genes
   - Identify patterns

3. **Validation**:
   - Export gene lists
   - Plan qPCR validation
   - Pathway analysis

4. **Reporting**:
   - Screenshot volcano plots
   - Export data tables
   - Document threshold choices

---

## FAQ

### General Questions

**Q: What file formats are supported?**
A: CSV (comma-separated values) only. Excel files should be saved as CSV first.

**Q: How large can my dataset be?**
A: Tested up to 50,000 genes. Performance depends on your computer's RAM.

**Q: Can I analyze multiple comparisons?**
A: Currently, one comparison at a time. Upload different files for multiple comparisons.

**Q: Is my data stored anywhere?**
A: No, all processing is local. Data is only in your browser session.

### Data Questions

**Q: My columns have different names. Will it work?**
A: Yes! You manually select which columns contain which data.

**Q: What if I don't have a regulation column?**
A: Optional! Dashboard will calculate it based on thresholds.

**Q: Can I use gene IDs instead of gene names?**
A: Yes, any identifier works (Ensembl, Entrez, symbols, etc.).

**Q: What if I have NA values?**
A: Rows with NA in critical columns (gene, FC, p-value) are automatically removed with a warning.

### Analysis Questions

**Q: Why are no genes significant?**
A: Try lowering thresholds. May indicate:
- Low statistical power
- No true biological difference
- Data quality issues

**Q: Why are ALL genes significant?**
A: Check data quality. May indicate:
- Data not properly normalized
- Batch effects
- Thresholds too permissive

**Q: Should I use raw or adjusted p-values?**
A: Always use adjusted (FDR, Bonferroni, etc.) to control for multiple testing.

**Q: How do I choose the fold change threshold?**
A: Depends on:
- Biological context (subtle vs dramatic changes expected)
- Sample size (smaller samples → lower threshold)
- Validation capacity (higher threshold = fewer genes to validate)

### Technical Questions

**Q: Dashboard won't start?**
A: Check:
1. Python version (3.8+)
2. Dependencies installed (`pip install -r requirements.txt`)
3. Firewall not blocking localhost:8501

**Q: Plots not showing?**
A: Check browser console for errors. Try different browser or refresh.

**Q: Export not working?**
A: Check browser download settings. Try different format.

**Q: Can I customize colors?**
A: Yes, edit the color_map dictionaries in the code.

---

## Troubleshooting

### Common Issues

#### Issue: "Data validation failed"

**Symptoms**: Error message after selecting columns

**Solutions**:
1. Check selected columns contain numbers (not text) for FC and p-values
2. Verify no formula errors in source file
3. Re-export from analysis tool
4. Check for extra header rows

#### Issue: "No significant genes found"

**Symptoms**: Empty table, warning message

**Solutions**:
1. Lower thresholds (try 0.5 FC, 0.1 p-value)
2. Check if data was already filtered
3. Verify p-values are adjusted values
4. Review distribution plots for data quality

#### Issue: Slow performance

**Symptoms**: Long load times, lag

**Solutions**:
1. Reduce dataset size (filter before upload)
2. Close other browser tabs
3. Use CSV instead of reading large files
4. Restart dashboard

#### Issue: Export downloads empty file

**Symptoms**: Download completes but file is empty

**Solutions**:
1. Check if any genes are significant
2. Try different export format
3. Check browser download settings
4. Manually copy table data

#### Issue: Plots look wrong

**Symptoms**: Strange scales, missing data points

**Solutions**:
1. Check for inf/-inf values in data
2. Verify log2FC and p-values in reasonable ranges
3. Try switching plot engine (Plotly ↔ Altair)
4. Reset zoom on plot

### Error Messages

| Error Message | Meaning | Solution |
|--------------|---------|----------|
| "Column 'X' not found" | Selected column doesn't exist | Check spelling, reload file |
| "Numeric conversion error" | Column contains non-numeric data | Clean data in source file |
| "X% missing values" | Many NA values detected | Investigate data quality |
| "File must contain..." | Missing required columns | Add columns or different file |

### Getting Help

If issues persist:

1. **Check documentation**: README, IMPROVEMENTS.md
2. **Review sample data**: Compare with `sample_data.csv`
3. **Test with sample**: Verify dashboard works with included sample
4. **Check dependencies**: Re-install requirements
5. **Browser console**: Look for JavaScript errors (F12)

---

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl + Shift + R` | Reload dashboard |
| `Ctrl + S` | Save plot (in plot mode) |
| `Esc` | Exit fullscreen |
| `Tab` | Navigate controls |
| `Space` | Toggle checkboxes |

---

## Best Practices Summary

✅ **DO**:
- Start with standard thresholds
- Review all visualizations
- Check data quality indicators
- Export gene lists for validation
- Document your threshold choices
- Use adjusted p-values

❌ **DON'T**:
- Use raw p-values without adjustment
- Ignore data quality warnings
- Set extreme thresholds without justification
- Rely on visualization alone (validate genes)
- Share or publish without checking data

---

## Quick Reference Card

### Standard Workflow
```
1. Upload CSV → 2. Map columns → 3. Set thresholds →
4. Review plots → 5. Search genes → 6. Export results
```

### Typical Thresholds
```
Standard: |log2FC| ≥ 1.0, padj < 0.05
Strict:   |log2FC| ≥ 1.5, padj < 0.01
Loose:    |log2FC| ≥ 0.5, padj < 0.10
```

### Export Formats
```
CSV:   Universal, smallest
Excel: Formatted, shareable
All:   Complete dataset
```

---

**Last Updated**: October 2025  
**Version**: 2.0 Enhanced  
**Questions?** Check the FAQ or IMPROVEMENTS.md

---

Happy analyzing! 🧬📊

