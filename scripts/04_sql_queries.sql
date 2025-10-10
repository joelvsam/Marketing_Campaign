-- ============================================================
-- MARKETING CAMPAIGN ANALYSIS - SQL QUERIES
-- ============================================================

-- 1. CUSTOMER OVERVIEW KPIs
-- ============================================================

-- Total Customers
SELECT COUNT(*) as total_customers FROM marketing_campaigns;

-- Average Customer Lifetime Value
SELECT 
    ROUND(AVG(clv), 2) as avg_clv,
    ROUND(MAX(clv), 2) as max_clv,
    ROUND(MIN(clv), 2) as min_clv
FROM marketing_campaigns;

-- Total Revenue
SELECT 
    ROUND(SUM(total_spent), 2) as total_revenue,
    ROUND(AVG(total_spent), 2) as avg_customer_spend
FROM marketing_campaigns;


-- 2. CUSTOMER SEGMENTATION ANALYSIS
-- ============================================================

-- Customer Segments Distribution
SELECT 
    customer_segment_label,
    COUNT(*) as customer_count,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM marketing_campaigns), 2) as percentage
FROM marketing_campaigns
GROUP BY customer_segment_label
ORDER BY customer_count DESC;

-- Segment Performance Metrics
SELECT 
    customer_segment_label,
    COUNT(*) as customers,
    ROUND(AVG(age), 0) as avg_age,
    ROUND(AVG(income), 2) as avg_income,
    ROUND(AVG(total_spent), 2) as avg_spending,
    ROUND(AVG(total_purchases), 2) as avg_purchases,
    ROUND(AVG(clv), 2) as avg_clv
FROM marketing_campaigns
GROUP BY customer_segment_label
ORDER BY avg_clv DESC;


-- 3. CAMPAIGN PERFORMANCE ANALYSIS
-- ============================================================

-- Overall Campaign Response Rates
SELECT 
    'Campaign 1' as campaign,
    SUM(accepted_cmp1) as acceptances,
    ROUND(AVG(accepted_cmp1) * 100, 2) as acceptance_rate_pct
FROM marketing_campaigns
UNION ALL
SELECT 
    'Campaign 2',
    SUM(accepted_cmp2),
    ROUND(AVG(accepted_cmp2) * 100, 2)
FROM marketing_campaigns
UNION ALL
SELECT 
    'Campaign 3',
    SUM(accepted_cmp3),
    ROUND(AVG(accepted_cmp3) * 100, 2)
FROM marketing_campaigns
UNION ALL
SELECT 
    'Campaign 4',
    SUM(accepted_cmp4),
    ROUND(AVG(accepted_cmp4) * 100, 2)
FROM marketing_campaigns
UNION ALL
SELECT 
    'Campaign 5',
    SUM(accepted_cmp5),
    ROUND(AVG(accepted_cmp5) * 100, 2)
FROM marketing_campaigns
ORDER BY acceptance_rate_pct DESC;

-- Campaign Effectiveness by Customer Segment
SELECT 
    customer_segment_label,
    ROUND(AVG(total_campaigns_accepted), 2) as avg_campaigns_accepted,
    ROUND(AVG(CASE WHEN total_campaigns_accepted > 0 THEN 1 ELSE 0 END) * 100, 2) as response_rate_pct
FROM marketing_campaigns
GROUP BY customer_segment_label
ORDER BY avg_campaigns_accepted DESC;


-- 4. PRODUCT CATEGORY ANALYSIS
-- ============================================================

-- Revenue by Product Category
SELECT 
    'Wines' as category,
    ROUND(SUM(mnt_wines), 2) as total_revenue,
    ROUND(AVG(mnt_wines), 2) as avg_per_customer,
    ROUND(SUM(mnt_wines) * 100.0 / (SELECT SUM(total_spent) FROM marketing_campaigns), 2) as revenue_share_pct
FROM marketing_campaigns
UNION ALL
SELECT 
    'Meat Products',
    ROUND(SUM(mnt_meat_products), 2),
    ROUND(AVG(mnt_meat_products), 2),
    ROUND(SUM(mnt_meat_products) * 100.0 / (SELECT SUM(total_spent) FROM marketing_campaigns), 2)
FROM marketing_campaigns
UNION ALL
SELECT 
    'Fish Products',
    ROUND(SUM(mnt_fish_products), 2),
    ROUND(AVG(mnt_fish_products), 2),
    ROUND(SUM(mnt_fish_products) * 100.0 / (SELECT SUM(total_spent) FROM marketing_campaigns), 2)
FROM marketing_campaigns
UNION ALL
SELECT 
    'Gold Products',
    ROUND(SUM(mnt_gold_prods), 2),
    ROUND(AVG(mnt_gold_prods), 2),
    ROUND(SUM(mnt_gold_prods) * 100.0 / (SELECT SUM(total_spent) FROM marketing_campaigns), 2)
FROM marketing_campaigns
UNION ALL
SELECT 
    'Fruits',
    ROUND(SUM(mnt_fruits), 2),
    ROUND(AVG(mnt_fruits), 2),
    ROUND(SUM(mnt_fruits) * 100.0 / (SELECT SUM(total_spent) FROM marketing_campaigns), 2)
FROM marketing_campaigns
UNION ALL
SELECT 
    'Sweet Products',
    ROUND(SUM(mnt_sweet_products), 2),
    ROUND(AVG(mnt_sweet_products), 2),
    ROUND(SUM(mnt_sweet_products) * 100.0 / (SELECT SUM(total_spent) FROM marketing_campaigns), 2)
FROM marketing_campaigns
ORDER BY total_revenue DESC;


-- 5. CHANNEL PERFORMANCE ANALYSIS
-- ============================================================

-- Purchases by Channel
SELECT 
    'Store' as channel,
    SUM(num_store_purchases) as total_purchases,
    ROUND(AVG(num_store_purchases), 2) as avg_per_customer,
    ROUND(SUM(num_store_purchases) * 100.0 / 
        (SELECT SUM(total_purchases) FROM marketing_campaigns), 2) as channel_share_pct
FROM marketing_campaigns
UNION ALL
SELECT 
    'Web',
    SUM(num_web_purchases),
    ROUND(AVG(num_web_purchases), 2),
    ROUND(SUM(num_web_purchases) * 100.0 / 
        (SELECT SUM(total_purchases) FROM marketing_campaigns), 2)
FROM marketing_campaigns
UNION ALL
SELECT 
    'Catalog',
    SUM(num_catalog_purchases),
    ROUND(AVG(num_catalog_purchases), 2),
    ROUND(SUM(num_catalog_purchases) * 100.0 / 
        (SELECT SUM(total_purchases) FROM marketing_campaigns), 2)
FROM marketing_campaigns
ORDER BY total_purchases DESC;


-- 6. DEMOGRAPHIC ANALYSIS
-- ============================================================

-- Spending by Age Group
SELECT 
    age_group,
    COUNT(*) as customers,
    ROUND(AVG(income), 2) as avg_income,
    ROUND(AVG(total_spent), 2) as avg_spending,
    ROUND(SUM(total_spent), 2) as total_revenue
FROM marketing_campaigns
GROUP BY age_group
ORDER BY age_group;

-- Spending by Income Group
SELECT 
    income_group,
    COUNT(*) as customers,
    ROUND(AVG(total_spent), 2) as avg_spending,
    ROUND(SUM(total_spent), 2) as total_revenue
FROM marketing_campaigns
GROUP BY income_group
ORDER BY 
    CASE income_group
        WHEN 'Low' THEN 1
        WHEN 'Lower-Mid' THEN 2
        WHEN 'Mid' THEN 3
        WHEN 'Upper-Mid' THEN 4
        WHEN 'High' THEN 5
    END;

-- Education Level Impact
SELECT 
    education,
    COUNT(*) as customers,
    ROUND(AVG(income), 2) as avg_income,
    ROUND(AVG(total_spent), 2) as avg_spending,
    ROUND(AVG(total_campaigns_accepted), 2) as avg_campaign_response
FROM marketing_campaigns
GROUP BY education
ORDER BY avg_spending DESC;


-- 7. HIGH-VALUE CUSTOMERS
-- ============================================================

-- Top 20 Customers by Lifetime Value
SELECT 
    id,
    age,
    income,
    total_spent,
    total_purchases,
    clv,
    customer_segment_label
FROM marketing_campaigns
ORDER BY clv DESC
LIMIT 20;

-- High Spenders (Top 10%)
SELECT 
    COUNT(*) as high_spender_count,
    ROUND(AVG(total_spent), 2) as avg_spending,
    ROUND(SUM(total_spent), 2) as total_revenue,
    ROUND(SUM(total_spent) * 100.0 / (SELECT SUM(total_spent) FROM marketing_campaigns), 2) as revenue_share_pct
FROM marketing_campaigns
WHERE total_spent > (SELECT PERCENTILE_CONT(0.9) WITHIN GROUP (ORDER BY total_spent) FROM marketing_campaigns);


-- 8. CUSTOMER RETENTION INSIGHTS
-- ============================================================

-- Customers by Recency
SELECT 
    CASE 
        WHEN recency <= 30 THEN 'Active (0-30 days)'
        WHEN recency <= 60 THEN 'Recent (31-60 days)'
        WHEN recency <= 90 THEN 'At Risk (61-90 days)'
        ELSE 'Inactive (90+ days)'
    END as recency_category,
    COUNT(*) as customer_count,
    ROUND(AVG(total_spent), 2) as avg_spending,
    ROUND(AVG(clv), 2) as avg_clv
FROM marketing_campaigns
GROUP BY recency_category
ORDER BY 
    CASE recency_category
        WHEN 'Active (0-30 days)' THEN 1
        WHEN 'Recent (31-60 days)' THEN 2
        WHEN 'At Risk (61-90 days)' THEN 3
        WHEN 'Inactive (90+ days)' THEN 4
    END;


-- 9. FAMILY COMPOSITION IMPACT
-- ============================================================

-- Spending by Family Size
SELECT 
    total_children as number_of_children,
    COUNT(*) as customers,
    ROUND(AVG(total_spent), 2) as avg_spending,
    ROUND(AVG(income), 2) as avg_income
FROM marketing_campaigns
GROUP BY total_children
ORDER BY total_children;


-- 10. COMPLAINT ANALYSIS
-- ============================================================

-- Impact of Complaints on Customer Behavior
SELECT 
    CASE WHEN complain = 1 THEN 'Complained' ELSE 'No Complaint' END as complaint_status,
    COUNT(*) as customers,
    ROUND(AVG(total_spent), 2) as avg_spending,
    ROUND(AVG(total_campaigns_accepted), 2) as avg_campaign_response,
    ROUND(AVG(recency), 2) as avg_recency
FROM marketing_campaigns
GROUP BY complaint_status;