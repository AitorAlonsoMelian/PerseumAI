#!/usr/bin/env python3
#sudo apt-get install python3-tk
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from PIL import Image, ImageTk
from matplotlib.pyplot import text, title
from matplotlib.figure import Figure
import pattern_utils
import main as mn
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import re

"""Code for GUI of Perseum AI"""

FG = '#ffffff'
FONT = 'Raleway'
BUTTON_BG = '#0C60DB'
MAIN_BG = "#20385C"

class LandingWindow:
    """Landing window where the program starts"""
    def __init__(self, master):
        """Definition of constructor for landing page"""
        self.master = master
        self.master.geometry('800x600')
        self.master.configure(bg="#20385C")
        self.master.title('PerseumAI')
        self.frame = Frame(self.master, width=500, height=300, bg=MAIN_BG)
        self.image = Image.open('./resources/images/PerseumAI.PNG')
        self.logo = ImageTk.PhotoImage(self.image)
        self.logo_label = Label(self.frame, image=self.logo)
        self.button1 = Button(self.frame, text = 'Click here to start', command = self.nextWindow, font=FONT, bg=BUTTON_BG, fg='white', height=2, width=15, pady=5, activebackground="#69AAF5")
        
        self.frame.pack()
        self.frame.place(anchor='center', relx=0.5, rely=0.5)
        self.logo_label.pack()
        self.button1.pack(pady=10)

    def nextWindow(self):
        """Method for advancing to next window"""
        self.frame.destroy()
        self.app = MenuWindow(self.master)

class MenuWindow:
    """Menu window where the user specifies the parameters for the program"""
    def __init__(self, master):
        self.master = master
        self.companies = None
        pattern_types = ['Double top', 'Double bottom']
        self.selected_types = []

        self.frame = Frame(self.master, height=2000, width=500, bg=MAIN_BG)
        self.patterns_type = Label(self.frame, text='Choose which patterns to find', font=(FONT, 18), fg=FG, bg=MAIN_BG, highlightthickness=0)
        self.types_frame = Frame(self.frame, height=200, bg=MAIN_BG)
        for type in pattern_types:
            value = BooleanVar(self.types_frame)
            pattern_type_dict = {
                'type': type,
                'value': value,
                'button': Checkbutton(self.types_frame, text=type, height=1, width=12, variable=value, font=FONT, bg="#69AAF5", activebackground="#69AAF5", highlightthickness=0, fg=MAIN_BG) #, font=FONT, variable=value, bg=MAIN_BG, fg=FG, activebackground="#69AAF5", highlightthickness=0
            }
            pattern_type_dict['button'].pack(side=LEFT, pady=15)
            self.selected_types.append(pattern_type_dict)
        self.empty_label = Label(self.frame, text='\n')
        self.year_label = Label(self.frame, text='Year to start counting from', font=FONT, bg=MAIN_BG, fg=FG)
        self.year_entry = Entry(self.frame)
        self.open_file_button = Button(self.frame, text = 'Open file', width = 25, command = self.openTxt, font=FONT, fg=FG, bg=BUTTON_BG, activebackground="#69AAF5")
        self.warning_file_label = Label(self.frame, text='', font=FONT, bg=MAIN_BG, fg=FG)
        self.intensive_search_frame = Frame(self.frame, bg=MAIN_BG)
        self.intensive_search_value = BooleanVar(self.intensive_search_frame)
        self.intensive_search_check = Checkbutton(self.intensive_search_frame, text='Intensive search mode', height=1, width=18, variable=self.intensive_search_value, font=FONT, bg="#69AAF5", activebackground="#69AAF5", highlightthickness=0, fg=MAIN_BG) 
        self.run_button = Button(self.frame, text = 'Run', width = 25, command = self.runProgram, font=FONT, fg=FG, bg=BUTTON_BG, activebackground="#69AAF5")
        self.quit_button = Button(self.frame, text = 'Quit', width = 25, command = self.closeWindow, font=FONT, fg=FG, bg=BUTTON_BG, activebackground="#69AAF5")
       
        self.patterns_type.pack()
        self.year_label.pack()
        self.types_frame.pack()
        self.year_entry.pack(pady=5)
        self.open_file_button.pack(pady=5)
        self.warning_file_label.pack()
        self.intensive_search_frame.pack()
        self.intensive_search_check.pack()
        self.run_button.pack(pady=(100,5))
        self.quit_button.pack()

        self.frame.pack(fill=BOTH, expand=True)
        self.frame.place(relx=.5, rely=.5, anchor='c')

    def runProgram(self):
        """Execute the back-end program with the parametes given by the user"""
        if self.companies == None:
            self.warning_file_label.configure(text='Please select a file')
            return
        if not self.year_entry.get():
            return
        selected_types_set = set()
        for pattern_type in self.selected_types:
            if (pattern_type['value'].get()):
                if pattern_type['type'] == 'Double top':
                    selected_types_set.add('double_top')
                elif pattern_type['type'] == 'Double bottom':
                    selected_types_set.add('double_bottom')
        patterns_dictionary = pattern_utils.loadPatterns(15, selected_types_set)
        historic_results = []
        current_results = []
        if not re.search("^\d{4}$", self.year_entry.get()):
            raise Exception('Enter a valid year format %dddd')
        for company in self.companies:
            historic_results = historic_results + mn.trainHistoricDatabase(company, self.year_entry.get(), patterns_dictionary)
            current_results = current_results + mn.findCurrentPatterns(company, patterns_dictionary, self.intensive_search_value.get())
        tendency_results = pattern_utils.calculateTendencyProbability(historic_results, selected_types_set)
        self.results_window = Toplevel(self.master)
        self.app = ResultsWindow(self.results_window, historic_results, current_results, tendency_results)

    def closeWindow(self):
        """End the program by closing the window"""
        self.master.destroy()

    def openTxt(self):
        """Read the txt file chose by the user"""
        text_file = filedialog.askopenfile(initialdir='./', title="Open Text File", filetypes=(("Text Files", "*.txt"), ))
        if text_file != None:
            text_file = open(text_file.name, 'r')
            input_text = text_file.read()
            self.companies = self.parseTxt(input_text)
            text_file.close()
    
    def parseTxt(self, text):
        """Parse a given txt file"""
        text = text.split()
        result_companies = []
        for word in text:
            if re.search(",$", word):
                result_companies.append(word[:-1])
            else:
                result_companies.append(word)
        return result_companies           

class ResultsWindow:
    """Window where the user can see the tendency results and choose to see historic patterns or current patterns"""
    def __init__(self, master, historic_patterns, current_patterns, tendency_results):
        self.historic_patterns = historic_patterns
        self.current_patterns = current_patterns
        self.tendency_results = tendency_results
        self.master = master
        self.master.geometry('1000x800')
        self.master.configure(bg=MAIN_BG)
        self.frame = Frame(self.master, bg=MAIN_BG)
        temp_text = ''
        for key, value in tendency_results.items():
            if isinstance(value, float):
                value = str(round(value)) + '%'
            if key == 'double_top':
                temp_text += f'Double top: {value}\n'
            elif key == 'double_bottom':
                temp_text += f'Double bottom: {value}\n'
            elif key == 'triple_top':
                temp_text += f'Triple top: {value}\n' 

        self.title_text = Label(self.frame, text='Achieve objective probability', font=(FONT,18), fg=FG, bg=MAIN_BG, highlightthickness=0)
        self.tendency_results_text = Label(self.frame, text=temp_text, font=FONT, fg=FG, bg=MAIN_BG, highlightthickness=0) #Añadir otra label comno esta para el titulo
        self.buttons_frame = Frame(self.frame, highlightthickness=0, bg=MAIN_BG)
        self.show_historic = Button(self.buttons_frame, text = 'Show historic patterns', command = self.showHistoricPatterns, font=(FONT,16), bg=BUTTON_BG, activebackground="#69AAF5", fg='white', height=3, width=20)
        self.show_current = Button(self.buttons_frame, text = 'Show current patterns', command = self.showCurrentPatterns, font=(FONT,16), bg=BUTTON_BG, activebackground="#69AAF5",  fg='white', height=3, width=20)
        self.quit_button = Button(self.frame, text = 'Quit', width = 25, command = self.closeWindow, font=FONT, fg=FG, bg=BUTTON_BG, activebackground="#69AAF5")
        
        self.title_text.pack(pady=(0,10))
        self.tendency_results_text.pack(pady=(0,125))
        self.buttons_frame.pack()
        self.show_current.pack(side=RIGHT, padx=(125, 40), anchor='w')
        self.show_historic.pack(side=LEFT, padx=(40, 125), anchor='e')
        self.quit_button.pack(side=BOTTOM, anchor='s', pady=(200, 0))
        self.frame.pack(fill=BOTH, expand=True)
        self.frame.place(relx=.5, rely=.5, anchor='c')

    def closeWindow(self):
        """Destroy the window"""
        self.master.destroy()

    def showHistoricPatterns(self):
        """Show the historic patterns that were found"""
        self.frame.destroy()
        self.app = ShowPatternsWindow(self.master, [self.historic_patterns, self.current_patterns, self.tendency_results], 0)
    
    def showCurrentPatterns(self):
        """Show the current patterns that were found"""
        self.frame.destroy()
        self.app = ShowPatternsWindow(self.master, [self.historic_patterns, self.current_patterns, self.tendency_results], 1)

class ShowPatternsWindow:
    def __init__(self, master, results, mode):
        self.results = results
        self.master = master
        self.master.configure(bg=MAIN_BG)
        self.frame = Frame(self.master, bg=MAIN_BG)
        self.canvas = Canvas(self.frame, bg=MAIN_BG)
        self.scroll_bar = ttk.Scrollbar(self.frame, orient=VERTICAL, command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scroll_bar.set)
        self.canvas.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.second_frame = Frame(self.canvas, bg=MAIN_BG)
        self.canvas.create_window((0,0), window=self.second_frame, anchor="nw")
        self.go_back_frame = Frame(self.canvas, bg=MAIN_BG)
        self.go_back = Button(self.go_back_frame, text = 'Return', command = self.goBack, font=FONT, bg=BUTTON_BG, fg='white', height=1, width=20)
        
        self.frame.pack(fill=BOTH, expand=1)
        self.canvas.pack(side=LEFT, fill=BOTH, expand=1)
        self.scroll_bar.pack(side=RIGHT, fill=Y)
        self.go_back_frame.pack(side=BOTTOM, fill=X)
        self.go_back.pack(anchor='w', padx=5, pady=5)
        if mode == 0:
            self.showPatterns(results[0])
        elif mode == 1:
            self.showPatterns(results[1])
            

    def goBack(self):
        """Go back to ResultsWindow"""
        self.frame.destroy()
        self.app = ResultsWindow(self.master, self.results[0], self.results[1], self.results[2])

    def showPatterns(self, results):
        """Show patterns given as a list"""
        for pattern in results:
            temp_frame = Frame(self.second_frame, bg=MAIN_BG)
            fig = Figure(figsize = (9,5), dpi = 100)
            plot1 = fig.add_subplot(111)
            plot1.plot(pattern.dataframe_segment)
            fig.suptitle(f'{pattern.company_name} {pattern.pattern_type} {pattern.starting_date[:10]} - {pattern.ending_date[:10]}')
            canvas = FigureCanvasTkAgg(fig, master=temp_frame)
            canvas.draw()
            temp_frame.pack()
            canvas.get_tk_widget().pack(side=LEFT, pady=10)
            if pattern.tendency is True:
                pattern_tendency_text = Text(temp_frame, height=1, width=2, bg="#40BD2E")
                tendency = '✅'
            elif pattern.tendency is False:
                pattern_tendency_text = Text(temp_frame, height=1, width=2, bg="red")
                tendency = '❌'
            else:
                continue
            pattern_tendency_text.insert(INSERT, tendency)
            pattern_tendency_text.pack(side=RIGHT, padx=20)

            # toolbar = NavigationToolbar2Tk(canvas, self.second_frame)
            # toolbar.update()
            # canvas.get_tk_widget().pack()

def main():
    """Main function for GUI app"""
    try:
        root = Tk()
        app = LandingWindow(root)
        root.mainloop()
    except Exception as err:
        print(err)


if __name__ == '__main__':
    main()
