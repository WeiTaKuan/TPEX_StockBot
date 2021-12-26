#!/usr/bin/env python
# -*- coding: utf-8 -*-
#--------------------------------#
"""
File name: TPEX_STOCKBOT/main.py
Author: WEI-TA KUAN
Date created: 12/9/2021
Date last modified: 9/10/2021
Version: 1.0
Python Version: 3.8.8
Status: Developing
"""
#--------------------------------#

from scraping_data import stock_daily_scraping, tpex_holiday
import pickle
import datetime

year = datetime.datetime.today().strftime("%Y")
today = datetime.datetime.today().strftime("%Y/%m/%d")
holiday = pickle.load(open("assets/tpex_holiday.pkl",'rb'))

# update the market close date for each year
while True:
    if year != holiday["休市日期"][0].split("/")[0]:
        print("Update Holiday")
        tpex_holiday.get_holiday()
        holiday = pickle.load(open("assets/tpex_holiday.pkl",'rb'))
    break  

# Dont run the code if the market is close
if (today != holiday["休市日期"]).any() and datetime.datetime.today().weekday() not in [5, 6]:

    print("Run 360 TPEX Stockbot...")

    # run the daily scraping method to store today stock data
    stock_daily_scraping.daily_scraping()