"""
Univariate, Bivariate, and Multivariate Analysis
Comprehensive analysis of health data
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# Set style
sns.set_style('whitegrid')
plt.rcParams['figure.figsize'] = (14, 8)

def load_and_clean_data():
    """Load and clean the health data"""
    df = pd.read_csv('../data/health_data.csv')
    if 'Unnamed: 0' in df.columns:
        df = df.drop('Unnamed: 0', axis=1)
    df['age_years'] = df['age'] / 365.25
    df['bmi'] = df['weight'] / ((df['height'] / 100) ** 2)
    df = df[(df['ap_hi'] >= 80) & (df['ap_hi'] <= 250)]
    df = df[(df['ap_lo'] >= 40) & (df['ap_lo'] <= 150)]
    df = df[df['ap_hi'] >= df['ap_lo']]
    df = df[(df['height'] >= 100) & (df['height'] <= 220)]
    df = df[(df['weight'] >= 30) & (df['weight'] <= 200)]
    df = df[(df['bmi'] >= 10) & (df['bmi'] <= 60)]
    return df

def univariate_analysis(df):
    """Perform univariate analysis"""
    print("=" * 80)
    print("UNIVARIATE ANALYSIS")
    print("=" * 80)
    
    # Numerical variables
    numerical_cols = ['age_years', 'height', 'weight', 'ap_hi', 'ap_lo', 'bmi']
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    axes = axes.ravel()
    
    for i, col in enumerate(numerical_cols):
        axes[i].hist(df[col], bins=50, density=True, alpha=0.7, edgecolor='black')
        df[col].plot.density(ax=axes[i], color='red', linewidth=2)
        axes[i].set_title(f'{col.upper()} Distribution', fontsize=12, fontweight='bold')
        axes[i].set_xlabel(col)
        axes[i].set_ylabel('Density')
        axes[i].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('../figures/univariate_numerical.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # Categorical variables
    categorical_cols = ['gender', 'cholesterol', 'gluc', 'smoke', 'alco', 'active', 'cardio']
    fig, axes = plt.subplots(3, 3, figsize=(18, 15))
    axes = axes.ravel()
    
    for i, col in enumerate(categorical_cols):
        value_counts = df[col].value_counts().sort_index()
        axes[i].bar(value_counts.index.astype(str), value_counts.values, color='steelblue', edgecolor='black')
        axes[i].set_title(f'{col.upper()} Distribution', fontsize=12, fontweight='bold')
        axes[i].set_xlabel(col)
        axes[i].set_ylabel('Count')
        axes[i].grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    plt.savefig('../figures/univariate_categorical.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("Univariate analysis completed. Figures saved.")

def bivariate_analysis(df):
    """Perform bivariate analysis"""
    print("=" * 80)
    print("BIVARIATE ANALYSIS")
    print("=" * 80)
    
    # Scatter plots
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    axes = axes.ravel()
    
    pairs = [('age_years', 'bmi'), ('ap_hi', 'ap_lo'), ('weight', 'height'), ('ap_hi', 'bmi')]
    for i, (x, y) in enumerate(pairs):
        axes[i].scatter(df[x], df[y], alpha=0.3, s=10)
        axes[i].set_xlabel(x, fontsize=11)
        axes[i].set_ylabel(y, fontsize=11)
        axes[i].set_title(f'{x.upper()} vs {y.upper()}', fontsize=12, fontweight='bold')
        axes[i].grid(True, alpha=0.3)
        
        corr = df[[x, y]].corr().iloc[0, 1]
        axes[i].text(0.05, 0.95, f'r = {corr:.3f}', transform=axes[i].transAxes, 
                    fontsize=11, verticalalignment='top', 
                    bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    plt.tight_layout()
    plt.savefig('../figures/bivariate_scatter.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # Box plots
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    axes = axes.ravel()
    
    comparisons = [('bmi', 'cardio'), ('age_years', 'cardio'), ('ap_hi', 'cardio'),
                   ('bmi', 'gender'), ('ap_hi', 'cholesterol'), ('bmi', 'smoke')]
    
    for i, (numerical, categorical) in enumerate(comparisons):
        sns.boxplot(data=df, x=categorical, y=numerical, ax=axes[i])
        axes[i].set_title(f'{numerical.upper()} by {categorical.upper()}', fontsize=12, fontweight='bold')
        axes[i].set_xlabel(categorical)
        axes[i].set_ylabel(numerical)
        axes[i].grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    plt.savefig('../figures/bivariate_boxplots.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # Heatmaps
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    axes = axes.ravel()
    
    categorical_vars = ['gender', 'cholesterol', 'gluc', 'smoke', 'alco', 'active']
    for i, var in enumerate(categorical_vars):
        crosstab = pd.crosstab(df[var], df['cardio'], normalize='index') * 100
        sns.heatmap(crosstab, annot=True, fmt='.1f', cmap='YlOrRd', ax=axes[i], cbar_kws={'label': '%'})
        axes[i].set_title(f'{var.upper()} vs Cardio', fontsize=12, fontweight='bold')
        axes[i].set_xlabel('Cardio')
        axes[i].set_ylabel(var)
    
    plt.tight_layout()
    plt.savefig('../figures/bivariate_heatmaps.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("Bivariate analysis completed. Figures saved.")

def multivariate_analysis(df):
    """Perform multivariate analysis"""
    print("=" * 80)
    print("MULTIVARIATE ANALYSIS")
    print("=" * 80)
    
    # Correlation heatmap
    numerical_cols = ['age_years', 'height', 'weight', 'ap_hi', 'ap_lo', 'bmi', 'cardio']
    correlation_matrix = df[numerical_cols].corr()
    
    plt.figure(figsize=(12, 10))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0, 
                square=True, linewidths=1, cbar_kws={'shrink': 0.8}, fmt='.3f')
    plt.title('Multivariate Correlation Matrix', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig('../figures/multivariate_correlation.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # Pair plot
    key_vars = ['age_years', 'bmi', 'ap_hi', 'ap_lo', 'cardio']
    pair_df = df[key_vars].sample(n=min(5000, len(df)), random_state=42)
    
    sns.pairplot(pair_df, hue='cardio', diag_kind='kde', palette=['skyblue', 'salmon'])
    plt.suptitle('Pair Plot: Key Variables by Cardio Status', y=1.02, fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig('../figures/multivariate_pairplot.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("Multivariate analysis completed. Figures saved.")

if __name__ == "__main__":
    df = load_and_clean_data()
    univariate_analysis(df)
    bivariate_analysis(df)
    multivariate_analysis(df)
    print("\nAll analyses completed successfully!")

