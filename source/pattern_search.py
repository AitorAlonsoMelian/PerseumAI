import pandas as pd
import pattern_utils
import Pattern as p
import tendencyCalculator as tc
import matplotlib.pyplot as plt
from random import randint
import normalize_utils as nu

INCREMENT = 1
    
def findCurrentPatterns(start_index, finish_index, company_dataframe, patterns_dictionary, company_name, intensive_search):
    """Find patterns that are occuring the day of the search  
    
    Args:  
        start_index (int): starting size of the searching window
        finish_index (int): ending size of the searching window
        company_datadrame (dataframe): dataframe containing the company prices in the entire year
        patterns_dictionary (Dict[]): dictionary containing types of patterns as keys an pattern data as value
        company_name (str): name of the company where the search is taking place  
    Returns:  
        results (List[Pattern]): list of patterns found
    """
    distances_dict = {
        'double_top': [pattern_utils.BIG_NUMBER, -1],
        'double_bottom': [pattern_utils.BIG_NUMBER, -1]
    }
    patterns_dictionary_copy = patterns_dictionary.copy()
    results = []
    for i in range(finish_index, start_index, -1): # hay que añadir que itere por todos y que se quede con el de menor distancia 
        if len(patterns_dictionary_copy.keys()) == 1:
            break
        if i > company_dataframe.size:
            i = company_dataframe.size
        sliced_dataframe = company_dataframe.iloc[company_dataframe.size - i:]
        normalized_vector = nu.normalizeVector(sliced_dataframe['Close'].tolist())
        new_pattern_type, distance = pattern_utils.findCommonPattern(normalized_vector, patterns_dictionary_copy)
        if new_pattern_type != 'rest_normalized':
            if intensive_search == True:
                if distance < distances_dict[new_pattern_type][0]:
                    distances_dict[new_pattern_type] = [distance, i]
            else:
                distances_dict[new_pattern_type] = [distance, i]
                patterns_dictionary_copy.pop(new_pattern_type)

    for key in distances_dict:
        if distances_dict[key][1] == -1:
            continue
        new_pattern = p.Pattern(key, company_dataframe[company_dataframe.size - distances_dict[key][1]:], company_name, str(company_dataframe.iloc[company_dataframe.size - i].name), str(company_dataframe.iloc[company_dataframe.size - 1].name), None)
        results.append(new_pattern)
            #patterns_dictionary_copy.pop(new_pattern_type)

    return results

def findHistoricPatterns(window_width, company_data, patterns_dictionary, company_name):
    """Find patterns through historic data  
    Args:  
        window_width (int): fixed window size for the search
        company_data (datarame): dataframe containing the company's close prices
        atterns_dictionary (Dict[]): dictionary containing types of patterns as keys an pattern data as value
        company_name (str): name of the company where the search is taking place  
    Returns:  
        patterns_found (List[Pattern]): list of patterns found
    """
    patterns_found = []
    offset = 0
    i = 0
    while i < company_data.size - window_width - 1:
        right_window_index = i + window_width
        if right_window_index >= company_data.size:
            break
        sliced_dataframe = company_data.iloc[i:right_window_index]
        normalized_vector = nu.normalizeVector(sliced_dataframe['Close'].tolist())
        new_pattern_type, best_distance_found = pattern_utils.findCommonPattern(normalized_vector, patterns_dictionary)
        if new_pattern_type != 'rest_normalized' and new_pattern_type != '':
            left_index, right_index = pattern_utils.enhanceDataframe(best_distance_found, new_pattern_type, sliced_dataframe['Close'].tolist(), patterns_dictionary, [1,2,3,4])
            dataframe_segment = sliced_dataframe[left_index:right_index] #Esto sin ventana mejorada
            longer_dataframe = company_data[i + left_index:] #Quitar left_index si no se usa enhanced dataframe
            pattern_tendency = tc.findPatternTendency(dataframe_segment, longer_dataframe, new_pattern_type)
            if pattern_tendency != None:
                new_pattern = p.Pattern(new_pattern_type, pattern_tendency[1], company_name, str(dataframe_segment.iloc[0].name), str(dataframe_segment.iloc[dataframe_segment.size - 1].name), pattern_tendency[0])
                patterns_found.append(new_pattern)
            offset = sliced_dataframe.size
        else:
            offset = 0
        i += INCREMENT + offset
    return patterns_found
