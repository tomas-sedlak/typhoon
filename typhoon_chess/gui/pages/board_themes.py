import tkinter as tk
import json
import os

from components.button import Button
from components.board_theme import BoardTheme
from constants import BG_COLOR, FG_COLOR

dirname = os.path.dirname(__file__)

class BoardThemes(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG_COLOR)

        content = tk.Frame(self, bg=BG_COLOR)
        content.place(relx=0.5, rely=0.5, anchor="center")

        title = tk.Label(content, text="Select board theme", font="Helvetica 24 bold", bg=BG_COLOR, fg=FG_COLOR)
        title.pack(pady=(0, 24))

        go_back = lambda event: controller.show_frame("home")
        back_button = Button(content, text="Back", icon_left="arrow_back", command=go_back)
        back_button.place(x=0, y=0)

        path = os.path.join(dirname, "../../assets/board_colors.json")
        data = json.load(open(path, "r"))

        config_path = os.path.join(dirname, "../../config.json")
        config_data = json.load(open(config_path, "r"))
        selected_index = config_data["board_theme_index"]

        def on_press(event=None):
            for item in grid_frame.winfo_children():
                item.deselect()

        grid_frame = tk.Frame(content, bg=BG_COLOR)
        grid_frame.pack()

        for index, item in enumerate(data):
            board_theme = BoardTheme(grid_frame, index, item, on_press)
            if index == selected_index:
                board_theme.select()