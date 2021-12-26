#!/usr/bin/env python
# -*- coding: utf-8 -*-
#--------------------------------#
"""
File name: /stockbot/function.py
Author: WEI-TA KUAN
Date created: 10/9/2021
Date last modified: 11/9/2021
Version: 1.0
Python Version: 3.8.8
Status: Developing
"""
#--------------------------------#
from notion.client import NotionClient
import pandas_datareader as pdr
import mysql.connector as mysql 
from dotenv import load_dotenv
import datetime
import pandas as pd
import numpy as np
import datetime
import requests
import json
import os
import time
import urllib.error

class Database:

    def __init__(self, **kwargs):
        """The main function of connect to the database, change mysql to any type of sql database"""

        self.con =  mysql.connect(
            host=kwargs['host'],
            user=kwargs['user'],
            passwd=kwargs['passwd'],
            database=kwargs['database'],
            raise_on_warnings= True)

        print("Connected to Database")  
    
    def execution(self, query):
        """This function execute the query"""
        cur = self.con.cursor()

        cur.execute(query)
        
        self.con.commit()

        print("excuted")

    def read_table(self, query):
        """This function return the pandas dataframe of your query"""

        with self.con as db:

            dataframe = pd.read_sql(query, db)

        return dataframe
    
    def close_connection(self):
        """Remember to close the connection at the end of your script"""
        self.con.close()
        print("Connection Close Successfully")

    def reconnect(self):
        """Reconnect to the mysql database"""
        self.con.reconnect()


def lineNotifyMessage(token, msg):
    """This function use line notify for sending message"""

    url = "https://notify-api.line.me/api/notify"
    
    headers = {
        "Authorization": "Bearer " + token,
        "Content-Type" : "application/x-www-form-urlencoded"
    }

    post = {'message': msg}

    r = requests.post(url, headers=headers, params=post)
    
    return r.status_code

    
def SMA(stock, period):
    """This function calculate the simple moving average for sepcific period of time"""

    close = np.mean(stock["close"][:period])
    
    return close

def bank_power(code):
    """This function return the buying power of investment bank, 
    we are not able to provide the website that we use for calculating investment bank buying power
    """
    
    url = os.environ["WEBSITE"] + str(code) 
    table = pd.read_html(url)[0]
    final_df = table[:10]
    if sum(final_df["外資"]) > 0 and sum(final_df["投信"]) >= 0:        
        return True
