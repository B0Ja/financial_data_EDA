"""
Testing the normed spagetti chart on Nifty
"""

#Importing
import bs4 as bs
import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import mplfinance as mpf
import matplotlib.dates as mdates
import matplotlib.animation as animation
import numpy as np
import os
import pandas as pd
import pandas_datareader.data as pdr
import pickle
import requests
import yfinance as yf


#Setting the start and end dates for the data
start = dt.datetime(2017,1,1)
end = dt.date.today()

#Getting the Nifty tickers - Sentdex
def save_nifty_tickers():
    
    resp = requests.get('http://en.wikipedia.org/wiki/NIFTY_50')
    soup = bs.BeautifulSoup(resp.text, 'lxml')
    table = soup.find('table', {'class': 'wikitable sortable'})
    
    tickers = []
    
    for row in table.findAll('tr')[1:]:
        ticker = row.findAll('td')[1].text.replace('.', '-')
        ticker = ticker[:-3]+".NS"
        tickers.append(ticker)
        
    with open("niftytickers.pickle", "wb") as f:
        pickle.dump(tickers, f)
    return tickers

save_nifty_tickers()


#Getting data, and setting the columns


def get_data_from_yahoo(reload_nifty=False):
    
    if reload_nifty:
        tickers = save_nifty_tickers()
    else:
        with open("niftytickers.pickle", "rb") as f:
            tickers = pickle.load(f)
    
    if not os.path.exists('nifty_data'):
        os.makedirs('nifty_data')
    
    #start = dt.datetime(2019, 6, 8)
    #end = dt.datetime.now()
    
    
    for ticker in tickers[0:50]:
        
        print(ticker)
        
        if not os.path.exists('nifty_data/{}.csv'.format(ticker)):
            #df = pdr.get_data_yahoo(ticker, start, end)
            
            df = pdr.DataReader(ticker, 'yahoo', start, end)
            
            df.reset_index(inplace=True)
            df.set_index("Date", inplace=True)
            
            
            
            #adding the transformed columns
            df['{}_35ma'.format(ticker)] = df['Adj Close'].rolling(window=35, min_periods = 0).mean()
            df['{}_55ma'.format(ticker)] = df['Adj Close'].rolling(window=55, min_periods = 0).mean()
            df['{}_100ma'.format(ticker)] = df['Adj Close'].rolling(window=100, min_periods = 0).mean()
            df['{}_200ma'.format(ticker)] = df['Adj Close'].rolling(window=200, min_periods = 0).mean()
   
            df['flag_55'] = np.where( df['Adj Close'.format(ticker)] - df['{}_55ma'.format(ticker)] < 0, 1, -1 )
            df['flag_100'] = np.where( df['Adj Close'.format(ticker)] - df['{}_100ma'.format(ticker)] < 0, 1, -1 )
            df['flag_200'] = np.where( df['Adj Close'.format(ticker)] - df['{}_200ma'.format(ticker)] < 0, 1, -1 )
            
            x_temp = df['Adj Close'][0]
            df['norm_{}'.format(ticker)] = (df['Adj Close'] * 100) / x_temp

            
            
            df.to_csv('nifty_data/{}.csv'.format(ticker))
        else:
            print('Already have {}'.format(ticker))

            
get_data_from_yahoo()



def compile_data():
    with open("niftytickers.pickle", "rb") as f:
        tickers = pickle.load(f)
        
    main_df = pd.DataFrame()
    
    for count, ticker in enumerate (tickers):
        df = pd.read_csv('nifty_data/{}.csv'.format(ticker))
        df.set_index('Date', inplace = True)
        
        #df.rename(columns = {'norm_{}'.format(ticker): ticker}, inplace = True)
        #df.drop(['Open','High','Low','Close','Volume', 'Adj Close'], 1, inplace = True)
        
        df = df.filter(['norm_{}'.format(ticker)])
        
        if main_df.empty:
            main_df = df
        else:
            main_df = main_df.join(df, how = "outer")
            
            
        if count % 10 == 0:
            print (count)
            
    print (main_df.head())
    main_df.to_csv('.nifty_data/nifty_normalized.csv')

    
compile_data()

