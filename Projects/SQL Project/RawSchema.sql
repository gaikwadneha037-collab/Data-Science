-- creating a db for online retail
CREATE DATABASE if NOT EXISTS retail_analysis;

-- use db
USE retail_analysis;

-- Raw data imported via MySQL Workbench CSV Import Wizard

-- check the import data 
show tables;

show tables from retail_analysis;

-- validate the imported table data
select count(*) from online_retail_ii;

select * from online_retail_ii;