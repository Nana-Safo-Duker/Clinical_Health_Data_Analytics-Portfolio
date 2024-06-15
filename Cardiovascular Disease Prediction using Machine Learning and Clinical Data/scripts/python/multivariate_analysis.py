"""
Multivariate Analysis

This script performs multivariate analysis on the Cardiovascular Disease Dataset.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import warnings
warnings.filterwarnings('ignore')

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)

def load_data():
    """Load the dataset"""
    df = pd.read_csv('../../data/Cardiovascular_Disease_Dataset.csv')
    return df

def pca_analysis(df):
    """Perform Principal Component Analysis"""
    numerical_cols = ['age', 'restingBP', 'serumcholestrol', 'maxheartrate', 'oldpeak']
    X = df[numerical_cols].dropna()
    X_scaled = StandardScaler().fit_transform(X)
    
    # Perform PCA
    pca = PCA()
    pca.fit(X_scaled)
    
    # Explained variance
    explained_variance = pca.explained_variance_ratio_
    cumulative_variance = np.cumsum(explained_variance)
    
    print("=" * 80)
    print("PRINCIPAL COMPONENT ANALYSIS (PCA)")
    print("=" * 80)
    print("\nExplained Variance by Component:")
    for i, (var, cum_var) in enumerate(zip(explained_variance, cumulative_variance)):
        print(f"  PC{i+1}: {var:.4f} ({var*100:.2f}%) - Cumulative: {cum_var:.4f} ({cum_var*100:.2f}%)")
    
    # Transform data to first 2 principal components
    pca_2d = PCA(n_components=2)
    X_pca = pca_2d.fit_transform(X_scaled)
    
    # Plot
    plt.figure(figsize=(10, 8))
    target_labels = df.loc[X.index, 'target']
    plt.scatter(X_pca[:, 0], X_pca[:, 1], c=target_labels, cmap='viridis', alpha=0.6)
    plt.colorbar(label='Target')
    plt.title('PCA: First Two Principal Components')
    plt.xlabel(f'PC1 ({explained_variance[0]*100:.2f}% variance)')
    plt.ylabel(f'PC2 ({explained_variance[1]*100:.2f}% variance)')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('../../results/pca_analysis.png')
    plt.close()
    
    print(f"\nFirst two principal components explain {cumulative_variance[1]*100:.2f}% of variance")

def feature_importance(df):
    """Feature importance based on correlation with target"""
    numerical_cols = ['age', 'restingBP', 'serumcholestrol', 'maxheartrate', 'oldpeak']
    
    print("\n" + "=" * 80)
    print("FEATURE IMPORTANCE")
    print("=" * 80)
    
    feature_importance = {}
    for col in numerical_cols:
        if col in df.columns:
            correlation = df[col].corr(df['target'])
            feature_importance[col] = abs(correlation)
    
    # Sort by importance
    sorted_importance = sorted(feature_importance.items(), key=lambda x: x[1], reverse=True)
    
    print("\nFeature Importance (absolute correlation with target):")
    for feature, importance in sorted_importance:
        print(f"  {feature}: {importance:.4f}")
    
    # Visualize
    plt.figure(figsize=(10, 6))
    features, importances = zip(*sorted_importance)
    plt.barh(features, importances, color='steelblue')
    plt.xlabel('Absolute Correlation with Target')
    plt.title('Feature Importance Based on Correlation with Target')
    plt.gca().invert_yaxis()
    plt.grid(True, alpha=0.3, axis='x')
    plt.tight_layout()
    plt.savefig('../../results/feature_importance.png')
    plt.close()

def multivariate_correlation(df):
    """Multivariate correlation analysis"""
    numerical_cols = ['age', 'restingBP', 'serumcholestrol', 'maxheartrate', 'oldpeak', 'target']
    correlation_matrix = df[numerical_cols].corr()
    
    plt.figure(figsize=(12, 10))
    sns.heatmap(correlation_matrix, annot=True, fmt='.3f', cmap='coolwarm', center=0,
                square=True, linewidths=1)
    plt.title('Multivariate Correlation Matrix (Including Target)')
    plt.tight_layout()
    plt.savefig('../../results/multivariate_correlation.png')
    plt.close()

def main():
    """Main function"""
    df = load_data()
    pca_analysis(df)
    feature_importance(df)
    multivariate_correlation(df)
    print("\nMultivariate analysis complete!")

if __name__ == "__main__":
    main()

