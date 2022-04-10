#!/usr/bin/env python

# -*- coding: utf-8 -*-

import pandas as pd
import sqlite3
class DataBase:

    def __init__(self, database):

        self.con =  sqlite3.connect(database)
        print("Connected to Database")
    
    def execution(self, query):
        
        cur = self.con.cursor()

        cur.execute(query)
        
        self.con.commit()

        print("executed")
    
    def read_table(self, query):

        with self.con as db:

            dataframe = pd.read_sql(query, db)

        return dataframe
    
    def close_connection(self):

        self.con.close()
        
        print("Connection Close Successfully")
