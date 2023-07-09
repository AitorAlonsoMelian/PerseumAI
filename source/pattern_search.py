import pandas as pd
import pattern_utils
import Pattern as p
import tendencyCalculator as tc
import matplotlib.pyplot as plt
from random import randint
import normalize_utils as nu

INCREMENT = 25
SMA_VALUE = 3
    
def findCurrentPatterns(company_dataframe, patterns_dictionary, company_name):
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
    results = []
    company_dataframe = pattern_utils.calculateSimpleMovingAverage(company_dataframe, SMA_VALUE)
    company_dataframe = company_dataframe.iloc[SMA_VALUE-1:]
    normalized_vector = nu.normalizeVector(company_dataframe['SMA'].tolist())
    new_pattern_type, distance = pattern_utils.findCommonPattern(normalized_vector, patterns_dictionary)
    if distance < 30:
        pattern_tendency = tc.findPatternTendency(company_dataframe, company_dataframe, new_pattern_type)
        if pattern_tendency != None:
            new_pattern = p.Pattern(new_pattern_type, company_dataframe, company_name, str(company_dataframe.iloc[0].name), str(company_dataframe.iloc[-1].name), None, distance, pattern_tendency[2])
            results.append(new_pattern)

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
    i = 0
    separated_execute = False
    company_data = pattern_utils.calculateSimpleMovingAverage(company_data, SMA_VALUE)
    company_data = company_data.iloc[SMA_VALUE-1:]
    if ('double_top' in patterns_dictionary.keys() and 'head_and_shoulders' in patterns_dictionary.keys()) or ('double_bottom' in patterns_dictionary.keys() and 'inv_head_and_shoulders' in patterns_dictionary.keys()):
        separated_execute = True
    #print("Company Data: " + company_data.to_string())
    if separated_execute:
        for key in patterns_dictionary.keys():
            if key == 'rest_normalized':
                continue
            temp_dict = {key: patterns_dictionary[key]}
            i = 0
            while i < len(company_data) - window_width - 1:
                right_window_index = i + window_width
                #print("I: " + str(i) + " Right: " + str(right_window_index) + " Window: " + str(right_window_index - i))
                if right_window_index >= len(company_data):
                    break
                sliced_dataframe = company_data.iloc[i:right_window_index]
                normalized_vector = nu.normalizeVector(sliced_dataframe['SMA'].tolist())
                new_pattern_type, best_distance_found = pattern_utils.findCommonPattern(normalized_vector, temp_dict)
                if new_pattern_type != 'rest_normalized' and new_pattern_type != '' and best_distance_found < 40:
                    left_index, right_index = pattern_utils.enhanceDataframeDistancesMean(best_distance_found, new_pattern_type, sliced_dataframe['SMA'].tolist(), temp_dict, [1,2,3,4])
                    dataframe_segment = sliced_dataframe[left_index:right_index] #Esto sin ventana mejorada
                    longer_dataframe = company_data[i + left_index:] #Quitar left_index si no se usa enhanced dataframe
                    ##########################################################
                    ## ESTO ES PARA HACERLO CON TENDENCIA
                    pattern_tendency = tc.findPatternTendency(dataframe_segment, longer_dataframe, new_pattern_type)
                    if pattern_tendency != None:
                        new_pattern = p.Pattern(new_pattern_type, pattern_tendency[1], company_name, str(dataframe_segment.iloc[0].name), str(dataframe_segment.iloc[len(dataframe_segment) - 1].name), pattern_tendency[0], best_distance_found, pattern_tendency[2])
                        patterns_found.append(new_pattern)
                    ##########################################################
                    ## ESTO ES PARA HACERLO SIN TENDENCIA
                    # new_pattern = p.Pattern(new_pattern_type, dataframe_segment, company_name, str(dataframe_segment.iloc[0].name), str(dataframe_segment.iloc[len(dataframe_segment) - 1].name), True, best_distance_found)
                    # patterns_found.append(new_pattern)
                    ##########################################################
                    #print("Right index: " + str(right_index) + " Left index: " + str(left_index) + " Window: " + str(right_index - left_index))
                    i += right_index
                else:
                    i += INCREMENT
    else:
        while i < len(company_data) - window_width - 1:
            right_window_index = i + window_width
            #print("I: " + str(i) + " Right: " + str(right_window_index) + " Window: " + str(right_window_index - i))
            if right_window_index >= len(company_data):
                break
            sliced_dataframe = company_data.iloc[i:right_window_index]
            normalized_vector = nu.normalizeVector(sliced_dataframe['SMA'].tolist())
            new_pattern_type, best_distance_found = pattern_utils.findCommonPattern(normalized_vector, patterns_dictionary)
            if new_pattern_type != 'rest_normalized' and new_pattern_type != '' and best_distance_found < 40:
                left_index, right_index = pattern_utils.enhanceDataframeDistancesMean(best_distance_found, new_pattern_type, sliced_dataframe['SMA'].tolist(), patterns_dictionary, [1,2,3,4])
                dataframe_segment = sliced_dataframe[left_index:right_index] #Esto sin ventana mejorada
                longer_dataframe = company_data[i + left_index:] #Quitar left_index si no se usa enhanced dataframe
                ##########################################################
                ## ESTO ES PARA HACERLO CON TENDENCIA
                pattern_tendency = tc.findPatternTendency(dataframe_segment, longer_dataframe, new_pattern_type)
                if pattern_tendency != None:
                    new_pattern = p.Pattern(new_pattern_type, pattern_tendency[1], company_name, str(dataframe_segment.iloc[0].name), str(dataframe_segment.iloc[len(dataframe_segment) - 1].name), pattern_tendency[0], best_distance_found, pattern_tendency[2])
                    patterns_found.append(new_pattern)
                ##########################################################
                ## ESTO ES PARA HACERLO SIN TENDENCIA
                # new_pattern = p.Pattern(new_pattern_type, dataframe_segment, company_name, str(dataframe_segment.iloc[0].name), str(dataframe_segment.iloc[len(dataframe_segment) - 1].name), True, best_distance_found)
                # patterns_found.append(new_pattern)
                ##########################################################
                #print("Right index: " + str(right_index) + " Left index: " + str(left_index) + " Window: " + str(right_index - left_index))
                i += right_index
            else:
                i += INCREMENT
    return patterns_found
