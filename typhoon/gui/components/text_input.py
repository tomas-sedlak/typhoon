import tkinter as tk
from colors import BG_COLOR_SECONDARY, FG_COLOR

class TextInput(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=BG_COLOR_SECONDARY, padx=12, pady=8)
        
        self.entry =  tk.Entry(self, bg=BG_COLOR_SECONDARY, fg=FG_COLOR, font="Helvetica 16", relief="flat")
        self.entry.pack()

    def get(self):
        return self.entry.get()