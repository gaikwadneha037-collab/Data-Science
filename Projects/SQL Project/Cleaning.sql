-- table to be clean
select * from online_retail_ii;

-- create a clean table 
Create table online_retail_clean as
select * from online_retail_ii 
where quantity > 0 and price > 0 
and customerid is not null;

-- check clean table 
select * from online_retail_clean;

-- verify the clean table
select 
count(*) as clean_rows,
Sum(case when Quantity <= 0 then 1 else 0 end) as bad_qty,
Sum(case when Price <= 0 then 1 else 0 end) as bad_price
from online_retail_clean;

-- check duplicates
select 
invoice,stockcode,invoicedate,customerid,count(*) as cnt
from online_retail_clean
group by invoice,stockcode,invoicedate,customerid
having count(*) >1 ;

-- remove duplicates
CREATE TABLE online_retail_dedup AS
SELECT *
FROM (
    SELECT *,
           ROW_NUMBER() OVER (
               PARTITION BY
                   Invoice,
                   StockCode,
                   InvoiceDate,
                   CustomerID
               ORDER BY InvoiceDate
           ) AS rn
    FROM online_retail_clean
) t
WHERE rn = 1;

-- verify the duplicate table 
select 
Invoice,StockCode,InvoiceDate,CustomerID,count(*) as cnt
from online_retail_dedup
group by Invoice,StockCode,InvoiceDate,CustomerID
having count(*)>1;

-- check price & quantity if -ve
select
count(*) as total_rows,
sum(case when price <=0 then 1 else 0 end) as price_qty,
sum(case when quantity <= 0 then 1 else 0 end)
from online_retail_dedup;

-- add the InvoiceDate_ts
alter table online_retail_dedup
add column InvoiceDate_ts datetime;

SET SQL_SAFE_UPDATES = 0;

-- update the invoicedate 
UPDATE online_retail_dedup
SET InvoiceDate_ts = STR_TO_DATE(InvoiceDate,'%d-%m-%Y %H:%i');

-- verify online_retail_dedup table
select * from online_retail_dedup
limit 10;

-- final cleaned table 
create table online_retail_final as
select Invoice, StockCode, Description, Quantity, InvoiceDate, Price, CustomerID, Country, rn, InvoiceDate_ts
from online_retail_dedup
where quantity > 0 and price > 0;

-- chevk the final table
select * from online_retail_final;