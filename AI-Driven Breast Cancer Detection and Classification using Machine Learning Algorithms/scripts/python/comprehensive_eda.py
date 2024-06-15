"""
Comprehensive Exploratory Data Analysis (EDA)
Breast Cancer Diagnosis Dataset
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import os
import warnings
warnings.filterwarnings('ignore')

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)

def load_data():
    """Load the breast cancer dataset"""
    df = pd.read_csv('../../data/breast_cancer.csv')
    return df

def data_overview(df):
    """Comprehensive data overview"""
    print("=" * 80)
    print("COMPREHENSIVE EXPLORATORY DATA ANALYSIS")
    print("=" * 80)
    
    print("\n1. DATA OVERVIEW")
    print("-" * 80)
    print(f"Dataset shape: {df.shape}")
    print(f"Number of rows: {len(df)}")
    print(f"Number of columns: {len(df.columns)}")
    print(f"\nColumn names:\n{df.columns.tolist()}")
    
    print("\n2. DATA TYPES")
    print("-" * 80)
    print(df.dtypes)
    
    print("\n3. MISSING VALUES")
    print("-" * 80)
    missing = df.isnull().sum()
    missing_pct = (missing / len(df)) * 100
    missing_df = pd.DataFrame({
        'Missing Count': missing,
        'Missing Percentage': missing_pct
    })
    missing_df = missing_df[missing_df['Missing Count'] > 0]
    if len(missing_df) > 0:
        print(missing_df)
    else:
        print("No missing values found!")
    
    print("\n4. DUPLICATE ROWS")
    print("-" * 80)
    duplicates = df.duplicated().sum()
    print(f"Number of duplicate rows: {duplicates}")
    
    print("\n5. BASIC STATISTICS")
    print("-" * 80)
    numerical_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    numerical_cols = [col for col in numerical_cols if col != 'id']
    print(df[numerical_cols].describe())
    
    return numerical_cols

def target_variable_analysis(df):
    """Analyze the target variable (diagnosis)"""
    print("\n6. TARGET VARIABLE ANALYSIS")
    print("-" * 80)
    
    # Count and proportion
    diagnosis_counts = df['diagnosis'].value_counts()
    diagnosis_props = df['diagnosis'].value_counts(normalize=True) * 100
    
    print("Diagnosis distribution:")
    for diagnosis in diagnosis_counts.index:
        print(f"  {diagnosis}: {diagnosis_counts[diagnosis]} ({diagnosis_props[diagnosis]:.2f}%)")
    
    # Visualization
    os.makedirs('../../results/eda', exist_ok=True)
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    diagnosis_counts.plot(kind='bar', ax=axes[0], color=['#3498db', '#e74c3c'])
    axes[0].set_title('Diagnosis Count Distribution', fontsize=14, fontweight='bold')
    axes[0].set_xlabel('Diagnosis')
    axes[0].set_ylabel('Count')
    axes[0].tick_params(axis='x', rotation=0)
    
    diagnosis_props.plot(kind='pie', ax=axes[1], autopct='%1.1f%%', 
                        colors=['#3498db', '#e74c3c'], startangle=90)
    axes[1].set_title('Diagnosis Proportion', fontsize=14, fontweight='bold')
    axes[1].set_ylabel('')
    
    plt.tight_layout()
    plt.savefig('../../results/eda/target_distribution.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    return diagnosis_counts, diagnosis_props

def feature_analysis(df, numerical_cols):
    """Comprehensive feature analysis"""
    print("\n7. FEATURE ANALYSIS")
    print("-" * 80)
    
    # Separate features by type
    mean_features = [col for col in numerical_cols if '_mean' in col]
    se_features = [col for col in numerical_cols if '_se' in col]
    worst_features = [col for col in numerical_cols if '_worst' in col]
    
    print(f"Mean features: {len(mean_features)}")
    print(f"Standard error features: {len(se_features)}")
    print(f"Worst features: {len(worst_features)}")
    
    # Statistical summary by diagnosis
    print("\n8. STATISTICAL SUMMARY BY DIAGNOSIS")
    print("-" * 80)
    
    malignant = df[df['diagnosis'] == 'M']
    benign = df[df['diagnosis'] == 'B']
    
    key_features = ['radius_mean', 'texture_mean', 'perimeter_mean', 
                   'area_mean', 'smoothness_mean', 'compactness_mean']
    
    summary_by_diagnosis = df.groupby('diagnosis')[key_features].agg([
        'mean', 'std', 'median', 'min', 'max'
    ])
    print(summary_by_diagnosis)
    
    # Distribution plots
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    axes = axes.ravel()
    
    for idx, feature in enumerate(key_features):
        for diagnosis in ['M', 'B']:
            subset = df[df['diagnosis'] == diagnosis][feature]
            axes[idx].hist(subset, alpha=0.6, label=diagnosis, bins=30, edgecolor='black')
        
        axes[idx].set_title(f'Distribution of {feature}', fontweight='bold')
        axes[idx].set_xlabel(feature)
        axes[idx].set_ylabel('Frequency')
        axes[idx].legend()
        axes[idx].grid(True, alpha=0.3)
    
    plt.suptitle('Feature Distributions by Diagnosis', 
                 fontsize=16, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig('../../results/eda/feature_distributions.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # Box plots
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    axes = axes.ravel()
    
    for idx, feature in enumerate(key_features):
        df.boxplot(column=feature, by='diagnosis', ax=axes[idx])
        axes[idx].set_title(f'{feature} by Diagnosis', fontweight='bold')
        axes[idx].set_xlabel('Diagnosis')
        axes[idx].set_ylabel(feature)
    
    plt.suptitle('Box Plots: Features by Diagnosis', 
                 fontsize=16, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig('../../results/eda/boxplots_by_diagnosis.png', 
                dpi=300, bbox_inches='tight')
    plt.close()
    
    return mean_features, se_features, worst_features

def correlation_analysis(df, numerical_cols):
    """Comprehensive correlation analysis"""
    print("\n9. CORRELATION ANALYSIS")
    print("-" * 80)
    
    # Full correlation matrix
    correlation_matrix = df[numerical_cols].corr()
    
    # Visualization
    plt.figure(figsize=(20, 16))
    sns.heatmap(correlation_matrix, annot=False, cmap='coolwarm', center=0, 
                square=True, linewidths=0.5, cbar_kws={"shrink": 0.8})
    plt.title('Correlation Matrix of All Numerical Features', 
              fontsize=16, fontweight='bold', pad=20)
    plt.tight_layout()
    plt.savefig('../../results/eda/correlation_matrix_full.png', 
                dpi=300, bbox_inches='tight')
    plt.close()
    
    # Highly correlated pairs
    high_corr_pairs = []
    for i in range(len(correlation_matrix.columns)):
        for j in range(i+1, len(correlation_matrix.columns)):
            corr_val = correlation_matrix.iloc[i, j]
            if abs(corr_val) > 0.9:
                high_corr_pairs.append((
                    correlation_matrix.columns[i],
                    correlation_matrix.columns[j],
                    corr_val
                ))
    
    print(f"Number of highly correlated pairs (|r| > 0.9): {len(high_corr_pairs)}")
    if len(high_corr_pairs) > 0:
        print("\nTop 10 highly correlated pairs:")
        high_corr_pairs.sort(key=lambda x: abs(x[2]), reverse=True)
        for pair in high_corr_pairs[:10]:
            print(f"  {pair[0]} <-> {pair[1]}: {pair[2]:.4f}")
    
    # Correlation with target (diagnosis encoded as 0/1)
    df_encoded = df.copy()
    df_encoded['diagnosis_encoded'] = df_encoded['diagnosis'].map({'M': 1, 'B': 0})
    
    target_corr = df_encoded[numerical_cols + ['diagnosis_encoded']].corr()['diagnosis_encoded']
    target_corr = target_corr.drop('diagnosis_encoded').sort_values(ascending=False, key=abs)
    
    print("\nTop 10 features most correlated with diagnosis:")
    print(target_corr.head(10))
    
    # Visualization
    plt.figure(figsize=(12, 8))
    target_corr.head(15).plot(kind='barh', color='steelblue')
    plt.title('Top 15 Features Most Correlated with Diagnosis', 
              fontsize=14, fontweight='bold')
    plt.xlabel('Correlation Coefficient')
    plt.tight_layout()
    plt.savefig('../../results/eda/target_correlation.png', 
                dpi=300, bbox_inches='tight')
    plt.close()
    
    return correlation_matrix, high_corr_pairs

def outlier_analysis(df, numerical_cols):
    """Comprehensive outlier analysis"""
    print("\n10. OUTLIER ANALYSIS")
    print("-" * 80)
    
    # IQR method
    outlier_counts_iqr = {}
    key_features = ['radius_mean', 'texture_mean', 'perimeter_mean', 
                   'area_mean', 'smoothness_mean', 'compactness_mean']
    
    for feature in key_features:
        Q1 = df[feature].quantile(0.25)
        Q3 = df[feature].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        outliers = df[(df[feature] < lower_bound) | (df[feature] > upper_bound)]
        outlier_counts_iqr[feature] = len(outliers)
        
        if len(outliers) > 0:
            print(f"{feature}: {len(outliers)} outliers ({len(outliers)/len(df)*100:.2f}%)")
    
    # Z-score method
    outlier_counts_zscore = {}
    for feature in key_features:
        z_scores = np.abs(stats.zscore(df[feature]))
        outliers = df[z_scores > 3]
        outlier_counts_zscore[feature] = len(outliers)
        
        if len(outliers) > 0:
            print(f"{feature} (Z-score): {len(outliers)} outliers ({len(outliers)/len(df)*100:.2f}%)")
    
    return outlier_counts_iqr, outlier_counts_zscore

def feature_engineering_insights(df, numerical_cols):
    """Provide insights for feature engineering"""
    print("\n11. FEATURE ENGINEERING INSIGHTS")
    print("-" * 80)
    
    # Check for constant or near-constant features
    constant_features = []
    for col in numerical_cols:
        if df[col].nunique() == 1:
            constant_features.append(col)
        elif df[col].std() < 0.01:
            constant_features.append(col)
    
    if constant_features:
        print(f"Constant or near-constant features: {constant_features}")
    else:
        print("No constant features found")
    
    # Feature ranges and scales
    print("\nFeature ranges:")
    ranges = pd.DataFrame({
        'Min': df[numerical_cols].min(),
        'Max': df[numerical_cols].max(),
        'Range': df[numerical_cols].max() - df[numerical_cols].min(),
        'Std': df[numerical_cols].std()
    })
    print(ranges.head(10))
    
    return constant_features

def summary_insights(df, numerical_cols):
    """Generate summary insights"""
    print("\n12. SUMMARY INSIGHTS")
    print("-" * 80)
    
    insights = []
    
    # Dataset balance
    diagnosis_counts = df['diagnosis'].value_counts()
    balance_ratio = min(diagnosis_counts) / max(diagnosis_counts)
    insights.append(f"Dataset balance ratio: {balance_ratio:.3f} "
                   f"({'Balanced' if balance_ratio > 0.8 else 'Imbalanced'})")
    
    # Feature count
    insights.append(f"Total features: {len(numerical_cols)}")
    
    # Missing values
    missing_count = df.isnull().sum().sum()
    insights.append(f"Missing values: {missing_count} ({'None' if missing_count == 0 else 'Present'})")
    
    # Correlation insights
    correlation_matrix = df[numerical_cols].corr()
    high_corr_count = sum([1 for i in range(len(correlation_matrix.columns))
                          for j in range(i+1, len(correlation_matrix.columns))
                          if abs(correlation_matrix.iloc[i, j]) > 0.9])
    insights.append(f"Highly correlated feature pairs (|r| > 0.9): {high_corr_count}")
    
    for insight in insights:
        print(f"  - {insight}")
    
    return insights

def main():
    """Main function to run comprehensive EDA"""
    # Load data
    df = load_data()
    
    # Data overview
    numerical_cols = data_overview(df)
    
    # Target variable analysis
    diagnosis_counts, diagnosis_props = target_variable_analysis(df)
    
    # Feature analysis
    mean_features, se_features, worst_features = feature_analysis(df, numerical_cols)
    
    # Correlation analysis
    correlation_matrix, high_corr_pairs = correlation_analysis(df, numerical_cols)
    
    # Outlier analysis
    outlier_counts_iqr, outlier_counts_zscore = outlier_analysis(df, numerical_cols)
    
    # Feature engineering insights
    constant_features = feature_engineering_insights(df, numerical_cols)
    
    # Summary insights
    insights = summary_insights(df, numerical_cols)
    
    print("\n" + "=" * 80)
    print("EDA COMPLETE - All visualizations saved to results/eda/")
    print("=" * 80)

if __name__ == "__main__":
    main()

