-- Create database (Postgres does not allow IF NOT EXISTS here)
CREATE DATABASE marketing_campaign;

-- Connect to the new database
\c marketing_campaign

-- Create schemas
CREATE SCHEMA IF NOT EXISTS staging;
CREATE SCHEMA IF NOT EXISTS analytics;

-- Create staging table
CREATE TABLE IF NOT EXISTS staging.customers_raw (
  source_file TEXT,
  raw_id BIGINT,
  customer_id TEXT,
  age TEXT,
  gender TEXT,
  income TEXT,
  campaign_response TEXT,
  channel TEXT,
  date_sent TEXT,
  ingested_at TIMESTAMP DEFAULT now()
);

-- Create analytics table
CREATE TABLE IF NOT EXISTS analytics.customers (
  customer_id BIGINT PRIMARY KEY,
  age INT,
  age_group TEXT,
  gender TEXT,
  income NUMERIC,
  income_bracket TEXT,
  campaign_response BOOLEAN,
  channel TEXT,
  date_sent DATE,
  month_sent INT,
  days_since_sent INT,
  created_at TIMESTAMP DEFAULT now(),
  updated_at TIMESTAMP DEFAULT now()
);
