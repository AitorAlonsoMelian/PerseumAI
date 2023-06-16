# Python program to create a table
  
from tkinter import *
FG = '#ffffff'
FONT = 'Raleway'
BUTTON_BG = '#0C60DB'
MAIN_BG = "#20385C"
RED = '#FF0000'
 
class Table:
     
    def __init__(self,root):
         
        # code for creating table
        for i in range(total_rows):
            for j in range(total_columns):
                if j == 0:
                    self.e = Entry(root, width=16, font=FONT, fg=FG, bg=MAIN_BG, highlightthickness=0)
                else:
                    self.e = Entry(root, width=24, font=FONT, fg=FG, bg=MAIN_BG, highlightthickness=0, justify=CENTER)
                 
                self.e.grid(row=i, column=j)
                self.e.insert(END, lst[i][j])
 
# take the data
lst = [('','Recommended window values'),
       ('Double top/bottom','~120'),
       ('Asc/Desc Triangle','~200'),
       ('Head & Shoulders','~120'),]
  
# find total number of rows and
# columns in list
total_rows = len(lst)
total_columns = len(lst[0])
  
# create root window
root = Tk()
t = Table(root)
root.mainloop()