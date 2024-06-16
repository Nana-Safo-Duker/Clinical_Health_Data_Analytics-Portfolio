"""
Heart Disease Dataset - Univariate, Bivariate, and Multivariate Analysis

This script performs comprehensive univariate, bivariate, and multivariate analysis
on the heart disease dataset.

Author: Data Science Team
Date: 2024
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import warnings
import os
import sys

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

warnings.filterwarnings('ignore')

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)

# Load data
def load_data():
    """Load the heart disease dataset."""
    data_path = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'heart-disease.csv')
    df = pd.read_csv(data_path)
    print("Dataset loaded successfully!")
    print(f"Shape: {df.shape}")
    return df

# Univariate Analysis
def univariate_analysis(df, output_dir='../../results/figures'):
    """Perform univariate analysis on the dataset."""
    print("\n" + "="*60)
    print("UNIVARIATE ANALYSIS")
    print("="*60)
    
    numerical_cols = ['age', 'rest_bp', 'chol', 'max_hr', 'st_depr']
    categorical_cols = ['sex', 'chest_pain', 'heart_disease']
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Numerical variables - distributions
    fig, axes = plt.subplots(2, 3, figsize=(18, 10))
    axes = axes.ravel()
    
    for idx, col in enumerate(numerical_cols):
        axes[idx].hist(df[col], bins=30, alpha=0.7, edgecolor='black', density=True)
        df[col].plot.density(ax=axes[idx], color='red', linewidth=2)
        axes[idx].axvline(df[col].mean(), color='green', linestyle='--', label=f'Mean: {df[col].mean():.2f}')
        axes[idx].axvline(df[col].median(), color='blue', linestyle='--', label=f'Median: {df[col].median():.2f}')
        axes[idx].set_title(f'Distribution of {col}', fontsize=12, fontweight='bold')
        axes[idx].set_xlabel(col)
        axes[idx].set_ylabel('Density')
        axes[idx].legend()
        axes[idx].grid(True, alpha=0.3)
    
    fig.delaxes(axes[5])
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'univariate_numerical_distributions.png'), dpi=300, bbox_inches='tight')
    plt.close()
    print("Saved: univariate_numerical_distributions.png")
    
    # Box plots
    fig, axes = plt.subplots(1, 5, figsize=(20, 4))
    for idx, col in enumerate(numerical_cols):
        axes[idx].boxplot(df[col], vert=True)
        axes[idx].set_title(f'Box Plot: {col}', fontsize=10, fontweight='bold')
        axes[idx].set_ylabel(col)
        axes[idx].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'univariate_boxplots.png'), dpi=300, bbox_inches='tight')
    plt.close()
    print("Saved: univariate_boxplots.png")
    
    # Categorical variables
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    for idx, col in enumerate(categorical_cols):
        value_counts = df[col].value_counts()
        axes[idx].bar(value_counts.index.astype(str), value_counts.values, alpha=0.7, edgecolor='black')
        axes[idx].set_title(f'Distribution of {col}', fontsize=12, fontweight='bold')
        axes[idx].set_xlabel(col)
        axes[idx].set_ylabel('Frequency')
        axes[idx].grid(True, alpha=0.3, axis='y')
        for i, v in enumerate(value_counts.values):
            axes[idx].text(i, v, str(v), ha='center', va='bottom')
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'univariate_categorical.png'), dpi=300, bbox_inches='tight')
    plt.close()
    print("Saved: univariate_categorical.png")
    
    # Summary statistics
    print("\nSummary Statistics:")
    for col in numerical_cols:
        print(f"\n{col.upper()}:")
        print(f"  Mean: {df[col].mean():.2f}")
        print(f"  Median: {df[col].median():.2f}")
        print(f"  Std Dev: {df[col].std():.2f}")
        print(f"  Skewness: {df[col].skew():.2f}")
        print(f"  Kurtosis: {df[col].kurtosis():.2f}")

# Bivariate Analysis
def bivariate_analysis(df, output_dir='../../results/figures'):
    """Perform bivariate analysis on the dataset."""
    print("\n" + "="*60)
    print("BIVARIATE ANALYSIS")
    print("="*60)
    
    numerical_cols = ['age', 'rest_bp', 'chol', 'max_hr', 'st_depr']
    
    # Violin plots: Numerical vs Target
    fig, axes = plt.subplots(2, 3, figsize=(18, 10))
    axes = axes.ravel()
    
    for idx, col in enumerate(numerical_cols):
        data_to_plot = [df[df['heart_disease'] == 0][col], df[df['heart_disease'] == 1][col]]
        parts = axes[idx].violinplot(data_to_plot, positions=[0, 1], showmeans=True, showmedians=True)
        axes[idx].set_xticks([0, 1])
        axes[idx].set_xticklabels(['No Heart Disease', 'Heart Disease'])
        axes[idx].set_title(f'{col} vs Heart Disease', fontsize=12, fontweight='bold')
        axes[idx].set_ylabel(col)
        axes[idx].grid(True, alpha=0.3, axis='y')
    
    fig.delaxes(axes[5])
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'bivariate_violin_plots.png'), dpi=300, bbox_inches='tight')
    plt.close()
    print("Saved: bivariate_violin_plots.png")
    
    # Categorical vs Target
    fig, axes = plt.subplots(1, 2, figsize=(15, 5))
    
    crosstab1 = pd.crosstab(df['sex'], df['heart_disease'])
    crosstab1.plot(kind='bar', ax=axes[0], alpha=0.7, edgecolor='black')
    axes[0].set_title('Sex vs Heart Disease', fontsize=12, fontweight='bold')
    axes[0].set_xlabel('Sex')
    axes[0].set_ylabel('Frequency')
    axes[0].legend(['No Heart Disease', 'Heart Disease'])
    axes[0].grid(True, alpha=0.3, axis='y')
    axes[0].tick_params(axis='x', rotation=0)
    
    crosstab2 = pd.crosstab(df['chest_pain'], df['heart_disease'])
    crosstab2.plot(kind='bar', ax=axes[1], alpha=0.7, edgecolor='black')
    axes[1].set_title('Chest Pain vs Heart Disease', fontsize=12, fontweight='bold')
    axes[1].set_xlabel('Chest Pain Type')
    axes[1].set_ylabel('Frequency')
    axes[1].legend(['No Heart Disease', 'Heart Disease'])
    axes[1].grid(True, alpha=0.3, axis='y')
    axes[1].tick_params(axis='x', rotation=0)
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'bivariate_categorical.png'), dpi=300, bbox_inches='tight')
    plt.close()
    print("Saved: bivariate_categorical.png")
    
    # Correlation matrix
    correlation_matrix = df[numerical_cols].corr()
    plt.figure(figsize=(10, 8))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0, 
                square=True, linewidths=1, cbar_kws={"shrink": 0.8}, fmt='.2f')
    plt.title('Correlation Matrix - Numerical Variables', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'bivariate_correlation_matrix.png'), dpi=300, bbox_inches='tight')
    plt.close()
    print("Saved: bivariate_correlation_matrix.png")
    
    # Pairwise scatter plots
    sns.pairplot(df[numerical_cols + ['heart_disease']], hue='heart_disease', 
                 diag_kind='kde', markers=['o', 's'], palette='Set2')
    plt.suptitle('Pairwise Relationships - Numerical Variables', 
                 fontsize=14, fontweight='bold', y=1.02)
    plt.savefig(os.path.join(output_dir, 'bivariate_pairplot.png'), dpi=300, bbox_inches='tight')
    plt.close()
    print("Saved: bivariate_pairplot.png")

# Multivariate Analysis
def multivariate_analysis(df, output_dir='../../results/figures'):
    """Perform multivariate analysis on the dataset."""
    print("\n" + "="*60)
    print("MULTIVARIATE ANALYSIS")
    print("="*60)
    
    numerical_cols = ['age', 'rest_bp', 'chol', 'max_hr', 'st_depr']
    
    # Multivariate correlation heatmap
    plt.figure(figsize=(12, 10))
    correlation_matrix_full = df[numerical_cols + ['heart_disease']].corr()
    sns.heatmap(correlation_matrix_full, annot=True, cmap='RdYlBu_r', center=0, 
                square=True, linewidths=2, cbar_kws={"shrink": 0.8}, fmt='.2f',
                annot_kws={'size': 10})
    plt.title('Multivariate Correlation Heatmap', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'multivariate_heatmap.png'), dpi=300, bbox_inches='tight')
    plt.close()
    print("Saved: multivariate_heatmap.png")
    
    # Faceted plots
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    
    # Age vs Cholesterol
    for hd_status in [0, 1]:
        subset = df[df['heart_disease'] == hd_status]
        axes[0, 0].scatter(subset['age'], subset['chol'], 
                          alpha=0.6, label=f'HD={hd_status}', s=50)
    axes[0, 0].set_xlabel('Age')
    axes[0, 0].set_ylabel('Cholesterol')
    axes[0, 0].set_title('Age vs Cholesterol by Heart Disease', fontweight='bold')
    axes[0, 0].legend()
    axes[0, 0].grid(True, alpha=0.3)
    
    # Age vs Max Heart Rate
    for hd_status in [0, 1]:
        subset = df[df['heart_disease'] == hd_status]
        axes[0, 1].scatter(subset['age'], subset['max_hr'], 
                          alpha=0.6, label=f'HD={hd_status}', s=50)
    axes[0, 1].set_xlabel('Age')
    axes[0, 1].set_ylabel('Max Heart Rate')
    axes[0, 1].set_title('Age vs Max Heart Rate by Heart Disease', fontweight='bold')
    axes[0, 1].legend()
    axes[0, 1].grid(True, alpha=0.3)
    
    # Cholesterol vs Max Heart Rate
    for hd_status in [0, 1]:
        subset = df[df['heart_disease'] == hd_status]
        axes[1, 0].scatter(subset['chol'], subset['max_hr'], 
                          alpha=0.6, label=f'HD={hd_status}', s=50)
    axes[1, 0].set_xlabel('Cholesterol')
    axes[1, 0].set_ylabel('Max Heart Rate')
    axes[1, 0].set_title('Cholesterol vs Max Heart Rate by Heart Disease', fontweight='bold')
    axes[1, 0].legend()
    axes[1, 0].grid(True, alpha=0.3)
    
    # Rest BP vs ST Depression
    for hd_status in [0, 1]:
        subset = df[df['heart_disease'] == hd_status]
        axes[1, 1].scatter(subset['rest_bp'], subset['st_depr'], 
                          alpha=0.6, label=f'HD={hd_status}', s=50)
    axes[1, 1].set_xlabel('Resting Blood Pressure')
    axes[1, 1].set_ylabel('ST Depression')
    axes[1, 1].set_title('Rest BP vs ST Depression by Heart Disease', fontweight='bold')
    axes[1, 1].legend()
    axes[1, 1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'multivariate_faceted_plots.png'), dpi=300, bbox_inches='tight')
    plt.close()
    print("Saved: multivariate_faceted_plots.png")
    
    # Grouped statistics
    print("\nGrouped Statistics by Sex and Heart Disease:")
    grouped_stats = df.groupby(['sex', 'heart_disease'])[numerical_cols].mean()
    print(grouped_stats)
    
    print("\n\nGrouped Statistics by Chest Pain and Heart Disease:")
    grouped_stats2 = df.groupby(['chest_pain', 'heart_disease'])[numerical_cols].mean()
    print(grouped_stats2)
    
    # Correlations with target
    print("\n\nCorrelations with Heart Disease:")
    for col in numerical_cols:
        corr = df[col].corr(df['heart_disease'])
        print(f"  {col}: {corr:.4f}")

def main():
    """Main function to run all analyses."""
    print("Heart Disease Dataset - Univariate, Bivariate, Multivariate Analysis")
    print("="*60)
    
    # Load data
    df = load_data()
    
    # Run analyses
    univariate_analysis(df)
    bivariate_analysis(df)
    multivariate_analysis(df)
    
    print("\n" + "="*60)
    print("Analysis complete! Check results/figures/ for output files.")
    print("="*60)

if __name__ == "__main__":
    main()

