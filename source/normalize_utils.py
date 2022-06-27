import pandas as pd
import numpy as np
import sys
import matplotlib.pyplot as plt
import os

"""File containing code used as utility to normalize files, vector, etc"""

def getFileName(argument):
    """Given a full path name, returns only the name of the file"""
    index = argument.rfind('/')
    return argument[index:] 

def normalizeFile(filename, des_path, source_path):
    """Normalize an entire file"""
    dataframe = pd.read_csv(source_path + filename, index_col=0)
    dataframe.plot(title=f"{filename}")

    data_array = []

    max_value = 0
    min_value = 999999999

    for index,row in dataframe.iterrows():
        data_array.append(row[0])
        if row[0] > max_value:
            max_value = row[0]
        if row[0] < min_value:
            min_value = row[0]

    normalized_data_array = []

    for value in data_array:
        normalized_value = (value - min_value) / (max_value - min_value)
        normalized_data_array.append(normalized_value)

    normalized_data_dict = {"Precio": normalized_data_array}

    normalized_dataframe = pd.DataFrame(normalized_data_dict)
    normalized_dataframe.plot()

    normalized_dataframe.to_csv(des_path + filename)

def normalizeVector(vector):
    """Normalize a given vector with max min normalization"""
    max_number = 0
    min_number = 99999999
    for number in vector:
        number = float(number)
        if number > max_number:
            max_number = number
        if number < min_number:
            min_number = number
    
    normalized_vector = []

    for number in vector:
        number = float(number)
        normalized_number = (number - min_number) / (max_number - min_number)
        normalized_vector.append(round(normalized_number, 3))

    return normalized_vector

# file_list = os.listdir(sys.argv[1])
# for file in file_list:
#     normalizeFile(file, sys.argv[2], sys.argv[1])
# plt.show()