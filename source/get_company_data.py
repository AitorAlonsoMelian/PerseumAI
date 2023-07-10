import yfinance as yf
import pandas as pd
import normalize_utils as nu
import matplotlib.pyplot as plt
from random import randint
import os

def getCompanyDataWithYahoo(company, start_date, finish_date=None):
    """
    Gets company data using Yahoo Finance API  

    Args:  
        company (str): Company name
        start_date (str): The moment from which we want to collect the data  
    Returns:  
        dataframe (dataframe): A dataframe representing the company's stock prices  
    """
    if finish_date == None:
        dataframe = yf.download(company, 
                            start = start_date, 
                            progress=False,
        )
    else:
        dataframe = yf.download(company, 
                        start = start_date,
                        end = finish_date, 
                        progress=False,
    )

    unwanted_labels = ['Open', 'High', 'Low', 'Adj Close', 'Volume']
    dataframe.drop(unwanted_labels, axis = 1, inplace = True)

    return dataframe

def createDatasetsFromList(list, patterns_path):
    """Given a list containing companies, dates, and pattern type,
    it creates the dataset and stores in the destiny path  

    Args:  
        list (list): list of companies to download the information from
        patterns_path (str): path where the dataframes will be stores
    """
    for item in list:
        dataframe = getCompanyDataWithYahoo(item[0], item[1], item[2])
        dataframe['Close'] = nu.normalizeVector(dataframe['Close'].tolist())
        dataframe.reset_index(drop=True, inplace=True)
        dataframe.plot(title=item[0])
        dataframe.to_csv(patterns_path + item[3] + '/' + item[0] + str(randint(0, 999)) + '.csv', sep = ',')
        plt.show()

# companies_list = [ #['', '', '', 'triple_top'],
#     ['WHR', '2021-11-16', '2022-01-04', 'double_bottom']
# ]

companies_list = [ 
    ['STXD', '2022-12-20', '2023-06-7', 'inv_head_and_shoulders'],
]

#createDatasetsFromList(companies_list, './patterns/')