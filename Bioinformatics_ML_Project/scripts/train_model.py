"""
Script to train a specific model with custom parameters.

Usage:
    python scripts/train_model.py --model rf --n_estimators 100 --max_depth 10
"""

import sys
import os
import argparse

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.data_processing import generate_synthetic_data, preprocess_data, load_clinical_data
from src.models import (train_random_forest, train_svm, train_gradient_boosting,
                       train_neural_network, save_model, cross_validate_model)
from src.evaluation import generate_evaluation_report


def main():
    parser = argparse.ArgumentParser(description='Train a specific ML model')
    
    # Model selection
    parser.add_argument('--model', type=str, required=True,
                       choices=['rf', 'svm', 'gb', 'nn'],
                       help='Model to train: rf (Random Forest), svm (SVM), gb (Gradient Boosting), nn (Neural Network)')
    
    # Data options
    parser.add_argument('--data', type=str, help='Path to data file')
    parser.add_argument('--n_samples', type=int, default=1000,
                       help='Number of synthetic samples if no data provided')
    
    # Random Forest parameters
    parser.add_argument('--n_estimators', type=int, default=100,
                       help='Number of trees (RF, GB)')
    parser.add_argument('--max_depth', type=int, default=10,
                       help='Maximum depth of trees (RF, GB)')
    
    # SVM parameters
    parser.add_argument('--kernel', type=str, default='rbf',
                       choices=['linear', 'poly', 'rbf', 'sigmoid'],
                       help='SVM kernel type')
    parser.add_argument('--C', type=float, default=1.0,
                       help='SVM regularization parameter')
    
    # Neural Network parameters
    parser.add_argument('--hidden_layers', type=int, nargs='+',
                       default=[100, 50],
                       help='Hidden layer sizes for Neural Network')
    
    # General options
    parser.add_argument('--cv', type=int, default=5,
                       help='Number of cross-validation folds')
    parser.add_argument('--output', type=str, default='results/models',
                       help='Output directory for saved model')
    
    args = parser.parse_args()
    
    print("=" * 70)
    print("MODEL TRAINING SCRIPT")
    print("=" * 70)
    
    # Load or generate data
    print("\n--- Loading Data ---")
    if args.data:
        df = load_clinical_data(args.data)
    else:
        df = generate_synthetic_data(n_samples=args.n_samples)
    
    # Preprocess
    print("\n--- Preprocessing Data ---")
    X_train, X_test, y_train, y_test, scaler = preprocess_data(df)
    
    # Train model
    print("\n--- Training Model ---")
    model_name = {
        'rf': 'Random Forest',
        'svm': 'SVM',
        'gb': 'Gradient Boosting',
        'nn': 'Neural Network'
    }[args.model]
    
    if args.model == 'rf':
        model = train_random_forest(
            X_train, y_train,
            n_estimators=args.n_estimators,
            max_depth=args.max_depth
        )
    elif args.model == 'svm':
        model = train_svm(
            X_train, y_train,
            kernel=args.kernel,
            C=args.C
        )
    elif args.model == 'gb':
        model = train_gradient_boosting(
            X_train, y_train,
            n_estimators=args.n_estimators,
            max_depth=args.max_depth
        )
    elif args.model == 'nn':
        model = train_neural_network(
            X_train, y_train,
            hidden_layer_sizes=tuple(args.hidden_layers)
        )
    
    # Cross-validation
    print("\n--- Cross-Validation ---")
    cv_results = cross_validate_model(model, X_train, y_train, cv=args.cv)
    
    # Evaluation
    print("\n--- Model Evaluation ---")
    generate_evaluation_report(model, X_test, y_test, model_name)
    
    # Save model
    print("\n--- Saving Model ---")
    os.makedirs(args.output, exist_ok=True)
    model_path = f'{args.output}/{args.model}_model.pkl'
    save_model(model, model_path)
    
    print("\n" + "=" * 70)
    print("TRAINING COMPLETE!")
    print("=" * 70)
    print(f"Model saved to: {model_path}")


if __name__ == "__main__":
    main()


