'''
This program assigns translations to a dictionary and writes it into a json file.
To use this program, change the langAcronym your desired language abbreviation.
! This program requires the googletrans module to be installed.
'''

import json
import googletrans
from googletrans import Translator
import os

translator = Translator() # Translator instance

translationsDb = { # Text within the program
    "entries" :      ["First term", "Common difference", "Common ratio", "Number of terms"],
    "buttons" :      ["Clear", "Calculate"],
    "radiobuttons" : ["Arithmetic Series", "Geometric Series"],
    "fontsize" :     ["Size", "Small", "Medium", "Large"],
    "appearance" :   ["Appearance", "Themes", "Light", "Dark", "System", "Blue", "Green", "Dark blue"],
    "languages" :    ["Languages"],
    "errors" :       ["An exception occured: ValueError - Ensure all fields are filled and have numeric entries",
                      "An exception occured: InvalidNumberOfTerms - The length of the series cannot be a negative number or 0, please choose an appropriate length",
                      "An exception occured: OverflowError - Please reduce the value of the entered integers"],
    "filemenu" :     ["File", "Restart", "Exit"], 
    "title" :        ["Summing Series"]
}

transDict = translationsDb.copy() 
languages = googletrans.LANGUAGES

currentDir = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(currentDir, "translations")

langAcronym = "fr" 

for key in translationsDb:
    for i, text in enumerate(translationsDb[key]):
        if langAcronym != "en":
            transtext = translator.translate(translationsDb[key][i], dest = langAcronym, src = "en")
            transDict[key][i] = transtext.text
        else:
            transDict[key][i] = text

jsonDict = json.dumps(transDict, indent = 4)
lang = languages[langAcronym].title()
lang = lang.replace(".json", "")

with open(f"{path}/{lang}.json", "w") as transfile: 
    transfile.write(jsonDict)