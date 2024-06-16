"""
Machine Learning Analysis
Predicting cardiovascular disease using various ML algorithms
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score, roc_curve
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
import warnings
warnings.filterwarnings('ignore')

sns.set_style('whitegrid')
plt.rcParams['figure.figsize'] = (14, 8)

def load_and_prepare_data():
    """Load and prepare data for machine learning"""
    df = pd.read_csv('../data/health_data.csv')
    if 'Unnamed: 0' in df.columns:
        df = df.drop('Unnamed: 0', axis=1)
    
    # Feature engineering
    df['age_years'] = df['age'] / 365.25
    df['bmi'] = df['weight'] / ((df['height'] / 100) ** 2)
    
    # Data cleaning
    df = df[(df['ap_hi'] >= 80) & (df['ap_hi'] <= 250)]
    df = df[(df['ap_lo'] >= 40) & (df['ap_lo'] <= 150)]
    df = df[df['ap_hi'] >= df['ap_lo']]
    df = df[(df['height'] >= 100) & (df['height'] <= 220)]
    df = df[(df['weight'] >= 30) & (df['weight'] <= 200)]
    df = df[(df['bmi'] >= 10) & (df['bmi'] <= 60)]
    
    # Select features
    feature_cols = ['age_years', 'gender', 'height', 'weight', 'ap_hi', 'ap_lo', 
                    'cholesterol', 'gluc', 'smoke', 'alco', 'active', 'bmi']
    X = df[feature_cols]
    y = df['cardio']
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    return X_train, X_test, X_train_scaled, X_test_scaled, y_train, y_test, feature_cols

def train_models(X_train, X_test, X_train_scaled, X_test_scaled, y_train, y_test):
    """Train multiple ML models and compare performance"""
    print("=" * 80)
    print("MACHINE LEARNING MODEL TRAINING")
    print("=" * 80)
    
    models = {
        'Logistic Regression': LogisticRegression(random_state=42, max_iter=1000),
        'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1),
        'Gradient Boosting': GradientBoostingClassifier(n_estimators=100, random_state=42),
        'XGBoost': XGBClassifier(random_state=42, eval_metric='logloss'),
        'LightGBM': LGBMClassifier(random_state=42, verbose=-1),
        'SVM': SVC(probability=True, random_state=42)
    }
    
    results = {}
    
    for name, model in models.items():
        print(f"\nTraining {name}...")
        
        # Use scaled data for Logistic Regression and SVM
        if name in ['Logistic Regression', 'SVM']:
            model.fit(X_train_scaled, y_train)
            y_pred = model.predict(X_test_scaled)
            y_pred_proba = model.predict_proba(X_test_scaled)[:, 1]
            # Cross validation on scaled data
            cv_scores = cross_val_score(model, X_train_scaled, y_train, cv=5, scoring='roc_auc')
        else:
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
            y_pred_proba = model.predict_proba(X_test)[:, 1]
            # Cross validation on original data
            cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring='roc_auc')
        
        # Calculate metrics
        roc_auc = roc_auc_score(y_test, y_pred_proba)
        
        results[name] = {
            'model': model,
            'y_pred': y_pred,
            'y_pred_proba': y_pred_proba,
            'roc_auc': roc_auc,
            'cv_mean': cv_scores.mean(),
            'cv_std': cv_scores.std()
        }
        
        print(f"  ROC-AUC: {roc_auc:.4f}")
        print(f"  CV ROC-AUC: {cv_scores.mean():.4f} (+/- {cv_scores.std() * 2:.4f})")
    
    return results

def evaluate_models(results, y_test):
    """Evaluate and visualize model performance"""
    print("=" * 80)
    print("MODEL EVALUATION")
    print("=" * 80)
    
    # Classification reports
    for name, result in results.items():
        print(f"\n{name} - Classification Report:")
        print(classification_report(y_test, result['y_pred']))
    
    # ROC curves
    plt.figure(figsize=(12, 8))
    for name, result in results.items():
        fpr, tpr, _ = roc_curve(y_test, result['y_pred_proba'])
        plt.plot(fpr, tpr, label=f'{name} (AUC = {result["roc_auc"]:.4f})', linewidth=2)
    
    plt.plot([0, 1], [0, 1], 'k--', linewidth=1, label='Random')
    plt.xlabel('False Positive Rate', fontsize=12)
    plt.ylabel('True Positive Rate', fontsize=12)
    plt.title('ROC Curves - Model Comparison', fontsize=14, fontweight='bold')
    plt.legend(loc='lower right', fontsize=10)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('../figures/roc_curves.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # Confusion matrices
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    axes = axes.ravel()
    
    for i, (name, result) in enumerate(results.items()):
        cm = confusion_matrix(y_test, result['y_pred'])
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=axes[i], cbar=False)
        axes[i].set_title(f'{name}\nROC-AUC: {result["roc_auc"]:.4f}', fontsize=11, fontweight='bold')
        axes[i].set_xlabel('Predicted')
        axes[i].set_ylabel('Actual')
    
    plt.tight_layout()
    plt.savefig('../figures/confusion_matrices.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # Model comparison
    comparison_df = pd.DataFrame({
        'Model': list(results.keys()),
        'ROC-AUC': [r['roc_auc'] for r in results.values()],
        'CV Mean': [r['cv_mean'] for r in results.values()],
        'CV Std': [r['cv_std'] for r in results.values()]
    }).sort_values('ROC-AUC', ascending=False)
    
    print("\n" + "=" * 80)
    print("MODEL COMPARISON")
    print("=" * 80)
    print(comparison_df.to_string(index=False))
    
    # Bar plot
    plt.figure(figsize=(12, 6))
    plt.barh(comparison_df['Model'], comparison_df['ROC-AUC'], color='steelblue', edgecolor='black')
    plt.xlabel('ROC-AUC Score', fontsize=12)
    plt.ylabel('Model', fontsize=12)
    plt.title('Model Performance Comparison', fontsize=14, fontweight='bold')
    plt.xlim(0.5, 1.0)
    for i, v in enumerate(comparison_df['ROC-AUC']):
        plt.text(v + 0.01, i, f'{v:.4f}', va='center', fontweight='bold')
    plt.grid(True, alpha=0.3, axis='x')
    plt.tight_layout()
    plt.savefig('../figures/model_comparison.png', dpi=300, bbox_inches='tight')
    plt.close()

def feature_importance_analysis(results, feature_cols, X_train):
    """Analyze and visualize feature importance"""
    print("=" * 80)
    print("FEATURE IMPORTANCE ANALYSIS")
    print("=" * 80)
    
    # Get feature importance from tree-based models
    tree_models = ['Random Forest', 'Gradient Boosting', 'XGBoost', 'LightGBM']
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    axes = axes.ravel()
    
    for i, name in enumerate(tree_models):
        if name in results:
            model = results[name]['model']
            if hasattr(model, 'feature_importances_'):
                importances = model.feature_importances_
                indices = np.argsort(importances)[::-1]
                
                axes[i].barh(range(len(feature_cols)), importances[indices], color='steelblue', edgecolor='black')
                axes[i].set_yticks(range(len(feature_cols)))
                axes[i].set_yticklabels([feature_cols[j] for j in indices])
                axes[i].set_xlabel('Importance', fontsize=10)
                axes[i].set_title(f'{name} - Feature Importance', fontsize=12, fontweight='bold')
                axes[i].grid(True, alpha=0.3, axis='x')
    
    plt.tight_layout()
    plt.savefig('../figures/feature_importance.png', dpi=300, bbox_inches='tight')
    plt.close()

def hyperparameter_tuning(X_train, y_train):
    """Perform hyperparameter tuning for best model"""
    print("=" * 80)
    print("HYPERPARAMETER TUNING")
    print("=" * 80)
    
    # Tune Random Forest
    print("\nTuning Random Forest...")
    param_grid_rf = {
        'n_estimators': [100, 200, 300],
        'max_depth': [10, 20, None],
        'min_samples_split': [2, 5, 10]
    }
    
    rf = RandomForestClassifier(random_state=42, n_jobs=-1)
    grid_search_rf = GridSearchCV(rf, param_grid_rf, cv=5, scoring='roc_auc', n_jobs=-1, verbose=1)
    grid_search_rf.fit(X_train, y_train)
    
    print(f"Best parameters: {grid_search_rf.best_params_}")
    print(f"Best CV score: {grid_search_rf.best_score_:.4f}")
    
    return grid_search_rf.best_estimator_

if __name__ == "__main__":
    X_train, X_test, X_train_scaled, X_test_scaled, y_train, y_test, feature_cols = load_and_prepare_data()
    
    print(f"Training set size: {X_train.shape}")
    print(f"Test set size: {X_test.shape}")
    print(f"Features: {feature_cols}")
    
    results = train_models(X_train, X_test, X_train_scaled, X_test_scaled, y_train, y_test)
    evaluate_models(results, y_test)
    feature_importance_analysis(results, feature_cols, X_train)
    
    # Hyperparameter tuning
    best_model = hyperparameter_tuning(X_train, y_train)
    print(f"\nBest model: {best_model}")
    
    print("\nMachine Learning Analysis completed successfully!")

