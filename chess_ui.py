import time
import tkinter as tk
from tkinter import messagebox
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
from chess_engine import get_stockfish_move

#Capital letters are black pieces and lowercase letters are white pieces
UNICODE_PIECES = {
    "P": "♙", "N": "♘", "B": "♗", "R": "♖", "Q": "♕", "K": "♔",
    "p": "♟", "n": "♞", "b": "♝", "r": "♜", "q": "♛", "k": "♚",
}


class ChessRobotUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Robot Chess")

        self.board = chess.Board()
        self.selected_square = None
        self.buttons = {}

        self.above, self.touch = make_square_maps(
            xA1=X_A1,
            yA1=Y_A1,
            square=SQUARE_SIZE,
            z_above=Z_ABOVE,
            z_touch=Z_TOUCH,
            rx=RX,
            ry=RY,
            rz=RZ,
        )

        self.engine = chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH)

        self.status_label = tk.Label(root, text="Your turn: click a piece, then click destination.", font=("Arial", 12))
        self.status_label.grid(row=0, column=0, columnspan=8, pady=10)

        self.build_board()
        self.draw_board()

        send_urscript(HOST, PORT, NEUTRAL_MOVEJ)
        time.sleep(STARTUP_DELAY)

    def build_board(self):
        for row in range(8):
            for col in range(8):
                color = "#F0D9B5" if (row + col) % 2 == 0 else "#B58863"
                btn = tk.Button(
                    self.root,
                    width=4,
                    height=2,
                    font=("Arial", 24),
                    bg=color,
                    command=lambda r=row, c=col: self.on_square_click(r, c)
                )
                btn.grid(row=row + 1, column=col)
                self.buttons[(row, col)] = btn

    def draw_board(self):
        for row in range(8):
            for col in range(8):
                square = chess.square(col, 7 - row)
                piece = self.board.piece_at(square)

                text = UNICODE_PIECES.get(piece.symbol(), "") if piece else ""
                color = "#F0D9B5" if (row + col) % 2 == 0 else "#B58863"

                self.buttons[(row, col)].config(text=text, bg=color)

        if self.selected_square is not None:
            row, col = self.square_to_rowcol(self.selected_square)
            self.buttons[(row, col)].config(bg="yellow")

    def square_to_rowcol(self, square):
        col = chess.square_file(square)
        row = 7 - chess.square_rank(square)
        return row, col

    def rowcol_to_square(self, row, col):
        return chess.square(col, 7 - row)

    def on_square_click(self, row, col):
        clicked_square = self.rowcol_to_square(row, col)

        if self.selected_square is None:
            piece = self.board.piece_at(clicked_square)
            if piece is None:
                return
            if piece.color != chess.WHITE:
                return
            self.selected_square = clicked_square
            self.draw_board()
            return

        from_sq = self.selected_square
        to_sq = clicked_square
        self.selected_square = None
        self.draw_board()

        move = chess.Move(from_sq, to_sq)

        if move not in self.board.legal_moves:
            messagebox.showerror("Illegal Move", "That move is not legal.")
            return

        self.execute_human_move(move)

    def execute_human_move(self, move):
        src = chess.square_name(move.from_square).upper()
        dst = chess.square_name(move.to_square).upper()

        self.status_label.config(text=f"You played: {src} -> {dst}")
        self.root.update()

        pick_and_place_one_program(HOST, PORT, self.above, self.touch, src, dst)
        self.board.push(move)
        self.draw_board()

        time.sleep(MOVE_DELAY)

        if self.board.is_game_over():
            self.status_label.config(text=f"Game over: {self.board.result()}")
            return

        self.execute_ai_move()

    def execute_ai_move(self):
        ai_move = get_stockfish_move(self.engine, self.board, think_time_s=THINK_TIME)

        src = chess.square_name(ai_move.from_square).upper()
        dst = chess.square_name(ai_move.to_square).upper()

        self.status_label.config(text=f"Stockfish plays: {src} -> {dst}")
        self.root.update()

        pick_and_place_one_program(HOST, PORT, self.above, self.touch, src, dst)
        self.board.push(ai_move)
        self.draw_board()

        time.sleep(MOVE_DELAY)

        if self.board.is_game_over():
            self.status_label.config(text=f"Game over: {self.board.result()}")
        else:
            self.status_label.config(text="Your turn: click a piece, then click destination.")

    def close(self):
        self.engine.quit()


def run_ui():
    root = tk.Tk()
    app = ChessRobotUI(root)

    def on_close():
        app.close()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_close)
    root.mainloop()
