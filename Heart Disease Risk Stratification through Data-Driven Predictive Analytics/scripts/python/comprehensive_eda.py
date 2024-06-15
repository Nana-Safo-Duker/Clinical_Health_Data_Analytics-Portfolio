"""
Heart Disease Dataset - Comprehensive Exploratory Data Analysis

This script performs comprehensive EDA including data quality assessment,
univariate, bivariate, and multivariate analysis.

Author: Data Science Team
Date: 2024
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from scipy.stats import normaltest, shapiro, chi2_contingency, ttest_ind, pearsonr
import warnings
import os

warnings.filterwarnings('ignore')

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)

def load_data():
    """Load the heart disease dataset."""
    data_path = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'heart-disease.csv')
    df = pd.read_csv(data_path)
    print("Dataset loaded successfully!")
    print(f"Shape: {df.shape}")
    return df

def data_overview(df):
    """Perform data overview and quality assessment."""
    print("="*60)
    print("DATA OVERVIEW")
    print("="*60)
    print(f"Dataset shape: {df.shape}")
    print(f"Columns: {list(df.columns)}")
    print(f"\nData types:\n{df.dtypes}")
    print(f"\nMissing values:\n{df.isnull().sum()}")
    print(f"\nDuplicate rows: {df.duplicated().sum()}")
    print(f"\nBasic statistics:\n{df.describe()}")
    return df

def univariate_analysis(df, output_dir='../../results/figures'):
    """Perform univariate analysis."""
    print("="*60)
    print("UNIVARIATE ANALYSIS")
    print("="*60)
    
    numerical_cols = ['age', 'rest_bp', 'chol', 'max_hr', 'st_depr']
    categorical_cols = ['sex', 'chest_pain', 'heart_disease']
    
    os.makedirs(output_dir, exist_ok=True)
    
    # Numerical distributions
    fig, axes = plt.subplots(2, 3, figsize=(18, 10))
    axes = axes.ravel()
    
    for idx, col in enumerate(numerical_cols):
        axes[idx].hist(df[col], bins=30, alpha=0.7, edgecolor='black', density=True)
        df[col].plot.density(ax=axes[idx], color='red', linewidth=2)
        axes[idx].axvline(df[col].mean(), color='green', linestyle='--', label='Mean')
        axes[idx].axvline(df[col].median(), color='blue', linestyle='--', label='Median')
        axes[idx].set_title(f'Distribution of {col}', fontweight='bold')
        axes[idx].legend()
        axes[idx].grid(True, alpha=0.3)
    
    fig.delaxes(axes[5])
    plt.suptitle('Univariate Analysis: Numerical Distributions', fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'eda_univariate_numerical.png'), dpi=300, bbox_inches='tight')
    plt.close()
    
    # Categorical distributions
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    for idx, col in enumerate(categorical_cols):
        value_counts = df[col].value_counts().sort_index()
        axes[idx].bar(range(len(value_counts)), value_counts.values, alpha=0.7, edgecolor='black')
        axes[idx].set_xticks(range(len(value_counts)))
        axes[idx].set_xticklabels([str(x) for x in value_counts.index], rotation=0)
        axes[idx].set_title(f'Distribution of {col}', fontweight='bold')
        axes[idx].set_ylabel('Frequency')
        axes[idx].grid(True, alpha=0.3, axis='y')
    
    plt.suptitle('Univariate Analysis: Categorical Distributions', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'eda_univariate_categorical.png'), dpi=300, bbox_inches='tight')
    plt.close()
    
    print("Univariate analysis plots saved.")

def bivariate_analysis(df, output_dir='../../results/figures'):
    """Perform bivariate analysis."""
    print("="*60)
    print("BIVARIATE ANALYSIS")
    print("="*60)
    
    numerical_cols = ['age', 'rest_bp', 'chol', 'max_hr', 'st_depr']
    os.makedirs(output_dir, exist_ok=True)
    
    # Numerical vs Target
    fig, axes = plt.subplots(2, 3, figsize=(18, 10))
    axes = axes.ravel()
    
    for idx, col in enumerate(numerical_cols):
        data_to_plot = [df[df['heart_disease'] == 0][col], df[df['heart_disease'] == 1][col]]
        axes[idx].boxplot(data_to_plot, labels=['No HD', 'HD'])
        axes[idx].set_title(f'{col} vs Heart Disease', fontweight='bold')
        axes[idx].set_ylabel(col)
        axes[idx].grid(True, alpha=0.3, axis='y')
    
    fig.delaxes(axes[5])
    plt.suptitle('Bivariate Analysis: Numerical vs Target', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'eda_bivariate_numerical.png'), dpi=300, bbox_inches='tight')
    plt.close()
    
    # Correlation heatmap
    correlation_matrix = df[numerical_cols + ['heart_disease']].corr()
    plt.figure(figsize=(10, 8))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0, 
                square=True, linewidths=1, fmt='.2f')
    plt.title('Correlation Heatmap', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'eda_correlation_heatmap.png'), dpi=300, bbox_inches='tight')
    plt.close()
    
    print("Bivariate analysis plots saved.")

def multivariate_analysis(df, output_dir='../../results/figures'):
    """Perform multivariate analysis."""
    print("="*60)
    print("MULTIVARIATE ANALYSIS")
    print("="*60)
    
    numerical_cols = ['age', 'rest_bp', 'chol', 'max_hr', 'st_depr']
    os.makedirs(output_dir, exist_ok=True)
    
    # Pairplot
    sns.pairplot(df[numerical_cols + ['heart_disease']], hue='heart_disease', 
                 diag_kind='kde', markers=['o', 's'], palette='Set2')
    plt.suptitle('Multivariate Pairwise Relationships', fontsize=14, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'eda_multivariate_pairplot.png'), dpi=300, bbox_inches='tight')
    plt.close()
    
    print("Multivariate analysis plots saved.")

def main():
    """Main function to run EDA."""
    print("="*60)
    print("COMPREHENSIVE EXPLORATORY DATA ANALYSIS")
    print("="*60)
    
    # Load data
    df = load_data()
    
    # Data overview
    data_overview(df)
    
    # Analyses
    univariate_analysis(df)
    bivariate_analysis(df)
    multivariate_analysis(df)
    
    print("\n" + "="*60)
    print("EDA Complete! Check results/figures/ for output files.")
    print("="*60)

if __name__ == "__main__":
    main()

