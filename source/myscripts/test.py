import tkinter as tk
import tkinter.filedialog
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os

def plot_data(df):
    fig, ax = plt.subplots()
    ax.plot(df['Close'])
    return fig

root = tk.Tk()
root.title("Multi-file CSV Plotter")

canvas = tk.Canvas(root, bg="white", scrollregion=(0, 0, 1000, 1000))
vbar = tk.Scrollbar(root, orient=tk.VERTICAL)
vbar.pack(side=tk.RIGHT, fill=tk.Y)
vbar.config(command=canvas.yview)
canvas.config(width=400, height=400)
canvas.config(yscrollcommand=vbar.set)
canvas.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

# Prompt the user to select multiple CSV files
#filenames = tkinter.filedialog.askopenfilenames(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
file_list = os.listdir('patterns/double_bottom')


# Read each file and plot the data
for filename in file_list:
    df = pd.read_csv('patterns/double_bottom/' + filename)
    print(df)
    fig = plot_data(df)

    # Convert the matplotlib figure to a tkinter canvas and add it to the scrollable canvas
    canvas_figure = FigureCanvasTkAgg(fig, canvas)
    canvas_figure.draw()
    canvas.create_window((0, 0), window=canvas_figure.get_tk_widget(), anchor=tk.NW)

root.mainloop()
