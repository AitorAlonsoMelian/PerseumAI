import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import csv
import numpy as np
#from mpl_point_clicker import clicker

#[18263.46493787, 74.83552998], [18656.4576964 ,131.6303238 ]

# fig, ax = plt.subplots(constrained_layout=True)

# aapl_df = yf.download('AAPL', 
#                       start='2021-11-30',
#                       end='2021-12-30', 
#                       progress=False,
# )
# aapl_df_total = yf.download('AAPL', 
#                       progress=False,
# )

# idx = pd.date_range('2021-11-30', '2021-12-30')

# dataset = aapl_df['Close']
# dataset.index = pd.DatetimeIndex(dataset.index)

# dataset.plot(title="APPLE's stock price")
# #for item in dataset:
#     #copy_dataset['Date'] = dataset.index[item]
# #aapl_df.to_csv("results.csv", sep='\t')

# #ax.plot(x,y)
# #1980-12-12   '2022-02-22'
# coords = []
# x = plt.ginput(3)
# print(x)
# #plt.show()
# filled_dataset = dataset.reindex(idx, fill_value=None)

# idx_total = pd.date_range('1980-12-12', '2022-02-22')
# aapl_df_total['Close'].index = pd.DatetimeIndex(aapl_df_total['Close'].index)
# filled_dataset_total = aapl_df_total['Close'].reindex(idx_total, fill_value=None)

# #print(dataset.__dict__)

# start_date='2021-12-30'
# print(start_date[start_date.find('-') + 1:])


# def onclick(event):
#     global ix, iy
#     ix, iy = event.xdata, event.ydata
#     print(f'x = {ix}, y = {iy}')

#     global coords
#     coords.append((ix, iy))

#     if len(coords) == 2:
#         fig.canvas.mpl_disconnect(cid)

#     return coords
# cid = fig.canvas.mpl_connect('button_press_event', onclick)