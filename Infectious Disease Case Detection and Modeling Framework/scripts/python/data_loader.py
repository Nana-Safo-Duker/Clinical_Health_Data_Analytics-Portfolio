"""
Data Loading and Preprocessing Module
"""
import os
import pandas as pd
import numpy as np

def load_data(file_path=None):
    """
    Load the cancer incidence dataset with proper encoding handling
    
    Parameters:
    -----------
    file_path : str
        Path to the CSV file. If not provided, resolves the bundled
        dataset relative to this script's location so the function
        works regardless of the current working directory.
        
    Returns:
    --------
    df : DataFrame
        Loaded dataset
    """
    if file_path is None:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(script_dir, '..', '..', 'data', 'incd.csv')

    try:
        df = pd.read_csv(file_path, encoding='utf-8')
    except UnicodeDecodeError:
        df = pd.read_csv(file_path, encoding='latin-1')
    
    return df

def clean_data(df):
    """
    Clean and preprocess the dataset
    
    Parameters:
    -----------
    df : DataFrame
        Raw dataset
        
    Returns:
    --------
    df_clean : DataFrame
        Cleaned dataset
    """
    # Clean column names
    df.columns = df.columns.str.strip()
    df.columns = df.columns.str.replace(' ', '_')
    df.columns = df.columns.str.replace('(', '')
    df.columns = df.columns.str.replace(')', '')
    
    # Rename columns for easier access
    column_mapping = {
        'County': 'County',
        'FIPS': 'FIPS',
    }
    
    # Map columns dynamically
    for col in df.columns:
        # Note: the "Recent 5-Year Trend ... in Incidence Rates" column also
        # contains the substrings "Incidence" and "Rate", so it must be
        # excluded here (via the "Trend" check) or it gets misclassified as
        # the main Incidence_Rate column instead of Trend_5yr below.
        if ('Age-Adjusted' in col or 'Incidence' in col) and 'Trend' not in col:
            if 'Rate' in col:
                column_mapping[col] = 'Incidence_Rate'
        elif 'Lower' in col and '95' in col and 'Confidence' in col:
            # The dataset has two "Lower 95% Confidence Interval" columns: one for
            # the incidence rate and one for the 5-year trend. Pandas disambiguates
            # the duplicate header by appending ".1" to the second occurrence, so
            # use that suffix (rather than an absent "Trend" substring) to tell
            # them apart and avoid mapping both to the same column name.
            if col.endswith('.1'):
                column_mapping[col] = 'Trend_CI_Lower'
            else:
                column_mapping[col] = 'CI_Lower'
        elif 'Upper' in col and '95' in col and 'Confidence' in col:
            if col.endswith('.1'):
                column_mapping[col] = 'Trend_CI_Upper'
            else:
                column_mapping[col] = 'CI_Upper'
        elif 'Average' in col and 'Annual' in col:
            column_mapping[col] = 'Annual_Count'
        elif 'Recent' in col and 'Trend' in col and '5-Year' not in col:
            column_mapping[col] = 'Trend'
        elif '5-Year' in col and 'Trend' in col:
            column_mapping[col] = 'Trend_5yr'
    
    df = df.rename(columns=column_mapping)
    
    # Handle numeric columns
    numeric_columns = ['Incidence_Rate', 'CI_Lower', 'CI_Upper', 'Annual_Count', 
                      'Trend_5yr', 'Trend_CI_Lower', 'Trend_CI_Upper', 'FIPS']
    
    for col in numeric_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # Remove rows where key variables are missing
    df_clean = df.dropna(subset=['Incidence_Rate']).copy()
    
    return df_clean

if __name__ == "__main__":
    df = load_data()
    df_clean = clean_data(df)
    print(f"Dataset loaded: {df_clean.shape}")
    print(f"Columns: {df_clean.columns.tolist()}")

