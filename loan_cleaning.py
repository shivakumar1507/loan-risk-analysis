# ============================================================
# Loan Portfolio Risk Analysis — Data Cleaning & Feature Engineering
# Dataset : Lending Club Loan Data (Kaggle)
# Author  : Shiva Kumar Devatha
# Tools   : Python (Pandas, NumPy)
# ============================================================

import pandas as pd
import numpy as np

# ============================================================
# 1. CONFIGURATION
# ============================================================

# Reproducible random sampling
np.random.seed(42)

# File path
FILE_PATH = r"C:\Users\SHIVA\Downloads\files\lending_club_loans.csv"

# Sample only 10% rows for faster development
SAMPLE_RATIO = 0.10

# ============================================================
# 2. LOAD DATA
# ============================================================

print("[INFO] Loading dataset...")

df = pd.read_csv(
    FILE_PATH,
    skiprows=lambda x: x > 0 and np.random.random() > SAMPLE_RATIO,
    low_memory=False
)

print(f"[INFO] Raw dataset shape: {df.shape}")

# ============================================================
# 3. SELECT RELEVANT COLUMNS
# ============================================================

print("[INFO] Selecting relevant columns...")

cols = [
    'loan_amnt',
    'funded_amnt',
    'term',
    'int_rate',
    'installment',
    'grade',
    'sub_grade',
    'emp_length',
    'home_ownership',
    'annual_inc',
    'verification_status',
    'issue_d',
    'loan_status',
    'purpose',
    'addr_state',
    'dti',
    'open_acc',
    'total_pymnt',
    'total_rec_prncp',
    'total_rec_int',
    'last_pymnt_d',
    'recoveries'
]

df = df[[c for c in cols if c in df.columns]].copy()

print(f"[INFO] Shape after column selection: {df.shape}")

# ============================================================
# 4. INITIAL DATA QUALITY CHECKS
# ============================================================

print("\n[INFO] Checking missing values...")
print(df.isnull().sum())

print("\n[INFO] Checking data types...")
print(df.dtypes)

print(
    f"\n[INFO] Memory usage: "
    f"{df.memory_usage(deep=True).sum()/1024**2:.2f} MB"
)

# ============================================================
# 5. REMOVE NULLS & DUPLICATES
# ============================================================

print("\n[INFO] Removing nulls and duplicates...")

critical_cols = [
    'loan_amnt',
    'loan_status',
    'grade',
    'annual_inc',
    'dti'
]

df.dropna(subset=critical_cols, inplace=True)

before_dupes = len(df)

df.drop_duplicates(inplace=True)

after_dupes = len(df)

print(f"[INFO] Removed duplicates: {before_dupes - after_dupes}")
print(f"[INFO] Shape after cleanup: {df.shape}")

# ============================================================
# 6. CLEAN INDIVIDUAL COLUMNS
# ============================================================

print("\n[INFO] Cleaning columns...")

# -----------------------------
# Interest Rate
# -----------------------------
df['int_rate'] = (
    df['int_rate']
    .astype(str)
    .str.replace('%', '', regex=False)
    .str.strip()
)

df['int_rate'] = pd.to_numeric(
    df['int_rate'],
    errors='coerce'
)

# -----------------------------
# Loan Term
# -----------------------------
df['term'] = (
    df['term']
    .astype(str)
    .str.extract(r'(\d+)')[0]
)

df['term'] = pd.to_numeric(
    df['term'],
    errors='coerce'
)

# -----------------------------
# Employment Length Mapping
# -----------------------------
emp_map = {
    '< 1 year': 0,
    '1 year': 1,
    '2 years': 2,
    '3 years': 3,
    '4 years': 4,
    '5 years': 5,
    '6 years': 6,
    '7 years': 7,
    '8 years': 8,
    '9 years': 9,
    '10+ years': 10
}

df['emp_length_num'] = df['emp_length'].map(emp_map)

df['emp_length_num'] = df['emp_length_num'].fillna(-1)

# -----------------------------
# Issue Date
# -----------------------------
df['issue_d'] = pd.to_datetime(
    df['issue_d'],
    format='%b-%Y',
    errors='coerce'
)

df['issue_year'] = df['issue_d'].dt.year
df['issue_month'] = df['issue_d'].dt.month

# -----------------------------
# Standardize Text Columns
# -----------------------------
text_cols = [
    'grade',
    'home_ownership',
    'purpose',
    'verification_status',
    'loan_status'
]

for col in text_cols:
    if col in df.columns:
        df[col] = (
            df[col]
            .astype(str)
            .str.strip()
            .str.upper()
        )

# ============================================================
# 7. OUTLIER HANDLING
# ============================================================

print("\n[INFO] Removing extreme outliers...")

before_outliers = len(df)

# Remove unrealistic annual income
df = df[df['annual_inc'] < 1000000]

# Remove extreme DTI values
df = df[df['dti'] < 60]

after_outliers = len(df)

print(f"[INFO] Outlier rows removed: {before_outliers - after_outliers}")

# ============================================================
# 8. FEATURE ENGINEERING
# ============================================================

print("\n[INFO] Creating engineered features...")

# -----------------------------
# Default Flag
# -----------------------------
default_statuses = [
    'CHARGED OFF',
    'DEFAULT',
    'DOES NOT MEET THE CREDIT POLICY. STATUS:CHARGED OFF'
]

df['is_default'] = (
    df['loan_status']
    .isin(default_statuses)
    .astype(int)
)

# -----------------------------
# Fully Paid Flag
# -----------------------------
df['is_fully_paid'] = (
    df['loan_status'] == 'FULLY PAID'
).astype(int)

# -----------------------------
# Risk Tier
# -----------------------------
risk_map = {
    'A': 'Low Risk',
    'B': 'Low Risk',
    'C': 'Medium Risk',
    'D': 'Medium Risk',
    'E': 'High Risk',
    'F': 'High Risk',
    'G': 'High Risk'
}

df['risk_tier'] = (
    df['grade']
    .map(risk_map)
    .fillna('Unknown')
)

# -----------------------------
# DTI Bands
# -----------------------------
dti_bins = [0, 10, 20, 30, 40, float('inf')]

dti_labels = [
    '0-10',
    '10-20',
    '20-30',
    '30-40',
    '40+'
]

df['dti_band'] = pd.cut(
    df['dti'],
    bins=dti_bins,
    labels=dti_labels,
    right=False
)

# -----------------------------
# Income Bands
# -----------------------------
inc_bins = [0, 40000, 75000, 120000, float('inf')]

inc_labels = [
    '<40K',
    '40K-75K',
    '75K-120K',
    '120K+'
]

df['income_band'] = pd.cut(
    df['annual_inc'],
    bins=inc_bins,
    labels=inc_labels,
    right=False
)

# -----------------------------
# Recovery Rate
# -----------------------------
df['recovery_rate'] = np.where(
    df['loan_amnt'] > 0,
    (
        df['recoveries']
        / df['loan_amnt']
        * 100
    ).round(2),
    0
)

df['recovery_rate'] = (
    df['recovery_rate']
    .fillna(0)
    .clip(0, 100)
)

# -----------------------------
# Employment Stability
# -----------------------------
df['emp_stable'] = (
    df['emp_length_num'] >= 5
).astype(int)

# -----------------------------
# High Income Flag
# -----------------------------
df['high_income'] = (
    df['annual_inc'] >= 100000
).astype(int)

# -----------------------------
# Net Gain Metric
# -----------------------------
df['net_gain'] = (
    df['total_rec_int']
    + df['recoveries']
) - (
    df['loan_amnt']
    - df['total_rec_prncp']
)

# ============================================================
# 9. FINAL CLEANUP
# ============================================================

print("\n[INFO] Final cleanup...")

fill_zero_cols = [
    'recoveries',
    'total_pymnt',
    'total_rec_prncp',
    'total_rec_int'
]

for col in fill_zero_cols:
    df[col] = df[col].fillna(0)

df['last_pymnt_d'] = df['last_pymnt_d'].fillna('Unknown')

# Drop unused columns
df.drop(columns=['issue_d'], inplace=True)

# ============================================================
# 10. FINAL SUMMARY
# ============================================================

print("\n================================================")
print("FINAL DATASET SUMMARY")
print("================================================")

print(f"Final shape: {df.shape}")

print(
    f"Default Rate: "
    f"{df['is_default'].mean() * 100:.2f}%"
)

print(
    f"Average Interest Rate: "
    f"{df['int_rate'].mean():.2f}%"
)

print("\nRisk Tier Distribution:")
print(df['risk_tier'].value_counts())

print("\nLoan Status Distribution:")
print(df['loan_status'].value_counts().head())

print("\nFinal Columns:")
print(list(df.columns))

print(
    f"\nFinal Memory Usage: "
    f"{df.memory_usage(deep=True).sum()/1024**2:.2f} MB"
)

# ============================================================
# 11. EXPORT CLEAN DATA
# ============================================================

print("\n[INFO] Exporting cleaned dataset...")

# ── CSV Export ───────────────────────────────────────────────
OUTPUT_PATH = r"C:\Users\SHIVA\Downloads\files\loan_cleaned.csv"

df.to_csv(
    OUTPUT_PATH,
    index=False
)

print(f"[SUCCESS] CSV saved to: {OUTPUT_PATH}")

# ── Optional Parquet Export ──────────────────────────────────
try:
    df.to_parquet(
        r"C:\Users\SHIVA\Downloads\files\loan_cleaned.parquet",
        index=False
    )
    print("[SUCCESS] Parquet exported: loan_cleaned.parquet")

except Exception:
    print(
        "[WARNING] Parquet export skipped "
        "(run: pip install pyarrow)"
    )


# ============================================================
# 12. EXPORT TO SQLITE
# ============================================================

import sqlite3

print("\n[INFO] Starting SQLite export...")

DB_PATH = r"C:\Users\SHIVA\Downloads\files\loan_portfolio.db"

try:
    conn = sqlite3.connect(DB_PATH)

    # Convert categorical columns to string
    # (SQLite doesn't support pandas Categorical dtype)
    cat_cols = df.select_dtypes(include='category').columns.tolist()
    for col in cat_cols:
        df[col] = df[col].astype(str)

    total_rows = len(df)
    print(f"[INFO] Inserting {total_rows:,} rows...")
    print("[INFO] This should take under 60 seconds. Please wait...")

    df.to_sql(
        name="loan_data",
        con=conn,
        if_exists="replace",    # drop & recreate table each run
        index=False,
        chunksize=5000          # inserts 5000 rows at a time
    )

    # Verify row count
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM loan_data")
    count = cursor.fetchone()[0]

    conn.close()

    print(f"[SUCCESS] SQLite export complete!")
    print(f"[SUCCESS] Rows inserted  : {count:,}")
    print(f"[SUCCESS] Database saved : {DB_PATH}")

except Exception as e:
    print(f"[ERROR] SQLite export failed: {e}")
    print("[INFO]  CSV is still saved — you can load that into Power BI directly")

# ============================================================
# DONE
# ============================================================

print("\n================================================")
print("PIPELINE COMPLETE")
print("================================================")
print("[SUCCESS] CSV ready        → loan_cleaned.csv")
print("[SUCCESS] SQLite ready     → loan_portfolio.db")
print("[INFO]    Next step        → Open loan_portfolio.db in DB Browser for SQLite")
print("[INFO]    Run queries      → Paste from loan_queries.sql into DB Browser")
print("[INFO]    Power BI         → Get Data → SQLite or load loan_cleaned.csv")