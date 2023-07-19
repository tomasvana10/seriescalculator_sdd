import tkinter as tk 
import tkinter.messagebox
import customtkinter as ctk
import json
import os
from configparser import ConfigParser

class Program(ctk.CTk):
    '''Main Program Window'''
    def __init__(self, title, size): 
        super().__init__()
        # Providing program directory for assistance to child classes
        self.currentDir = os.path.dirname(os.path.abspath(__file__)) 

        self.cfg = ConfigParser() # Allows program to edit config file
        self.cfg.read(f"{self.currentDir}/config.ini")

        '''Default program configuration'''
        self.title(title)
        self.geometry(f"{size[0]}x{size[1]}")
        self.maxsize(size[0], size[1])
        ctk.set_appearance_mode(self.cfg.get("Main", "appearance"))
        ctk.set_default_color_theme(self.cfg.get("Main", "theme"))
        ctk.set_widget_scaling(self.cfg.getfloat("Main", "scale"))

        self.frameGen()
        self.classInst()

    def frameGen(self):
        '''Frames'''
        self.mainFrame = ctk.CTkFrame(self)
        self.mainFrame.pack(fill = tk.BOTH, expand = True)
        self.mainFrame.grid_columnconfigure(1, weight = 1)
        self.mainFrame.grid_columnconfigure(2, weight = 0)
        self.mainFrame.grid_rowconfigure(1, weight = 1)

        self.calcFrame = ctk.CTkFrame(self.mainFrame, fg_color = ("#dbdbdb", "gray17"))
        self.calcFrame.grid(row = 1, column = 1, sticky = "nsew")
        self.calcFrame.grid_rowconfigure(1, weight = 0)
        self.calcFrame.grid_rowconfigure((2, 3), weight = 2)
        self.calcFrame.grid_columnconfigure((1, 2), weight = 1)

        self.sidebarFrame = ctk.CTkFrame(self.mainFrame, fg_color = ("#cccccc", "gray20"), 
                                         corner_radius = 0)
        self.sidebarFrame.grid(row = 1, column = 2, sticky = "nsew")
        self.sidebarFrame.grid_rowconfigure(1, weight = 3)
        self.sidebarFrame.grid_rowconfigure((2, 3, 4), weight = 2)
        self.titleLabel = ctk.CTkLabel(self.sidebarFrame, text = "Summing Series", 
                                       font = ctk.CTkFont(size = 23, weight = "bold"))
        self.titleLabel.grid(row = 1, column = 1, padx = 20)

    def classInst(self):
        '''Widget Classes'''
        self.entries = Entries(self, self.calcFrame) 
        self.output = Output(self, self.calcFrame)
        self.radiobuttons = Radiobuttons(self, self.calcFrame, self.entries)
        self.buttons = Buttons(self, self.calcFrame, self.entries, self.radiobuttons, self.output)

        '''File Menu Classes'''
        self.filemenu = FileMenu(self)

        '''Accessibility Classes'''
        self.fontsize = FontSize(self, self.sidebarFrame)
        self.appearance = Appearance(self, self.sidebarFrame)
        self.languages = Languages(self, self.sidebarFrame, self.entries, self.buttons, 
                                   self.radiobuttons, self.fontsize, self.appearance, self.filemenu)
        self.languages.switchLang(self.cfg.get("Main", "language"))
    
    def configUpdater(self, scale = False, appearance = False, theme = False, language = False):
        self.cfg.read(f"{self.currentDir}/config.ini")
        if scale:
            self.cfg["Main"]["scale"] = str(scale)
        if appearance:
            self.cfg["Main"]["appearance"] = appearance
        if theme:
            self.cfg["Main"]["theme"] = theme
        if language:
            self.cfg["Main"]["language"] = str(language)
        
        with open(f"{self.currentDir}/config.ini", "w") as f:
            self.cfg.write(f)

    def restartProgram(self):
        self.destroy()
        self.program = Program("Summing Series", (700, 580)) 
        self.program.mainloop()


class Entries(ctk.CTkFrame):
    '''Entry creation and gridding and clear entry function'''
    def __init__(self, master, calcframe): 
        super().__init__(calcframe) # All widgets are gridded in a frame, which is gridded onto calcframe
        self.grid(row = 2, column = 1, sticky = "e")

        self.placeholderText = ["Common difference", "Common ratio"] # Modified by translator which then 
                                                                     # calls placeholderSwitcher()

        self.entryGen() 

    def entryGen(self): 
        self.firstTerm = ctk.CTkEntry(self, placeholder_text = "First term") 
        self.commonDifference = ctk.CTkEntry(self, placeholder_text = "Common difference")
        self.numberOfTerms = ctk.CTkEntry(self, placeholder_text = "Number of terms")

        self.firstTerm.grid(row = 1, column = 1)
        self.commonDifference.grid(row = 2, column = 1, pady = 10)
        self.numberOfTerms.grid(row = 3, column = 1)

    def placeholderSwitcher(self, entry): 
        if entry == 1:
            self.commonDifference.configure(placeholder_text = self.placeholderText[0])
        else:
            self.commonDifference.configure(placeholder_text = self.placeholderText[1])
        self.master.focus() # Remove focus from widget to prevent placeholder text 
                            # becoming editable (focusing on main CTk() instance)

    def clearEntries(self): 
        if self.firstTerm.get() != "": # Entries are only cleared if there is a string of length > 0
                                       # Prevents clearing placeholder text
            self.firstTerm.delete(0, ctk.END)
        if self.commonDifference.get() != "":
            self.commonDifference.delete(0, ctk.END)
        if self.numberOfTerms.get() != "":
            self.numberOfTerms.delete(0, ctk.END)
        self.master.focus() # Same concept in placeholderSwitcher()


class Output(ctk.CTkFrame):
    '''Text box creation and gridding and text insertion function'''
    def __init__(self, master, calcframe):
        super().__init__(calcframe)
        self.grid(row = 3, column = 1, columnspan = 2, sticky = "n", padx = 10, 
                  pady = (10, 30))
        self.grid_columnconfigure(1, weight=1)  
        self.grid_rowconfigure(1, weight=1) 

        self.outputGen()

    def outputGen(self):
        self.sumOutput = ctk.CTkTextbox(self, state = "disabled", width = 300, 
                                        height = 200, wrap = tk.WORD) # Only allows copying of 
                                                                      # text, not entry or deletion

        self.sumOutput.grid(row=1, column=1)
    
    def insertText(self, text):
        self.sumOutput.configure(state = "normal") # Enable text entry
        self.sumOutput.delete(1.0, tk.END) 
        self.sumOutput.insert(1.0, text) # Insert text
        self.sumOutput.configure(state = "disabled") # Disable text entry


class Radiobuttons(ctk.CTkFrame):
    '''Radiobutton creation and gridding'''
    def __init__(self, master, calcframe, entries):
        super().__init__(calcframe)
        self.grid(row = 1, column = 1, columnspan = 2, pady = (55, 20), sticky = "s")

        self.entries = entries

        self.radioButtonGen()

    def radioButtonGen(self):
        self.selection = tk.IntVar(value = 1) # Default value (Arithmetic Series)
        self.arithButton = ctk.CTkRadioButton(self, text = "Arithmetic Series", variable = self.selection, 
                                              value = 1, command = lambda: 
                                              self.entries.placeholderSwitcher(1))
        self.geomButton = ctk.CTkRadioButton(self, text = "Geometric Series", variable = self.selection, 
                                             value = 2, command = lambda: 
                                             self.entries.placeholderSwitcher(2))
        
        self.arithButton.grid(row = 1, column = 1, padx = (0, 10))
        self.geomButton.grid(row = 1, column = 2)


class Buttons(ctk.CTkFrame):
    '''Button creation and gridding, clear and calculate functions and error handling'''
    def __init__(self, master, calcframe, entries, radiobuttons, output):
        super().__init__(calcframe)
        self.grid(row = 2, column = 2, padx = (20, 0), sticky = "w")

        self.entries = entries 
        self.radiobuttons = radiobuttons
        self.output = output

        self.errors = [
            "An exception occured: ValueError - Ensure all fields are filled and have numeric entries",
            "An exception occured: InvalidNumberOfTerms - The length of the \
            series cannot be a negative number or 0, please choose an appropriate length",
            "An exception occured: OverflowError - Please reduce the value of the entered integers",
        ]
    
        self.buttonGen()
        
    def buttonGen(self):
        self.clearButton = ctk.CTkButton(self, text = "Clear", command = self.clear)
        self.calculateButton = ctk.CTkButton(self, text = "Calculate", command = self.calculate)

        self.clearButton.grid(row = 1, column = 1, pady = (0, 10))
        self.calculateButton.grid(row = 2, column = 1)
    
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
                    self.sum = (self.numberOfTerms / 2) * (2 * self.firstTerm + (self.numberOfTerms - 1) * \
                                                           self.commonDiffOrRatio)
                    self.output.insertText(self.sum)
                
            elif self.seqType == 2: # Geometric Series
                if self.numberOfTerms <= 0:
                    self.output.insertText(self.errors[1])

                else:
                    if self.commonDiffOrRatio == 1:
                        self.sum = self.firstTerm * self.numberOfTerms

                    else:
                        self.sum = self.firstTerm * (1 - self.commonDiffOrRatio ** self.numberOfTerms) / \
                                                    (1 - self.commonDiffOrRatio)

                    self.output.insertText(self.sum)
    
        except Exception as ex:
            if type(ex).__name__ == "ValueError":
                self.output.insertText(self.errors[0])
            elif type(ex).__name__ == "OverflowError":
                self.output.insertText(self.errors[2])


class FontSize(ctk.CTkFrame):
    '''Font size option menu creation'''
    def __init__(self, master, sidebarframe):
        super().__init__(sidebarframe)
        self.grid(row = 2, column = 1)

        self.master = master

        self.sizes = ["Small", "Medium", "Large"]

        self.fontOptionsMaker()
    
    def fontOptionsMaker(self):
        self.fontOptions = ctk.CTkOptionMenu(self, values = self.sizes, 
                                             command = self.changeScale)
        self.fontOptionsLabel = ctk.CTkLabel(self, text = "Size")

        # Default values from config.ini
        self.scaleFloat = float(self.master.cfg.get("Main", "scale"))
        self.scaleStr = "Small" if self.scaleFloat == 0.7 else \
        "Medium" if self.scaleFloat == 1.0 else "Large"
        self.fontOptions.set(self.scaleStr)

        self.fontOptions.grid(row = 2, column = 1)
        self.fontOptionsLabel.grid(row = 1, column = 1)
    
    def changeScale(self, choice):
        self.scaleChoice = 0.7 if self.sizes.index(choice) == 0 else \
        1.0 if self.sizes.index(choice) == 1 else 1.3
        ctk.set_widget_scaling(self.scaleChoice)
        self.master.configUpdater(scale = self.scaleChoice)


class Appearance(ctk.CTkFrame):
    '''Options to change appearance and colour themes'''
    def __init__(self, master, sidebarframe):
        super().__init__(sidebarframe)
        self.grid(row = 3, column = 1)
        
        self.master = master

        self.appearances = ["light", "dark", "system"]
        self.themes =      ["blue", "green", "dark-blue"]

        self.appearanceOptionsMaker()

    def appearanceOptionsMaker(self):
        self.appearanceOptions = ctk.CTkOptionMenu(self, values = self.appearances, 
                                                   command = self.changeAppearance)
        self.themeOptions = ctk.CTkOptionMenu(self, values = self.themes, 
                                              command = self.changeTheme)
        self.appearanceOptionsLabel = ctk.CTkLabel(self)
        self.themeOptionsLabel = ctk.CTkLabel(self)
        
        # Default values from config.ini
        self.appearanceOptions.set(self.master.cfg.get("Main", "appearance"))
        self.themeOptions.set(self.master.cfg.get("Main", "theme"))

        self.appearanceOptions.grid(row = 2, column = 1)
        self.themeOptions.grid(row = 4, column = 1)
        self.appearanceOptionsLabel.grid(row = 1, column = 1)
        self.themeOptionsLabel.grid(row = 3, column = 1)

    def changeAppearance(self, choice): 
        self.appearanceChoice = "light" if self.appearances.index(choice) == 0 else \
        "dark" if self.appearances.index(choice) == 1 else "system"
        ctk.set_appearance_mode(self.appearanceChoice)
        self.master.configUpdater(appearance = self.appearanceChoice)

    def changeTheme(self, choice):
        self.themeChoice = "blue" if self.themes.index(choice)== 0 else \
        "green" if self.themes.index(choice) == 1 else "dark-blue"
        self.master.configUpdater(theme = self.themeChoice)
        self.master.restartProgram()


class FileMenu(tk.Menu):
    '''Filemenu structure creation with commands'''
    def __init__(self, master):
        super().__init__(master)
    
        self.master = master

        self.menuLabels = ["File", "Restart", "Exit"]

        self.createFileMenu()

    def createFileMenu(self):
        # Creating main program menu
        self.menu = tk.Menu(self)

        # Creating file menu cascade
        self.fileMenu = tk.Menu(self.menu)
        self.menu.add_cascade(label = self.menuLabels[0], menu = self.fileMenu)
        # Creating commands within the file cascade
        self.fileMenu.add_command(label = self.menuLabels[1], command = lambda: self.master.restartProgram())
        self.fileMenu.add_separator()
        self.fileMenu.add_command(label = self.menuLabels[2], command = lambda: self.master.quit())

        # Setting main menu
        self.master.config(menu = self.menu)


class Languages(ctk.CTkFrame):
    '''Loads language jsons and switches widget text'''
    def __init__(self, master, sidebarframe, entries, buttons, radiobuttons, fontsize, appearance, filemenu):
        super().__init__(sidebarframe)
        self.grid(row = 4, column = 1)

        self.master = master
        self.entries = entries
        self.buttons = buttons
        self.radiobuttons = radiobuttons
        self.fontsize = fontsize
        self.appearance = appearance
        self.filemenu = filemenu

        self.translationsPath = os.path.join(self.master.currentDir, "translations") 
        self.currentLangDb = {} # Stores text of current language and it's relation to widget variables
        self.loadedLanguages = [] # Stores loaded language dictionaries in tuple form; ("langname", langDb)
        self.loadedLangTuple = ("",) # Must be created outside of switchLang(). Aids to detect if
                                     # user is switching to same language

        self.langOptionsMaker() 

    def langOptionsMaker(self):
        self.availableLanguages = os.listdir(self.translationsPath) # Reads json file and returns a list of available languages
        self.availableLanguages = [jsonFile.replace(".json", "") for jsonFile in self.availableLanguages]
        self.availableLanguages = sorted(self.availableLanguages) 
        # Available languages look like this: ["English", "Spanish", "French"]
        self.langOptions = ctk.CTkOptionMenu(self, values = self.availableLanguages, 
                                              command = self.switchLang)
        self.langOptionsLabel = ctk.CTkLabel(self, text = "Languages")
        self.langOptions.grid(row = 2, column = 1)
        self.langOptionsLabel.grid(row = 1, column = 1)

    def switchLang(self, lang):
        self.langLoader(lang) 

        '''Entries'''
        self.entries.firstTerm.configure(placeholder_text = self.currentLangDb["entries"][0])
        self.entries.placeholderText[0] = self.currentLangDb["entries"][1][0]
        self.entries.placeholderText[1] = self.currentLangDb["entries"][1][1]
        self.entries.placeholderSwitcher(self.radiobuttons.selection.get())
        self.entries.numberOfTerms.configure(placeholder_text = self.currentLangDb["entries"][2])

        '''Buttons'''
        self.buttons.clearButton.configure(text = self.currentLangDb["buttons"][0])
        self.buttons.calculateButton.configure(text = self.currentLangDb["buttons"][1])

        '''Radiobuttons'''
        self.radiobuttons.arithButton.configure(text = self.currentLangDb["radiobuttons"][0])
        self.radiobuttons.geomButton.configure(text = self.currentLangDb["radiobuttons"][1])

        '''Fontsize optionbox and label'''
        self.fontsize.fontOptionsLabel.configure(text = self.currentLangDb["fontsize"][0])
        # Remembers prior selection and sets option display to that selection but in the new language
        self.sizeIndex = self.fontsize.sizes.index(self.fontsize.fontOptions.get())
        for i, _ in enumerate(self.fontsize.sizes):
            self.fontsize.sizes[i] = self.currentLangDb["fontsize"][1][i]
        self.fontsize.fontOptions.configure(values = self.fontsize.sizes)
        self.fontsize.fontOptions.set(self.fontsize.sizes[self.sizeIndex])

        '''Appearance optionbox and label'''
        self.appearance.appearanceOptionsLabel.configure(text = self.currentLangDb["appearance"][0][0])
        self.appearanceIndex = self.appearance.appearances.index(self.appearance.appearanceOptions.get())
        for i, _ in enumerate(self.appearance.appearances):
            self.appearance.appearances[i] = self.currentLangDb["appearance"][0][1][i]
        self.appearance.appearanceOptions.configure(values = self.appearance.appearances)
        self.appearance.appearanceOptions.set(self.appearance.appearances[self.appearanceIndex])
        
        self.appearance.themeOptionsLabel.configure(text = self.currentLangDb["appearance"][1][0])
        self.themeIndex = self.appearance.themes.index(self.appearance.themeOptions.get())
        for i, _ in enumerate(self.appearance.themes):
            self.appearance.themes[i] = self.currentLangDb["appearance"][1][1][i]
        self.appearance.themeOptions.configure(values = self.appearance.themes)
        self.appearance.themeOptions.set(self.appearance.themes[self.themeIndex])

        '''Language optionbox and label'''
        self.langOptionsLabel.configure(text = self.currentLangDb["languages"][0])
        self.langOptions.set(self.master.cfg.get("Main", "language"))

        '''Error text'''
        for i, _ in enumerate(self.buttons.errors):
            self.buttons.errors[i] = self.currentLangDb["errors"][i]
        self.buttons.calculate() 

        '''Filemenu'''
        self.filemenu.menu.entryconfigure(self.filemenu.menuLabels[0], label = self.currentLangDb["filemenu"][0])
        self.filemenu.fileMenu.entryconfigure(self.filemenu.menuLabels[1], label = self.currentLangDb["filemenu"][1])
        self.filemenu.fileMenu.entryconfigure(self.filemenu.menuLabels[2], label = self.currentLangDb["filemenu"][2])
        for i, _ in enumerate(self.filemenu.menuLabels):
            self.filemenu.menuLabels[i] = self.currentLangDb["filemenu"][i]

        '''Title and title label'''
        self.master.title(self.currentLangDb["title"][0])
        self.master.titleLabel.configure(text = self.currentLangDb["title"][0])
        
    def langLoader(self, lang):
        # If language is already set to the language being switched to
        if self.loadedLangTuple[0] == lang:
            tk.messagebox.showinfo(title = self.currentLangDb["langloader"][0], 
                                   message = f"{self.currentLangDb['langloader'][1]} {lang}")
            return

        if not any(langTuple[0] == lang for langTuple in self.loadedLanguages):
            # Load new language and switch database
            try:
                with open(f"{self.translationsPath}/{lang.title()}.json", "r") as f: 
                    rawLangDb = json.load(f)
                    self.loadedLangTuple = self.langDbConfigurer(lang, rawLangDb) # Returns ("lang", 
                                                                                  # lang dictionary)
                    self.loadedLanguages.append(self.loadedLangTuple) 
                    self.currentLangDb = self.loadedLangTuple[1] # Only assigns dictionary part of 
                                                                 # tuple to currentLangDb
                    self.master.configUpdater(language = self.loadedLangTuple[0])
            
            except json.decoder.JSONDecodeError:
                tk.messagebox.showinfo(title = self.currentLangDb["langloader"][0], 
                                       message = f"{lang} {self.currentLangDb['langloader'][2]}")
                self.langOptions.set(self.loadedLangTuple[0]) # Change optionmenu selection back to
                                                              # the current language

        else:
            # Switch database to already loaded language
            self.loadedLangTuple = [langTuple for langTuple in self.loadedLanguages if langTuple[0] == lang]
            self.currentLangDb = self.loadedLangTuple[0][1]
            self.master.configUpdater(language = self.loadedLangTuple[0])

    def langDbConfigurer(self, lang, rawLangDb):
        rawLangDb["entries"][1:3] = [rawLangDb["entries"][1:3]] # Group index 1 and 2 into single list
        
        rawLangDb["fontsize"][1:4] = [rawLangDb["fontsize"][1:4]]

        values = rawLangDb["appearance"]
        self.groupedValues = [values[0], values[2:5]], [values[1], values[5:]]
        rawLangDb["appearance"] = self.groupedValues

        return (lang, rawLangDb) # Assigned to the variable loadedLangTuple 

if __name__ == "__main__": # Allows program to only run when the file is 
                           # executed as a script, allowing for modularity and reusability
    program = Program("Summing Series", (700, 580)) 
    program.mainloop() 