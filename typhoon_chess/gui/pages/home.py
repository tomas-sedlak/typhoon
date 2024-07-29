import tkinter as tk

from components import Button
from constants import BG_COLOR, FG_COLOR, FG_COLOR_SECONDARY

class Home(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG_COLOR)

        content = tk.Frame(self, bg=BG_COLOR)
        content.place(relx=0.5, rely=0.5, width=300, anchor="center")

        title = tk.Label(content, text="Typhoon Chess", font="Helvetica 24 bold", bg=BG_COLOR, fg=FG_COLOR)
        title.pack()

        subtitle = tk.Label(content, text="AI powered robotic arm", font="Helvetica 12", bg=BG_COLOR, fg=FG_COLOR_SECONDARY)
        subtitle.pack(pady=(0, 24))

        go_play = lambda event: controller.show_frame("play")
        play_button = Button(content, text="Play", icon_left="play_circle", command=go_play)
        play_button.pack(fill="x", pady=(0, 8))

        go_themes = lambda event: controller.show_frame("themes")
        themes_button = Button(content, text="Board Themes", icon_left="grid_view", command=go_themes)
        themes_button.pack(fill="x")