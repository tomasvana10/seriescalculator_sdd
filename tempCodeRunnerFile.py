s))

    def whenFocused(self, entry): # Controls what happens when the user focuses on the entry (above bindings provide the functionality)
        if entry.get() in self.entryTempText: