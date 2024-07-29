import tkinter as tk
import chess
import chess.engine
import json
import tk_async_execute as tae

import os
dirname = os.path.dirname(__file__)

from components import Button
from constants import BG_COLOR, FG_COLOR

class Play(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG_COLOR)

        self.piece_images = {}
        self.load_pieces()

        content = tk.Frame(self, bg=BG_COLOR)
        content.place(relx=0.5, rely=0.5, anchor="center")

        title = tk.Label(content, text="Chess game", font="Helvetica 24 bold", bg=BG_COLOR, fg=FG_COLOR)
        title.pack(pady=(0, 24))

        go_back = lambda event: controller.show_frame("home")
        back_button = Button(content, text="Back", icon_left="arrow_back", command=go_back)
        back_button.place(x=0, y=0)

        self.rect_size = 64
        self.canvas_size = self.rect_size * 8
        self.canvas = tk.Canvas(content, width=self.canvas_size, height=self.canvas_size, highlightthickness=0)
        self.canvas.pack()

        tae.start()

    def load_pieces(self):
        for piece_type in ("p", "r", "n", "b", "q", "k"):
            for color in ("w", "b"):
                filename = os.path.join(dirname, f"../../assets/pieces/{color}{piece_type}.png")
                image = tk.PhotoImage(file=filename)

                piece_name = piece_type.upper() if color == "w" else piece_type.lower()
                self.piece_images[piece_name] = image

    def load_theme(self):
        config_path = os.path.join(dirname, "../../config.json")
        config_data = json.load(open(config_path, "r"))

        themes_path = os.path.join(dirname, "../../assets/board_themes.json")
        themes_data = json.load(open(themes_path, "r"))

        board_theme_index = config_data["board_theme_index"]
        theme = themes_data[board_theme_index]

        self.light_color = theme["light"]
        self.dark_color = theme["dark"]

    def draw_board(self):
        for row in range(8):
            for col in range(8):
                color = self.light_color if (row + col) % 2 == 0 else self.dark_color
                self.canvas.create_rectangle(col * self.rect_size, row * self.rect_size, (col + 1) * self.rect_size, (row + 1) * self.rect_size, fill=color, width=0)

    def draw_pieces(self):
        for square in chess.SQUARES:
            piece = self.board.piece_at(square)
            if piece is not None:
                row = 7 - chess.square_rank(square)
                col = chess.square_file(square)
                x = (col * self.rect_size) + self.rect_size // 2
                y = (row * self.rect_size) + self.rect_size // 2
                piece_name = piece.symbol()
                image = self.piece_images.get(piece_name)
                if image:
                    self.canvas.create_image(x, y, image=image)

    async def main(self):
        path = os.path.join(dirname, "../../../stockfish/stockfish.exe")
        transport, engine = await chess.engine.popen_uci(path)

        while not self.board.is_game_over():
            result = await engine.play(self.board, chess.engine.Limit(time=0.1))
            self.board.push(result.move)
            print(self.board)
            self.draw_pieces()

        await engine.quit()

    def start(self):
        self.board = chess.Board()
        tae.async_execute(self.main(), wait=False, visible=False, pop_up=False)
        self.load_theme()
        self.draw_board()
        self.draw_pieces()