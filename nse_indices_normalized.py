"""
This code helps sets up the tickers for the indices, downloads the data, and calculated normalized values.

Charting is carried out in the supplementary file (nse_indices_normalized_charting.py)
"""


#=====================================================================
#   Imports & Modules
#=====================================================================
#Core
import datetime
from datetime import date, timedelta
import numpy as np
import os
import pandas as pd
#Scrape
import bs4 as bs
#Graphing
import matplotlib.pyplot as plt
from matplotlib import style
import matplotlib.dates as mdates
import matplotlib.animation as animation
from matplotlib import cm
#Finance
import mplfinance as mpf
import pandas_datareader.data as pdr
#Utilities
import pickle
import requests
import yfinance as yf


#=====================================================================
#   Setting some constants
#=====================================================================

os.chdir('/home/lubuntu/Downloads/TempDelete/norm')
    
if not os.path.exists('Constants'):
    os.makedirs('Constants')
if not os.path.exists('Data'):
    os.makedirs('Data')

#Setting the constant date
start = datetime.datetime(2017, 1, 1)
end = datetime.datetime.now()


#=====================================================================
#   Reading and Downloading the tickers
#=====================================================================

# dictionary for purposes of Testing
#ticker_list = { 
#        'nifty_50' : 'https://www1.nseindia.com/content/indices/ind_nifty50list.csv',
#        'next_50' : 'https://www1.nseindia.com/content/indices/ind_niftynext50list.csv',
#      #  'nifty_100' : 'https://www1.nseindia.com/content/indices/ind_nifty100list.csv',
#}

ticker_list = { 
        'nifty_50' : 'https://www1.nseindia.com/content/indices/ind_nifty50list.csv',
        'next_50' : 'https://www1.nseindia.com/content/indices/ind_niftynext50list.csv',
        #'nifty_100' : 'https://www1.nseindia.com/content/indices/ind_nifty100list.csv',
        #'nifty_200' : 'https://www1.nseindia.com/content/indices/ind_nifty200list.csv',
        #'nifty_500' : 'https://www1.nseindia.com/content/indices/ind_nifty500list.csv',
        #'midcap_50' : 'https://www1.nseindia.com/content/indices/ind_niftymidcap50list.csv',
        #'midcap_150' : 'https://www1.nseindia.com/content/indices/ind_niftymidcap150list.csv',
        #'midcap_100' : 'https://www1.nseindia.com/content/indices/ind_niftymidcap100list.csv',
        #'smallcap_50' : 'https://www1.nseindia.com/content/indices/ind_niftysmallcap50list.csv',
        #'smallcap_100' : 'https://www1.nseindia.com/content/indices/ind_niftysmallcap100list.csv',
        #'smallcap_250' : 'https://www1.nseindia.com/content/indices/ind_niftysmallcap250list.csv',
        #'auto_index' : 'https://www1.nseindia.com/content/indices/ind_niftyautolist.csv',
        #'bank_index' : 'https://www1.nseindia.com/content/indices/ind_niftybanklist.csv',
        #'con_durables' : 'https://www1.nseindia.com/content/indices/ind_niftyconsumerdurableslist.csv',
        #'fin_index' : 'https://www1.nseindia.com/content/indices/ind_niftyfinancelist.csv',
        #'fin_serv' : 'https://www1.nseindia.com/content/indices/ind_niftyfinancialservices25_50list.csv',
        #'fmcg_nse' : 'https://www1.nseindia.com/content/indices/ind_niftyfmcglist.csv',
        'it_nse' : 'https://www1.nseindia.com/content/indices/ind_niftyitlist.csv',
        #'media_nse' : 'https://www1.nseindia.com/content/indices/ind_niftymedialist.csv',
        #'metal_nse' : 'https://www1.nseindia.com/content/indices/ind_niftymetallist.csv',
        #'oil_nse' : 'https://www1.nseindia.com/content/indices/ind_niftyoilgaslist.csv',
        'pharma_nse' : 'https://www1.nseindia.com/content/indices/ind_niftypharmalist.csv',
        'pbank_nse' : 'https://www1.nseindia.com/content/indices/ind_nifty_privatebanklist.csv',
        'psu_bank' : 'https://www1.nseindia.com/content/indices/ind_niftypsubanklist.csv',
        #'realty_nse' : 'https://www1.nseindia.com/content/indices/ind_niftyrealtylist.csv',
}

#Reading and Downloading the tickers
dataframe_tickers = pd.DataFrame()

"""
Below loop can be used to update the tickers or add new tickers. Can be used to check but not
enabled currently. Delete the folder Constants or the dataframe_tickers file for now.
"""


for key in ticker_list:
    print (key, '--->', ticker_list[key])
    df_temp = pd.read_csv(ticker_list[key])
    dataframe_tickers['{}'.format(key)] = df_temp['Symbol']

dataframe_tickers.to_csv('Constants/dataframe_tickers.csv')
    

#=====================================================================
#  Create the Ticker & Data, or Update the data
#=====================================================================    
    
column_list = list(dataframe_tickers.columns.values)

for col_ in column_list:
    

    tickers = dataframe_tickers[col_].values.tolist()

    for ticker in tickers:
        
        print ("Updating Index: {}. Updating ticker: {}".format(col_, ticker))
        
        ticker = str(ticker) + ".NS"
        
        if not os.path.exists('Data/{}_normalized.csv'.format(ticker)): #
            
            df_normalized = pd.DataFrame()
        
            if ticker is not None:
        
                #ticker = str(ticker) + ".NS"
            
                try:
                    df_get_data = pdr.DataReader(ticker, 'yahoo', start, end)
                    df_get_data.reset_index(inplace=True)
                    df_get_data.set_index("Date", inplace=True)

                    x_temp = df_get_data['Adj Close'][0]

                    df_normalized['norm_{}'.format(ticker)] = (df_get_data['Adj Close'] * 100) / x_temp

                    df_normalized.to_csv('Data/{}_normalized.csv'.format(ticker)) #
                
                except:
                    pass
            
            else:
                pass

        else:
        
            print('{} - {}: File exists. Checking for updates.'.format(col_, ticker))

            df_temp = pd.read_csv('Data/{}_normalized.csv'.format(ticker), parse_dates = True) #

            if len(df_temp['Date']) > 0:                              
                if df_temp['Date'].iloc[-1] != datetime.date.today(): 
                    print (f'{ticker}: Updating data.')

                    try:
                        with open('Data/{}_normalized.csv'.format(ticker),'a') as file: #
                            start_day = end - timedelta(500)
                            
                            #Using DataReader for Yahoo
                            get_file = pdr.DataReader(ticker, 'yahoo', start, end)
                            
                            #Modification if NSEPY is needed
                            #get_file = get_history(ticker, start_day, end)
                            
                            file.write(get_file.to_string(index=True, header=False))
                            print (f'{ticker}: Chart updated.')

                    except EnvironmentError:
                        print (f'{ticker}: Error in updating the file/data.')


            
