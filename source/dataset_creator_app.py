import pandas as pd
import yfinance as yf
import sys
from random import randint
import signal

"""Implementation of a app made to run on the shell. This app downloads data using yFinance API
and creates a dataset with the starting date and ending date specified by the user. Also, it creates
a random dataset representing a non important pattern"""

def signal_handler(sig, frame):
    print('\nBye bye!\n')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

CURRENT_YEAR = '2021'

while(True):

    company = input('Enter company name: ')
    start_date = input('Enter pattern\'s start date: ')
    finish_date = input('Enter pattern\'s finish date: ')

    dataframe = yf.download(company, 
                        start = CURRENT_YEAR + '-01-01', 
                        progress=False,
    )

    unwanted_labels = ['Open', 'High', 'Low', 'Adj Close', 'Volume']
    dataframe.drop(unwanted_labels, axis = 1, inplace = True)

    result_dataframe = pd.DataFrame()
    non_pattern_dataframe = pd.DataFrame()

    start_loc = dataframe.index.get_loc(start_date)
    finish_loc = dataframe.index.get_loc(finish_date)

    for i in range(start_loc, finish_loc):
        result_dataframe = pd.concat([result_dataframe, dataframe.iloc[i]], ignore_index = True)

    patterns_size = finish_loc - start_loc
    for i in range(start_loc - patterns_size, start_loc):
        non_pattern_dataframe = pd.concat([non_pattern_dataframe, dataframe.iloc[i]], ignore_index = True)

    result_dataframe[0].to_csv(sys.argv[1] + company + str(randint(0, 999)) + '.csv', sep = ',')
    non_pattern_dataframe[0].to_csv('patterns/rest/' + str(randint(0, 999)) + '.csv', sep = ',')
