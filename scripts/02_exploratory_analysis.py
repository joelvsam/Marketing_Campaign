import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette('husl')

print("=" * 60)
print("EXPLORATORY DATA ANALYSIS")
print("=" * 60)

# Load cleaned data
print("\n[1/5] Loading cleaned data...")
df = pd.read_csv('/app/data/marketing_campaign_cleaned.csv')
print(f"   ✓ Loaded {len(df)} records")

# Create output directory for visualizations
os.makedirs('/app/data/visualizations', exist_ok=True)

# 1. Customer Demographics
print("\n[2/5] Analyzing customer demographics...")
print("\nAge Distribution:")
print(df['Age'].describe())
print("\nIncome Distribution:")
print(df['Income'].describe())
print("\nEducation Distribution:")
print(df['Education'].value_counts())
print("\nMarital Status Distribution:")
print(df['Marital_Status'].value_counts())

# 2. Spending Analysis
print("\n[3/5] Analyzing spending patterns...")
spending_cols = ['MntWines', 'MntFruits', 'MntMeatProducts', 'MntFishProducts', 'MntSweetProducts', 'MntGoldProds']
print("\nAverage Spending by Category:")
for col in spending_cols:
    print(f"  • {col.replace('Mnt', '')}: ${df[col].mean():,.2f}")

print(f"\nTotal Average Spending: ${df['TotalSpent'].mean():,.2f}")
print(f"Total Median Spending: ${df['TotalSpent'].median():,.2f}")

# 3. Campaign Performance
print("\n[4/5] Analyzing campaign performance...")
campaign_cols = ['AcceptedCmp1', 'AcceptedCmp2', 'AcceptedCmp3', 'AcceptedCmp4', 'AcceptedCmp5']
print("\nCampaign Acceptance Rates:")
for col in campaign_cols:
    rate = df[col].mean() * 100
    print(f"  • {col}: {rate:.2f}%")

total_response_rate = (df['TotalCampaignsAccepted'] > 0).mean() * 100
print(f"\nOverall Response Rate: {total_response_rate:.2f}%")

# 4. Channel Performance
print("\n[5/5] Analyzing purchase channels...")
channel_cols = ['NumWebPurchases', 'NumCatalogPurchases', 'NumStorePurchases']
print("\nAverage Purchases by Channel:")
for col in channel_cols:
    print(f"  • {col.replace('Num', '').replace('Purchases', '')}: {df[col].mean():.2f}")

# Customer Segmentation Analysis
print("\n" + "=" * 60)
print("CUSTOMER SEGMENTATION ANALYSIS")
print("=" * 60)
print("\nSegment Distribution:")
print(df['CustomerSegmentLabel'].value_counts())
print("\nSegment Characteristics:")
segment_analysis = df.groupby('CustomerSegmentLabel').agg({
    'Age': 'mean',
    'Income': 'mean',
    'TotalSpent': 'mean',
    'TotalPurchases': 'mean',
    'CLV': 'mean'
}).round(2)
print(segment_analysis)

# Key Insights
print("\n" + "=" * 60)
print("KEY INSIGHTS")
print("=" * 60)
print(f"\n1. Customer Base:")
print(f"   • Average Age: {df['Age'].mean():.0f} years")
print(f"   • Average Income: ${df['Income'].mean():,.2f}")
print(f"   • Most Common Education: {df['Education'].mode()[0]}")

print(f"\n2. Spending Behavior:")
print(f"   • Top Spending Category: Wines (${df['MntWines'].mean():,.2f})")
print(f"   • Average CLV: ${df['CLV'].mean():,.2f}")
print(f"   • High Spenders (>$1000): {(df['TotalSpent'] > 1000).sum()} ({(df['TotalSpent'] > 1000).mean()*100:.1f}%)")

print(f"\n3. Campaign Effectiveness:")
print(f"   • Best Campaign: Campaign {df[campaign_cols].sum().idxmax()[-1]}")
print(f"   • Average Campaigns Accepted: {df['TotalCampaignsAccepted'].mean():.2f}")
print(f"   • Never Responded: {(df['TotalCampaignsAccepted'] == 0).sum()} customers")

print(f"\n4. Purchase Channels:")
store_total = df['NumStorePurchases'].sum()
web_total = df['NumWebPurchases'].sum()
catalog_total = df['NumCatalogPurchases'].sum()
total = store_total + web_total + catalog_total
print(f"   • Store: {store_total/total*100:.1f}%")
print(f"   • Web: {web_total/total*100:.1f}%")
print(f"   • Catalog: {catalog_total/total*100:.1f}%")

print("\n✓ Exploratory analysis completed!")
print("=" * 60)