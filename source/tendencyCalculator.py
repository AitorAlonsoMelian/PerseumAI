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
    if type == 'head_and_shoulders':
        return findHeadAndShouldersTendency(data_sequence, longer_data_sequence)
    if type == 'inv_head_and_shoulders':
        return findInverseHeadAndShouldersTendency(data_sequence, longer_data_sequence)
    if type == 'descending_triangle':
        return findDescendingTriangleTendency(data_sequence, longer_data_sequence)
    if type == 'ascending_triangle':
        return findAscendingTriangleTendency(data_sequence, longer_data_sequence)
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
    for i in range(len(data_sequence) - 3): #Buscar los dos techos
        day_value = data_sequence.iloc[i][predefined_type_of_price]
        if i > 1 and all(x <= day_value for x in data_sequence.iloc[i-2:i][predefined_type_of_price]) and all(x <= day_value for x in data_sequence.iloc[i+1:i+3][predefined_type_of_price]): #hemos encontrado un maximo
            relative_maximum = day_value
            if relative_maximum > first_top[0]: 
                first_top = second_top
                second_top = [relative_maximum, i]
            elif relative_maximum > second_top[0]:
                second_top = [relative_maximum, i]
    
    if first_top[1] == None or second_top[1] == None:
        return None #No se encontraron dos techos

    support = [BIG_NUMBER, None]
    for i in range(first_top[1], second_top[1]): #Busqueda de la linea de apoyo
        current_value = data_sequence.iloc[i][predefined_type_of_price]
        if current_value < support[0]:
            support[0] = current_value
            support[1] = i

    #Añadir que los dos techo no estas muy lejos, como mucho en la mitad entre el mas alto y la linea de soporte
    first_top_to_support_distance = first_top[0] - support[0]
    second_top_to_support_distance = second_top[0] - support[0]
    if first_top_to_support_distance > second_top_to_support_distance and second_top_to_support_distance < first_top_to_support_distance * 2 / 3:
        return None # Demasiada diferencia entre techos
    if second_top_to_support_distance > first_top_to_support_distance and first_top_to_support_distance < second_top_to_support_distance * 2 / 3:
        return None # Demasiada diferencia entre techos
    if abs(first_top[1] - second_top[1]) < 5:
        return None

    breaks_support_from_left = [False, None]
    breaks_support_from_right = [False, None]

    #Confirmar que en rompe por la linea de apoyo en ambos lados
    i = first_top[1]
    while i >= 0 and not breaks_support_from_left[0]:
        current_value_left = data_sequence.iloc[i][predefined_type_of_price]
        if current_value_left < support[0]:
            breaks_support_from_left[0] = True
            breaks_support_from_left[1] = i
        i -= 1

    # Hacer esto pero en longer dataset
    i = second_top[1]
    while i < len(data_sequence) and not breaks_support_from_right[0]:
        current_value_right = data_sequence.iloc[i][predefined_type_of_price]
        if current_value_right < support[0]:
            breaks_support_from_right[0] = True
            breaks_support_from_right[1] = i
        i += 1

    if breaks_support_from_left[1] is None or breaks_support_from_right[1] is None: # Comprobar que se rompe la linea de apoyo
        return None
        #DiscardPatterns
    #Una vez rompe el patron, debemos averiguar en que direccion

    pattern_width = breaks_support_from_right[1] - breaks_support_from_left[1]

    average_height = ((first_top[0] + second_top[0]) / 2) - support[0]
    objective = support[0] - average_height

    objective_line = pd.Series(objective, index=data_sequence.iloc[[breaks_support_from_right[1]]].index, name='Close')
    if breaks_support_from_right[1] + pattern_width >= len(longer_data_sequence):
        new_date_3 = pd.to_datetime(longer_data_sequence.iloc[[len(longer_data_sequence) - 1]].index)
    else:
        new_date_3 = pd.to_datetime(longer_data_sequence.iloc[[breaks_support_from_right[1] + pattern_width]].index)
    objective_line_2 = pd.Series(objective, index=new_date_3, name='Close')
    objective_line = pd.concat([objective_line, objective_line_2])

    if pattern_width:
        if any(x < objective for x in longer_data_sequence.iloc[breaks_support_from_right[1]:breaks_support_from_right[1] + pattern_width][predefined_type_of_price]):
            return [True, longer_data_sequence.iloc[:breaks_support_from_right[1] + pattern_width], [longer_data_sequence.iloc[[first_top[1],second_top[1]]][predefined_type_of_price], objective_line]]
        else:
            return [False, longer_data_sequence.iloc[:breaks_support_from_right[1] + pattern_width], [longer_data_sequence.iloc[[first_top[1],second_top[1]]][predefined_type_of_price], objective_line]]
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
    for i in range(len(data_sequence) - 3): #Buscar los dos suelos
        day_value = data_sequence.iloc[i][predefined_type_of_price]
        if i > 1 and all(x > day_value for x in data_sequence.iloc[i - 2:i][predefined_type_of_price]) and all(x > day_value for x in data_sequence.iloc[i + 1:i + 3][predefined_type_of_price]):
            relative_minimum = day_value
            if relative_minimum < first_bottom[0]:
                first_bottom = second_bottom
                second_bottom = [relative_minimum, i]
            elif relative_minimum < second_bottom[0]:
                second_bottom = [relative_minimum, i]
    
    if first_bottom[1] == None or second_bottom[1] == None:
        return None #No se encontraron dos suelos

    resistance = [0, None]
    for i in range(first_bottom[1], second_bottom[1]): #Busqueda de la linea de resistencia
        current_value = data_sequence.iloc[i][predefined_type_of_price]
        if current_value > resistance[0]:
            resistance[0] = current_value
            resistance[1] = i

    # Comprobamos si las resistencias no estan muy lejos
    first_bottom_to_resistance_distance = resistance[0] - first_bottom[0]
    second_bottom_to_resistance_distance = resistance[0] - second_bottom[0]
    if first_bottom_to_resistance_distance > second_bottom_to_resistance_distance and second_bottom_to_resistance_distance < first_bottom_to_resistance_distance * 2 / 3:
        return None # Demasiada diferencia entre resistencias
    if second_bottom_to_resistance_distance > first_bottom_to_resistance_distance and first_bottom_to_resistance_distance < second_bottom_to_resistance_distance * 2 / 3:
        return None # Demasiada diferencia entre resistencias
    if abs(first_bottom[1] - second_bottom[1]) < 5:
        return None

    breaks_resistance_from_left = [False, None]
    breaks_resistance_from_right = [False, None]

    #Confirmar que en rompe por la linea de resistencia en ambos lados
    i = first_bottom[1]
    while i >= 0 and not breaks_resistance_from_left[0]:
        current_value_left = data_sequence.iloc[i][predefined_type_of_price]
        if current_value_left > resistance[0]:
            breaks_resistance_from_left[0] = True
            breaks_resistance_from_left[1] = i
        i -= 1

    # Hacer esto pero en longer dataset
    i = second_bottom[1]
    while i < len(data_sequence) and not breaks_resistance_from_right[0]:
        current_value_right = data_sequence.iloc[i][predefined_type_of_price]
        if current_value_right > resistance[0]:
            breaks_resistance_from_right[0] = True
            breaks_resistance_from_right[1] = i
        i += 1

    if breaks_resistance_from_left[1] is None or breaks_resistance_from_right[1] is None: # Comprobar que se rompe la linea de resistencia
        return None # Pattern\'s resistance not broken
    #Una vez rompe el patron, debemos averiguar en que direccion

    pattern_width = breaks_resistance_from_right[1] - breaks_resistance_from_left[1]

    average_height = abs(((first_bottom[0] + second_bottom[0]) / 2) - resistance[0])
    objective = resistance[0] + average_height

    objective_line = pd.Series(objective, index=data_sequence.iloc[[breaks_resistance_from_right[1]]].index, name='Close')
    if breaks_resistance_from_right[1] + pattern_width >= len(longer_data_sequence):
        new_date_3 = pd.to_datetime(longer_data_sequence.iloc[[len(longer_data_sequence) - 1]].index)
    else:
        new_date_3 = pd.to_datetime(longer_data_sequence.iloc[[breaks_resistance_from_right[1] + pattern_width]].index)
    objective_line_2 = pd.Series(objective, index=new_date_3, name='Close')
    objective_line = pd.concat([objective_line, objective_line_2])

    if pattern_width:
        if any(x > objective for x in longer_data_sequence.iloc[breaks_resistance_from_right[1]:breaks_resistance_from_right[1] + pattern_width][predefined_type_of_price]):
            return [True, longer_data_sequence.iloc[:breaks_resistance_from_right[1] + pattern_width], [longer_data_sequence.iloc[[first_bottom[1],second_bottom[1]]][predefined_type_of_price], objective_line]]
        else:
            return [False, longer_data_sequence.iloc[:breaks_resistance_from_right[1] + pattern_width], [longer_data_sequence.iloc[[first_bottom[1],second_bottom[1]]][predefined_type_of_price], objective_line]]
    else:
        return None #Significa que el valor no cruzo ningun limite
    
def findHeadAndShouldersTendency(data_sequence, longer_data_sequence):
    """Calculates the tendency for a head and shoulders pattern  

        Args:  
            data_sequence (dataframe): dataframe representing the pattern
            longer_data_sequence (dataframe): dataframe representing the pattern but ends on the day the search is made  
        Return:  
            tendency (Pair[]): first element for True, False or None, and second element for the specific dataframe containing the pattern
            but it ends where the tendency was determined
    """
    first_top = [0, None] #index 0 representa el valor y el index 1 representa la posicion dentro del dataframe
    second_top = [0, None]
    third_top = [0, None]
    for i in range(len(data_sequence) - 3): #Buscar 3 tops
        day_value = data_sequence.iloc[i][predefined_type_of_price]
        if i > 1 and all(x <= day_value for x in data_sequence.iloc[i-2:i][predefined_type_of_price]) and all(x <= day_value for x in data_sequence.iloc[i+1:i+3][predefined_type_of_price]): #hemos encontrado un maximo
            relative_maximum = day_value
            if relative_maximum > first_top[0]: 
                third_top = second_top
                second_top = first_top
                first_top = [relative_maximum, i]
            elif relative_maximum > second_top[0] and i not in range(first_top[1] - 5, first_top[1] + 5):
                third_top = second_top
                second_top = [relative_maximum, i]
            elif relative_maximum > third_top[0] and i not in range(first_top[1] - 5, first_top[1] + 5):
                third_top = [relative_maximum, i]


    if first_top[1] == None or second_top[1] == None or third_top[1] == None:
        return None #No se encontró alguno de los 3 techos
    if first_top[1] > second_top[1] and first_top[1] > third_top[1]:
        return None # La cabeza no está en medio
    if first_top[1] < second_top[1] and first_top[1] < third_top[1]:
        return None # La cabeza no está en medio

    support = [BIG_NUMBER, None]
    second_top_support = [BIG_NUMBER, None]
    third_top_support = [BIG_NUMBER, None]
    if second_top[1] > third_top[1]:
        for i in range(third_top[1], second_top[1]): #Busqueda de la linea de apoyo
            current_value = data_sequence.iloc[i][predefined_type_of_price]
            if current_value < support[0]:
                support[0] = current_value
                support[1] = i
            if i < first_top[1] and current_value < third_top_support[0]:
                third_top_support[0] = current_value
                third_top_support[1] = i
            if i > first_top[1] and current_value < second_top_support[0]:
                second_top_support[0] = current_value
                second_top_support[1] = i
    else:
        for i in range(second_top[1], third_top[1]):
            current_value = data_sequence.iloc[i][predefined_type_of_price]
            if current_value < support[0]:
                support[0] = current_value
                support[1] = i
            if i < first_top[1] and current_value < third_top_support[0]:
                third_top_support[0] = current_value
                third_top_support[1] = i
            if i > first_top[1] and current_value < second_top_support[0]:
                second_top_support[0] = current_value
                second_top_support[1] = i

    # Se comprueba que los hombros están a alturas similares
    first_top_to_support_distance = first_top[0] - support[0]
    second_top_to_support_distance = second_top[0] - support[0]
    third_top_to_support_distance = third_top[0] - support[0]
    if third_top_to_support_distance > second_top_to_support_distance and second_top_to_support_distance < third_top_to_support_distance * 2 / 3:
        return None
    if second_top_to_support_distance > third_top_to_support_distance and third_top_to_support_distance < second_top_to_support_distance * 2 / 3:
        return None
    if first_top_to_support_distance * 0.85 < second_top_to_support_distance or first_top_to_support_distance * 0.85 < third_top_to_support_distance:
        return None
    if (first_top[0]/second_top[0] < 1.007 and first_top[0]/second_top[0] > 0.993) or (first_top[0]/third_top[0] < 1.007 and first_top[0]/third_top[0] > 0.993):
        return None
    
    # Comprobar la altura entre los suelos y la cabeza
    if not (second_top_support[0]/third_top_support[0] < 1.02 and second_top_support[0]/third_top_support[0] > 0.98):
        return None


    #Confirmar que en rompe por la linea de apoyo en ambos lados
    breaks_support_from_left = [False, None]
    breaks_support_from_right = [False, None]
    i = first_top[1]
    while i >= 0 and not breaks_support_from_left[0]:
        current_value_left = data_sequence.iloc[i][predefined_type_of_price]
        if current_value_left < support[0]:
            breaks_support_from_left[0] = True
            breaks_support_from_left[1] = i
        i -= 1

    # Hacer esto pero en longer dataset
    i = first_top[1]
    while i < len(data_sequence) and not breaks_support_from_right[0]:
        current_value_right = data_sequence.iloc[i][predefined_type_of_price]
        if current_value_right < support[0]:
            breaks_support_from_right[0] = True
            breaks_support_from_right[1] = i
        i += 1

    if breaks_support_from_left[1] is None or breaks_support_from_right[1] is None: # Comprobar que se rompe la linea de apoyo
        return None # Pattern\'s support not broken
    #Una vez rompe el patron, debemos averiguar en que direccion

    pattern_width = breaks_support_from_right[1] - breaks_support_from_left[1]
    if pattern_width < 12:
        return None # Patrón demasiado pequeño

    average_height = abs(((first_top[0] + second_top[0]) / 2) - support[0])
    objective = support[0] - average_height

    objective_line = pd.Series(objective, index=data_sequence.iloc[[breaks_support_from_right[1]]].index, name='Close')
    if breaks_support_from_right[1] + pattern_width >= len(longer_data_sequence):
        new_date_3 = pd.to_datetime(longer_data_sequence.iloc[[len(longer_data_sequence) - 1]].index)
    else:
        new_date_3 = pd.to_datetime(longer_data_sequence.iloc[[breaks_support_from_right[1] + pattern_width]].index)
    objective_line_2 = pd.Series(objective, index=new_date_3, name='Close')
    objective_line = pd.concat([objective_line, objective_line_2])

    if pattern_width:
        if any(x < objective for x in longer_data_sequence.iloc[breaks_support_from_right[1]:breaks_support_from_right[1] + pattern_width][predefined_type_of_price]):
            return [True, longer_data_sequence.iloc[:breaks_support_from_right[1] + pattern_width], [longer_data_sequence.iloc[[second_top[1],first_top[1],third_top[1]]][predefined_type_of_price], objective_line]]
        else:
            return [False, longer_data_sequence.iloc[:breaks_support_from_right[1] + pattern_width], [longer_data_sequence.iloc[[second_top[1],first_top[1],third_top[1]]][predefined_type_of_price], objective_line]]
    else:
        return None

def findInverseHeadAndShouldersTendency(data_sequence, longer_data_sequence):
    """Calculates the tendency for a head and shoulders pattern  

        Args:  
            data_sequence (dataframe): dataframe representing the pattern
            longer_data_sequence (dataframe): dataframe representing the pattern but ends on the day the search is made  
        Return:  
            tendency (Pair[]): first element for True, False or None, and secondthird_top element for the specific dataframe containing the pattern
            but it ends where the tendency was determined
    """
    first_bottom = [BIG_NUMBER, None] #index 0 representa el valor y el index 1 representa la posicion dentro del dataframe
    second_bottom = [BIG_NUMBER, None]
    third_bottom = [BIG_NUMBER, None]
    for i in range(len(data_sequence) - 3): #Buscar 3 bottoms
        day_value = data_sequence.iloc[i][predefined_type_of_price]
        if i > 1 and all(x >= day_value for x in data_sequence.iloc[i-2:i][predefined_type_of_price]) and all(x >= day_value for x in data_sequence.iloc[i+1:i+3][predefined_type_of_price]): #hemos encontrado un minimo
            relative_minimum = day_value
            if relative_minimum < first_bottom[0]: 
                third_bottom = second_bottom
                second_bottom = first_bottom
                first_bottom = [relative_minimum, i]
            elif relative_minimum < second_bottom[0] and i not in range(first_bottom[1] - 5, first_bottom[1] + 5):
                third_bottom = second_bottom
                second_bottom = [relative_minimum, i]
            elif relative_minimum < third_bottom[0] and i not in range(first_bottom[1] - 5, first_bottom[1] + 5):
                third_bottom = [relative_minimum, i]

    if first_bottom[1] == None or second_bottom[1] == None or third_bottom[1] == None:
        return None #No se encontró alguno de los 3 suelos
    if first_bottom[1] > second_bottom[1] and first_bottom[1] > third_bottom[1]:
        return None # La cabeza no está en medio
    if first_bottom[1] < second_bottom[1] and first_bottom[1] < third_bottom[1]:
        return None # La cabeza no está en medio
    resistance = [0, None]
    second_shoulder_resistance = [0, None]
    third_shoulder_resistance = [0, None]
    if second_bottom[1] > third_bottom[1]:
        rangeofsearch = range(third_bottom[1], second_bottom[1])
    else:
        rangeofsearch = range(second_bottom[1], third_bottom[1])
    for i in rangeofsearch: #Busqueda de la linea de resistencia
        current_value = data_sequence.iloc[i][predefined_type_of_price]
        if current_value > resistance[0]:
            resistance[0] = current_value
            resistance[1] = i
        if i < first_bottom[1] and current_value > third_shoulder_resistance[0]:
            third_shoulder_resistance[0] = current_value
            third_shoulder_resistance[1] = i
        if i > first_bottom[1] and current_value > second_shoulder_resistance[0]:
            second_shoulder_resistance[0] = current_value
            second_shoulder_resistance[1] = i

    # Se comprueba que los picos están a alturas similares
    first_bottom_to_resistance_distance = resistance[0] - first_bottom[0]
    second_bottom_to_resistance_distance = resistance[0] - second_bottom[0]
    third_bottom_to_resistance_distance = resistance[0] - third_bottom[0]
    if third_bottom_to_resistance_distance > second_bottom_to_resistance_distance and second_bottom_to_resistance_distance < third_bottom_to_resistance_distance * 2 / 3:
        return None
    if second_bottom_to_resistance_distance > third_bottom_to_resistance_distance and third_bottom_to_resistance_distance < second_bottom_to_resistance_distance * 2 / 3:
        return None
    if first_bottom_to_resistance_distance * 0.85 < second_bottom_to_resistance_distance or first_bottom_to_resistance_distance * 0.85 < third_bottom_to_resistance_distance:
        return None
    # Comprobar la altura entre los suelos y la cabeza
    if not (second_shoulder_resistance[0]/third_shoulder_resistance[0] < 1.04 and second_shoulder_resistance[0]/third_shoulder_resistance[0] > 0.96):
        return None

    #Confirmar que en rompe por la linea de apoyo en ambos lados
    breaks_support_from_left = [False, None]
    breaks_support_from_right = [False, None]
    i = first_bottom[1]
    while i >= 0 and not breaks_support_from_left[0]:
        current_value_left = data_sequence.iloc[i][predefined_type_of_price]
        if current_value_left > resistance[0]:
            breaks_support_from_left[0] = True
            breaks_support_from_left[1] = i
        i -= 1

    # Hacer esto pero en longer dataset
    i = first_bottom[1]
    while i < len(data_sequence) and not breaks_support_from_right[0]:
        current_value_right = data_sequence.iloc[i][predefined_type_of_price]
        if current_value_right > resistance[0]:
            breaks_support_from_right[0] = True
            breaks_support_from_right[1] = i
        i += 1

    if breaks_support_from_left[1] is None or breaks_support_from_right[1] is None: # Comprobar que se rompe la linea de apoyo
        return None # Pattern\'s support not broken

    pattern_width = breaks_support_from_right[1] - breaks_support_from_left[1]
    if pattern_width < 12:
        return None # Patrón demasiado pequeño
    average_height = abs(((first_bottom[0] + second_bottom[0] + third_bottom[0]) / 3) - resistance[0])
    objective = resistance[0] + average_height

    objective_line = pd.Series(objective, index=data_sequence.iloc[[breaks_support_from_right[1]]].index, name='Close')
    if breaks_support_from_right[1] + pattern_width >= len(longer_data_sequence):
        new_date_3 = pd.to_datetime(longer_data_sequence.iloc[[len(longer_data_sequence) - 1]].index)
    else:
        new_date_3 = pd.to_datetime(longer_data_sequence.iloc[[breaks_support_from_right[1] + pattern_width]].index)
    objective_line_2 = pd.Series(objective, index=new_date_3, name='Close')
    objective_line = pd.concat([objective_line, objective_line_2])

    limit = breaks_support_from_right[1] + pattern_width
    if pattern_width:
        if any(x > objective for x in longer_data_sequence.iloc[breaks_support_from_right[1]:limit][predefined_type_of_price]):
            return [True, longer_data_sequence.iloc[:limit], [longer_data_sequence.iloc[[second_bottom[1],first_bottom[1],third_bottom[1]]][predefined_type_of_price], objective_line]]
        else:
            return [False, longer_data_sequence.iloc[:limit], [longer_data_sequence.iloc[[second_bottom[1],first_bottom[1],third_bottom[1]]][predefined_type_of_price], objective_line]]
    else:
        return None


def findDescendingTriangleTendency(data_sequence, longer_data_sequence):
    """Calculates the tendency for a descending triangle pattern

        Args:
            data_sequence (dataframe): dataframe representing the pattern
            longer_data_sequence (dataframe): dataframe representing the pattern but ends on the day the search is made
        Return:
            tendency (Pair[]): first element for True, False or None, and second element for the specific dataframe containing the pattern
            but it ends where the tendency was determined
    """
    support = [BIG_NUMBER, None]
    for i in range(int(len(data_sequence)*(2/3))):
        day_value = data_sequence.iloc[i][predefined_type_of_price]
        if day_value < support[0]:
            support[0] = day_value
            support[1] = i

    times_near_support = 0

    local_maxs = []
    absolute_maximum = [0, None]
    for i in range(len(data_sequence) - 1):
        # Comprobar si es un máximo local
        if data_sequence.iloc[i][predefined_type_of_price] < data_sequence.iloc[i + 1][predefined_type_of_price] and data_sequence.iloc[i][predefined_type_of_price] < data_sequence.iloc[i - 1][predefined_type_of_price]:
            if (data_sequence.iloc[i][predefined_type_of_price] / support[0]) > 0.98 and (data_sequence.iloc[i][predefined_type_of_price] / support[0]) < 1.02:
                times_near_support += 1
        if all(x < data_sequence.iloc[i][predefined_type_of_price] for x in data_sequence.iloc[i-3:i][predefined_type_of_price]) and all (x < data_sequence.iloc[i][predefined_type_of_price] for x in data_sequence.iloc[i+1:i+4][predefined_type_of_price]):
            local_maxs.append(i)
        if data_sequence.iloc[i][predefined_type_of_price] > absolute_maximum[0]:
            absolute_maximum = [data_sequence.iloc[i][predefined_type_of_price], i]

    #  Comprobar que el precio se acerca al soporte al menos 3 veces
    if times_near_support < 3:
        return None
    # Comprobar que el máximo absoluto está en el primer tercio del patrón
    if absolute_maximum[1] > len(data_sequence) / 3:
        return None 
    # Comprobar que los máximos locales son decrecientes
    for i in range(len(local_maxs)):
        if local_maxs[i] <= absolute_maximum[1]:
            continue
        if data_sequence.iloc[local_maxs[i]][predefined_type_of_price] * 0.96 > data_sequence.iloc[local_maxs[i-1]][predefined_type_of_price]: # Si un pico es mayor que el anterior en un 4% o más se descarta
            return None
        
    # Comprobar si el triangulo está cerrado (O próximo a cerrarse)
    if (data_sequence.iloc[-1][predefined_type_of_price] / support[0]) > 1.03:
        return None
    pattern_height = absolute_maximum[0] - support[0]
    if (data_sequence.iloc[-1][predefined_type_of_price] - support[0]) > pattern_height * 0.20:
        return None
    
    # Crear la pendiente de la diagonal P(X,Y) = (indice,valor) P1 = (Maximo absoluto), P2 = (Ultimo valor del patron)
    m = (data_sequence.iloc[absolute_maximum[1]][predefined_type_of_price] - data_sequence.iloc[-1][predefined_type_of_price] )/(absolute_maximum[1] - (len(data_sequence)-1))
    b =  absolute_maximum[0] - m * absolute_maximum[1]
    intersection = None
    for i in range(absolute_maximum[1], len(data_sequence)):
        if data_sequence.iloc[i][predefined_type_of_price] / (m * i + b) > 1.01:
            return None
        if ((m * i + b) / support[0]) < 1.01 and ((m * i + b) / support[0]) > 0.99:
            intersection = i

    # Se crea la línea de soporte y la línea diagonal
    support_line = longer_data_sequence.iloc[[support[1]]][predefined_type_of_price]

    new_date = pd.to_datetime(data_sequence.iloc[[0]].index)
    new_entry = pd.Series(support_line.iloc[0], index=new_date, name='Close')
    if intersection is None:
        new_date_2 = pd.to_datetime(data_sequence.iloc[[-1]].index) #+ pd.DateOffset(days=5)
    else:
        new_date_2 = pd.to_datetime(data_sequence.iloc[[intersection]].index)
    new_entry_2 = pd.Series(support_line.iloc[0], index=new_date_2, name='Close')

    support_line = pd.concat([support_line, new_entry, new_entry_2])

    new_entry_3 = pd.Series(data_sequence.iloc[absolute_maximum[1]][predefined_type_of_price], index=data_sequence.iloc[[absolute_maximum[1]]].index, name='Close')
    if intersection is None:
        new_entry_4 = pd.Series(data_sequence.iloc[-1][predefined_type_of_price], index=new_date_2, name='Close')
    else:
        new_entry_4 = pd.Series(data_sequence.iloc[intersection][predefined_type_of_price], index=new_date_2, name='Close')
    diagonal_line = pd.concat([new_entry_3, new_entry_4])

    #Comprobar que se cumple el objetivo del patrón.
    objective = support[0] - ((absolute_maximum[0] - support[0])*0.70)

    objective_line = pd.Series(objective, index=data_sequence.iloc[[-1]].index, name='Close')
    new_date_3 = pd.to_datetime(data_sequence.iloc[[-1]].index) + pd.DateOffset(days=(int(len(data_sequence)* 1.5)))
    if new_date_3 > longer_data_sequence.iloc[[-1]].index:
        new_date_3 = pd.to_datetime(longer_data_sequence.iloc[[-1]].index)
    objective_line_2 = pd.Series(objective, index=new_date_3, name='Close')
    objective_line = pd.concat([objective_line, objective_line_2])
        
    limit = len(data_sequence) * 2
    if limit > len(longer_data_sequence):
        limit = len(longer_data_sequence)-1
    if any(x <= objective for x in longer_data_sequence.iloc[len(data_sequence):limit][predefined_type_of_price]):
        return [True, longer_data_sequence.iloc[:limit], [support_line, diagonal_line, objective_line]]
    else:
        return [False, longer_data_sequence.iloc[:limit], [support_line, diagonal_line, objective_line]]
    


def findAscendingTriangleTendency(data_sequence, longer_data_sequence):
    """Calculates the tendency for a ascending triangle pattern

        Args:
            data_sequence (dataframe): dataframe representing the pattern
            longer_data_sequence (dataframe): dataframe representing the pattern but ends on the day the search is made
        Return:
            tendency (Pair[]): first element for True, False or None, and second element for the specific dataframe containing the pattern
            but it ends where the tendency was determined
    """

    resistance = [0, None]
    for i in range(int(len(data_sequence)*(2/3))):
        day_value = data_sequence.iloc[i][predefined_type_of_price]
        if day_value > resistance[0]:
            resistance[0] = day_value
            resistance[1] = i

    times_near_resistance = 0

    local_mins = []
    absolute_minimum = [BIG_NUMBER, None]
    for i in range(len(data_sequence) - 1):
        # Comprobar si es un máximo local
        if data_sequence.iloc[i][predefined_type_of_price] > data_sequence.iloc[i + 1][predefined_type_of_price] and data_sequence.iloc[i][predefined_type_of_price] > data_sequence.iloc[i - 1][predefined_type_of_price]:
            if (data_sequence.iloc[i][predefined_type_of_price] / resistance[0]) > 0.98 and (data_sequence.iloc[i][predefined_type_of_price] / resistance[0]) < 1.02:
                times_near_resistance += 1
        if all(x > data_sequence.iloc[i][predefined_type_of_price] for x in data_sequence.iloc[i-3:i][predefined_type_of_price]) and all (x > data_sequence.iloc[i][predefined_type_of_price] for x in data_sequence.iloc[i+1:i+4][predefined_type_of_price]):
            local_mins.append(i)
        if data_sequence.iloc[i][predefined_type_of_price] < absolute_minimum[0]:
            absolute_minimum = [data_sequence.iloc[i][predefined_type_of_price], i]

    #  Comprobar que el precio se acerca a la resistencia al menos 3 veces
    if times_near_resistance < 3:
        return None
    # Comprobar que el máximo absoluto está en el primer tercio del patrón
    if absolute_minimum[1] > len(data_sequence) / 3:
        return None 
    # Comprobar que los mínimos locales son ascendentes
    for i in range(len(local_mins)):
        if local_mins[i] <= absolute_minimum[1]:
            continue
        if data_sequence.iloc[local_mins[i]][predefined_type_of_price] * 1.04 < data_sequence.iloc[local_mins[i-1]][predefined_type_of_price]: # Si un pico es mayor que el anterior en un 4% o más se descarta
            return None
        
    # Comprobar si el triangulo está cerrado (O próximo a cerrarse)
    if (data_sequence.iloc[-1][predefined_type_of_price] / resistance[0]) < 0.97:
        return None
    pattern_height = resistance[0] - absolute_minimum[0]
    if (resistance[0] - data_sequence.iloc[-1][predefined_type_of_price]) > pattern_height * 0.20:
        return None
    
    # Crear la pendiente de la diagonal P(X,Y) = (indice,valor) P1 = (Mínimo absoluto), P2 = (Ultimo valor del patron)
    m = (data_sequence.iloc[absolute_minimum[1]][predefined_type_of_price] - data_sequence.iloc[-1][predefined_type_of_price] )/(absolute_minimum[1] - (len(data_sequence)-1))
    b =  absolute_minimum[0] - m * absolute_minimum[1]
    intersection = None
    for i in range(absolute_minimum[1], len(data_sequence)):
        if data_sequence.iloc[i][predefined_type_of_price] / (m * i + b) < 0.99:
            return None
        if ((m * i + b) / resistance[0]) < 1.01 and ((m * i + b) / resistance[0]) > 0.99:
            intersection = i

    # Se crea la línea de soporte y la línea diagonal
    support_line = longer_data_sequence.iloc[[resistance[1]]][predefined_type_of_price]

    new_date = pd.to_datetime(data_sequence.iloc[[0]].index)
    new_entry = pd.Series(support_line.iloc[0], index=new_date, name='Close')
    if intersection is None:
        new_date_2 = pd.to_datetime(data_sequence.iloc[[-1]].index) #+ pd.DateOffset(days=5)
    else:
        new_date_2 = pd.to_datetime(data_sequence.iloc[[intersection]].index)
    new_entry_2 = pd.Series(support_line.iloc[0], index=new_date_2, name='Close')

    support_line = pd.concat([support_line, new_entry, new_entry_2])

    new_entry_3 = pd.Series(data_sequence.iloc[absolute_minimum[1]][predefined_type_of_price], index=data_sequence.iloc[[absolute_minimum[1]]].index, name='Close')
    if intersection is None:
        new_entry_4 = pd.Series(data_sequence.iloc[-1][predefined_type_of_price], index=new_date_2, name='Close')
    else:
        new_entry_4 = pd.Series(data_sequence.iloc[intersection][predefined_type_of_price], index=new_date_2, name='Close')
    diagonal_line = pd.concat([new_entry_3, new_entry_4])

    #Comprobar que se cumple el objetivo del patrón.
    objective = resistance[0] + ((resistance[0] - absolute_minimum[0])*0.70)

    objective_line = pd.Series(objective, index=data_sequence.iloc[[-1]].index, name='Close')
    new_date_3 = pd.to_datetime(data_sequence.iloc[[-1]].index) + pd.DateOffset(days=(int(len(data_sequence)* 1.5)))
    if new_date_3 > longer_data_sequence.iloc[[-1]].index:
        new_date_3 = pd.to_datetime(longer_data_sequence.iloc[[-1]].index)
    objective_line_2 = pd.Series(objective, index=new_date_3, name='Close')
    objective_line = pd.concat([objective_line, objective_line_2])
        
    limit = len(data_sequence) * 2
    if limit > len(longer_data_sequence):
        limit = len(longer_data_sequence)-1
    if any(x >= objective for x in longer_data_sequence.iloc[len(data_sequence):limit][predefined_type_of_price]):
        return [True, longer_data_sequence.iloc[:limit], [support_line, diagonal_line, objective_line]]
    else:
        return [False, longer_data_sequence.iloc[:limit], [support_line, diagonal_line, objective_line]]
