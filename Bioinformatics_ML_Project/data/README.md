# Data Directory

This directory contains all data files for the project.

## Structure

```
data/
├── raw/           # Original, immutable data
├── processed/     # Cleaned and transformed data
└── README.md      # This file
```

## Data Sources

### Clinical Dataset

The project uses clinical data containing:

- **Patient Demographics**: Age, gender, BMI
- **Clinical Measurements**: Blood pressure (systolic/diastolic), heart rate
- **Laboratory Results**: Glucose, cholesterol levels
- **Biomarkers**: Biomarker A (gamma-distributed), Biomarker B (exponentially-distributed)
- **Outcome**: Binary diagnosis (0 = Negative, 1 = Positive)

### Data Dictionary

| Column | Type | Description | Range/Values |
|--------|------|-------------|--------------|
| `patient_id` | String | Unique patient identifier | PT0001 - PTnnnn |
| `age` | Integer | Patient age in years | 18-85 |
| `gender` | Categorical | Patient gender | M, F |
| `bmi` | Float | Body Mass Index (kg/m²) | 15.0-50.0 |
| `blood_pressure_sys` | Float | Systolic blood pressure (mmHg) | 90-180 |
| `blood_pressure_dia` | Float | Diastolic blood pressure (mmHg) | 60-120 |
| `glucose` | Float | Fasting blood glucose (mg/dL) | 70-200 |
| `cholesterol` | Float | Total cholesterol (mg/dL) | 150-300 |
| `heart_rate` | Float | Resting heart rate (bpm) | 50-120 |
| `biomarker_a` | Float | Novel biomarker A (arbitrary units) | 0-20 |
| `biomarker_b` | Float | Novel biomarker B (arbitrary units) | 0-10 |
| `diagnosis` | Binary | Disease diagnosis | 0 (Negative), 1 (Positive) |

## Data Privacy and Ethics

⚠️ **IMPORTANT**: This project uses synthetic/de-identified data. When working with real patient data:

1. **Obtain Proper Approval**: 
   - IRB approval for human subjects research
   - Appropriate data use agreements

2. **Ensure Compliance**:
   - HIPAA (Health Insurance Portability and Accountability Act)
   - GDPR (General Data Protection Regulation) if applicable
   - Local data protection regulations

3. **Data Security**:
   - Never commit real patient data to version control
   - Use encryption for data storage and transmission
   - Implement access controls
   - Maintain audit logs

4. **De-identification**:
   - Remove all direct identifiers (names, SSN, dates, etc.)
   - Apply appropriate statistical disclosure control
   - Follow HIPAA Safe Harbor or Expert Determination methods

## Data Processing Pipeline

### 1. Raw Data (`data/raw/`)

Store original data files here. These should **never** be modified.

```python
# Load raw data
df = pd.read_csv('data/raw/clinical_data.csv')
```

### 2. Data Cleaning

- Handle missing values
- Remove duplicates
- Correct data types
- Validate ranges

### 3. Feature Engineering

- Create derived features
- Encode categorical variables
- Scale numerical features
- Generate interaction terms

### 4. Processed Data (`data/processed/`)

Store cleaned and transformed data here.

```python
# Save processed data
df_processed.to_csv('data/processed/cleaned_data.csv', index=False)
```

## Generating Synthetic Data

For testing and development, you can generate synthetic data:

```python
from src.data_processing import generate_synthetic_data

# Generate 1000 samples
df = generate_synthetic_data(n_samples=1000, random_state=42)

# Save to raw directory
df.to_csv('data/raw/synthetic_clinical_data.csv', index=False)
```

## Data Quality Checks

Before using data for modeling:

- [ ] Check for missing values
- [ ] Verify data types
- [ ] Validate value ranges
- [ ] Check for duplicates
- [ ] Assess class balance
- [ ] Detect outliers
- [ ] Verify data distribution

## Citation

If using external datasets, cite appropriately:

```
[Author(s)]. (Year). Dataset Name. Repository/Journal. DOI or URL.
```

## Contact

For questions about data sources or access:
- Email: your.email@example.com
- Data Steward: [Name]

---

*Last Updated: October 27, 2025*


