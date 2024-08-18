import json
import tkinter as tk
from components import Button
from colors import BG_COLOR, FG_COLOR_SECONDARY
from config import ICONS_DIR_PATH, PAGES_DIR_PATH

class TyphoonGui(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Typhoon GUI")
        self.config(bg=BG_COLOR)
        self.minsize(800, 480)
        icon = tk.PhotoImage(file=ICONS_DIR_PATH / "icon.png")
        self.iconphoto(True, icon)

        self.typhoon_label = tk.Label(self, text="Typhoon, v1.0.0", font="Helvetica 10", bg=BG_COLOR, fg=FG_COLOR_SECONDARY, padx=8, pady=8)
        self.typhoon_label.place(relx=1, rely=1, anchor="se")

        pages = []
        for page in PAGES_DIR_PATH.iterdir():
            config = page / "config.json"
            if not config.is_file(): continue

            f = open(config)
            data = json.load(f)
            pages.append(data)

        # self.frames = {}

        # for page in ((Home, "home"), (Play, "play"), (BoardThemes, "themes"), (Paint, "paint")):
        #     frame = page[0](self, self)
        #     frame.place(relx=0, rely=0, relwidth=1, relheight=1)
        #     self.frames[page[1]] = frame

        # self.show_frame("home")

    def show_frame(self, cont):
        frame = self.frames[cont]
        if cont == "play": frame.start()
        frame.tkraise()
        self.typhoon_label.tkraise()

if __name__ == "__main__":
    app = TyphoonGui()
    app.mainloop()