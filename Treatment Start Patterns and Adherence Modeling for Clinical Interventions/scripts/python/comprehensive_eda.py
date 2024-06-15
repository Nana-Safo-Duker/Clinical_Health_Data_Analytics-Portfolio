"""
Comprehensive Exploratory Data Analysis Script

This script performs thorough exploratory data analysis of the treatment starts dataset.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
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
    df['Quarter'] = df['TreatmentStart'].dt.quarter
    return df

def data_quality_assessment(df):
    """Assess data quality."""
    print("=" * 60)
    print("DATA QUALITY ASSESSMENT")
    print("=" * 60)
    
    print(f"\nDataset shape: {df.shape}")
    print(f"Missing values:\n{df.isnull().sum()}")
    print(f"\nData types:\n{df.dtypes}")
    print(f"\nDate range: {df['TreatmentStart'].min()} to {df['TreatmentStart'].max()}")
    
    # Outlier detection
    Q1 = df['Dosage'].quantile(0.25)
    Q3 = df['Dosage'].quantile(0.75)
    IQR = Q3 - Q1
    outliers = df[(df['Dosage'] < Q1 - 1.5*IQR) | (df['Dosage'] > Q3 + 1.5*IQR)]
    print(f"\nOutliers detected: {len(outliers)}")
    if len(outliers) > 0:
        print("Outlier details:")
        print(outliers[['PatientID', 'Drug', 'Dosage']])
    
    return outliers

def descriptive_statistics(df):
    """Compute descriptive statistics."""
    print("\n" + "=" * 60)
    print("DESCRIPTIVE STATISTICS")
    print("=" * 60)
    
    print("\nNumerical variables:")
    print(df['Dosage'].describe())
    print(f"\nSkewness: {df['Dosage'].skew():.4f}")
    print(f"Kurtosis: {df['Dosage'].kurtosis():.4f}")
    
    print("\nCategorical variables:")
    print("Drug distribution:")
    print(df['Drug'].value_counts())
    print(f"\nProportions:\n{df['Drug'].value_counts(normalize=True) * 100}")

def temporal_analysis(df, output_dir='outputs'):
    """Analyze temporal patterns."""
    print("\n" + "=" * 60)
    print("TEMPORAL ANALYSIS")
    print("=" * 60)
    
    month_order = ['January', 'February', 'March', 'April', 'May', 'June']
    monthly_counts = df['MonthName'].value_counts().reindex(month_order, fill_value=0)
    
    print("\nTreatment starts by month:")
    print(monthly_counts)
    
    print("\nMean dosage by month:")
    mean_dosage_month = df.groupby('MonthName')['Dosage'].mean().reindex(month_order, fill_value=0)
    print(mean_dosage_month)
    
    # Visualizations
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    
    # Monthly counts
    axes[0, 0].bar(range(len(monthly_counts)), monthly_counts.values)
    axes[0, 0].set_xticks(range(len(monthly_counts)))
    axes[0, 0].set_xticklabels(monthly_counts.index, rotation=45)
    axes[0, 0].set_title('Treatment Starts by Month')
    axes[0, 0].set_ylabel('Count')
    
    # Mean dosage by month
    axes[0, 1].plot(range(len(mean_dosage_month)), mean_dosage_month.values, marker='o')
    axes[0, 1].set_xticks(range(len(mean_dosage_month)))
    axes[0, 1].set_xticklabels(mean_dosage_month.index, rotation=45)
    axes[0, 1].set_title('Mean Dosage by Month')
    axes[0, 1].set_ylabel('Mean Dosage')
    
    # Timeline
    df_sorted = df.sort_values('TreatmentStart')
    axes[1, 0].plot(df_sorted['TreatmentStart'], range(len(df_sorted)), marker='o', markersize=4)
    axes[1, 0].set_title('Treatment Starts Timeline')
    axes[1, 0].set_xlabel('Date')
    axes[1, 0].set_ylabel('Cumulative Count')
    axes[1, 0].tick_params(axis='x', rotation=45)
    
    # Drug usage by month
    drug_month = pd.crosstab(df['MonthName'], df['Drug']).reindex(month_order, fill_value=0)
    sns.heatmap(drug_month, annot=True, fmt='d', cmap='YlOrRd', ax=axes[1, 1])
    axes[1, 1].set_title('Drug Usage by Month')
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/temporal_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()

def relationship_analysis(df, output_dir='outputs'):
    """Analyze relationships between variables."""
    print("\n" + "=" * 60)
    print("RELATIONSHIP ANALYSIS")
    print("=" * 60)
    
    # Correlation
    df_encoded = df.copy()
    df_encoded['Drug_encoded'] = df_encoded['Drug'].map({'Cisplatin': 0, 'Nivolumab': 1})
    corr_matrix = df_encoded[['Dosage', 'Drug_encoded', 'Month']].corr()
    
    print("\nCorrelation matrix:")
    print(corr_matrix)
    
    # Visualizations
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    
    # Dosage by Drug
    sns.boxplot(data=df, x='Drug', y='Dosage', ax=axes[0, 0])
    axes[0, 0].set_title('Dosage Distribution by Drug')
    
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
    
    # Distribution comparison
    for drug in df['Drug'].unique():
        drug_data = df[df['Drug'] == drug]
        axes[1, 1].hist(drug_data['Dosage'], alpha=0.6, label=drug, bins=10)
    axes[1, 1].set_title('Dosage Distribution by Drug')
    axes[1, 1].set_xlabel('Dosage')
    axes[1, 1].set_ylabel('Frequency')
    axes[1, 1].legend()
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/relationship_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()

def patient_analysis(df):
    """Analyze patient-level patterns."""
    print("\n" + "=" * 60)
    print("PATIENT ANALYSIS")
    print("=" * 60)
    
    patient_stats = df.groupby('PatientID').agg({
        'Drug': 'count',
        'Dosage': ['mean', 'sum', 'min', 'max']
    }).round(2)
    
    patient_stats.columns = ['Treatment_Count', 'Mean_Dosage', 'Total_Dosage', 
                            'Min_Dosage', 'Max_Dosage']
    
    print(f"\nNumber of unique patients: {df['PatientID'].nunique()}")
    print(f"Patients with multiple treatments: {len(patient_stats[patient_stats['Treatment_Count'] > 1])}")
    print("\nPatient Statistics (top 10):")
    print(patient_stats.sort_values('Treatment_Count', ascending=False).head(10))

def generate_summary(df, outliers):
    """Generate EDA summary."""
    print("\n" + "=" * 60)
    print("EDA SUMMARY")
    print("=" * 60)
    
    print(f"\n1. Dataset Overview:")
    print(f"   - Total records: {len(df)}")
    print(f"   - Unique patients: {df['PatientID'].nunique()}")
    print(f"   - Date range: {df['TreatmentStart'].min().date()} to {df['TreatmentStart'].max().date()}")
    
    print(f"\n2. Drug Distribution:")
    for drug, count in df['Drug'].value_counts().items():
        print(f"   - {drug}: {count} treatments ({count/len(df)*100:.1f}%)")
    
    print(f"\n3. Dosage Statistics:")
    print(f"   - Mean: {df['Dosage'].mean():.2f}")
    print(f"   - Median: {df['Dosage'].median():.2f}")
    print(f"   - Std Dev: {df['Dosage'].std():.2f}")
    print(f"   - Range: {df['Dosage'].min()} - {df['Dosage'].max()}")
    
    print(f"\n4. Data Quality:")
    print(f"   - Missing values: {df.isnull().sum().sum()}")
    print(f"   - Outliers detected: {len(outliers)}")
    
    print(f"\n5. Key Findings:")
    print("   - Dataset contains treatment starts for two drugs: Cisplatin and Nivolumab")
    print("   - Some patients have multiple treatment records")
    print("   - Dosage varies significantly between drugs")
    print("   - Treatment patterns show temporal variations")

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
    outliers = data_quality_assessment(df)
    descriptive_statistics(df)
    temporal_analysis(df, output_dir)
    relationship_analysis(df, output_dir)
    patient_analysis(df)
    generate_summary(df, outliers)
    
    print("\n" + "=" * 60)
    print("EDA COMPLETE")
    print("=" * 60)

if __name__ == "__main__":
    main()


