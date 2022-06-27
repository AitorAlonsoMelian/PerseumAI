from dtw import *

def comparePatterns(first_pattern, second_pattern):
    """
    Given two lists, compares them using dtw algorithm  
    
    Args:  
        first_pattern (List[float]): First pattern to be compared
        second_pattern (List[float]): Second pattern to be compared  
    Returns:  
        float: Distance between the two patterns
    """
    alignment_result = dtw(first_pattern, second_pattern, keep_internals=True)
    return alignment_result.distance






















# first_dataframe = pd.read_csv(sys.argv[1], index_col=0)
# second_dataframe = pd.read_csv(sys.argv[2], index_col=0)

# first_data_array = []
# second_data_array = []

# for index,row in first_dataframe.iterrows():
#     first_data_array.append(row[0])

# for index,row in second_dataframe.iterrows():
#     second_data_array.append(row[0])

# print(first_data_array)
# alignment = dtw(first_data_array, second_data_array, keep_internals=True)
# #alignment, cost_matrix, acc_cost_matrix, path = dtw(first_data_array, second_data_array, keep_internals=True, step_pattern=rabinerJuangStepPattern(6, "c"))
# #print(dir(alignment))
# print("Sequence x: ")
# print(alignment.index1)
# print("Sequence y: ")
# print(alignment.index2)
# print(alignment.distance)
# alignment.plot(type='twoway', offset=-2)
#print(alignment.index2)
# plt.imshow(alignment.costMatrix)
# plt.show()

#print(first_dataframe.values.tolist())

#dtw(query, template, keep_internals=True,step_pattern=rabinerJuangStepPattern(6, "c")).plot(type="twoway",offset=-2)