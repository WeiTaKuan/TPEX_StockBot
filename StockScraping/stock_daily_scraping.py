#!/usr/bin/env python
# -*- coding: utf-8 -*-
#--------------------------------#
"""
File name: /scraping_data/stock_daily_scraping.py
Author: WEI-TA KUAN
Date created: 10/9/2021
Date last modified: 12/9/2021
Version: 1.0
Python Version: 3.8.8
Status: Developing
"""
#--------------------------------#

from StockScraping.function import *

def daily_scraping():

    # load env file
    load_dotenv()

    # stock database config detail, which will looks like this {"host":"localhost","user": your_username,"passwd" : your_password, "database" : your_database}
    stock_db = json.loads(os.environ["STOCK_DATABASE"])

    # history database config detail
    history_db = json.loads(os.environ["HISTORY_DATABASE"])

    # pass the config into database
    stock_db = Database(**stock_db)

    history_db = Database(**history_db)

    today = datetime.datetime.today().strftime("%Y-%m-%d")

    # list out all the TPEX stock
    stock_list = [i for i in stock_db.read_table("select stock_id from TPEX;").iloc[:,0]]


    # Download today stock price from TWSE website, the stock price usually will update at "2 pm UTC+8"
    r = requests.post('https://www.twse.com.tw/exchangeReport/MI_INDEX?response=csv&date=' + datetime.datetime.today().strftime("%y%m%d") + '&type=ALL')


    # re-format the data into pandas dataframe
    df = pd.read_csv(StringIO(r.text.replace("=", "")), header=["證券代號" in l for l in r.text.split("\n")].index(True)-1)
    df = df[["證券代號", "開盤價","最高價", "最低價", "收盤價", "成交股數"]]

    # set the stock ID as index
    df = df.set_index("證券代號", drop=True)

    # Turn the dataframe into a dictionary
    stock_dict = df.to_dict("index")


    for i in stock_list:
        print(i)
        
        data = history_db.read_table(f"select date from {i}_tw order by date DESC limit 1")

        # reconnect the database everytime in the for loop
        history_db.reconnect()

        # if there is no data for today, insert the data into table
        if pd.to_datetime(data['date'])[0].strftime("%Y-%m-%d") != today:

            try:
                data = stock_dict[str(i)]

                date = datetime.datetime.today().strftime("%Y-%m-%d 00:00:00")

                high = data['最高價'].replace(",", "")
                low = data['最低價'].replace(",", "")
                open_price = data["開盤價"].replace(",", "")
                close_price = data["收盤價"].replace(",", "")
                volume = data["成交股數"].replace(",", "")

            except KeyError:
                pass

            query = f'insert into {i}_tw (date, high, low, open, close, volume) value ("{date}", {high}, {low}, {open_price}, {close_price}, {volume});'
            
            try:
                history_db.execution(query)

            except ProgrammingError:
                pass
        

