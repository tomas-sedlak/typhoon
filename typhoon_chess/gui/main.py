import tkinter as tk
import os
dirname = os.path.dirname(__file__)

from pages.play import Play
from pages.home import Home
from pages.board_themes import BoardThemes
from constants import BG_COLOR, FG_COLOR_SECONDARY

class TyphoonChessGui(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Typhoon Chess")
        self.config(bg=BG_COLOR)
        self.minsize(800, 480)
        # icon = tk.PhotoImage(file=)
        # self.iconphoto(True, icon)

        self.typhoon_label = tk.Label(self, text="Typhoon, v1.0.0", font="Helvetica 10", bg=BG_COLOR, fg=FG_COLOR_SECONDARY, padx=8, pady=8)
        self.typhoon_label.place(relx=1, rely=1, anchor="se")

        self.frames = {}

        home = Home(self, self)
        home.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.frames["home"] = home

        play = Play(self, self)
        play.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.frames["play"] = play
        
        themes = BoardThemes(self, self)
        themes.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.frames["themes"] = themes

        self.show_frame("home")

    def show_frame(self, cont):
        frame = self.frames[cont]
        if cont == "play": frame.start()
        frame.tkraise()
        self.typhoon_label.tkraise()

if __name__ == "__main__":
    app = TyphoonChessGui()
    app.mainloop()