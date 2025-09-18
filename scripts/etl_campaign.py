import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime

# --- 1. Connect to PostgreSQL ---
# Replace YOUR_PASSWORD with your actual Postgres password
engine = create_engine('postgresql+psycopg2://postgres:pass1123@127.0.0.1:5432/marketing_campaign')

# --- 2. Load raw data from CSV (semicolon separated) ---
df = pd.read_csv('data/marketing_campaign.csv', sep=';')
df.columns = df.columns.str.strip()  # remove any leading/trailing spaces

# --- 3. Convert numeric columns ---
numeric_cols = [
    'Year_Birth', 'Income', 'Kidhome', 'Teenhome', 'Recency',
    'MntWines', 'MntFruits', 'MntMeatProducts', 'MntFishProducts',
    'MntSweetProducts', 'MntGoldProds', 'NumDealsPurchases',
    'NumWebPurchases', 'NumCatalogPurchases', 'NumStorePurchases',
    'NumWebVisitsMonth', 'AcceptedCmp1', 'AcceptedCmp2',
    'AcceptedCmp3', 'AcceptedCmp4', 'AcceptedCmp5', 'Complain',
    'Z_CostContact', 'Z_Revenue', 'Response'
]

for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# --- 4. Feature engineering ---
df['age'] = 2025 - df['Year_Birth']  # adjust to current year

# Age group
def age_group(a):
    if a < 25:
        return '<25'
    elif a <= 35:
        return '25-35'
    elif a <= 50:
        return '36-50'
    elif a <= 65:
        return '51-65'
    else:
        return '65+'

df['age_group'] = df['age'].apply(age_group)

# Income bracket
def income_bracket(x):
    if x < 40000:
        return 'Low'
    elif x < 70000:
        return 'Medium'
    elif x < 100000:
        return 'High'
    else:
        return 'Very High'

df['income_bracket'] = df['Income'].apply(income_bracket)

# Campaign response as boolean
df['campaign_response'] = df['Response'].apply(lambda x: True if x == 1 else False)

# Total money spent and total purchases
df['total_money_spent'] = df[['MntWines','MntFruits','MntMeatProducts','MntFishProducts','MntSweetProducts','MntGoldProds']].sum(axis=1)
df['total_purchases'] = df[['NumDealsPurchases','NumWebPurchases','NumCatalogPurchases','NumStorePurchases']].sum(axis=1)

# Convert date
df['date_sent'] = pd.to_datetime(df['Dt_Customer'], errors='coerce')
df['month_sent'] = df['date_sent'].dt.month
df['days_since_sent'] = (datetime.now() - df['date_sent']).dt.days

# --- 5. Select columns for analytics.customers ---
analytics_cols = [
    'age', 'age_group', 'education', 'marital_status', 'income', 'income_bracket', 
    'campaign_response', 'date_sent', 'month_sent', 'days_since_sent'
]

df_analytics = df_analytics[analytics_cols]

# --- 6. Load into analytics.customers ---
df_analytics.to_sql('customers', engine, schema='analytics', if_exists='append', index=False)

print("ETL completed successfully!")
