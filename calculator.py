import tkinter as tk 
import customtkinter as ctk

class Program(ctk.CTk):
    '''Main Program Window'''
    def __init__(self, title, size, appearance, theme, scale): 
        super().__init__()

        '''Default program specifications'''
        self.title(title)
        self.geometry(f"{size[0]}x{size[1]}")
        ctk.set_appearance_mode(appearance)
        ctk.set_default_color_theme(theme)
        ctk.set_widget_scaling(scale)

        self.frame = ctk.CTkFrame(self) # Main frame/background
        self.frame.pack(expand = 1, fill = tk.BOTH)

        '''File Menu Classes'''
        self.filemenu = FileMenu(self)

        '''Widget Classes'''
        self.entries = Entries(self) 
        self.output = Output(self)
        self.radiobuttons = Radiobuttons(self, self.entries)
        self.buttons = Buttons(self, self.entries, self.radiobuttons, self.output)

        '''Accessibility Classes'''
        self.fontsize = FontSize(self)
        self.appearance = Appearance(self)
        self.translator = Translator(self, self.entries, self.buttons, self.radiobuttons, 
                                    self.filemenu)

class Entries(ctk.CTkFrame):
    '''Entry creation and related functions'''
    def __init__(self, master): 
        super().__init__(master) # Ensures proper inheritance
        self.place(x = 210, y = 190, anchor = "center")

        self.entryGen() 
        self.entryPlacer()

    def entryGen(self): # Widget creation
        self.firstTerm = ctk.CTkEntry(self,placeholder_text = "First term") 
        self.commonDifference = ctk.CTkEntry(self, placeholder_text = "Common difference")
        self.numberOfTerms = ctk.CTkEntry(self, placeholder_text = "Number of terms")
        
    def entryPlacer(self): # Placing widgets
        self.firstTerm.pack()
        self.commonDifference.pack()
        self.numberOfTerms.pack()

    def placeholderSwitcher(self, entry):
        if entry == 1:
            self.commonDifference.configure(placeholder_text = "Common difference")
        else:
            self.commonDifference.configure(placeholder_text = "Common ratio")
        self.master.focus() # Remove focus from widget to prevent placeholder text 
                            # becoming editable (focusing on main CTk() instance)

    def clearEntries(self): 
        self.firstTerm.delete(0, ctk.END)
        self.commonDifference.delete(0, ctk.END)
        self.numberOfTerms.delete(0, ctk.END)
        self.master.focus()

class Output(ctk.CTkFrame):
    '''Text box creation and insertion of result'''
    def __init__(self, master):
        super().__init__(master)
        self.place(x = 255, y = 325, anchor = "center")

        self.outputGen()
        self.outputPlacer()

    def outputGen(self):
        self.sumOutput = ctk.CTkTextbox(self, state = "disabled", width = 200, 
                                        height = 120) # Only allows copying of text, not entry or deletion

    def outputPlacer(self):
        self.sumOutput.pack()
    
    def insertText(self, result):
        self.sumOutput.configure(state = "normal") # Enable text entry
        self.sumOutput.delete(1.0, tk.END) 
        self.sumOutput.insert(1.0, result) # Enter text
        self.sumOutput.configure(state = "disabled")

class Radiobuttons(ctk.CTkFrame):
    '''Radiobutton creation'''
    def __init__(self, master, entries):
        super().__init__(master)
        self.place(x = 400, y = 172, anchor = "center")

        self.entries = entries

        self.radioButtonGen()
        self.radioButtonPlacer()

    def radioButtonGen(self):
        self.selection = tk.IntVar(value = 1) # Set radiobutton selection to Arithmetic Series
        self.arithButton = ctk.CTkRadioButton(self, text = "Arithmetic Series", variable = self.selection, 
                                              value = 1, command = lambda: self.entries.placeholderSwitcher(1))
        self.geomButton = ctk.CTkRadioButton(self, text = "Geometric Series", variable = self.selection, 
                                             value = 2, command = lambda: self.entries.placeholderSwitcher(2))
        
    def radioButtonPlacer(self):
        self.arithButton.pack()
        self.geomButton.pack()

class Buttons(ctk.CTkFrame):
    '''Button creation, clear and calculate functions and error handling'''
    def __init__(self, master, entries, radiobuttons, output):
        super().__init__(master)
        self.place(x = 337, y = 200)

        self.entries = entries 
        self.radiobuttons = radiobuttons
        self.output = output

        self.errors = [
            "An exception occured: ValueError - Ensure all fields are filled and have numeric entries",
            "An exception occured: InvalidNumberOfTerms - The length of the \
            series cannot be a negative number or 0, please choose an appropriate length",
        ]
    
        self.buttonGen()
        self.buttonPlacer()
        
    def buttonGen(self):
        self.clear = ctk.CTkButton(self, text = "Clear", command = self.clear)
        self.calculate = ctk.CTkButton(self, text = "Calculate", command = self.calculate)
    
    def buttonPlacer(self):
        self.clear.pack()
        self.calculate.pack()
    
    def clear(self):
        self.entries.clearEntries()
        self.radiobuttons.selection.set(1)
        self.output.insertText("")

    def calculate(self):
        self.seqType = self.radiobuttons.selection.get()

        try:
            self.firstTerm = float(self.entries.firstTerm.get())
            self.commonDiffOrRatio = float(self.entries.commonDifference.get())
            self.numberOfTerms = int(self.entries.numberOfTerms.get())

            if self.seqType == 1: # Arithmetic series
                if self.numberOfTerms <= 0: # Common difference must be greater than 0
                    self.output.insertText(self.errors[1])

                else:
                    self.sum = (self.numberOfTerms / 2) * (2 * self.firstTerm + \
                                                           (self.numberOfTerms - 1) * self.commonDiffOrRatio)
                    self.output.insertText(self.sum)
                
            elif self.seqType == 2: # Geometric Series
                if self.numberOfTerms <= 0:
                    self.output.insertText(self.errors[1])

                else:
                    if self.commonDiffOrRatio == 1:
                        self.sum = self.firstTerm * self.numberOfTerms

                    else:
                        self.sum = self.firstTerm * (1 - self.commonDiffOrRatio \
                                                     ** self.numberOfTerms) / (1 - self.commonDiffOrRatio)

                    self.output.insertText(self.sum)
    
        except Exception:
            self.output.insertText(self.errors[0])

class FileMenu(tk.Menu):
    '''Filemenu structure creation with commands'''
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
        self.helpMenu.add_cascade(label = "Appearance") # Add commands later
        self.helpMenu.add_cascade(label = "Theme")

        # Creating font size menu and adding 3 presets
        self.sizeMenu = tk.Menu(self.helpMenu) 
        self.helpMenu.add_cascade(label = "Size", menu = self.sizeMenu)  # Adding cascade to sizeMenu
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

class FontSize(ctk.CTkFrame):
    '''Font size option menu creation'''
    def __init__(self, master):
        super().__init__(master)
        self.place(x=150, y = 500)

        self.fontOptionsMaker()
        self.fontOptionsPlacer()
    
    def fontOptionsMaker(self):
        self.fontOptions = ctk.CTkOptionMenu(self, values = ["Small", "Medium", "Large"], 
                                             command = self.changeScale)
        self.fontOptions.set("Medium")
        self.fontOptionsLabel = ctk.CTkLabel(self, text = "Size")
    
    def fontOptionsPlacer(self):
        self.fontOptions.pack()
        self.fontOptionsLabel.pack()
    
    def changeScale(self, size):
        self.scale = 0
        match size:
            case "Small":
                self.scale = 0.7
            case "Medium":
                self.scale = 1.0
            case "Large":
                self.scale = 1.3
        ctk.set_widget_scaling(self.scale)

class Appearance(ctk.CTkFrame):
    '''Options to change appearance and colour themes'''
    def __init__(self, master):
        super().__init__(master)
        self.place(x = 370, y = 400)

        self.master = master

        self.appearanceOptionsMaker()
        self.appearanceOptionsPlacer()

    def appearanceOptionsMaker(self):
        self.appearanceOptions = ctk.CTkOptionMenu(self, values = ["Light", "Dark", "System"], 
                                                   command = self.changeAppearance)
        self.appearanceOptions.set("Dark")
        self.themeOptions = ctk.CTkOptionMenu(self, values = ["Blue", "Green", "Dark blue"], 
                                              command = self.changeColour)
        self.appearanceOptionsLabel = ctk.CTkLabel(self, text = "Appearance")
        self.themeOptionsLabel = ctk.CTkLabel(self, text = "Themes")
        
    def appearanceOptionsPlacer(self):
        self.appearanceOptions.grid(row = 2, column = 1)
        self.themeOptions.grid(row = 4, column = 1)
        self.appearanceOptionsLabel.grid(row = 1, column = 1)
        self.themeOptionsLabel.grid(row = 3, column = 1)

    def changeAppearance(self, appearance):
        ctk.set_appearance_mode(appearance)

    def changeColour(self, colour: str):
        colour = colour.casefold()
        colour = colour.replace(" ", "-")
        ctk.set_default_color_theme(colour) # currently not working

class Translator(ctk.CTkFrame):

    def __init__(self, master, entries, buttons, radiobuttons, filemenu):
        super().__init__(master)

        self.entries = entries
        self.buttons = buttons
        self.radiobuttons = radiobuttons
        self.filemenu = filemenu

    def langOptionsMaker(func):
        def wrapper():
            pass

        return wrapper

    @langOptionsMaker
    def langDbLoader():
        pass

if __name__ == "__main__": # Allows program to only run when the file is 
                           # executed as a script, allowing for modularity and reusability
    program = Program("Summing Series", (550, 650), "Dark", "blue", 1.0) 
    program.mainloop() 