"""
Univariate Analysis Module
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from data_loader import load_data, clean_data

def univariate_analysis(df_clean, variable='Incidence_Rate'):
    """
    Perform univariate analysis on a single variable
    
    Parameters:
    -----------
    df_clean : DataFrame
        Cleaned dataset
    variable : str
        Variable to analyze
    """
    data = df_clean[variable].dropna()
    
    print(f"=== UNIVARIATE ANALYSIS: {variable} ===\n")
    
    # Descriptive statistics
    print("1. Descriptive Statistics:")
    print(data.describe())
    
    # Distribution characteristics
    print(f"\n2. Distribution Characteristics:")
    print(f"   Skewness: {data.skew():.4f}")
    print(f"   Kurtosis: {data.kurtosis():.4f}")
    print(f"   Coefficient of Variation: {(data.std()/data.mean()*100):.2f}%")
    
    # Visualizations
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    
    # Histogram
    axes[0, 0].hist(data, bins=50, edgecolor='black', alpha=0.7)
    axes[0, 0].set_title(f'Histogram of {variable}')
    axes[0, 0].set_xlabel(variable)
    axes[0, 0].set_ylabel('Frequency')
    axes[0, 0].axvline(data.mean(), color='r', linestyle='--', label='Mean')
    axes[0, 0].axvline(data.median(), color='g', linestyle='--', label='Median')
    axes[0, 0].legend()
    
    # Box plot
    axes[0, 1].boxplot(data)
    axes[0, 1].set_title(f'Box Plot of {variable}')
    axes[0, 1].set_ylabel(variable)
    
    # Density plot
    data.plot(kind='density', ax=axes[0, 2])
    axes[0, 2].set_title(f'Density Plot of {variable}')
    axes[0, 2].set_xlabel(variable)
    
    # Q-Q plot
    stats.probplot(data, dist="norm", plot=axes[1, 0])
    axes[1, 0].set_title(f'Q-Q Plot of {variable}')
    
    # Violin plot
    sns.violinplot(y=data, ax=axes[1, 1])
    axes[1, 1].set_title(f'Violin Plot of {variable}')
    
    # Cumulative distribution
    sorted_data = np.sort(data)
    y = np.arange(1, len(sorted_data) + 1) / len(sorted_data)
    axes[1, 2].plot(sorted_data, y)
    axes[1, 2].set_title(f'Cumulative Distribution of {variable}')
    axes[1, 2].set_xlabel(variable)
    axes[1, 2].set_ylabel('Cumulative Probability')
    
    plt.tight_layout()
    plt.savefig(f'univariate_{variable}.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    # Outlier detection
    Q1 = data.quantile(0.25)
    Q3 = data.quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    
    outliers = data[(data < lower_bound) | (data > upper_bound)]
    print(f"\n3. Outlier Detection (IQR Method):")
    print(f"   Lower bound: {lower_bound:.2f}")
    print(f"   Upper bound: {upper_bound:.2f}")
    print(f"   Number of outliers: {len(outliers)}")
    print(f"   Percentage: {len(outliers)/len(data)*100:.2f}%")
    
    return {
        'data': data,
        'outliers': outliers,
        'stats': data.describe()
    }

if __name__ == "__main__":
    df = load_data()
    df_clean = clean_data(df)
    result = univariate_analysis(df_clean, 'Incidence_Rate')

