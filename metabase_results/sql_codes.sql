-- MoM Retention
WITH monthly_customers AS (
    SELECT 
        customer_id,
        DATE_FORMAT(transaction_date, '%Y-%m-01') AS month
    FROM transactions
    GROUP BY customer_id, month
),
retention AS (
    SELECT 
        a.month AS current_month,
        COUNT(DISTINCT a.customer_id) AS current_month_customers,
        COUNT(DISTINCT b.customer_id) AS retained_customers
    FROM monthly_customers a
    LEFT JOIN monthly_customers b
    ON a.customer_id = b.customer_id
    AND DATE_ADD(a.month, INTERVAL 1 MONTH) = b.month
    GROUP BY a.month
)
SELECT 
    current_month,
    CASE 
        WHEN current_month_customers = 0 THEN 0
        ELSE (retained_customers / current_month_customers) * 100 
    END AS retention_rate
FROM retention
ORDER BY current_month;

-- Retention Cohorts
WITH first_purchase AS (
    SELECT 
        customer_id,
        MIN(transaction_date) AS first_purchase_date
    FROM transactions
    GROUP BY customer_id
),
cohorts AS (
    SELECT 
        a.customer_id,
        DATE_FORMAT(a.first_purchase_date, '%Y-%m') AS cohort_month,
        DATE_FORMAT(b.transaction_date, '%Y-%m') AS transaction_month
    FROM first_purchase a
    INNER JOIN transactions b
    ON a.customer_id = b.customer_id
),
cohort_sizes AS (
    SELECT 
        cohort_month,
        COUNT(DISTINCT customer_id) AS cohort_size
    FROM cohorts
    GROUP BY cohort_month
)
SELECT 
    c.cohort_month,
    c.transaction_month,
    COUNT(DISTINCT c.customer_id) AS customers,
    (COUNT(DISTINCT c.customer_id) / cs.cohort_size) * 100 AS retention_rate
FROM cohorts c
INNER JOIN cohort_sizes cs
ON c.cohort_month = cs.cohort_month
GROUP BY c.cohort_month, c.transaction_month, cs.cohort_size
ORDER BY c.cohort_month, c.transaction_month;

-- Monthly Repurchase Rate
WITH monthly_purchase_counts AS (
    SELECT 
        customer_id,
        DATE_FORMAT(transaction_date, '%Y-%m') AS month,
        COUNT(transaction_id) AS purchase_count
    FROM transactions
    GROUP BY customer_id, month
),
monthly_repurchase_rate AS (
    SELECT 
        month,
        COUNT(CASE WHEN purchase_count > 1 THEN 1 END) / COUNT(*) * 100 AS repurchase_rate
    FROM monthly_purchase_counts
    GROUP BY month
)
SELECT 
    month,
    repurchase_rate
FROM monthly_repurchase_rate
ORDER BY month;