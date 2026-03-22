-- RFM segments customers based on Recency, Frequency, and Monetary value of purchases.
-- Recency (raw) → last purchase date
-- Frequency → number of orders
-- Monetary → total spend

-- final table
select * from online_retail_final;

-- rfm base table
with rfm_base as(
select CustomerID, 
max(InvoiceDate_ts) as last_purchase_date,
count(distinct Invoice) as frequency,
sum(price * quantity) as monetary
from online_retail_final 
group by CustomerID)
select * from rfm_base;

-- Calculate Recency in Days
with rfm_base as (
select customerid,
datediff(max(InvoiceDate_ts),'2011-12-09') * -1 AS recency_days,
count(distinct invoice) as frequency,
sum(price*quantity) as monetary
from online_retail_final 
group by CustomerID
)
select * from rfm_base;

-- rfm scores
WITH rfm_base AS (
    SELECT
        CustomerID,
        DATEDIFF('2011-12-09', MAX(InvoiceDate_ts)) AS recency,
        COUNT(DISTINCT Invoice) AS frequency,
        SUM(Quantity * Price) AS monetary
    FROM online_retail_final
    GROUP BY CustomerID
),
rfm_scores AS (
    SELECT *,
        NTILE(5) OVER (ORDER BY recency ASC)  AS r_score,
        NTILE(5) OVER (ORDER BY frequency DESC) AS f_score,
        NTILE(5) OVER (ORDER BY monetary DESC)  AS m_score
    FROM rfm_base
)
SELECT *
FROM rfm_scores;

-- Create RFM SEGMENTS
WITH rfm_base AS (
    SELECT
        CustomerID,
        DATEDIFF('2011-12-09', MAX(InvoiceDate_ts)) AS recency,
        COUNT(DISTINCT Invoice) AS frequency,
        SUM(Quantity * Price) AS monetary
    FROM online_retail_final
    GROUP BY CustomerID
),
rfm_scores AS (
    SELECT *,
        NTILE(5) OVER (ORDER BY recency ASC)  AS r_score,
        NTILE(5) OVER (ORDER BY frequency DESC) AS f_score,
        NTILE(5) OVER (ORDER BY monetary DESC)  AS m_score
    FROM rfm_base
)
SELECT *,
       CONCAT(r_score, f_score, m_score) AS rfm_score,
       CASE
           WHEN r_score >= 4 AND f_score >= 4 AND m_score >= 4 THEN 'Champions'
           WHEN r_score >= 3 AND f_score >= 3 THEN 'Loyal Customers'
           WHEN r_score >= 4 AND f_score <= 2 THEN 'New Customers'
           WHEN r_score <= 2 AND f_score >= 4 THEN 'At Risk'
           WHEN r_score <= 2 AND f_score <= 2 THEN 'Lost'
           ELSE 'Others'
       END AS rfm_segment
FROM rfm_scores;