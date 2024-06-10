"""
Bioinformatics ML Project - Source Package

This package contains modules for machine learning-based medical diagnosis.

Modules:
- data_processing: Data loading and preprocessing
- feature_engineering: Feature transformation and selection
- models: ML model implementations
- evaluation: Model evaluation metrics
- visualization: Plotting utilities
"""

__version__ = "1.0.0"
__author__ = "Your Name"

# Import main functions for easy access
from .data_processing import load_clinical_data, preprocess_data
from .models import train_random_forest, train_svm, train_gradient_boosting
from .evaluation import evaluate_model, calculate_metrics
from .visualization import plot_roc_curve, plot_feature_importance

__all__ = [
    'load_clinical_data',
    'preprocess_data',
    'train_random_forest',
    'train_svm',
    'train_gradient_boosting',
    'evaluate_model',
    'calculate_metrics',
    'plot_roc_curve',
    'plot_feature_importance'
]


