import tkinter as tk
from constants import BG_COLOR_SECONDARY, FG_COLOR

import os
dirname = os.path.dirname(__file__)

class Button(tk.Frame):
    def __init__(self, master, text=None, icon_left=None, icon_right=None, command=None):
        super().__init__(master, bg=BG_COLOR_SECONDARY, padx=16, pady=8, cursor="hand2")

        self.columnconfigure(1, weight=1)

        if command: self.bind("<Button-1>", command)

        if icon_left:
            path = os.path.join(dirname, f"../../assets/icons/{icon_left}.png")
            self.icon_left_image = tk.PhotoImage(file=path)
            icon_label = tk.Label(self, image=self.icon_left_image, bg=BG_COLOR_SECONDARY)
            icon_label.grid(row=0, column=0, padx=(0, 4))
            if command: icon_label.bind("<Button-1>", command)

        if text:
            label = tk.Label(self, text=text, font="Helvetica 16", bg=BG_COLOR_SECONDARY, fg=FG_COLOR)
            label.grid(row=0, column=1, sticky="w")
            if command: label.bind("<Button-1>", command)

        if icon_right:
            path = os.path.join(dirname, f"../../assets/icons/{icon_right}.png")
            self.icon_right_image = tk.PhotoImage(file=path)
            icon_label = tk.Label(self, image=self.icon_right_image, bg=BG_COLOR_SECONDARY)
            icon_label.grid(row=0, column=2, padx=(4, 0))
            if command: icon_label.bind("<Button-1>", command)
        