import pandas as pd
import re
import os
import csv
import dtw_applier
import normalize_utils
import numpy as np
import matplotlib.pyplot as plt
from random import randint

PATTERNS_FILE_PATH = 'patterns/'
BIG_NUMBER = 99999999

def createMorningDataframeFromJson(day, inputData):
    """Create a dataset with close prices from 08:00 AM to 13:00 PM"""
    regex = rf"^{day} (0(8|9):\w*|1(0|1|2|3):\w*)"

    dataframe = pd.DataFrame({})
    for day, value in inputData.items():
        if re.search(regex, day) :
            dataframe = pd.concat([dataframe, pd.Series({day: value['4. close']})])
    return dataframe 

def loadPatterns(number_of_desired_patterns, pattern_types_set):
    """Create a pattern dictionary with pattern type contained in the set as key, 
    and n patterns data for each type  

    Args:  
        number_of_desired_patterns (int): number of patterns desired for each type
        pattern_types_set (Set{}): set containing the desired pattern types for the dictionary  
    Return:  
        pattern_dictionary (Dict{})
    """
    patterns_dictionary = {
        'rest_normalized': []
    }

    for pattern_type in pattern_types_set:
        file_list = os.listdir(PATTERNS_FILE_PATH + pattern_type)
        total_results = []
        elected_files_indexes_set = set()
        while len(elected_files_indexes_set) < number_of_desired_patterns:
            elected_files_indexes_set.add(randint(0, len(file_list) - 1))

        for index in elected_files_indexes_set:
            file = file_list[index]
            single_file_results = []
            #print("Opening file: " + file)
            with open(PATTERNS_FILE_PATH + pattern_type + '/' + file) as csvfile:
                reader = csv.reader(csvfile)
                next(reader, None)
                for row in reader:
                    #print(row)
                    single_file_results.append(round(float(row[1]), 3))
            total_results.append(single_file_results)
        patterns_dictionary[pattern_type] = total_results
    patterns_dictionary = calculateDictSimpleMovingAverage(patterns_dictionary, 3)
    #print(patterns_dictionary)
    return patterns_dictionary

def findCommonPattern(normalized_vector, all_patterns_dictionary):
    """Find the type of pattern for a given vector

        Args:  
            normalized_vector (List[]): previous normalized vector containing prices
            all_patterns_dictionary (Dict{}): dictionary containing pattern types and prices  
        Return:  
            common_pattern_type (str): type of the type for the pattern
            minimum_distance (float): minimum distance found between the best match and the vector
    """
    #print("Finding common pattern for: " + str(normalized_vector))
    #print("All patterns: " + str(all_patterns_dictionary))
    minimun_distance = BIG_NUMBER
    common_pattern_type = 'rest_normalized'
    dict_of_distances = {}
    for pattern_type in all_patterns_dictionary.keys():
        array_of_distances = []
        for single_pattern in all_patterns_dictionary[pattern_type]:
            current_distance = dtw_applier.comparePatterns(normalized_vector, single_pattern)
            array_of_distances.append(current_distance)
        if pattern_type != 'rest_normalized':
            array_of_distances = np.array(array_of_distances)
            mean = np.mean(array_of_distances)
            print(array_of_distances)
            print("Mean: " + str(mean))
            dict_of_distances[pattern_type] = mean
            print(dict_of_distances)

    for pattern_type, distance in dict_of_distances.items():
        if distance < minimun_distance:
            common_pattern_type = pattern_type
            minimun_distance = distance
    print("Common pattern found: " + common_pattern_type + " with distance: " + str(minimun_distance))
    return common_pattern_type, minimun_distance

def enhanceDataframe(distance_found, pattern_type, sliced_vector, all_patterns_dictionary, window_divisions):
    """Given a pattern, find a better match, if possible, inside the vector  

        Args:  
            distance_found (float): minimum distance found between the best match and the vector at the moment
            pattern_type (str): type of the pattern found
            sliced_vector (List[]): vector containing the data where the search will take plave
            all_patterns_dictionary (Dict{}): dictionary containing pattern types and prices
            windows_divisions (List[]): list contaning the number that the window is wanted to be fragmented equally  
        Return:  
            best_segment_i (int): index where the best segment starts
            best_segment_j (int): index where the best segment ends
    """
    minimum_distance = distance_found
    best_segment_i = 0
    best_segment_j = len(sliced_vector) - 1
    for number_of_parts in window_divisions:
        window_size = len(sliced_vector) // number_of_parts
        left_index = 0
        right_index = window_size
        for i in range(number_of_parts):
            split_vector = sliced_vector[left_index:right_index]
            normalized_split_vector = normalize_utils.normalizeVector(split_vector)
            for single_pattern in all_patterns_dictionary[pattern_type]:
                current_distance = dtw_applier.comparePatterns(normalized_split_vector, single_pattern)
                if current_distance <= minimum_distance:
                    minimum_distance = current_distance
                    best_segment_i = left_index
                    best_segment_j = right_index
            left_index = right_index
            right_index += window_size
        if i == window_divisions[len(window_divisions) - 1]: #Si es la ultima parte, cogemos todo hasta donde termine
            right_index = len(sliced_vector) - 1
    return best_segment_i, best_segment_j

def smoothData(dataframe):
    """Smooth the data inside a dataframe using average smoothing"""
    rolling = dataframe.rolling(window=2)
    rolling_mean = rolling.mean()
    dataframe.plot()
    random_number = str(randint(0,999))
    #plt.savefig('images/Results/AAP' + random_number)
    rolling_mean.plot(color='red')
    #plt.savefig('images/Results/AAP' + random_number + 'smooth', color='red')
    plt.show()
    return None

def minimumAndMaximumPatternSizes(patterns_dict):
    """Find inside the paterns_dict the longest and shortest patterns and its size"""
    min_size = BIG_NUMBER
    max_size = 0
    for key, vector in patterns_dict.items():
        if key == 'rest_normalized':
            continue
        for pattern in vector:
            current_size = len(pattern)
            if current_size < min_size:
                min_size = current_size
            if current_size > max_size:
                max_size = current_size
    return min_size, max_size

def calculateTendencyProbability(results, pattern_types):
    """Calculate the probability of achieving the expected tendency for the pattern types contained in pattern_types  

        Args:  
            results (List[]): list of results
            pattern_type (List[]): list of types to calculate probability for  
        Return:  
            average_tendency_dict (Dict{}): dictionary containing the average probability for each pattern type
    """
    average_tendency_dict = {}
    for key in pattern_types:
        if key == 'rest_normalized':
            continue
        average_tendency_dict[key] = [0, 0, 0] # [0] para decir cuantos cumplen la tendencia y [1] para saber el total de patrones
    for pattern_found in results:
        if pattern_found.tendency is True:
            average_tendency_dict[pattern_found.pattern_type][0] += 1
        average_tendency_dict[pattern_found.pattern_type][1] += 1
    for pattern_type, value in average_tendency_dict.items():
        if value[1] == 0:
            average_tendency_dict[pattern_type] = 'Not found'
        else: 
            average_tendency_dict[pattern_type] = value[0] / value[1] * 100
    return average_tendency_dict

def calculateSimpleMovingAverage(dataframe, window_size):
    """Calculate the simple moving average for a given dataframe and window size

        Args:  
            dataframe (DataFrame): dataframe containing the prices
            window_size (int): size of the window to calculate the moving average  
        Return:  
            dataframe (DataFrame): dataframe containing the prices and the moving average
    """
    dataframe['SMA'] = dataframe['Close'].rolling(window=window_size).mean()
    return dataframe

#Create a function that calculates the simple moving average of a given Dictionary and window size that does not use the calculateSimpleMovingAverage function
def calculateDictSimpleMovingAverage(patterns_dict, window_size):
    """Calculate the simple moving average for a given dictionary and window size

        Args:  
            patterns_dict (Dict{}): dictionary containing the prices
            window_size (int): size of the window to calculate the moving average  
        Return:  
            patterns_dict (Dict{}): dictionary containing the prices and the moving average
    """
    results = dict()
    #print("\n\n\n\nTest\n\n\n\n")
    for key, vector in patterns_dict.items():
        for i in range(len(vector)):
            vector[i] = calculateArraySimpleMovingAverage(vector[i], window_size)
    # print("\n\n\n\n")
    # print(patterns_dict)
    # print("\n\n\n\n")
    return patterns_dict

#A function that calculates simple moving average of an array
def calculateArraySimpleMovingAverage(array, window_size):
    """Calculate the simple moving average for a given array and window size

        Args:  
            array (List[]): array containing the prices
            window_size (int): size of the window to calculate the moving average  
        Return:  
            array (List[]): array containing the prices and the moving average
    """
    results = []
    for i in range(len(array)):
        if i >= window_size:
            aux = sum(array[i-window_size:i]) / window_size
            results.append(round(aux,4))
    return results