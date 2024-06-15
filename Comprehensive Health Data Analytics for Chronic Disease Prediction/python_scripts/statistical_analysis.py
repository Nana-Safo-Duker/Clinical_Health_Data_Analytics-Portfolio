"""
Statistical Analysis: Descriptive, Inferential, and Exploratory
Comprehensive statistical analysis of health data
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from scipy.stats import chi2_contingency, ttest_ind, mannwhitneyu
import warnings
warnings.filterwarnings('ignore')

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)

def load_and_clean_data():
    """Load and clean the health data"""
    df = pd.read_csv('../data/health_data.csv')
    if 'Unnamed: 0' in df.columns:
        df = df.drop('Unnamed: 0', axis=1)
    
    # Convert age from days to years
    df['age_years'] = df['age'] / 365.25
    
    # Calculate BMI
    df['bmi'] = df['weight'] / ((df['height'] / 100) ** 2)
    
    # Clean blood pressure data
    df = df[(df['ap_hi'] >= 80) & (df['ap_hi'] <= 250)]
    df = df[(df['ap_lo'] >= 40) & (df['ap_lo'] <= 150)]
    df = df[df['ap_hi'] >= df['ap_lo']]
    
    # Clean height and weight
    df = df[(df['height'] >= 100) & (df['height'] <= 220)]
    df = df[(df['weight'] >= 30) & (df['weight'] <= 200)]
    df = df[(df['bmi'] >= 10) & (df['bmi'] <= 60)]
    
    return df

def descriptive_statistics(df):
    """Perform descriptive statistics"""
    print("=" * 80)
    print("DESCRIPTIVE STATISTICS - NUMERICAL VARIABLES")
    print("=" * 80)
    
    numerical_cols = ['age_years', 'height', 'weight', 'ap_hi', 'ap_lo', 'bmi']
    desc_stats = df[numerical_cols].describe()
    print(desc_stats)
    
    print("\n" + "=" * 80)
    print("ADDITIONAL STATISTICS")
    print("=" * 80)
    for col in numerical_cols:
        print(f"\n{col.upper()}:")
        print(f"  Skewness: {stats.skew(df[col].dropna()):.4f}")
        print(f"  Kurtosis: {stats.kurtosis(df[col].dropna()):.4f}")
        print(f"  Median: {df[col].median():.4f}")
        print(f"  IQR: {df[col].quantile(0.75) - df[col].quantile(0.25):.4f}")
    
    print("\n" + "=" * 80)
    print("DESCRIPTIVE STATISTICS - CATEGORICAL VARIABLES")
    print("=" * 80)
    categorical_cols = ['gender', 'cholesterol', 'gluc', 'smoke', 'alco', 'active', 'cardio']
    for col in categorical_cols:
        print(f"\n{col.upper()}:")
        print(df[col].value_counts().sort_index())
        print(f"Proportions:")
        print(df[col].value_counts(normalize=True).sort_index())

def inferential_statistics(df):
    """Perform inferential statistics"""
    print("\n" + "=" * 80)
    print("T-TEST: Age difference between cardio and non-cardio patients")
    print("=" * 80)
    
    cardio_yes = df[df['cardio'] == 1]['age_years']
    cardio_no = df[df['cardio'] == 0]['age_years']
    
    t_stat, p_value = ttest_ind(cardio_yes, cardio_no)
    print(f"T-statistic: {t_stat:.4f}")
    print(f"P-value: {p_value:.4f}")
    print(f"Mean age (Cardio=1): {cardio_yes.mean():.2f} years")
    print(f"Mean age (Cardio=0): {cardio_no.mean():.2f} years")
    if p_value < 0.05:
        print("Result: Significant difference (p < 0.05)")
    else:
        print("Result: No significant difference (p >= 0.05)")
    
    print("\n" + "=" * 80)
    print("CHI-SQUARE TESTS: Association between categorical variables and cardio")
    print("=" * 80)
    
    categorical_vars = ['gender', 'cholesterol', 'gluc', 'smoke', 'alco', 'active']
    for var in categorical_vars:
        contingency_table = pd.crosstab(df[var], df['cardio'])
        chi2, p_value, dof, expected = chi2_contingency(contingency_table)
        print(f"\n{var.upper()} vs Cardio:")
        print(f"  Chi-square statistic: {chi2:.4f}")
        print(f"  P-value: {p_value:.4f}")
        print(f"  Degrees of freedom: {dof}")
        if p_value < 0.05:
            print(f"  Result: Significant association (p < 0.05)")
        else:
            print(f"  Result: No significant association (p >= 0.05)")

def correlation_analysis(df):
    """Perform correlation analysis"""
    print("\n" + "=" * 80)
    print("CORRELATION ANALYSIS")
    print("=" * 80)
    
    correlation_cols = ['age_years', 'height', 'weight', 'ap_hi', 'ap_lo', 'bmi', 'cardio']
    correlation_matrix = df[correlation_cols].corr()
    print("\nCorrelation Matrix:")
    print(correlation_matrix)
    
    # Visualize correlation matrix
    plt.figure(figsize=(10, 8))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0, 
                square=True, linewidths=1, cbar_kws={"shrink": 0.8})
    plt.title('Correlation Matrix of Numerical Variables', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig('../figures/correlation_matrix.png', dpi=300, bbox_inches='tight')
    plt.close()

def exploratory_analysis(df):
    """Perform exploratory data analysis"""
    print("\n" + "=" * 80)
    print("EXPLORATORY DATA ANALYSIS")
    print("=" * 80)
    
    # Distribution of target variable
    plt.figure(figsize=(8, 6))
    cardio_counts = df['cardio'].value_counts()
    plt.bar(cardio_counts.index, cardio_counts.values, color=['skyblue', 'salmon'])
    plt.xlabel('Cardiovascular Disease', fontsize=12)
    plt.ylabel('Count', fontsize=12)
    plt.title('Distribution of Cardiovascular Disease', fontsize=14, fontweight='bold')
    plt.xticks([0, 1], ['No (0)', 'Yes (1)'])
    for i, v in enumerate(cardio_counts.values):
        plt.text(i, v + 500, str(v), ha='center', va='bottom', fontweight='bold')
    plt.tight_layout()
    plt.savefig('../figures/cardio_distribution.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # Distribution of numerical variables
    numerical_cols = ['age_years', 'height', 'weight', 'ap_hi', 'ap_lo', 'bmi']
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    axes = axes.ravel()
    
    for i, col in enumerate(numerical_cols):
        axes[i].hist(df[col], bins=50, edgecolor='black', alpha=0.7)
        axes[i].set_title(f'Distribution of {col.upper()}', fontsize=12, fontweight='bold')
        axes[i].set_xlabel(col, fontsize=10)
        axes[i].set_ylabel('Frequency', fontsize=10)
        axes[i].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('../figures/numerical_distributions.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # Box plots by cardio status
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    axes = axes.ravel()
    
    for i, col in enumerate(numerical_cols):
        df.boxplot(column=col, by='cardio', ax=axes[i])
        axes[i].set_title(f'{col.upper()} by Cardio Status', fontsize=12, fontweight='bold')
        axes[i].set_xlabel('Cardiovascular Disease', fontsize=10)
        axes[i].set_ylabel(col, fontsize=10)
        axes[i].grid(True, alpha=0.3)
    
    plt.suptitle('', fontsize=16)
    plt.tight_layout()
    plt.savefig('../figures/boxplots_by_cardio.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("Exploratory analysis completed. Figures saved.")

if __name__ == "__main__":
    df = load_and_clean_data()
    print(f"Dataset shape: {df.shape}")
    print(f"\nMissing values:\n{df.isnull().sum()}")
    
    descriptive_statistics(df)
    inferential_statistics(df)
    correlation_analysis(df)
    exploratory_analysis(df)
    
    print("\nStatistical analysis completed successfully!")

