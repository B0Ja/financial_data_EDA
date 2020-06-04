"""
Objective: Dashboard of the NSE Nifty & NSE Next Index stocks and its distribution.

Plots: Weightages, Returns (1yr, 6m, 3m, 1m) and Free Float Market Capitalization.
"""

import datetime
from datetime import date, timedelta
import matplotlib.pyplot as plt
import mplfinance as mpf
from mplfinance.original_flavor import candlestick_ohlc
import matplotlib.dates as mdates
import nsepy
from nsepy import get_history
import numpy as np
import pandas as pd
from sklearn import preprocessing


#Top Level Settings:
plt.style.use('seaborn-darkgrid')


#================================================================================
#Top 10 nifty stock weightage
#================================================================================

t = datetime.datetime.today()

day = t.strftime('%d')
month = t.strftime('%m')
year = t.strftime('%y')

#Dynamic URL
top10_url = 'https://www1.nseindia.com/content/indices/top10nifty50_{}{}{}.csv'.format(day, month, year)

df_weightage = pd.DataFrame()

try:
    df_weightage = pd.read_csv(top10_url)
    if not df_weightage.empty:
        print('Updating cache file.')
        df_weightage.to_csv('nifty_weightage.csv')
except:
    print ("Error reading file online: Reading cached file.")
    try:
        df_weightage = pd.read_csv('nifty_weightage.csv', index_col = 0)
    except:
        print ("Error: File Not Found: Did not find 'nifty_weightage.csv' file.")
        
else:    
    if df_weightage.empty == True:
        print ("Error: File Not Found: Did not find 'nifty_weightage.csv' file.")
        print ("Error: Data Read: Check if the date is valid business day.")


#================================================================================
#Monthly Index Returns
#================================================================================

#Static URL
monthly_index_returns = 'https://www1.nseindia.com/content/indices/mir.csv'

df_monthly_index_returns = pd.read_csv(monthly_index_returns, skiprows = 2)
df_monthly_index_returns.rename(columns={'Unnamed: 0': 'indices'}, inplace=True)


#================================================================================
#Market Capitalization and Weightages for Nifty and Next nifty
#================================================================================

#Static URL
next_url = 'https://www1.nseindia.com/content/indices/niftynext50_mcwb.csv'
nifty_url = 'https://www1.nseindia.com/content/indices/nifty50_mcwb.csv'

df_nifty_mcap = pd.read_csv(nifty_url, skiprows = 2, index_col = 0)
df_next_mcap = pd.read_csv(next_url, skiprows = 2, index_col = 0)

df_columns_names_weightage = {
                                'Security Symbol' : 'symbol',
                                'Security Name' : 'security',
                                'Industry' : 'industry',
                                'Equity Capital (In Rs.)' : 'equity',
                                'Free Float Market Capitalisation (Rs. Crores)' : 'FFMC',
                                'Weightage (%)' : 'weightage',
                                'Volatility (%)' : 'volatility',
                                'Monthly Return' : 'monthly_return',
                                'Avg. Impact Cost (%)' : 'impact_cost'
}

df_nifty_mcap.rename(columns = df_columns_names_weightage, inplace = True)
df_nifty_mcap = df_nifty_mcap[0:49]
df_nifty_mcap['industry'] = df_nifty_mcap['industry'].str[:15]
df_nifty_mcap.sort_values('FFMC', ascending = False, inplace = True)

df_next_mcap.rename(columns = df_columns_names_weightage, inplace = True)
df_next_mcap = df_next_mcap[0:49]
df_next_mcap['industry'] = df_next_mcap['industry'].str[:15]
df_next_mcap.sort_values('FFMC', ascending = False, inplace = True)


#================================================================================
# Plotting Charts
#================================================================================

#Plot Settings
fig = plt.figure(figsize=(15,20))


#Index Returns
ax1 = plt.subplot2grid((5, 4), (0, 0), rowspan = 1, colspan = 3)

#Top 10 weightage
ax2 = plt.subplot2grid((5, 4), (0, 3), rowspan = 1, colspan = 1)

#Monthly returns
ax6 = plt.subplot2grid((5, 4), (1, 3), rowspan = 2, colspan = 1)
ax3 = plt.subplot2grid((5, 4), (1, 0), rowspan = 2, colspan = 1, sharey=ax6)
ax4 = plt.subplot2grid((5, 4), (1, 1), rowspan = 2, colspan = 1, sharey=ax6)
ax5 = plt.subplot2grid((5, 4), (1, 2), rowspan = 2, colspan = 1, sharey=ax6)


#FreeFloat & MarketCaps & Weightages
ax7 = plt.subplot2grid((5, 4), (3, 0), rowspan = 1, colspan = 2)
ax8 = plt.subplot2grid((5, 4), (4, 0), rowspan = 1, colspan = 2)
ax9 = plt.subplot2grid((5, 4), (3, 2), rowspan = 1, colspan = 2)
ax10 = plt.subplot2grid((5, 4), (4, 2), rowspan = 1, colspan = 2)


#================================================================================
# Charts & Settings
#================================================================================

#Plotting Monthly Index Returns 
colored = ['tab:green' if x else 'tab:red' for x in (df_monthly_index_returns['1 year'] >= 0)]
ax1.barh(df_monthly_index_returns['indices'], df_monthly_index_returns['1 year'], color = colored)
plt.xticks(rotation=90)


#Basic bar plot of Nifty Top 10 weights
k_temp = df_weightage['WEIGHTAGE(%)'].sum().round(2)
ax2.barh(df_weightage['SYMBOL'], df_weightage['WEIGHTAGE(%)'], color = 'tab:blue')
#ax2 = df_weightage.plot.bar('SYMBOL', 'WEIGHTAGE(%)')
ax2.annotate('TotalWeight={}'.format(k_temp), (5, 9))
#ax2.xticks(rotation=90)
#ax2.set_xticklabels(df_weightage['SYMBOL'], rotation=90, ha='center')


#Plotting Monthly Index Returns - 1 year, 6 months, 3 months, 1 month
#
colored_ax3 = ['tab:green' if x else 'tab:red' for x in (df_monthly_index_returns['1 year'] >= 0)]
ax3.barh(df_monthly_index_returns['indices'], df_monthly_index_returns['1 year'], color = colored_ax3)
ax3.axes.get_yaxis().set_visible(True)
ax3.set_title('1-year', loc='center', color = 'tab:gray')
ax3.grid(which='minor', axis='both', color = 'tab:gray', linestyle='--', linewidth=1 )


colored_ax4 = ['tab:green' if x else 'tab:red' for x in (df_monthly_index_returns['6 month'] >= 0)]
ax4.barh(df_monthly_index_returns['indices'], df_monthly_index_returns['6 month'], color = colored_ax4)
ax4.axes.get_yaxis().set_visible(False)
ax4.set_title('6-month', loc='center', color = 'tab:gray')
ax4.grid(which='minor', axis='both', color = 'tab:gray', linestyle='--', linewidth=1 )


colored_ax5 = ['tab:green' if x else 'tab:red' for x in (df_monthly_index_returns['3 month'] >= 0)]
ax5.barh(df_monthly_index_returns['indices'], df_monthly_index_returns['3 month'], color = colored_ax5)
ax5.axes.get_yaxis().set_visible(False)
ax5.set_title('3-month', loc='center', color = 'tab:gray')
ax5.grid(which='minor', axis='both', color = 'tab:gray', linestyle='--', linewidth=1 )

colored_ax6 = ['tab:green' if x else 'tab:red' for x in (df_monthly_index_returns['1 month'] >= 0)]
ax6.barh(df_monthly_index_returns['indices'], df_monthly_index_returns['1 month'], color = colored_ax6)
ax6.axes.get_yaxis().set_visible(False)
ax6.set_title('1-month', loc='center', color = 'tab:gray')
ax6.grid(which='minor', axis='both', color = 'tab:gray', linestyle='--', linewidth=1 )


#================================================================================
#First Column - Plotting
#ax7 = df_nifty_mcap.plot(x='symbol', y= 'FFMC', kind = 'bar', ax=ax7, label = 'Free Float Market Cap (Rs Crs)', secondary_y=True)
ax7.bar(df_nifty_mcap['symbol'], df_nifty_mcap['FFMC'], label = 'Free Float Market Cap (Rs Crs)')
#ax7.set_xlabel("Security")
#ax7.set_ylabel("Market Capitalization in (Rs Crs)")
ax7.set_xticklabels(df_nifty_mcap['symbol'].str.upper().str[:8], rotation=90, ha='center')
ax7.yaxis.tick_right()
ax7.legend(['Free Float Market Cap (Rs Crs)'])

xmin, xmax = ax7.get_xlim()
mean_FFMC_nifty = round(df_nifty_mcap["FFMC"].mean(), 2)
mean_FFMC_displace_nifty = mean_FFMC_nifty * 1.05

ax7.axhline(y=df_nifty_mcap["FFMC"].mean(), xmin=0, xmax=1, color = 'black', alpha = 0.5)
ax7.xaxis.grid(False, which='major', color = 'whitesmoke', linestyle='--', linewidth=0.02)
ax7.yaxis.grid(True, which='major', color = 'gray', linestyle='--', linewidth=0.25)
ax7.annotate(mean_FFMC_nifty, (xmax-10, mean_FFMC_displace_nifty) )


#FirstColumn = Industry Weightage chart
c = df_nifty_mcap.pivot_table(index = ['security', 'industry'], values = ['FFMC','weightage']).sort_values('weightage', ascending = False)
Weight = c.groupby('industry')[['weightage', 'FFMC']].sum().sort_values('FFMC', ascending = False)
ax8 = Weight.plot(kind = 'bar', secondary_y= 'weightage', grid = True, ax=ax8)
ax8.xaxis.grid(True, which='major', color = 'gray', linestyle='--', linewidth=0.25)
ax8.yaxis.grid(True, which='major', color = 'gray', linestyle='--', linewidth=0.25)
ax8.get_xaxis().get_label().set_visible(False)

#================================================================================

#Second Column - Plotting
#ax9 = df_next_mcap.plot(x='symbol', y= 'FFMC', kind = 'bar', ax=ax9, label = 'Free Float Market Cap (Rs Crs)', secondary_y=True)
ax9.bar(df_next_mcap['symbol'], df_next_mcap['FFMC'], label = 'Free Float Market Cap (Rs Crs)')
#ax9.set_xlabel("Security")
#ax9.set_ylabel("Market Capitalization in (Rs Crs)")
ax9.set_xticklabels(df_next_mcap['symbol'].str.upper().str[:8], rotation=90, ha='center')
ax9.yaxis.tick_right()
ax9.legend(['Free Float Market Cap (Rs Crs)'])

xmin, xmax = ax9.get_xlim()
mean_FFMC_next = round(df_next_mcap["FFMC"].mean(), 2)
mean_FFMC_displace_next = mean_FFMC_next * 1.05

ax9.axhline(y=df_next_mcap["FFMC"].mean(), xmin=0, xmax=1, color = 'black', alpha = 0.5)
ax9.xaxis.grid(False, which='major', color = 'whitesmoke', linestyle='--', linewidth=0.02)
ax9.yaxis.grid(True, which='major', color = 'gray', linestyle='--', linewidth=0.25)
ax9.annotate(mean_FFMC_next, (xmax-10, mean_FFMC_displace_next) )


#SecondColumn = Industry Weightage chart
c = df_next_mcap.pivot_table(index = ['security', 'industry'], values = ['FFMC','weightage']).sort_values('weightage', ascending = False)
Weight = c.groupby('industry')[['weightage', 'FFMC']].sum().sort_values('FFMC', ascending = False)
ax10 = Weight.plot(kind = 'bar', secondary_y= 'weightage', grid = True, ax=ax10)
ax10.xaxis.grid(True, which='major', color = 'gray', linestyle='--', linewidth=0.25)
ax10.yaxis.grid(True, which='major', color = 'gray', linestyle='--', linewidth=0.25)
ax10.get_xaxis().get_label().set_visible(False)


#================================================================================

plt.subplots_adjust(wspace=0.1, hspace=0.15)
fig.tight_layout()
