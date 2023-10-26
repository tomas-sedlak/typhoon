import tkinter as tk
import chess
import chess.engine

width, height = 600, 600
board_offset_x, board_offset_y = 60, 60
size = 60
move_from = None

canvas = tk.Canvas(width=width, height=height)
canvas.pack()

board = chess.Board()

levels = {
    "1": {"skill": 3, "depth": 1, "elo": 800},
    "2": {"skill": 6, "depth": 2, "elo": 1000},
    "3": {"skill": 9, "depth": 3, "elo": 1400},
    "4": {"skill": 11, "depth": 4, "elo": 1600},
    "5": {"skill": 14, "depth": 6, "elo": 1700},
    "6": {"skill": 17, "depth": 8, "elo": 1900},
    "7": {"skill": 20, "depth": 10, "elo": 2000},
    "8": {"skill": 20, "depth": 12, "elo": 2200}
}

images = {
    "P": tk.PhotoImage(file="pieces/p_white.png"),
    "N": tk.PhotoImage(file="pieces/n_white.png"),
    "B": tk.PhotoImage(file="pieces/b_white.png"),
    "R": tk.PhotoImage(file="pieces/r_white.png"),
    "Q": tk.PhotoImage(file="pieces/q_white.png"),
    "K": tk.PhotoImage(file="pieces/k_white.png"),
    "p": tk.PhotoImage(file="pieces/p_black.png"),
    "n": tk.PhotoImage(file="pieces/n_black.png"),
    "b": tk.PhotoImage(file="pieces/b_black.png"),
    "r": tk.PhotoImage(file="pieces/r_black.png"),
    "q": tk.PhotoImage(file="pieces/q_black.png"),
    "k": tk.PhotoImage(file="pieces/k_black.png"),
}

level = 5
engine_path = "./stockfish/stockfish.exe"
engine = chess.engine.SimpleEngine.popen_uci(engine_path)
engine.configure({"Skill level": levels[level]["skill"]})
limit = chess.engine.Limit(depth=levels[level]["depth"])

def pos_to_grid(x, y):
    return (x - board_offset_x) // size, (y - board_offset_y) // size

def grid_to_uci(grid):
    return chr(ord("a") + grid[0]) + str(8 - grid[1])

def pos_to_uci(x, y):
    return grid_to_uci(pos_to_grid(x, y))

def valid_move(uci):
    move = chess.Move.from_uci(uci)
    return move in board.legal_moves

def handle_rect(event):
    global move_from, move_to

    if board.turn == chess.WHITE:
        x = event.x
        y = event.y
        uci = pos_to_uci(x, y)

        if not move_from:
            move_from = uci
            draw_gui()
            return
        
        if move_from != uci:
            move = move_from + uci

            if valid_move(move):
                board.push_uci(move)
                draw_pieces()
                draw_gui()

                board.push(engine.play(board, limit).move)
                draw_pieces()
                draw_gui()
            else:
                print("Invalid move")

            move_from = None

def draw_board(color_dark, color_light):
    x, y = board_offset_x, board_offset_y
    for i in range(8):
        x = board_offset_x

        canvas.create_rectangle(x - size // 2, y, x, y + size)
        canvas.create_text(x - size // 4, y + size // 2, text=(8 - i))

        for j in range(8):
            rect = canvas.create_rectangle(x, y, x + size, y + size, fill=color_dark)
            canvas.tag_bind(rect, "<Button-1>", handle_rect)

            if i == 7:
                canvas.create_rectangle(x, y + size + size // 2, x + size, y + size)
                canvas.create_text(x + size // 2, y + size + size // 4, text=chr(ord("A") + j))

            color_dark, color_light = color_light, color_dark
            x += size
        
        color_dark, color_light = color_light, color_dark
        y += size

    canvas.update()

def draw_pieces():
    canvas.delete("piece")

    rows = board.board_fen().split("/")
    x, y = board_offset_x, board_offset_y

    for row in rows:
        x = board_offset_x

        for piece in row:
            if piece.isdigit():
                x += int(piece) * size
                continue
            
            piece = canvas.create_image(x + size // 2, y + size // 2, image=images[piece], tags=("piece"))
            canvas.tag_bind(piece, "<Button-1>", handle_rect)

            x += size

        y += size

    canvas.update()

def draw_gui():
    turn = "White" if board.turn else "Black"
    canvas.itemconfig(turn_label, text=f"Turn: {turn}")
    
    if board.is_check():
        canvas.itemconfig(check_label, text="Check!!!")
    else:
        canvas.itemconfig(check_label, text="")

    canvas.update()

draw_board("green", "white")
draw_pieces()

turn_label = canvas.create_text(board_offset_x, board_offset_y // 2, text="Turn: White")
check_label = canvas.create_text(width // 2, board_offset_y // 2, font=("Helvetica", 20), fill="red")

canvas.mainloop()