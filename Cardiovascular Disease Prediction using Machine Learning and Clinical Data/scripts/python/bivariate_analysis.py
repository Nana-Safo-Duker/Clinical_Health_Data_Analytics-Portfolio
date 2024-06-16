"""
Bivariate Analysis

This script performs bivariate analysis on the Cardiovascular Disease Dataset.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)

def load_data():
    """Load the dataset"""
    df = pd.read_csv('../../data/Cardiovascular_Disease_Dataset.csv')
    return df

def correlation_analysis(df):
    """Correlation analysis"""
    numerical_cols = ['age', 'restingBP', 'serumcholestrol', 'maxheartrate', 'oldpeak']
    correlation_matrix = df[numerical_cols].corr()
    
    print("=" * 80)
    print("CORRELATION ANALYSIS")
    print("=" * 80)
    print("\nCorrelation Matrix:")
    print(correlation_matrix)
    
    # Visualize
    plt.figure(figsize=(10, 8))
    sns.heatmap(correlation_matrix, annot=True, fmt='.3f', cmap='coolwarm', center=0)
    plt.title('Correlation Matrix - Numerical Variables')
    plt.tight_layout()
    plt.savefig('../../results/correlation_matrix.png')
    plt.close()

def numerical_vs_target(df):
    """Analyze numerical variables vs target"""
    numerical_cols = ['age', 'restingBP', 'serumcholestrol', 'maxheartrate', 'oldpeak']
    
    print("\n" + "=" * 80)
    print("NUMERICAL VARIABLES VS TARGET")
    print("=" * 80)
    
    for col in numerical_cols:
        if col in df.columns:
            print(f"\n{col.upper()} by Target:")
            grouped = df.groupby('target')[col].agg(['mean', 'median', 'std'])
            print(grouped)
            
            # Statistical test
            group_0 = df[df['target'] == 0][col].dropna()
            group_1 = df[df['target'] == 1][col].dropna()
            statistic, p_value = stats.ttest_ind(group_0, group_1)
            print(f"  t-test p-value: {p_value:.4f} ({'Significant' if p_value < 0.05 else 'Not significant'})")

def categorical_vs_target(df):
    """Analyze categorical variables vs target"""
    categorical_vars = ['gender', 'chestpain', 'fastingbloodsugar', 'restingrelectro', 
                        'exerciseangia', 'slope', 'noofmajorvessels']
    
    print("\n" + "=" * 80)
    print("CATEGORICAL VARIABLES VS TARGET")
    print("=" * 80)
    
    for var in categorical_vars:
        if var in df.columns:
            print(f"\n{var.upper()} vs TARGET:")
            crosstab = pd.crosstab(df[var], df['target'])
            print(crosstab)
            
            # Chi-square test
            chi2, p_value, dof, expected = stats.chi2_contingency(crosstab)
            print(f"  Chi-square p-value: {p_value:.4f} ({'Significant' if p_value < 0.05 else 'Not significant'})")

def visualize_relationships(df):
    """Visualize relationships"""
    numerical_cols = ['age', 'restingBP', 'serumcholestrol', 'maxheartrate', 'oldpeak']
    
    fig, axes = plt.subplots(2, 3, figsize=(18, 10))
    axes = axes.ravel()
    
    for idx, col in enumerate(numerical_cols):
        if col in df.columns and idx < len(axes):
            data_to_plot = [df[df['target'] == 0][col].dropna(), 
                            df[df['target'] == 1][col].dropna()]
            axes[idx].violinplot(data_to_plot, positions=[0, 1])
            axes[idx].set_xticks([0, 1])
            axes[idx].set_xticklabels(['No Disease', 'Disease'])
            axes[idx].set_title(f'{col} by Target')
            axes[idx].set_ylabel(col)
    
    if len(numerical_cols) < len(axes):
        fig.delaxes(axes[len(numerical_cols)])
    
    plt.tight_layout()
    plt.savefig('../../results/bivariate_analysis.png')
    plt.close()

def main():
    """Main function"""
    df = load_data()
    correlation_analysis(df)
    numerical_vs_target(df)
    categorical_vs_target(df)
    visualize_relationships(df)
    print("\nBivariate analysis complete!")

if __name__ == "__main__":
    main()

