''' Refer to translator.py if you are unsure what exactly is contained 
in the keys, values and array elements of currentLangDb (translations)
'''

import re
import json
import os
from configparser import ConfigParser
import tkinter as tk 
import tkinter.messagebox
from typing import (
    Tuple,
    List,
    Dict,
)

import customtkinter as ctk

class Program(ctk.CTk):
    '''Main Program Window'''
    def __init__(self, title: str, size: Tuple[int, int]) -> None: 
        super().__init__()
        # Providing program directory for assistance to child classes
        self.currentDir = os.path.dirname(os.path.abspath(__file__)) 
        # Detect window deletion -> display messagebox
        self.protocol("WM_DELETE_WINDOW", 
                      lambda: self.restartProgram(themeRestart=False))
        self.cfg = ConfigParser() # Assign config parser instance to variable
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

    def frameGen(self) -> None:
        '''Frames'''
        # mainFrame holds all other frames
        self.mainFrame = ctk.CTkFrame(self)
        self.mainFrame.pack(fill=tk.BOTH, expand=True) # Expand to fill 
        self.mainFrame.grid_columnconfigure(1, weight=1)
        self.mainFrame.grid_columnconfigure(2, weight=0)
        self.mainFrame.grid_rowconfigure(1, weight=1)
        # calcFrame holds all calculator-related widgets
        self.calcFrame = ctk.CTkFrame(self.mainFrame, fg_color=("#dbdbdb", 
                                                                "gray17"))
        self.calcFrame.grid(row=1, column=1, sticky="nsew")
        self.calcFrame.grid_rowconfigure(1, weight=0)
        self.calcFrame.grid_rowconfigure((2, 3), weight=2)
        self.calcFrame.grid_columnconfigure((1, 2), weight=1)
        # sidebarFrame holds all accessibility widgets and title label
        self.sidebarFrame = ctk.CTkFrame(self.mainFrame, fg_color=(
                                                                "#cccccc", 
                                                                "gray20"), 
                                                        corner_radius=0)
        self.sidebarFrame.grid(row=1, column=2, sticky="nsew")
        self.sidebarFrame.grid_rowconfigure(1, weight=3)
        self.sidebarFrame.grid_rowconfigure((2, 3, 4), weight=2)
        self.titleLabel = ctk.CTkLabel(self.sidebarFrame, 
                                       text="Summing Series", 
                                       font=ctk.CTkFont(size=23, 
                                                        weight="bold"))
        self.titleLabel.grid(row=1, column=1, padx=20)

    def classInst(self) -> None:
        '''Widget Classes'''
        self.entries = Entries(self, self.calcFrame) 
        self.output = Output(self, self.calcFrame)
        self.radiobuttons = Radiobuttons(self, self.calcFrame, self.entries)
        self.buttons = Buttons(self, self.calcFrame, self.entries, 
                               self.radiobuttons, self.output)
        '''File Menu Classes'''
        self.filemenu = FileMenu(self)
        '''Accessibility Classes'''
        self.fontsize = FontSize(self, self.sidebarFrame)
        self.appearance = Appearance(self, self.sidebarFrame)
        self.languages = Languages(self, self.sidebarFrame, self.entries, 
                                   self.buttons, self.radiobuttons, 
                                   self.fontsize, self.appearance, 
                                   self.filemenu)
        self.languages.switchLang(self.cfg.get("Main", "language"))
    
    def configUpdater(self, 
                      scale: bool = False, 
                      appearance: bool = False, 
                      theme: bool = False, 
                      language: bool = False) -> None:
        # Read data from self.cfg
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

    def onWindowDestroy(self, themeRestart: bool) -> bool:
        if themeRestart:
            # Create message box (Y/n)
            if tk.messagebox.askokcancel(
                    self.languages.currentLangDb["destroy"][2], 
                    self.languages.currentLangDb["destroy"][0]\
                    .format(self.languages.currentLangDb["destroy"][2])):
                return True 
        else:
            if tk.messagebox.askokcancel(
                    self.languages.currentLangDb["destroy"][1], 
                    self.languages.currentLangDb["destroy"][0]\
                    .format(self.languages.currentLangDb["destroy"][1])):
                return True

    def restartProgram(self, themeRestart: bool = True) -> None:
        if self.onWindowDestroy(themeRestart):
            if themeRestart: # Restart
                self.destroy()
                self.program = Program("Summing Series", (700, 580)) 
                self.program.mainloop()
            else: # Close
                self.destroy() 


class Entries(ctk.CTkFrame):
    '''Entry creation and gridding and clear entry function'''
    def __init__(self, master: Program, calcframe: ctk.CTkFrame) -> None: 
        super().__init__(calcframe) 
        self.grid(row=2, column=1, sticky="e")
        self.placeholderText = ["Common difference", "Common ratio"] 
        self.entryGen() 

    def entryGen(self) -> None: 
        self.firstTerm = ctk.CTkEntry(self) 
        self.commonDifference = ctk.CTkEntry(self)
        self.numberOfTerms = ctk.CTkEntry(self)
        self.firstTerm.grid(row=1, column=1)
        self.commonDifference.grid(row=2, column=1, pady=10)
        self.numberOfTerms.grid(row=3, column=1)

    def placeholderSwitcher(self, entry: int) -> None: 
        if entry == 1:
            self.commonDifference.configure(
                placeholder_text = self.placeholderText[0])
        else:
            self.commonDifference.configure(
                placeholder_text = self.placeholderText[1])
        self.master.focus() # Remove focus from widget to prevent placeholder 
                            # text becoming editable (focusing on main CTk 
                            # instance which acts as a dummy)

    def clearEntries(self) -> None: 
        if self.firstTerm.get() != "": 
            self.firstTerm.delete(0, ctk.END)
        if self.commonDifference.get() != "":
            self.commonDifference.delete(0, ctk.END)
        if self.numberOfTerms.get() != "":
            self.numberOfTerms.delete(0, ctk.END)
        self.refreshPlaceholderText()

    def refreshPlaceholderText(self) -> None:
        self.firstTerm.focus()
        self.commonDifference.focus()
        self.numberOfTerms.focus()
        self.master.focus() 


class Output(ctk.CTkFrame):
    '''Text box creation and gridding and text insertion function'''
    def __init__(self, master: Program, calcframe: ctk.CTkFrame) -> None:
        super().__init__(calcframe)
        self.grid(row=3, column=1, columnspan=2, sticky="n", padx=10, 
                  pady=(10, 30))
        self.grid_columnconfigure(1, weight=1)  
        self.grid_rowconfigure(1, weight=1) 
        self.outputGen()

    def outputGen(self) -> None:
        self.sumOutput = ctk.CTkTextbox(self, state="disabled", width=300, 
                                        height=200, wrap=tk.WORD) 
        self.sumOutput.grid(row=1, column=1)
    
    def insertText(self, text: str) -> None:
        # Enable text entry, insert text, disable text entry
        self.sumOutput.configure(state="normal") 
        self.sumOutput.delete(1.0, tk.END) 
        self.sumOutput.insert(1.0, text) 
        self.sumOutput.configure(state="disabled") 


class Radiobuttons(ctk.CTkFrame):
    '''Radiobutton creation and gridding'''
    def __init__(self, master: Program, calcframe: ctk.CTkFrame, 
                 entries: Entries) -> None:
        super().__init__(calcframe)
        self.grid(row=1, column=1, columnspan=2, pady=(55, 20), sticky="s")
        self.entries = entries
        self.radioButtonGen()

    def radioButtonGen(self) -> None:
        self.selection = tk.IntVar(value=1) 
        # Dynamic text switching for entry no.2
        self.arithButton = ctk.CTkRadioButton(
                        self, 
                        variable=self.selection, 
                        value=1, 
                        command=lambda: self.entries.placeholderSwitcher(1))
        self.geomButton = ctk.CTkRadioButton(
                        self, 
                        variable=self.selection, 
                        value=2, 
                        command=lambda: self.entries.placeholderSwitcher(2))
        self.arithButton.grid(row=1, column=1, padx=(0, 10))
        self.geomButton.grid(row=1, column=2)


class Buttons(ctk.CTkFrame):
    '''Button creation and gridding, clear and calculate functions and 
    error handling'''
    def __init__(self, master: Program, calcframe: ctk.CTkFrame, 
                 entries: Entries, radiobuttons: Radiobuttons, 
                 output: Output) -> None:
        super().__init__(calcframe)
        self.grid(row=2, column=2, padx=(20, 0), sticky="w")
        self.entries = entries 
        self.radiobuttons = radiobuttons
        self.output = output
        self.errors = [ 
            "An exception occured: ValueError - Ensure all fields are filled \
            and have numeric entries",
            "An exception occured: InvalidNumberOfTerms - The length of the \
            series cannot be a negative number or 0, please choose an \
            appropriate length",
            "An exception occured: OverflowError - Please reduce the value of \
            the entered integers",
            ]
        self.buttonGen()
        
    def buttonGen(self) -> None:
        self.clearButton = ctk.CTkButton(self, command=self.clear)
        self.calculateButton = ctk.CTkButton(self, command=self.calculate)
        self.clearButton.grid(row=1, column=1, pady=(0, 10))
        self.calculateButton.grid(row=2, column=1)
    
    def clear(self) -> None:
        self.entries.clearEntries()
        self.radiobuttons.arithButton.invoke() # Simulate clicking
        self.output.insertText("")

    def calculate(self) -> None:
        self.seqType = self.radiobuttons.selection.get() # 1 or 2

        try: 
            self.firstTerm = float(self.entries.firstTerm.get())
            self.commonDiffOrRatio = float(self.entries.commonDifference.get())
            self.numberOfTerms = int(self.entries.numberOfTerms.get())
            if self.seqType == 1: # Arithmetic series
                if self.numberOfTerms <= 0: 
                    self.output.insertText(self.errors[1])
                else:
                    self.sum = ((
                        self.numberOfTerms / 2) 
                        * (2 * self.firstTerm + (self.numberOfTerms - 1) \
                        * self.commonDiffOrRatio))
                    self.output.insertText(self.sum)
                    
            elif self.seqType == 2: # Geometric Series
                if self.numberOfTerms <= 0: 
                    self.output.insertText(self.errors[1])
                else:
                    if self.commonDiffOrRatio == 1:
                        self.sum = self.firstTerm * self.numberOfTerms
                    else:
                        self.sum = (
                            self.firstTerm 
                            * (1 - self.commonDiffOrRatio 
                               ** self.numberOfTerms) 
                            / (1 - self.commonDiffOrRatio))
                    self.output.insertText(self.sum)
    
        except ValueError:
            self.output.insertText(self.errors[0])
        except OverflowError:
            self.output.insertText(self.errors[2])


class FontSize(ctk.CTkFrame):
    '''Font size option menu creation'''
    def __init__(self, master: Program, sidebarframe: ctk.CTkFrame) -> None:
        super().__init__(sidebarframe)
        self.grid(row=2, column=1)
        self.master = master
        self.sizes = ["Small", 
                      "Medium", 
                      "Large",
                      ]
        self.sameSelection = "Program is already set to"
        self.fontOptionsMaker()

    def fontOptionsMaker(self) -> None:
        self.fontOptions = ctk.CTkOptionMenu(self, values=self.sizes, 
                                             command=self.changeScale)
        self.fontOptionsLabel = ctk.CTkLabel(self)
        # Default values from config.ini
        self.scaleFloat = float(self.master.cfg.get("Main", "scale"))
        self.scaleStr = ("Small" if self.scaleFloat == 0.7 else 
                        "Medium" if self.scaleFloat == 1.0 else "Large")
        self.fontOptions.set(self.scaleStr) # Set current optionbox selection
        self.fontOptions.grid(row=2, column=1)
        self.fontOptionsLabel.grid(row=1, column=1)
    
    def changeScale(self, choice: int) -> None:
        self.scaleChoice = (0.7 if self.sizes.index(choice) == 0 else 
                            1.0 if self.sizes.index(choice) == 1 else 1.3)
        # Is the user trying to switch to an already selected option? 
        self.master.cfg.read(f"{self.master.currentDir}/config.ini")
        if self.master.cfg.getfloat("Main", "scale") == self.scaleChoice:
            tk.messagebox.showinfo(message=f"{self.sameSelection} {choice}")
            return
        ctk.set_widget_scaling(self.scaleChoice)
        self.master.configUpdater(scale=self.scaleChoice)


class Appearance(ctk.CTkFrame):
    '''Options to change appearance and colour themes'''
    def __init__(self, master: Program, sidebarframe: ctk.CTkFrame) -> None:
        super().__init__(sidebarframe)
        self.grid(row=3, column=1)
        self.master = master
        self.appearances = ["light", 
                            "dark", 
                            "system"
                            ]
        self.themes = ["blue", 
                       "green", 
                       "dark-blue"
                       ]
        self.sameSelection = "Program is already set to"
        self.appearanceOptionsMaker()

    def appearanceOptionsMaker(self) -> None:
        self.appearanceOptions = ctk.CTkOptionMenu(
                                    self, 
                                    values=self.appearances, 
                                    command=self.changeAppearance)
        self.themeOptions = ctk.CTkOptionMenu(
                                    self, 
                                    values=self.themes, 
                                    command=self.changeTheme)
        self.appearanceOptionsLabel = ctk.CTkLabel(self)
        self.themeOptionsLabel = ctk.CTkLabel(self)
        # Default values from config.ini
        self.appearanceOptions.set(self.master.cfg.get("Main", "appearance"))
        self.themeOptions.set(self.master.cfg.get("Main", "theme"))
        self.appearanceOptions.grid(row=2, column=1)
        self.themeOptions.grid(row=4, column=1)
        self.appearanceOptionsLabel.grid(row=1, column=1)
        self.themeOptionsLabel.grid(row=3, column=1)

    def changeAppearance(self, choice: int) -> None: 
        self.appearanceChoice = (
                "light" if self.appearances.index(choice) == 0 else 
                "dark" if self.appearances.index(choice) == 1 else "system")
        self.master.cfg.read(f"{self.master.currentDir}/config.ini")
        if self.master.cfg.get("Main", "appearance") == self.appearanceChoice: 
            tk.messagebox.showinfo(message=f"{self.sameSelection} {choice}")
            return
        ctk.set_appearance_mode(self.appearanceChoice)
        self.master.configUpdater(appearance=self.appearanceChoice)

    def changeTheme(self, choice: int) -> None:
        self.themeChoice = "blue" if self.themes.index(choice) == 0 else \
        "green" if self.themes.index(choice) == 1 else "dark-blue"
        self.master.cfg.read(f"{self.master.currentDir}/config.ini")
        if self.master.cfg.get("Main", "theme") == self.themeChoice:
            tk.messagebox.showinfo(message=f"{self.sameSelection} {choice}")
            return
        self.master.configUpdater(theme=self.themeChoice)
        self.master.restartProgram() # Must restart to reapply theme


class FileMenu(tk.Menu):
    '''Filemenu structure creation with commands'''
    def __init__(self, master: Program) -> None:
        super().__init__(master)
        self.master = master
        self.menuLabels = ["File", 
                           "Restart", 
                           "Exit"
                           ]
        self.createFileMenu()

    def createFileMenu(self) -> None:
        # Creating main program menu
        self.menu = tk.Menu(self)
        # Creating file menu cascade
        self.fileMenu = tk.Menu(self.menu)
        self.menu.add_cascade(label=self.menuLabels[0], menu=self.fileMenu)
        # Creating commands within the file cascade
        self.fileMenu.add_command(
                            label=self.menuLabels[1], 
                            command=lambda: self.master.restartProgram())
        self.fileMenu.add_separator()
        self.fileMenu.add_command(
                            label=self.menuLabels[2], 
                            command=lambda: self.master.restartProgram(
                                                    themeRestart=False))
        # Setting main menu
        self.master.config(menu=self.menu)


class Languages(ctk.CTkFrame):
    '''Loads language jsons and switches widget text'''
    def __init__(self, 
                 master: Program, 
                 sidebarframe: ctk.CTkFrame, 
                 entries: Entries, 
                 buttons: Buttons, 
                 radiobuttons: Radiobuttons,
                 fontsize: FontSize, 
                 appearance: Appearance, 
                 filemenu: FileMenu) -> None:
        super().__init__(sidebarframe)
        self.grid(row=4, column=1)
        self.master = master
        self.entries = entries
        self.buttons = buttons
        self.radiobuttons = radiobuttons
        self.fontsize = fontsize
        self.appearance = appearance
        self.filemenu = filemenu
        
        self.translationsPath = os.path.join(self.master.currentDir, 
                                             "translations") 
        self.currentLangDb = {} 
        self.loadedLangTuple = ("",) # Aids to detect if user is switching to
                                     # the same language
        self.loadedLanguages = [] # Stores loaded language dictionaries
        self.langOptionsMaker() 

    def langOptionsMaker(self) -> None:
        self.availableLanguages = os.listdir(self.translationsPath) 
        self.availableLanguages = [jsonFile.replace(".json", "") 
                                   for jsonFile in self.availableLanguages]
        self.availableLanguages = sorted(self.availableLanguages) 
        self.langOptions = ctk.CTkOptionMenu(self, 
                                            values=self.availableLanguages, 
                                            command=self.switchLang)
        self.langOptionsLabel = ctk.CTkLabel(self)
        self.langOptions.grid(row=2, column=1)
        self.langOptionsLabel.grid(row=1, column=1)

    def switchLang(self, lang: str) -> None:
        self.langLoader(lang) 
        '''Entries'''
        self.entries.firstTerm.configure(
                        placeholder_text=self.currentLangDb["entries"][0])
        self.entries.placeholderText[0] = self.currentLangDb["entries"][1][0]
        self.entries.placeholderText[1] = self.currentLangDb["entries"][1][1]
        self.entries.placeholderSwitcher(self.radiobuttons.selection.get())
        self.entries.numberOfTerms.configure(
                        placeholder_text=self.currentLangDb["entries"][2])
        '''Buttons'''
        self.buttons.clearButton.configure(
                                    text=self.currentLangDb["buttons"][0])
        self.buttons.calculateButton.configure(
                                    text=self.currentLangDb["buttons"][1])
        '''Radiobuttons'''
        self.radiobuttons.arithButton.configure(
                                    text=self.currentLangDb["radiobuttons"][0])
        self.radiobuttons.geomButton.configure(
                                    text=self.currentLangDb["radiobuttons"][1])
        '''Fontsize optionbox and label'''
        self.fontsize.fontOptionsLabel.configure(
                                        text=self.currentLangDb["fontsize"][0])
        self.sizeIndex = self.fontsize.sizes.index(
                                            self.fontsize.fontOptions.get())
        for i, _ in enumerate(self.fontsize.sizes):
            self.fontsize.sizes[i] = self.currentLangDb["fontsize"][1][i]
        self.fontsize.fontOptions.configure(values=self.fontsize.sizes)
        self.fontsize.fontOptions.set(self.fontsize.sizes[self.sizeIndex])
        # Reuse same selection text from the array in the "langloader" key 
        self.fontsize.sameSelection = self.currentLangDb["langloader"][1]

        '''Appearance optionbox and label'''
        self.appearance.appearanceOptionsLabel.configure(
                                text=self.currentLangDb["appearance"][0][0])
        self.appearanceIndex = self.appearance.appearances.index(
                                    self.appearance.appearanceOptions.get())
        for i, _ in enumerate(self.appearance.appearances):
            self.appearance.appearances[i] = \
                                    self.currentLangDb["appearance"][0][1][i]
        self.appearance.appearanceOptions.configure(
                                            values=self.appearance.appearances)
        self.appearance.appearanceOptions.set(
                            self.appearance.appearances[self.appearanceIndex])

        self.appearance.themeOptionsLabel.configure(
                                text=self.currentLangDb["appearance"][1][0])
        self.themeIndex = self.appearance.themes.index(
                                            self.appearance.themeOptions.get())
        for i, _ in enumerate(self.appearance.themes):
            self.appearance.themes[i] = \
                                    self.currentLangDb["appearance"][1][1][i]
        self.appearance.themeOptions.configure(
                                                values=self.appearance.themes)
        self.appearance.themeOptions.set(
                                    self.appearance.themes[self.themeIndex])
        self.appearance.sameSelection = self.currentLangDb["langloader"][1]

        '''Language optionbox and label'''
        self.langOptionsLabel.configure(
                                    text=self.currentLangDb["languages"][0])
        self.langOptions.set(self.master.cfg.get("Main", "language"))

        '''Error text'''
        for i, _ in enumerate(self.buttons.errors):
            self.buttons.errors[i] = self.currentLangDb["errors"][i]
        self.buttons.calculate() # Regenerate error (if there is one), now 
                                 # with the updated language 

        '''Filemenu'''
        self.filemenu.menu.entryconfigure(self.filemenu.menuLabels[0], 
                                    label=self.currentLangDb["filemenu"][0])
        self.filemenu.fileMenu.entryconfigure(self.filemenu.menuLabels[1], 
                                    label=self.currentLangDb["filemenu"][1])
        self.filemenu.fileMenu.entryconfigure(self.filemenu.menuLabels[2], 
                                    label=self.currentLangDb["filemenu"][2])
        for i, _ in enumerate(self.filemenu.menuLabels):
            self.filemenu.menuLabels[i] = self.currentLangDb["filemenu"][i]

        '''Title and title label'''
        self.master.title(self.currentLangDb["title"][0])
        self.master.titleLabel.configure(text=self.currentLangDb["title"][0])
        
    def langLoader(self, lang: str) -> None:
        '''Handles loading and storing of language data and responds to errors 
        and repetitive inputs'''
        # If the language is already set to the language being switched to
        if self.loadedLangTuple[0] == lang:
            tk.messagebox.showinfo(
                    title=self.currentLangDb["langloader"][0], 
                    message=f"{self.currentLangDb['langloader'][1]} {lang}")
            return

        # If the required language is not loaded, load the new language and
        # switch the database
        if not any(langTuple[0] == lang for langTuple in self.loadedLanguages):
            try:
                with open(f"{self.translationsPath}/{lang.title()}.json", 
                        "r") as f: 
                    self.rawLangDb = json.load(f)
                    self.loadedLangTuple = self.langDbConfigurer(
                                                        lang, self.rawLangDb)
                    self.currentLangDb = self.loadedLangTuple[1] 
                    self.master.configUpdater(
                                            language=self.loadedLangTuple[0])
            
            # The json file is likely empty or formatted incorrectly
            except json.decoder.JSONDecodeError:
                tk.messagebox.showinfo(
                    title=self.currentLangDb["langloader"][0], 
                    message=f"{lang} {self.currentLangDb['langloader'][2]}")
                self.langOptions.set(self.loadedLangTuple[0]) 
        # Switch database to already loaded language
        else:
            self.loadedLangTuple = tuple(langTuple for langTuple 
                                         in self.loadedLanguages 
                                         if langTuple[0] == lang)
            self.currentLangDb = self.loadedLangTuple[0][1]
            self.master.configUpdater(language = self.loadedLangTuple[0][0])
            

    def langDbConfigurer(self, 
          lang: str, 
          rawLangDb: Dict[str, List[str]]) -> Tuple[str: Dict[str, List[str]]]:
        '''Make the order of arrays more logical based on hierarchy 
        (using array slicing)'''
        rawLangDb["entries"][1:3] = [rawLangDb["entries"][1:3]] 
        rawLangDb["fontsize"][1:4] = [rawLangDb["fontsize"][1:4]]
        self.values = rawLangDb["appearance"]
        self.groupedValues = [self.values[0], self.values[2:5]], [
                                            self.values[1], self.values[5:]]
        rawLangDb["appearance"] = self.groupedValues

        return (lang, rawLangDb) # Assigned to the variable loadedLangTuple 


if __name__ == "__main__": # Allows program to only run when the file is 
                           # executed as a script, allowing for modularity 
                           # and reusability
    program = Program("Summing Series", (700, 580)) 
    program.mainloop() 