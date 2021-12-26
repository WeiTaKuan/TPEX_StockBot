#!/usr/bin/env python
# -*- coding: utf-8 -*-
#--------------------------------#
"""
File name: /StockScanning/stockbot.py
Author: WEI-TA KUAN
Date created: 10/9/2021
Date last modified: 26/12/2021
Version: 1.0
Python Version: 3.8.12
Status: Developing
"""
#--------------------------------#

from StockScanning.function import *

def potential_stock():
    # load env file
    load_dotenv()

    # history database config detail
    history_db = json.loads(os.environ["HISTORY_DATABASE"])

    history_db = Database(**history_db)

    potential_stock = list()

    # SMA condition
    short_period = int(os.environ["SHORT"])
    long_period = int(os.environ["LONG"])

    # read through the database
    for i in history_db.read_table("show tables;").iloc[:,0]:

        # reconnect to the database
        history_db.reconnect()

        df = history_db.read_table(f"select * from {i} order by date DESC limit 310")

        if SMA(df, short_period) < df["close"][0] < SMA(df, long_period) and df['volume'][0] >= int(os.environ["VOLUME"]):

            potential_stock.append(i.split("_")[0])

    for i in potential_stock:

        print(i)
        
        # try again for the stock if error occur
        while True:
            try:
                if bank_power(i):
                    pass

                else:
                    potential_stock.pop(potential_stock.index(i)) # remove unsatisified stock
                
                time.sleep(10)
                
            
            # error handling if the website refuse to return
            except urllib.error.URLError:
                print(f"try again {i}")
                time.sleep(30)
                
                continue
            break

    potential_stock = [int(i) for i in potential_stock]

    # push the result to line bot
    lineNotifyMessage(os.environ['LINE_TOKEN'], potential_stock)




    