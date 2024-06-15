"""
Comprehensive Exploratory Data Analysis
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

def data_overview(df):
    """Comprehensive data overview"""
    print("=" * 60)
    print("DATA OVERVIEW")
    print("=" * 60)
    
    print(f"\nDataset Shape: {df.shape}")
    print(f"Number of features: {len(df.columns)}")
    print(f"Number of records: {len(df):,}")
    
    print("\n" + "-" * 60)
    print("DATA TYPES")
    print("-" * 60)
    print(df.dtypes)
    
    print("\n" + "-" * 60)
    print("MISSING VALUES")
    print("-" * 60)
    missing = df.isnull().sum()
    missing_pct = (missing / len(df)) * 100
    missing_df = pd.DataFrame({
        'Missing Count': missing,
        'Missing Percentage': missing_pct
    })
    print(missing_df[missing_df['Missing Count'] > 0])
    
    print("\n" + "-" * 60)
    print("DUPLICATE ROWS")
    print("-" * 60)
    print(f"Number of duplicate rows: {df.duplicated().sum()}")
    
    return df

def descriptive_statistics(df):
    """Comprehensive descriptive statistics"""
    print("=" * 60)
    print("DESCRIPTIVE STATISTICS")
    print("=" * 60)
    
    numerical_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    
    print("\n" + "-" * 60)
    print("NUMERICAL VARIABLES SUMMARY")
    print("-" * 60)
    desc_stats = df[numerical_cols].describe()
    print(desc_stats)
    
    print("\n" + "-" * 60)
    print("ADDITIONAL STATISTICS")
    print("-" * 60)
    additional_stats = pd.DataFrame({
        'Mean': df[numerical_cols].mean(),
        'Median': df[numerical_cols].median(),
        'Std Dev': df[numerical_cols].std(),
        'Variance': df[numerical_cols].var(),
        'Skewness': df[numerical_cols].skew(),
        'Kurtosis': df[numerical_cols].kurtosis(),
        'Min': df[numerical_cols].min(),
        'Max': df[numerical_cols].max(),
        'Range': df[numerical_cols].max() - df[numerical_cols].min(),
        'Q1': df[numerical_cols].quantile(0.25),
        'Q3': df[numerical_cols].quantile(0.75),
        'IQR': df[numerical_cols].quantile(0.75) - df[numerical_cols].quantile(0.25)
    })
    print(additional_stats.T)
    
    return desc_stats, additional_stats

def target_variable_analysis(df, output_dir='../../results/figures/'):
    """Analyze target variable"""
    print("=" * 60)
    print("TARGET VARIABLE ANALYSIS")
    print("=" * 60)
    
    target_dist = df['Diabetes_binary'].value_counts()
    target_prop = target_dist / len(df)
    
    print("\nDistribution:")
    print(target_dist)
    print("\nProportions:")
    print(target_prop)
    
    # Visualization
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    
    axes[0].bar(target_dist.index, target_dist.values, color=['skyblue', 'salmon'])
    axes[0].set_title('Diabetes Distribution (Count)', fontsize=12, fontweight='bold')
    axes[0].set_xlabel('Diabetes (0=No, 1=Yes)')
    axes[0].set_ylabel('Frequency')
    axes[0].set_xticks([0, 1])
    
    axes[1].bar(target_prop.index, target_prop.values, color=['skyblue', 'salmon'])
    axes[1].set_title('Diabetes Distribution (Proportion)', fontsize=12, fontweight='bold')
    axes[1].set_xlabel('Diabetes (0=No, 1=Yes)')
    axes[1].set_ylabel('Proportion')
    axes[1].set_xticks([0, 1])
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}target_distribution.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    return target_dist, target_prop

def feature_distributions(df, output_dir='../../results/figures/'):
    """Visualize feature distributions"""
    print("=" * 60)
    print("FEATURE DISTRIBUTIONS")
    print("=" * 60)
    
    key_vars = ['BMI', 'Age', 'GenHlth', 'MentHlth', 'PhysHlth']
    
    fig, axes = plt.subplots(2, 3, figsize=(18, 10))
    axes = axes.ravel()
    
    for i, var in enumerate(key_vars):
        if var in df.columns:
            axes[i].hist(df[var].dropna(), bins=30, color='steelblue', alpha=0.7, edgecolor='black')
            axes[i].set_title(f'Distribution of {var}', fontsize=12, fontweight='bold')
            axes[i].set_xlabel(var)
            axes[i].set_ylabel('Frequency')
            axes[i].axvline(df[var].mean(), color='red', linestyle='--', 
                           label=f'Mean: {df[var].mean():.2f}')
            axes[i].axvline(df[var].median(), color='green', linestyle='--', 
                           label=f'Median: {df[var].median():.2f}')
            axes[i].legend()
            axes[i].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}feature_distributions.png', dpi=300, bbox_inches='tight')
    plt.close()

def correlation_analysis(df, output_dir='../../results/figures/'):
    """Comprehensive correlation analysis"""
    print("=" * 60)
    print("CORRELATION ANALYSIS")
    print("=" * 60)
    
    numerical_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    correlation_matrix = df[numerical_cols].corr()
    
    # Correlation with target
    diabetes_corr = correlation_matrix['Diabetes_binary'].sort_values(ascending=False)
    print("\nCorrelation with Diabetes_binary:")
    print(diabetes_corr)
    
    # Visualization
    plt.figure(figsize=(14, 10))
    sns.heatmap(correlation_matrix, annot=True, fmt='.2f', cmap='coolwarm', center=0,
                square=True, linewidths=0.5, cbar_kws={"shrink": 0.8})
    plt.title('Correlation Matrix Heatmap', fontsize=16, fontweight='bold', pad=20)
    plt.tight_layout()
    plt.savefig(f'{output_dir}correlation_matrix.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # Correlation with target variable
    plt.figure(figsize=(10, 8))
    diabetes_corr.drop('Diabetes_binary').sort_values().plot(kind='barh', color='steelblue')
    plt.title('Correlation with Diabetes_binary', fontsize=14, fontweight='bold')
    plt.xlabel('Correlation Coefficient')
    plt.axvline(x=0, color='red', linestyle='--', linewidth=1)
    plt.tight_layout()
    plt.savefig(f'{output_dir}diabetes_correlation.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    return correlation_matrix, diabetes_corr

def categorical_analysis(df, output_dir='../../results/figures/'):
    """Analyze categorical variables"""
    print("=" * 60)
    print("CATEGORICAL VARIABLE ANALYSIS")
    print("=" * 60)
    
    categorical_vars = ['HighBP', 'HighChol', 'Smoker', 'PhysActivity', 'Sex', 'HeartDiseaseorAttack']
    
    fig, axes = plt.subplots(2, 3, figsize=(18, 10))
    axes = axes.ravel()
    
    for i, var in enumerate(categorical_vars):
        if var in df.columns:
            crosstab = pd.crosstab(df[var], df['Diabetes_binary'], normalize='index') * 100
            crosstab.plot(kind='bar', ax=axes[i], color=['skyblue', 'salmon'], width=0.8)
            axes[i].set_title(f'Diabetes Prevalence by {var}', fontsize=12, fontweight='bold')
            axes[i].set_xlabel(var)
            axes[i].set_ylabel('Percentage (%)')
            axes[i].legend(['No Diabetes', 'Diabetes'])
            axes[i].tick_params(axis='x', rotation=0)
            axes[i].grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}categorical_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()

def outlier_analysis(df):
    """Detect and analyze outliers"""
    print("=" * 60)
    print("OUTLIER ANALYSIS")
    print("=" * 60)
    
    numerical_cols = ['BMI', 'GenHlth', 'MentHlth', 'PhysHlth', 'Age']
    
    outlier_summary = []
    for col in numerical_cols:
        if col in df.columns:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)]
            outlier_summary.append({
                'Variable': col,
                'Lower Bound': lower_bound,
                'Upper Bound': upper_bound,
                'Number of Outliers': len(outliers),
                'Percentage': (len(outliers) / len(df)) * 100
            })
    
    outlier_df = pd.DataFrame(outlier_summary)
    print(outlier_df.to_string(index=False))
    
    return outlier_df

def main():
    """Main function"""
    # Load data
    df = load_data()
    
    # Perform comprehensive EDA
    data_overview(df)
    descriptive_statistics(df)
    target_variable_analysis(df)
    feature_distributions(df)
    correlation_analysis(df)
    categorical_analysis(df)
    outlier_analysis(df)
    
    print("\n" + "=" * 60)
    print("COMPREHENSIVE EDA COMPLETE")
    print("=" * 60)

if __name__ == "__main__":
    main()

