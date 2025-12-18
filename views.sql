-- views.sql
-- Reusable views for bank customer analytics
-- Run this file after creating your database and loading data

-- ============================================
-- CHURN ANALYSIS VIEWS
-- ============================================

-- View 1: Churn rate by branch
CREATE VIEW churn_by_branch AS
SELECT 
    branch,
    COUNT(*) AS num_customers,
    SUM(churned) AS churned_customers,
    AVG(churned) * 100 AS churn_rate_pct
FROM bank_customers
GROUP BY branch
ORDER BY churn_rate_pct DESC;

-- View 2: Churn by account type
CREATE VIEW churn_by_account_type AS
SELECT 
    account_type,
    COUNT(*) AS num_customers,
    SUM(churned) AS churned_customers,
    AVG(churned) * 100 AS churn_rate_pct
FROM bank_customers
GROUP BY account_type
ORDER BY churn_rate_pct DESC;

-- View 3: Income bands vs churn
CREATE VIEW income_band_churn AS
SELECT
    CASE
        WHEN income < 5000 THEN 'Low (<5k)'
        WHEN income BETWEEN 5000 AND 15000 THEN 'Middle (5k–15k)'
        ELSE 'High (>15k)'
    END AS income_band,
    COUNT(*) AS num_customers,
    SUM(churned) AS churned_customers,
    AVG(churned) * 100 AS churn_rate_pct,
    AVG(income) AS avg_income
FROM bank_customers
GROUP BY income_band
ORDER BY churn_rate_pct DESC;

-- ============================================
-- BALANCE & FINANCIAL VIEWS
-- ============================================

-- View 4: Average balance by branch
CREATE VIEW avg_balance_by_branch AS
SELECT 
    branch,
    COUNT(*) AS num_customers,
    AVG(balance) AS avg_balance,
    SUM(balance) AS total_balance,
    MIN(balance) AS min_balance,
    MAX(balance) AS max_balance
FROM bank_customers
GROUP BY branch
ORDER BY avg_balance DESC;

-- View 5: Average balance by account type
CREATE VIEW avg_balance_by_account_type AS
SELECT 
    account_type,
    COUNT(*) AS num_customers,
    AVG(balance) AS avg_balance,
    SUM(balance) AS total_balance
FROM bank_customers
GROUP BY account_type
ORDER BY avg_balance DESC;

-- View 6: Tenure vs average balance
CREATE VIEW balance_by_tenure AS
SELECT
    CASE
        WHEN tenure_years < 1 THEN 'New (<1y)'
        WHEN tenure_years BETWEEN 1 AND 3 THEN '1–3 years'
        WHEN tenure_years BETWEEN 3 AND 5 THEN '3–5 years'
        ELSE '5+ years'
    END AS tenure_group,
    COUNT(*) AS num_customers,
    AVG(balance) AS avg_balance,
    AVG(tenure_years) AS avg_tenure_years
FROM bank_customers
GROUP BY tenure_group
ORDER BY avg_balance DESC;

-- ============================================
-- CUSTOMER SEGMENTATION VIEWS
-- ============================================

-- View 7: Account type distribution
CREATE VIEW account_type_distribution AS
SELECT 
    account_type,
    COUNT(*) AS num_customers,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM bank_customers), 2) AS pct_of_total
FROM bank_customers
GROUP BY account_type
ORDER BY num_customers DESC;

-- View 8: Branch customer distribution
CREATE VIEW branch_distribution AS
SELECT 
    branch,
    COUNT(*) AS num_customers,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM bank_customers), 2) AS pct_of_total
FROM bank_customers
GROUP BY branch
ORDER BY num_customers DESC;

-- View 9: High-value customers (top 10% by balance)
CREATE VIEW high_value_customers AS
SELECT 
    customer_id,
    branch,
    account_type,
    age,
    income,
    balance,
    tenure_years,
    churned
FROM bank_customers
WHERE balance >= (SELECT balance FROM bank_customers ORDER BY balance DESC LIMIT 1 OFFSET (SELECT CAST(COUNT(*) * 0.1 AS INTEGER) FROM bank_customers))
ORDER BY balance DESC;

-- ============================================
-- SUMMARY / KPI VIEWS
-- ============================================

-- View 10: Overall KPIs (single row summary)
CREATE VIEW overall_kpis AS
SELECT 
    COUNT(*) AS total_customers,
    SUM(churned) AS total_churned,
    ROUND(AVG(churned) * 100, 2) AS overall_churn_rate_pct,
    ROUND(AVG(balance), 2) AS avg_balance,
    ROUND(SUM(balance), 2) AS total_balance,
    ROUND(AVG(income), 2) AS avg_income,
    ROUND(AVG(tenure_years), 2) AS avg_tenure_years,
    COUNT(DISTINCT branch) AS num_branches,
    COUNT(DISTINCT account_type) AS num_account_types
FROM bank_customers;

-- View 11: Branch performance summary (combines multiple metrics)
CREATE VIEW branch_performance AS
SELECT 
    b.branch,
    b.num_customers,
    b.churn_rate_pct,
    a.avg_balance,
    a.total_balance,
    ROUND(a.total_balance / b.num_customers, 2) AS balance_per_customer
FROM churn_by_branch b
JOIN avg_balance_by_branch a ON b.branch = a.branch
ORDER BY churn_rate_pct DESC;

