import sys
import os
carpeta_padre = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(carpeta_padre)
import pattern_utils
import Pattern as p
import tendencyCalculator as tc
import matplotlib.pyplot as plt
from random import randint
import normalize_utils as nu
import os
import pandas as pd
import csv



PATTERNS_FILE_PATH = 'patterns/'
PATTERN_TO_ANALIZE = 'descending_triangle'
NUMBER_OF_TRAINING_PATTERNS = 6

pattern_types_set = set()
pattern_types_set.add(PATTERN_TO_ANALIZE)
training_patterns_data = {}
test_patterns_data = {}

for pattern_type in pattern_types_set:
    file_list = os.listdir(PATTERNS_FILE_PATH + pattern_type)
    total_results = []
    training_patterns = set()
    while len(training_patterns) < NUMBER_OF_TRAINING_PATTERNS:
        element_to_add = randint(0, len(file_list) - 1)
        training_patterns.add(file_list[element_to_add])
        file_list.pop(file_list.index(file_list[element_to_add]))
    test_patterns = file_list
    #print("Trainin patterns: " + str(training_patterns))
    #print("Test patterns: " + str(test_patterns))
    total_results = []
    for training_pattern in training_patterns:
        single_file_results = []
        with open(PATTERNS_FILE_PATH + pattern_type + '/' + training_pattern) as csvfile:
            reader = csv.reader(csvfile)
            next(reader, None)
            for row in reader:
                #print(row)
                single_file_results.append(round(float(row[1]), 3))
            total_results.append(single_file_results)
    training_patterns_data[pattern_type] = total_results
    total_results = []
    for test_pattern in test_patterns:
        single_file_results = []
        with open(PATTERNS_FILE_PATH + pattern_type + '/' + test_pattern) as csvfile:
            reader = csv.reader(csvfile)
            next(reader, None)
            for row in reader:
                #print(row)
                single_file_results.append(round(float(row[1]), 3))
            total_results.append(single_file_results)
    test_patterns_data[pattern_type] = total_results
training_patterns_data = pattern_utils.calculateDictSimpleMovingAverage(training_patterns_data, 3)
test_patterns_data = pattern_utils.calculateDictSimpleMovingAverage(test_patterns_data, 3)
array_of_distances = []
for test_pattern_vector in test_patterns_data[PATTERN_TO_ANALIZE]:
    pattern_type, distance = pattern_utils.findCommonPattern(test_pattern_vector, training_patterns_data)
    array_of_distances.append(distance)
    #print("Pattern type: " + pattern_type + " Mean distance: " + str(distance))

print("Mean distance for "+ PATTERN_TO_ANALIZE + ': ' + str(sum(array_of_distances) / len(array_of_distances)))
#print(training_patterns_data)
#print(test_patterns_data)
    
        



#print(os.listdir(PATTERNS_FILE_PATH + "head_and_shoulders"))
