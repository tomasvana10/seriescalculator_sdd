import tkinter as tk # Alias is used as it is more concise
from tkinter import ttk # Improved tkinter module 
import googletrans # Required for translation database
from googletrans import Translator # Required for translator instance


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

        # ! Circular dependency fixes: Call function in one class that passes an instance of the dependency to it
        self.buttons.setRadiobuttons(self.radiobuttons) 
        self.entries.setRadiobuttons(self.radiobuttons)

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

        self.seqElement = 0 # Allows element 0 of commonDifference temp text to be accessed (default)

    def setRadiobuttons(self, radiobuttons): # Function that was discussed in the Program class to eliminate the circular dependency error
        self.radiobuttons = radiobuttons # Saving instance to be used in the clear() function later on

    def entryGen(self): 
        self.firstTerm = ttk.Entry(self, foreground = "gray") 
        self.commonDifference = ttk.Entry(self, foreground = "gray")
        self.numberOfTerms = ttk.Entry(self, foreground = "gray")
        
        self.tempTextDb = { # Storing relation between entry variables and their text
            self.firstTerm : ["First term"],
            self.commonDifference : ["Common difference", "Common ratio"],
            self.numberOfTerms : ["Number of terms"]
        }

        self.engTempTextDb = self.tempTextDb.copy() # Used when setting language back to English (faster)

        for entry in self.tempTextDb: 
            entry.insert(0, self.tempTextDb[entry][0]) 
            self.bindEvents(entry)  

    def bindEvents(self, entry): # Binds focus in and focus out events to their respective functions
        entry.bind("<FocusIn>", lambda event: self.whenFocused(entry))
        entry.bind("<FocusOut>", lambda event: self.whenUnfocused(entry))
        entry.bind("<Key>", lambda event: self.whenKeyPressed(entry))
    
    def whenFocused(self, entry):
        if entry.get() in self.tempTextDb[entry]:
            entry.config(foreground = "white")
            entry.icursor(tk.END)

    def whenUnfocused(self, entry):
        if entry.get() == "":
            if entry == self.commonDifference:
                entry.insert(0, "".join(self.tempTextDb[entry][self.seqElement])) # Access seqElement (int) of value of self.commonDifference
            else:
                entry.insert(0, "".join(self.tempTextDb[entry][0])) 
            entry.config(foreground = "gray")
        else:
            if entry.get() in self.tempTextDb[entry]:
                entry.config(foreground = "gray")

    def whenKeyPressed(self, entry):
        if entry.get() in self.tempTextDb[entry]:
            entry.delete(0, tk.END)

    def updateTempText(self, radioButtonVar = "arith", fullReload = False): # Using keyword arguments
        if radioButtonVar == "arith": 
            self.seqElement = 0 
        elif radioButtonVar == "geom":
            self.seqElement = 1 # If radioButtonVar is "geom", seqElement becomes one which refers to the second element in the temp text values list for the commonDifference entry
        else:
            pass # For reset via Translator class

        if fullReload: # Useful with clear button
            for key in self.tempTextDb:
                key.delete(0, tk.END)
                if key == self.commonDifference:
                    key.insert(0, "".join(self.tempTextDb[key][self.seqElement]))
                else:
                    key.insert(0, "".join(self.tempTextDb[key]))
                key.config(foreground = "gray")
        
        else: # This only updates the commonDifference entry
            self.commonDifference.delete(0, tk.END)
            self.commonDifference.insert(0, self.tempTextDb[self.commonDifference][self.seqElement])
            self.commonDifference.config(foreground = "gray")
        
    def entryPlacer(self): # Place entry widgets
        self.firstTerm.pack()
        self.commonDifference.pack()
        self.numberOfTerms.pack()


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
    
    def insertText(self, sum):
        self.sumOutput.config(state = "normal")
        self.sumOutput.delete(1.0, tk.END)
        self.sumOutput.insert(1.0, sum)
        self.sumOutput.config(state = "disabled")
    

class Radiobuttons(ttk.Frame):

    def __init__(self, master, entries):
        super().__init__(master)
        self.place(x = 400, y = 172, anchor = "center")

        self.entries = entries

        self.radioButtonGen()
        self.radioButtonPlacer()

    def radioButtonGen(self):
        self.var = tk.IntVar()
        self.arithButton = ttk.Radiobutton(self, text = "Arithmetic Series", variable = self.var, value = 1, command = lambda: self.entries.updateTempText(radioButtonVar = "arith"))
        self.geomButton = ttk.Radiobutton(self, text = "Geometric Series", variable = self.var, value = 2, command = lambda: self.entries.updateTempText(radioButtonVar = "geom"))
        self.var.set(1)
        
    def radioButtonPlacer(self):
        self.arithButton.pack()
        self.geomButton.pack()
    

class Buttons(ttk.Frame):

    def __init__(self, master, entries, output):
        super().__init__(master)
        self.place(x = 337, y = 200)

        self.entries = entries # Saving passed arguments of Entries and Output classes
        self.output = output

        self.errorDb = {
            "ValueError" : "Description",
            "AttributeError" : "Description"
        }
    
        self.buttonGen()
        self.buttonPlacer()
    
    def setRadiobuttons(self, radiobuttons): 
        self.radiobuttons = radiobuttons 
        
    def buttonGen(self):
        self.clear = ttk.Button(self, text = "Clear", command = self.clear)
        self.calculate = ttk.Button(self, text = "Calculate", command = self.calculate)
    
    def buttonPlacer(self):
        self.clear.pack()
        self.calculate.pack()
    
    def clear(self):
        self.entries.updateTempText(fullReload = True)
        self.radiobuttons.var.set(1)

    def calculate(self):
        self.seqType = self.radiobuttons.var.get()
        try:
            self.firstTerm = float(self.entries.firstTerm.get())
            self.commonDiffOrRatio = float(self.entries.commonDifference.get())
            self.numberOfTerms = int(self.entries.numberOfTerms.get())

            if self.seqType == 1: # Arithmetic series
                if self.numberOfTerms <= 0: # Common difference must be greater than 0
                    self.output.insertText("The length of the series cannot be a negative number or 0, please choose an appropriate length.")

                else:
                    self.sum = (self.numberOfTerms / 2) * (2 * self.firstTerm + (self.numberOfTerms - 1) * self.commonDiffOrRatio)
                    self.output.insertText(self.sum)
                
            elif self.seqType == 2: # Geometric Series
                if self.commonDiffOrRatio == 1:
                    self.sum = self.firstTerm * self.numberOfTerms
                
                else:
                    self.sum = self.firstTerm * (1 - self.commonDiffOrRatio ** self.numberOfTerms) / (1 - self.commonDiffOrRatio)

                self.output.insertText(self.sum)
        
        except Exception as ex:
            if type(ex).__name__ == "ValueError":
                self.output.insertText(f"An exception occured: {type(ex).__name__} - {ex}. Ensure all fields have an integer")
            else:
                self.output.insertText(f"An exception occured: {type(ex).__name__} - {ex}")


class FileMenu(tk.Menu):

    def __init__(self, master):
        super().__init__(master)
    
        self.master = master

        self.createFileMenu()

    def restartProgram(self):
        self.master.destroy()
        self.program = Program("Calculator", (600, 600))
        self.program.mainloop()

    def createFileMenu(self):
        # Creating main menu
        self.menu = tk.Menu(self)

        # Creating file menu
        self.fileMenu = tk.Menu(self.menu)
        self.menu.add_cascade(label = "File", menu = self.fileMenu)
        # Creating options within the accessibility menu
        self.fileMenu.add_command(label = "Restart", command = lambda: self.restartProgram())
        self.fileMenu.add_separator()
        self.fileMenu.add_command(label = "Exit", command = lambda: self.master.quit())

        # Creating accessibility options menu
        self.helpMenu = tk.Menu(self.menu)
        self.menu.add_cascade(label = "Accessibility", menu = self.helpMenu)
        # Creating options within the accessibility menu
        self.helpMenu.add_command(label = "Toggle high contrast") # Add commands later

        # Creating font size menu and adding 3 presets
        self.sizeMenu = tk.Menu(self.helpMenu) 
        self.helpMenu.add_cascade(label = "Font size", menu = self.sizeMenu)  # Adding cascade to sizeMenu
        # Creating commands within the font size menu
        self.sizeMenu.add_command(label = "Small")
        self.sizeMenu.add_command(label = "Medium")
        self.sizeMenu.add_command(label = "Large")

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
        
        self.textConfigDb = {
            "entries" : {
                self.entries.firstTerm : ["First term"],
                self.entries.commonDifference : ["Common difference", "Common ratio"],
                self.entries.numberOfTerms : ["Number of terms"]
            },

            "buttons" : {
                self.buttons.clear : "Clear",
                self.buttons.calculate : "Calculate"
            },

            "radiobuttons" : {
                self.radiobuttons.arithButton : "Arithmetic Series",
                self.radiobuttons.geomButton : "Geometric Series"
            },

            "filemenu" : {
                self.filemenu.menu : ["File", "Accessibility"],
                self.filemenu.fileMenu : ["Restart", "Exit"],
                self.filemenu.helpMenu : ["Toggle high contrast", "Font size", "Languages"],
                self.filemenu.sizeMenu : ["Small", "Medium", "Large"]

            }
        }

        self.fullEnglishDb = self.textConfigDb.copy() # fullEnglishDb does not include modified file menu names (file menu commands must be directly modified by name)

        self.langFilemenuCommands()

    def langFilemenuCommands(self):
        self.languageDb = googletrans.LANGUAGES
        for name, acronym in self.languageDb.items():
            # Capture current value of value and assigns it to the lang parameter of the translator function 
            self.filemenu.langMenu.add_command(label = acronym.title(), command = lambda lang = name: self.translatorFunc(lang))
    
    def translatorFunc(self, lang):
        self.trans = googletrans.Translator()

        if lang != "en": # Changing title of the program
            self.title = "Calculator"
            self.transtitle = self.trans.translate(self.title, dest = lang)
            self.master.title(str(self.transtitle.text))
        else:
            self.master.title("Calculator")
            
        for mainKey in self.textConfigDb: # mainKey is widget name 
            if mainKey != "filemenu": # Filemenu is not configured by .config (grouping with if statement is done by configuration methods)

                if mainKey == "entries":

                    for subKey in self.textConfigDb[mainKey]:
                        for i, item in enumerate(self.textConfigDb[mainKey][subKey]): # Enumerating each list (using enumerate to update tempTextDb)
                            self.text = item
                            if lang != "en":
                                self.transtext = self.trans.translate(self.text, dest = lang)
                                self.entries.tempTextDb[subKey][i] = str(self.transtext.text)
                            else:
                                self.entries.tempTextDb[subKey][i] = self.text 
                    self.entries.updateTempText(fullReload = True) # Reloads temporary text
                
                else: # Translating buttons and radiobuttons
                    
                    for subKey in self.textConfigDb[mainKey]:
                        self.text = self.textConfigDb[mainKey][subKey]
                        self.transtext = self.trans.translate(self.text, dest = lang)
                        subKey.config(text = str(self.transtext.text))
            
            else: 
                
                for subKey in self.textConfigDb[mainKey]:
                    for i, item in enumerate(self.textConfigDb[mainKey][subKey]):
                        self.text = self.fullEnglishDb[mainKey][subKey][i] # Uses fullEnglishDb so translation goes from English to lang
                        if lang != "en":
                            self.transtext = self.trans.translate(self.text, dest = lang)
                            subKey.entryconfig(item, label = str(self.transtext.text)) # Filemenu is configured by [level of hierarchy].entryconfig("name", label = "newname")
                            self.textConfigDb[mainKey][subKey][i] = str(self.transtext.text) # Assigns new names to textConfigDb to reconfigure subsequent File menus
                        else:
                            subKey.entryconfig(item, label = self.text) # Does not change file menu text to English??
                            self.textConfigDb[mainKey][subKey][i] = self.text 

        self.radiobuttons.var.set(1) # Selects arithmetic series by default
        self.buttons.clear.focus_set() # Redirect focus from entry widget to prevent user being able to edit temporary text


def startProgram(): # Start program function
    program = Program("Summing Series", (500, 600)) 
    program.mainloop() 

if __name__ == "__main__": # Allows program to only run when the file is executed as a script, allowing for modularity and reusability
    startProgram() 