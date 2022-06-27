from numpy import average
import pandas as pd

BIG_NUMBER = 999999999
predefined_type_of_price = 'Close'

#TODO Añadir que con longer dataset compruebe si pasa la resistencia

def findPatternTendency(data_sequence, longer_data_sequence, type):
    """Method to redirect and calculate the tendency for a given dataframe"""
    if type == 'double_top':
        return findDoubleTopTendency(data_sequence, longer_data_sequence)
    if type == 'double_bottom':
        return findDoubleBottomTendency(data_sequence, longer_data_sequence)
    else:
        raise Exception('Pattern type not found')

def findDoubleTopTendency(data_sequence, longer_data_sequence):
    """Calculates the tendency for a double top pattern  
    
        Args:  
            data_sequence (dataframe): dataframe representing the pattern
            longer_data_sequence (dataframe): dataframe representing the pattern but ends on the day the search is made  
        Return:  
            tendency (Pair[]): first element for True, False or None, and second element for the specific dataframe containing the pattern
            but it ends where the tendency was determined
    """
    first_top = [0, None] #index 0 representa el valor y el index 1 representa la posicion dentro del dataframe
    second_top = [0, None]
    for i in range(data_sequence.size - 1): #Buscar los dos techos
        day_value = data_sequence.iloc[i][predefined_type_of_price]
        if i > 0:
            previous_day_value = data_sequence.iloc[i - 1][predefined_type_of_price]
        if i < data_sequence.size - 1:
            next_day_value = data_sequence.iloc[i + 1][predefined_type_of_price]
        if i > 0 and previous_day_value < day_value and day_value > next_day_value: #hemos encontrado un maximo
            relative_maximum = day_value
            if relative_maximum > first_top[0]: # [1] para acceder a lo que no es timestamps y Close porque es la etiqueta del valor
                first_top = second_top
                second_top = [relative_maximum, i]
            elif relative_maximum > second_top[0]:
                second_top = [relative_maximum, i]
    
    if first_top[1] == None or second_top[1] == None:
        return None #No se encontraron dos techos

    resistance = [BIG_NUMBER, None]
    for i in range(first_top[1], second_top[1]): #Busqueda de la linea de apoyo
        current_value = data_sequence.iloc[i][predefined_type_of_price]
        if current_value < resistance[0]:
            resistance[0] = current_value
            resistance[1] = i

    #Añadir que los dos techo no estas muy lejos, como mucho en la mitad entre el mas alto y la linea de soporte

    first_top_to_resistance_distance = first_top[0] - resistance[0]
    second_top_to_resistance_distance = second_top[0] - resistance[0]
    if first_top_to_resistance_distance > second_top_to_resistance_distance and second_top_to_resistance_distance < first_top_to_resistance_distance * 2 / 3:
        return None # Demasiada diferencia entre techos
    if second_top_to_resistance_distance > first_top_to_resistance_distance and first_top_to_resistance_distance < second_top_to_resistance_distance * 2 / 3:
        return None # Demasiada diferencia entre techos

    breaks_resistance_from_left = [False, None]
    breaks_resistance_from_right = [False, None]

    #Confirmar que en rompe por la linea de apoyo en ambos lados
    i = first_top[1]
    while i >= 0 and not breaks_resistance_from_left[0]:
        current_value_left = data_sequence.iloc[i][predefined_type_of_price]
        if current_value_left < resistance[0]:
            breaks_resistance_from_left[0] = True
            breaks_resistance_from_left[1] = i
        i -= 1

    # Hacer esto pero en longer dataset
    i = second_top[1]
    while i < data_sequence.size and not breaks_resistance_from_right[0]:
        current_value_right = data_sequence.iloc[i][predefined_type_of_price]
        if current_value_right < resistance[0]:
            breaks_resistance_from_right[0] = True
            breaks_resistance_from_right[1] = i
        i += 1

    if breaks_resistance_from_left[1] is None or breaks_resistance_from_right[1] is None: # Comprobar que se rompe la linea de apoyo
        return None
        #DiscardPatterns
    #Una vez rompe el patron, debemos averiguar en que direccion

    pattern_width = breaks_resistance_from_right[1] - breaks_resistance_from_left[1]

    average_height = ((first_top[0] + second_top[0]) / 2) - resistance[0]
    objective = resistance[0] - average_height

    if pattern_width:
        for i in range(breaks_resistance_from_right[1], breaks_resistance_from_right[1] + pattern_width * 2):
            if i >= longer_data_sequence.size:
                break
            current_value = longer_data_sequence.iloc[i][predefined_type_of_price]
            if current_value > resistance[0]:
                return [False, longer_data_sequence.iloc[:i + 1]]
            if current_value < objective:
                return [True, longer_data_sequence.iloc[:i + 1]]
    else:
        return None #Significa que el valor no cruzo ningun limite

def findDoubleBottomTendency(data_sequence, longer_data_sequence):
    """Calculates the tendency for a double top pattern  

        Args:  
            data_sequence (dataframe): dataframe representing the pattern
            longer_data_sequence (dataframe): dataframe representing the pattern but ends on the day the search is made  
        Return:  
            tendency (Pair[]): first element for True, False or None, and second element for the specific dataframe containing the pattern
            but it ends where the tendency was determined
    """
    first_bottom = [BIG_NUMBER, None] #index 0 representa el valor y el index 1 representa la posicion dentro del dataframe
    second_bottom = [BIG_NUMBER, None]
    for i in range(data_sequence.size - 1): #Buscar los dos suelos
        day_value = data_sequence.iloc[i][predefined_type_of_price]
        if i > 0:
            previous_day_value = data_sequence.iloc[i - 1][predefined_type_of_price]
        if i < data_sequence.size - 1:
            next_day_value = data_sequence.iloc[i + 1][predefined_type_of_price]
        if i > 0 and previous_day_value > day_value and day_value < next_day_value: #hemos encontrado un minimo
            relative_minimum = day_value
            if relative_minimum < first_bottom[0]: # [1] para acceder a lo que no es timestamps y Close porque es la etiqueta del valor
                first_bottom = second_bottom
                second_bottom = [relative_minimum, i]
            elif relative_minimum < second_bottom[0]:
                second_bottom = [relative_minimum, i]
    
    if first_bottom[1] == None or second_bottom[1] == None:
        return None #No se encontraron dos suelos

    resistance = [0, None]
    for i in range(first_bottom[1], second_bottom[1]): #Busqueda de la linea de apoyo
        current_value = data_sequence.iloc[i][predefined_type_of_price]
        if current_value > resistance[0]:
            resistance[0] = current_value
            resistance[1] = i

    # Comprobamos si los suelos no estan muy lejos
    first_bottom_to_resistance_distance = resistance[0] - first_bottom[0]
    second_bottom_to_resistance_distance = resistance[0] - second_bottom[0]
    if first_bottom_to_resistance_distance > second_bottom_to_resistance_distance and second_bottom_to_resistance_distance < first_bottom_to_resistance_distance * 2 / 3:
        return None # Demasiada diferencia entre suelos
    if second_bottom_to_resistance_distance > first_bottom_to_resistance_distance and first_bottom_to_resistance_distance < second_bottom_to_resistance_distance * 2 / 3:
        return None # Demasiada diferencia entre suelos

    breaks_resistance_from_left = [False, None]
    breaks_resistance_from_right = [False, None]

    #Confirmar que en rompe por la linea de apoyo en ambos lados
    i = first_bottom[1]
    while i >= 0 and not breaks_resistance_from_left[0]:
        current_value_left = data_sequence.iloc[i][predefined_type_of_price]
        if current_value_left > resistance[0]:
            breaks_resistance_from_left[0] = True
            breaks_resistance_from_left[1] = i
        i -= 1

    # Hacer esto pero en longer dataset
    i = second_bottom[1]
    while i < data_sequence.size and not breaks_resistance_from_right[0]:
        current_value_right = data_sequence.iloc[i][predefined_type_of_price]
        if current_value_right > resistance[0]:
            breaks_resistance_from_right[0] = True
            breaks_resistance_from_right[1] = i
        i += 1

    if breaks_resistance_from_left[1] is None or breaks_resistance_from_right[1] is None: # Comprobar que se rompe la linea de apoyo
        return None # Pattern\'s resistance not broken
    #Una vez rompe el patron, debemos averiguar en que direccion

    pattern_width = breaks_resistance_from_right[1] - breaks_resistance_from_left[1]

    average_height = abs(((first_bottom[0] + second_bottom[0]) / 2) - resistance[0])
    objective = resistance[0] + average_height
    if pattern_width:
        for i in range(breaks_resistance_from_right[1], breaks_resistance_from_right[1] + pattern_width):
            if i >= longer_data_sequence.size:
                break
            current_value = longer_data_sequence.iloc[i][predefined_type_of_price]
            if current_value < resistance[0]:
                return [False, longer_data_sequence.iloc[:i + 1]]
            if current_value > objective:
                return [True, longer_data_sequence.iloc[:i + 1]]
    else:
        return None #Significa que el valor no cruzo ningun limite