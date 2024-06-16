"""
Bivariate Analysis Module
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

def bivariate_analysis(df_clean, var1='Incidence_Rate', var2='Annual_Count'):
    """
    Perform bivariate analysis between two variables
    
    Parameters:
    -----------
    df_clean : DataFrame
        Cleaned dataset
    var1 : str
        First variable
    var2 : str
        Second variable
    """
    print(f"=== BIVARIATE ANALYSIS: {var1} vs {var2} ===\n")
    
    # Remove missing values
    data = df_clean[[var1, var2]].dropna()
    
    # Correlation analysis
    correlation = data[var1].corr(data[var2])
    print(f"1. Correlation Coefficient: {correlation:.4f}")
    
    # Pearson correlation test
    pearson_r, pearson_p = stats.pearsonr(data[var1], data[var2])
    print(f"   Pearson correlation: r={pearson_r:.4f}, p-value={pearson_p:.4f}")
    
    # Spearman correlation
    spearman_r, spearman_p = stats.spearmanr(data[var1], data[var2])
    print(f"   Spearman correlation: r={spearman_r:.4f}, p-value={spearman_p:.4f}")
    
    # Visualizations
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    
    # Scatter plot
    axes[0, 0].scatter(data[var1], data[var2], alpha=0.5)
    axes[0, 0].set_xlabel(var1)
    axes[0, 0].set_ylabel(var2)
    axes[0, 0].set_title(f'Scatter Plot: {var1} vs {var2}')
    
    # Add regression line
    z = np.polyfit(data[var1], data[var2], 1)
    p = np.poly1d(z)
    axes[0, 0].plot(data[var1], p(data[var1]), "r--", alpha=0.8, label=f'Trend line')
    axes[0, 0].legend()
    
    # Hexbin plot
    axes[0, 1].hexbin(data[var1], data[var2], gridsize=20, cmap='Blues')
    axes[0, 1].set_xlabel(var1)
    axes[0, 1].set_ylabel(var2)
    axes[0, 1].set_title(f'Hexbin Plot: {var1} vs {var2}')
    
    # 2D histogram
    axes[1, 0].hist2d(data[var1], data[var2], bins=30, cmap='Blues')
    axes[1, 0].set_xlabel(var1)
    axes[1, 0].set_ylabel(var2)
    axes[1, 0].set_title(f'2D Histogram: {var1} vs {var2}')
    
    # Joint plot (simplified)
    sns.scatterplot(data=data, x=var1, y=var2, ax=axes[1, 1])
    axes[1, 1].set_title(f'Scatter with Density: {var1} vs {var2}')
    
    plt.tight_layout()
    plt.savefig(f'bivariate_{var1}_vs_{var2}.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    return {
        'correlation': correlation,
        'pearson_r': pearson_r,
        'pearson_p': pearson_p,
        'spearman_r': spearman_r,
        'spearman_p': spearman_p
    }

def categorical_bivariate_analysis(df_clean, cat_var='Trend', num_var='Incidence_Rate'):
    """
    Analyze relationship between categorical and numerical variables
    
    Parameters:
    -----------
    df_clean : DataFrame
        Cleaned dataset
    cat_var : str
        Categorical variable
    num_var : str
        Numerical variable
    """
    print(f"=== BIVARIATE ANALYSIS: {cat_var} vs {num_var} ===\n")
    
    if cat_var not in df_clean.columns:
        print(f"Variable {cat_var} not found in dataset")
        return
    
    data = df_clean[[cat_var, num_var]].dropna()
    
    # Group statistics
    group_stats = data.groupby(cat_var)[num_var].agg(['count', 'mean', 'median', 'std'])
    print("1. Group Statistics:")
    print(group_stats)
    
    # Visualizations
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    
    # Box plot
    categories = data[cat_var].unique()
    box_data = [data[data[cat_var] == cat][num_var].values for cat in categories if pd.notna(cat)]
    axes[0, 0].boxplot(box_data, labels=[cat for cat in categories if pd.notna(cat)])
    axes[0, 0].set_xlabel(cat_var)
    axes[0, 0].set_ylabel(num_var)
    axes[0, 0].set_title(f'Box Plot: {num_var} by {cat_var}')
    axes[0, 0].tick_params(axis='x', rotation=45)
    
    # Violin plot
    sns.violinplot(data=data, x=cat_var, y=num_var, ax=axes[0, 1])
    axes[0, 1].set_title(f'Violin Plot: {num_var} by {cat_var}')
    axes[0, 1].tick_params(axis='x', rotation=45)
    
    # Bar plot of means
    means = data.groupby(cat_var)[num_var].mean()
    axes[1, 0].bar(means.index, means.values)
    axes[1, 0].set_xlabel(cat_var)
    axes[1, 0].set_ylabel(f'Mean {num_var}')
    axes[1, 0].set_title(f'Mean {num_var} by {cat_var}')
    axes[1, 0].tick_params(axis='x', rotation=45)
    
    # Strip plot
    sns.stripplot(data=data, x=cat_var, y=num_var, ax=axes[1, 1], alpha=0.5)
    axes[1, 1].set_title(f'Strip Plot: {num_var} by {cat_var}')
    axes[1, 1].tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    plt.savefig(f'bivariate_{cat_var}_vs_{num_var}.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    # ANOVA test
    groups = [data[data[cat_var] == cat][num_var].values 
              for cat in categories if pd.notna(cat) and len(data[data[cat_var] == cat]) > 0]
    if len(groups) > 2:
        f_stat, p_value = stats.f_oneway(*groups)
        print(f"\n2. ANOVA Test:")
        print(f"   F-statistic: {f_stat:.4f}")
        print(f"   p-value: {p_value:.4f}")
        print(f"   Result: {'Significant difference' if p_value < 0.05 else 'No significant difference'}")
    
    return group_stats

if __name__ == "__main__":
    df = load_data()
    df_clean = clean_data(df)
    
    # Numerical vs Numerical
    result1 = bivariate_analysis(df_clean, 'Incidence_Rate', 'Annual_Count')
    
    # Categorical vs Numerical
    if 'Trend' in df_clean.columns:
        result2 = categorical_bivariate_analysis(df_clean, 'Trend', 'Incidence_Rate')

