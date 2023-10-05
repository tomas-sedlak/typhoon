# from typhoon import Typhoon
import chess
import chess.engine

# typhoon = Typhoon(port="COM4")

engine_path = "./stockfish/stockfish.exe"
engine = chess.engine.SimpleEngine.popen_uci(engine_path)
engine.configure({"Skill level": 1})
limit = chess.engine.Limit(time=1)

board = chess.Board()


def player_move(old_board, new_board):
    move_from, move_to = "", ""
    hrac_urobil_tah = 0

    for row in range(8):
        for col in range(8):
            if old_board[row][col] != new_board[row][col]:
                if new_board[row][col] == 0:
                    hrac_urobil_tah = 1
                    move_from = chr(col + 97) + str(8 - row)
                else:
                    move_to = chr(col + 97) + str(8 - row)

    move = chess.Move.from_uci(move_from + move_to)
    if hrac_urobil_tah == 1:
        print('Hrac:', move)

    return move


def typhoon_move(engine_move):
    col_from = ord(engine_move[0]) - 96
    row_from = engine_move[1]
    col_to = ord(engine_move[2]) - 96
    row_to = engine_move[3]
    print(col_from)


move = player_move(
    [[1, 1, 1, 1, 1, 1, 1, 1, 1],
     [1, 1, 1, 1, 1, 1, 1, 1, 1],
     [0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0],
     [1, 1, 1, 1, 1, 1, 1, 1, 1],
     [1, 1, 1, 1, 1, 1, 1, 1, 1]],
    [[1, 1, 1, 1, 1, 1, 1, 1, 1],
     [1, 1, 1, 1, 1, 1, 1, 1, 1],
     [0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 1, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0],
     [1, 1, 1, 1, 1, 0, 1, 1, 1],
     [1, 1, 1, 1, 1, 1, 1, 1, 1]]
)
board.push(move)


def get_outcome():
    winner = board.outcome().winner
    if winner == chess.WHITE:
        print("White won!")
    elif winner == chess.BLACK:
        print("Black won!")
    else:
        print("Draw!")


while not board.is_game_over():
    turn = board.turn
    if turn == chess.WHITE:
        move = chess.Move.from_uci(input("Tvoj tah: "))
        board.push(move)
    elif turn == chess.BLACK:
        engine_move = engine.play(board, limit).move
        board.push(engine_move)
        print(board.uci(engine_move))
        typhoon_move(board.uci(engine_move))

    print(board, "\n")

get_outcome()
engine.quit()
