'''
This program assigns translations to a dictionary and writes it into a JSON file.
! This program requires the googletrans module to be installed.

Limitations: 
- When updating a JSON language file, new translations can only be APPENDED to a key's value
- Due to a bug in the googletrans module, some languages will not be translatable
- Translation to some languages result in a timeout of the Google Translate API
'''

import json
import os
import googletrans
from googletrans import Translator

translator = Translator() 

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
    "title" :        ["Summing Series"],
    "langloader":    ["Translator", "Program is already set to", "is either not available, or its JSON data is formatted incorrectly"]
}

transDict = translationsDb.copy() 

languages = googletrans.LANGUAGES
languages = {v.title(): k for k, v in languages.items()}

currentDir = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(currentDir, "translations")


def jsonUpdater(lang):
    jsonFile = os.path.join(path, f"{lang}.json")
    if not os.path.exists(jsonFile):
        print("File does not exist. Try writing a new file instead.")
        return 
    
    try:
        with open(jsonFile, "r") as f:
            jsonDict = json.load(f)

    except json.decoder.JSONDecodeError:
        print(f"{lang}'s JSON data is either formatted incorrectly, or it is empty.")
        return

    changes = {"keys": 0, "arrays": 0}
    for key in translationsDb:
        if key not in jsonDict:
            jsonDict[key] = [] # Add missing keys
            changes["keys"] += 1

        transDbLen = len(translationsDb[key])
        dataLen = len(jsonDict[key])

        if transDbLen > dataLen:
            missingItems = translationsDb[key][dataLen:] # Find all missing items in each key's array
            for i, item in enumerate(missingItems):
                transtext = translator.translate(item, dest = languages[lang], src = "en")
                missingItems[i] = transtext.text
            jsonDict[key].extend(missingItems)
            changes["arrays"] += len(missingItems)

    print(f"{lang} was updated with {changes['keys']} keys added and {changes['arrays']} array items added.")

    with open(jsonFile, "w") as f:
        newJsonDict = json.dumps(jsonDict, indent = 4)
        f.write(newJsonDict) 

def updateAll():
    langList = sorted(os.listdir(path))
    langList = [lang.replace(".json", "") for lang in langList]
    for lang in langList:
        jsonUpdater(lang)

def jsonWriter(lang):
    jsonFile = os.path.join(path, f"{lang}.json")
    
    if not os.path.exists(jsonFile):
        open(f"{path}/{lang}.json", "x")

    if os.path.getsize(jsonFile) > 0:
        print(f"Data appears to already exist in {lang}.json. You might want to try updating it instead.")
        return

    for key in translationsDb:
        for i, text in enumerate(translationsDb[key]):
            if lang != "en":

                try:
                    transtext = translator.translate(translationsDb[key][i], dest = languages[lang], src = "en")
                except TypeError or TimeoutError:
                    print(f"Due to a bug with the googletrans module, translation to some languages such as {lang} result in incomplete translation. Sorry.")
                    with open(jsonFile, "w") as f:
                        f.truncate(0)
                    return

                transDict[key][i] = transtext.text
            else:
                transDict[key][i] = text

        newJsonDict = json.dumps(transDict, indent = 4)

        with open(f"{path}/{lang}.json", "w") as f: 
            f.write(newJsonDict)
            
    print(f"{lang} translations are complete")

def onStart():
    updateAllChoice = True if input(f"Do you wish to update all language JSONs in {path}? (Y/n): ").upper() in ["Y", "Yes"] else False
    if updateAllChoice:
        updateAll()
        return

    print("\nRefer to the values of langCodes.json for the following input")
    lang = str(input("Enter the destination language (e.g. French): ")).title()
    if lang not in languages.keys():
        print("\nInvalid language\n")
        return
            
    choice = str(input(f"\nEnter 1 to update {lang}'s existing json file.\nEnter 2 to write new translations into {lang}.json (file will be created if it doesn't exist)\n"))
    if choice == "1":
        jsonUpdater(lang)
    elif choice == "2":
        jsonWriter(lang)
    else:
        print("\nEnter either 1 or 2")

onStart()