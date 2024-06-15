"""
Statistical Analysis: Descriptive, Inferential, and Exploratory
Breast Cancer Diagnosis Dataset
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from scipy.stats import ttest_ind, mannwhitneyu, shapiro
import json
import os

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)

def load_data():
    """Load the breast cancer dataset"""
    import os
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Navigate to project root and then to data directory
    project_root = os.path.join(script_dir, '../..')
    data_path = os.path.join(project_root, 'data', 'breast_cancer.csv')
    df = pd.read_csv(data_path)
    return df

def descriptive_statistics(df):
    """Perform descriptive statistical analysis"""
    print("=== DESCRIPTIVE STATISTICS ===")
    print(f"Total samples: {len(df)}")
    print(f"Total features: {len(df.columns)}")
    print(f"Missing values: {df.isnull().sum().sum()}")
    print(f"Duplicate rows: {df.duplicated().sum()}")
    
    numerical_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    numerical_cols = [col for col in numerical_cols if col != 'id']
    
    desc_stats = df[numerical_cols].describe()
    print("\nDescriptive Statistics:")
    print(desc_stats)
    
    # Additional statistics
    additional_stats = pd.DataFrame({
        'Mean': df[numerical_cols].mean(),
        'Median': df[numerical_cols].median(),
        'Std': df[numerical_cols].std(),
        'Skewness': df[numerical_cols].skew(),
        'Kurtosis': df[numerical_cols].kurtosis(),
        'IQR': df[numerical_cols].quantile(0.75) - df[numerical_cols].quantile(0.25)
    })
    
    # Diagnosis distribution
    print("\n=== DIAGNOSIS DISTRIBUTION ===")
    diagnosis_counts = df['diagnosis'].value_counts()
    diagnosis_props = df['diagnosis'].value_counts(normalize=True) * 100
    print(diagnosis_counts)
    print(f"\nProportions:\n{diagnosis_props}")
    
    return desc_stats, additional_stats, numerical_cols

def inferential_statistics(df, numerical_cols):
    """Perform inferential statistical analysis"""
    malignant = df[df['diagnosis'] == 'M']
    benign = df[df['diagnosis'] == 'B']
    
    print("\n=== INFERENTIAL STATISTICS ===")
    print(f"Malignant samples: {len(malignant)}")
    print(f"Benign samples: {len(benign)}")
    
    # T-tests
    print("\n=== INDEPENDENT T-TESTS ===")
    ttest_results = {}
    key_features = numerical_cols[:15]
    
    for feature in key_features:
        t_stat, p_value = ttest_ind(malignant[feature], benign[feature])
        mean_m = malignant[feature].mean()
        mean_b = benign[feature].mean()
        
        ttest_results[feature] = {
            't-statistic': float(t_stat),
            'p-value': float(p_value),
            'mean_malignant': float(mean_m),
            'mean_benign': float(mean_b),
            'significant': p_value < 0.05
        }
        
        significance = "***" if p_value < 0.001 else "**" if p_value < 0.01 else "*" if p_value < 0.05 else ""
        print(f"{feature}: t={t_stat:.4f}, p={p_value:.4f} {significance}")
    
    # Effect sizes (Cohen's d)
    print("\n=== EFFECT SIZE (Cohen's d) ===")
    def cohens_d(group1, group2):
        n1, n2 = len(group1), len(group2)
        var1, var2 = group1.var(), group2.var()
        pooled_std = np.sqrt(((n1 - 1) * var1 + (n2 - 1) * var2) / (n1 + n2 - 2))
        return (group1.mean() - group2.mean()) / pooled_std
    
    effect_sizes = {}
    for feature in key_features:
        d = cohens_d(malignant[feature], benign[feature])
        effect_sizes[feature] = float(d)
        
        if abs(d) < 0.2:
            interpretation = "negligible"
        elif abs(d) < 0.5:
            interpretation = "small"
        elif abs(d) < 0.8:
            interpretation = "medium"
        else:
            interpretation = "large"
        
        print(f"{feature}: Cohen's d = {d:.4f} ({interpretation} effect)")
    
    return ttest_results, effect_sizes

def exploratory_analysis(df, numerical_cols):
    """Perform exploratory statistical analysis"""
    print("\n=== EXPLORATORY ANALYSIS ===")
    
    # Correlation analysis
    correlation_matrix = df[numerical_cols].corr()
    
    # Find highly correlated features
    high_corr_pairs = []
    for i in range(len(correlation_matrix.columns)):
        for j in range(i+1, len(correlation_matrix.columns)):
            corr_val = correlation_matrix.iloc[i, j]
            if abs(corr_val) > 0.9:
                high_corr_pairs.append((
                    correlation_matrix.columns[i],
                    correlation_matrix.columns[j],
                    float(corr_val)
                ))
    
    print(f"\nHighly correlated features (|r| > 0.9): {len(high_corr_pairs)} pairs")
    for pair in high_corr_pairs[:10]:  # Show first 10
        print(f"  {pair[0]} <-> {pair[1]}: {pair[2]:.4f}")
    
    # Outlier detection
    print("\n=== OUTLIER DETECTION (IQR Method) ===")
    outlier_counts = {}
    for feature in numerical_cols[:10]:
        Q1 = df[feature].quantile(0.25)
        Q3 = df[feature].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        outliers = df[(df[feature] < lower_bound) | (df[feature] > upper_bound)]
        outlier_counts[feature] = len(outliers)
        
        if len(outliers) > 0:
            print(f"{feature}: {len(outliers)} outliers ({len(outliers)/len(df)*100:.2f}%)")
    
    return correlation_matrix, outlier_counts

def create_visualizations(df, numerical_cols):
    """Create statistical visualizations"""
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.join(script_dir, '../..')
    results_dir = os.path.join(project_root, 'results')
    os.makedirs(results_dir, exist_ok=True)
    
    # Diagnosis distribution
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    diagnosis_counts = df['diagnosis'].value_counts()
    diagnosis_props = df['diagnosis'].value_counts(normalize=True) * 100
    
    diagnosis_counts.plot(kind='bar', ax=axes[0], color=['#3498db', '#e74c3c'])
    axes[0].set_title('Diagnosis Count', fontsize=14, fontweight='bold')
    axes[0].set_xlabel('Diagnosis')
    axes[0].set_ylabel('Count')
    axes[0].tick_params(axis='x', rotation=0)
    
    diagnosis_props.plot(kind='pie', ax=axes[1], autopct='%1.1f%%', colors=['#3498db', '#e74c3c'])
    axes[1].set_title('Diagnosis Proportion', fontsize=14, fontweight='bold')
    axes[1].set_ylabel('')
    
    plt.tight_layout()
    results_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../..', 'results')
    plt.savefig(os.path.join(results_dir, 'diagnosis_distribution.png'), dpi=300, bbox_inches='tight')
    plt.close()
    
    # Correlation matrix
    correlation_matrix = df[numerical_cols].corr()
    plt.figure(figsize=(20, 16))
    sns.heatmap(correlation_matrix, annot=False, cmap='coolwarm', center=0, 
                square=True, linewidths=0.5, cbar_kws={"shrink": 0.8})
    plt.title('Correlation Matrix of Numerical Features', fontsize=16, fontweight='bold', pad=20)
    plt.tight_layout()
    plt.savefig(os.path.join(results_dir, 'correlation_matrix.png'), dpi=300, bbox_inches='tight')
    plt.close()
    
    print("\nVisualizations saved to results/ directory")

def main():
    """Main function to run all analyses"""
    # Load data
    df = load_data()
    
    # Descriptive statistics
    desc_stats, additional_stats, numerical_cols = descriptive_statistics(df)
    
    # Inferential statistics
    ttest_results, effect_sizes = inferential_statistics(df, numerical_cols)
    
    # Exploratory analysis
    correlation_matrix, outlier_counts = exploratory_analysis(df, numerical_cols)
    
    # Create visualizations
    create_visualizations(df, numerical_cols)
    
    # Save results
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.join(script_dir, '../..')
    results_dir = os.path.join(project_root, 'results')
    os.makedirs(results_dir, exist_ok=True)
    
    summary_stats = {
        'descriptive_stats': desc_stats.to_dict(),
        'ttest_results': ttest_results,
        'effect_sizes': effect_sizes,
        'outlier_counts': outlier_counts
    }
    
    summary_path = os.path.join(results_dir, 'statistical_summary.json')
    with open(summary_path, 'w') as f:
        json.dump(summary_stats, f, indent=2, default=str)
    
    print(f"\nStatistical summary saved to {summary_path}")

if __name__ == "__main__":
    main()

