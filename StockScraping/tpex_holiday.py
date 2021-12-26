#!/usr/bin/env python
# -*- coding: utf-8 -*-
#--------------------------------#
"""
File name: /scraping_data/tpex_holiday.py
Author: WEI-TA KUAN
Date created: 12/9/2021
Date last modified: 12/9/2021
Version: 1.0
Python Version: 3.8.8
Status: Developing
"""
#--------------------------------#

import pandas as pd 
import pickle
from dotenv import load_dotenv
import os

load_dotenv()

def get_holiday():
    """This function get the holiday for TPEX market, which the market is closed"""
    url = os.environ["HOLIDAY"]
    table = pd.read_html(url)
    data = table[-1]
    file = open("assets/tpex_holiday.pkl", 'wb') 
    pickle.dump(data, file)

