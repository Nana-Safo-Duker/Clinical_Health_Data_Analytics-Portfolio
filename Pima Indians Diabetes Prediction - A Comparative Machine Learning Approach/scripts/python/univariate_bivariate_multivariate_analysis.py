"""
Pima Indians Diabetes Dataset - Univariate, Bivariate, and Multivariate Analysis
Python Script for Comprehensive Analysis
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import warnings
warnings.filterwarnings('ignore')

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (14, 8)

def load_data():
    """Load and prepare the dataset"""
    df = pd.read_csv('../../data/pima-indians-diabetes.csv', skiprows=9, header=None)
    columns = [
        'Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness',
        'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age', 'Outcome'
    ]
    df.columns = columns
    return df

def univariate_analysis(df, output_dir='../../outputs/'):
    """Perform univariate analysis on each feature"""
    print("=" * 80)
    print("UNIVARIATE ANALYSIS")
    print("=" * 80)
    
    numeric_features = ['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness',
                       'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age']
    
    # Summary statistics
    univariate_stats = pd.DataFrame({
        'Feature': numeric_features,
        'Mean': [df[col].mean() for col in numeric_features],
        'Median': [df[col].median() for col in numeric_features],
        'Std': [df[col].std() for col in numeric_features],
        'Variance': [df[col].var() for col in numeric_features],
        'Skewness': [df[col].skew() for col in numeric_features],
        'Kurtosis': [df[col].kurtosis() for col in numeric_features],
        'Min': [df[col].min() for col in numeric_features],
        'Max': [df[col].max() for col in numeric_features],
        'Q1': [df[col].quantile(0.25) for col in numeric_features],
        'Q3': [df[col].quantile(0.75) for col in numeric_features],
        'IQR': [df[col].quantile(0.75) - df[col].quantile(0.25) for col in numeric_features]
    })
    
    print("\nUnivariate Statistics:")
    print(univariate_stats)
    
    # Distribution plots
    fig, axes = plt.subplots(2, 4, figsize=(20, 10))
    axes = axes.ravel()
    
    for idx, feature in enumerate(numeric_features):
        axes[idx].hist(df[feature], bins=30, edgecolor='black', alpha=0.7, color='steelblue')
        axes[idx].axvline(df[feature].mean(), color='red', linestyle='--', label='Mean', linewidth=2)
        axes[idx].axvline(df[feature].median(), color='green', linestyle='--', label='Median', linewidth=2)
        axes[idx].set_title(f'Distribution of {feature}', fontsize=12, fontweight='bold')
        axes[idx].set_xlabel(feature)
        axes[idx].set_ylabel('Frequency')
        axes[idx].legend()
        axes[idx].grid(alpha=0.3)
    
    plt.suptitle('Univariate Analysis: Feature Distributions', fontsize=16, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig(f'{output_dir}univariate_distributions.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    # Box plots
    fig, axes = plt.subplots(2, 4, figsize=(20, 10))
    axes = axes.ravel()
    
    for idx, feature in enumerate(numeric_features):
        bp = axes[idx].boxplot(df[feature], vert=True, patch_artist=True)
        bp['boxes'][0].set_facecolor('lightblue')
        axes[idx].set_title(f'Box Plot of {feature}', fontsize=12, fontweight='bold')
        axes[idx].set_ylabel(feature)
        axes[idx].grid(alpha=0.3, axis='y')
    
    plt.suptitle('Univariate Analysis: Box Plots', fontsize=16, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig(f'{output_dir}univariate_boxplots.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    # Normality tests
    print("\n" + "=" * 80)
    print("NORMALITY TESTS (Shapiro-Wilk Test)")
    print("=" * 80)
    
    normality_results = []
    for feature in numeric_features:
        sample = df[feature].sample(min(5000, len(df)), random_state=42)
        stat, p_value = stats.shapiro(sample)
        normality_results.append({
            'Feature': feature,
            'W-statistic': stat,
            'P-value': p_value,
            'Normal': 'Yes' if p_value > 0.05 else 'No'
        })
    
    normality_df = pd.DataFrame(normality_results)
    print(normality_df)
    
    return univariate_stats, normality_df

def bivariate_analysis(df, output_dir='../../outputs/'):
    """Perform bivariate analysis between features and outcome"""
    print("\n" + "=" * 80)
    print("BIVARIATE ANALYSIS")
    print("=" * 80)
    
    numeric_features = ['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness',
                       'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age']
    
    # Feature vs Outcome box plots
    fig, axes = plt.subplots(2, 4, figsize=(20, 10))
    axes = axes.ravel()
    
    for idx, feature in enumerate(numeric_features):
        df.boxplot(column=feature, by='Outcome', ax=axes[idx], patch_artist=True)
        axes[idx].set_title(f'{feature} by Outcome', fontsize=12, fontweight='bold')
        axes[idx].set_xlabel('Outcome (0=No Diabetes, 1=Diabetes)')
        axes[idx].set_ylabel(feature)
        axes[idx].grid(alpha=0.3, axis='y')
    
    plt.suptitle('Bivariate Analysis: Features by Outcome', fontsize=16, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig(f'{output_dir}bivariate_boxplots.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    # Density plots by outcome
    fig, axes = plt.subplots(2, 4, figsize=(20, 10))
    axes = axes.ravel()
    
    for idx, feature in enumerate(numeric_features):
        df[df['Outcome'] == 0][feature].plot(kind='density', ax=axes[idx], 
                                             label='No Diabetes', alpha=0.7, color='skyblue', linewidth=2)
        df[df['Outcome'] == 1][feature].plot(kind='density', ax=axes[idx], 
                                             label='Diabetes', alpha=0.7, color='salmon', linewidth=2)
        axes[idx].set_title(f'{feature} Distribution by Outcome', fontsize=12, fontweight='bold')
        axes[idx].set_xlabel(feature)
        axes[idx].set_ylabel('Density')
        axes[idx].legend()
        axes[idx].grid(alpha=0.3)
    
    plt.suptitle('Bivariate Analysis: Feature Distributions by Outcome', fontsize=16, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig(f'{output_dir}bivariate_densities.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    # Correlation analysis
    correlation_matrix = df[numeric_features + ['Outcome']].corr()
    outcome_correlations = correlation_matrix['Outcome'].drop('Outcome').sort_values(ascending=False)
    
    print("\nCorrelation with Outcome:")
    print(outcome_correlations)
    
    # Visualize correlations
    plt.figure(figsize=(10, 6))
    outcome_correlations.plot(kind='barh', color='steelblue')
    plt.title('Feature Correlations with Outcome', fontsize=14, fontweight='bold')
    plt.xlabel('Correlation Coefficient')
    plt.grid(alpha=0.3, axis='x')
    plt.tight_layout()
    plt.savefig(f'{output_dir}bivariate_correlations.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    # Statistical tests (T-tests)
    print("\n" + "=" * 80)
    print("STATISTICAL TESTS (Independent T-tests)")
    print("=" * 80)
    
    diabetic = df[df['Outcome'] == 1]
    non_diabetic = df[df['Outcome'] == 0]
    
    ttest_results = []
    for feature in numeric_features:
        stat, p_value = stats.ttest_ind(diabetic[feature], non_diabetic[feature])
        ttest_results.append({
            'Feature': feature,
            'T-statistic': stat,
            'P-value': p_value,
            'Significant': 'Yes' if p_value < 0.05 else 'No',
            'Diabetic Mean': diabetic[feature].mean(),
            'Non-Diabetic Mean': non_diabetic[feature].mean(),
            'Difference': diabetic[feature].mean() - non_diabetic[feature].mean()
        })
    
    ttest_df = pd.DataFrame(ttest_results)
    print(ttest_df)
    
    return outcome_correlations, ttest_df

def multivariate_analysis(df, output_dir='../../outputs/'):
    """Perform multivariate analysis"""
    print("\n" + "=" * 80)
    print("MULTIVARIATE ANALYSIS")
    print("=" * 80)
    
    numeric_features = ['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness',
                       'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age']
    
    # Correlation heatmap
    correlation_matrix = df[numeric_features + ['Outcome']].corr()
    
    plt.figure(figsize=(12, 10))
    sns.heatmap(correlation_matrix, annot=True, fmt='.2f', cmap='coolwarm', 
                center=0, square=True, linewidths=1, cbar_kws={"shrink": 0.8},
                vmin=-1, vmax=1)
    plt.title('Multivariate Analysis: Feature Correlation Heatmap', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(f'{output_dir}multivariate_correlation_heatmap.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    # PCA Analysis
    print("\n" + "=" * 80)
    print("PRINCIPAL COMPONENT ANALYSIS (PCA)")
    print("=" * 80)
    
    # Prepare data (handle zeros)
    df_clean = df[numeric_features].copy()
    df_clean = df_clean.replace(0, np.nan)
    df_clean = df_clean.fillna(df_clean.median())
    
    # Standardize
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(df_clean)
    
    # Apply PCA
    pca = PCA(n_components=min(8, len(numeric_features)))
    X_pca = pca.fit_transform(X_scaled)
    
    # Explained variance
    explained_variance = pca.explained_variance_ratio_
    cumulative_variance = np.cumsum(explained_variance)
    
    print(f"Explained Variance by Component:")
    for i, (var, cum_var) in enumerate(zip(explained_variance, cumulative_variance)):
        print(f"PC{i+1}: {var:.4f} ({var*100:.2f}%) - Cumulative: {cum_var:.4f} ({cum_var*100:.2f}%)")
    
    # Scree plot
    plt.figure(figsize=(10, 6))
    plt.bar(range(1, len(explained_variance) + 1), explained_variance, alpha=0.7, color='steelblue', label='Individual')
    plt.plot(range(1, len(cumulative_variance) + 1), cumulative_variance, 'ro-', label='Cumulative')
    plt.xlabel('Principal Component')
    plt.ylabel('Explained Variance Ratio')
    plt.title('PCA Scree Plot', fontsize=14, fontweight='bold')
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(f'{output_dir}multivariate_pca_scree.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    # PCA visualization (2D)
    pca_2d = PCA(n_components=2)
    X_pca_2d = pca_2d.fit_transform(X_scaled)
    
    plt.figure(figsize=(12, 8))
    scatter = plt.scatter(X_pca_2d[:, 0], X_pca_2d[:, 1], c=df['Outcome'], 
                         cmap='viridis', alpha=0.6, edgecolors='black', s=50)
    plt.colorbar(scatter, label='Outcome')
    plt.xlabel(f'First Principal Component (Explained Variance: {pca_2d.explained_variance_ratio_[0]:.2%})')
    plt.ylabel(f'Second Principal Component (Explained Variance: {pca_2d.explained_variance_ratio_[1]:.2%})')
    plt.title('PCA 2D Visualization', fontsize=14, fontweight='bold')
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(f'{output_dir}multivariate_pca_2d.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    # PCA component loadings
    pca_loadings = pd.DataFrame(
        pca_2d.components_.T,
        columns=['PC1', 'PC2'],
        index=numeric_features
    )
    print("\nPCA Component Loadings (First 2 Components):")
    print(pca_loadings)
    
    # 3D scatter plot
    from mpl_toolkits.mplot3d import Axes3D
    
    top_features = ['Glucose', 'BMI', 'Age']
    fig = plt.figure(figsize=(14, 10))
    ax = fig.add_subplot(111, projection='3d')
    
    scatter = ax.scatter(df[top_features[0]], df[top_features[1]], df[top_features[2]], 
                        c=df['Outcome'], cmap='viridis', alpha=0.6, edgecolors='black', s=50)
    ax.set_xlabel(top_features[0])
    ax.set_ylabel(top_features[1])
    ax.set_zlabel(top_features[2])
    ax.set_title('3D Scatter Plot: Top 3 Features (Colored by Outcome)', fontsize=14, fontweight='bold')
    plt.colorbar(scatter, label='Outcome')
    plt.savefig(f'{output_dir}multivariate_3d_scatter.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    return pca, pca_loadings

def main():
    """Main function to run all analyses"""
    print("Pima Indians Diabetes Dataset - Univariate, Bivariate, Multivariate Analysis")
    print("=" * 80)
    
    # Create output directory
    import os
    os.makedirs('../../outputs', exist_ok=True)
    
    # Load data
    df = load_data()
    print(f"\nDataset loaded: {df.shape}")
    print(f"Features: {list(df.columns)}")
    
    # Univariate analysis
    univariate_stats, normality_df = univariate_analysis(df)
    
    # Bivariate analysis
    correlations, ttest_df = bivariate_analysis(df)
    
    # Multivariate analysis
    pca_model, pca_loadings = multivariate_analysis(df)
    
    print("\n" + "=" * 80)
    print("ANALYSIS COMPLETE")
    print("=" * 80)
    print("\nKey Findings:")
    print("1. Univariate: Features show varying distributions and normality")
    print("2. Bivariate: Strong correlations between Glucose, BMI, Age and Outcome")
    print("3. Multivariate: PCA reveals patterns in high-dimensional space")
    print("=" * 80)

if __name__ == "__main__":
    main()


