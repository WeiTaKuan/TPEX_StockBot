#!/usr/bin/env python
# -*- coding: utf-8 -*-
#--------------------------------#
"""
File name: /scraping_data/function.py
Author: WEI-TA KUAN
Date created: 10/9/2021
Date last modified: 12/9/2021
Version: 1.0
Python Version: 3.8.8
Status: Developing
"""
#--------------------------------#

from mysql.connector.errors import ProgrammingError, IntegrityError
import pandas_datareader as pdr
import mysql.connector as mysql 
from dotenv import load_dotenv
import datetime
import pandas as pd
import numpy as np
import datetime
import time 
import requests
import json
import os
from io import StringIO

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