"""
This code goes along with the nse_indices_normalized.py. In this code
we calculate the normed data, with an option to save it, and
do a basic chart the normalized data.
"""

#=====================================================================
#  Quick Charting of the normalized data
#=====================================================================    

import pandas as pd
import os
from matplotlib import cm

os.chdir('/home/lubuntu/Downloads/TempDelete/norm')

if not os.path.exists('Normalized'):
    os.makedirs('Normalized')

normalized_df = pd.read_csv('Constants/dataframe_tickers.csv', index_col = 0,) 

column_norm_list = list(normalized_df.columns.values)

norm = pd.DataFrame()

for col_ in column_norm_list:

    tickers = normalized_df[col_].values.tolist()

    for i in tickers[:10]:
        df_temp = pd.read_csv('Data/{}.NS_normalized.csv'.format(i))
        norm['{}'.format(i)] = df_temp['norm_{}.NS'.format(i)]

    norm.to_csv('Normalized/normalized_{}'.format(col_), float_format='%.2f', index = False)
    
    ax = norm.plot(legend = False, cmap = cm.get_cmap('Spectral'), rot = 90, figsize = (10,8))
    y_pos = ax.get_ylim()
    ax.annotate(col_, (10, 300))
    
