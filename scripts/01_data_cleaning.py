import pandas as pd
import numpy as np
from datetime import datetime
import os

print("=" * 60)
print("MARKETING CAMPAIGN DATA CLEANING SCRIPT")
print("=" * 60)

# Load the dataset
print("\n[1/6] Loading dataset")
df = pd.read_csv('/app/marketing_campaign.csv', sep=';', encoding='utf-8-sig')
print(f"Loaded {len(df)} records with {len(df.columns)} columns")

# Display basic info
print("\n[2/6] Analyzing data structure...")
print(f"   - Shape: {df.shape}")
print(f"   - Columns: {list(df.columns)}")
print(f"   - Missing values:")
missing = df.isnull().sum()
for col, count in missing[missing > 0].items():
    print(f"     • {col}: {count} ({count/len(df)*100:.2f}%)")

# Data Cleaning Steps
print("\n[3/6] Cleaning data")

# 1. Handle missing Income values
print("   - Handling missing Income values...")
if df['Income'].isnull().sum() > 0:
    median_income = df['Income'].median()
    df['Income'].fillna(median_income, inplace=True)
    print(f"Filled {df['Income'].isnull().sum()} missing values with median: ${median_income:,.2f}")

# 2. Clean Year_Birth - remove unrealistic values
print("Cleaning Year_Birth")
current_year = datetime.now().year
df = df[(df['Year_Birth'] >= 1940) & (df['Year_Birth'] <= current_year - 18)]
print(f"Removed records with invalid birth years")

# 3. Clean Marital_Status - standardize values
print("Standardizing Marital_Status")
marital_mapping = {
    'Married': 'Married',
    'Together': 'Married',
    'Single': 'Single',
    'Divorced': 'Divorced',
    'Widow': 'Widowed',
    'Alone': 'Single',
    'Absurd': 'Other',
    'YOLO': 'Other'
}
df['Marital_Status'] = df['Marital_Status'].map(marital_mapping)
print(f"Standardized marital status categories")

# 4. Feature Engineering
print("\n[4/6] Engineering new features...")

# Age
df['Age'] = current_year - df['Year_Birth']
print(f"Created Age column")

# Total Spending
spending_cols = ['MntWines', 'MntFruits', 'MntMeatProducts', 'MntFishProducts', 'MntSweetProducts', 'MntGoldProds']
df['TotalSpent'] = df[spending_cols].sum(axis=1)
print(f"Created TotalSpent column")

# Total Purchases
purchase_cols = ['NumWebPurchases', 'NumCatalogPurchases', 'NumStorePurchases']
df['TotalPurchases'] = df[purchase_cols].sum(axis=1)
print(f"Created TotalPurchases column")

# Total Children
df['TotalChildren'] = df['Kidhome'] + df['Teenhome']
print(f"Created TotalChildren column")

# Total Campaigns Accepted
campaign_cols = ['AcceptedCmp1', 'AcceptedCmp2', 'AcceptedCmp3', 'AcceptedCmp4', 'AcceptedCmp5']
df['TotalCampaignsAccepted'] = df[campaign_cols].sum(axis=1)
print(f"Created TotalCampaignsAccepted column")

# Customer Tenure (days)
df['Dt_Customer'] = pd.to_datetime(df['Dt_Customer'])
df['CustomerTenureDays'] = (datetime.now() - df['Dt_Customer']).dt.days
print(f"Created CustomerTenureDays column")

# Customer Lifetime Value (CLV)
df['CLV'] = df['TotalSpent'] / (df['CustomerTenureDays'] / 365.25)
df['CLV'] = df['CLV'].replace([np.inf, -np.inf], 0)
print(f"Created CLV (Customer Lifetime Value) column")

# Income Groups
df['IncomeGroup'] = pd.cut(df['Income'], 
                            bins=[0, 30000, 50000, 75000, 100000, float('inf')],
                            labels=['Low', 'Lower-Mid', 'Mid', 'Upper-Mid', 'High'])
print(f"Created IncomeGroup column")

# Age Groups
df['AgeGroup'] = pd.cut(df['Age'], 
                        bins=[0, 30, 40, 50, 60, float('inf')],
                        labels=['<30', '30-40', '40-50', '50-60', '60+'])
print(f"Created AgeGroup column")

# RFM Segmentation
print("\n[5/6] Performing RFM segmentation")
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

# Prepare RFM features
rfm_data = df[['Recency', 'TotalPurchases', 'TotalSpent']].copy()
scaler = StandardScaler()
rfm_scaled = scaler.fit_transform(rfm_data)

# K-Means clustering
kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
df['CustomerSegment'] = kmeans.fit_predict(rfm_scaled)

# Label segments based on characteristics
segment_labels = {0: 'Champions', 1: 'At Risk', 2: 'Potential', 3: 'Lost'}
df['CustomerSegmentLabel'] = df['CustomerSegment'].map(segment_labels)
print(f"   ✓ Created customer segments using K-Means clustering")

# Save cleaned data
print("\nSaving cleaned data")
output_path = '/app/data/marketing_campaign_cleaned.csv'
os.makedirs('/app/data', exist_ok=True)
df.to_csv(output_path, index=False)
print(f"Saved to {output_path}")

# Summary Statistics
print("\n" + "=" * 60)
print("CLEANING SUMMARY")
print("=" * 60)
print(f"Total Records: {len(df)}")
print(f"Total Features: {len(df.columns)}")
print(f"\nNew Features Created:")
print("  • Age, TotalSpent, TotalPurchases, TotalChildren")
print("  • TotalCampaignsAccepted, CustomerTenureDays, CLV")
print("  • IncomeGroup, AgeGroup, CustomerSegment")
print("\nData Quality:")
print(f"  • Missing Values: {df.isnull().sum().sum()}")
print(f"  • Duplicate Records: {df.duplicated().sum()}")
print("\n✓ Data cleaning completed successfully!")
print("=" * 60)