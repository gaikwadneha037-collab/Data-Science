-- Final table
select * from online_retail_final;

-- high-level understanding of transactions, customers, and products
select count(*) as total_rows,
count(distinct Invoice) as total_invoice,
count(distinct StockCode) as total_stockcode,
count(distinct CustomerID) as total_customers
from online_retail_final;

-- check Date span  
select 
min(InvoiceDate_ts) as startdate,
max(InvoiceDate_ts) as enddate
from online_retail_final;

-- check the revenue
select 
sum(Quantity * price) as total_revenue,
AVG(quantity * price) as avg_revenue
from online_retail_final;

-- negative analysis of quantity
select
count(*) as return_rows,
sum(quantity) as total_quantity_returned
from online_retail_final
where Quantity < 0;

-- country disctibution
select
country,
count(*) as transactions,
sum(price * Quantity) as total_revenue
from online_retail_final
where Quantity > 0
group by Country 
order by total_revenue desc ;

-- top products sold
select
stockcode,
description,
sum(Quantity) as units_sold,
sum(Quantity*price) as revenue
from online_retail_final
group by stockcode, description
order by revenue desc
limit 10;

-- top customers
select 
customerid,
count(distinct invoice) as total_orders,
sum(quantity* price) as revenue
from online_retail_final
where Quantity > 0
group by CustomerID
order by revenue desc
limit 10;