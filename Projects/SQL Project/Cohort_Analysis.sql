-- Cohort analysis groups customers by their first purchase period and tracks their retention over time.

-- Find First Purchase (Customer Cohort)
with first_purchase as (
select customerid,
date_format(max(InvoiceDate_ts),'%Y-%m') as cohort_month
from online_retail_final
group by customerid)
select * from first_purchase;

-- Attach Cohort to Every Order (JOIN)
WITH first_purchase AS (
    SELECT
        CustomerID,
        DATE_FORMAT(MIN(InvoiceDate_ts), '%Y-%m') AS cohort_month
    FROM online_retail_final
    GROUP BY CustomerID
),
orders_with_cohort AS (
    SELECT
        o.CustomerID,
        DATE_FORMAT(o.InvoiceDate_ts, '%Y-%m') AS order_month,
        fp.cohort_month
    FROM online_retail_final o
    JOIN first_purchase fp
        ON o.CustomerID = fp.CustomerID
)
SELECT *
FROM orders_with_cohort;

-- Calculate Cohort Index (Month Number)
WITH first_purchase AS (
    SELECT
        CustomerID,
        DATE_FORMAT(MIN(InvoiceDate_ts), '%Y-%m') AS cohort_month,
        MIN(InvoiceDate_ts) AS cohort_date
    FROM online_retail_final
    GROUP BY CustomerID
),
orders_with_cohort AS (
    SELECT
        o.CustomerID,
        o.InvoiceDate_ts,
        DATE_FORMAT(o.InvoiceDate_ts, '%Y-%m') AS order_month,
        fp.cohort_month,
        fp.cohort_date
    FROM online_retail_final o
    JOIN first_purchase fp
        ON o.CustomerID = fp.CustomerID
),
cohort_index AS (
    SELECT
        CustomerID,
        cohort_month,
        order_month,
        PERIOD_DIFF(
            DATE_FORMAT(InvoiceDate_ts, '%Y%m'),
            DATE_FORMAT(cohort_date, '%Y%m')
        ) AS cohort_index
    FROM orders_with_cohort
)
SELECT
    cohort_month,
    cohort_index,
    COUNT(DISTINCT CustomerID) AS active_customers
FROM cohort_index
GROUP BY cohort_month, cohort_index
ORDER BY cohort_month, cohort_index;

-- Cohort Retention Table 
WITH first_purchase AS (
    SELECT
        CustomerID,
        MIN(InvoiceDate_ts) AS cohort_date,
        DATE_FORMAT(MIN(InvoiceDate_ts), '%Y-%m') AS cohort_month
    FROM online_retail_final
    GROUP BY CustomerID
),
orders_with_cohort AS (
    SELECT
        o.CustomerID,
        o.InvoiceDate_ts,
        fp.cohort_date,
        fp.cohort_month
    FROM online_retail_final o
    JOIN first_purchase fp
        ON o.CustomerID = fp.CustomerID
),
cohort_index AS (
    SELECT
        CustomerID,
        cohort_month,
        PERIOD_DIFF(
            DATE_FORMAT(InvoiceDate_ts, '%Y%m'),
            DATE_FORMAT(cohort_date, '%Y%m')
        ) AS cohort_index
    FROM orders_with_cohort
)
SELECT
    cohort_month,
    cohort_index,
    COUNT(DISTINCT CustomerID) AS active_customers
FROM cohort_index
GROUP BY cohort_month, cohort_index
ORDER BY cohort_month, cohort_index;

