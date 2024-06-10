"""
Data Processing Module

Functions for loading, cleaning, and preprocessing clinical data.
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.impute import SimpleImputer


def load_clinical_data(filepath, **kwargs):
    """
    Load clinical data from CSV file.
    
    Parameters:
    -----------
    filepath : str
        Path to the CSV file
    **kwargs : dict
        Additional arguments for pd.read_csv
        
    Returns:
    --------
    df : pd.DataFrame
        Loaded dataframe
        
    Example:
    --------
    >>> data = load_clinical_data('data/raw/clinical_data.csv')
    """
    try:
        df = pd.read_csv(filepath, **kwargs)
        print(f"✓ Data loaded successfully: {df.shape}")
        return df
    except FileNotFoundError:
        print(f"✗ Error: File not found at {filepath}")
        raise
    except Exception as e:
        print(f"✗ Error loading data: {str(e)}")
        raise


def handle_missing_values(df, strategy='mean', categorical_strategy='most_frequent'):
    """
    Handle missing values in the dataset.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Input dataframe
    strategy : str, default='mean'
        Strategy for numeric columns ('mean', 'median', 'most_frequent')
    categorical_strategy : str, default='most_frequent'
        Strategy for categorical columns
        
    Returns:
    --------
    df : pd.DataFrame
        Dataframe with imputed values
        
    Example:
    --------
    >>> df_clean = handle_missing_values(df, strategy='median')
    """
    df_copy = df.copy()
    
    # Identify numeric and categorical columns
    numeric_cols = df_copy.select_dtypes(include=[np.number]).columns
    categorical_cols = df_copy.select_dtypes(include=['object', 'category']).columns
    
    # Impute numeric columns
    if len(numeric_cols) > 0 and df_copy[numeric_cols].isnull().sum().sum() > 0:
        numeric_imputer = SimpleImputer(strategy=strategy)
        df_copy[numeric_cols] = numeric_imputer.fit_transform(df_copy[numeric_cols])
        print(f"✓ Imputed {len(numeric_cols)} numeric columns with strategy '{strategy}'")
    
    # Impute categorical columns
    if len(categorical_cols) > 0 and df_copy[categorical_cols].isnull().sum().sum() > 0:
        categorical_imputer = SimpleImputer(strategy=categorical_strategy)
        df_copy[categorical_cols] = categorical_imputer.fit_transform(df_copy[categorical_cols])
        print(f"✓ Imputed {len(categorical_cols)} categorical columns")
    
    return df_copy


def encode_categorical_features(df, columns=None, method='onehot'):
    """
    Encode categorical features.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Input dataframe
    columns : list, optional
        List of columns to encode (if None, auto-detect)
    method : str, default='onehot'
        Encoding method ('onehot' or 'label')
        
    Returns:
    --------
    df : pd.DataFrame
        Dataframe with encoded features
    encoders : dict
        Dictionary of encoders for each column
        
    Example:
    --------
    >>> df_encoded, encoders = encode_categorical_features(df, method='onehot')
    """
    df_copy = df.copy()
    
    if columns is None:
        columns = df_copy.select_dtypes(include=['object', 'category']).columns.tolist()
    
    encoders = {}
    
    if method == 'onehot':
        df_encoded = pd.get_dummies(df_copy, columns=columns, drop_first=True)
        print(f"✓ One-hot encoded {len(columns)} categorical columns")
        return df_encoded, encoders
    
    elif method == 'label':
        for col in columns:
            le = LabelEncoder()
            df_copy[col] = le.fit_transform(df_copy[col].astype(str))
            encoders[col] = le
        print(f"✓ Label encoded {len(columns)} categorical columns")
        return df_copy, encoders
    
    else:
        raise ValueError("Method must be 'onehot' or 'label'")


def remove_outliers(df, columns, method='iqr', threshold=1.5):
    """
    Remove outliers from specified columns.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Input dataframe
    columns : list
        Columns to check for outliers
    method : str, default='iqr'
        Method for outlier detection ('iqr' or 'zscore')
    threshold : float, default=1.5
        Threshold for outlier detection (IQR multiplier or z-score)
        
    Returns:
    --------
    df : pd.DataFrame
        Dataframe with outliers removed
    removed : int
        Number of rows removed
        
    Example:
    --------
    >>> df_clean, n_removed = remove_outliers(df, ['age', 'glucose'])
    """
    df_copy = df.copy()
    initial_shape = df_copy.shape[0]
    
    if method == 'iqr':
        for col in columns:
            Q1 = df_copy[col].quantile(0.25)
            Q3 = df_copy[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - threshold * IQR
            upper_bound = Q3 + threshold * IQR
            df_copy = df_copy[(df_copy[col] >= lower_bound) & (df_copy[col] <= upper_bound)]
    
    elif method == 'zscore':
        from scipy.stats import zscore
        for col in columns:
            z_scores = np.abs(zscore(df_copy[col].dropna()))
            df_copy = df_copy[(z_scores < threshold) | df_copy[col].isnull()]
    
    else:
        raise ValueError("Method must be 'iqr' or 'zscore'")
    
    removed = initial_shape - df_copy.shape[0]
    print(f"✓ Removed {removed} outlier rows ({removed/initial_shape*100:.2f}%)")
    
    return df_copy, removed


def scale_features(X, method='standard'):
    """
    Scale numerical features.
    
    Parameters:
    -----------
    X : pd.DataFrame or np.ndarray
        Feature matrix
    method : str, default='standard'
        Scaling method ('standard', 'minmax', or 'robust')
        
    Returns:
    --------
    X_scaled : np.ndarray
        Scaled features
    scaler : object
        Fitted scaler object
        
    Example:
    --------
    >>> X_scaled, scaler = scale_features(X_train, method='standard')
    """
    if method == 'standard':
        scaler = StandardScaler()
    elif method == 'minmax':
        from sklearn.preprocessing import MinMaxScaler
        scaler = MinMaxScaler()
    elif method == 'robust':
        from sklearn.preprocessing import RobustScaler
        scaler = RobustScaler()
    else:
        raise ValueError("Method must be 'standard', 'minmax', or 'robust'")
    
    X_scaled = scaler.fit_transform(X)
    print(f"✓ Features scaled using {method} scaling")
    
    return X_scaled, scaler


def preprocess_data(df, target_column='diagnosis', test_size=0.2, 
                   random_state=42, scale=True, handle_outliers=False):
    """
    Complete preprocessing pipeline for clinical data.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Input dataframe
    target_column : str, default='diagnosis'
        Name of the target column
    test_size : float, default=0.2
        Proportion of data for testing
    random_state : int, default=42
        Random seed for reproducibility
    scale : bool, default=True
        Whether to scale features
    handle_outliers : bool, default=False
        Whether to remove outliers
        
    Returns:
    --------
    X_train : np.ndarray
        Training features
    X_test : np.ndarray
        Testing features
    y_train : np.ndarray
        Training labels
    y_test : np.ndarray
        Testing labels
    scaler : object or None
        Fitted scaler (if scale=True)
        
    Example:
    --------
    >>> X_train, X_test, y_train, y_test, scaler = preprocess_data(df)
    """
    print("=" * 60)
    print("PREPROCESSING PIPELINE")
    print("=" * 60)
    
    df_processed = df.copy()
    
    # Remove patient ID if present
    id_cols = ['patient_id', 'id', 'ID']
    for col in id_cols:
        if col in df_processed.columns:
            df_processed = df_processed.drop(columns=[col])
            print(f"✓ Removed ID column: {col}")
    
    # Handle missing values
    if df_processed.isnull().sum().sum() > 0:
        df_processed = handle_missing_values(df_processed)
    
    # Encode categorical features
    categorical_cols = df_processed.select_dtypes(include=['object', 'category']).columns.tolist()
    if target_column in categorical_cols:
        categorical_cols.remove(target_column)
    
    if len(categorical_cols) > 0:
        df_processed, _ = encode_categorical_features(df_processed, columns=categorical_cols)
    
    # Separate features and target
    if target_column not in df_processed.columns:
        raise ValueError(f"Target column '{target_column}' not found in dataframe")
    
    X = df_processed.drop(columns=[target_column])
    y = df_processed[target_column]
    
    print(f"✓ Separated features (n={X.shape[1]}) and target")
    
    # Handle outliers if requested
    if handle_outliers:
        numeric_cols = X.select_dtypes(include=[np.number]).columns.tolist()
        combined = pd.concat([X, y], axis=1)
        combined, _ = remove_outliers(combined, numeric_cols)
        X = combined.drop(columns=[target_column])
        y = combined[target_column]
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )
    print(f"✓ Split data: Train={X_train.shape[0]}, Test={X_test.shape[0]}")
    
    # Scale features
    scaler = None
    if scale:
        X_train, scaler = scale_features(X_train, method='standard')
        X_test = scaler.transform(X_test)
    
    print("=" * 60)
    print("PREPROCESSING COMPLETE")
    print("=" * 60)
    
    return X_train, X_test, y_train, y_test, scaler


def generate_synthetic_data(n_samples=1000, n_features=10, random_state=42):
    """
    Generate synthetic clinical data for testing.
    
    Parameters:
    -----------
    n_samples : int, default=1000
        Number of samples to generate
    n_features : int, default=10
        Number of features
    random_state : int, default=42
        Random seed
        
    Returns:
    --------
    df : pd.DataFrame
        Synthetic clinical dataset
        
    Example:
    --------
    >>> df = generate_synthetic_data(n_samples=500)
    """
    np.random.seed(random_state)
    
    data = {
        'patient_id': [f'PT{str(i).zfill(4)}' for i in range(1, n_samples + 1)],
        'age': np.random.randint(18, 85, n_samples),
        'gender': np.random.choice(['M', 'F'], n_samples),
        'bmi': np.random.normal(27, 5, n_samples),
        'blood_pressure_sys': np.random.normal(130, 20, n_samples),
        'blood_pressure_dia': np.random.normal(85, 12, n_samples),
        'glucose': np.random.normal(100, 25, n_samples),
        'cholesterol': np.random.normal(200, 40, n_samples),
        'heart_rate': np.random.normal(75, 10, n_samples),
        'biomarker_a': np.random.gamma(2, 2, n_samples),
        'biomarker_b': np.random.exponential(1.5, n_samples),
        'diagnosis': np.random.choice([0, 1], n_samples, p=[0.7, 0.3])
    }
    
    df = pd.DataFrame(data)
    
    # Introduce some missing values
    missing_indices = np.random.choice(df.index, size=int(n_samples*0.05), replace=False)
    df.loc[missing_indices, 'biomarker_a'] = np.nan
    
    print(f"✓ Generated synthetic data: {df.shape}")
    
    return df


if __name__ == "__main__":
    # Example usage
    print("Data Processing Module - Example Usage\n")
    
    # Generate synthetic data
    df = generate_synthetic_data(n_samples=1000)
    print(f"\nDataset shape: {df.shape}")
    print(f"Missing values: {df.isnull().sum().sum()}")
    
    # Preprocess
    X_train, X_test, y_train, y_test, scaler = preprocess_data(df, scale=True)
    
    print(f"\nFinal shapes:")
    print(f"  X_train: {X_train.shape}")
    print(f"  X_test: {X_test.shape}")
    print(f"  y_train: {y_train.shape}")
    print(f"  y_test: {y_test.shape}")


