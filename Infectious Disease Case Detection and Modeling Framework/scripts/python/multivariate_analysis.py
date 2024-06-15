"""
Multivariate Analysis Module
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.manifold import TSNE
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from data_loader import load_data, clean_data

def multivariate_analysis(df_clean):
    """
    Perform multivariate analysis
    
    Parameters:
    -----------
    df_clean : DataFrame
        Cleaned dataset
    """
    print("=== MULTIVARIATE ANALYSIS ===\n")
    
    # Select numeric columns
    numeric_cols = ['Incidence_Rate', 'CI_Lower', 'CI_Upper', 'Annual_Count', 'Trend_5yr']
    numeric_cols = [col for col in numeric_cols if col in df_clean.columns]
    data = df_clean[numeric_cols].dropna()
    
    # Correlation matrix
    print("1. Correlation Matrix:")
    corr_matrix = data.corr()
    print(corr_matrix)
    
    # Visualize correlation matrix
    plt.figure(figsize=(12, 10))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0, fmt='.2f', square=True)
    plt.title('Correlation Matrix')
    plt.tight_layout()
    plt.savefig('correlation_matrix.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    # Principal Component Analysis (PCA)
    print("\n2. Principal Component Analysis (PCA):")
    scaler = StandardScaler()
    data_scaled = scaler.fit_transform(data)
    
    pca = PCA()
    pca.fit(data_scaled)
    
    # Explained variance
    explained_variance = pca.explained_variance_ratio_
    cumulative_variance = np.cumsum(explained_variance)
    
    print("Explained Variance Ratio:")
    for i, (var, cum_var) in enumerate(zip(explained_variance, cumulative_variance)):
        print(f"   PC{i+1}: {var:.4f} ({var*100:.2f}%), Cumulative: {cum_var:.4f} ({cum_var*100:.2f}%)")
    
    # Scree plot
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))
    
    axes[0].bar(range(1, len(explained_variance) + 1), explained_variance)
    axes[0].set_xlabel('Principal Component')
    axes[0].set_ylabel('Explained Variance Ratio')
    axes[0].set_title('Scree Plot')
    
    axes[1].plot(range(1, len(cumulative_variance) + 1), cumulative_variance, marker='o')
    axes[1].set_xlabel('Number of Components')
    axes[1].set_ylabel('Cumulative Explained Variance')
    axes[1].set_title('Cumulative Explained Variance')
    axes[1].axhline(y=0.95, color='r', linestyle='--', label='95% Variance')
    axes[1].legend()
    
    plt.tight_layout()
    plt.savefig('pca_analysis.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    # PCA Biplot (first two components)
    pca_2 = PCA(n_components=2)
    pca_data = pca_2.fit_transform(data_scaled)
    
    plt.figure(figsize=(12, 8))
    plt.scatter(pca_data[:, 0], pca_data[:, 1], alpha=0.5)
    
    # Add variable vectors
    components = pca_2.components_.T * np.sqrt(pca_2.explained_variance_)
    for i, (comp, name) in enumerate(zip(components, numeric_cols)):
        plt.arrow(0, 0, comp[0], comp[1], head_width=0.1, head_length=0.1, fc='red', ec='red')
        plt.text(comp[0]*1.2, comp[1]*1.2, name, fontsize=10, color='red')
    
    plt.xlabel(f'PC1 ({explained_variance[0]*100:.2f}%)')
    plt.ylabel(f'PC2 ({explained_variance[1]*100:.2f}%)')
    plt.title('PCA Biplot')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('pca_biplot.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    # Component loadings
    print("\n3. PCA Component Loadings:")
    loadings = pd.DataFrame(
        pca_2.components_.T,
        columns=['PC1', 'PC2'],
        index=numeric_cols
    )
    print(loadings)
    
    return {
        'correlation_matrix': corr_matrix,
        'pca': pca,
        'explained_variance': explained_variance,
        'loadings': loadings
    }

def cluster_analysis(df_clean, n_clusters=3):
    """
    Perform cluster analysis using K-means
    
    Parameters:
    -----------
    df_clean : DataFrame
        Cleaned dataset
    n_clusters : int
        Number of clusters
    """
    from sklearn.cluster import KMeans
    
    print(f"\n4. Cluster Analysis (K-means, k={n_clusters}):")
    
    # Select numeric columns
    numeric_cols = ['Incidence_Rate', 'Annual_Count', 'Trend_5yr']
    numeric_cols = [col for col in numeric_cols if col in df_clean.columns]
    data = df_clean[numeric_cols].dropna()
    
    # Scale data
    scaler = StandardScaler()
    data_scaled = scaler.fit_transform(data)
    
    # K-means clustering
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    clusters = kmeans.fit_predict(data_scaled)
    
    # Add cluster labels to data
    data_with_clusters = data.copy()
    data_with_clusters['Cluster'] = clusters
    
    # Cluster statistics
    print("Cluster Statistics:")
    print(data_with_clusters.groupby('Cluster')[numeric_cols].mean())
    
    # Visualize clusters (if 2D or using PCA)
    if len(numeric_cols) >= 2:
        plt.figure(figsize=(10, 8))
        scatter = plt.scatter(data[numeric_cols[0]], data[numeric_cols[1]], 
                            c=clusters, cmap='viridis', alpha=0.6)
        plt.xlabel(numeric_cols[0])
        plt.ylabel(numeric_cols[1])
        plt.title(f'K-means Clustering (k={n_clusters})')
        plt.colorbar(scatter, label='Cluster')
        plt.tight_layout()
        plt.savefig('cluster_analysis.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    return {
        'kmeans': kmeans,
        'clusters': clusters,
        'data_with_clusters': data_with_clusters
    }

if __name__ == "__main__":
    df = load_data()
    df_clean = clean_data(df)
    
    # Multivariate analysis
    result = multivariate_analysis(df_clean)
    
    # Cluster analysis
    cluster_result = cluster_analysis(df_clean, n_clusters=3)

