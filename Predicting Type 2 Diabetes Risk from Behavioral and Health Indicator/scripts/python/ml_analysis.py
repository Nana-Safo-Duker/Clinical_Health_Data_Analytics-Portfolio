"""
Machine Learning Analysis
Diabetes Binary Health Indicators - BRFSS 2021
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score, roc_curve
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import warnings
warnings.filterwarnings('ignore')

# Set style
sns.set_style('whitegrid')
plt.rcParams['figure.figsize'] = (12, 8)

def load_data():
    """Load and prepare data"""
    df = pd.read_csv('../../data/diabetes_binary_health_indicators_BRFSS2021.csv')
    return df

def prepare_data(df):
    """Prepare data for machine learning"""
    # Separate features and target
    X = df.drop('Diabetes_binary', axis=1)
    y = df['Diabetes_binary']
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    return X_train, X_test, X_train_scaled, X_test_scaled, y_train, y_test, scaler

def train_models(X_train, X_test, X_train_scaled, X_test_scaled, y_train, y_test):
    """Train multiple machine learning models"""
    print("=" * 60)
    print("TRAINING MACHINE LEARNING MODELS")
    print("=" * 60)
    
    models = {
        'Logistic Regression': LogisticRegression(random_state=42, max_iter=1000),
        'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1),
        'Gradient Boosting': GradientBoostingClassifier(n_estimators=100, random_state=42),
        'SVM': SVC(probability=True, random_state=42)
    }
    
    results = {}
    
    for name, model in models.items():
        print(f"\n{'='*60}")
        print(f"Training {name}")
        print(f"{'='*60}")
        
        # Use scaled data for Logistic Regression and SVM
        if name in ['Logistic Regression', 'SVM']:
            model.fit(X_train_scaled, y_train)
            y_pred = model.predict(X_test_scaled)
            y_pred_proba = model.predict_proba(X_test_scaled)[:, 1]
        else:
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
            y_pred_proba = model.predict_proba(X_test)[:, 1]
        
        # Calculate metrics
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred)
        recall = recall_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)
        auc = roc_auc_score(y_test, y_pred_proba)
        
        results[name] = {
            'model': model,
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1': f1,
            'auc': auc,
            'y_pred': y_pred,
            'y_pred_proba': y_pred_proba
        }
        
        print(f"Accuracy: {accuracy:.4f}")
        print(f"Precision: {precision:.4f}")
        print(f"Recall: {recall:.4f}")
        print(f"F1 Score: {f1:.4f}")
        print(f"AUC-ROC: {auc:.4f}")
        
        # Classification report
        print(f"\nClassification Report:")
        print(classification_report(y_test, y_pred))
    
    return results

def plot_results(results, y_test, output_dir='../../results/figures/'):
    """Plot model results"""
    # ROC Curves
    plt.figure(figsize=(10, 8))
    for name, result in results.items():
        fpr, tpr, _ = roc_curve(y_test, result['y_pred_proba'])
        plt.plot(fpr, tpr, label=f"{name} (AUC = {result['auc']:.3f})")
    
    plt.plot([0, 1], [0, 1], 'k--', label='Random')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('ROC Curves - Model Comparison', fontsize=14, fontweight='bold')
    plt.legend(loc="lower right")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(f'{output_dir}roc_curves.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # Model comparison
    metrics_df = pd.DataFrame({
        name: {
            'Accuracy': result['accuracy'],
            'Precision': result['precision'],
            'Recall': result['recall'],
            'F1 Score': result['f1'],
            'AUC-ROC': result['auc']
        }
        for name, result in results.items()
    }).T
    
    # Visualization
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    metrics_df[['Accuracy', 'Precision', 'Recall', 'F1 Score']].plot(kind='bar', ax=axes[0])
    axes[0].set_title('Model Performance Metrics', fontsize=12, fontweight='bold')
    axes[0].set_ylabel('Score')
    axes[0].set_xlabel('Model')
    axes[0].legend(loc='upper right')
    axes[0].tick_params(axis='x', rotation=45)
    axes[0].grid(True, alpha=0.3, axis='y')
    
    metrics_df['AUC-ROC'].plot(kind='bar', ax=axes[1], color='steelblue')
    axes[1].set_title('AUC-ROC Scores', fontsize=12, fontweight='bold')
    axes[1].set_ylabel('AUC-ROC')
    axes[1].set_xlabel('Model')
    axes[1].tick_params(axis='x', rotation=45)
    axes[1].grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}model_comparison.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    return metrics_df

def feature_importance_analysis(results, X_train, output_dir='../../results/figures/'):
    """Analyze feature importance for tree-based models"""
    print("=" * 60)
    print("FEATURE IMPORTANCE ANALYSIS")
    print("=" * 60)
    
    # Random Forest feature importance
    if 'Random Forest' in results:
        rf_model = results['Random Forest']['model']
        feature_importance = pd.DataFrame({
            'feature': X_train.columns,
            'importance': rf_model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        print("\nTop 10 Most Important Features (Random Forest):")
        print(feature_importance.head(10))
        
        # Visualization
        plt.figure(figsize=(10, 8))
        top_features = feature_importance.head(15)
        plt.barh(range(len(top_features)), top_features['importance'], color='steelblue')
        plt.yticks(range(len(top_features)), top_features['feature'])
        plt.xlabel('Importance')
        plt.title('Top 15 Feature Importance (Random Forest)', fontsize=14, fontweight='bold')
        plt.gca().invert_yaxis()
        plt.tight_layout()
        plt.savefig(f'{output_dir}feature_importance_rf.png', dpi=300, bbox_inches='tight')
        plt.close()
    
    # Gradient Boosting feature importance
    if 'Gradient Boosting' in results:
        gb_model = results['Gradient Boosting']['model']
        feature_importance_gb = pd.DataFrame({
            'feature': X_train.columns,
            'importance': gb_model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        print("\nTop 10 Most Important Features (Gradient Boosting):")
        print(feature_importance_gb.head(10))
        
        # Visualization
        plt.figure(figsize=(10, 8))
        top_features_gb = feature_importance_gb.head(15)
        plt.barh(range(len(top_features_gb)), top_features_gb['importance'], color='salmon')
        plt.yticks(range(len(top_features_gb)), top_features_gb['feature'])
        plt.xlabel('Importance')
        plt.title('Top 15 Feature Importance (Gradient Boosting)', fontsize=14, fontweight='bold')
        plt.gca().invert_yaxis()
        plt.tight_layout()
        plt.savefig(f'{output_dir}feature_importance_gb.png', dpi=300, bbox_inches='tight')
        plt.close()

def confusion_matrix_plots(results, y_test, output_dir='../../results/figures/'):
    """Plot confusion matrices for all models"""
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    axes = axes.ravel()
    
    for idx, (name, result) in enumerate(results.items()):
        cm = confusion_matrix(y_test, result['y_pred'])
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=axes[idx])
        axes[idx].set_title(f'Confusion Matrix - {name}', fontsize=12, fontweight='bold')
        axes[idx].set_ylabel('True Label')
        axes[idx].set_xlabel('Predicted Label')
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}confusion_matrices.png', dpi=300, bbox_inches='tight')
    plt.close()

def main():
    """Main function"""
    # Load data
    df = load_data()
    print(f"Dataset shape: {df.shape}")
    
    # Prepare data
    X_train, X_test, X_train_scaled, X_test_scaled, y_train, y_test, scaler = prepare_data(df)
    
    # Train models
    results = train_models(X_train, X_test, X_train_scaled, X_test_scaled, y_train, y_test)
    
    # Plot results
    metrics_df = plot_results(results, y_test)
    
    # Feature importance
    feature_importance_analysis(results, X_train)
    
    # Confusion matrices
    confusion_matrix_plots(results, y_test)
    
    # Save results
    metrics_df.to_csv('../../results/models/model_performance.csv')
    
    print("\n" + "=" * 60)
    print("MACHINE LEARNING ANALYSIS COMPLETE")
    print("=" * 60)
    print("\nBest Model (by AUC-ROC):")
    best_model = metrics_df['AUC-ROC'].idxmax()
    print(f"{best_model}: {metrics_df.loc[best_model, 'AUC-ROC']:.4f}")

if __name__ == "__main__":
    main()

