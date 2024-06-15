"""
Comprehensive Exploratory Data Analysis Module
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from data_loader import load_data, clean_data
import warnings
warnings.filterwarnings('ignore')

def comprehensive_eda(df_clean):
    """
    Perform comprehensive exploratory data analysis
    
    Parameters:
    -----------
    df_clean : DataFrame
        Cleaned dataset
    """
    print("=== COMPREHENSIVE EXPLORATORY DATA ANALYSIS ===\n")
    
    # 1. Data Overview
    print("1. DATA OVERVIEW")
    print("=" * 50)
    print(f"Dataset shape: {df_clean.shape}")
    print(f"Number of rows: {len(df_clean)}")
    print(f"Number of columns: {len(df_clean.columns)}")
    print(f"Memory usage: {df_clean.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
    
    # 2. Data Types and Missing Values
    print("\n2. DATA QUALITY")
    print("=" * 50)
    print("Data Types:")
    print(df_clean.dtypes)
    print("\nMissing Values:")
    missing = df_clean.isnull().sum()
    missing_pct = (missing / len(df_clean)) * 100
    missing_df = pd.DataFrame({
        'Missing Count': missing,
        'Percentage': missing_pct
    })
    print(missing_df[missing_df['Missing Count'] > 0])
    
    # 3. Summary Statistics
    print("\n3. SUMMARY STATISTICS")
    print("=" * 50)
    numeric_cols = df_clean.select_dtypes(include=[np.number]).columns
    print(df_clean[numeric_cols].describe())
    
    # 4. Distribution Analysis
    print("\n4. DISTRIBUTION ANALYSIS")
    print("=" * 50)
    for col in numeric_cols[:5]:  # First 5 numeric columns
        print(f"\n{col}:")
        print(f"  Skewness: {df_clean[col].skew():.4f}")
        print(f"  Kurtosis: {df_clean[col].kurtosis():.4f}")
        print(f"  CV: {(df_clean[col].std()/df_clean[col].mean()*100):.2f}%")
    
    # 5. Visualizations
    create_eda_visualizations(df_clean)
    
    # 6. Feature Engineering Opportunities
    print("\n5. FEATURE ENGINEERING OPPORTUNITIES")
    print("=" * 50)
    if 'County' in df_clean.columns:
        # Extract state from county name
        df_clean['State'] = df_clean['County'].str.extract(r',\s*(\w+)\(')
        print("Extracted state information from county names")
    
    if 'FIPS' in df_clean.columns:
        # State FIPS code (first 2 digits)
        df_clean['State_FIPS'] = (df_clean['FIPS'] // 1000).astype(int)
        print("Extracted state FIPS codes")
    
    # 7. Outlier Analysis
    print("\n6. OUTLIER ANALYSIS")
    print("=" * 50)
    for col in numeric_cols[:3]:
        Q1 = df_clean[col].quantile(0.25)
        Q3 = df_clean[col].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        outliers = df_clean[(df_clean[col] < lower_bound) | (df_clean[col] > upper_bound)]
        print(f"{col}: {len(outliers)} outliers ({len(outliers)/len(df_clean)*100:.2f}%)")
    
    return df_clean

def create_eda_visualizations(df_clean):
    """Create comprehensive EDA visualizations"""
    
    # Set style
    sns.set_style("whitegrid")
    plt.rcParams['figure.figsize'] = (15, 10)
    
    numeric_cols = df_clean.select_dtypes(include=[np.number]).columns.tolist()
    
    # 1. Distribution plots for key variables
    if 'Incidence_Rate' in df_clean.columns:
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        
        # Histogram
        axes[0, 0].hist(df_clean['Incidence_Rate'].dropna(), bins=50, edgecolor='black', alpha=0.7)
        axes[0, 0].set_title('Distribution of Incidence Rate')
        axes[0, 0].set_xlabel('Incidence Rate')
        axes[0, 0].set_ylabel('Frequency')
        
        # Box plot
        axes[0, 1].boxplot(df_clean['Incidence_Rate'].dropna())
        axes[0, 1].set_title('Box Plot of Incidence Rate')
        axes[0, 1].set_ylabel('Incidence Rate')
        
        # Q-Q plot
        from scipy import stats
        stats.probplot(df_clean['Incidence_Rate'].dropna(), dist="norm", plot=axes[1, 0])
        axes[1, 0].set_title('Q-Q Plot')
        
        # Density plot
        df_clean['Incidence_Rate'].dropna().plot(kind='density', ax=axes[1, 1])
        axes[1, 1].set_title('Density Plot of Incidence Rate')
        axes[1, 1].set_xlabel('Incidence Rate')
        
        plt.tight_layout()
        plt.savefig('eda_distributions.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    # 2. Correlation heatmap
    if len(numeric_cols) > 1:
        plt.figure(figsize=(12, 10))
        corr_matrix = df_clean[numeric_cols].corr()
        sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0, fmt='.2f', square=True)
        plt.title('Correlation Heatmap')
        plt.tight_layout()
        plt.savefig('eda_correlation.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    # 3. Pair plot for key variables
    key_vars = [col for col in ['Incidence_Rate', 'Annual_Count', 'Trend_5yr'] if col in df_clean.columns]
    if len(key_vars) >= 2:
        plt.figure(figsize=(15, 12))
        sns.pairplot(df_clean[key_vars].dropna(), diag_kind='kde')
        plt.suptitle('Pair Plot of Key Variables', y=1.02)
        plt.tight_layout()
        plt.savefig('eda_pairplot.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    # 4. Trend analysis
    if 'Trend' in df_clean.columns:
        fig, axes = plt.subplots(1, 2, figsize=(15, 5))
        
        # Count by trend
        trend_counts = df_clean['Trend'].value_counts()
        axes[0].bar(trend_counts.index, trend_counts.values)
        axes[0].set_title('Count of Counties by Trend')
        axes[0].set_xlabel('Trend')
        axes[0].set_ylabel('Count')
        axes[0].tick_params(axis='x', rotation=45)
        
        # Box plot by trend
        if 'Incidence_Rate' in df_clean.columns:
            sns.boxplot(data=df_clean, x='Trend', y='Incidence_Rate', ax=axes[1])
            axes[1].set_title('Incidence Rate by Trend')
            axes[1].tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        plt.savefig('eda_trend_analysis.png', dpi=300, bbox_inches='tight')
        plt.show()

if __name__ == "__main__":
    df = load_data()
    df_clean = clean_data(df)
    df_enhanced = comprehensive_eda(df_clean)

