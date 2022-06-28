import yfinance as yf
import pandas as pd
import normalize_utils as nu
import matplotlib.pyplot as plt
from random import randint

def getCompanyDataWithAlpha(company):
    """
    Gets company data using Alpha API  

    Args:  
        company (str): Company name  
    Returns:
        Dict[]: Dictionary with all price and dates data 
    """
    api_key = 'H9KPSUTGEPR86VB6'
    time_interval = 5
    history_slice = 'year1month2'
    URL = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={company}&interval={time_interval}min&slice={history_slice}&apikey={api_key}]'
    download = requests.get(URL).json()
    dict = download[f'Time Series ({time_interval}min)']
    
    return dict

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

companies_list = [ #['', '', '', 'triple_top'],
    ['WHR', '2021-11-16', '2022-01-04', 'double_bottom']
]

#createDatasetsFromList(companies_list, './patterns/')