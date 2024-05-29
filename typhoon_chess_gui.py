import tkinter as tk
import chess

square_size = 70
padding_x, padding_y = 50, 100
light_square_color = "#eeeed2"
dark_square_color = "#769656"
font = ("Arial", 12, "bold")
text_offset = 15

piece_images = {}

# Count dynamic sizes
board_width = square_size * 8
window_width = board_width + 2 * padding_x
board_height = square_size * 8
window_height = board_height + 2 * padding_y

# Setup tkinter Canvas
canvas = tk.Canvas(width=window_width, height=window_height)
canvas.pack()

turn_label = tk.Label(canvas, font=("Arial", 24))
turn_label.place(x = window_width / 2, y = padding_y / 2, anchor="center")

message_label = tk.Label(canvas, font=("Arial", 24))
message_label.place(x = window_width / 2, y = window_height - padding_y / 2, anchor="center")

def load_pieces():
    for piece_type in ("p", "r", "n", "b", "q", "k"):
        for color in ("white", "black"):
            filename = f"images/{color}_{piece_type}.png"
            image = tk.PhotoImage(file=filename)

            piece_type = piece_type.upper() if color == "white" else piece_type.lower()
            piece_images[piece_type] = image

def draw_square(row, col, color):
    x1 = (col * square_size) + padding_x
    y1 = (row * square_size) + padding_y
    x2 = x1 + square_size
    y2 = y1 + square_size
    canvas.create_rectangle(x1, y1, x2, y2, fill=color, width=0)

def draw_board():
    for row in range(8):
        for col in range(8):
            color = light_square_color if (row + col) % 2 == 0 else dark_square_color
            draw_square(row, col, color)

    # Draw numbers
    for i in range(8):
        number = str(i + 1)
        # Top
        canvas.create_text((i + 0.5) * square_size + padding_x, padding_y - text_offset, text=number, font=font)
        # Bottom
        canvas.create_text((i + 0.5) * square_size + padding_x, board_height + padding_y + text_offset, text=number, font=font)

    # Draw letters
    for i in range(8):
        letter = chr(65 + i)  # Convert number to uppercase letter (A-H)
        # Left
        canvas.create_text(padding_x - text_offset, (i + 0.5) * square_size + padding_y, text=letter, font=font)
        # Right
        canvas.create_text(board_width + padding_x + text_offset, (i + 0.5) * square_size + padding_y, text=letter, font=font)

def draw_pieces(board):
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece is not None:
            rank, file = chess.square_name(square)
            row = ord(rank) - 97
            col = int(file) - 1
            x = (col * square_size) + square_size // 2 + padding_x
            y = (row * square_size) + square_size // 2 + padding_y
            piece_name = piece.symbol()
            image = piece_images.get(piece_name)
            if image:
                canvas.create_image(x, y, image=image)

def set_turn(turn, color="black"):
    turn_label.config(text=turn, fg=color)
    canvas.update()

def set_message(message, color="black"):
    message_label.config(text=message, fg=color)
    canvas.update()

def draw(board):
    canvas.delete("all")
    draw_board()
    draw_pieces(board)
    canvas.update()
    canvas.update_idletasks()

load_pieces()