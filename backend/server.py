from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.orm import Session
import os
import logging
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import List, Dict, Any
from database import get_db, engine

load_dotenv()

app = FastAPI(title="Marketing Analytics API")

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.getenv('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Pydantic models
class KPIResponse(BaseModel):
    total_customers: int
    total_revenue: float
    avg_customer_spend: float
    avg_clv: float
    response_rate: float

class SegmentData(BaseModel):
    segment: str
    count: int
    avg_spending: float
    avg_clv: float

class CampaignData(BaseModel):
    campaign: str
    acceptances: int
    rate: float

class ProductData(BaseModel):
    category: str
    revenue: float
    share: float

class ChannelData(BaseModel):
    channel: str
    purchases: int
    share: float

@app.get("/api/")
async def root():
    return {"message": "Marketing Analytics API", "status": "active"}

@app.get("/api/health")
async def health_check(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=503, detail="Database connection failed")

@app.get("/api/kpis", response_model=KPIResponse)
async def get_kpis(db: Session = Depends(get_db)):
    try:
        query = text("""
            SELECT 
                COUNT(*) as total_customers,
                ROUND(SUM(total_spent), 2) as total_revenue,
                ROUND(AVG(total_spent), 2) as avg_customer_spend,
                ROUND(AVG(clv), 2) as avg_clv,
                ROUND(AVG(CASE WHEN total_campaigns_accepted > 0 THEN 1 ELSE 0 END) * 100, 2) as response_rate
            FROM marketing_campaigns
        """)
        result = db.execute(query).fetchone()
        return {
            "total_customers": result[0],
            "total_revenue": float(result[1] or 0),
            "avg_customer_spend": float(result[2] or 0),
            "avg_clv": float(result[3] or 0),
            "response_rate": float(result[4] or 0)
        }
    except Exception as e:
        logger.error(f"Error fetching KPIs: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/segments", response_model=List[SegmentData])
async def get_segments(db: Session = Depends(get_db)):
    try:
        query = text("""
            SELECT 
                customer_segment_label as segment,
                COUNT(*) as count,
                ROUND(AVG(total_spent), 2) as avg_spending,
                ROUND(AVG(clv), 2) as avg_clv
            FROM marketing_campaigns
            GROUP BY customer_segment_label
            ORDER BY avg_clv DESC
        """)
        results = db.execute(query).fetchall()
        return [
            {
                "segment": row[0],
                "count": row[1],
                "avg_spending": float(row[2] or 0),
                "avg_clv": float(row[3] or 0)
            }
            for row in results
        ]
    except Exception as e:
        logger.error(f"Error fetching segments: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/campaigns", response_model=List[CampaignData])
async def get_campaigns(db: Session = Depends(get_db)):
    try:
        query = text("""
            SELECT 'Campaign 1' as campaign, SUM(accepted_cmp1) as acceptances, 
                   ROUND(AVG(accepted_cmp1) * 100, 2) as rate
            FROM marketing_campaigns
            UNION ALL
            SELECT 'Campaign 2', SUM(accepted_cmp2), ROUND(AVG(accepted_cmp2) * 100, 2)
            FROM marketing_campaigns
            UNION ALL
            SELECT 'Campaign 3', SUM(accepted_cmp3), ROUND(AVG(accepted_cmp3) * 100, 2)
            FROM marketing_campaigns
            UNION ALL
            SELECT 'Campaign 4', SUM(accepted_cmp4), ROUND(AVG(accepted_cmp4) * 100, 2)
            FROM marketing_campaigns
            UNION ALL
            SELECT 'Campaign 5', SUM(accepted_cmp5), ROUND(AVG(accepted_cmp5) * 100, 2)
            FROM marketing_campaigns
            ORDER BY rate DESC
        """)
        results = db.execute(query).fetchall()
        return [
            {
                "campaign": row[0],
                "acceptances": row[1],
                "rate": float(row[2] or 0)
            }
            for row in results
        ]
    except Exception as e:
        logger.error(f"Error fetching campaigns: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/products", response_model=List[ProductData])
async def get_products(db: Session = Depends(get_db)):
    try:
        query = text("""
            WITH product_revenue AS (
                SELECT 
                    'Wines' as category,
                    SUM(mnt_wines) as revenue
                FROM marketing_campaigns
                UNION ALL
                SELECT 'Meat', SUM(mnt_meat_products) FROM marketing_campaigns
                UNION ALL
                SELECT 'Fish', SUM(mnt_fish_products) FROM marketing_campaigns
                UNION ALL
                SELECT 'Gold', SUM(mnt_gold_prods) FROM marketing_campaigns
                UNION ALL
                SELECT 'Fruits', SUM(mnt_fruits) FROM marketing_campaigns
                UNION ALL
                SELECT 'Sweets', SUM(mnt_sweet_products) FROM marketing_campaigns
            )
            SELECT 
                category,
                revenue,
                ROUND(revenue * 100.0 / (SELECT SUM(revenue) FROM product_revenue), 2) as share
            FROM product_revenue
            ORDER BY revenue DESC
        """)
        results = db.execute(query).fetchall()
        return [
            {
                "category": row[0],
                "revenue": float(row[1] or 0),
                "share": float(row[2] or 0)
            }
            for row in results
        ]
    except Exception as e:
        logger.error(f"Error fetching products: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/channels", response_model=List[ChannelData])
async def get_channels(db: Session = Depends(get_db)):
    try:
        query = text("""
            WITH channel_purchases AS (
                SELECT 'Store' as channel, SUM(num_store_purchases) as purchases
                FROM marketing_campaigns
                UNION ALL
                SELECT 'Web', SUM(num_web_purchases) FROM marketing_campaigns
                UNION ALL
                SELECT 'Catalog', SUM(num_catalog_purchases) FROM marketing_campaigns
            )
            SELECT 
                channel,
                purchases,
                ROUND(purchases * 100.0 / (SELECT SUM(purchases) FROM channel_purchases), 2) as share
            FROM channel_purchases
            ORDER BY purchases DESC
        """)
        results = db.execute(query).fetchall()
        return [
            {
                "channel": row[0],
                "purchases": row[1],
                "share": float(row[2] or 0)
            }
            for row in results
        ]
    except Exception as e:
        logger.error(f"Error fetching channels: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/demographics")
async def get_demographics(db: Session = Depends(get_db)):
    try:
        age_query = text("""
            SELECT 
                age_group,
                COUNT(*) as customers,
                ROUND(AVG(total_spent), 2) as avg_spending
            FROM marketing_campaigns
            GROUP BY age_group
            ORDER BY age_group
        """)
        age_results = db.execute(age_query).fetchall()
        
        income_query = text("""
            SELECT 
                income_group,
                COUNT(*) as customers,
                ROUND(AVG(total_spent), 2) as avg_spending
            FROM marketing_campaigns
            GROUP BY income_group
            ORDER BY 
                CASE income_group
                    WHEN 'Low' THEN 1
                    WHEN 'Lower-Mid' THEN 2
                    WHEN 'Mid' THEN 3
                    WHEN 'Upper-Mid' THEN 4
                    WHEN 'High' THEN 5
                END
        """)
        income_results = db.execute(income_query).fetchall()
        
        return {
            "age_groups": [
                {"group": row[0], "customers": row[1], "avg_spending": float(row[2] or 0)}
                for row in age_results
            ],
            "income_groups": [
                {"group": row[0], "customers": row[1], "avg_spending": float(row[2] or 0)}
                for row in income_results
            ]
        }
    except Exception as e:
        logger.error(f"Error fetching demographics: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/insights")
async def get_insights(db: Session = Depends(get_db)):
    try:
        query = text("""
            SELECT 
                COUNT(*) as total_customers,
                ROUND(AVG(age), 0) as avg_age,
                ROUND(AVG(income), 2) as avg_income,
                ROUND(SUM(total_spent), 2) as total_revenue,
                (SELECT customer_segment_label FROM marketing_campaigns 
                 GROUP BY customer_segment_label ORDER BY COUNT(*) DESC LIMIT 1) as largest_segment,
                (SELECT COUNT(*) FROM marketing_campaigns WHERE total_spent > 1000) as high_spenders
            FROM marketing_campaigns
        """)
        result = db.execute(query).fetchone()
        
        return {
            "total_customers": result[0],
            "avg_age": int(result[1] or 0),
            "avg_income": float(result[2] or 0),
            "total_revenue": float(result[3] or 0),
            "largest_segment": result[4],
            "high_spenders": result[5]
        }
    except Exception as e:
        logger.error(f"Error fetching insights: {e}")
        raise HTTPException(status_code=500, detail=str(e))