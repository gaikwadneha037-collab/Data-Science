-- check for table
select * from online_retail_ii;

-- changing the column name to invoice
ALTER TABLE online_retail_ii 
CHANGE `Customer ID` CustomerID INT;

-- recheck the table
select * from online_retail_ii;

-- check for nulls
select * from online_retail_ii
where StockCode is null 
or Invoice is null 
or Description is null
or Quantity is null
or Price is null
or InvoiceDate is null
or CustomerID is null
or Country is null;

-- count nulls
select 
Sum(case when StockCode is null then 1 else 0 end) as StockCodenulls,
Sum(case when Invoice is null then 1 else 0 end) as Invoicenulls,
Sum(case when Description is null then 1 else 0 end) as Descriptionnulls,
Sum(case when Quantity is null then 1 else 0 end) as Quantitynulls,
Sum(case when Price is null then 1 else 0 end) as Pricenulls,
Sum(case when InvoiceDate is null then 1 else 0 end) as InvoiceDatenulls,
Sum(case when CustomerID is null then 1 else 0 end) as CustomerIDnulls,
Sum(case when Country is null then 1 else 0 end) as Countrynulls
from online_retail_ii;

-- check negatives for int
select 
count(*) as total_rows,
Sum(case when Quantity<=0 then 1 else 0 end) as invalid_quantity,
Sum(case when Price<=0 then 1 else 0 end) as invalid_price
from online_retail_ii;