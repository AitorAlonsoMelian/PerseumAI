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
