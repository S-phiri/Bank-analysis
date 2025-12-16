SELECT
  branch,
  COUNT(*) AS num_customers,
  AVG(churned) * 100 AS churn_rate_pct
FROM bank_customers
GROUP BY branch
ORDER BY churn_rate_pct DESC;
