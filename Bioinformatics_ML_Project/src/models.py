"""
Machine Learning Models Module

Implementations of various ML algorithms for clinical diagnosis.
"""

import numpy as np
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import cross_val_score, GridSearchCV
from sklearn.metrics import make_scorer, f1_score
import joblib


def train_random_forest(X_train, y_train, **kwargs):
    """
    Train a Random Forest classifier.
    
    Parameters:
    -----------
    X_train : np.ndarray
        Training features
    y_train : np.ndarray
        Training labels
    **kwargs : dict
        Additional parameters for RandomForestClassifier
        
    Returns:
    --------
    model : RandomForestClassifier
        Trained model
        
    Example:
    --------
    >>> model = train_random_forest(X_train, y_train, n_estimators=100)
    """
    default_params = {
        'n_estimators': 100,
        'max_depth': 10,
        'min_samples_split': 5,
        'min_samples_leaf': 2,
        'random_state': 42,
        'n_jobs': -1
    }
    
    # Update with user params
    default_params.update(kwargs)
    
    print(f"Training Random Forest with params: {default_params}")
    
    model = RandomForestClassifier(**default_params)
    model.fit(X_train, y_train)
    
    # Calculate training score
    train_score = model.score(X_train, y_train)
    print(f"✓ Random Forest trained successfully")
    print(f"  Training accuracy: {train_score:.4f}")
    
    return model


def train_svm(X_train, y_train, **kwargs):
    """
    Train a Support Vector Machine classifier.
    
    Parameters:
    -----------
    X_train : np.ndarray
        Training features
    y_train : np.ndarray
        Training labels
    **kwargs : dict
        Additional parameters for SVC
        
    Returns:
    --------
    model : SVC
        Trained model
        
    Example:
    --------
    >>> model = train_svm(X_train, y_train, kernel='rbf')
    """
    default_params = {
        'kernel': 'rbf',
        'C': 1.0,
        'gamma': 'scale',
        'probability': True,
        'random_state': 42
    }
    
    default_params.update(kwargs)
    
    print(f"Training SVM with params: {default_params}")
    
    model = SVC(**default_params)
    model.fit(X_train, y_train)
    
    train_score = model.score(X_train, y_train)
    print(f"✓ SVM trained successfully")
    print(f"  Training accuracy: {train_score:.4f}")
    
    return model


def train_gradient_boosting(X_train, y_train, **kwargs):
    """
    Train a Gradient Boosting classifier.
    
    Parameters:
    -----------
    X_train : np.ndarray
        Training features
    y_train : np.ndarray
        Training labels
    **kwargs : dict
        Additional parameters for GradientBoostingClassifier
        
    Returns:
    --------
    model : GradientBoostingClassifier
        Trained model
        
    Example:
    --------
    >>> model = train_gradient_boosting(X_train, y_train, n_estimators=100)
    """
    default_params = {
        'n_estimators': 100,
        'learning_rate': 0.1,
        'max_depth': 3,
        'min_samples_split': 5,
        'min_samples_leaf': 2,
        'random_state': 42
    }
    
    default_params.update(kwargs)
    
    print(f"Training Gradient Boosting with params: {default_params}")
    
    model = GradientBoostingClassifier(**default_params)
    model.fit(X_train, y_train)
    
    train_score = model.score(X_train, y_train)
    print(f"✓ Gradient Boosting trained successfully")
    print(f"  Training accuracy: {train_score:.4f}")
    
    return model


def train_neural_network(X_train, y_train, **kwargs):
    """
    Train a Multi-layer Perceptron (Neural Network) classifier.
    
    Parameters:
    -----------
    X_train : np.ndarray
        Training features
    y_train : np.ndarray
        Training labels
    **kwargs : dict
        Additional parameters for MLPClassifier
        
    Returns:
    --------
    model : MLPClassifier
        Trained model
        
    Example:
    --------
    >>> model = train_neural_network(X_train, y_train, hidden_layer_sizes=(100, 50))
    """
    default_params = {
        'hidden_layer_sizes': (100, 50),
        'activation': 'relu',
        'solver': 'adam',
        'alpha': 0.0001,
        'max_iter': 500,
        'random_state': 42
    }
    
    default_params.update(kwargs)
    
    print(f"Training Neural Network with params: {default_params}")
    
    model = MLPClassifier(**default_params)
    model.fit(X_train, y_train)
    
    train_score = model.score(X_train, y_train)
    print(f"✓ Neural Network trained successfully")
    print(f"  Training accuracy: {train_score:.4f}")
    
    return model


def cross_validate_model(model, X, y, cv=5, scoring='accuracy'):
    """
    Perform cross-validation on a model.
    
    Parameters:
    -----------
    model : sklearn model
        Model to validate
    X : np.ndarray
        Feature matrix
    y : np.ndarray
        Labels
    cv : int, default=5
        Number of cross-validation folds
    scoring : str or callable, default='accuracy'
        Scoring metric
        
    Returns:
    --------
    scores : dict
        Dictionary with mean, std, and all scores
        
    Example:
    --------
    >>> results = cross_validate_model(model, X_train, y_train, cv=5)
    """
    print(f"\nPerforming {cv}-fold cross-validation...")
    
    scores = cross_val_score(model, X, y, cv=cv, scoring=scoring)
    
    results = {
        'mean': scores.mean(),
        'std': scores.std(),
        'scores': scores
    }
    
    print(f"✓ Cross-validation complete")
    print(f"  Mean {scoring}: {results['mean']:.4f} ± {results['std']:.4f}")
    print(f"  Individual scores: {[f'{s:.4f}' for s in scores]}")
    
    return results


def tune_hyperparameters(model_class, param_grid, X_train, y_train, cv=5):
    """
    Perform hyperparameter tuning using GridSearchCV.
    
    Parameters:
    -----------
    model_class : sklearn model class
        Model class to tune
    param_grid : dict
        Dictionary of parameters to search
    X_train : np.ndarray
        Training features
    y_train : np.ndarray
        Training labels
    cv : int, default=5
        Number of cross-validation folds
        
    Returns:
    --------
    best_model : sklearn model
        Best model found
    best_params : dict
        Best parameters
    results : dict
        GridSearch results
        
    Example:
    --------
    >>> param_grid = {'n_estimators': [50, 100], 'max_depth': [5, 10]}
    >>> best_model, params, results = tune_hyperparameters(
    ...     RandomForestClassifier, param_grid, X_train, y_train
    ... )
    """
    print(f"\nTuning hyperparameters...")
    print(f"Parameter grid: {param_grid}")
    
    grid_search = GridSearchCV(
        model_class(),
        param_grid,
        cv=cv,
        scoring='f1',
        n_jobs=-1,
        verbose=1
    )
    
    grid_search.fit(X_train, y_train)
    
    print(f"\n✓ Hyperparameter tuning complete")
    print(f"  Best score: {grid_search.best_score_:.4f}")
    print(f"  Best parameters: {grid_search.best_params_}")
    
    return grid_search.best_estimator_, grid_search.best_params_, grid_search.cv_results_


def save_model(model, filepath):
    """
    Save a trained model to disk.
    
    Parameters:
    -----------
    model : sklearn model
        Trained model to save
    filepath : str
        Path where to save the model
        
    Example:
    --------
    >>> save_model(model, 'results/models/random_forest.pkl')
    """
    joblib.dump(model, filepath)
    print(f"✓ Model saved to {filepath}")


def load_model(filepath):
    """
    Load a trained model from disk.
    
    Parameters:
    -----------
    filepath : str
        Path to the saved model
        
    Returns:
    --------
    model : sklearn model
        Loaded model
        
    Example:
    --------
    >>> model = load_model('results/models/random_forest.pkl')
    """
    model = joblib.load(filepath)
    print(f"✓ Model loaded from {filepath}")
    return model


def get_feature_importance(model, feature_names=None, top_n=10):
    """
    Extract and display feature importance from a trained model.
    
    Parameters:
    -----------
    model : sklearn model
        Trained model with feature_importances_ attribute
    feature_names : list, optional
        Names of features
    top_n : int, default=10
        Number of top features to display
        
    Returns:
    --------
    importance_df : pd.DataFrame
        DataFrame with feature names and importances
        
    Example:
    --------
    >>> importance = get_feature_importance(model, feature_names=['age', 'bmi'])
    """
    import pandas as pd
    
    if not hasattr(model, 'feature_importances_'):
        print("✗ Model does not have feature_importances_ attribute")
        return None
    
    importances = model.feature_importances_
    
    if feature_names is None:
        feature_names = [f'Feature_{i}' for i in range(len(importances))]
    
    importance_df = pd.DataFrame({
        'Feature': feature_names,
        'Importance': importances
    }).sort_values('Importance', ascending=False)
    
    print(f"\nTop {top_n} most important features:")
    print("=" * 50)
    for idx, row in importance_df.head(top_n).iterrows():
        print(f"{row['Feature']:30s} : {row['Importance']:.4f}")
    
    return importance_df


if __name__ == "__main__":
    # Example usage
    from data_processing import generate_synthetic_data, preprocess_data
    
    print("Machine Learning Models Module - Example Usage\n")
    
    # Generate and preprocess data
    df = generate_synthetic_data(n_samples=1000)
    X_train, X_test, y_train, y_test, _ = preprocess_data(df)
    
    # Train Random Forest
    print("\n" + "=" * 60)
    rf_model = train_random_forest(X_train, y_train, n_estimators=50)
    
    # Cross-validate
    rf_cv = cross_validate_model(rf_model, X_train, y_train, cv=5)
    
    # Get feature importance
    feature_names = ['age', 'bmi', 'blood_pressure_sys', 'blood_pressure_dia',
                     'glucose', 'cholesterol', 'heart_rate', 'biomarker_a', 'biomarker_b']
    importance = get_feature_importance(rf_model, feature_names, top_n=5)


