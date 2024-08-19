import tkinter as tk

from components import Button, TextInput
from constants import BG_COLOR, FG_COLOR_SECONDARY

class Paint(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG_COLOR)

        self.current_drawing = []
        self.dragging = False
        self.last_x, self.last_y = 0, 0

        content = tk.Frame(self, bg=BG_COLOR)
        content.place(relx=0.5, rely=0.5, width=600, anchor="center")

        buttons_wrapper = tk.Frame(content, bg=BG_COLOR)
        buttons_wrapper.pack(fill="x", pady=(0, 16))

        go_back = lambda event: controller.show_frame("home")
        back_button = Button(buttons_wrapper, text="Back", icon_left="arrow_back", command=go_back)
        back_button.pack(side="left")

        send_button = Button(buttons_wrapper, text="Send", icon_left="send")
        send_button.pack(side="right")

        clear_button = Button(buttons_wrapper, text="Clear", icon_left="close", command=self.clear)
        clear_button.pack(side="right", padx=(0, 8))

        width, height = 600, 400
        self.canvas = tk.Canvas(content, width=width, height=height, bg="#fff", highlightthickness=0)
        self.canvas.pack()

        self.canvas.bind("<ButtonPress-1>", self.press)
        self.canvas.bind("<ButtonRelease-1>", self.release)
        self.canvas.bind("<Motion>", self.motion)

        options_wrapper = tk.Frame(content, bg=BG_COLOR)
        options_wrapper.pack(fill="x", pady=(16, 0))

        text_input_label = tk.Label(options_wrapper, text="Name:", font="Helvetica 16", bg=BG_COLOR, fg=FG_COLOR_SECONDARY)
        text_input_label.pack(side="left", padx=(0, 4))

        self.text_input = TextInput(options_wrapper)
        self.text_input.pack(side="left", padx=(0, 8))

        save_button = Button(options_wrapper, text="Save", icon_left="save", command=self.save)
        save_button.pack(side="left", padx=(0, 16))

        open_button = Button(options_wrapper, text="Open", icon_left="folder_open")
        open_button.pack(side="left")

    def press(self, event):
        self.dragging = True
        self.last_x, self.last_y = event.x, event.y

    def release(self, event):
        self.dragging = False

    def motion(self, event):
        if not self.dragging: return
        self.current_drawing.append(f"{event.x} {event.y}")
        self.canvas.create_line(event.x, event.y, self.last_x, self.last_y, width=2)
        self.last_x, self.last_y = event.x, event.y

    def clear(self, event):
        self.canvas.delete("all")

    def save(self, event):
        name = self.text_input.get()
        
        with open(f"{name}.txt", "w") as f:
            f.write(" ".join(self.current_drawing))