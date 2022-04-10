import os
import pandas_datareader as pdr 
import pandas as pd 
import numpy as np
from matplotlib import pyplot as plt

def stock_index():
    stock = pdr.DataReader("^TWII", "yahoo")
    return round(stock.Close[-1], 2)

def option_strategy(data):
    
    data["call_put_ratio"] = data.call/data.put

    ratio_list = [np.nan]

    for index, _ in data.iterrows():
        start = index
        end = index + 1

        try:
            value = round(data["call_put_ratio"][end]/data["call_put_ratio"][start], 1)
            ratio_list.append(value)
        
        except KeyError:
            
            pass
    
    data["price_change_ratio"] = ratio_list

    return (data["price_change_ratio"].iloc[-1], data)

def draw_pic(low_data, mid_data, high_data, current_index):

    plt.suptitle(f"Taiwan Index Current Price: {current_index}", fontsize=12, horizontalalignment='center')
    
    plt.subplot(3,1,1)
    plt.plot(low_data.price_change_ratio)
    plt.axhline(y=0.6, color='r', linestyle='-')
    plt.axhline(y=1.6, color='b', linestyle='-')

    plt.subplot(3,1,2)
    plt.plot(mid_data.price_change_ratio)
    plt.axhline(y=0.6, color='r', linestyle='-')
    plt.axhline(y=1.6, color='b', linestyle='-')

    plt.subplot(3,1,3)
    plt.plot(high_data.Date,high_data.price_change_ratio)
    plt.axhline(y=0.6, color='r', linestyle='-')
    plt.axhline(y=1.6, color='b', linestyle='-')
    return plt.show()


if __name__ == "__main__":
    pass
