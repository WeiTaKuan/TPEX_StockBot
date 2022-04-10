#!/usr/bin/env python

# -*- coding: utf-8 -*-

# selenium package components
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.options import Options

# original package
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import time
import requests
import pandas_datareader as pdr 

# function 
def wrangling_dataframe(data):

    call_data = data[["Call_Buy","Call_Sell", "Call_Bid", "Price"]]
    call_data["divide"] = call_data["Price"].astype(int).mod(1000)
    call_data = call_data[call_data["divide"] == 0].reset_index(drop=True)
    for index, row in call_data.iterrows():
        if row["Call_Bid"] == "--":
            if row["Call_Sell"] != "--":
                call_data.at[index, "Call_Bid"] = row["Call_Sell"]
            else:
                call_data.at[index, "Call_Bid"] = 0


    put_data = data[["Put_Buy","Put_Sell", "Put_Bid", "Price"]]
    put_data["divide"] = put_data["Price"].astype(int).mod(1000)
    put_data = put_data[put_data["divide"] == 0].reset_index(drop=True)
    for index, row in put_data.iterrows():
        if row["Put_Bid"] == "--":
            if row["Put_Sell"] != "--":
                put_data.at[index, "Put_Bid"] = row["Put_Sell"]
            else:
                put_data.at[index, "Put_Bid"] = 0

    return call_data.merge(put_data, on="Price")[["Price", "Call_Bid", "Put_Bid"]]

# main function
def option_scraping(url, product_list, optionDB):
    # set chrome browser to slience mode
    options = Options()
    options.add_argument("start-maximized")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-extensions")
    options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(options=options, executable_path='/usr/bin/chromedriver')
    print("Chrome Open OK")
    today_date = datetime.today().strftime('%Y/%m/%d')

    print("Getting_website")
    driver.get(url)
    print("Website Get")
    driver.find_element_by_xpath('//*[@id="content"]/main/div[2]/div[2]/button[1]').click()

    for i in product_list:

        print(i)

        product_date = datetime.strptime(i,"%Y%m").strftime("%Y%b").upper() 

        element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, f"//select[@class='form-control form-select']/option[@value={str(i)}]")))

        element.click()

        time.sleep(5)

        WebDriverWait(driver, 3).until(EC.text_to_be_present_in_element((By.XPATH, f"//select[@class='form-control form-select']/option[@value={str(i)}]"), f"{str(i)}"))

        page = driver.page_source

        data = pd.read_html(page)[1].iloc[:,[6, 5, 4, 7, 8, 9, 10]]

        data.columns = ["Call_Buy", "Call_Sell", "Call_Bid", "Price", "Put_Buy", "Put_Sell", "Put_Bid"]

        final_data = wrangling_dataframe(data) # get today's option price for each product

        all_table = optionDB.read_table("select * from sqlite_master;")["name"].tolist() # list all the table in database

        for _, row in final_data.iterrows():

            table_name = f"TXO{product_date}{row['Price']}" # table name in to database

            print(table_name)

            if table_name not in all_table:

                optionDB.execution(f"create table {table_name} (date varchar(20), call numeric(10), put numeric(10))")
            
            # add data into the existing table

            # if the date is already in the table, update the data
            if today_date in optionDB.read_table(f"select * from {table_name};")["date"].tolist():

                optionDB.execution(f"update {table_name} set call = {row['Call_Bid']}, put = {row['Put_Bid']} where date = '{today_date}';")
            
            # if the data is not in the table insert a new data
            else:
                try:
                    optionDB.execution(f"insert into {table_name} (date, call, put) values ('{today_date}', {row['Call_Bid']}, {row['Put_Bid']});")
                except:
                    pass

    driver.quit() 

def lineNotifyMessage(token, msg):

    url = "https://notify-api.line.me/api/notify"
    
    headers = {
        "Authorization": "Bearer " + token,
        "Content-Type" : "application/x-www-form-urlencoded"
    }

    post = {'message': msg}

    r = requests.post(url, headers=headers, params=post)
    
    return r.status_code

def stock_index():

    stock = pdr.DataReader("^TWII", "yahoo")
    
    return round(stock.Close[-1], 2)

def option_strategy(data):
    
    data["call_put_ratio"] = data.call/data.put

    count = 1

    while count < len(data):

        data.at[count, "price_change_ratio"] = round(data["call_put_ratio"][count]/data["call_put_ratio"][count - 1], 1)
       
        count += 1

    if data["price_change_ratio"].iloc[-1] >= os.environ['THRESHOLD_1'] or data["price_change_ratio"].iloc[-1] <= os.environ['THRESHOLD_2']:

        ratio = f'{data["price_change_ratio"].iloc[-1]}*'

    else:

        ratio = data["price_change_ratio"].iloc[-1]

    return (ratio, data, round(data["price_change_ratio"].iloc[-1]/data["price_change_ratio"].iloc[-2], 2))

if __name__ == "__main__":
    pass