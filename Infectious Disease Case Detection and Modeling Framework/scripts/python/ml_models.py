"""
Machine Learning Analysis Module
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import xgboost as xgb
import lightgbm as lgb
import warnings
warnings.filterwarnings('ignore')

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from data_loader import load_data, clean_data

def prepare_ml_data(df_clean, target='Incidence_Rate'):
    """
    Prepare data for machine learning
    
    Parameters:
    -----------
    df_clean : DataFrame
        Cleaned dataset
    target : str
        Target variable
    """
    # Select features
    feature_cols = ['CI_Lower', 'CI_Upper', 'Annual_Count', 'Trend_5yr', 'FIPS']
    feature_cols = [col for col in feature_cols if col in df_clean.columns]
    
    # Handle categorical variables
    if 'Trend' in df_clean.columns:
        le = LabelEncoder()
        df_clean['Trend_encoded'] = le.fit_transform(df_clean['Trend'].astype(str))
        feature_cols.append('Trend_encoded')
    
    # Create feature matrix and target vector
    X = df_clean[feature_cols].dropna()
    y = df_clean.loc[X.index, target]
    
    # Remove rows with missing target
    mask = ~y.isna()
    X = X[mask]
    y = y[mask]
    
    # Scale features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y, test_size=0.2, random_state=42
    )
    
    return X_train, X_test, y_train, y_test, scaler, feature_cols

def train_and_evaluate_models(X_train, X_test, y_train, y_test):
    """
    Train and evaluate multiple ML models
    
    Parameters:
    -----------
    X_train : array
        Training features
    X_test : array
        Test features
    y_train : array
        Training target
    y_test : array
        Test target
    """
    models = {
        'Linear Regression': LinearRegression(),
        'Ridge Regression': Ridge(alpha=1.0),
        'Lasso Regression': Lasso(alpha=1.0),
        'Elastic Net': ElasticNet(alpha=1.0, l1_ratio=0.5),
        'Random Forest': RandomForestRegressor(n_estimators=100, random_state=42),
        'Gradient Boosting': GradientBoostingRegressor(n_estimators=100, random_state=42),
        'XGBoost': xgb.XGBRegressor(random_state=42),
        'LightGBM': lgb.LGBMRegressor(random_state=42, verbosity=-1)
    }
    
    results = {}
    
    print("=== MACHINE LEARNING MODEL EVALUATION ===\n")
    
    for name, model in models.items():
        print(f"Training {name}...")
        
        # Train model
        model.fit(X_train, y_train)
        
        # Predictions
        y_pred_train = model.predict(X_train)
        y_pred_test = model.predict(X_test)
        
        # Metrics
        train_rmse = np.sqrt(mean_squared_error(y_train, y_pred_train))
        test_rmse = np.sqrt(mean_squared_error(y_test, y_pred_test))
        train_mae = mean_absolute_error(y_train, y_pred_train)
        test_mae = mean_absolute_error(y_test, y_pred_test)
        train_r2 = r2_score(y_train, y_pred_train)
        test_r2 = r2_score(y_test, y_pred_test)
        
        # Cross-validation
        cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring='r2')
        
        results[name] = {
            'model': model,
            'train_rmse': train_rmse,
            'test_rmse': test_rmse,
            'train_mae': train_mae,
            'test_mae': test_mae,
            'train_r2': train_r2,
            'test_r2': test_r2,
            'cv_mean': cv_scores.mean(),
            'cv_std': cv_scores.std()
        }
        
        print(f"  Train RMSE: {train_rmse:.4f}, Test RMSE: {test_rmse:.4f}")
        print(f"  Train R²: {train_r2:.4f}, Test R²: {test_r2:.4f}")
        print(f"  CV R²: {cv_scores.mean():.4f} (±{cv_scores.std():.4f})")
        print()
    
    return results

def plot_model_comparison(results):
    """Plot model comparison"""
    model_names = list(results.keys())
    test_r2_scores = [results[name]['test_r2'] for name in model_names]
    test_rmse_scores = [results[name]['test_rmse'] for name in model_names]
    
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))
    
    # R² scores
    axes[0].barh(model_names, test_r2_scores)
    axes[0].set_xlabel('R² Score')
    axes[0].set_title('Model Comparison: R² Score')
    axes[0].grid(axis='x', alpha=0.3)
    
    # RMSE scores
    axes[1].barh(model_names, test_rmse_scores)
    axes[1].set_xlabel('RMSE')
    axes[1].set_title('Model Comparison: RMSE')
    axes[1].grid(axis='x', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('ml_model_comparison.png', dpi=300, bbox_inches='tight')
    plt.show()

def feature_importance_analysis(model, feature_names):
    """Analyze feature importance"""
    if hasattr(model, 'feature_importances_'):
        importances = model.feature_importances_
    elif hasattr(model, 'coef_'):
        importances = np.abs(model.coef_)
    else:
        print("Model does not support feature importance")
        return
    
    # Create DataFrame
    importance_df = pd.DataFrame({
        'Feature': feature_names,
        'Importance': importances
    }).sort_values('Importance', ascending=False)
    
    # Plot
    plt.figure(figsize=(10, 6))
    plt.barh(importance_df['Feature'], importance_df['Importance'])
    plt.xlabel('Importance')
    plt.title('Feature Importance')
    plt.tight_layout()
    plt.savefig('ml_feature_importance.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    return importance_df

def hyperparameter_tuning(X_train, y_train, model_type='random_forest'):
    """Perform hyperparameter tuning"""
    print(f"\n=== HYPERPARAMETER TUNING: {model_type.upper()} ===\n")
    
    if model_type == 'random_forest':
        model = RandomForestRegressor(random_state=42)
        param_grid = {
            'n_estimators': [50, 100, 200],
            'max_depth': [10, 20, None],
            'min_samples_split': [2, 5, 10]
        }
    elif model_type == 'xgboost':
        model = xgb.XGBRegressor(random_state=42)
        param_grid = {
            'n_estimators': [50, 100, 200],
            'max_depth': [3, 5, 7],
            'learning_rate': [0.01, 0.1, 0.2]
        }
    else:
        print("Model type not supported for tuning")
        return None
    
    grid_search = GridSearchCV(
        model, param_grid, cv=5, scoring='r2', n_jobs=-1, verbose=1
    )
    grid_search.fit(X_train, y_train)
    
    print(f"Best parameters: {grid_search.best_params_}")
    print(f"Best CV score: {grid_search.best_score_:.4f}")
    
    return grid_search.best_estimator_

if __name__ == "__main__":
    # Load and prepare data
    df = load_data()
    df_clean = clean_data(df)
    
    X_train, X_test, y_train, y_test, scaler, feature_cols = prepare_ml_data(df_clean)
    
    print(f"Training set size: {X_train.shape}")
    print(f"Test set size: {X_test.shape}")
    print(f"Features: {feature_cols}\n")
    
    # Train and evaluate models
    results = train_and_evaluate_models(X_train, X_test, y_train, y_test)
    
    # Plot comparison
    plot_model_comparison(results)
    
    # Feature importance for best model
    best_model_name = max(results.keys(), key=lambda x: results[x]['test_r2'])
    best_model = results[best_model_name]['model']
    print(f"\nBest Model: {best_model_name}")
    importance_df = feature_importance_analysis(best_model, feature_cols)
    print("\nFeature Importance:")
    print(importance_df)
    
    # Hyperparameter tuning
    tuned_model = hyperparameter_tuning(X_train, y_train, 'random_forest')

