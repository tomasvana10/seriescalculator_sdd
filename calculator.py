import tkinter as tk # Alias is used as it is more concise
from tkinter import ttk # Improved tkinter module 


class Program(tk.Tk): # Main program window that instantiates all the child classes and runs the mainloop() of its tk.Tk instance

    def __init__(self, title, size): # Core initialisation parameters
        super().__init__()
        self.title(title)
        self.geometry(f"{size[0]}x{size[1]}")
        
        self.frame = tk.Frame(self, background = "#D3D3D3") # Main frame/background
        self.frame.pack(expand = 1, fill = tk.BOTH)

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

        self.firstTerm.bind("<FocusIn>", lambda event: self.whenFocused(0)) 
        self.commonDifference.bind("<FocusIn>", lambda event: self.whenFocused(1))
        self.numberOfTerms.bind("<FocusIn>", lambda event: self.whenFocused(2))

        self.firstTerm.bind("<FocusOut>", lambda event: self.whenUnfocused(0))
        self.commonDifference.bind("<FocusOut>", lambda event: self.whenUnfocused(1))
        self.numberOfTerms.bind("<FocusOut>", lambda event: self.whenUnfocused(2))

    def whenFocused(self, entryPos): # Controls what happens when the user focuses on the entry (above bindings provide the functionality)
        if self.entryVars[entryPos].get() in self.entryTempText:
            self.entryVars[entryPos].delete(0, tk.END)
            self.entryVars[entryPos].insert(0, "")
            self.entryVars[entryPos].config(foreground = "white")

    def whenUnfocused(self, entryPos): # Controls what happens when the user unfocuses from the entry
        if self.entryVars[entryPos].get() == "":
            self.entryVars[entryPos].insert(0, self.entryTempText[entryPos])
            self.entryVars[entryPos].config(foreground = "gray")
  
    def entryPlacer(self): # Place entry widgets
        self.firstTerm.pack()
        self.commonDifference.pack()
        self.numberOfTerms.pack()


class Output(ttk.Frame):

    def __init__(self, parent):
        super().__init__(parent)
        self.place(x = 255, y = 325, anchor = "center")
        self.outputGen()
        self.outputPlacer()

    def outputGen(self):
        self.sumOutput = tk.Text(self, state = "disabled", height = 10, width = 40) # Doesn't allow input but allows copying of result

    def outputPlacer(self):
        self.sumOutput.pack()
    

class Radiobuttons(ttk.Frame):

    def __init__(self, parent, buttons):
        super().__init__(parent)
        self.place(x = 400, y = 172, anchor = "center")

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
        self.place(x = 337, y = 200)

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
        i = 0
        self.entryText = []
        for x in self.entries.entryVars:
            self.entryText.append(self.entries.entryVars[i].get())
            i += 1

        i = 0
        self.fieldModified = []
        for x in self.entryText:
            if self.entryText[i] == self.entries.entryTempText[i]:
                self.fieldModified.append(False)
            else:
                self.fieldModified.append(True)
            i += 1
        
        i = 0
        for x in self.fieldModified:
            if self.fieldModified[i] == True:
                self.entries.entryVars[i].delete(0, tk.END)
                self.entries.entryVars[i].insert(0, self.entries.entryTempText[i])
                self.entries.entryVars[i].config(foreground = "gray")
            else:
                pass
            i += 1

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