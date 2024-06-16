"""
Heart Disease Dataset - Machine Learning Analysis

This script performs comprehensive machine learning analysis including:
- Data Preprocessing
- Feature Engineering
- Model Training and Evaluation
- Model Comparison
- Feature Importance Analysis

Author: Data Science Team
Date: 2024
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import (accuracy_score, precision_score, recall_score, 
                             f1_score, roc_auc_score, confusion_matrix, 
                             classification_report, roc_curve, auc)
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
import warnings
import os
import joblib

warnings.filterwarnings('ignore')

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)

def load_data():
    """Load the heart disease dataset."""
    data_path = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'heart-disease.csv')
    df = pd.read_csv(data_path)
    print("Dataset loaded successfully!")
    print(f"Shape: {df.shape}")
    return df

def preprocess_data(df):
    """Preprocess the data for machine learning."""
    df_processed = df.copy()
    
    # Encode categorical variables
    le_sex = LabelEncoder()
    df_processed['sex'] = le_sex.fit_transform(df_processed['sex'])
    
    # Separate features and target
    X = df_processed.drop('heart_disease', axis=1)
    y = df_processed['heart_disease']
    
    return X, y, le_sex

def train_models(X_train, X_test, y_train, y_test):
    """Train multiple machine learning models."""
    models = {
        'Logistic Regression': LogisticRegression(random_state=42, max_iter=1000),
        'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42),
        'Support Vector Machine': SVC(probability=True, random_state=42),
        'K-Nearest Neighbors': KNeighborsClassifier(n_neighbors=5),
        'Naive Bayes': GaussianNB(),
        'Gradient Boosting': GradientBoostingClassifier(random_state=42),
        'XGBoost': XGBClassifier(random_state=42, eval_metric='logloss'),
        'LightGBM': LGBMClassifier(random_state=42, verbose=-1)
    }
    
    results = {}
    
    for name, model in models.items():
        print(f"\nTraining {name}...")
        model.fit(X_train, y_train)
        
        # Predictions
        y_pred = model.predict(X_test)
        y_pred_proba = model.predict_proba(X_test)[:, 1]
        
        # Metrics
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred)
        recall = recall_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)
        roc_auc = roc_auc_score(y_test, y_pred_proba)
        
        # Cross-validation
        cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring='accuracy')
        
        results[name] = {
            'model': model,
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1': f1,
            'roc_auc': roc_auc,
            'cv_mean': cv_scores.mean(),
            'cv_std': cv_scores.std(),
            'y_pred': y_pred,
            'y_pred_proba': y_pred_proba
        }
        
        print(f"  Accuracy: {accuracy:.4f}")
        print(f"  Precision: {precision:.4f}")
        print(f"  Recall: {recall:.4f}")
        print(f"  F1-Score: {f1:.4f}")
        print(f"  ROC-AUC: {roc_auc:.4f}")
        print(f"  CV Accuracy: {cv_scores.mean():.4f} (+/- {cv_scores.std() * 2:.4f})")
    
    return results

def plot_results(results, y_test):
    """Plot model comparison and ROC curves."""
    # Model comparison
    models_list = list(results.keys())
    metrics = ['accuracy', 'precision', 'recall', 'f1', 'roc_auc']
    
    fig, axes = plt.subplots(2, 3, figsize=(18, 10))
    axes = axes.ravel()
    
    for idx, metric in enumerate(metrics):
        values = [results[model][metric] for model in models_list]
        axes[idx].bar(models_list, values, alpha=0.7, edgecolor='black')
        axes[idx].set_title(f'{metric.upper()} Comparison', fontweight='bold')
        axes[idx].set_ylabel(metric.upper())
        axes[idx].tick_params(axis='x', rotation=45, ha='right')
        axes[idx].grid(True, alpha=0.3, axis='y')
        
        # Add value labels
        for i, v in enumerate(values):
            axes[idx].text(i, v, f'{v:.3f}', ha='center', va='bottom', fontsize=8)
    
    # ROC Curves
    axes[5].plot([0, 1], [0, 1], 'k--', label='Random')
    for name, result in results.items():
        fpr, tpr, _ = roc_curve(y_test, result['y_pred_proba'])
        roc_auc = result['roc_auc']
        axes[5].plot(fpr, tpr, label=f'{name} (AUC = {roc_auc:.3f})')
    axes[5].set_xlabel('False Positive Rate')
    axes[5].set_ylabel('True Positive Rate')
    axes[5].set_title('ROC Curves Comparison', fontweight='bold')
    axes[5].legend(loc='lower right', fontsize=8)
    axes[5].grid(True, alpha=0.3)
    
    plt.suptitle('Machine Learning Models Comparison', fontsize=16, fontweight='bold')
    plt.tight_layout()
    return fig

def plot_confusion_matrices(results, y_test, output_dir='../../results/figures'):
    """Plot confusion matrices for all models."""
    n_models = len(results)
    n_cols = 4
    n_rows = (n_models + n_cols - 1) // n_cols
    
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(16, 4*n_rows))
    axes = axes.ravel() if n_models > 1 else [axes]
    
    for idx, (name, result) in enumerate(results.items()):
        cm = confusion_matrix(y_test, result['y_pred'])
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=axes[idx])
        axes[idx].set_title(f'{name}\nAccuracy: {result["accuracy"]:.3f}', fontweight='bold')
        axes[idx].set_ylabel('True Label')
        axes[idx].set_xlabel('Predicted Label')
    
    # Hide unused subplots
    for idx in range(n_models, len(axes)):
        axes[idx].axis('off')
    
    plt.suptitle('Confusion Matrices - All Models', fontsize=16, fontweight='bold')
    plt.tight_layout()
    return fig

def feature_importance_analysis(results, X_train, output_dir='../../results/figures'):
    """Analyze and plot feature importance."""
    # Get models that have feature_importances_
    importance_models = {}
    for name, result in results.items():
        model = result['model']
        if hasattr(model, 'feature_importances_'):
            importance_models[name] = model
    
    if not importance_models:
        print("No models with feature importance available.")
        return
    
    n_models = len(importance_models)
    fig, axes = plt.subplots(1, n_models, figsize=(6*n_models, 6))
    if n_models == 1:
        axes = [axes]
    
    for idx, (name, model) in enumerate(importance_models.items()):
        importances = model.feature_importances_
        indices = np.argsort(importances)[::-1]
        
        axes[idx].bar(range(len(importances)), importances[indices], alpha=0.7, edgecolor='black')
        axes[idx].set_title(f'{name} - Feature Importance', fontweight='bold')
        axes[idx].set_xticks(range(len(importances)))
        axes[idx].set_xticklabels([X_train.columns[i] for i in indices], rotation=45, ha='right')
        axes[idx].set_ylabel('Importance')
        axes[idx].grid(True, alpha=0.3, axis='y')
    
    plt.suptitle('Feature Importance Analysis', fontsize=16, fontweight='bold')
    plt.tight_layout()
    return fig

def save_results(results, output_dir='../../results'):
    """Save model results and best model."""
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(os.path.join(output_dir, 'models'), exist_ok=True)
    
    # Create results DataFrame
    results_df = pd.DataFrame({
        name: {
            'Accuracy': result['accuracy'],
            'Precision': result['precision'],
            'Recall': result['recall'],
            'F1-Score': result['f1'],
            'ROC-AUC': result['roc_auc'],
            'CV Mean': result['cv_mean'],
            'CV Std': result['cv_std']
        }
        for name, result in results.items()
    }).T
    
    results_df = results_df.sort_values('roc_auc', ascending=False)
    results_df.to_csv(os.path.join(output_dir, 'model_results.csv'))
    print(f"\nResults saved to {output_dir}/model_results.csv")
    
    # Save best model
    best_model_name = results_df.index[0]
    best_model = results[best_model_name]['model']
    joblib.dump(best_model, os.path.join(output_dir, 'models', 'best_model.pkl'))
    print(f"Best model ({best_model_name}) saved to {output_dir}/models/best_model.pkl")
    
    return results_df

def main():
    """Main function to run ML analysis."""
    print("="*60)
    print("HEART DISEASE MACHINE LEARNING ANALYSIS")
    print("="*60)
    
    # Load data
    df = load_data()
    
    # Preprocess
    X, y, le_sex = preprocess_data(df)
    print(f"\nFeatures: {list(X.columns)}")
    print(f"Target distribution: {y.value_counts().to_dict()}")
    
    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    print(f"\nTrain set: {X_train.shape[0]} samples")
    print(f"Test set: {X_test.shape[0]} samples")
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Convert back to DataFrame
    X_train_scaled = pd.DataFrame(X_train_scaled, columns=X_train.columns)
    X_test_scaled = pd.DataFrame(X_test_scaled, columns=X_test.columns)
    
    # Train models
    results = train_models(X_train_scaled, X_test_scaled, y_train, y_test)
    
    # Plot results
    output_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'results', 'figures')
    os.makedirs(output_dir, exist_ok=True)
    
    fig1 = plot_results(results, y_test)
    fig1.savefig(os.path.join(output_dir, 'ml_model_comparison.png'), dpi=300, bbox_inches='tight')
    print(f"\nModel comparison plot saved to {output_dir}/ml_model_comparison.png")
    
    fig2 = plot_confusion_matrices(results, y_test, output_dir)
    fig2.savefig(os.path.join(output_dir, 'ml_confusion_matrices.png'), dpi=300, bbox_inches='tight')
    print(f"Confusion matrices saved to {output_dir}/ml_confusion_matrices.png")
    
    fig3 = feature_importance_analysis(results, X_train_scaled, output_dir)
    if fig3:
        fig3.savefig(os.path.join(output_dir, 'ml_feature_importance.png'), dpi=300, bbox_inches='tight')
        print(f"Feature importance plot saved to {output_dir}/ml_feature_importance.png")
    
    # Save results
    results_df = save_results(results)
    print("\n" + "="*60)
    print("MODEL PERFORMANCE SUMMARY")
    print("="*60)
    print(results_df)
    
    print("\n" + "="*60)
    print("Analysis complete!")
    print("="*60)

if __name__ == "__main__":
    main()

