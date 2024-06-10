"""
Visualization Module

Functions for creating plots and visualizations for model analysis.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import roc_curve, auc, confusion_matrix


def plot_roc_curve(model, X_test, y_test, save_path=None):
    """
    Plot ROC curve for a model.
    
    Parameters:
    -----------
    model : sklearn model
        Trained model with predict_proba method
    X_test : np.ndarray
        Test features
    y_test : np.ndarray
        Test labels
    save_path : str, optional
        Path to save the figure
        
    Example:
    --------
    >>> plot_roc_curve(model, X_test, y_test, 'results/figures/roc_curve.png')
    """
    y_pred_proba = model.predict_proba(X_test)[:, 1]
    fpr, tpr, _ = roc_curve(y_test, y_pred_proba)
    roc_auc = auc(fpr, tpr)
    
    plt.figure(figsize=(8, 6))
    plt.plot(fpr, tpr, color='darkorange', lw=2, 
             label=f'ROC curve (AUC = {roc_auc:.3f})')
    plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--', 
             label='Random Classifier')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate', fontsize=12)
    plt.ylabel('True Positive Rate', fontsize=12)
    plt.title('Receiver Operating Characteristic (ROC) Curve', 
              fontsize=14, fontweight='bold')
    plt.legend(loc='lower right', fontsize=11)
    plt.grid(alpha=0.3)
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✓ ROC curve saved to {save_path}")
    
    plt.show()


def plot_feature_importance(model, feature_names=None, top_n=10, save_path=None):
    """
    Plot feature importance for tree-based models.
    
    Parameters:
    -----------
    model : sklearn model
        Trained model with feature_importances_ attribute
    feature_names : list, optional
        Names of features
    top_n : int, default=10
        Number of top features to display
    save_path : str, optional
        Path to save the figure
        
    Example:
    --------
    >>> plot_feature_importance(model, feature_names, top_n=15)
    """
    if not hasattr(model, 'feature_importances_'):
        print("✗ Model does not have feature_importances_ attribute")
        return
    
    importances = model.feature_importances_
    
    if feature_names is None:
        feature_names = [f'Feature_{i}' for i in range(len(importances))]
    
    # Create DataFrame and sort
    importance_df = pd.DataFrame({
        'Feature': feature_names,
        'Importance': importances
    }).sort_values('Importance', ascending=False).head(top_n)
    
    # Plot
    plt.figure(figsize=(10, 8))
    bars = plt.barh(range(len(importance_df)), importance_df['Importance'])
    plt.yticks(range(len(importance_df)), importance_df['Feature'])
    plt.xlabel('Importance', fontsize=12)
    plt.title(f'Top {top_n} Feature Importances', fontsize=14, fontweight='bold')
    plt.gca().invert_yaxis()
    plt.grid(axis='x', alpha=0.3)
    
    # Color bars
    colors = plt.cm.viridis(np.linspace(0.3, 0.9, len(bars)))
    for bar, color in zip(bars, colors):
        bar.set_color(color)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✓ Feature importance plot saved to {save_path}")
    
    plt.show()


def plot_confusion_matrix(y_test, y_pred, save_path=None):
    """
    Plot confusion matrix.
    
    Parameters:
    -----------
    y_test : np.ndarray
        True labels
    y_pred : np.ndarray
        Predicted labels
    save_path : str, optional
        Path to save the figure
        
    Example:
    --------
    >>> plot_confusion_matrix(y_test, y_pred, 'results/figures/confusion_matrix.png')
    """
    cm = confusion_matrix(y_test, y_pred)
    
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', cbar=True,
                square=True, linewidths=1, linecolor='gray')
    plt.xlabel('Predicted Label', fontsize=12)
    plt.ylabel('True Label', fontsize=12)
    plt.title('Confusion Matrix', fontsize=14, fontweight='bold')
    
    # Add labels
    plt.gca().set_xticklabels(['Negative', 'Positive'])
    plt.gca().set_yticklabels(['Negative', 'Positive'])
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✓ Confusion matrix saved to {save_path}")
    
    plt.show()


def plot_model_comparison(comparison_df, metric='f1_score', save_path=None):
    """
    Plot comparison of multiple models.
    
    Parameters:
    -----------
    comparison_df : pd.DataFrame
        DataFrame with model comparison results
    metric : str, default='f1_score'
        Metric to plot
    save_path : str, optional
        Path to save the figure
        
    Example:
    --------
    >>> plot_model_comparison(comparison_df, metric='accuracy')
    """
    plt.figure(figsize=(10, 6))
    
    models = comparison_df['Model']
    values = comparison_df[metric]
    
    bars = plt.bar(models, values)
    plt.ylabel(metric.replace('_', ' ').title(), fontsize=12)
    plt.title(f'Model Comparison: {metric.replace("_", " ").title()}', 
              fontsize=14, fontweight='bold')
    plt.ylim([0, 1.0])
    plt.grid(axis='y', alpha=0.3)
    
    # Add value labels on bars
    for bar, value in zip(bars, values):
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{value:.3f}',
                ha='center', va='bottom', fontweight='bold')
    
    # Color bars
    colors = plt.cm.viridis(np.linspace(0.3, 0.9, len(bars)))
    for bar, color in zip(bars, colors):
        bar.set_color(color)
    
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✓ Model comparison plot saved to {save_path}")
    
    plt.show()


def plot_learning_curve(model, X_train, y_train, cv=5, save_path=None):
    """
    Plot learning curve showing model performance vs training size.
    
    Parameters:
    -----------
    model : sklearn model
        Model to evaluate
    X_train : np.ndarray
        Training features
    y_train : np.ndarray
        Training labels
    cv : int, default=5
        Number of cross-validation folds
    save_path : str, optional
        Path to save the figure
        
    Example:
    --------
    >>> plot_learning_curve(model, X_train, y_train, cv=5)
    """
    from sklearn.model_selection import learning_curve
    
    train_sizes, train_scores, val_scores = learning_curve(
        model, X_train, y_train, cv=cv, n_jobs=-1,
        train_sizes=np.linspace(0.1, 1.0, 10),
        scoring='accuracy'
    )
    
    train_mean = train_scores.mean(axis=1)
    train_std = train_scores.std(axis=1)
    val_mean = val_scores.mean(axis=1)
    val_std = val_scores.std(axis=1)
    
    plt.figure(figsize=(10, 6))
    plt.plot(train_sizes, train_mean, 'o-', color='r', label='Training score')
    plt.plot(train_sizes, val_mean, 'o-', color='g', label='Cross-validation score')
    
    plt.fill_between(train_sizes, train_mean - train_std, train_mean + train_std, 
                     alpha=0.1, color='r')
    plt.fill_between(train_sizes, val_mean - val_std, val_mean + val_std, 
                     alpha=0.1, color='g')
    
    plt.xlabel('Training Set Size', fontsize=12)
    plt.ylabel('Accuracy Score', fontsize=12)
    plt.title('Learning Curve', fontsize=14, fontweight='bold')
    plt.legend(loc='best', fontsize=11)
    plt.grid(alpha=0.3)
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✓ Learning curve saved to {save_path}")
    
    plt.show()


def plot_multiple_roc_curves(models_dict, X_test, y_test, save_path=None):
    """
    Plot ROC curves for multiple models on the same plot.
    
    Parameters:
    -----------
    models_dict : dict
        Dictionary of {model_name: model}
    X_test : np.ndarray
        Test features
    y_test : np.ndarray
        Test labels
    save_path : str, optional
        Path to save the figure
        
    Example:
    --------
    >>> models = {'Random Forest': rf_model, 'SVM': svm_model}
    >>> plot_multiple_roc_curves(models, X_test, y_test)
    """
    plt.figure(figsize=(10, 8))
    
    colors = plt.cm.tab10(np.linspace(0, 1, len(models_dict)))
    
    for (name, model), color in zip(models_dict.items(), colors):
        y_pred_proba = model.predict_proba(X_test)[:, 1]
        fpr, tpr, _ = roc_curve(y_test, y_pred_proba)
        roc_auc = auc(fpr, tpr)
        
        plt.plot(fpr, tpr, lw=2, color=color, 
                label=f'{name} (AUC = {roc_auc:.3f})')
    
    plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--', 
             label='Random Classifier')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate', fontsize=12)
    plt.ylabel('True Positive Rate', fontsize=12)
    plt.title('ROC Curves Comparison', fontsize=14, fontweight='bold')
    plt.legend(loc='lower right', fontsize=10)
    plt.grid(alpha=0.3)
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✓ Multiple ROC curves saved to {save_path}")
    
    plt.show()


if __name__ == "__main__":
    # Example usage
    from data_processing import generate_synthetic_data, preprocess_data
    from models import train_random_forest, train_svm
    
    print("Visualization Module - Example Usage\n")
    
    # Generate and preprocess data
    df = generate_synthetic_data(n_samples=1000)
    X_train, X_test, y_train, y_test, _ = preprocess_data(df)
    
    # Train models
    rf_model = train_random_forest(X_train, y_train, n_estimators=50)
    svm_model = train_svm(X_train, y_train)
    
    # Create visualizations
    print("\nGenerating visualizations...")
    
    # ROC curve
    plot_roc_curve(rf_model, X_test, y_test)
    
    # Feature importance
    feature_names = ['age', 'bmi', 'blood_pressure_sys', 'blood_pressure_dia',
                     'glucose', 'cholesterol', 'heart_rate', 'biomarker_a', 'biomarker_b']
    plot_feature_importance(rf_model, feature_names, top_n=9)
    
    # Confusion matrix
    y_pred = rf_model.predict(X_test)
    plot_confusion_matrix(y_test, y_pred)
    
    # Multiple ROC curves
    models = {'Random Forest': rf_model, 'SVM': svm_model}
    plot_multiple_roc_curves(models, X_test, y_test)


