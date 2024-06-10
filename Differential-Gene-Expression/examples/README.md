# Examples

This directory contains example data and demonstrations for the Differential Gene Expression Dashboard.

## Contents

### Sample Data

#### `sample_data.csv`
A complete example dataset containing 51 genes with realistic differential expression data.

**Columns:**
- `Gene`: Gene symbols (e.g., TP53, BRCA1, EGFR)
- `log2FoldChange`: Log2 fold change values (range: -2.5 to 3.2)
- `padj`: Adjusted p-values (range: 0.0001 to 0.089)
- `baseMean`: Mean expression values (enables MA plot)
- `pvalue`: Raw p-values
- `regulation`: Upregulated/Downregulated/Not Significant

**Statistics:**
- Total genes: 51
- Significant (padj < 0.05, |log2FC| >= 1.0): 48
- Upregulated: 28
- Downregulated: 20
- Not significant: 3

**Usage:**
```bash
# Launch dashboard
streamlit run app/dashboard.py

# Upload sample_data.csv
# Column mapping will be automatic (names already match)
# Explore all visualizations
```

---

## Quick Start with Sample Data

### Step 1: Launch Dashboard
```bash
python scripts/quick_start.py
```

### Step 2: Upload File
Click "Browse files" and select `examples/sample_data.csv`

### Step 3: Verify Mapping
Columns should auto-map:
- Gene Name Column → `Gene`
- Log2 Fold Change → `log2FoldChange`
- Adjusted P-value → `padj`
- Regulation Column → `regulation`
- Mean Expression → `baseMean`

### Step 4: Explore
- View volcano plot (48 significant genes)
- Check MA plot (baseMean included)
- See top 20 genes chart
- Review distributions
- Export results

---

## Creating Your Own Test Data

### From R (DESeq2)

```R
library(DESeq2)

# After running DESeq2 analysis
results_df <- as.data.frame(results(dds))
results_df$Gene <- rownames(results_df)

# Add regulation column
results_df$regulation <- ifelse(
  results_df$padj < 0.05 & abs(results_df$log2FoldChange) >= 1,
  ifelse(results_df$log2FoldChange > 0, "Upregulated", "Downregulated"),
  "Not Significant"
)

# Export
write.csv(results_df, "my_deseq2_results.csv", row.names=FALSE)
```

### From R (edgeR)

```R
library(edgeR)

# After running edgeR analysis
results_df <- topTags(lrt, n=Inf)$table
results_df$Gene <- rownames(results_df)

# Rename columns to match expected names
colnames(results_df)[colnames(results_df) == "logFC"] <- "log2FoldChange"
colnames(results_df)[colnames(results_df) == "FDR"] <- "padj"
colnames(results_df)[colnames(results_df) == "PValue"] <- "pvalue"

# Add regulation
results_df$regulation <- ifelse(
  results_df$padj < 0.05 & abs(results_df$log2FoldChange) >= 1,
  ifelse(results_df$log2FoldChange > 0, "Upregulated", "Downregulated"),
  "Not Significant"
)

write.csv(results_df, "my_edger_results.csv", row.names=FALSE)
```

### From Python (Synthetic)

```python
import pandas as pd
import numpy as np

np.random.seed(42)

n_genes = 100

# Create synthetic data
data = {
    'Gene': [f'GENE{i:03d}' for i in range(1, n_genes + 1)],
    'log2FoldChange': np.random.normal(0, 1.5, n_genes),
    'padj': np.random.beta(0.5, 2, n_genes),
    'baseMean': np.random.lognormal(8, 2, n_genes),
    'pvalue': np.random.beta(0.5, 2, n_genes)
}

df = pd.DataFrame(data)

# Add regulation
df['regulation'] = 'Not Significant'
df.loc[(df['padj'] < 0.05) & (df['log2FoldChange'] >= 1), 'regulation'] = 'Upregulated'
df.loc[(df['padj'] < 0.05) & (df['log2FoldChange'] <= -1), 'regulation'] = 'Downregulated'

# Save
df.to_csv('synthetic_data.csv', index=False)
```

---

## Example Analyses

### Example 1: Cancer vs Normal

Dataset characteristics:
- Many upregulated oncogenes
- Downregulated tumor suppressors
- Clear separation in volcano plot

**Expected results:**
- ~30-40% significant genes
- Stronger upregulation than downregulation
- Enrichment in cancer-related pathways

### Example 2: Treatment vs Control

Dataset characteristics:
- Moderate number of DE genes
- Balanced up/down regulation
- Drug target genes highly significant

**Expected results:**
- ~10-20% significant genes
- Roughly equal up/down genes
- Treatment response pathways enriched

### Example 3: Time Series

Dataset characteristics:
- Progressive changes over time
- Early vs late response genes
- Transient vs sustained changes

**Expected results:**
- Time-dependent significance
- Different genes at each timepoint
- Patterns in expression dynamics

---

## Validation Datasets

For testing dashboard functionality:

### Small Dataset (10 genes)
Good for: Quick testing, demonstrations
```csv
Gene,log2FoldChange,padj
GENE1,2.5,0.001
GENE2,-2.1,0.002
...
```

### Medium Dataset (100-1000 genes)
Good for: Typical analyses, performance testing
- Representative of real experiments
- All features accessible

### Large Dataset (10,000+ genes)
Good for: Performance testing, edge cases
- Tests scalability
- May need optimization

---

## File Format Requirements

### Minimum Required
```csv
Gene,log2FoldChange,padj
GENE1,2.5,0.001
GENE2,-1.8,0.01
```

### Recommended
```csv
Gene,log2FoldChange,padj,baseMean,pvalue,regulation
GENE1,2.5,0.001,5432.1,0.0005,Upregulated
GENE2,-1.8,0.01,3421.2,0.005,Downregulated
```

### With Additional Metadata
```csv
Gene,log2FoldChange,padj,baseMean,pvalue,regulation,description,pathway
GENE1,2.5,0.001,5432.1,0.0005,Upregulated,"Tumor protein p53","Cell cycle"
GENE2,-1.8,0.01,3421.2,0.005,Downregulated,"BRCA1 DNA repair","DNA repair"
```

---

## Tips for Good Example Data

1. **Include edge cases**
   - Very high fold changes
   - Very low p-values
   - Borderline significance

2. **Realistic distributions**
   - Most genes not significant
   - P-values enriched near 0
   - Fold changes centered at 0

3. **Include metadata**
   - Gene descriptions
   - Pathway annotations
   - External IDs

4. **Document source**
   - Where data came from
   - Analysis parameters used
   - Date and version

---

## Contributing Examples

Have an interesting dataset? Contribute it!

1. Ensure data is anonymized (if needed)
2. Document the experimental design
3. Include expected results
4. Add to this directory with descriptive name
5. Update this README
6. Submit pull request

---

## Additional Resources

- **Dashboard documentation**: [docs/USER_GUIDE.md](../docs/USER_GUIDE.md)
- **Data preparation**: [docs/INSTALLATION.md](../docs/INSTALLATION.md)
- **API reference**: [docs/API.md](../docs/API.md)

---

**Questions?** Open an issue or discussion on GitHub!


