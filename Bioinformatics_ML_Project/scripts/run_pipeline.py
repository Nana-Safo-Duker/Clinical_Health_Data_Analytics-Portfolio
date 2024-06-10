"""
Complete ML Pipeline Script

This script runs the entire machine learning pipeline from data loading
to model training and evaluation.

Usage:
    python scripts/run_pipeline.py
"""

import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.data_processing import generate_synthetic_data, preprocess_data
from src.models import (train_random_forest, train_svm, train_gradient_boosting,
                       cross_validate_model, save_model)
from src.evaluation import evaluate_model, compare_models, generate_evaluation_report
from src.visualization import (plot_roc_curve, plot_feature_importance, 
                               plot_confusion_matrix, plot_multiple_roc_curves)
import argparse


def main():
    """
    Main pipeline function.
    """
    print("=" * 80)
    print("MACHINE LEARNING PIPELINE FOR CLINICAL DIAGNOSIS")
    print("=" * 80)
    
    # Parse arguments
    parser = argparse.ArgumentParser(description='Run ML pipeline for clinical diagnosis')
    parser.add_argument('--data', type=str, help='Path to data file (optional)')
    parser.add_argument('--n_samples', type=int, default=1000, 
                       help='Number of synthetic samples if no data provided')
    parser.add_argument('--models', type=str, nargs='+', 
                       default=['rf', 'svm', 'gb'],
                       help='Models to train: rf, svm, gb, nn')
    parser.add_argument('--output', type=str, default='results',
                       help='Output directory for results')
    
    args = parser.parse_args()
    
    # Step 1: Load/Generate Data
    print("\n" + "=" * 80)
    print("STEP 1: DATA LOADING")
    print("=" * 80)
    
    if args.data:
        from src.data_processing import load_clinical_data
        df = load_clinical_data(args.data)
    else:
        print(f"Generating synthetic data with {args.n_samples} samples...")
        df = generate_synthetic_data(n_samples=args.n_samples)
    
    print(f"Dataset shape: {df.shape}")
    
    # Step 2: Preprocessing
    print("\n" + "=" * 80)
    print("STEP 2: DATA PREPROCESSING")
    print("=" * 80)
    
    X_train, X_test, y_train, y_test, scaler = preprocess_data(
        df, 
        target_column='diagnosis',
        test_size=0.2,
        scale=True
    )
    
    # Step 3: Model Training
    print("\n" + "=" * 80)
    print("STEP 3: MODEL TRAINING")
    print("=" * 80)
    
    models = {}
    
    if 'rf' in args.models:
        print("\n--- Training Random Forest ---")
        models['Random Forest'] = train_random_forest(
            X_train, y_train, 
            n_estimators=100,
            max_depth=10
        )
    
    if 'svm' in args.models:
        print("\n--- Training SVM ---")
        models['SVM'] = train_svm(
            X_train, y_train,
            kernel='rbf',
            C=1.0
        )
    
    if 'gb' in args.models:
        print("\n--- Training Gradient Boosting ---")
        models['Gradient Boosting'] = train_gradient_boosting(
            X_train, y_train,
            n_estimators=100,
            learning_rate=0.1
        )
    
    if 'nn' in args.models:
        from src.models import train_neural_network
        print("\n--- Training Neural Network ---")
        models['Neural Network'] = train_neural_network(
            X_train, y_train,
            hidden_layer_sizes=(100, 50)
        )
    
    # Step 4: Model Evaluation
    print("\n" + "=" * 80)
    print("STEP 4: MODEL EVALUATION")
    print("=" * 80)
    
    # Evaluate each model
    for name, model in models.items():
        print(f"\n{'=' * 80}")
        generate_evaluation_report(model, X_test, y_test, name)
        
        # Cross-validation
        cv_results = cross_validate_model(model, X_train, y_train, cv=5)
    
    # Compare models
    if len(models) > 1:
        print("\n" + "=" * 80)
        print("MODEL COMPARISON")
        print("=" * 80)
        comparison_df = compare_models(models, X_test, y_test)
    
    # Step 5: Visualization
    print("\n" + "=" * 80)
    print("STEP 5: VISUALIZATION")
    print("=" * 80)
    
    # Create output directories
    os.makedirs(f'{args.output}/figures', exist_ok=True)
    os.makedirs(f'{args.output}/models', exist_ok=True)
    
    # Get feature names
    feature_names = ['age', 'bmi', 'blood_pressure_sys', 'blood_pressure_dia',
                     'glucose', 'cholesterol', 'heart_rate', 'biomarker_a', 'biomarker_b']
    
    # Plot for first model
    first_model_name = list(models.keys())[0]
    first_model = models[first_model_name]
    
    print(f"\nGenerating visualizations for {first_model_name}...")
    
    # ROC curve
    plot_roc_curve(
        first_model, X_test, y_test,
        save_path=f'{args.output}/figures/roc_curve_{first_model_name.replace(" ", "_").lower()}.png'
    )
    
    # Feature importance (if applicable)
    if hasattr(first_model, 'feature_importances_'):
        plot_feature_importance(
            first_model, feature_names, top_n=9,
            save_path=f'{args.output}/figures/feature_importance_{first_model_name.replace(" ", "_").lower()}.png'
        )
    
    # Confusion matrix
    y_pred = first_model.predict(X_test)
    plot_confusion_matrix(
        y_test, y_pred,
        save_path=f'{args.output}/figures/confusion_matrix_{first_model_name.replace(" ", "_").lower()}.png'
    )
    
    # Multiple ROC curves if multiple models
    if len(models) > 1:
        plot_multiple_roc_curves(
            models, X_test, y_test,
            save_path=f'{args.output}/figures/roc_curves_comparison.png'
        )
    
    # Step 6: Save Models
    print("\n" + "=" * 80)
    print("STEP 6: SAVING MODELS")
    print("=" * 80)
    
    for name, model in models.items():
        model_filename = f'{args.output}/models/{name.replace(" ", "_").lower()}_model.pkl'
        save_model(model, model_filename)
    
    # Save scaler
    import joblib
    scaler_path = f'{args.output}/models/scaler.pkl'
    joblib.dump(scaler, scaler_path)
    print(f"✓ Scaler saved to {scaler_path}")
    
    # Final Summary
    print("\n" + "=" * 80)
    print("PIPELINE COMPLETE!")
    print("=" * 80)
    print(f"\n✓ Trained {len(models)} model(s)")
    print(f"✓ Results saved to {args.output}/")
    print(f"✓ Models saved to {args.output}/models/")
    print(f"✓ Figures saved to {args.output}/figures/")
    print("\n" + "=" * 80)


if __name__ == "__main__":
    main()


