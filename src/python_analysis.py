#!/usr/bin/env python3
"""
Python Differential Gene Expression Analysis Script

This script provides a Python-based alternative for analyzing differential
gene expression data. It includes functions for data loading, statistical
analysis, and visualization.

Author: Differential Gene Expression Dashboard Project
Date: 2025
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from typing import Tuple, Dict, Optional
import warnings

warnings.filterwarnings('ignore')

# ============================================================================
# CONFIGURATION
# ============================================================================

# Set paths
DATA_DIR = "data/raw"
OUTPUT_DIR = "data/processed"
PLOTS_DIR = "docs/images"

# Analysis parameters
PADJ_THRESHOLD = 0.05
LOG2FC_THRESHOLD = 1.0

# Plotting style
sns.set_style("whitegrid")
plt.rcParams['figure.dpi'] = 300

# ============================================================================
# DATA LOADING AND PROCESSING
# ============================================================================

def load_results(filepath: str) -> pd.DataFrame:
    """
    Load differential expression results from CSV file.
    
    Parameters:
    -----------
    filepath : str
        Path to CSV file with results
        
    Returns:
    --------
    pd.DataFrame
        Loaded and validated data
    """
    print(f"Loading data from {filepath}...")
    
    df = pd.read_csv(filepath)
    
    # Strip whitespace from column names
    df.columns = df.columns.str.strip()
    
    print(f"✅ Loaded {len(df):,} genes")
    print(f"Columns: {', '.join(df.columns)}")
    
    return df


def validate_data(df: pd.DataFrame, 
                  required_cols: list = ['Gene', 'log2FoldChange', 'padj']) -> bool:
    """
    Validate that dataframe has required columns and data quality.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Data to validate
    required_cols : list
        List of required column names
        
    Returns:
    --------
    bool
        True if validation passes
    """
    print("\nValidating data...")
    
    # Check for required columns
    missing_cols = set(required_cols) - set(df.columns)
    if missing_cols:
        raise ValueError(f"Missing required columns: {missing_cols}")
    
    # Check for NaN values
    for col in required_cols:
        nan_count = df[col].isna().sum()
        nan_pct = nan_count / len(df) * 100
        if nan_pct > 50:
            warnings.warn(f"Column '{col}' has {nan_pct:.1f}% missing values")
    
    print("✅ Data validation passed")
    return True


def add_regulation_status(df: pd.DataFrame,
                          logfc_threshold: float = LOG2FC_THRESHOLD,
                          padj_threshold: float = PADJ_THRESHOLD) -> pd.DataFrame:
    """
    Add regulation status column based on significance thresholds.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Data with log2FoldChange and padj columns
    logfc_threshold : float
        Log2 fold change threshold
    padj_threshold : float
        Adjusted p-value threshold
        
    Returns:
    --------
    pd.DataFrame
        Data with added 'regulation' column
    """
    df = df.copy()
    
    df['regulation'] = 'Not Significant'
    
    # Upregulated genes
    up_mask = (df['padj'] < padj_threshold) & (df['log2FoldChange'] > logfc_threshold)
    df.loc[up_mask, 'regulation'] = 'Upregulated'
    
    # Downregulated genes
    down_mask = (df['padj'] < padj_threshold) & (df['log2FoldChange'] < -logfc_threshold)
    df.loc[down_mask, 'regulation'] = 'Downregulated'
    
    # Calculate -log10(padj) for plotting
    df['-log10(padj)'] = -np.log10(df['padj'])
    
    # Print summary
    print(f"\n📊 Regulation Summary:")
    print(f"  Total genes: {len(df):,}")
    print(f"  Upregulated: {(df['regulation'] == 'Upregulated').sum():,}")
    print(f"  Downregulated: {(df['regulation'] == 'Downregulated').sum():,}")
    print(f"  Not significant: {(df['regulation'] == 'Not Significant').sum():,}")
    
    return df


# ============================================================================
# STATISTICAL ANALYSIS
# ============================================================================

def calculate_statistics(df: pd.DataFrame) -> Dict:
    """
    Calculate summary statistics for the dataset.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Differential expression data
        
    Returns:
    --------
    dict
        Dictionary of statistics
    """
    stats_dict = {
        'total_genes': len(df),
        'significant_genes': (df['regulation'] != 'Not Significant').sum(),
        'upregulated': (df['regulation'] == 'Upregulated').sum(),
        'downregulated': (df['regulation'] == 'Downregulated').sum(),
        'mean_logfc': df['log2FoldChange'].mean(),
        'median_logfc': df['log2FoldChange'].median(),
        'mean_padj': df['padj'].mean(),
        'median_padj': df['padj'].median(),
    }
    
    # Add percentage
    if stats_dict['significant_genes'] > 0:
        stats_dict['percent_significant'] = (
            stats_dict['significant_genes'] / stats_dict['total_genes'] * 100
        )
    else:
        stats_dict['percent_significant'] = 0.0
    
    return stats_dict


def print_statistics(stats: Dict) -> None:
    """Print formatted statistics."""
    print("\n" + "=" * 60)
    print("📊 STATISTICAL SUMMARY")
    print("=" * 60)
    print(f"\nTotal genes:          {stats['total_genes']:,}")
    print(f"Significant genes:    {stats['significant_genes']:,} ({stats['percent_significant']:.2f}%)")
    print(f"  - Upregulated:      {stats['upregulated']:,}")
    print(f"  - Downregulated:    {stats['downregulated']:,}")
    print(f"\nMean log2FC:          {stats['mean_logfc']:.3f}")
    print(f"Median log2FC:        {stats['median_logfc']:.3f}")
    print(f"Mean adj. p-value:    {stats['mean_padj']:.4e}")
    print(f"Median adj. p-value:  {stats['median_padj']:.4e}")
    print("=" * 60 + "\n")


# ============================================================================
# VISUALIZATION
# ============================================================================

def create_volcano_plot(df: pd.DataFrame, 
                       output_path: Optional[str] = None,
                       figsize: Tuple[int, int] = (10, 8)) -> plt.Figure:
    """
    Create volcano plot of differential expression results.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Data with log2FoldChange, padj, and regulation columns
    output_path : str, optional
        Path to save figure
    figsize : tuple
        Figure size (width, height)
        
    Returns:
    --------
    matplotlib.figure.Figure
        The created figure
    """
    fig, ax = plt.subplots(figsize=figsize)
    
    # Plot points by regulation status
    colors = {
        'Upregulated': '#d62728',
        'Downregulated': '#2ca02c',
        'Not Significant': '#7f7f7f'
    }
    
    for regulation, color in colors.items():
        mask = df['regulation'] == regulation
        ax.scatter(
            df.loc[mask, 'log2FoldChange'],
            df.loc[mask, '-log10(padj)'],
            c=color,
            label=regulation,
            alpha=0.6,
            s=20
        )
    
    # Add threshold lines
    ax.axhline(y=-np.log10(PADJ_THRESHOLD), color='black', linestyle='--', 
               linewidth=1, alpha=0.5, label=f'p-adj = {PADJ_THRESHOLD}')
    ax.axvline(x=LOG2FC_THRESHOLD, color='black', linestyle='--', 
               linewidth=1, alpha=0.5)
    ax.axvline(x=-LOG2FC_THRESHOLD, color='black', linestyle='--', 
               linewidth=1, alpha=0.5)
    
    # Labels and title
    ax.set_xlabel('log₂ Fold Change', fontsize=12, fontweight='bold')
    ax.set_ylabel('-log₁₀ Adjusted P-value', fontsize=12, fontweight='bold')
    ax.set_title('Volcano Plot: Differential Gene Expression', 
                 fontsize=14, fontweight='bold', pad=20)
    
    # Legend
    ax.legend(loc='upper right', frameon=True, shadow=True)
    
    # Grid
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    if output_path:
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"✅ Volcano plot saved to {output_path}")
    
    return fig


def create_ma_plot(df: pd.DataFrame,
                   output_path: Optional[str] = None,
                   figsize: Tuple[int, int] = (10, 8)) -> Optional[plt.Figure]:
    """
    Create MA plot if baseMean column is available.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Data with log2FoldChange, baseMean, and regulation columns
    output_path : str, optional
        Path to save figure
    figsize : tuple
        Figure size
        
    Returns:
    --------
    matplotlib.figure.Figure or None
        The created figure, or None if baseMean not available
    """
    if 'baseMean' not in df.columns:
        print("⚠️  baseMean column not found, skipping MA plot")
        return None
    
    fig, ax = plt.subplots(figsize=figsize)
    
    # Calculate log10 base mean
    df['log10_baseMean'] = np.log10(df['baseMean'] + 1)
    
    # Plot by regulation status
    colors = {
        'Upregulated': '#d62728',
        'Downregulated': '#2ca02c',
        'Not Significant': '#7f7f7f'
    }
    
    for regulation, color in colors.items():
        mask = df['regulation'] == regulation
        ax.scatter(
            df.loc[mask, 'log10_baseMean'],
            df.loc[mask, 'log2FoldChange'],
            c=color,
            label=regulation,
            alpha=0.5,
            s=15
        )
    
    # Add zero line
    ax.axhline(y=0, color='black', linestyle='-', linewidth=1, alpha=0.5)
    
    # Labels
    ax.set_xlabel('log₁₀ Mean Expression', fontsize=12, fontweight='bold')
    ax.set_ylabel('log₂ Fold Change', fontsize=12, fontweight='bold')
    ax.set_title('MA Plot: log₂FC vs Mean Expression', 
                 fontsize=14, fontweight='bold', pad=20)
    
    ax.legend(loc='upper right', frameon=True, shadow=True)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    if output_path:
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"✅ MA plot saved to {output_path}")
    
    return fig


# ============================================================================
# EXPORT FUNCTIONS
# ============================================================================

def export_results(df: pd.DataFrame, 
                   output_path: str,
                   export_significant_only: bool = True) -> None:
    """
    Export results to CSV file.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Results data
    output_path : str
        Path for output file
    export_significant_only : bool
        Whether to also export significant genes only
    """
    # Export all results
    df.to_csv(output_path, index=False)
    print(f"✅ All results exported to {output_path}")
    
    # Export significant genes only
    if export_significant_only:
        sig_df = df[df['regulation'] != 'Not Significant'].copy()
        sig_path = output_path.replace('.csv', '_significant.csv')
        sig_df.to_csv(sig_path, index=False)
        print(f"✅ Significant genes exported to {sig_path}")


# ============================================================================
# MAIN ANALYSIS PIPELINE
# ============================================================================

def main():
    """
    Main analysis pipeline.
    
    This is a template - modify paths and parameters as needed.
    """
    print("=" * 60)
    print("Python Differential Gene Expression Analysis")
    print("=" * 60)
    print()
    
    # Example usage - uncomment and modify for your data
    # -----------------------------------------------
    
    # # Load data
    # df = load_results("data/examples/sample_data.csv")
    # 
    # # Validate
    # validate_data(df)
    # 
    # # Add regulation status
    # df = add_regulation_status(df, 
    #                            logfc_threshold=1.0,
    #                            padj_threshold=0.05)
    # 
    # # Calculate and print statistics
    # stats = calculate_statistics(df)
    # print_statistics(stats)
    # 
    # # Create visualizations
    # fig_volcano = create_volcano_plot(df, output_path="docs/images/volcano_plot_python.png")
    # fig_ma = create_ma_plot(df, output_path="docs/images/ma_plot_python.png")
    # 
    # # Export results
    # export_results(df, "data/processed/python_analysis_results.csv")
    # 
    # plt.show()
    
    print("\n" + "=" * 60)
    print("NOTE: This is a template script.")
    print("Please uncomment and modify the main() function with your data paths.")
    print("=" * 60)


if __name__ == "__main__":
    main()

