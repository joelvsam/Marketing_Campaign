import pandas as pd
import psycopg2
from psycopg2 import sql
import os
from dotenv import load_dotenv

load_dotenv('/app/backend/.env')

print("=" * 60)
print("LOADING DATA TO POSTGRESQL")
print("=" * 60)

# Database connection parameters
db_params = {
    'host': os.getenv('POSTGRES_HOST', 'localhost'),
    'port': os.getenv('POSTGRES_PORT', '5432'),
    'database': os.getenv('POSTGRES_DB', 'marketing_analytics'),
    'user': os.getenv('POSTGRES_USER', 'postgres'),
    'password': os.getenv('POSTGRES_PASSWORD', 'postgres')
}

print("\n[1/5] Connecting to PostgreSQL...")
try:
    conn = psycopg2.connect(**db_params)
    conn.autocommit = True
    cursor = conn.cursor()
    print(f"   ✓ Connected to {db_params['database']}")
except psycopg2.Error as e:
    print(f"   ✗ Connection failed: {e}")
    print("\n   Note: Ensure PostgreSQL is running with the following command:")
    print("   sudo service postgresql start")
    exit(1)

# Create table
print("\n[2/5] Creating marketing_campaigns table...")
create_table_query = """
DROP TABLE IF EXISTS marketing_campaigns;

CREATE TABLE marketing_campaigns (
    id INTEGER PRIMARY KEY,
    year_birth INTEGER,
    education VARCHAR(50),
    marital_status VARCHAR(50),
    income DECIMAL(10,2),
    kidhome INTEGER,
    teenhome INTEGER,
    dt_customer DATE,
    recency INTEGER,
    mnt_wines INTEGER,
    mnt_fruits INTEGER,
    mnt_meat_products INTEGER,
    mnt_fish_products INTEGER,
    mnt_sweet_products INTEGER,
    mnt_gold_prods INTEGER,
    num_deals_purchases INTEGER,
    num_web_purchases INTEGER,
    num_catalog_purchases INTEGER,
    num_store_purchases INTEGER,
    num_web_visits_month INTEGER,
    accepted_cmp3 INTEGER,
    accepted_cmp4 INTEGER,
    accepted_cmp5 INTEGER,
    accepted_cmp1 INTEGER,
    accepted_cmp2 INTEGER,
    complain INTEGER,
    z_cost_contact INTEGER,
    z_revenue INTEGER,
    response INTEGER,
    age INTEGER,
    total_spent DECIMAL(10,2),
    total_purchases INTEGER,
    total_children INTEGER,
    total_campaigns_accepted INTEGER,
    customer_tenure_days INTEGER,
    clv DECIMAL(10,2),
    income_group VARCHAR(20),
    age_group VARCHAR(20),
    customer_segment INTEGER,
    customer_segment_label VARCHAR(50)
);
"""

try:
    cursor.execute(create_table_query)
    print("   ✓ Table created successfully")
except psycopg2.Error as e:
    print(f"   ✗ Error creating table: {e}")
    conn.close()
    exit(1)

# Load cleaned data
print("\n[3/5] Loading cleaned data...")
df = pd.read_csv('/app/data/marketing_campaign_cleaned.csv')
print(f"   ✓ Loaded {len(df)} records")

# Prepare data for insertion
print("\n[4/5] Preparing data for insertion...")
df.columns = df.columns.str.lower()
df = df.rename(columns={
    'mntmeatproducts': 'mnt_meat_products',
    'mntfishproducts': 'mnt_fish_products',
    'mntsweetproducts': 'mnt_sweet_products',
    'mntgoldprods': 'mnt_gold_prods',
    'numdealspurchases': 'num_deals_purchases',
    'numwebpurchases': 'num_web_purchases',
    'numcatalogpurchases': 'num_catalog_purchases',
    'numstorepurchases': 'num_store_purchases',
    'numwebvisitsmonth': 'num_web_visits_month',
    'acceptedcmp1': 'accepted_cmp1',
    'acceptedcmp2': 'accepted_cmp2',
    'acceptedcmp3': 'accepted_cmp3',
    'acceptedcmp4': 'accepted_cmp4',
    'acceptedcmp5': 'accepted_cmp5',
    'z_costcontact': 'z_cost_contact',
    'totalspent': 'total_spent',
    'totalpurchases': 'total_purchases',
    'totalchildren': 'total_children',
    'totalcampaignsaccepted': 'total_campaigns_accepted',
    'customertenuredays': 'customer_tenure_days',
    'incomegroup': 'income_group',
    'agegroup': 'age_group',
    'customersegment': 'customer_segment',
    'customersegmentlabel': 'customer_segment_label'
})

# Replace NaN with None for SQL
df = df.where(pd.notnull(df), None)

# Insert data
print("\n[5/5] Inserting data into PostgreSQL...")
insert_query = """
INSERT INTO marketing_campaigns VALUES (
    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
)
"""

try:
    for idx, row in df.iterrows():
        cursor.execute(insert_query, tuple(row))
        if (idx + 1) % 100 == 0:
            print(f"   • Inserted {idx + 1}/{len(df)} records...", end='\r')
    print(f"   ✓ Inserted all {len(df)} records successfully" + " " * 20)
except psycopg2.Error as e:
    print(f"\n   ✗ Error inserting data: {e}")
    conn.close()
    exit(1)

# Verify data
print("\n" + "=" * 60)
print("VERIFICATION")
print("=" * 60)
cursor.execute("SELECT COUNT(*) FROM marketing_campaigns;")
count = cursor.fetchone()[0]
print(f"\nTotal records in database: {count}")

cursor.execute("SELECT customer_segment_label, COUNT(*) FROM marketing_campaigns GROUP BY customer_segment_label;")
print("\nCustomer Segments:")
for row in cursor.fetchall():
    print(f"  • {row[0]}: {row[1]} customers")

# Close connection
cursor.close()
conn.close()

print("\n✓ Data loaded to PostgreSQL successfully!")
print("=" * 60)