"""
Machine Learning Analysis
Breast Cancer Diagnosis Dataset
Classification Problem: Malignant (M) vs Benign (B)
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold, GridSearchCV
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import (accuracy_score, precision_score, recall_score, 
                            f1_score, confusion_matrix, classification_report,
                            roc_auc_score, roc_curve, precision_recall_curve,
                            plot_confusion_matrix)
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, VotingClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
import os
import warnings
warnings.filterwarnings('ignore')

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)

def load_and_prepare_data():
    """Load and prepare the data for machine learning"""
    # Load data
    df = pd.read_csv('../../data/breast_cancer.csv')
    
    # Separate features and target
    X = df.drop(['id', 'diagnosis'], axis=1)
    y = df['diagnosis']
    
    # Encode target variable
    le = LabelEncoder()
    y_encoded = le.fit_transform(y)  # M=1, B=0
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
    )
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    return X_train, X_test, X_train_scaled, X_test_scaled, y_train, y_test, scaler, le

def train_and_evaluate_model(model, model_name, X_train, X_test, y_train, y_test, scaled=True):
    """Train and evaluate a machine learning model"""
    if scaled:
        X_train_use = X_train
        X_test_use = X_test
    else:
        X_train_use = X_train
        X_test_use = X_test
    
    # Train model
    model.fit(X_train_use, y_train)
    
    # Predictions
    y_train_pred = model.predict(X_train_use)
    y_test_pred = model.predict(X_test_use)
    y_test_proba = model.predict_proba(X_test_use)[:, 1] if hasattr(model, 'predict_proba') else None
    
    # Metrics
    train_accuracy = accuracy_score(y_train, y_train_pred)
    test_accuracy = accuracy_score(y_test, y_test_pred)
    precision = precision_score(y_test, y_test_pred)
    recall = recall_score(y_test, y_test_pred)
    f1 = f1_score(y_test, y_test_pred)
    
    # ROC AUC
    roc_auc = None
    if y_test_proba is not None:
        roc_auc = roc_auc_score(y_test, y_test_proba)
    
    # Confusion matrix
    cm = confusion_matrix(y_test, y_test_pred)
    
    results = {
        'model_name': model_name,
        'train_accuracy': train_accuracy,
        'test_accuracy': test_accuracy,
        'precision': precision,
        'recall': recall,
        'f1_score': f1,
        'roc_auc': roc_auc,
        'confusion_matrix': cm,
        'y_test_pred': y_test_pred,
        'y_test_proba': y_test_proba
    }
    
    return model, results

def cross_validate_model(model, X, y, cv=5):
    """Perform cross-validation"""
    cv_scores = cross_val_score(model, X, y, cv=cv, scoring='accuracy')
    return cv_scores.mean(), cv_scores.std()

def compare_models(X_train_scaled, X_test_scaled, y_train, y_test):
    """Compare multiple machine learning models"""
    print("=" * 80)
    print("MACHINE LEARNING MODEL COMPARISON")
    print("=" * 80)
    
    # Define models
    models = {
        'Logistic Regression': LogisticRegression(random_state=42, max_iter=1000),
        'Decision Tree': DecisionTreeClassifier(random_state=42),
        'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42),
        'Gradient Boosting': GradientBoostingClassifier(random_state=42),
        'SVM': SVC(probability=True, random_state=42),
        'K-Nearest Neighbors': KNeighborsClassifier(n_neighbors=5),
        'Naive Bayes': GaussianNB(),
        'XGBoost': XGBClassifier(random_state=42, eval_metric='logloss'),
        'LightGBM': LGBMClassifier(random_state=42, verbose=-1)
    }
    
    # Train and evaluate all models
    results_dict = {}
    trained_models = {}
    
    for model_name, model in models.items():
        print(f"\nTraining {model_name}...")
        trained_model, results = train_and_evaluate_model(
            model, model_name, X_train_scaled, X_test_scaled, 
            y_train, y_test, scaled=True
        )
        results_dict[model_name] = results
        trained_models[model_name] = trained_model
        
        print(f"  Test Accuracy: {results['test_accuracy']:.4f}")
        print(f"  Precision: {results['precision']:.4f}")
        print(f"  Recall: {results['recall']:.4f}")
        print(f"  F1 Score: {results['f1_score']:.4f}")
        if results['roc_auc']:
            print(f"  ROC AUC: {results['roc_auc']:.4f}")
    
    # Create comparison dataframe
    comparison_df = pd.DataFrame({
        'Model': [r['model_name'] for r in results_dict.values()],
        'Test Accuracy': [r['test_accuracy'] for r in results_dict.values()],
        'Precision': [r['precision'] for r in results_dict.values()],
        'Recall': [r['recall'] for r in results_dict.values()],
        'F1 Score': [r['f1_score'] for r in results_dict.values()],
        'ROC AUC': [r['roc_auc'] if r['roc_auc'] else np.nan for r in results_dict.values()]
    }).sort_values('Test Accuracy', ascending=False)
    
    print("\n" + "=" * 80)
    print("MODEL COMPARISON RESULTS")
    print("=" * 80)
    print(comparison_df.to_string(index=False))
    
    # Visualization
    os.makedirs('../../results/ml', exist_ok=True)
    
    # Accuracy comparison
    plt.figure(figsize=(12, 8))
    comparison_df_sorted = comparison_df.sort_values('Test Accuracy', ascending=True)
    plt.barh(comparison_df_sorted['Model'], comparison_df_sorted['Test Accuracy'], color='steelblue')
    plt.xlabel('Test Accuracy')
    plt.title('Model Comparison: Test Accuracy', fontsize=14, fontweight='bold')
    plt.xlim([0.9, 1.0])
    plt.tight_layout()
    plt.savefig('../../results/ml/model_comparison_accuracy.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # Metrics comparison
    metrics = ['Test Accuracy', 'Precision', 'Recall', 'F1 Score', 'ROC AUC']
    fig, axes = plt.subplots(1, len(metrics), figsize=(20, 5))
    
    for idx, metric in enumerate(metrics):
        comparison_df_sorted = comparison_df.sort_values(metric, ascending=True)
        axes[idx].barh(comparison_df_sorted['Model'], comparison_df_sorted[metric], color='steelblue')
        axes[idx].set_xlabel(metric)
        axes[idx].set_title(metric, fontweight='bold')
        if metric == 'ROC AUC':
            axes[idx].set_xlim([0.9, 1.0])
        else:
            axes[idx].set_xlim([0.85, 1.0])
    
    plt.suptitle('Model Comparison: All Metrics', fontsize=16, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig('../../results/ml/model_comparison_all_metrics.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    return results_dict, trained_models, comparison_df

def detailed_model_analysis(best_model_name, best_model, X_test_scaled, y_test, results_dict):
    """Perform detailed analysis of the best model"""
    print("\n" + "=" * 80)
    print(f"DETAILED ANALYSIS: {best_model_name}")
    print("=" * 80)
    
    results = results_dict[best_model_name]
    
    # Classification report
    print("\nClassification Report:")
    print(classification_report(y_test, results['y_test_pred'], 
                              target_names=['Benign', 'Malignant']))
    
    # Confusion matrix visualization
    plt.figure(figsize=(8, 6))
    cm = results['confusion_matrix']
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                xticklabels=['Benign', 'Malignant'],
                yticklabels=['Benign', 'Malignant'])
    plt.title(f'Confusion Matrix: {best_model_name}', fontsize=14, fontweight='bold')
    plt.ylabel('True Label')
    plt.xlabel('Predicted Label')
    plt.tight_layout()
    plt.savefig(f'../../results/ml/confusion_matrix_{best_model_name.replace(" ", "_")}.png', 
                dpi=300, bbox_inches='tight')
    plt.close()
    
    # ROC Curve
    if results['y_test_proba'] is not None:
        fpr, tpr, _ = roc_curve(y_test, results['y_test_proba'])
        plt.figure(figsize=(8, 6))
        plt.plot(fpr, tpr, linewidth=2, label=f'ROC curve (AUC = {results["roc_auc"]:.4f})')
        plt.plot([0, 1], [0, 1], 'k--', linewidth=1, label='Random Classifier')
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title(f'ROC Curve: {best_model_name}', fontsize=14, fontweight='bold')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(f'../../results/ml/roc_curve_{best_model_name.replace(" ", "_")}.png', 
                    dpi=300, bbox_inches='tight')
        plt.close()
        
        # Precision-Recall Curve
        precision, recall, _ = precision_recall_curve(y_test, results['y_test_proba'])
        plt.figure(figsize=(8, 6))
        plt.plot(recall, precision, linewidth=2)
        plt.xlabel('Recall')
        plt.ylabel('Precision')
        plt.title(f'Precision-Recall Curve: {best_model_name}', fontsize=14, fontweight='bold')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(f'../../results/ml/pr_curve_{best_model_name.replace(" ", "_")}.png', 
                    dpi=300, bbox_inches='tight')
        plt.close()
    
    # Feature importance (if available)
    if hasattr(best_model, 'feature_importances_'):
        feature_importance = pd.DataFrame({
            'Feature': [f'Feature_{i}' for i in range(len(best_model.feature_importances_))],
            'Importance': best_model.feature_importances_
        }).sort_values('Importance', ascending=False)
        
        plt.figure(figsize=(10, 8))
        top_features = feature_importance.head(15)
        plt.barh(top_features['Feature'], top_features['Importance'], color='steelblue')
        plt.xlabel('Importance')
        plt.title(f'Top 15 Feature Importances: {best_model_name}', 
                 fontsize=14, fontweight='bold')
        plt.tight_layout()
        plt.savefig(f'../../results/ml/feature_importance_{best_model_name.replace(" ", "_")}.png', 
                    dpi=300, bbox_inches='tight')
        plt.close()
        
        print("\nTop 10 Most Important Features:")
        print(feature_importance.head(10).to_string(index=False))

def hyperparameter_tuning(X_train_scaled, y_train):
    """Perform hyperparameter tuning for the best models"""
    print("\n" + "=" * 80)
    print("HYPERPARAMETER TUNING")
    print("=" * 80)
    
    # Random Forest tuning
    print("\nTuning Random Forest...")
    rf_param_grid = {
        'n_estimators': [100, 200, 300],
        'max_depth': [10, 20, None],
        'min_samples_split': [2, 5, 10]
    }
    rf_grid = GridSearchCV(
        RandomForestClassifier(random_state=42),
        rf_param_grid,
        cv=5,
        scoring='accuracy',
        n_jobs=-1
    )
    rf_grid.fit(X_train_scaled, y_train)
    print(f"Best parameters: {rf_grid.best_params_}")
    print(f"Best CV score: {rf_grid.best_score_:.4f}")
    
    # XGBoost tuning
    print("\nTuning XGBoost...")
    xgb_param_grid = {
        'n_estimators': [100, 200],
        'max_depth': [3, 5, 7],
        'learning_rate': [0.01, 0.1, 0.2]
    }
    xgb_grid = GridSearchCV(
        XGBClassifier(random_state=42, eval_metric='logloss'),
        xgb_param_grid,
        cv=5,
        scoring='accuracy',
        n_jobs=-1
    )
    xgb_grid.fit(X_train_scaled, y_train)
    print(f"Best parameters: {xgb_grid.best_params_}")
    print(f"Best CV score: {xgb_grid.best_score_:.4f}")
    
    return rf_grid.best_estimator_, xgb_grid.best_estimator_

def main():
    """Main function to run ML analysis"""
    # Load and prepare data
    X_train, X_test, X_train_scaled, X_test_scaled, y_train, y_test, scaler, le = load_and_prepare_data()
    
    print(f"Training set size: {X_train.shape}")
    print(f"Test set size: {X_test.shape}")
    print(f"Number of features: {X_train.shape[1]}")
    
    # Compare models
    results_dict, trained_models, comparison_df = compare_models(
        X_train_scaled, X_test_scaled, y_train, y_test
    )
    
    # Get best model
    best_model_name = comparison_df.iloc[0]['Model']
    best_model = trained_models[best_model_name]
    
    print(f"\nBest Model: {best_model_name}")
    print(f"Test Accuracy: {comparison_df.iloc[0]['Test Accuracy']:.4f}")
    
    # Detailed analysis of best model
    detailed_model_analysis(best_model_name, best_model, X_test_scaled, y_test, results_dict)
    
    # Hyperparameter tuning
    rf_tuned, xgb_tuned = hyperparameter_tuning(X_train_scaled, y_train)
    
    # Evaluate tuned models
    print("\nEvaluating tuned models...")
    rf_tuned_results = train_and_evaluate_model(
        rf_tuned, 'Random Forest (Tuned)', X_train_scaled, X_test_scaled,
        y_train, y_test, scaled=True
    )[1]
    
    xgb_tuned_results = train_and_evaluate_model(
        xgb_tuned, 'XGBoost (Tuned)', X_train_scaled, X_test_scaled,
        y_train, y_test, scaled=True
    )[1]
    
    print(f"\nRandom Forest (Tuned) - Test Accuracy: {rf_tuned_results['test_accuracy']:.4f}")
    print(f"XGBoost (Tuned) - Test Accuracy: {xgb_tuned_results['test_accuracy']:.4f}")
    
    # Save results
    comparison_df.to_csv('../../results/ml/model_comparison.csv', index=False)
    
    print("\n" + "=" * 80)
    print("ML ANALYSIS COMPLETE")
    print("All results saved to results/ml/")
    print("=" * 80)

if __name__ == "__main__":
    main()

