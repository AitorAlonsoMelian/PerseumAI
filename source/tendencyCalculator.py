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
    for i in range(len(data_sequence) - 1): #Buscar los dos techos
        day_value = data_sequence.iloc[i][predefined_type_of_price]
        if i > 0:
            previous_day_value = data_sequence.iloc[i - 1][predefined_type_of_price]
        if i < len(data_sequence) - 1:
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
    while i < len(data_sequence) and not breaks_resistance_from_right[0]:
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
            if i >= len(longer_data_sequence):
                break
            current_value = longer_data_sequence.iloc[i][predefined_type_of_price]
            if current_value > resistance[0]:
                return [False, longer_data_sequence.iloc[:i + 1], longer_data_sequence.iloc[[first_top[1],second_top[1]]][predefined_type_of_price]]
            if current_value < objective:
                return [True, longer_data_sequence.iloc[:i + 1], longer_data_sequence.iloc[[first_top[1],second_top[1]]][predefined_type_of_price]]
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
    for i in range(len(data_sequence) - 1): #Buscar los dos suelos
        day_value = data_sequence.iloc[i][predefined_type_of_price]
        if i > 0:
            previous_day_value = data_sequence.iloc[i - 1][predefined_type_of_price]
        if i < len(data_sequence) - 1:
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
    while i < len(data_sequence) and not breaks_resistance_from_right[0]:
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
            if i >= len(longer_data_sequence):
                break
            current_value = longer_data_sequence.iloc[i][predefined_type_of_price]
            if current_value < resistance[0]:
                return [False, longer_data_sequence.iloc[:i + 1], longer_data_sequence.iloc[[first_bottom[1],second_bottom[1]]][predefined_type_of_price]]
            if current_value > objective:
                return [True, longer_data_sequence.iloc[:i + 1], longer_data_sequence.iloc[[first_bottom[1],second_bottom[1]]][predefined_type_of_price]]
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
    #aux = 0
    #print(data_sequence)
    for i in range(len(data_sequence) - 1): #Buscar 3 tops
        day_value = data_sequence.iloc[i][predefined_type_of_price]
        if i > 1:
            previous_previous_day_value = data_sequence.iloc[i - 2][predefined_type_of_price]
            previous_day_value = data_sequence.iloc[i - 1][predefined_type_of_price]
        if i < len(data_sequence) - 2:
            #print("HELLO " + str(aux) + " i: " + str(i) + " size: " + str(len(data_sequence) - 1))
            #aux+=1
            next_day_value = data_sequence.iloc[i + 1][predefined_type_of_price]
            next_next_day_value = data_sequence.iloc[i + 2][predefined_type_of_price]
            #print(next_day_value)
        if i > 1 and previous_day_value < day_value and day_value > next_day_value and day_value > previous_previous_day_value and day_value > next_next_day_value: #hemos encontrado un maximo
            relative_maximum = day_value
            if relative_maximum > first_top[0]: # [1] para acceder a lo que no es timestamps y Close porque es la etiqueta del valor
                third_top = second_top
                second_top = first_top
                first_top = [relative_maximum, i]
            elif relative_maximum > second_top[0] and i not in range(first_top[1] - 5, first_top[1] + 5):
                third_top = second_top
                second_top = [relative_maximum, i]
            elif relative_maximum > third_top[0] and i not in range(first_top[1] - 5, first_top[1] + 5):
                third_top = [relative_maximum, i]


    if first_top[1] == None or second_top[1] == None or third_top[1] == None:
        print("1")
        return None #No se encontró alguno de los 3 techos
    if first_top[1] > second_top[1] and first_top[1] > third_top[1]:
        print("2")
        return None # La cabeza no está en medio
    if first_top[1] < second_top[1] and first_top[1] < third_top[1]:
        print("3")
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

    # Se comprueba que los picos están a alturas similares
    first_top_to_support_distance = first_top[0] - support[0]
    second_top_to_support_distance = second_top[0] - support[0]
    third_top_to_support_distance = third_top[0] - support[0]
    if third_top_to_support_distance > second_top_to_support_distance and second_top_to_support_distance < third_top_to_support_distance * 2 / 3:
        print("4")
        return None
    if second_top_to_support_distance > third_top_to_support_distance and third_top_to_support_distance < second_top_to_support_distance * 2 / 3:
        print("5")
        return None
    if first_top_to_support_distance * 0.85 < second_top_to_support_distance or first_top_to_support_distance * 0.85 < third_top_to_support_distance:
        print("5.5")
        return None
    
    # Comprobar la altura entre los suelos y la cabeza
    if not (second_top_support[0]/third_top_support[0] < 1.05 and second_top_support[0]/third_top_support[0] > 0.95):
        print("9")
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
        print("6")
        return None # Pattern\'s support not broken
    #Una vez rompe el patron, debemos averiguar en que direccion

    pattern_width = breaks_support_from_right[1] - breaks_support_from_left[1]
    if pattern_width < 12:
        print("7")
        return None # Patrón demasiado pequeño

    average_height = abs(((first_top[0] + second_top[0]) / 2) - support[0])
    objective = support[0] - average_height
    if pattern_width:
        for i in range(breaks_support_from_right[1], breaks_support_from_right[1] + pattern_width):
            if i >= len(longer_data_sequence):
                break
            current_value = longer_data_sequence.iloc[i][predefined_type_of_price]
            if current_value > support[0]:
                return [False, longer_data_sequence.iloc[:i + 1], longer_data_sequence.iloc[[second_top[1],first_top[1],third_top[1]]][predefined_type_of_price]]
                #return [False, longer_data_sequence.iloc[first_top[1]-30:first_top[1]+30], longer_data_sequence.iloc[[second_top[1],first_top[1],third_top[1]]][predefined_type_of_price]]
            if current_value < objective:
                return [True, longer_data_sequence.iloc[:i + 1], longer_data_sequence.iloc[[second_top[1],first_top[1],third_top[1]]][predefined_type_of_price]]
                #return [True, longer_data_sequence.iloc[first_top[1]-30:first_top[1]+30], longer_data_sequence.iloc[[second_top[1],first_top[1],third_top[1]]][predefined_type_of_price]]
    else:
        print("8")
        return None
    

    