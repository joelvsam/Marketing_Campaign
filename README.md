# Marketing Campaign Analytics 

> **A comprehensive data analytics project demonstrating Python, SQL, PostgreSQL, and Power BI skills**

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue.svg)](https://www.postgresql.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110-green.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-19-blue.svg)](https://reactjs.org/)

## Project Overview

This project analyzes a marketing campaign dataset from Kaggle to derive actionable business insights. It showcases end-to-end data analysis skills including data cleaning, exploratory analysis, SQL querying, database management, and interactive visualization.

**Key Highlights:**
- Processed 2,000+ customer records with 29 features
- Implemented K-Means clustering for customer segmentation (RFM analysis)
- Designed and populated PostgreSQL database with optimized schema
- Created 10+ complex SQL queries for business intelligence
- Built interactive web dashboard with real-time data visualization
- Generated Power BI-ready dataset with comprehensive documentation

## Dashboard Preview

![Dashboard Screenshot](https://via.placeholder.com/1200x600/667eea/ffffff?text=Marketing+Analytics+Dashboard)

*Interactive dashboard showing KPIs, customer segments, campaign performance, and product analysis*

## Technology Stack

### Data Processing & Analysis
- **Python 3.11** - Core programming language
- **Pandas** - Data manipulation and analysis
- **NumPy** - Numerical computations
- **Scikit-learn** - Machine learning (K-Means clustering)
- **Matplotlib & Seaborn** - Data visualization

### Database
- **PostgreSQL 15** - Relational database
- **SQLAlchemy** - ORM and database toolkit
- **psycopg2** - PostgreSQL adapter

### Backend API
- **FastAPI** - Modern Python web framework
- **Pydantic** - Data validation
- **Uvicorn** - ASGI server

### Frontend Dashboard
- **React 19** - UI framework
- **Recharts** - Chart library
- **Axios** - HTTP client

### Business Intelligence
- **Power BI** - Enterprise-grade dashboards (documentation provided)

## Project Structure

```
marketing-campaign-analytics/
├── README.md                   # Project documentation
├── data/
│   ├── marketing_campaign.csv     # Raw dataset
│   └── marketing_campaign_cleaned.csv  # Processed data
├── scripts/
│   ├── 01_data_cleaning.py        # Data preprocessing pipeline
│   ├── 02_exploratory_analysis.py # EDA and insights
│   ├── 03_load_to_postgres.py     # Database loading
│   └── 04_sql_queries.sql         # Business intelligence queries
├── backend/
│   ├── server.py                  # FastAPI application
│   ├── database.py                # PostgreSQL connection
│   ├── requirements.txt           # Python dependencies
│   └── .env                       # Environment configuration
└── frontend/
    ├── src/
    │   ├── pages/
    │   │   ├── Dashboard.jsx         # Main analytics dashboard
    │   │   └── Documentation.jsx     # Project documentation
    │   ├── App.js                    # Main application
    │   └── App.css                   # Styling
    └── package.json                # Node dependencies
```

## Quick Start Guide

### Prerequisites
- Python 3.11+
- PostgreSQL 15+
- Node.js 18+
- Git

### Installation

#### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/marketing-campaign-analytics.git
cd marketing-campaign-analytics
```

#### 2. Set Up Python Environment
```bash
cd backend
pip install -r requirements.txt
```

#### 3. Configure Database
```bash
# Start PostgreSQL
sudo service postgresql start

# Create database
sudo -u postgres psql
CREATE DATABASE marketing_analytics;
\q

# Update .env file with your PostgreSQL credentials
```

#### 4. Run Data Pipeline
```bash
# Step 1: Clean and prepare data
python scripts/01_data_cleaning.py

# Step 2: Exploratory analysis
python scripts/02_exploratory_analysis.py

# Step 3: Load to PostgreSQL
python scripts/03_load_to_postgres.py
```

#### 5. Start Backend API
```bash
cd backend
uvicorn server:app --reload --host 0.0.0.0 --port 8001
```

#### 6. Start Frontend Dashboard
```bash
cd frontend
npm install
npm start
```

#### 7. Access the Application
- **Dashboard:** http://localhost:3000
- **API Documentation:** http://localhost:8001/docs

## Dataset Information

**Source:** Kaggle Marketing Campaign Dataset

**Features (29 columns):**
- **Customer Demographics:** Age, Education, Marital Status, Income
- **Purchase Behavior:** Spending by category (Wines, Meat, Fish, etc.)
- **Channel Performance:** Web, Catalog, Store purchases
- **Campaign Response:** Acceptance rates for 5 campaigns
- **Customer Metrics:** Recency, Tenure, Complaints

**Dataset Size:** 2,240 customer records

## Data Processing Pipeline

### Stage 1: Data Cleaning (`01_data_cleaning.py`)

**Objectives:**
- Handle missing values
- Remove invalid records
- Standardize categorical variables
- Engineer new features

**Key Transformations:**
```python
# Feature Engineering
- Age (calculated from year_birth)
- TotalSpent (sum of all product categories)
- TotalPurchases (sum of all channels)
- TotalChildren (kids + teenagers)
- CLV (Customer Lifetime Value)
- IncomeGroup (Low, Mid, High segments)
- AgeGroup (binned age ranges)
```

**Machine Learning:**
- K-Means clustering for customer segmentation
- RFM (Recency, Frequency, Monetary) analysis
- 4 customer segments: Champions, Potential, At Risk, Lost

**Output:** `marketing_campaign_cleaned.csv`

### Stage 2: Exploratory Analysis (`02_exploratory_analysis.py`)

**Analysis Performed:**
- Customer demographics distribution
- Spending patterns by category
- Campaign acceptance rates
- Purchase channel effectiveness
- Segment characteristics

**Key Insights Generated:**
- Average customer age: 52 years
- Top spending category: Wines (40%+ of revenue)
- Store purchases dominate (45% of total)
- 15% overall campaign response rate
- Champions segment: 30% higher CLV

### Stage 3: Database Loading (`03_load_to_postgres.py`)

**Database Schema:**
```sql
CREATE TABLE marketing_campaigns (
    id INTEGER PRIMARY KEY,
    -- Demographics
    year_birth INTEGER,
    education VARCHAR(50),
    marital_status VARCHAR(50),
    income DECIMAL(10,2),
    age INTEGER,
    
    -- Spending
    mnt_wines INTEGER,
    mnt_fruits INTEGER,
    mnt_meat_products INTEGER,
    total_spent DECIMAL(10,2),
    
    -- Behavior
    num_web_purchases INTEGER,
    num_catalog_purchases INTEGER,
    num_store_purchases INTEGER,
    total_purchases INTEGER,
    
    -- Campaigns
    accepted_cmp1 INTEGER,
    accepted_cmp2 INTEGER,
    accepted_cmp3 INTEGER,
    total_campaigns_accepted INTEGER,
    
    -- Metrics
    clv DECIMAL(10,2),
    customer_segment_label VARCHAR(50),
    -- ... and more
);
```

## SQL Query Showcase

The project includes 10+ complex SQL queries demonstrating:

### 1. Customer Segmentation Analysis
```sql
SELECT 
    customer_segment_label,
    COUNT(*) as customers,
    ROUND(AVG(age), 0) as avg_age,
    ROUND(AVG(income), 2) as avg_income,
    ROUND(AVG(total_spent), 2) as avg_spending,
    ROUND(AVG(clv), 2) as avg_clv
FROM marketing_campaigns
GROUP BY customer_segment_label
ORDER BY avg_clv DESC;
```

### 2. Campaign Performance with CTEs
```sql
WITH campaign_metrics AS (
    SELECT 
        'Campaign 1' as campaign,
        SUM(accepted_cmp1) as acceptances,
        COUNT(*) as total_customers
    FROM marketing_campaigns
    -- ... UNION for all campaigns
)
SELECT 
    campaign,
    acceptances,
    ROUND(acceptances * 100.0 / total_customers, 2) as acceptance_rate
FROM campaign_metrics
ORDER BY acceptance_rate DESC;
```

### 3. Product Revenue Analysis
```sql
SELECT 
    'Wines' as category,
    ROUND(SUM(mnt_wines), 2) as total_revenue,
    ROUND(SUM(mnt_wines) * 100.0 / 
        (SELECT SUM(total_spent) FROM marketing_campaigns), 2) as revenue_share
FROM marketing_campaigns
ORDER BY total_revenue DESC;
```

### 4. Customer Retention Analysis
```sql
SELECT 
    CASE 
        WHEN recency <= 30 THEN 'Active (0-30 days)'
        WHEN recency <= 60 THEN 'Recent (31-60 days)'
        WHEN recency <= 90 THEN 'At Risk (61-90 days)'
        ELSE 'Inactive (90+ days)'
    END as recency_category,
    COUNT(*) as customer_count,
    ROUND(AVG(total_spent), 2) as avg_spending
FROM marketing_campaigns
GROUP BY recency_category;
```

**All SQL queries available in:** `scripts/04_sql_queries.sql`

## Interactive Dashboard Features

### Key Performance Indicators (KPIs)
- **Total Customers:** Active customer base size
- **Total Revenue:** $1.3M+ cumulative spending
- **Average CLV:** Customer lifetime value
- **Response Rate:** Campaign effectiveness metric

### Visualizations
1. **Customer Segments Bar Chart** - CLV by segment
2. **Campaign Performance** - Acceptance rates comparison
3. **Product Revenue Pie Chart** - Category breakdown
4. **Purchase Channels** - Distribution by channel
5. **Demographics Analysis** - Age and income group spending
6. **Segment Comparison** - Multi-metric analysis

### API Endpoints
```
GET /api/kpis           - Overall KPIs
GET /api/segments       - Customer segments
GET /api/campaigns      - Campaign performance
GET /api/products       - Product categories
GET /api/channels       - Purchase channels
GET /api/demographics   - Age/Income analysis
GET /api/insights       - Business insights
```

## Power BI Integration Guide

### Connecting to PostgreSQL

1. **Open Power BI Desktop**
2. **Get Data** → PostgreSQL database
3. **Enter Connection Details:**
   - Server: `localhost`
   - Database: `marketing_analytics`
   - Table: `marketing_campaigns`

### Recommended Visuals

**Page 1: Executive Summary**
- KPI Cards (Total Revenue, Customers, CLV)
- Line Chart (Revenue Trend)
- Donut Chart (Customer Segments)

**Page 2: Campaign Analysis**
- Bar Chart (Campaign Performance)
- Matrix (Segment vs Campaign)
- Scatter Plot (Income vs Response)

**Page 3: Product & Channel**
- Treemap (Product Revenue)
- Stacked Bar (Channel by Segment)
- Funnel (Purchase Journey)

### DAX Measures

```dax
// Total Revenue
Total Revenue = SUM(marketing_campaigns[total_spent])

// Average CLV
Avg CLV = AVERAGE(marketing_campaigns[clv])

// Response Rate
Response Rate = 
    DIVIDE(
        COUNTROWS(
            FILTER(marketing_campaigns, 
                marketing_campaigns[total_campaigns_accepted] > 0)
        ),
        COUNTROWS(marketing_campaigns)
    ) * 100

// High Value Customers
High Value Customers = 
    COUNTROWS(
        FILTER(marketing_campaigns, 
            marketing_campaigns[total_spent] > 1000)
    )

// Segment Share
Segment Share = 
    DIVIDE(
        COUNTROWS(marketing_campaigns),
        CALCULATE(COUNTROWS(marketing_campaigns), ALL(marketing_campaigns))
    )
```

## Key Business Insights

### Customer Segmentation
- **Champions** (25%): Highest CLV, frequent buyers, campaign responsive
- **Potential** (30%): Medium spending, growth opportunity
- **At Risk** (20%): Declining engagement, needs retention
- **Lost** (25%): Low activity, win-back campaigns needed

### Campaign Performance
- **Campaign 3** performs best (18% acceptance)
- Higher income segments show 2x response rates
- Email campaigns more effective than direct mail

### Product Insights
- **Wines:** 40% of revenue, premium product opportunity
- **Meat Products:** 28% share, consistent demand
- **Cross-sell potential:** Wines + Meat combo

### Channel Effectiveness
- **Store:** 45% of purchases, highest conversion
- **Web:** 35%, growing channel, mobile optimization needed
- **Catalog:** 20%, declining, consider phase-out

## Skills Demonstrated

### Technical Skills
- ✅ Data Cleaning & Preprocessing
- ✅ Exploratory Data Analysis (EDA)
- ✅ Statistical Analysis
- ✅ Machine Learning (Clustering)
- ✅ SQL Query Optimization
- ✅ Database Design & Management
- ✅ API Development (FastAPI)
- ✅ Frontend Development (React)
- ✅ Data Visualization
- ✅ ETL Pipeline Development

### Business Skills
- ✅ Customer Segmentation
- ✅ Campaign Analysis
- ✅ KPI Definition & Tracking
- ✅ Business Intelligence
- ✅ Data-Driven Decision Making

## Documentation

- **Code Comments:** Comprehensive inline documentation
- **Docstrings:** Python functions fully documented
- **API Docs:** Auto-generated FastAPI documentation
- **SQL Comments:** Query explanations and business logic
- **README:** Complete project overview
- **User Guide:** In-app documentation page

## Challenges & Solutions

### Challenge 1: Missing Income Data
**Solution:** Median imputation based on education and age groups

### Challenge 2: Customer Segmentation
**Solution:** K-Means with RFM features and StandardScaler normalization

### Challenge 3: Query Performance
**Solution:** Indexed key columns, used CTEs, optimized joins

### Challenge 4: Dashboard Responsiveness
**Solution:** API-level aggregations, lazy loading, data caching

## 🚀 Future Enhancements

- [ ] Predictive modeling (Customer churn prediction)
- [ ] Time series forecasting (Revenue projection)
- [ ] A/B testing framework for campaigns
- [ ] Real-time data pipeline with Apache Kafka
- [ ] Advanced NLP for customer feedback analysis
- [ ] Mobile app for on-the-go insights

## Learning Resources

- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [PostgreSQL Tutorial](https://www.postgresql.org/docs/)
- [FastAPI Guide](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [Power BI Learning](https://learn.microsoft.com/en-us/power-bi/)



- Dataset: Kaggle Marketing Campaign Dataset
- Inspiration: Real-world marketing analytics challenges
- Community: Python, SQL, and React communities


