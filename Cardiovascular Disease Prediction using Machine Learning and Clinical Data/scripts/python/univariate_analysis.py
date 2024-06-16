"""
Univariate Analysis

This script performs univariate analysis on the Cardiovascular Disease Dataset.
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

def univariate_numerical(df):
    """Univariate analysis for numerical variables"""
    numerical_cols = ['age', 'restingBP', 'serumcholestrol', 'maxheartrate', 'oldpeak']
    
    print("=" * 80)
    print("UNIVARIATE ANALYSIS - NUMERICAL VARIABLES")
    print("=" * 80)
    
    for col in numerical_cols:
        if col in df.columns:
            print(f"\n{col.upper()}:")
            print(f"  Mean: {df[col].mean():.2f}")
            print(f"  Median: {df[col].median():.2f}")
            print(f"  Std Dev: {df[col].std():.2f}")
            print(f"  Min: {df[col].min():.2f}")
            print(f"  Max: {df[col].max():.2f}")
            print(f"  Skewness: {df[col].skew():.4f}")
            print(f"  Kurtosis: {df[col].kurtosis():.4f}")
            
            # Outlier detection
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            outliers = df[(df[col] < Q1 - 1.5 * IQR) | (df[col] > Q3 + 1.5 * IQR)]
            print(f"  Outliers: {len(outliers)} ({len(outliers)/len(df)*100:.2f}%)")

def univariate_categorical(df):
    """Univariate analysis for categorical variables"""
    categorical_cols = ['gender', 'chestpain', 'fastingbloodsugar', 'restingrelectro', 
                        'exerciseangia', 'slope', 'noofmajorvessels', 'target']
    
    print("\n" + "=" * 80)
    print("UNIVARIATE ANALYSIS - CATEGORICAL VARIABLES")
    print("=" * 80)
    
    for col in categorical_cols:
        if col in df.columns:
            print(f"\n{col.upper()}:")
            value_counts = df[col].value_counts()
            print(value_counts)
            print(f"Percentage: {value_counts / len(df) * 100}")

def visualize_distributions(df):
    """Visualize distributions"""
    numerical_cols = ['age', 'restingBP', 'serumcholestrol', 'maxheartrate', 'oldpeak']
    
    fig, axes = plt.subplots(len(numerical_cols), 2, figsize=(14, 4*len(numerical_cols)))
    
    for idx, col in enumerate(numerical_cols):
        if col in df.columns:
            # Histogram
            axes[idx, 0].hist(df[col].dropna(), bins=30, color='steelblue', alpha=0.7)
            axes[idx, 0].set_title(f'Histogram: {col}')
            axes[idx, 0].set_xlabel(col)
            axes[idx, 0].set_ylabel('Frequency')
            
            # Box plot
            axes[idx, 1].boxplot(df[col].dropna())
            axes[idx, 1].set_title(f'Box Plot: {col}')
            axes[idx, 1].set_ylabel(col)
    
    plt.tight_layout()
    plt.savefig('../../results/univariate_analysis.png')
    plt.close()

def main():
    """Main function"""
    df = load_data()
    univariate_numerical(df)
    univariate_categorical(df)
    visualize_distributions(df)
    print("\nUnivariate analysis complete!")

if __name__ == "__main__":
    main()

