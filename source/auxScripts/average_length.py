import os
import csv

def calcular_longitud_media(carpeta_madre):
    resultados = {}

    # Obtener la lista de carpetas hijas
    carpetas_hijas = [nombre for nombre in os.listdir(carpeta_madre) if os.path.isdir(os.path.join(carpeta_madre, nombre))]

    # Recorrer cada carpeta hija
    for carpeta_hija in carpetas_hijas:
        ruta_carpeta_hija = os.path.join(carpeta_madre, carpeta_hija)
        longitud_total = 0
        num_archivos = 0

        # Obtener la lista de archivos CSV en la carpeta hija
        archivos_csv = [nombre for nombre in os.listdir(ruta_carpeta_hija) if nombre.endswith('.csv')]

        # Recorrer cada archivo CSV y calcular la longitud
        for archivo_csv in archivos_csv:
            ruta_archivo_csv = os.path.join(ruta_carpeta_hija, archivo_csv)
            with open(ruta_archivo_csv, 'r') as archivo:
                reader = csv.reader(archivo)
                longitud_total += sum(1 for _ in reader)
                num_archivos += 1

        # Calcular la longitud media
        longitud_media = longitud_total / num_archivos if num_archivos > 0 else 0

        # Almacenar el resultado
        resultados[carpeta_hija] = longitud_media

    return resultados

# Ejemplo de uso
carpeta_madre = 'patterns'
resultados = calcular_longitud_media(carpeta_madre)

# Imprimir los resultados
for carpeta_hija, media in resultados.items():
    print(f"{carpeta_hija}: {media}")
