#!/usr/bin/env python
# -*- coding: utf-8 -*-
#--------------------------------#
"""
File name: /scraping_data/stock_history_scraping.py
Author: WEI-TA KUAN
Date created: 10/9/2021
Date last modified: 10/9/2021
Version: 1.0
Python Version: 3.8.8
Status: Developing
"""
#--------------------------------#
from scraping_data.function import *

def history_stock_scraping():
    # load env file
    load_dotenv()

    # stock database config detail
    stock_db = json.loads(os.environ["STOCK_DATABASE"])

    # history database confit detail
    history_db = json.loads(os.environ["HISTORY_DATABASE"])

    stock_db = Database(**stock_db)

    history_db = Database(**history_db)

    stock_id =  stock_db.read_table("select stock_id from tpex;")

    for i in stock_id["stock_id"]:

        print(i)

        try:

            # create table for each stock into SQL database
            query = f"create table {i}_tw (date varchar(30), high float(10), low float(10), open float(10), close float(10), volume float(20));"

            # execute the query
            history_db.execution(query)

            # fetching historical data from yahoo finance
            data = pdr.DataReader(f"{i}.TWO", "yahoo", start="2010-1-1").round(2).reset_index()

            # parsing through all the row and store the historical data into the table
            for index, row in data.iterrows():
                date = row['Date']
                high = row['High']
                low = row['Low']
                open_price = row["Open"]
                close_price = row["Close"]
                volume = row["Volume"]

                # insert into query for SQL database
                query = f'insert into {i}_tw (date, high, low, open, close, volume) value ("{date}", {high}, {low}, {open_price}, {close_price}, {volume});'

                # execute the query
                history_db.execution(query)
            
            # Sleep for 3 seconds
            time.sleep(3)

        except ProgrammingError:
            
            pass

    # remember to close connection at the end
    history_db.close_connection()