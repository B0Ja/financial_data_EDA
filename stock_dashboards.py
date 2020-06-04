"""
This code creates and lays the basis for dashboard, using the 
stock_data_transformations.py transformations.

Charting is based on Daily and Weekly time frames. The option
of the saving the dashboard in a PDF format.

Sequence of code execution: stock_get_data.py > stock_data_transformations.py > stock_dashboards.py
"""

#===================================================================
#
#   Dashboard 1 for the Daily data
#===================================================================


fig1 = plt.figure(figsize=(15,12))

plt.style.use('seaborn-darkgrid')

plt.rcParams['ytick.right'] = plt.rcParams['ytick.labelright'] = True
plt.rcParams['ytick.left'] = plt.rcParams['ytick.labelleft'] = False

#fig.autofmt_xdate()

ax1 = plt.subplot2grid((4, 5), (0, 0), colspan=3, rowspan=3)
ax2 = plt.subplot2grid((4, 5), (3, 0), colspan=3, sharex = ax1)
ax3 = plt.subplot2grid((4, 5), (0, 3))
ax4 = plt.subplot2grid((4, 5), (1, 3), sharex = ax3)
ax5 = plt.subplot2grid((4, 5), (2, 3), sharex = ax3)
ax6 = plt.subplot2grid((4, 5), (3, 3), sharex = ax3)
ax7 = plt.subplot2grid((4, 5), (0, 4))
ax8 = plt.subplot2grid((4, 5), (1, 4), sharex = ax7)
ax9 = plt.subplot2grid((4, 5), (2, 4))
ax10 = plt.subplot2grid((4, 5), (3, 4))



ax1.plot(sbin.index, sbin['Close'], color='tab:blue', label = 'PriceD')
ax1.plot(sbin.index, sbin['Typical_200ma'], color='tab:red', label = '200ma')
ax1.plot(sbin.index, sbin['Typical_100ma'], color='tab:orange', label = '100ma')
ax1.plot(sbin.index, sbin['Typical_55ma'], color='tab:green', label = '55ma')
ax1.set_title("Price (Close)", color = 'grey', loc='right')
ax1.legend()

ax2.bar(sbin.index, sbin['Volume'], color = 'tab:green', label = 'Vol')
ax2.plot(sbin.index, sbin['Volume_200ma'], color = 'tab:red', label = '200ma')
ax2.set_title("Volume", color = 'grey', loc='right')
ax2.legend()


#xmin, xmax = ax3.get_xlim()
ax3.plot(sbin.index, sbin['Deliverable Volume'], color ='tab:gray', label ='DelVol')
#ax3.plot(sbin.index, sbin['DelVol50ma'], color = 'orange')
ax3.set_title("DelVol", color = 'tab:gray', loc='right')
ax3.axes.get_xaxis().set_visible(False)
ax9.axes.get_yaxis().set_visible(False)


ax4.plot(sbin.index, sbin['%Deliverble'], color = 'tab:gray', label = '%Del')
ax4.plot(sbin.index, sbin['%Del50ma'], color = 'tab:orange')
ax4.set_title("%Del", color = 'tab:gray', loc='right')
#ax4.annotate(str(sbin['%Del50ma'][-1].round(2)), xy= (xmax+0.7, sbin['%Del50ma'].iloc[-1]), color = 'k')
ax4.axes.get_xaxis().set_visible(False)
ax9.axes.get_yaxis().set_visible(False)


ax5.plot(sbin.index, sbin['M2M'], color ='tab:gray', label = 'M2M')
ax5.plot(sbin.index, sbin['M2M50ma'], color = 'tab:orange')
ax5.set_title("M2M", color = 'tab:gray', loc='right')
ax5.axes.get_xaxis().set_visible(False)
ax9.axes.get_yaxis().set_visible(False)


ax6.plot(sbin.index, sbin['Trades_trunc'], color ='tab:gray', label = 'Trades')
ax6.set_title("Trades(M)", color = 'tab:gray', loc='right')
ax6.axes.get_xaxis().set_visible(False)
ax9.axes.get_yaxis().set_visible(False)



#AX7 #Daily  Above Below Moving Averages
#df_temp_ax7 = pd.DataFrame()
#df_temp_ax7['Value'] = ['Color']
#df_temp_ax7.set_index('Value', inplace = True)
#df_temp_ax7['200ma'], df_temp_ax7['100ma'], df_temp_ax7['55ma'] = 1,1,1 
clr_200 = 'tab:blue' if (sbin['Typical_200ma'][-1] < sbin['Typical'][-1]) else 'tab:red'
clr_100 = 'tab:blue' if (sbin['Typical_100ma'][-1] < sbin['Typical'][-1]) else 'tab:red'
clr_55 = 'tab:blue' if (sbin['Typical_55ma'][-1] < sbin['Typical'][-1]) else 'tab:red'
barlist = ax7.barh([1,2,3], [1,1,1])
barlist[0].set_color(clr_200)
#ax7.annotate("200 MA", xy= (1, 0.5), color = 'k')
barlist[1].set_color(clr_100)
barlist[2].set_color(clr_55)
ax7.axes.get_xaxis().set_visible(False)
ax7.axes.get_yaxis().set_visible(False)
ax7.set_title("Daily: Above/Below MA", color = 'tab:gray', loc='right')

#AX8 #Weekly Above Below Moving Averages
clr_w200 = 'tab:blue' if (sbin_weekly['Typical_200ma'][-1] < sbin_weekly['Typical'][-1]) else 'tab:red'
clr_w100 = 'tab:blue' if (sbin_weekly['Typical_100ma'][-1] < sbin_weekly['Typical'][-1]) else 'tab:red'
clr_w55 = 'tab:blue' if (sbin_weekly['Typical_55ma'][-1] < sbin_weekly['Typical'][-1]) else 'tab:red'
barlist_w = ax8.barh([1,2,3], [1,1,1])
barlist_w[0].set_color(clr_w200)
#ax8.annotate("200 MA", xy= (1, 0.5), color = 'k')
barlist_w[1].set_color(clr_w100)
barlist_w[2].set_color(clr_w55)
ax8.axes.get_xaxis().set_visible(False)
ax8.axes.get_yaxis().set_visible(False)
ax8.set_title("Weekly: Above/Below MA", color = 'tab:gray', loc='right')



ax9.plot(sbin.index, sbin['DelPerTrade'], color ='tab:gray', label = 'DelPerTrades')
ax9.plot(sbin.index, sbin['DelPerTrade50ma'], color = 'tab:orange')
ax9.set_title("Del/Trade", color = 'tab:gray', loc='right')
ax9.axes.get_xaxis().set_visible(False)
ax9.axes.get_yaxis().set_visible(False)

ax10.plot(sbin.index, sbin['Typical_55ma'])
ax10.plot(sbin.index, sbin['Typical_100ma'])
ax10.fill_between(sbin.index, sbin['Typical_55ma'], sbin['Typical_100ma'], where=(sbin['Typical_55ma'] >= sbin['Typical_100ma']), color='tab:green', alpha=0.3)
ax10.fill_between(sbin.index, sbin['Typical_55ma'], sbin['Typical_100ma'], where=(sbin['Typical_55ma'] < sbin['Typical_100ma']), color='tab:red', alpha=0.3)
ax10.set_title("Momentum", color = 'tab:gray', loc='right')
ax10.axes.get_xaxis().set_visible(False)
ax10.axes.get_yaxis().set_visible(False)


fig1.tight_layout()
##plt.show()


#===================================================================
#
#Dashboard 2 for the Daily data
#===================================================================


fig2 = plt.figure(figsize=(15,12))

plt.style.use('seaborn-darkgrid')

plt.rcParams['ytick.right'] = plt.rcParams['ytick.labelright'] = True
plt.rcParams['ytick.left'] = plt.rcParams['ytick.labelleft'] = False

fig2.autofmt_xdate()


#Global Constant for this set of axes
#Period to chart
PTU = 100


ax1 = plt.subplot2grid((4, 5), (0, 0), colspan=2, rowspan=3)
#ax2 = plt.subplot2grid((4, 5), (2, 0), colspan=2,  rowspan=2, sharex = ax1)
ax3 = plt.subplot2grid((4, 5), (0, 2), colspan=2, rowspan=3)
ax4 = plt.subplot2grid((4, 5), (3, 0), colspan=2, rowspan=1, sharex = ax1)
ax5 = plt.subplot2grid((4, 5), (3, 2), colspan=2, rowspan=1, sharex = ax3)
ax6 = plt.subplot2grid((4, 5), (0, 4), colspan=1, rowspan=3, sharey = ax3)
ax7 = plt.subplot2grid((4, 5), (3, 4), colspan=1, rowspan=1)

"""
ax1 = plt.subplot2grid((4, 5), (0, 0), colspan=2, rowspan=2)
ax2 = plt.subplot2grid((4, 5), (2, 0), colspan=2,  rowspan=2, sharex = ax1)
ax3 = plt.subplot2grid((4, 5), (0, 2), colspan=2, rowspan=2)
ax4 = plt.subplot2grid((4, 5), (2, 2), colspan=2, rowspan=1, sharex = ax3)
ax5 = plt.subplot2grid((4, 5), (3, 2), colspan=2, rowspan=1, sharex = ax3)
ax6 = plt.subplot2grid((4, 5), (0, 4), colspan=1, rowspan=2, sharey = ax3)
ax7 = plt.subplot2grid((4, 5), (2, 4), colspan=1, rowspan=2)
"""

#Bolinger Chart
candlestick_ohlc(ax1, candle_data[-PTU: ], colorup='limegreen', colordown='indianred')
ax1.plot(sbin.index[-PTU: ], sbin['20ma'][-PTU: ], color='tab:gray')
ax1.plot(sbin.index[-PTU: ], sbin['lower_2_band'][-PTU: ], color='tab:olive', linestyle="dotted")
ax1.plot(sbin.index[-PTU: ], sbin['upper_2_band'][-PTU: ], color='tab:olive', linestyle="dotted")
ax1.plot(sbin.index[-PTU: ], sbin['lower_3_band'][-PTU: ], color='tab:purple', linestyle="dashed")
ax1.plot(sbin.index[-PTU: ], sbin['upper_3_band'][-PTU: ], color='tab:purple', linestyle="dashed")
ax1.set_title("Bolinger Bands", color = 'grey', loc='right')
ax1.axes.get_xaxis().set_visible(False)
ax1.axes.get_yaxis().set_visible(True)
#ax1.legend(False)


#VWAP with STD DEV Chart
candlestick_ohlc(ax2, candle_data[-PTU: ], colorup='limegreen', colordown='indianred')
ax2.plot(sbin.index[-PTU: ], sbin['VWAP_20ma'][-PTU: ], color='tab:gray')
ax2.plot(sbin.index[-PTU: ], sbin['VWAP_lower_2_band'][-PTU: ], color='tab:olive', linestyle="dotted")
ax2.plot(sbin.index[-PTU: ], sbin['VWAP_upper_2_band'][-PTU: ], color='tab:olive', linestyle="dotted")
ax2.plot(sbin.index[-PTU: ], sbin['VWAP_lower_3_band'][-PTU: ], color='tab:purple', linestyle="dashed")
ax2.plot(sbin.index[-PTU: ], sbin['VWAP_upper_3_band'][-PTU: ], color='tab:purple', linestyle="dashed")
ax2.set_title("VWAP bands", color = 'grey', loc='right')
ax2.axes.get_xaxis().set_visible(True)
ax2.axes.get_yaxis().set_visible(True)
#ax2.legend(False)



#Ichimoku Chart
candlestick_ohlc(ax3, candle_data[-PTU:], colorup='limegreen', colordown='indianred')
ax3.plot(sbin.index[-PTU:], sbin['tenkan_avg'][-PTU: ], color='cornflowerblue')
ax3.plot(sbin.index[-PTU: ], sbin['kijun_avg'][-PTU: ], color='tab:red', alpha = 0.6)
ax3.plot(sbin.index[-PTU: ], sbin['senkou_a'][-PTU: ], color='tab:purple', linestyle="dotted")
ax3.plot(sbin.index[-PTU: ], sbin['senkou_b'][-PTU: ], color='tab:purple', linestyle="dotted")
ax3.fill_between(sbin.index[-PTU: ], sbin['senkou_a'][-PTU: ], sbin['senkou_b'][-PTU: ], where=(sbin['senkou_a'][-PTU: ] >= sbin['senkou_b'][-PTU: ]), color='tab:green', alpha=0.3)
ax3.fill_between(sbin.index[-PTU: ], sbin['senkou_a'][-PTU: ], sbin['senkou_b'][-PTU: ], where=(sbin['senkou_a'][-PTU: ] < sbin['senkou_b'][-PTU: ]), color='tab:red', alpha=0.3)
ax3.plot(sbin.index[-PTU: ], sbin['chikou'][-PTU: ], color='tab:gray', linestyle="dotted")
ax3.set_title("Ichimoku", color = 'grey', loc='right')
ax3.axes.get_xaxis().set_visible(False)
ax3.axes.get_yaxis().set_visible(True)
#ax3.legend(False)

#MACD Chart
ax4.plot(sbin.index[-PTU:], sbin['macd_daily_trigger'][-PTU: ], color='cornflowerblue', alpha = 0.05)
ax4.plot(sbin.index[-PTU:], sbin['macd_daily_macd'][-PTU: ], color='cornflowerblue', alpha = 0.05)
ax4.fill_between(sbin.index[-PTU: ], sbin['macd_daily_trigger'][-PTU: ], sbin['macd_daily_macd'][-PTU: ], where=(sbin['macd_daily_trigger'][-PTU: ] >= sbin['macd_daily_macd'][-PTU: ]), color='tab:red', alpha=0.3)
ax4.fill_between(sbin.index[-PTU: ], sbin['macd_daily_trigger'][-PTU: ], sbin['macd_daily_macd'][-PTU: ], where=(sbin['macd_daily_trigger'][-PTU: ] < sbin['macd_daily_macd'][-PTU: ]), color='tab:green', alpha=0.3)
ax4.set_title("MACD", color = 'grey', loc='right')
ax4.axes.get_xaxis().set_visible(True)
ax4.axes.get_yaxis().set_visible(False)


#PMF
ax5.plot(sbin.index[-PTU:], sbin['m2m_daily_trigger'][-PTU: ], color='cornflowerblue', alpha = 0.05)
ax5.plot(sbin.index[-PTU:], sbin['m2m_daily_macd'][-PTU: ], color='cornflowerblue', alpha = 0.05)
ax5.fill_between(sbin.index[-PTU: ], sbin['m2m_daily_trigger'][-PTU: ], sbin['m2m_daily_macd'][-PTU: ], where=(sbin['m2m_daily_trigger'][-PTU: ] >= sbin['m2m_daily_macd'][-PTU: ]), color='tab:green', alpha=0.3)
ax5.fill_between(sbin.index[-PTU: ], sbin['m2m_daily_trigger'][-PTU: ], sbin['m2m_daily_macd'][-PTU: ], where=(sbin['m2m_daily_trigger'][-PTU: ] < sbin['m2m_daily_macd'][-PTU: ]), color='tab:red', alpha=0.3)
ax5.set_title("PMF", color = 'grey', loc='right')
ax5.axes.get_xaxis().set_visible(True)
ax5.axes.get_yaxis().set_visible(False)


#Add AX6
colored = ['tab:olive' if x else 'tab:brown' for x in (sbin_daily_volPro['pct_change'] >= 0)]
ax6.barh(sbin_daily_volPro['Close'], sbin_daily_volPro['delvolchange'], color = colored)
ax6.invert_xaxis();
ax6.set_title("DelVol", color = 'grey', loc='right')
ax6.axes.get_xaxis().set_visible(False)
#ax6.axes.get_yaxis().set_visible(False)

#Add AX7
ax7.hist(sbin_daily_volPro['sum_vol'], bins=200, orientation='horizontal', density=True, color = 'tab:brown')
ax7.invert_xaxis();
ax7.set_title("MktVol", color = 'grey', loc='right')
ax7.axes.get_xaxis().set_visible(False)
ax7.axes.get_yaxis().set_visible(False)


fig2.tight_layout()
##plt.show()


#===================================================================
#
#Dashboard for the weekly data
#===================================================================

fig3 = plt.figure(figsize=(15,12))

plt.style.use('seaborn-darkgrid')

plt.rcParams['ytick.right'] = plt.rcParams['ytick.labelright'] = True
plt.rcParams['ytick.left'] = plt.rcParams['ytick.labelleft'] = False

fig3.autofmt_xdate()

#Global Constant for this set of axes
#Period to chart
PTU = 100

ax1 = plt.subplot2grid((4, 5), (0, 0), colspan=2, rowspan=3)
#ax2 = plt.subplot2grid((4, 5), (2, 0), colspan=2,  rowspan=2, sharex = ax1)
ax3 = plt.subplot2grid((4, 5), (0, 2), colspan=2, rowspan=3)
ax4 = plt.subplot2grid((4, 5), (3, 0), colspan=2, rowspan=1, sharex = ax1)
ax5 = plt.subplot2grid((4, 5), (3, 2), colspan=2, rowspan=1, sharex = ax3)
ax6 = plt.subplot2grid((4, 5), (0, 4), colspan=1, rowspan=3, sharey = ax3)
ax7 = plt.subplot2grid((4, 5), (3, 4), colspan=1, rowspan=1)


#Bolinger Chart
candlestick_ohlc(ax1, sbin_weekly_candle_data[-PTU: ], colorup='tab:green', colordown='tab:red', width = 2)
ax1.plot(sbin_weekly['Date'].tail(PTU), sbin_weekly['20ma'].tail(PTU), color='tab:gray')
ax1.plot(sbin_weekly['Date'].tail(PTU), sbin_weekly['lower_2_band'].tail(PTU), color='tab:olive', linestyle="dotted")
ax1.plot(sbin_weekly['Date'].tail(PTU), sbin_weekly['upper_2_band'].tail(PTU), color='tab:olive', linestyle="dotted")
ax1.plot(sbin_weekly['Date'].tail(PTU), sbin_weekly['lower_3_band'].tail(PTU), color='tab:purple', linestyle="dashed")
ax1.plot(sbin_weekly['Date'].tail(PTU), sbin_weekly['upper_3_band'].tail(PTU), color='tab:purple', linestyle="dashed")
ax1.set_title("Bolinger Bands", color = 'grey', loc='right')
ax1.axes.get_xaxis().set_visible(False)
ax1.axes.get_yaxis().set_visible(True)
#ax1.legend(False)


#VWAP with STD DEV Chart
candlestick_ohlc(ax2, sbin_weekly_candle_data[-PTU: ], colorup='tab:green', colordown='tab:red', width = 2)
ax2.plot(sbin_weekly['Date'].tail(PTU), sbin_weekly['VWAP_20ma'].tail(PTU), color='tab:gray')
ax2.plot(sbin_weekly['Date'].tail(PTU), sbin_weekly['VWAP_lower_2_band'].tail(PTU), color='tab:olive', linestyle="dotted")
ax2.plot(sbin_weekly['Date'].tail(PTU), sbin_weekly['VWAP_upper_2_band'].tail(PTU), color='tab:olive', linestyle="dotted")
ax2.plot(sbin_weekly['Date'].tail(PTU), sbin_weekly['VWAP_lower_3_band'].tail(PTU), color='tab:purple', linestyle="dashed")
ax2.plot(sbin_weekly['Date'].tail(PTU), sbin_weekly['VWAP_upper_3_band'].tail(PTU), color='tab:purple', linestyle="dashed")
ax2.set_title("VWAP bands", color = 'grey', loc='right')
ax2.axes.get_xaxis().set_visible(True)
ax2.axes.get_yaxis().set_visible(True)
#ax2.legend(False)


#Ichimoku Chart
candlestick_ohlc(ax3, sbin_weekly_candle_data[-PTU:], colorup='tab:green', colordown='tab:red', width = 2)
ax3.plot(sbin_weekly['Date'].tail(PTU), sbin_weekly['tenkan_avg'].tail(PTU), color='cornflowerblue')
ax3.plot(sbin_weekly['Date'].tail(PTU), sbin_weekly['kijun_avg'].tail(PTU), color='tab:red', alpha = 0.6)
ax3.plot(sbin_weekly['Date'].tail(PTU), sbin_weekly['senkou_a'].tail(PTU), color='tab:purple', linestyle="dotted")
ax3.plot(sbin_weekly['Date'].tail(PTU), sbin_weekly['senkou_b'].tail(PTU), color='tab:purple', linestyle="dotted")
ax3.fill_between(sbin_weekly['Date'].tail(PTU), sbin_weekly['senkou_a'].tail(PTU), sbin_weekly['senkou_b'].tail(PTU), where=(sbin_weekly['senkou_a'].tail(PTU) >= sbin_weekly['senkou_b'].tail(PTU)), color='tab:green', alpha=0.3)
ax3.fill_between(sbin_weekly['Date'].tail(PTU), sbin_weekly['senkou_a'].tail(PTU), sbin_weekly['senkou_b'].tail(PTU), where=(sbin_weekly['senkou_a'].tail(PTU) < sbin_weekly['senkou_b'].tail(PTU)), color='tab:red', alpha=0.3)
ax3.plot(sbin_weekly['Date'].tail(PTU), sbin_weekly['chikou'].tail(PTU), color='tab:gray', linestyle="dotted")
ax3.set_title("Ichimoku", color = 'grey', loc='right')
ax3.axes.get_xaxis().set_visible(False)
ax3.axes.get_yaxis().set_visible(True)
#ax3.legend(False)


#MACD Chart
ax4.plot(sbin_weekly['Date'].tail(PTU), sbin_weekly['macd_daily_trigger'].tail(PTU), color='cornflowerblue', alpha = 0.4)
ax4.plot(sbin_weekly['Date'].tail(PTU), sbin_weekly['macd_daily_macd'].tail(PTU), color='cornflowerblue', alpha = 0.4)
ax4.fill_between(sbin_weekly['Date'].tail(PTU), sbin_weekly['macd_daily_trigger'].tail(PTU), sbin_weekly['macd_daily_macd'].tail(PTU), where=(sbin_weekly['macd_daily_trigger'].tail(PTU) >= sbin_weekly['macd_daily_macd'].tail(PTU)), color='tab:red', alpha=0.3)
ax4.fill_between(sbin_weekly['Date'].tail(PTU), sbin_weekly['macd_daily_trigger'].tail(PTU), sbin_weekly['macd_daily_macd'].tail(PTU), where=(sbin_weekly['macd_daily_trigger'].tail(PTU) < sbin_weekly['macd_daily_macd'].tail(PTU)), color='tab:green', alpha=0.3)
ax4.set_title("MACD", color = 'grey', loc='right')
ax4.axes.get_xaxis().set_visible(True)
ax4.axes.get_yaxis().set_visible(False)


#PMF
ax5.plot(sbin_weekly['Date'].tail(PTU), sbin_weekly['m2m_daily_trigger'].tail(PTU), color='cornflowerblue', alpha = 0.4)
ax5.plot(sbin_weekly['Date'].tail(PTU), sbin_weekly['m2m_daily_macd'].tail(PTU), color='cornflowerblue', alpha = 0.4)
ax5.fill_between(sbin_weekly['Date'].tail(PTU), sbin_weekly['m2m_daily_trigger'].tail(PTU), sbin_weekly['m2m_daily_macd'].tail(PTU), where=(sbin_weekly['m2m_daily_trigger'].tail(PTU) >= sbin_weekly['m2m_daily_macd'].tail(PTU)), color='tab:green', alpha=0.3)
ax5.fill_between(sbin_weekly['Date'].tail(PTU), sbin_weekly['m2m_daily_trigger'].tail(PTU), sbin_weekly['m2m_daily_macd'].tail(PTU), where=(sbin_weekly['m2m_daily_trigger'].tail(PTU) < sbin_weekly['m2m_daily_macd'].tail(PTU)), color='tab:red', alpha=0.3)
ax5.set_title("PMF", color = 'grey', loc='right')
ax5.axes.get_xaxis().set_visible(True)
ax5.axes.get_yaxis().set_visible(False)


#Add AX6
colored = ['tab:olive' if x else 'tab:brown' for x in (sbin_weekly_volPro['pct_change'] >= 0)]
ax6.barh(sbin_weekly_volPro['Close'], sbin_weekly_volPro['delvolchange'], color = colored)
ax6.invert_xaxis();
ax6.set_title("DelVol", color = 'grey', loc='right')
ax6.axes.get_xaxis().set_visible(False)
#ax6.axes.get_yaxis().set_visible(False)

#Add AX7
ax7.hist(sbin_weekly_volPro['sum_vol'], bins=200, orientation='horizontal', density=True, color = 'tab:brown')
ax7.invert_xaxis();
ax7.set_title("MktVol", color = 'grey', loc='right')
ax7.axes.get_xaxis().set_visible(True)
ax7.axes.get_yaxis().set_visible(True)


fig3.tight_layout()



#Set some plot settings
#plt.subplots_adjust(wspace=0, hspace=0)

#--------------------------------------------------------------------------------------------
#Create and Save dashboards as PDF files
from matplotlib.backends.backend_pdf import PdfPages
import datetime
import getpass

author = getpass.getuser()
dt = datetime.date.today()
name_of_file = '{}_{}.{}.{}_chart.pdf'.format(ticker,dt.year,dt.month,dt.day)

make_pdf = PdfPages(name_of_file)
make_pdf.savefig(fig1)
make_pdf.savefig(fig2)
make_pdf.savefig(fig3)

pdf_info = make_pdf.infodict()
pdf_info['Title'] = 'Charting {}'.format(ticker)
pdf_info['Author'] = author
pdf_info['Subject'] = ''
pdf_info['Keywords'] = ''
pdf_info['CreationDate'] = datetime.datetime.now()
pdf_info['ModDate'] = datetime.datetime.today()

make_pdf.close()
#--------------------------------------------------------------------------------------------


plt.show()

