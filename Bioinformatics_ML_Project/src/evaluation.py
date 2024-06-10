"""
Model Evaluation Module

Functions for evaluating and comparing ML models.
"""

import numpy as np
import pandas as pd
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, confusion_matrix, classification_report,
    roc_curve, precision_recall_curve, average_precision_score
)
from scipy import stats


def calculate_metrics(y_true, y_pred, y_pred_proba=None):
    """
    Calculate comprehensive classification metrics.
    
    Parameters:
    -----------
    y_true : np.ndarray
        True labels
    y_pred : np.ndarray
        Predicted labels
    y_pred_proba : np.ndarray, optional
        Predicted probabilities for positive class
        
    Returns:
    --------
    metrics : dict
        Dictionary of calculated metrics
        
    Example:
    --------
    >>> metrics = calculate_metrics(y_test, y_pred, y_pred_proba)
    """
    metrics = {
        'accuracy': accuracy_score(y_true, y_pred),
        'precision': precision_score(y_true, y_pred, zero_division=0),
        'recall': recall_score(y_true, y_pred, zero_division=0),
        'f1_score': f1_score(y_true, y_pred, zero_division=0),
    }
    
    # Add AUC if probabilities provided
    if y_pred_proba is not None:
        try:
            metrics['roc_auc'] = roc_auc_score(y_true, y_pred_proba)
            metrics['avg_precision'] = average_precision_score(y_true, y_pred_proba)
        except:
            pass
    
    return metrics


def evaluate_model(model, X_test, y_test, verbose=True):
    """
    Comprehensive evaluation of a trained model.
    
    Parameters:
    -----------
    model : sklearn model
        Trained model
    X_test : np.ndarray
        Test features
    y_test : np.ndarray
        Test labels
    verbose : bool, default=True
        Whether to print results
        
    Returns:
    --------
    results : dict
        Dictionary with all evaluation metrics and objects
        
    Example:
    --------
    >>> results = evaluate_model(model, X_test, y_test)
    """
    # Predictions
    y_pred = model.predict(X_test)
    
    # Predicted probabilities (if available)
    y_pred_proba = None
    if hasattr(model, 'predict_proba'):
        y_pred_proba = model.predict_proba(X_test)[:, 1]
    
    # Calculate metrics
    metrics = calculate_metrics(y_test, y_pred, y_pred_proba)
    
    # Confusion matrix
    cm = confusion_matrix(y_test, y_pred)
    
    # Classification report
    report = classification_report(y_test, y_pred, output_dict=True)
    
    # ROC curve
    fpr, tpr, roc_thresholds = None, None, None
    if y_pred_proba is not None:
        fpr, tpr, roc_thresholds = roc_curve(y_test, y_pred_proba)
    
    # Precision-Recall curve
    precision, recall, pr_thresholds = None, None, None
    if y_pred_proba is not None:
        precision, recall, pr_thresholds = precision_recall_curve(y_test, y_pred_proba)
    
    results = {
        'metrics': metrics,
        'confusion_matrix': cm,
        'classification_report': report,
        'y_pred': y_pred,
        'y_pred_proba': y_pred_proba,
        'roc_curve': (fpr, tpr, roc_thresholds),
        'pr_curve': (precision, recall, pr_thresholds)
    }
    
    if verbose:
        print_evaluation_results(results)
    
    return results


def print_evaluation_results(results):
    """
    Print formatted evaluation results.
    
    Parameters:
    -----------
    results : dict
        Results dictionary from evaluate_model
    """
    print("\n" + "=" * 60)
    print("MODEL EVALUATION RESULTS")
    print("=" * 60)
    
    # Metrics
    print("\nPerformance Metrics:")
    print("-" * 60)
    for metric, value in results['metrics'].items():
        print(f"  {metric.replace('_', ' ').title():20s} : {value:.4f}")
    
    # Confusion Matrix
    print("\nConfusion Matrix:")
    print("-" * 60)
    cm = results['confusion_matrix']
    print(f"  True Negatives  : {cm[0, 0]:4d}  |  False Positives: {cm[0, 1]:4d}")
    print(f"  False Negatives : {cm[1, 0]:4d}  |  True Positives : {cm[1, 1]:4d}")
    
    # Derived metrics
    tn, fp, fn, tp = cm.ravel()
    specificity = tn / (tn + fp) if (tn + fp) > 0 else 0
    sensitivity = tp / (tp + fn) if (tp + fn) > 0 else 0
    
    print("\nAdditional Metrics:")
    print("-" * 60)
    print(f"  Sensitivity (TPR)    : {sensitivity:.4f}")
    print(f"  Specificity (TNR)    : {specificity:.4f}")
    
    print("=" * 60)


def compare_models(models_dict, X_test, y_test):
    """
    Compare multiple models on the same test set.
    
    Parameters:
    -----------
    models_dict : dict
        Dictionary of {model_name: model}
    X_test : np.ndarray
        Test features
    y_test : np.ndarray
        Test labels
        
    Returns:
    --------
    comparison_df : pd.DataFrame
        DataFrame comparing all models
        
    Example:
    --------
    >>> models = {'Random Forest': rf_model, 'SVM': svm_model}
    >>> comparison = compare_models(models, X_test, y_test)
    """
    print("\n" + "=" * 70)
    print("COMPARING MODELS")
    print("=" * 70)
    
    results = []
    
    for name, model in models_dict.items():
        print(f"\nEvaluating {name}...")
        eval_results = evaluate_model(model, X_test, y_test, verbose=False)
        
        row = {'Model': name}
        row.update(eval_results['metrics'])
        results.append(row)
    
    comparison_df = pd.DataFrame(results)
    
    # Sort by F1 score
    comparison_df = comparison_df.sort_values('f1_score', ascending=False)
    
    print("\n" + "=" * 70)
    print("MODEL COMPARISON RESULTS")
    print("=" * 70)
    print(comparison_df.to_string(index=False))
    print("=" * 70)
    
    return comparison_df


def calculate_confidence_interval(scores, confidence=0.95):
    """
    Calculate confidence interval for a set of scores.
    
    Parameters:
    -----------
    scores : array-like
        Array of scores
    confidence : float, default=0.95
        Confidence level
        
    Returns:
    --------
    mean : float
        Mean score
    ci_lower : float
        Lower bound of CI
    ci_upper : float
        Upper bound of CI
        
    Example:
    --------
    >>> mean, lower, upper = calculate_confidence_interval([0.85, 0.87, 0.89])
    """
    scores = np.array(scores)
    mean = scores.mean()
    std_err = stats.sem(scores)
    ci_range = std_err * stats.t.ppf((1 + confidence) / 2, len(scores) - 1)
    
    return mean, mean - ci_range, mean + ci_range


def statistical_comparison(scores1, scores2, alpha=0.05):
    """
    Perform statistical test to compare two sets of scores.
    
    Parameters:
    -----------
    scores1 : array-like
        Scores from first model
    scores2 : array-like
        Scores from second model
    alpha : float, default=0.05
        Significance level
        
    Returns:
    --------
    results : dict
        Statistical test results
        
    Example:
    --------
    >>> results = statistical_comparison(rf_scores, svm_scores)
    """
    # Paired t-test
    t_stat, p_value = stats.ttest_rel(scores1, scores2)
    
    # Effect size (Cohen's d)
    mean_diff = np.mean(scores1) - np.mean(scores2)
    pooled_std = np.sqrt((np.var(scores1) + np.var(scores2)) / 2)
    cohens_d = mean_diff / pooled_std if pooled_std > 0 else 0
    
    results = {
        't_statistic': t_stat,
        'p_value': p_value,
        'significant': p_value < alpha,
        'cohens_d': cohens_d,
        'mean_diff': mean_diff
    }
    
    print("\nStatistical Comparison Results:")
    print("-" * 50)
    print(f"  Mean Difference : {mean_diff:.4f}")
    print(f"  T-statistic     : {t_stat:.4f}")
    print(f"  P-value         : {p_value:.4f}")
    print(f"  Cohen's d       : {cohens_d:.4f}")
    print(f"  Significant     : {'Yes' if results['significant'] else 'No'} (α={alpha})")
    
    return results


def generate_evaluation_report(model, X_test, y_test, model_name='Model'):
    """
    Generate a comprehensive evaluation report.
    
    Parameters:
    -----------
    model : sklearn model
        Trained model
    X_test : np.ndarray
        Test features
    y_test : np.ndarray
        Test labels
    model_name : str, default='Model'
        Name of the model for the report
        
    Returns:
    --------
    report : dict
        Comprehensive evaluation report
        
    Example:
    --------
    >>> report = generate_evaluation_report(model, X_test, y_test, 'Random Forest')
    """
    print(f"\n{'=' * 70}")
    print(f"EVALUATION REPORT: {model_name}")
    print(f"{'=' * 70}")
    
    # Basic evaluation
    results = evaluate_model(model, X_test, y_test, verbose=False)
    
    # Print detailed report
    print_evaluation_results(results)
    
    # Additional information
    print("\nDataset Information:")
    print("-" * 60)
    print(f"  Test Set Size     : {len(y_test)}")
    print(f"  Positive Cases    : {sum(y_test)} ({sum(y_test)/len(y_test)*100:.1f}%)")
    print(f"  Negative Cases    : {len(y_test)-sum(y_test)} ({(len(y_test)-sum(y_test))/len(y_test)*100:.1f}%)")
    
    if hasattr(model, 'feature_importances_'):
        print("\nModel Type: Tree-based (Feature importances available)")
    elif hasattr(model, 'coef_'):
        print("\nModel Type: Linear (Coefficients available)")
    else:
        print("\nModel Type: Other")
    
    print("=" * 70)
    
    return results


if __name__ == "__main__":
    # Example usage
    from data_processing import generate_synthetic_data, preprocess_data
    from models import train_random_forest, train_svm
    
    print("Model Evaluation Module - Example Usage\n")
    
    # Generate and preprocess data
    df = generate_synthetic_data(n_samples=1000)
    X_train, X_test, y_train, y_test, _ = preprocess_data(df)
    
    # Train models
    rf_model = train_random_forest(X_train, y_train, n_estimators=50)
    svm_model = train_svm(X_train, y_train)
    
    # Evaluate single model
    print("\n" + "=" * 70)
    print("SINGLE MODEL EVALUATION")
    rf_results = generate_evaluation_report(rf_model, X_test, y_test, 'Random Forest')
    
    # Compare models
    models = {
        'Random Forest': rf_model,
        'SVM': svm_model
    }
    comparison = compare_models(models, X_test, y_test)


