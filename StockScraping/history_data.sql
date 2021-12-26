-- File name: /scraping_data/history_data.sql
-- Author: WEI-TA KUAN
-- Date created: 26/12/2021
-- Date last modified: 26/12/2021
-- Version: 1.0
-- Status: Developing

-- Create a database to store historical data
CREATE DATABASE history;

-- Create a database to store the information of the company
-- There are two main market, which is TPEX and OTC in Taiwan Stock Market
create table tpex (
stock_id int primary key,
stock_name varchar(90),
sector_name varchar(10)
);

create table otc (
stock_id int primary key,
stock_name varchar(90),
sector_name varchar(10)
);

-- Create a table to store sector
create table stock_sector (
id INT AUTO_INCREMENT PRIMARY KEY,
sector_name varchar(10)
);