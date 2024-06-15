"""
Univariate, Bivariate, and Multivariate Analysis
Breast Cancer Diagnosis Dataset
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from scipy.stats import pearsonr, spearmanr
import os

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)

def load_data():
    """Load the breast cancer dataset"""
    df = pd.read_csv('../../data/breast_cancer.csv')
    return df

def univariate_analysis(df, numerical_cols):
    """Perform univariate analysis"""
    print("=== UNIVARIATE ANALYSIS ===")
    os.makedirs('../../results/univariate', exist_ok=True)
    
    # Select key features for analysis
    key_features = ['radius_mean', 'texture_mean', 'perimeter_mean', 
                   'area_mean', 'smoothness_mean', 'compactness_mean']
    
    # Distribution analysis
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    axes = axes.ravel()
    
    for idx, feature in enumerate(key_features):
        # Histogram
        axes[idx].hist(df[feature], bins=30, edgecolor='black', alpha=0.7)
        axes[idx].set_title(f'Distribution of {feature}', fontweight='bold')
        axes[idx].set_xlabel(feature)
        axes[idx].set_ylabel('Frequency')
        axes[idx].axvline(df[feature].mean(), color='red', linestyle='--', 
                         label=f'Mean: {df[feature].mean():.2f}')
        axes[idx].axvline(df[feature].median(), color='green', linestyle='--', 
                         label=f'Median: {df[feature].median():.2f}')
        axes[idx].legend()
    
    plt.suptitle('Univariate Analysis: Feature Distributions', 
                 fontsize=16, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig('../../results/univariate/distributions.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # Box plots
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    axes = axes.ravel()
    
    for idx, feature in enumerate(key_features):
        df.boxplot(column=feature, ax=axes[idx])
        axes[idx].set_title(f'Box Plot of {feature}', fontweight='bold')
        axes[idx].set_ylabel(feature)
    
    plt.suptitle('Univariate Analysis: Box Plots', 
                 fontsize=16, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig('../../results/univariate/boxplots.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # Statistical summary
    print("\nUnivariate Statistics:")
    univariate_stats = df[key_features].describe()
    print(univariate_stats)
    
    # Normality tests
    print("\n=== NORMALITY TESTS ===")
    for feature in key_features:
        stat, p_value = stats.shapiro(df[feature].sample(min(5000, len(df))))
        is_normal = p_value > 0.05
        print(f"{feature}: Shapiro-Wilk statistic={stat:.4f}, p-value={p_value:.4f}, "
              f"Normal={is_normal}")
    
    return univariate_stats

def bivariate_analysis(df, numerical_cols):
    """Perform bivariate analysis"""
    print("\n=== BIVARIATE ANALYSIS ===")
    os.makedirs('../../results/bivariate', exist_ok=True)
    
    # Correlation analysis
    correlation_matrix = df[numerical_cols].corr()
    
    # Select pairs for detailed analysis
    key_features = ['radius_mean', 'texture_mean', 'perimeter_mean', 
                   'area_mean', 'smoothness_mean', 'compactness_mean']
    
    # Scatter plots for highly correlated pairs
    highly_corr_pairs = [
        ('radius_mean', 'perimeter_mean'),
        ('radius_mean', 'area_mean'),
        ('perimeter_mean', 'area_mean'),
        ('radius_mean', 'radius_worst'),
        ('texture_mean', 'texture_worst')
    ]
    
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    axes = axes.ravel()
    
    for idx, (feat1, feat2) in enumerate(highly_corr_pairs[:6]):
        # Color by diagnosis
        for diagnosis in ['M', 'B']:
            subset = df[df['diagnosis'] == diagnosis]
            axes[idx].scatter(subset[feat1], subset[feat2], 
                            alpha=0.6, label=diagnosis, s=30)
        
        # Calculate correlation
        corr_coef, p_value = pearsonr(df[feat1], df[feat2])
        axes[idx].set_xlabel(feat1)
        axes[idx].set_ylabel(feat2)
        axes[idx].set_title(f'{feat1} vs {feat2}\n(r={corr_coef:.3f}, p={p_value:.4f})', 
                           fontweight='bold')
        axes[idx].legend()
        axes[idx].grid(True, alpha=0.3)
    
    plt.suptitle('Bivariate Analysis: Scatter Plots', 
                 fontsize=16, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig('../../results/bivariate/scatter_plots.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # Correlation heatmap for key features
    plt.figure(figsize=(12, 10))
    key_corr = df[key_features].corr()
    sns.heatmap(key_corr, annot=True, cmap='coolwarm', center=0, 
                square=True, linewidths=0.5, fmt='.3f')
    plt.title('Bivariate Analysis: Correlation Heatmap of Key Features', 
              fontsize=14, fontweight='bold', pad=20)
    plt.tight_layout()
    plt.savefig('../../results/bivariate/correlation_heatmap.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # Feature vs Diagnosis analysis
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    axes = axes.ravel()
    
    for idx, feature in enumerate(key_features):
        df.boxplot(column=feature, by='diagnosis', ax=axes[idx])
        axes[idx].set_title(f'{feature} by Diagnosis', fontweight='bold')
        axes[idx].set_xlabel('Diagnosis')
        axes[idx].set_ylabel(feature)
        
        # Statistical test
        malignant = df[df['diagnosis'] == 'M'][feature]
        benign = df[df['diagnosis'] == 'B'][feature]
        t_stat, p_value = stats.ttest_ind(malignant, benign)
        axes[idx].text(0.5, 0.95, f'p-value: {p_value:.4f}', 
                      transform=axes[idx].transAxes, 
                      verticalalignment='top', fontsize=10,
                      bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    plt.suptitle('Bivariate Analysis: Features by Diagnosis', 
                 fontsize=16, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig('../../results/bivariate/features_by_diagnosis.png', 
                dpi=300, bbox_inches='tight')
    plt.close()
    
    print("\nBivariate analysis visualizations saved to results/bivariate/")

def multivariate_analysis(df, numerical_cols):
    """Perform multivariate analysis"""
    print("\n=== MULTIVARIATE ANALYSIS ===")
    os.makedirs('../../results/multivariate', exist_ok=True)
    
    # Principal Component Analysis (PCA)
    from sklearn.decomposition import PCA
    from sklearn.preprocessing import StandardScaler
    
    # Prepare data
    X = df[numerical_cols].values
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Apply PCA
    pca = PCA()
    pca.fit(X_scaled)
    
    # Explained variance
    explained_variance = pca.explained_variance_ratio_
    cumulative_variance = np.cumsum(explained_variance)
    
    # Scree plot
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    
    axes[0].bar(range(1, min(21, len(explained_variance) + 1)), 
               explained_variance[:20], alpha=0.7)
    axes[0].set_xlabel('Principal Component')
    axes[0].set_ylabel('Explained Variance Ratio')
    axes[0].set_title('Scree Plot: Explained Variance by Component', 
                     fontweight='bold')
    axes[0].grid(True, alpha=0.3)
    
    axes[1].plot(range(1, min(21, len(cumulative_variance) + 1)), 
                cumulative_variance[:20], marker='o', linewidth=2)
    axes[1].axhline(y=0.95, color='r', linestyle='--', label='95% Variance')
    axes[1].set_xlabel('Number of Components')
    axes[1].set_ylabel('Cumulative Explained Variance')
    axes[1].set_title('Cumulative Explained Variance', fontweight='bold')
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('../../results/multivariate/pca_analysis.png', 
                dpi=300, bbox_inches='tight')
    plt.close()
    
    # Number of components for 95% variance
    n_components_95 = np.where(cumulative_variance >= 0.95)[0][0] + 1
    print(f"\nNumber of components explaining 95% variance: {n_components_95}")
    print(f"First 5 components explain {cumulative_variance[4]:.2%} of variance")
    
    # PCA biplot (first 2 components)
    pca_2d = PCA(n_components=2)
    X_pca = pca_2d.fit_transform(X_scaled)
    
    fig, ax = plt.subplots(figsize=(12, 10))
    for diagnosis in ['M', 'B']:
        mask = df['diagnosis'] == diagnosis
        ax.scatter(X_pca[mask, 0], X_pca[mask, 1], 
                  alpha=0.6, label=diagnosis, s=50)
    
    ax.set_xlabel(f'First Principal Component ({explained_variance[0]:.2%} variance)', 
                 fontweight='bold')
    ax.set_ylabel(f'Second Principal Component ({explained_variance[1]:.2%} variance)', 
                 fontweight='bold')
    ax.set_title('PCA: First Two Principal Components', fontsize=14, fontweight='bold')
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('../../results/multivariate/pca_biplot.png', 
                dpi=300, bbox_inches='tight')
    plt.close()
    
    # Feature importance from PCA
    feature_importance = pd.DataFrame({
        'Feature': numerical_cols,
        'PC1': pca_2d.components_[0],
        'PC2': pca_2d.components_[1]
    })
    feature_importance['PC1_abs'] = np.abs(feature_importance['PC1'])
    feature_importance['PC2_abs'] = np.abs(feature_importance['PC2'])
    
    # Top features for PC1
    top_pc1 = feature_importance.nlargest(10, 'PC1_abs')[['Feature', 'PC1']]
    print("\nTop 10 features for PC1:")
    print(top_pc1)
    
    # Correlation matrix visualization (multivariate relationships)
    key_features = ['radius_mean', 'texture_mean', 'perimeter_mean', 
                   'area_mean', 'smoothness_mean', 'compactness_mean',
                   'concavity_mean', 'symmetry_mean', 'fractal_dimension_mean']
    
    plt.figure(figsize=(14, 12))
    corr_matrix = df[key_features].corr()
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0, 
                square=True, linewidths=0.5, fmt='.3f', cbar_kws={"shrink": 0.8})
    plt.title('Multivariate Analysis: Correlation Matrix of Key Features', 
              fontsize=16, fontweight='bold', pad=20)
    plt.tight_layout()
    plt.savefig('../../results/multivariate/correlation_matrix.png', 
                dpi=300, bbox_inches='tight')
    plt.close()
    
    # Pair plot for key features (sample if too many points)
    sample_df = df.sample(min(200, len(df)))
    key_features_subset = key_features[:6]  # First 6 features
    
    pair_plot = sns.pairplot(sample_df, vars=key_features_subset, 
                            hue='diagnosis', diag_kind='kde', 
                            plot_kws={'alpha': 0.6, 's': 20})
    pair_plot.fig.suptitle('Multivariate Analysis: Pair Plot of Key Features', 
                          fontsize=14, fontweight='bold', y=1.02)
    plt.savefig('../../results/multivariate/pair_plot.png', 
                dpi=300, bbox_inches='tight')
    plt.close()
    
    print("\nMultivariate analysis visualizations saved to results/multivariate/")
    
    return {
        'n_components_95': int(n_components_95),
        'explained_variance': explained_variance.tolist(),
        'cumulative_variance': cumulative_variance.tolist(),
        'feature_importance': feature_importance.to_dict('records')
    }

def main():
    """Main function to run all analyses"""
    # Load data
    df = load_data()
    
    # Get numerical columns
    numerical_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    numerical_cols = [col for col in numerical_cols if col != 'id']
    
    # Univariate analysis
    univariate_stats = univariate_analysis(df, numerical_cols)
    
    # Bivariate analysis
    bivariate_analysis(df, numerical_cols)
    
    # Multivariate analysis
    multivariate_results = multivariate_analysis(df, numerical_cols)
    
    print("\n=== ANALYSIS COMPLETE ===")
    print("All visualizations and results saved to results/ directory")

if __name__ == "__main__":
    main()

