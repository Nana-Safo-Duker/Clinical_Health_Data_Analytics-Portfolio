"""
Univariate, Bivariate, and Multivariate Analysis
Diabetes Binary Health Indicators - BRFSS 2021
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

def load_data():
    """Load the dataset"""
    df = pd.read_csv('../../data/diabetes_binary_health_indicators_BRFSS2021.csv')
    return df

def univariate_analysis(df, numerical_cols, output_dir='../../results/figures/'):
    """Perform univariate analysis"""
    print("=" * 60)
    print("UNIVARIATE ANALYSIS")
    print("=" * 60)
    
    # Statistical summary
    univariate_summary = []
    for col in numerical_cols:
        if col in df.columns:
            data = df[col].dropna()
            univariate_summary.append({
                'Variable': col,
                'Mean': data.mean(),
                'Median': data.median(),
                'Std Dev': data.std(),
                'Skewness': data.skew(),
                'Kurtosis': data.kurtosis(),
                'Min': data.min(),
                'Max': data.max(),
                'IQR': data.quantile(0.75) - data.quantile(0.25)
            })
    
    summary_df = pd.DataFrame(univariate_summary)
    print(summary_df.to_string(index=False))
    
    # Visualizations
    fig, axes = plt.subplots(3, 3, figsize=(18, 15))
    axes = axes.ravel()
    
    for i, col in enumerate(numerical_cols[:9]):
        if col in df.columns:
            axes[i].hist(df[col].dropna(), bins=30, density=True, alpha=0.7, 
                        color='steelblue', edgecolor='black')
            axes[i].set_title(f'{col} - Distribution', fontsize=12, fontweight='bold')
            axes[i].set_xlabel(col)
            axes[i].set_ylabel('Density')
            axes[i].axvline(df[col].mean(), color='green', linestyle='--', 
                           linewidth=2, label=f'Mean: {df[col].mean():.2f}')
            axes[i].legend()
            axes[i].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}univariate_numerical.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    return summary_df

def bivariate_analysis(df, numerical_cols, output_dir='../../results/figures/'):
    """Perform bivariate analysis"""
    print("=" * 60)
    print("BIVARIATE ANALYSIS")
    print("=" * 60)
    
    # Correlation analysis
    correlation_results = []
    for col in numerical_cols:
        if col in df.columns and col != 'Diabetes_binary':
            pearson_corr, pearson_p = stats.pearsonr(
                df[col].dropna(), 
                df.loc[df[col].notna(), 'Diabetes_binary']
            )
            correlation_results.append({
                'Variable': col,
                'Pearson r': pearson_corr,
                'Pearson p-value': pearson_p,
                'Significant': 'Yes' if pearson_p < 0.05 else 'No'
            })
    
    corr_df = pd.DataFrame(correlation_results)
    print(corr_df.to_string(index=False))
    
    # Box plots
    fig, axes = plt.subplots(3, 3, figsize=(18, 15))
    axes = axes.ravel()
    
    for i, col in enumerate(numerical_cols[:9]):
        if col in df.columns and col != 'Diabetes_binary':
            df.boxplot(column=col, by='Diabetes_binary', ax=axes[i], grid=False)
            axes[i].set_title(f'{col} by Diabetes Status', fontsize=12, fontweight='bold')
            axes[i].set_xlabel('Diabetes (0=No, 1=Yes)')
            axes[i].set_ylabel(col)
            axes[i].get_figure().suptitle('')
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}bivariate_numerical_vs_target.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    return corr_df

def multivariate_analysis(df, numerical_cols, output_dir='../../results/figures/'):
    """Perform multivariate analysis"""
    print("=" * 60)
    print("MULTIVARIATE ANALYSIS")
    print("=" * 60)
    
    # Correlation heatmap
    correlation_matrix = df[numerical_cols].corr()
    
    plt.figure(figsize=(16, 12))
    sns.heatmap(correlation_matrix, annot=True, fmt='.2f', cmap='coolwarm', center=0,
                square=True, linewidths=0.5, cbar_kws={"shrink": 0.8})
    plt.title('Multivariate Correlation Heatmap', fontsize=16, fontweight='bold', pad=20)
    plt.tight_layout()
    plt.savefig(f'{output_dir}multivariate_correlation_heatmap.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # Multivariate group analysis
    df['BMI_Category'] = pd.cut(df['BMI'], bins=[0, 18.5, 25, 30, 100], 
                                labels=['Underweight', 'Normal', 'Overweight', 'Obese'])
    multi_group = df.groupby(['HighBP', 'HighChol'])['Diabetes_binary'].agg(['mean', 'count']).reset_index()
    multi_group['Diabetes_Rate'] = multi_group['mean'] * 100
    print("\nDiabetes Prevalence by HighBP and HighChol:")
    print(multi_group)
    
    # Heatmap for multivariate categorical analysis
    pivot_table = df.groupby(['HighBP', 'HighChol'])['Diabetes_binary'].mean().unstack() * 100
    
    plt.figure(figsize=(10, 6))
    sns.heatmap(pivot_table, annot=True, fmt='.2f', cmap='YlOrRd', 
                cbar_kws={'label': 'Diabetes Prevalence (%)'})
    plt.title('Diabetes Prevalence by HighBP and HighChol', fontsize=14, fontweight='bold')
    plt.xlabel('HighChol (0=No, 1=Yes)')
    plt.ylabel('HighBP (0=No, 1=Yes)')
    plt.tight_layout()
    plt.savefig(f'{output_dir}multivariate_heatmap_bp_chol.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    return correlation_matrix, multi_group

def main():
    """Main function"""
    # Load data
    df = load_data()
    print(f"Dataset shape: {df.shape}")
    
    # Define numerical columns
    numerical_cols = ['BMI', 'GenHlth', 'MentHlth', 'PhysHlth', 'Age', 'Education', 'Income', 
                     'Diabetes_binary', 'HighBP', 'HighChol']
    
    # Perform analyses
    univariate_summary = univariate_analysis(df, numerical_cols)
    bivariate_corr = bivariate_analysis(df, numerical_cols)
    multivariate_corr, multi_group = multivariate_analysis(df, numerical_cols)
    
    print("\n" + "=" * 60)
    print("ANALYSIS COMPLETE")
    print("=" * 60)

if __name__ == "__main__":
    main()

