import tkinter as tk
import chess

square_size = 70
window_size = square_size * 8
light_square_color = "#eeeed2"
dark_square_color = "#769656"
piece_images = {}

canvas = tk.Canvas(width=window_size, height=window_size)
canvas.pack()

def load_pieces():
    for piece_type in ("p", "r", "n", "b", "q", "k"):
        for color in ("white", "black"):
            filename = f"images/{color}_{piece_type}.png"
            image = tk.PhotoImage(file=filename)

            piece_type = piece_type.upper() if color == "white" else piece_type.lower()
            piece_images[piece_type] = image

def draw_square(row, col, color):
    x1 = (col * square_size)
    y1 = (row * square_size)
    x2 = x1 + square_size
    y2 = y1 + square_size
    canvas.create_rectangle(x1, y1, x2, y2, fill=color, width=0)

def draw_board():
    for row in range(8):
        for col in range(8):
            color = light_square_color if (row + col) % 2 == 0 else dark_square_color
            draw_square(row, col, color)

def draw_pieces(board):
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece is not None:
            rank, file = chess.square_name(square)
            row = ord(rank) - 97
            col = int(file) - 1
            x = (col * square_size) + square_size // 2
            y = (row * square_size) + square_size // 2
            piece_name = piece.symbol()
            image = piece_images.get(piece_name)
            if image:
                canvas.create_image(x, y, image=image)

def draw_chessboard(board):
    canvas.delete("all")
    draw_board()
    draw_pieces(board)
    canvas.update()
    canvas.update_idletasks()

load_pieces()