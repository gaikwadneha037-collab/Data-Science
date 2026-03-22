-- check tables in retail_analysis
show tables from retail_analysis;

-- final table
select * from online_retail_final;

-- total revenue 
select sum(price * quantity) as total_revenue
from online_retail_final;
 
-- Monthly revenue CTEs
with monthly_revenue as (
select date_format(InvoiceDate_ts,'%Y-%m') as month,
sum(price * quantity) as revenue
from online_retail_final
group by month) 
select * from monthly_revenue
order by month;

-- top customers & orders
select
count(distinct Invoice) as total_orders,
count(distinct CustomerID) as total_customers 
from online_retail_final;

-- Average Order Value Subquery
select AVG(order_value) as Avg_order_value 
from(
select Invoice,
sum(price * quantity) as order_value 
from online_retail_final
group by Invoice
) t;

-- top 10 products
SELECT *
FROM (
    SELECT
        StockCode,
        Description,
        SUM(Quantity * Price) AS revenue,
        RANK() OVER (ORDER BY SUM(Quantity * Price) DESC) AS rnk
    FROM online_retail_final
    GROUP BY StockCode, Description
) ranked
WHERE rnk <= 10;
