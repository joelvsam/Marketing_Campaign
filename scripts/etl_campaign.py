import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime

# -----------------------------
# 1. Connect to PostgreSQL
# -----------------------------
engine = create_engine('postgresql+psycopg2://postgres:pass1123@127.0.0.1:5432/marketing_campaign')

# -----------------------------
# 2. Load CSV (semicolon separated)
# -----------------------------
df = pd.read_csv('data/marketing_campaign.csv', sep=';')
df.columns = df.columns.str.strip()  # remove leading/trailing spaces

# Check columns
print("Columns in CSV:", df.columns.tolist())

# -----------------------------
# 3. Rename columns consistently
# -----------------------------
df.rename(columns={
    'Education': 'education',
    'Marital_Status': 'marital_status',
    'Income': 'income',
    'Dt_Customer': 'dt_customer',
    'Response': 'response'
}, inplace=True)

# -----------------------------
# 4. Convert numeric columns
# -----------------------------
numeric_cols = [
    'Year_Birth', 'income', 'Kidhome', 'Teenhome', 'Recency',
    'MntWines', 'MntFruits', 'MntMeatProducts', 'MntFishProducts',
    'MntSweetProducts', 'MntGoldProds', 'NumDealsPurchases',
    'NumWebPurchases', 'NumCatalogPurchases', 'NumStorePurchases',
    'NumWebVisitsMonth', 'AcceptedCmp1', 'AcceptedCmp2',
    'AcceptedCmp3', 'AcceptedCmp4', 'AcceptedCmp5', 'Complain',
    'Z_CostContact', 'Z_Revenue', 'response'
]

for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# -----------------------------
# 5. Feature Engineering
# -----------------------------
# Age and Age Group
df['age'] = 2025 - df['Year_Birth']

def age_group(a):
    if a < 25: return '<25'
    elif a <= 35: return '25-35'
    elif a <= 50: return '36-50'
    elif a <= 65: return '51-65'
    else: return '65+'

df['age_group'] = df['age'].apply(age_group)

# Income Bracket
def income_bracket(x):
    if x < 40000: return 'Low'
    elif x < 70000: return 'Medium'
    elif x < 100000: return 'High'
    else: return 'Very High'

df['income_bracket'] = df['income'].apply(income_bracket)

# Campaign Response Boolean
df['campaign_response'] = df['response'].apply(lambda x: True if x == 1 else False)

# Date Features
df['date_sent'] = pd.to_datetime(df['dt_customer'], errors='coerce')
df['month_sent'] = df['date_sent'].dt.month
df['days_since_sent'] = (datetime.now() - df['date_sent']).dt.days

# -----------------------------
# 6. Prepare Analytics Table
# -----------------------------
analytics_cols = [
    'age', 'age_group', 'education', 'marital_status', 'income', 'income_bracket',
    'campaign_response', 'date_sent', 'month_sent', 'days_since_sent'
]

df_analytics = df[analytics_cols]

# -----------------------------
# 7. Load into PostgreSQL
# -----------------------------
df_analytics.to_sql(
    'customers',
    engine,
    schema='analytics',
    if_exists='replace',  # replaces the table, ensuring all columns exist
    index=False,
    method='multi'
)


print("ETL completed successfully!")
