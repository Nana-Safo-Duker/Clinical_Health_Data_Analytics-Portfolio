"""
Univariate, Bivariate, and Multivariate Analysis Script

This script performs comprehensive analysis at different variable levels.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from scipy.stats import chi2_contingency
import warnings
warnings.filterwarnings('ignore')

def load_and_preprocess_data(file_path):
    """Load and preprocess the dataset."""
    df = pd.read_csv(file_path)
    df['TreatmentStart'] = pd.to_datetime(df['TreatmentStart'], format='%m/%d/%y')
    df['Year'] = df['TreatmentStart'].dt.year
    df['Month'] = df['TreatmentStart'].dt.month
    df['Day'] = df['TreatmentStart'].dt.day
    df['MonthName'] = df['TreatmentStart'].dt.strftime('%B')
    df['Weekday'] = df['TreatmentStart'].dt.day_name()
    return df

def univariate_analysis(df, output_dir='outputs'):
    """Perform univariate analysis."""
    print("=" * 60)
    print("UNIVARIATE ANALYSIS")
    print("=" * 60)
    
    # Numerical variable analysis
    print("\n1. Dosage (Numerical Variable):")
    print(df['Dosage'].describe())
    print(f"Skewness: {df['Dosage'].skew():.4f}")
    print(f"Kurtosis: {df['Dosage'].kurtosis():.4f}")
    
    # Categorical variable analysis
    print("\n2. Drug (Categorical Variable):")
    print(df['Drug'].value_counts())
    print(f"Proportions:\n{df['Drug'].value_counts(normalize=True) * 100}")
    
    # Visualizations
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    
    # Histogram
    axes[0, 0].hist(df['Dosage'], bins=15, edgecolor='black', alpha=0.7)
    axes[0, 0].set_title('Dosage Distribution')
    axes[0, 0].set_xlabel('Dosage')
    axes[0, 0].set_ylabel('Frequency')
    
    # Box plot
    axes[0, 1].boxplot(df['Dosage'], vert=True)
    axes[0, 1].set_title('Box Plot: Dosage')
    axes[0, 1].set_ylabel('Dosage')
    
    # Drug distribution
    drug_counts = df['Drug'].value_counts()
    axes[1, 0].bar(drug_counts.index, drug_counts.values)
    axes[1, 0].set_title('Drug Distribution')
    axes[1, 0].set_xlabel('Drug')
    axes[1, 0].set_ylabel('Count')
    
    # Q-Q plot
    stats.probplot(df['Dosage'], dist="norm", plot=axes[1, 1])
    axes[1, 1].set_title('Q-Q Plot: Normality Check')
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/univariate_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()
    print(f"\nVisualizations saved to {output_dir}/univariate_analysis.png")

def bivariate_analysis(df, output_dir='outputs'):
    """Perform bivariate analysis."""
    print("\n" + "=" * 60)
    print("BIVARIATE ANALYSIS")
    print("=" * 60)
    
    # Dosage vs Drug
    print("\n1. Dosage vs Drug:")
    print(df.groupby('Drug')['Dosage'].describe())
    
    # Correlation analysis
    df_encoded = df.copy()
    df_encoded['Drug_encoded'] = df_encoded['Drug'].map({'Cisplatin': 0, 'Nivolumab': 1})
    corr_matrix = df_encoded[['Dosage', 'Drug_encoded', 'Month']].corr()
    print("\n2. Correlation Matrix:")
    print(corr_matrix)
    
    # Chi-square test
    contingency_table = pd.crosstab(df['Drug'], df['MonthName'])
    chi2, p_value, dof, expected = chi2_contingency(contingency_table)
    print(f"\n3. Chi-square test for Drug-Month association:")
    print(f"   Chi-square: {chi2:.4f}, p-value: {p_value:.4f}")
    
    # Visualizations
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    
    # Box plot: Dosage by Drug
    sns.boxplot(data=df, x='Drug', y='Dosage', ax=axes[0, 0])
    axes[0, 0].set_title('Dosage by Drug')
    
    # Correlation heatmap
    sns.heatmap(corr_matrix, annot=True, fmt='.3f', cmap='coolwarm', center=0, ax=axes[0, 1])
    axes[0, 1].set_title('Correlation Matrix')
    
    # Scatter plot
    scatter = axes[1, 0].scatter(df['Month'], df['Dosage'], 
                                c=df_encoded['Drug_encoded'], cmap='viridis', alpha=0.6)
    axes[1, 0].set_title('Month vs Dosage (colored by Drug)')
    axes[1, 0].set_xlabel('Month')
    axes[1, 0].set_ylabel('Dosage')
    plt.colorbar(scatter, ax=axes[1, 0])
    
    # Heatmap: Drug by Month
    month_order = ['January', 'February', 'March', 'April', 'May', 'June']
    drug_month = pd.crosstab(df['MonthName'], df['Drug']).reindex(month_order, fill_value=0)
    sns.heatmap(drug_month, annot=True, fmt='d', cmap='YlOrRd', ax=axes[1, 1])
    axes[1, 1].set_title('Drug Usage by Month')
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/bivariate_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()
    print(f"\nVisualizations saved to {output_dir}/bivariate_analysis.png")

def multivariate_analysis(df, output_dir='outputs'):
    """Perform multivariate analysis."""
    print("\n" + "=" * 60)
    print("MULTIVARIATE ANALYSIS")
    print("=" * 60)
    
    # Mean dosage by Drug and Month
    month_order = ['January', 'February', 'March', 'April', 'May', 'June']
    drug_month_mean = df.groupby(['Drug', 'MonthName'])['Dosage'].mean().unstack(fill_value=0)
    drug_month_mean = drug_month_mean.reindex(columns=month_order, fill_value=0)
    
    print("\n1. Mean Dosage by Drug and Month:")
    print(drug_month_mean)
    
    print("\n2. Summary Statistics by Drug and Month:")
    print(df.groupby(['Drug', 'MonthName'])['Dosage'].describe())
    
    # Visualizations
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    
    # Grouped bar chart
    drug_month_mean.plot(kind='bar', ax=axes[0, 0])
    axes[0, 0].set_title('Mean Dosage by Drug and Month')
    axes[0, 0].set_xlabel('Drug')
    axes[0, 0].set_ylabel('Mean Dosage')
    axes[0, 0].legend(title='Month')
    
    # Heatmap
    sns.heatmap(drug_month_mean, annot=True, fmt='.1f', cmap='YlOrRd', ax=axes[0, 1])
    axes[0, 1].set_title('Mean Dosage Heatmap: Drug × Month')
    
    # Histogram by Drug
    for drug in df['Drug'].unique():
        drug_data = df[df['Drug'] == drug]
        axes[1, 0].hist(drug_data['Dosage'], alpha=0.6, label=drug, bins=10)
    axes[1, 0].set_title('Dosage Distribution by Drug')
    axes[1, 0].set_xlabel('Dosage')
    axes[1, 0].set_ylabel('Frequency')
    axes[1, 0].legend()
    
    # Multivariate scatter
    scatter = axes[1, 1].scatter(df['Month'], df['Dosage'], 
                                c=df['Drug'].map({'Cisplatin': 0, 'Nivolumab': 1}), 
                                s=df['Dosage']/5, alpha=0.6, cmap='viridis')
    axes[1, 1].set_title('Multivariate View: Month vs Dosage')
    axes[1, 1].set_xlabel('Month')
    axes[1, 1].set_ylabel('Dosage')
    plt.colorbar(scatter, ax=axes[1, 1])
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/multivariate_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()
    print(f"\nVisualizations saved to {output_dir}/multivariate_analysis.png")

def main():
    """Main function."""
    import os
    
    # Create output directory
    output_dir = 'outputs'
    os.makedirs(output_dir, exist_ok=True)
    
    # Load data
    file_path = '../../data/mock_treatment_starts_2016.csv'
    df = load_and_preprocess_data(file_path)
    
    # Perform analyses
    univariate_analysis(df, output_dir)
    bivariate_analysis(df, output_dir)
    multivariate_analysis(df, output_dir)
    
    print("\n" + "=" * 60)
    print("ANALYSIS COMPLETE")
    print("=" * 60)

if __name__ == "__main__":
    main()


