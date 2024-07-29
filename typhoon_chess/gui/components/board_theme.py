import tkinter as tk
import json
from constants import BG_COLOR, FG_COLOR

import os
dirname = os.path.dirname(__file__)

class BoardTheme(tk.Frame):
    def __init__(self, master, index, data, on_press, cols=5):
        super().__init__(master, bg=BG_COLOR, cursor="hand2")

        self.index = index

        # Needed to wrap canvas with frame because highligh bugged when only on canvas
        self.canvas_wrapper = tk.Frame(self, bg=BG_COLOR, highlightthickness=4, highlightbackground=BG_COLOR)
        self.canvas_wrapper.pack()

        size = 120
        size_half = size // 2
        self.canvas = tk.Canvas(self.canvas_wrapper, width=size, height=size, highlightthickness=0)
        self.canvas.create_rectangle(0, 0, size_half, size_half, fill=data["light"], width=0)
        self.canvas.create_rectangle(size_half, 0, size, size_half, fill=data["dark"], width=0)
        self.canvas.create_rectangle(0, size_half, size_half, size, fill=data["dark"], width=0)
        self.canvas.create_rectangle(size_half, size_half, size, size, fill=data["light"], width=0)
        self.canvas.pack()

        self.label = tk.Label(self, text=data["name"], font="Helvetica 16 italic", bg=BG_COLOR, fg=FG_COLOR)
        self.label.pack(pady=(4, 0))

        click = lambda event: [on_press(), self.select()]
        self.bind("<Button-1>", click)
        self.canvas.bind("<Button-1>", click)
        self.label.bind("<Button-1>", click)

        col = index % cols
        row = index // cols
        self.grid(row=row, column=col, padx=(0, 8 if col < cols else 0), pady=8)

    def select(self, event=None):
        path = os.path.join(dirname, "../../config.json")

        with open(path, "r") as jsonFile:
            data = json.load(jsonFile)

        data["board_theme_index"] = self.index

        with open(path, "w") as jsonFile:
            json.dump(data, jsonFile)

        self.canvas_wrapper.configure(highlightbackground="yellow")
        self.label.configure(fg="yellow")

    def deselect(self, event=None):
        self.canvas_wrapper.configure(highlightbackground=BG_COLOR)
        self.label.configure(fg=FG_COLOR)