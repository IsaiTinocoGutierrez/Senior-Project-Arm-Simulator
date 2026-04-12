import time
import chess
import chess.engine

from config import (
    HOST,
    PORT,
    NEUTRAL_MOVEJ,
    STARTUP_DELAY,
    MOVE_DELAY,
    X_A1,
    Y_A1,
    SQUARE_SIZE,
    Z_ABOVE,
    Z_TOUCH,
    RX,
    RY,
    RZ,
    STOCKFISH_PATH,
    THINK_TIME,
)
from robot_comm import send_urscript
from board_mapping import make_square_maps
from robot_moves import pick_and_place_one_program
from chess_engine import get_stockfish_move, parse_uci_move


def main():
    send_urscript(HOST, PORT, NEUTRAL_MOVEJ)
    time.sleep(STARTUP_DELAY)

    above, touch = make_square_maps(
        xA1=X_A1,
        yA1=Y_A1,
        square=SQUARE_SIZE,
        z_above=Z_ABOVE,
        z_touch=Z_TOUCH,
        rx=RX,
        ry=RY,
        rz=RZ,
    )

    board = chess.Board()

    with chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH) as engine:
        print("Stockfish connected. You are White. Enter moves like e2e4, g1f3, etc.")

        while not board.is_game_over():
            uci = input("Your move (uci): ").strip().lower()

            human_move, error = parse_uci_move(uci, board)
            if error:
                print(error)
                continue

            src = chess.square_name(human_move.from_square).upper()
            dst = chess.square_name(human_move.to_square).upper()
            print(f"Robot executes YOU: {src} -> {dst}")
            pick_and_place_one_program(HOST, PORT, above, touch, src, dst)

            board.push(human_move)
            print(board)
            time.sleep(MOVE_DELAY)

            if board.is_game_over():
                break

            ai_move = get_stockfish_move(engine, board, think_time_s=THINK_TIME)
            ai_uci = ai_move.uci()
            print(f"Stockfish plays: {ai_uci}")

            ai_src = chess.square_name(ai_move.from_square).upper()
            ai_dst = chess.square_name(ai_move.to_square).upper()
            print(f"Robot executes AI: {ai_src} -> {ai_dst}")
            pick_and_place_one_program(HOST, PORT, above, touch, ai_src, ai_dst)

            board.push(ai_move)
            print(board)
            time.sleep(MOVE_DELAY)

        print("Game over:", board.result())


if __name__ == "__main__":
    main()