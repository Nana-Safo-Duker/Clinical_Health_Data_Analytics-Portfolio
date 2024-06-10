"""
Radiomics Analysis Pipeline for Cancer Outcome Prediction

This script provides comprehensive functions for radiomics feature extraction,
statistical analysis, and machine learning model development for predicting
cancer outcomes from medical imaging data.

Author: Research Team
Date: 2025
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import warnings
warnings.filterwarnings('ignore')

# Medical imaging libraries
try:
    import SimpleITK as sitk
    import pydicom
    from radiomics import featureextractor
except ImportError:
    print("Warning: Some medical imaging libraries are not installed.")
    print("Install with: pip install SimpleITK pydicom pyradiomics")

# Machine learning libraries
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.preprocessing import StandardScaler, RobustScaler
from sklearn.feature_selection import SelectKBest, f_classif, mutual_info_classif
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.svm import SVC, SVR
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, roc_curve, confusion_matrix, classification_report,
    mean_squared_error, r2_score
)
from scipy import stats
from scipy.stats import ttest_ind, mannwhitneyu
import joblib

# Set style for plots
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")


class RadiomicsExtractor:
    """
    Class for extracting radiomic features from medical images.
    """
    
    def __init__(self, params_file: Optional[str] = None):
        """
        Initialize the radiomics feature extractor.
        
        Parameters:
        -----------
        params_file : str, optional
            Path to PyRadiomics parameters file. If None, uses default settings.
        """
        if params_file:
            self.extractor = featureextractor.RadiomicsFeatureExtractor(params_file)
        else:
            self.extractor = featureextractor.RadiomicsFeatureExtractor()
            # Set basic parameters
            self.extractor.enableAllFeatures()
    
    def extract_features_from_image(
        self, 
        image_path: str, 
        mask_path: str
    ) -> Dict[str, float]:
        """
        Extract radiomic features from a medical image and mask.
        
        Parameters:
        -----------
        image_path : str
            Path to the medical image (DICOM, NIfTI, etc.)
        mask_path : str
            Path to the segmentation mask
        
        Returns:
        --------
        dict : Dictionary of radiomic features
        """
        try:
            result = self.extractor.execute(image_path, mask_path)
            # Remove diagnostic features (not radiomic features)
            features = {k: v for k, v in result.items() 
                       if not k.startswith('diagnostics')}
            return features
        except Exception as e:
            print(f"Error extracting features from {image_path}: {e}")
            return {}
    
    def extract_features_batch(
        self, 
        image_mask_pairs: List[Tuple[str, str]]
    ) -> pd.DataFrame:
        """
        Extract features from multiple image-mask pairs.
        
        Parameters:
        -----------
        image_mask_pairs : list of tuples
            List of (image_path, mask_path) tuples
        
        Returns:
        --------
        pd.DataFrame : DataFrame with features for each image
        """
        all_features = []
        for image_path, mask_path in image_mask_pairs:
            features = self.extract_features_from_image(image_path, mask_path)
            features['image_id'] = Path(image_path).stem
            all_features.append(features)
        
        return pd.DataFrame(all_features)


class StatisticalAnalysis:
    """
    Class for statistical analysis of radiomic features.
    """
    
    @staticmethod
    def compare_groups(
        data: pd.DataFrame,
        feature_cols: List[str],
        group_col: str,
        group1: str,
        group2: str,
        test_type: str = 'ttest'
    ) -> pd.DataFrame:
        """
        Compare feature distributions between two groups.
        
        Parameters:
        -----------
        data : pd.DataFrame
            DataFrame with features and group labels
        feature_cols : list
            List of feature column names
        group_col : str
            Name of the column containing group labels
        group1 : str
            Name of first group
        group2 : str
            Name of second group
        test_type : str
            Type of statistical test ('ttest' or 'mannwhitney')
        
        Returns:
        --------
        pd.DataFrame : Results of statistical tests
        """
        group1_data = data[data[group_col] == group1]
        group2_data = data[data[group_col] == group2]
        
        results = []
        for feature in feature_cols:
            group1_values = group1_data[feature].dropna()
            group2_values = group2_data[feature].dropna()
            
            if len(group1_values) < 3 or len(group2_values) < 3:
                continue
            
            # Calculate descriptive statistics
            mean1, std1 = group1_values.mean(), group1_values.std()
            mean2, std2 = group2_values.mean(), group2_values.std()
            
            # Perform statistical test
            if test_type == 'ttest':
                # T-test is appropriate for comparing means between two groups
                statistic, p_value = ttest_ind(group1_values, group2_values)
            elif test_type == 'mannwhitney':
                statistic, p_value = mannwhitneyu(group1_values, group2_values)
            else:
                raise ValueError(f"Unknown test type: {test_type}")
            
            # Calculate effect size (Cohen's d)
            pooled_std = np.sqrt((std1**2 + std2**2) / 2)
            cohens_d = (mean1 - mean2) / pooled_std if pooled_std > 0 else 0
            
            results.append({
                'feature': feature,
                'group1_mean': mean1,
                'group1_std': std1,
                'group2_mean': mean2,
                'group2_std': std2,
                'mean_difference': mean1 - mean2,
                'statistic': statistic,
                'p_value': p_value,
                'cohens_d': cohens_d,
                'significant': p_value < 0.05
            })
        
        return pd.DataFrame(results)
    
    @staticmethod
    def correlation_analysis(
        data: pd.DataFrame,
        feature_cols: List[str],
        outcome_col: str,
        method: str = 'pearson'
    ) -> pd.DataFrame:
        """
        Calculate correlations between features and outcome.
        
        Parameters:
        -----------
        data : pd.DataFrame
            DataFrame with features and outcome
        feature_cols : list
            List of feature column names
        outcome_col : str
            Name of the outcome column
        method : str
            Correlation method ('pearson' or 'spearman')
        
        Returns:
        --------
        pd.DataFrame : Correlation results
        """
        correlations = []
        for feature in feature_cols:
            if feature in data.columns and outcome_col in data.columns:
                corr_data = data[[feature, outcome_col]].dropna()
                if len(corr_data) > 3:
                    corr, p_value = stats.pearsonr(
                        corr_data[feature], 
                        corr_data[outcome_col]
                    ) if method == 'pearson' else stats.spearmanr(
                        corr_data[feature],
                        corr_data[outcome_col]
                    )
                    correlations.append({
                        'feature': feature,
                        'correlation': corr,
                        'p_value': p_value,
                        'abs_correlation': abs(corr),
                        'significant': p_value < 0.05
                    })
        
        return pd.DataFrame(correlations).sort_values('abs_correlation', ascending=False)


class RadiomicsMLPipeline:
    """
    Machine learning pipeline for radiomics-based outcome prediction.
    """
    
    def __init__(
        self,
        task_type: str = 'classification',
        n_features: int = 50,
        scaler_type: str = 'standard'
    ):
        """
        Initialize the ML pipeline.
        
        Parameters:
        -----------
        task_type : str
            Type of task ('classification' or 'regression')
        n_features : int
            Number of features to select
        scaler_type : str
            Type of scaler ('standard' or 'robust')
        """
        self.task_type = task_type
        self.n_features = n_features
        self.scaler = StandardScaler() if scaler_type == 'standard' else RobustScaler()
        self.feature_selector = None
        self.pca = None
        self.model = None
        self.selected_features = None
    
    def prepare_features(
        self,
        X_train: pd.DataFrame,
        X_test: pd.DataFrame,
        y_train: pd.Series,
        use_pca: bool = False,
        n_components: Optional[int] = None
    ) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Prepare features through scaling and selection.
        
        Parameters:
        -----------
        X_train : pd.DataFrame
            Training features
        X_test : pd.DataFrame
            Test features
        y_train : pd.Series
            Training labels
        use_pca : bool
            Whether to use PCA for dimensionality reduction
        n_components : int, optional
            Number of PCA components (uses explained variance if None)
        
        Returns:
        --------
        tuple : (X_train_processed, X_test_processed)
        """
        # Remove non-numeric columns
        numeric_cols = X_train.select_dtypes(include=[np.number]).columns.tolist()
        X_train = X_train[numeric_cols]
        X_test = X_test[numeric_cols]
        
        # Handle missing values
        X_train = X_train.fillna(X_train.median())
        X_test = X_test.fillna(X_train.median())
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Feature selection
        if self.task_type == 'classification':
            self.feature_selector = SelectKBest(
                score_func=f_classif, 
                k=min(self.n_features, X_train_scaled.shape[1])
            )
        else:
            self.feature_selector = SelectKBest(
                score_func=mutual_info_classif,
                k=min(self.n_features, X_train_scaled.shape[1])
            )
        
        X_train_selected = self.feature_selector.fit_transform(X_train_scaled, y_train)
        X_test_selected = self.feature_selector.transform(X_test_scaled)
        
        # Get selected feature names
        selected_indices = self.feature_selector.get_support(indices=True)
        self.selected_features = [numeric_cols[i] for i in selected_indices]
        
        # Apply PCA if requested
        if use_pca:
            if n_components is None:
                # Use number of components that explain 95% of variance
                n_components = min(50, X_train_selected.shape[1])
            
            self.pca = PCA(n_components=n_components)
            X_train_final = self.pca.fit_transform(X_train_selected)
            X_test_final = self.pca.transform(X_test_selected)
            
            print(f"PCA: {n_components} components explain "
                  f"{self.pca.explained_variance_ratio_.sum():.2%} of variance")
        else:
            X_train_final = X_train_selected
            X_test_final = X_test_selected
        
        return pd.DataFrame(X_train_final), pd.DataFrame(X_test_final)
    
    def train_model(
        self,
        X_train: pd.DataFrame,
        y_train: pd.Series,
        model_type: str = 'random_forest',
        **model_params
    ):
        """
        Train a machine learning model.
        
        Parameters:
        -----------
        X_train : pd.DataFrame
            Training features
        y_train : pd.Series
            Training labels
        model_type : str
            Type of model ('random_forest', 'svm', 'xgboost')
        **model_params
            Additional parameters for the model
        """
        if model_type == 'random_forest':
            if self.task_type == 'classification':
                self.model = RandomForestClassifier(
                    n_estimators=100,
                    max_depth=10,
                    random_state=42,
                    **model_params
                )
            else:
                self.model = RandomForestRegressor(
                    n_estimators=100,
                    max_depth=10,
                    random_state=42,
                    **model_params
                )
        elif model_type == 'svm':
            if self.task_type == 'classification':
                self.model = SVC(
                    probability=True,
                    random_state=42,
                    **model_params
                )
            else:
                self.model = SVR(**model_params)
        
        self.model.fit(X_train, y_train)
    
    def evaluate_model(
        self,
        X_test: pd.DataFrame,
        y_test: pd.Series
    ) -> Dict:
        """
        Evaluate the trained model.
        
        Parameters:
        -----------
        X_test : pd.DataFrame
            Test features
        y_test : pd.Series
            Test labels
        
        Returns:
        --------
        dict : Evaluation metrics
        """
        y_pred = self.model.predict(X_test)
        
        if self.task_type == 'classification':
            metrics = {
                'accuracy': accuracy_score(y_test, y_pred),
                'precision': precision_score(y_test, y_pred, average='weighted'),
                'recall': recall_score(y_test, y_pred, average='weighted'),
                'f1_score': f1_score(y_test, y_pred, average='weighted')
            }
            
            # ROC AUC (for binary classification)
            if len(np.unique(y_test)) == 2:
                y_pred_proba = self.model.predict_proba(X_test)[:, 1]
                metrics['roc_auc'] = roc_auc_score(y_test, y_pred_proba)
            
            print("\nClassification Report:")
            print(classification_report(y_test, y_pred))
            
        else:
            metrics = {
                'mse': mean_squared_error(y_test, y_pred),
                'rmse': np.sqrt(mean_squared_error(y_test, y_pred)),
                'r2_score': r2_score(y_test, y_pred)
            }
            
            print(f"\nRegression Metrics:")
            print(f"MSE: {metrics['mse']:.4f}")
            print(f"RMSE: {metrics['rmse']:.4f}")
            print(f"R²: {metrics['r2_score']:.4f}")
        
        return metrics
    
    def cross_validate(
        self,
        X: pd.DataFrame,
        y: pd.Series,
        cv_folds: int = 5
    ) -> Dict:
        """
        Perform cross-validation.
        
        Parameters:
        -----------
        X : pd.DataFrame
            Features
        y : pd.Series
            Labels
        cv_folds : int
            Number of cross-validation folds
        
        Returns:
        --------
        dict : Cross-validation results
        """
        if self.task_type == 'classification':
            scoring = 'roc_auc' if len(np.unique(y)) == 2 else 'f1_weighted'
            cv = StratifiedKFold(n_splits=cv_folds, shuffle=True, random_state=42)
        else:
            scoring = 'r2'
            cv = cv_folds
        
        scores = cross_val_score(
            self.model, X, y, cv=cv, scoring=scoring, n_jobs=-1
        )
        
        return {
            'mean_score': scores.mean(),
            'std_score': scores.std(),
            'scores': scores
        }


def visualize_features(
    data: pd.DataFrame,
    feature_cols: List[str],
    outcome_col: str,
    save_path: Optional[str] = None
):
    """
    Create visualizations of radiomic features.
    
    Parameters:
    -----------
    data : pd.DataFrame
        DataFrame with features and outcome
    feature_cols : list
        List of feature columns to visualize
    outcome_col : str
        Name of the outcome column
    save_path : str, optional
        Path to save the figure
    """
    n_features = min(6, len(feature_cols))
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    axes = axes.flatten()
    
    for i, feature in enumerate(feature_cols[:n_features]):
        if feature in data.columns:
            ax = axes[i]
            if data[outcome_col].dtype in ['object', 'category']:
                # Box plot for categorical outcomes
                groups = data[outcome_col].unique()
                box_data = [data[data[outcome_col] == group][feature].dropna() 
                           for group in groups]
                ax.boxplot(box_data, labels=groups)
            else:
                # Scatter plot for continuous outcomes
                ax.scatter(data[feature], data[outcome_col], alpha=0.5)
                # Add trend line
                z = np.polyfit(data[feature].dropna(), 
                              data[data[feature].notna()][outcome_col], 1)
                p = np.poly1d(z)
                ax.plot(data[feature].dropna(), 
                       p(data[feature].dropna()), "r--", alpha=0.5)
            
            ax.set_xlabel(feature)
            ax.set_ylabel(outcome_col)
            ax.set_title(f'{feature} vs {outcome_col}')
            ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.show()


def main():
    """
    Example usage of the radiomics analysis pipeline.
    """
    print("Radiomics Analysis Pipeline for Cancer Outcome Prediction")
    print("=" * 60)
    
    # Example: Load sample data (in practice, load from actual image files)
    print("\n1. Loading data...")
    # This would typically load from actual DICOM/NIfTI files
    # For demonstration, we create synthetic data
    np.random.seed(42)
    n_samples = 100
    
    # Simulate radiomic features
    feature_data = {
        'firstorder_Mean': np.random.normal(100, 20, n_samples),
        'firstorder_StdDev': np.random.normal(15, 5, n_samples),
        'firstorder_Entropy': np.random.normal(3.5, 0.5, n_samples),
        'glcm_Correlation': np.random.normal(0.7, 0.1, n_samples),
        'glcm_Contrast': np.random.normal(5, 2, n_samples),
        'shape_Volume': np.random.normal(50, 15, n_samples),
        'shape_Sphericity': np.random.normal(0.7, 0.1, n_samples),
    }
    
    df = pd.DataFrame(feature_data)
    
    # Simulate binary outcome (0 = poor outcome, 1 = good outcome)
    # Outcome correlated with some features
    outcome = (
        (df['firstorder_Entropy'] > 3.5).astype(int) * 0.6 +
        (df['glcm_Correlation'] > 0.7).astype(int) * 0.4 +
        np.random.binomial(1, 0.2, n_samples)
    ).clip(0, 1)
    df['outcome'] = outcome
    
    print(f"Loaded {len(df)} samples with {len(df.columns)-1} features")
    
    # Statistical analysis
    print("\n2. Performing statistical analysis...")
    stats_analyzer = StatisticalAnalysis()
    
    # Compare groups
    df['group'] = ['Group_A' if x == 0 else 'Group_B' for x in outcome]
    feature_cols = [col for col in df.columns if col not in ['outcome', 'group']]
    
    comparison_results = stats_analyzer.compare_groups(
        df, feature_cols, 'group', 'Group_A', 'Group_B', test_type='ttest'
    )
    print("\nTop significant features (p < 0.05):")
    significant = comparison_results[comparison_results['significant']].sort_values('p_value')
    print(significant[['feature', 'p_value', 'mean_difference']].head(10))
    
    # Correlation analysis
    print("\n3. Correlation analysis...")
    corr_results = stats_analyzer.correlation_analysis(
        df, feature_cols, 'outcome', method='pearson'
    )
    print("\nTop correlated features:")
    print(corr_results.head(10)[['feature', 'correlation', 'p_value']])
    
    # Machine learning pipeline
    print("\n4. Building ML model...")
    pipeline = RadiomicsMLPipeline(
        task_type='classification',
        n_features=5
    )
    
    # Prepare data
    X = df[feature_cols]
    y = df['outcome']
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    X_train_proc, X_test_proc = pipeline.prepare_features(
        X_train, X_test, y_train, use_pca=False
    )
    
    # Train model
    pipeline.train_model(X_train_proc, y_train, model_type='random_forest')
    
    # Evaluate
    print("\n5. Model evaluation...")
    metrics = pipeline.evaluate_model(X_test_proc, y_test)
    print(f"\nModel Performance:")
    for metric, value in metrics.items():
        print(f"  {metric}: {value:.4f}")
    
    # Cross-validation
    print("\n6. Cross-validation...")
    cv_results = pipeline.cross_validate(X_train_proc, y_train, cv_folds=5)
    print(f"CV Score: {cv_results['mean_score']:.4f} (+/- {cv_results['std_score']:.4f})")
    
    # Visualization
    print("\n7. Creating visualizations...")
    visualize_features(df, feature_cols[:6], 'outcome')
    
    print("\n" + "=" * 60)
    print("Analysis complete!")


if __name__ == "__main__":
    main()

