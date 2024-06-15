"""
Descriptive Statistics Module
"""
import pandas as pd
import numpy as np
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from data_loader import load_data, clean_data

def descriptive_stats(data, col_name):
    """Calculate comprehensive descriptive statistics"""
    stats_dict = {
        'Mean': data.mean(),
        'Median': data.median(),
        'Mode': data.mode()[0] if len(data.mode()) > 0 else np.nan,
        'Standard Deviation': data.std(),
        'Variance': data.var(),
        'Minimum': data.min(),
        'Maximum': data.max(),
        'Range': data.max() - data.min(),
        'Q1 (25th percentile)': data.quantile(0.25),
        'Q3 (75th percentile)': data.quantile(0.75),
        'IQR': data.quantile(0.75) - data.quantile(0.25),
        'Skewness': data.skew(),
        'Kurtosis': data.kurtosis(),
        'Coefficient of Variation': (data.std() / data.mean()) * 100
    }
    return pd.Series(stats_dict, name=col_name)

def calculate_descriptive_stats(df_clean):
    """Calculate and display descriptive statistics"""
    print("=== DESCRIPTIVE STATISTICS ===\n")
    
    # Basic statistics
    print("1. Summary Statistics for Incidence Rate:")
    print(df_clean['Incidence_Rate'].describe())
    print("\n2. Summary Statistics for Annual Count:")
    print(df_clean['Annual_Count'].describe())
    
    # Comprehensive statistics
    print("\n3. Comprehensive Descriptive Statistics for Incidence Rate:")
    incidence_stats = descriptive_stats(df_clean['Incidence_Rate'], 'Incidence_Rate')
    print(incidence_stats)
    
    # Statistics by Trend
    if 'Trend' in df_clean.columns:
        print("\n4. Descriptive Statistics by Trend Category:")
        trend_stats = df_clean.groupby('Trend')['Incidence_Rate'].agg([
            'count', 'mean', 'median', 'std', 'min', 'max'
        ]).round(2)
        print(trend_stats)
    
    return incidence_stats

if __name__ == "__main__":
    df = load_data()
    df_clean = clean_data(df)
    stats = calculate_descriptive_stats(df_clean)

