from curses import window
from random import randint
import pandas as pd
import re
import os
import csv
import dtw_applier
import normalize_utils
from scipy.interpolate import make_interp_spline, BSpline
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
            with open(PATTERNS_FILE_PATH + pattern_type + '/' + file) as csvfile:
                reader = csv.reader(csvfile)
                next(reader, None)
                for row in reader:
                    single_file_results.append(round(float(row[1]), 3))
            total_results.append(single_file_results)
        patterns_dictionary[pattern_type] = total_results    
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
    minimun_distance = BIG_NUMBER
    common_pattern_type = 'rest_normalized'
    for pattern_type in all_patterns_dictionary.keys():
        for single_pattern in all_patterns_dictionary[pattern_type]:
            current_distance = dtw_applier.comparePatterns(normalized_vector, single_pattern)
            if current_distance < minimun_distance:
                common_pattern_type = pattern_type
                minimun_distance = current_distance
    
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
