import tkinter as tk # Alias is used as it is more concise
from tkinter import ttk # Improved tkinter module 
import googletrans # Required for translation function


class Program(tk.Tk): # Main program window that instantiates all the child classes and runs the mainloop() of its tk.Tk instance

    def __init__(self, title, size): # Core initialisation parameters
        super().__init__()
        self.title(title)
        self.geometry(f"{size[0]}x{size[1]}")
        
        self.frame = tk.Frame(self, background = "#D3D3D3") # Main frame/background
        self.frame.pack(expand = 1, fill = tk.BOTH)

        # ~~~~~ Different classes for different program elements - classes are instantiated and necessary instances are passed ~~~~~ 

        # File menu class
        self.filemenu = FileMenu(self) 

        # Widget classes
        self.entries = Entries(self) # Deferred initialisation is used to keep the main class's __init__ constructure cleaner
        self.output = Output(self)
        self.buttons = Buttons(self, self.entries, self.output)
        self.radiobuttons = Radiobuttons(self, self.entries)
        
        # ! Circular dependency fix: Call function in one class that passes an instance of the dependency to it
        self.buttons.set_radiobuttons(self.radiobuttons) 

        # Accessibility option classes
        self.fontsize = FontSize(self, self.entries, self.buttons, self.radiobuttons)
        self.highcontrast = HighContrast(self, self.entries, self.output, self.buttons, self.radiobuttons)
        self.translator = Translator(self, self.entries, self.buttons, self.radiobuttons, self.filemenu)

        
class Entries(ttk.Frame):
    
    def __init__(self, master): # Second argument allows the main instance (self) of Program() to be passed to Entries() for inheritance
        super().__init__(master) # Ensures proper inheritane of master class (in this case, Program())
        self.place(x = 210, y = 190, anchor = "center") # Placing window in which this class's widgets will be stored (like a subfolder)

        # Calling widget generator and placer functions
        self.entryGen() 
        self.entryPlacer()

    def entryGen(self): # Create entry widgets and add temporary text

        self.firstTerm = ttk.Entry(self, foreground = "gray") # Make widgets members of the object and not stay in the local scope of the function
        self.commonDifference = ttk.Entry(self, foreground = "gray")
        self.numberOfTerms = ttk.Entry(self, foreground = "gray")

        self.firstTerm.insert(0, "First term of the series") # Entering temporary text
        self.commonDifference.insert(0, "Common difference")
        self.numberOfTerms.insert(0, "Number of terms")

        # Storing data of temporary text and entry variable names in lists so they can be accessed by only 2 functions instead of more (focus in and focus out)
        self.entryTempText = ["First term of the series", "Common difference", "Number of terms"] 
        self.entryVars = [self.firstTerm, self.commonDifference, self.numberOfTerms] 

        for i, var in enumerate(self.entryVars): # Sending entry variables to be bound to events which control the 2 focus functions
            self.bind_events(var, i)

    def bind_events(self, entry, entryPos): # Binds events to entries (controlled by above for loop)
        entry.bind("<FocusIn>", lambda event: self.whenFocused(entry)) 
        entry.bind("<FocusOut>", lambda event: self.whenUnfocused(entry, entryPos))

    def whenFocused(self, entry): # Controls what happens when the user focuses on the entry (above bindings provide the functionality)
        if entry.get() in self.entryTempText:
            entry.delete(0, tk.END)
            entry.insert(0, "")
            entry.config(foreground = "white")

    def whenUnfocused(self, entry, entryPos): # Controls what happens when the user unfocuses from the entry
        if entry.get() == "":
            entry.insert(0, self.entryTempText[entryPos])
            entry.config(foreground = "gray")

    def entryPlacer(self): # Place entry widgets
        self.firstTerm.pack()
        self.commonDifference.pack()
        self.numberOfTerms.pack()

    def seriesEntryConfig(self, seqType): # Switches between temporary text in the second entry field
        if seqType == 1:
            self.commonDifference.delete(0, tk.END)
            self.entryTempText[1] = "Common difference"
            self.commonDifference.config(foreground = "gray")
            self.commonDifference.insert(0, "Common difference")
        
        else:
            self.commonDifference.delete(0, tk.END)
            self.commonDifference.config(foreground = "gray")
            self.entryTempText[1] = "Common ratio"
            self.commonDifference.insert(0, "Common ratio")


class Output(ttk.Frame):

    def __init__(self, master):
        super().__init__(master)
        self.place(x = 255, y = 325, anchor = "center")
        self.outputGen()
        self.outputPlacer()

    def outputGen(self):
        self.sumOutput = tk.Text(self, state = "disabled", height = 10, width = 40) # Doesn't allow input but allows copying of result

    def outputPlacer(self):
        self.sumOutput.pack()
    

class Radiobuttons(ttk.Frame):

    def __init__(self, master, entries):
        super().__init__(master)
        self.place(x = 400, y = 172, anchor = "center")

        self.entries = entries
    
        self.radioButtonGen()
        self.radioButtonPlacer()

    def radioButtonGen(self):
        self.var = tk.IntVar()
        self.arithButton = ttk.Radiobutton(self, text = "Arithmetic Series", variable = self.var, value = 1, command = lambda: self.entries.seriesEntryConfig(1))
        self.geomButton = ttk.Radiobutton(self, text = "Geometric Series", variable = self.var, value = 2, command = lambda: self.entries.seriesEntryConfig(2))
        
    def radioButtonPlacer(self):
        self.arithButton.pack()
        self.geomButton.pack()
    

class Buttons(ttk.Frame):

    def __init__(self, master, entries, output):
        super().__init__(master)
        self.place(x = 337, y = 200)

        self.entries = entries # Saving passed arguments of Entries and Output classes
        self.output = output

        self.buttonGen()
        self.buttonPlacer()
    
    def set_radiobuttons(self, radiobuttons): # Function that was discussed in the Program class to eliminate the circular dependency error
        self.radiobuttons = radiobuttons # Saving instance to be used in the clear() function later on
        
    def buttonGen(self):
        self.clear = ttk.Button(self, text = "Clear", command = self.clear)
        self.calculate = ttk.Button(self, text = "Calculate", command = self.calculate)
    
    def buttonPlacer(self):
        self.clear.pack()
        self.calculate.pack()
    
    def clear(self):
        # List comprehension that clears temporary text in entries only if the user has typed in them (and reinserts temporary text)
        self.entryText = [entry.get() for entry in self.entries.entryVars]

        self.fieldModified = [False if entry == self.entries.entryTempText[i] else True for i, entry in enumerate(self.entryText)]

        '''
        # The following list comprehension utilises short circuit evaluation:
        # "the concept of skipping the evaluation of the second part of a boolean expression in a 
        # conditional statement when the entire statement has already been determined to be either true or false"
        '''
        [self.entries.entryVars[i].delete(0, tk.END) or self.entries.entryVars[i].insert(0, self.entries.entryTempText[i]) or self.entries.entryVars[i].config(foreground="gray") for i, modified in enumerate(self.fieldModified) if modified]

        self.output.sumOutput.config(state = "normal") # Enabling text widget's state to modify text
        self.output.sumOutput.delete(1.0, tk.END)
        self.output.sumOutput.config(state = "disabled") # Disabling state

        self.radiobuttons.var.set(0) # Deselecting radiobuttons 

    def calculate(self):
        self.seqType = self.radiobuttons.var.get()
        try:
            pass # 1 is arithmetic, 2 is geometric
        
        except Exception as ex:
            print(ex)


class FileMenu(tk.Menu): 

    def __init__(self, master):
        super().__init__(master)
    
        self.master = master

        self.createFileMenu()

    def createFileMenu(self):
        # Creating main menu
        self.menu = tk.Menu(self)

        # Creating accessibility options menu
        self.helpMenu = tk.Menu(self.menu)
        self.menu.add_cascade(label = "Accessibility Options", menu = self.helpMenu)

        # Creating options within the accessibility menu
        self.helpMenu.add_command(label = "Toggle high contrast") # Add commands later
        self.helpMenu.add_separator()

        # Creating font size menu and adding 3 presets
        self.sizeMenu = tk.Menu(self.helpMenu) 
        self.helpMenu.add_cascade(label = "Font Size", menu = self.sizeMenu)  # Adding cascade to sizeMenu

        self.sizeMenu.add_command(label = "Large") # Add commands later
        self.sizeMenu.add_command(label = "Medium")
        self.sizeMenu.add_command(label = "Small")

        # Creating languages menu and adding 5 languages
        self.langMenu = tk.Menu(self.helpMenu)
        self.helpMenu.add_cascade(label = "Languages", menu = self.langMenu)
        # Commands added in Translator class for better organisation

        # Setting main menu
        self.master.config(menu = self.menu)


class FontSize(ttk.Frame):
    
    def __init__(self, master, entries, buttons, radiobuttons):
        super().__init__(master)
    
        self.master = master

        self.entries = entries
        self.buttons = buttons
        self.radiobuttons = radiobuttons


class HighContrast(ttk.Frame):
    
    def __init__(self, master, entries, output, buttons, radiobuttons):
        super().__init__(master)

        self.master = master

        self.entries = entries
        self.output = output
        self.buttons = buttons
        self.radiobuttons = radiobuttons


class Translator(ttk.Frame): 

    def __init__(self, master, entries, buttons, radiobuttons, filemenu):
        super().__init__(master)

        self.master = master

        self.entries = entries
        self.buttons = buttons
        self.radiobuttons = radiobuttons
        self.filemenu = filemenu

        self.languageDbMaker()
    
    def languageDbMaker(self):
        self.languageDb = googletrans.LANGUAGES
        self.sortedLanguageDb = {key: value for key, value in sorted(self.languageDb.items())} # Sorting languages alphabetically
        for name, acronym in self.sortedLanguageDb.items():
            # Capture current value of value and assigns it to the lang parameter of the translator function 
            self.filemenu.langMenu.add_command(label = acronym, command = lambda lang = name: self.translatorFunc(lang))
        
    def translatorFunc(self, lang):
        print(lang) # Placeholder 


def startProgram(): # Start program function
    program = Program("Calculator", (600, 600)) # Passing title and dimensions in tuple 
    program.mainloop() # Executing .mainloop() in the program object 

if __name__ == "__main__": # Allows program to only run when the file is executed as a script, allowing for modularity and reusability
    startProgram()