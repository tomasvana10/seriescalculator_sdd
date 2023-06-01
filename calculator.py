import tkinter as tk # Alias is used as it is more concise
from tkinter import ttk # Improved tkinter module 


class Program(tk.Tk): # Main program window that instantiates all the child classes and runs the mainloop() of its tk.Tk instance

    def __init__(self, title, size): # Core initialisation parameters
        super().__init__()
        self.title(title)
        self.geometry(f"{size[0]}x{size[1]}")
    
        # Program elements split into widget type (different classes)
        self.entries = Entries(self) # Deferred initialisation is used to keep the main class's __init__ constructure cleaner
        self.output = Output(self)
        self.buttons = Buttons(self, self.entries, self.output)
        self.radiobuttons = Radiobuttons(self, self.buttons)
    
        self.filemenu = FileMenu(self) # Initialising file menu

        # Run program
        self.mainloop()


class Entries(ttk.Frame):
    
    def __init__(self, parent): # Second argument allows the main instance (self) of Program() to be passed to Entries() for inheritance
        super().__init__(parent) # Ensures proper inheritane of parent class (in this case, Program())
        self.place(x = 0, y = 0) # Placing window in which this class's widgets will be stored (like a subfolder)

        # Calling widget generator and placer functions
        self.entryGen() 
        self.entryPlacer()
    
    def entryGen(self): # Create entry widgets and add temporary text
        self.firstTerm = ttk.Entry(self) # Make widgets members of the object and not stay in the local scope of the function
        self.commonDifference = ttk.Entry(self)
        self.numberOfTerms = ttk.Entry(self)

        self.firstTerm.insert(0, "First term of the series") # Entering temporary text
        self.commonDifference.insert(0, "Common difference")
        self.numberOfTerms.insert(0, "Number of terms")

        self.firstTerm.bind("<FocusIn>", lambda event: self.clearTemp(1)) 
        self.commonDifference.bind("<FocusIn>", lambda event: self.clearTemp(2))
        self.numberOfTerms.bind("<FocusIn>", lambda event: self.clearTemp(3))
    
    def clearTemp(self, entryNum): # Clear temporary text when entry is focused (above bindings provide the functionality)
        if entryNum == 1:
            self.firstTerm.delete(0, tk.END)
        elif entryNum == 2:
            self.commonDifference.delete(0, tk.END)
        else:
            self.numberOfTerms.delete(0, tk.END)
    
    def entryPlacer(self): # Place entry widgets
        self.firstTerm.pack()
        self.commonDifference.pack()
        self.numberOfTerms.pack()


class Output(ttk.Frame):

    def __init__(self, parent):
        super().__init__(parent)
        self.place(x = 0, y = 70) # Must place accurately later !!!

        self.outputGen()
        self.outputPlacer()

    def outputGen(self):
        self.sumOutput = tk.Text(self, state = "disabled") # Doesn't allow input but allows copying of result

    def outputPlacer(self):
        self.sumOutput.pack()
    

class Radiobuttons(ttk.Frame):

    def __init__(self, parent, buttons):
        super().__init__(parent)
        self.place(x = 0, y = 0)

        self.buttons = buttons # Saving passed argument of buttons class (so Radiobuttons can communicate with buttons)

        self.radioButtonGen()
        self.radioButtonPlacer()

    def radioButtonGen(self):
        self.var = tk.IntVar()
        self.arithButton = ttk.Radiobutton(self, text = "Arithmetic Series", variable = self.var, value = 1, command = lambda: self.buttons.seqChoice("arithmetic"))
        self.geomButton = ttk.Radiobutton(self, text = "Geometric Series", variable = self.var, value = 2, command = lambda: self.buttons.seqChoice("geometric"))

    def radioButtonPlacer(self):
        self.arithButton.pack()
        self.geomButton.pack()
    

class Buttons(ttk.Frame):

    def __init__(self, parent, entries, output):
        super().__init__(parent)
        self.place(x = 0, y = 0)

        self.entries = entries # Saving passed arguments of Entries and Output classes
        self.output = output

        self.seqType = "" # Creating variable to assign the sequence type to later on

        self.buttonGen()
        self.buttonPlacer()
        
    def buttonGen(self):
        self.clear = ttk.Button(self, text = "Clear", command = self.clear)
        self.calculate = ttk.Button(self, text = "Calculate", command = self.calculate)
    
    def buttonPlacer(self):
        self.clear.pack()
        self.calculate.pack()
    
    def clear(self):
        self.entries.firstTerm.delete(0, tk.END) # Clearing entry fields
        self.entries.commonDifference.delete(0, tk.END)
        self.entries.numberOfTerms.delete(0, tk.END)

        self.output.sumOutput.config(state = "normal") # Enabling text widget's state to modify text
        self.output.sumOutput.delete(1.0, tk.END)
        self.output.sumOutput.config(state = "disabled") # Disabling state
    
    def seqChoice(self, seqType):
        if seqType == "arithmetic":
            self.seqType = "arithmetic"
        else:
            self.seqType = "geometric"

    def calculate(self):
        try:
            pass # Calculation algorithm goes here
        
        except Exception as ex:
            print(ex)


class FileMenu(tk.Menu):

    def __init__(self, parent):
        super().__init__(parent)
    
        self.parent = parent

        self.createFileMenu()
    
    def createFileMenu(self):
        # Creating main menu
        self.menu = tk.Menu(self)

        # Creating accessibility options menu
        self.helpMenu = tk.Menu(self.menu)
        self.menu.add_cascade(label="Accessibility Options", menu=self.helpMenu)

        # Creating options within the accessibility menu
        self.helpMenu.add_command(label="Toggle high contrast") # Add commands later
        self.helpMenu.add_separator()

        # Creating font size menu and adding 3 presets
        self.sizeMenu = tk.Menu(self.helpMenu) 
        self.helpMenu.add_cascade(label="Font Size", menu=self.sizeMenu)  # Adding cascade to sizeMenu

        self.sizeMenu.add_command(label="Large") # Add commands later
        self.sizeMenu.add_command(label="Medium")
        self.sizeMenu.add_command(label="Small")

        self.parent.config(menu = self.menu)


# Instantiating the Program() class
Program("Calculator", (600, 600))