"""
AI-Driven Cancer Drug Discovery and Target Identification
Comprehensive Python Module with Reusable Functions

Author: Research Paper Review Project
Reference: Signal Transduction and Targeted Therapy - https://www.nature.com/articles/s41392-022-00994-0
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Tuple, Dict, List, Optional
import warnings
warnings.filterwarnings('ignore')

# Machine Learning
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (classification_report, confusion_matrix, 
                            roc_auc_score, accuracy_score, roc_curve)
from sklearn.manifold import TSNE
import umap.umap_ as umap

# Statistical analysis
from scipy.stats import ttest_ind, f_oneway


def generate_synthetic_data(
    n_genes: int = 200,
    n_normal_samples: int = 100,
    n_cancer_samples: int = 100,
    n_differential_genes: int = 50,
    random_state: int = 42
) -> Tuple[pd.DataFrame, List[str]]:
    """
    Generate synthetic gene expression data for demonstration purposes.
    
    Parameters:
    -----------
    n_genes : int
        Number of genes in the dataset
    n_normal_samples : int
        Number of normal tissue samples
    n_cancer_samples : int
        Number of cancer tissue samples
    n_differential_genes : int
        Number of differentially expressed genes between conditions
    random_state : int
        Random seed for reproducibility
        
    Returns:
    --------
    df : pd.DataFrame
        DataFrame with gene expression data and sample labels
    gene_names : List[str]
        List of gene names
    """
    np.random.seed(random_state)
    
    # Generate gene names
    gene_names = [f"Gene_{i+1}" for i in range(n_genes)]
    
    # Generate normal samples
    normal_data = np.random.normal(
        loc=5.0, scale=1.5, size=(n_normal_samples, n_genes)
    )
    
    # Generate cancer samples
    cancer_data = np.random.normal(
        loc=5.0, scale=1.5, size=(n_cancer_samples, n_genes)
    )
    
    # Create differential expression
    differential_indices = np.random.choice(
        n_genes, n_differential_genes, replace=False
    )
    
    # Upregulate half of differential genes
    n_upregulated = n_differential_genes // 2
    for idx in differential_indices[:n_upregulated]:
        cancer_data[:, idx] = np.random.normal(
            loc=8.0, scale=2.0, size=n_cancer_samples
        )
    
    # Downregulate remaining differential genes
    for idx in differential_indices[n_upregulated:]:
        cancer_data[:, idx] = np.random.normal(
            loc=2.0, scale=1.0, size=n_cancer_samples
        )
    
    # Combine data
    data = np.vstack([normal_data, cancer_data])
    labels = np.array(['Normal'] * n_normal_samples + 
                      ['Cancer'] * n_cancer_samples)
    
    # Create DataFrame
    df = pd.DataFrame(data, columns=gene_names)
    df['Sample_Type'] = labels
    
    return df, gene_names


def perform_differential_expression(
    df: pd.DataFrame,
    gene_names: List[str],
    group_col: str = 'Sample_Type',
    control_group: str = 'Normal',
    treatment_group: str = 'Cancer'
) -> pd.DataFrame:
    """
    Perform t-tests to identify differentially expressed genes.
    
    Parameters:
    -----------
    df : pd.DataFrame
        DataFrame with gene expression data
    gene_names : List[str]
        List of gene names to test
    group_col : str
        Column name containing group labels
    control_group : str
        Name of control group
    treatment_group : str
        Name of treatment group
        
    Returns:
    --------
    results : pd.DataFrame
        DataFrame with t-test results for each gene
    """
    results = []
    
    for gene in gene_names:
        # Extract data for each group
        control = df[df[group_col] == control_group][gene]
        treatment = df[df[group_col] == treatment_group][gene]
        
        # Perform t-test
        t_stat, p_value = ttest_ind(control, treatment)
        
        # Calculate effect size (Cohen's d)
        mean_diff = treatment.mean() - control.mean()
        pooled_std = np.sqrt((control.std()**2 + treatment.std()**2) / 2)
        cohens_d = mean_diff / pooled_std if pooled_std > 0 else 0
        
        results.append({
            'Gene': gene,
            'Mean_Control': control.mean(),
            'Mean_Treatment': treatment.mean(),
            'Mean_Difference': mean_diff,
            'T_Statistic': t_stat,
            'P_Value': p_value,
            'Cohen_D': cohens_d,
            'Std_Control': control.std(),
            'Std_Treatment': treatment.std()
        })
    
    # Create results DataFrame
    results_df = pd.DataFrame(results)
    results_df['Significant'] = results_df['P_Value'] < 0.05
    
    # Bonferroni correction
    num_comparisons = len(results_df)
    results_df['FDR_Corrected'] = results_df['P_Value'] < 0.05 / num_comparisons
    
    # Sort by P-value
    results_df = results_df.sort_values('P_Value')
    
    return results_df


def plot_volcano(
    results_df: pd.DataFrame,
    sig_threshold: float = 0.05,
    fc_threshold: float = 1.0,
    figsize: Tuple[int, int] = (10, 8),
    save_path: Optional[str] = None
) -> plt.Figure:
    """
    Create a volcano plot from differential expression results.
    
    Parameters:
    -----------
    results_df : pd.DataFrame
        DataFrame with differential expression results
    sig_threshold : float
        P-value threshold for significance
    fc_threshold : float
        Absolute fold change threshold
    figsize : Tuple[int, int]
        Figure size
    save_path : Optional[str]
        Path to save the figure
        
    Returns:
    --------
    fig : matplotlib Figure
    """
    fig, ax = plt.subplots(figsize=figsize)
    
    # Calculate log fold change and -log10 p-value
    log_fc = results_df['Mean_Difference']
    log_p = -np.log10(results_df['P_Value'])
    
    # Color points based on significance
    colors = [
        'red' if (p < sig_threshold and abs(fc) > fc_threshold) else 'gray'
        for p, fc in zip(results_df['P_Value'], log_fc)
    ]
    
    # Plot
    ax.scatter(log_fc, log_p, c=colors, alpha=0.6, s=30, edgecolors='black', linewidth=0.5)
    
    # Add threshold lines
    ax.axhline(-np.log10(sig_threshold), color='red', linestyle='--', 
               label=f'p = {sig_threshold}', alpha=0.7)
    ax.axvline(-fc_threshold, color='blue', linestyle='--', alpha=0.5)
    ax.axvline(fc_threshold, color='blue', linestyle='--', alpha=0.5)
    
    # Labels and title
    ax.set_xlabel('Mean Difference (Treatment - Control)', fontsize=12, fontweight='bold')
    ax.set_ylabel('-log10(P-Value)', fontsize=12, fontweight='bold')
    ax.set_title('Volcano Plot: Differential Gene Expression', fontsize=14, fontweight='bold')
    ax.legend(fontsize=10)
    ax.grid(alpha=0.3)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    return fig


def perform_dimensionality_reduction(
    X: np.ndarray,
    methods: List[str] = ['PCA', 't-SNE', 'UMAP'],
    n_components: int = 2,
    random_state: int = 42,
    perplexity: int = 30,
    umap_n_neighbors: int = 15
) -> Dict[str, np.ndarray]:
    """
    Perform multiple dimensionality reduction techniques.
    
    Parameters:
    -----------
    X : np.ndarray
        Input data matrix
    methods : List[str]
        List of methods to apply
    n_components : int
        Number of dimensions in output
    random_state : int
        Random seed
    perplexity : int
        t-SNE perplexity parameter
    umap_n_neighbors : int
        UMAP n_neighbors parameter
        
    Returns:
    --------
    results : Dict[str, np.ndarray]
        Dictionary with reduced data for each method
    """
    results = {}
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    if 'PCA' in methods:
        pca = PCA(n_components=min(50, X.shape[1]), random_state=random_state)
        results['PCA'] = pca.fit_transform(X_scaled)
        results['PCA_variance'] = pca.explained_variance_ratio_
    
    if 't-SNE' in methods:
        tsne = TSNE(
            n_components=n_components, 
            random_state=random_state, 
            perplexity=perplexity
        )
        results['t-SNE'] = tsne.fit_transform(X_scaled)
    
    if 'UMAP' in methods:
        umap_reducer = umap.UMAP(
            n_components=n_components, 
            random_state=random_state, 
            n_neighbors=umap_n_neighbors, 
            min_dist=0.1
        )
        results['UMAP'] = umap_reducer.fit_transform(X_scaled)
    
    return results


def train_ml_models(
    X: np.ndarray,
    y: np.ndarray,
    test_size: float = 0.3,
    random_state: int = 42,
    cv_folds: int = 5
) -> Dict[str, Dict]:
    """
    Train multiple machine learning models for classification.
    
    Parameters:
    -----------
    X : np.ndarray
        Feature matrix
    y : np.ndarray
        Target labels
    test_size : float
        Proportion of data for testing
    random_state : int
        Random seed
    cv_folds : int
        Number of cross-validation folds
        
    Returns:
    --------
    results : Dict[str, Dict]
        Dictionary with results for each model
    """
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )
    
    # Standardize
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Define models
    models = {
        'Logistic Regression': LogisticRegression(max_iter=1000, random_state=random_state),
        'Random Forest': RandomForestClassifier(n_estimators=100, random_state=random_state),
        'Gradient Boosting': GradientBoostingClassifier(n_estimators=100, random_state=random_state)
    }
    
    # Train and evaluate
    results = {}
    for name, model in models.items():
        # Train
        model.fit(X_train_scaled, y_train)
        
        # Predict
        y_pred = model.predict(X_test_scaled)
        y_pred_proba = model.predict_proba(X_test_scaled)[:, 1] if hasattr(model, 'predict_proba') else None
        
        # Evaluate
        accuracy = accuracy_score(y_test, y_pred)
        auc = roc_auc_score(y_test, y_pred_proba) if y_pred_proba is not None else None
        cv_scores = cross_val_score(model, X_train_scaled, y_train, cv=cv_folds)
        
        results[name] = {
            'model': model,
            'scaler': scaler,
            'accuracy': accuracy,
            'auc': auc,
            'cv_mean': cv_scores.mean(),
            'cv_std': cv_scores.std(),
            'y_pred': y_pred,
            'y_pred_proba': y_pred_proba if y_pred_proba is not None else None
        }
    
    return results, X_test_scaled, y_test


def plot_model_comparison(
    results: Dict[str, Dict],
    figsize: Tuple[int, int] = (12, 5),
    save_path: Optional[str] = None
) -> plt.Figure:
    """
    Create visualizations comparing multiple ML models.
    
    Parameters:
    -----------
    results : Dict[str, Dict]
        Model results dictionary
    figsize : Tuple[int, int]
        Figure size
    save_path : Optional[str]
        Path to save figure
        
    Returns:
    --------
    fig : matplotlib Figure
    """
    fig, axes = plt.subplots(1, 2, figsize=figsize)
    
    # Model names and metrics
    model_names = list(results.keys())
    accuracies = [results[m]['accuracy'] for m in model_names]
    aucs = [results[m]['auc'] for m in model_names if results[m]['auc'] is not None]
    
    # Bar plot
    x = np.arange(len(model_names))
    width = 0.35
    
    axes[0].bar(x - width/2, accuracies, width, label='Accuracy', color='steelblue', alpha=0.8)
    if aucs:
        axes[0].bar(x + width/2, aucs, width, label='AUC-ROC', color='crimson', alpha=0.8)
    
    axes[0].set_ylabel('Score', fontsize=12, fontweight='bold')
    axes[0].set_title('Model Performance Comparison', fontsize=14, fontweight='bold')
    axes[0].set_xticks(x)
    axes[0].set_xticklabels(model_names, rotation=45, ha='right')
    axes[0].legend()
    axes[0].grid(alpha=0.3, axis='y')
    axes[0].set_ylim([0.5, 1.0])
    
    # ROC curves
    for name, result in results.items():
        if result['auc'] is not None:
            fpr, tpr, _ = roc_curve(y_test, result['y_pred_proba'])
            axes[1].plot(fpr, tpr, label=f'{name} (AUC={result["auc"]:.3f})', linewidth=2)
    
    axes[1].plot([0, 1], [0, 1], 'k--', label='Random Classifier')
    axes[1].set_xlabel('False Positive Rate', fontsize=12, fontweight='bold')
    axes[1].set_ylabel('True Positive Rate', fontsize=12, fontweight='bold')
    axes[1].set_title('ROC Curves', fontsize=14, fontweight='bold')
    axes[1].legend()
    axes[1].grid(alpha=0.3)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    return fig


def extract_feature_importance(
    results: Dict[str, Dict],
    feature_names: List[str],
    top_n: int = 20
) -> pd.DataFrame:
    """
    Extract and compare feature importance across models.
    
    Parameters:
    -----------
    results : Dict[str, Dict]
        Model results dictionary
    feature_names : List[str]
        Names of features
    top_n : int
        Number of top features to return
        
    Returns:
    --------
    importance_df : pd.DataFrame
        DataFrame with feature importances
    """
    importance_dict = {}
    
    for name, result in results.items():
        model = result['model']
        if hasattr(model, 'feature_importances_'):
            importance_dict[name] = dict(zip(feature_names, model.feature_importances_))
    
    if importance_dict:
        importance_df = pd.DataFrame(importance_dict)
        importance_df = importance_df.sort_values(
            by=importance_df.columns[0], ascending=False
        ).head(top_n)
        return importance_df
    else:
        print("No models with feature_importances_ attribute found.")
        return pd.DataFrame()


def main():
    """
    Main workflow demonstrating the complete analysis pipeline.
    """
    print("="*80)
    print("AI-Driven Cancer Drug Discovery and Target Identification")
    print("="*80)
    
    # 1. Generate synthetic data
    print("\n1. Generating synthetic gene expression data...")
    df, gene_names = generate_synthetic_data(
        n_genes=200,
        n_normal_samples=100,
        n_cancer_samples=100,
        n_differential_genes=50
    )
    print(f"   Generated {len(df)} samples with {len(gene_names)} genes")
    
    # 2. Differential expression analysis
    print("\n2. Performing differential expression analysis...")
    de_results = perform_differential_expression(df, gene_names)
    n_sig = de_results['Significant'].sum()
    print(f"   Found {n_sig} significantly differentially expressed genes (p < 0.05)")
    
    # 3. Create volcano plot
    print("\n3. Creating volcano plot...")
    fig = plot_volcano(de_results)
    plt.savefig('volcano_plot.png', dpi=300, bbox_inches='tight')
    print("   Saved volcano_plot.png")
    
    # 4. Dimensionality reduction
    print("\n4. Performing dimensionality reduction...")
    X = df.drop('Sample_Type', axis=1).values
    dr_results = perform_dimensionality_reduction(X, methods=['PCA', 't-SNE', 'UMAP'])
    print("   Completed PCA, t-SNE, and UMAP")
    
    # 5. Machine learning models
    print("\n5. Training machine learning models...")
    le = LabelEncoder()
    y = le.fit_transform(df['Sample_Type'])
    ml_results, X_test, y_test = train_ml_models(X, y)
    
    for name, result in ml_results.items():
        print(f"   {name}: Accuracy={result['accuracy']:.4f}, "
              f"AUC={result['auc']:.4f if result['auc'] else 'N/A'}")
    
    # 6. Model comparison
    print("\n6. Creating model comparison plots...")
    fig = plot_model_comparison(ml_results)
    plt.savefig('model_comparison.png', dpi=300, bbox_inches='tight')
    print("   Saved model_comparison.png")
    
    # 7. Feature importance
    print("\n7. Extracting feature importance...")
    importance_df = extract_feature_importance(ml_results, gene_names, top_n=20)
    if not importance_df.empty:
        print(f"   Top 5 most important genes:")
        for gene in importance_df.index[:5]:
            importance_str = ", ".join([f"{model}={importance_df.loc[gene, model]:.4f}" 
                                        for model in importance_df.columns])
            print(f"   - {gene}: {importance_str}")
    
    print("\n" + "="*80)
    print("Analysis complete!")
    print("="*80)


if __name__ == "__main__":
    main()

