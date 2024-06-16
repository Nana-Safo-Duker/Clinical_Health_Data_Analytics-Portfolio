"""
Comprehensive Exploratory Data Analysis
Deep dive into the health dataset
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import missingno as msno
import warnings
warnings.filterwarnings('ignore')

sns.set_style('whitegrid')
plt.rcParams['figure.figsize'] = (14, 8)

def load_and_clean_data():
    """Load and clean the health data"""
    df = pd.read_csv('../data/health_data.csv')
    if 'Unnamed: 0' in df.columns:
        df = df.drop('Unnamed: 0', axis=1)
    df['age_years'] = df['age'] / 365.25
    df['bmi'] = df['weight'] / ((df['height'] / 100) ** 2)
    df = df[(df['ap_hi'] >= 80) & (df['ap_hi'] <= 250)]
    df = df[(df['ap_lo'] >= 40) & (df['ap_lo'] <= 150)]
    df = df[df['ap_hi'] >= df['ap_lo']]
    df = df[(df['height'] >= 100) & (df['height'] <= 220)]
    df = df[(df['weight'] >= 30) & (df['weight'] <= 200)]
    df = df[(df['bmi'] >= 10) & (df['bmi'] <= 60)]
    return df

def data_overview(df):
    """Provide comprehensive data overview"""
    print("=" * 80)
    print("DATA OVERVIEW")
    print("=" * 80)
    print(f"Dataset shape: {df.shape}")
    print(f"\nColumn names: {df.columns.tolist()}")
    print(f"\nData types:\n{df.dtypes}")
    print(f"\nMissing values:\n{df.isnull().sum()}")
    print(f"\nDuplicate rows: {df.duplicated().sum()}")
    print(f"\nFirst few rows:")
    print(df.head())
    print(f"\nSummary statistics:")
    print(df.describe())
    
    # Missing data visualization
    if df.isnull().sum().sum() > 0:
        msno.matrix(df)
        plt.title('Missing Data Pattern', fontsize=14, fontweight='bold')
        plt.tight_layout()
        plt.savefig('../figures/missing_data.png', dpi=300, bbox_inches='tight')
        plt.close()

def outlier_analysis(df):
    """Analyze outliers in the dataset"""
    print("=" * 80)
    print("OUTLIER ANALYSIS")
    print("=" * 80)
    
    numerical_cols = ['age_years', 'height', 'weight', 'ap_hi', 'ap_lo', 'bmi']
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    axes = axes.ravel()
    
    for i, col in enumerate(numerical_cols):
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)]
        print(f"\n{col.upper()}:")
        print(f"  Outliers: {len(outliers)} ({len(outliers)/len(df)*100:.2f}%)")
        print(f"  Lower bound: {lower_bound:.2f}")
        print(f"  Upper bound: {upper_bound:.2f}")
        
        axes[i].boxplot(df[col], vert=True)
        axes[i].set_title(f'{col.upper()} - Box Plot', fontsize=12, fontweight='bold')
        axes[i].set_ylabel(col)
        axes[i].grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    plt.savefig('../figures/outlier_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()

def distribution_analysis(df):
    """Analyze distributions of variables"""
    print("=" * 80)
    print("DISTRIBUTION ANALYSIS")
    print("=" * 80)
    
    numerical_cols = ['age_years', 'height', 'weight', 'ap_hi', 'ap_lo', 'bmi']
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    axes = axes.ravel()
    
    for i, col in enumerate(numerical_cols):
        # Histogram with normal distribution overlay
        axes[i].hist(df[col], bins=50, density=True, alpha=0.7, edgecolor='black', label='Data')
        
        # Normal distribution
        mu, sigma = df[col].mean(), df[col].std()
        x = np.linspace(df[col].min(), df[col].max(), 100)
        axes[i].plot(x, stats.norm.pdf(x, mu, sigma), 'r-', linewidth=2, label='Normal')
        
        # Statistics
        skewness = stats.skew(df[col])
        kurtosis = stats.kurtosis(df[col])
        axes[i].text(0.05, 0.95, f'Skew: {skewness:.2f}\nKurtosis: {kurtosis:.2f}', 
                    transform=axes[i].transAxes, fontsize=10, verticalalignment='top',
                    bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        
        axes[i].set_title(f'{col.upper()} Distribution', fontsize=12, fontweight='bold')
        axes[i].set_xlabel(col)
        axes[i].set_ylabel('Density')
        axes[i].legend()
        axes[i].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('../figures/distribution_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()

def relationship_analysis(df):
    """Analyze relationships between variables"""
    print("=" * 80)
    print("RELATIONSHIP ANALYSIS")
    print("=" * 80)
    
    # Correlation matrix
    numerical_cols = ['age_years', 'height', 'weight', 'ap_hi', 'ap_lo', 'bmi', 'cardio']
    correlation_matrix = df[numerical_cols].corr()
    
    plt.figure(figsize=(12, 10))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0, 
                square=True, linewidths=1, cbar_kws={'shrink': 0.8}, fmt='.3f')
    plt.title('Correlation Matrix', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig('../figures/relationship_correlation.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # Relationship with target variable
    print("\nCorrelation with target variable (cardio):")
    cardio_corr = correlation_matrix['cardio'].sort_values(ascending=False)
    print(cardio_corr)

def target_variable_analysis(df):
    """Analyze target variable distribution and relationships"""
    print("=" * 80)
    print("TARGET VARIABLE ANALYSIS")
    print("=" * 80)
    
    # Distribution
    plt.figure(figsize=(10, 6))
    cardio_counts = df['cardio'].value_counts()
    plt.bar(cardio_counts.index.astype(str), cardio_counts.values, color=['skyblue', 'salmon'], edgecolor='black')
    plt.xlabel('Cardiovascular Disease', fontsize=12)
    plt.ylabel('Count', fontsize=12)
    plt.title('Distribution of Target Variable (Cardio)', fontsize=14, fontweight='bold')
    plt.xticks([0, 1], ['No (0)', 'Yes (1)'])
    for i, v in enumerate(cardio_counts.values):
        plt.text(i, v + 500, f'{v}\n({v/len(df)*100:.2f}%)', ha='center', va='bottom', fontweight='bold')
    plt.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    plt.savefig('../figures/target_distribution.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # Comparison by target variable
    numerical_cols = ['age_years', 'height', 'weight', 'ap_hi', 'ap_lo', 'bmi']
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    axes = axes.ravel()
    
    for i, col in enumerate(numerical_cols):
        df.boxplot(column=col, by='cardio', ax=axes[i])
        axes[i].set_title(f'{col.upper()} by Cardio Status', fontsize=12, fontweight='bold')
        axes[i].set_xlabel('Cardiovascular Disease')
        axes[i].set_ylabel(col)
        axes[i].grid(True, alpha=0.3)
    
    plt.suptitle('')
    plt.tight_layout()
    plt.savefig('../figures/target_comparison.png', dpi=300, bbox_inches='tight')
    plt.close()

def feature_engineering_insights(df):
    """Provide insights for feature engineering"""
    print("=" * 80)
    print("FEATURE ENGINEERING INSIGHTS")
    print("=" * 80)
    
    # Blood pressure categories
    df['bp_category'] = pd.cut(df['ap_hi'], bins=[0, 120, 140, 160, 300], 
                               labels=['Normal', 'Elevated', 'High Stage 1', 'High Stage 2'])
    print("\nBlood Pressure Categories:")
    print(df['bp_category'].value_counts())
    
    # BMI categories
    df['bmi_category'] = pd.cut(df['bmi'], bins=[0, 18.5, 25, 30, 100], 
                                labels=['Underweight', 'Normal', 'Overweight', 'Obese'])
    print("\nBMI Categories:")
    print(df['bmi_category'].value_counts())
    
    # Age groups
    df['age_group'] = pd.cut(df['age_years'], bins=[0, 30, 40, 50, 60, 100], 
                             labels=['<30', '30-40', '40-50', '50-60', '60+'])
    print("\nAge Groups:")
    print(df['age_group'].value_counts())

if __name__ == "__main__":
    df = load_and_clean_data()
    data_overview(df)
    outlier_analysis(df)
    distribution_analysis(df)
    relationship_analysis(df)
    target_variable_analysis(df)
    feature_engineering_insights(df)
    print("\nComprehensive EDA completed successfully!")

