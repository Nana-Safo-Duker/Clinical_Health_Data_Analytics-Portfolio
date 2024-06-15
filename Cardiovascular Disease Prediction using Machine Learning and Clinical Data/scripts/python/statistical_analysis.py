"""
Statistical Analysis: Descriptive, Inferential, and Exploratory

This script performs comprehensive statistical analysis of the Cardiovascular Disease Dataset,
including descriptive statistics, inferential statistics, and exploratory data analysis.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from scipy.stats import ttest_ind, chi2_contingency, f_oneway, shapiro
import warnings
warnings.filterwarnings('ignore')

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)

def load_data():
    """Load the dataset"""
    df = pd.read_csv('../../data/Cardiovascular_Disease_Dataset.csv')
    print("Dataset loaded successfully!")
    print(f"Shape: {df.shape}")
    return df

def descriptive_statistics(df):
    """Perform descriptive statistics"""
    print("=" * 80)
    print("DESCRIPTIVE STATISTICS")
    print("=" * 80)
    
    numerical_cols = ['age', 'restingBP', 'serumcholestrol', 'maxheartrate', 'oldpeak']
    categorical_cols = ['gender', 'chestpain', 'fastingbloodsugar', 'restingrelectro', 
                        'exerciseangia', 'slope', 'noofmajorvessels', 'target']
    
    print("\nNumerical Variables Summary:")
    print(df[numerical_cols].describe())
    
    print("\n\nCategorical Variables Summary:")
    for col in categorical_cols:
        if col in df.columns:
            print(f"\n{col.upper()}:")
            print(df[col].value_counts())
            print(f"Percentage: {df[col].value_counts(normalize=True) * 100}")

def inferential_statistics(df):
    """Perform inferential statistics"""
    print("=" * 80)
    print("INFERENTIAL STATISTICS")
    print("=" * 80)
    
    numerical_cols = ['age', 'restingBP', 'serumcholestrol', 'maxheartrate', 'oldpeak']
    disease_0 = df[df['target'] == 0]
    disease_1 = df[df['target'] == 1]
    
    print("\nT-Test: Comparing means between disease and no-disease groups")
    for col in numerical_cols:
        if col in df.columns:
            group_0 = disease_0[col].dropna()
            group_1 = disease_1[col].dropna()
            
            if len(group_0) > 0 and len(group_1) > 0:
                statistic, p_value = ttest_ind(group_0, group_1)
                print(f"\n{col.upper()}:")
                print(f"  t-statistic: {statistic:.4f}")
                print(f"  p-value: {p_value:.4f}")
                print(f"  Significant: {'Yes' if p_value < 0.05 else 'No'}")

def exploratory_analysis(df):
    """Perform exploratory data analysis"""
    print("=" * 80)
    print("EXPLORATORY DATA ANALYSIS")
    print("=" * 80)
    
    # Correlation matrix
    numerical_cols = ['age', 'restingBP', 'serumcholestrol', 'maxheartrate', 'oldpeak', 'target']
    correlation_matrix = df[numerical_cols].corr()
    
    plt.figure(figsize=(10, 8))
    sns.heatmap(correlation_matrix, annot=True, fmt='.2f', cmap='coolwarm', center=0)
    plt.title('Correlation Matrix')
    plt.tight_layout()
    plt.savefig('../../results/correlation_matrix.png')
    plt.close()
    
    print("\nCorrelation with Target:")
    print(correlation_matrix['target'].sort_values(ascending=False))

def main():
    """Main function"""
    df = load_data()
    descriptive_statistics(df)
    inferential_statistics(df)
    exploratory_analysis(df)
    print("\nAnalysis complete!")

if __name__ == "__main__":
    main()

