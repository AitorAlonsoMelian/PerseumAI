from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from PIL import Image, ImageTk
from matplotlib.pyplot import text, title
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import os
import csv

FG = '#ffffff'
FONT = 'Raleway'
BUTTON_BG = '#0C60DB'
MAIN_BG = "#20385C"
PATTERNS_FILE_PATH = 'patterns/'
PATTERN_TO_SHOW = 'head_and_shoulders'
TOGGLE_SMA = True
SMA_WINDOW_SIZE = 3

def getData():
    file_list = os.listdir(PATTERNS_FILE_PATH + PATTERN_TO_SHOW)
    results = dict()
    for file in file_list:
        single_file_results = []
        with open(PATTERNS_FILE_PATH + PATTERN_TO_SHOW + '/' + file) as csvfile:
            reader = csv.reader(csvfile)
            next(reader, None)
            for row in reader:
                #print(row)
                single_file_results.append(round(float(row[1]), 3))
        results[file] = single_file_results
    return results

def calculateArraySimpleMovingAverage(array, window_size):
    """Calculate the simple moving average for a given array and window size

        Args:  
            array (List[]): array containing the prices
            window_size (int): size of the window to calculate the moving average  
        Return:  
            array (List[]): array containing the prices and the moving average
    """
    results = []
    for i in range(len(array)):
        if i >= window_size:
            aux = sum(array[i-window_size:i]) / window_size
            results.append(round(aux,4))
    return results


root = Tk()
root.title("See Data")

#Mainframe
main_frame = Frame(root, bg=MAIN_BG)
main_frame.pack(fill=BOTH, expand=1)  

#Canvas
canvas = Canvas(main_frame, bg='grey')
canvas.pack(side=LEFT, fill=BOTH, expand=1)

#Scrollbar
scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
scrollbar.pack(side=RIGHT, fill=Y)

#Configure canvas
canvas.configure(yscrollcommand=scrollbar.set)
canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

#Second frame
second_frame = Frame(canvas, bg=MAIN_BG)

#Add second frame to canvas
canvas.create_window((0,0), window=second_frame, anchor="nw")

data = getData()
#print(data)

#Bucle for para que imprima todos los datos con la média móvil
if (TOGGLE_SMA):
    for element in data.keys():
        print(element)
        print(data[element])
        data[element] = calculateArraySimpleMovingAverage(data[element], SMA_WINDOW_SIZE)
############################################

for file in data.keys():
    figure = Figure(figsize=(15, 5), dpi=100)
    figure.suptitle(file + " - " + str(len(data[file])) + " points")
    ax = figure.add_subplot(111)
    ax.plot(data[file])
    canvas2 = FigureCanvasTkAgg(figure, master=second_frame)
    canvas2.draw()
    canvas2.get_tk_widget().pack(side=TOP, fill=BOTH, expand=True)
#canvas.pack(side=LEFT, expand=True, fill=BOTH)

root.mainloop()

