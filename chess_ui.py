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

#Capital letters are black pieces and lowercase letters are white pieces.
UNICODE_PIECES = {
    "p": "♙", "n": "♘", "b": "♗", "r": "♖", "q": "♕", "k": "♔",
    "P": "♟", "N": "♞", "B": "♝", "R": "♜", "Q": "♛", "K": "♚",
}
PIECE_NAMES = {
    "p": "White pawn",
    "n": "White knight",
    "b": "White bishop",
    "r": "White rook",
    "q": "White queen",
    "k": "White king",
    "P": "Black pawn",
    "N": "Black knight",
    "B": "Black bishop",
    "R": "Black rook",
    "Q": "Black queen",
    "K": "Black king",
}


class ChessRobotUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Robot Chess")
        self.root.resizable(True, True)

        self.board = chess.Board()
        self.selected_square = None
        self.captured_white = []
        self.captured_black = []

        self.move_log = []
        self.buttons = {}
        self.root.geometry("900x600")
        for i in range(8):
            self.root.grid_rowconfigure(i + 1, weight=1)
            self.root.grid_columnconfigure(i, weight=1)

        # Allow right panel (reset button area) to resize too
        self.root.grid_columnconfigure(8, weight=1)

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

        self.status_label = tk.Label(
            root,
            text="Your turn: click a piece, then click destination.",
            font=("Arial", 12)
        )
        self.status_label.grid(row=0, column=0, columnspan=8, pady=10)

        self.build_board()
        self.draw_board()

        self.reset_button = tk.Button(
            root,
            text="Reset Game",
            font=("Arial", 12),
            command=self.reset_game
        )
        self.reset_button.grid(row=1, column=8, rowspan=2, padx=10)

        self.captured_white_label = tk.Label(
            root,
            text="Captured White: ",
            font=("Arial", 12),
            anchor="w",
            justify="left"
        )
        self.captured_white_label.grid(row=3, column=8, padx=10, sticky="nw")

        self.captured_black_label = tk.Label(
            root,
            text="Captured Black: ",
            font=("Arial", 12),
            anchor="w",
            justify="left"
        )
        self.captured_black_label.grid(row=4, column=8, padx=10, sticky="nw")

        self.move_log_title = tk.Label(
            root,
            text="Move Log:",
            font=("Arial", 12, "bold"),
            anchor="w",
            justify="left"
        )
        self.move_log_title.grid(row=5, column=8, padx=10, pady=(10, 0), sticky="nw")

        # Frame to hold text + scrollbar
        self.move_log_frame = tk.Frame(root)
        self.move_log_frame.grid(row=6, column=8, rowspan=3, padx=10, pady=5, sticky="nsew")

        # Scrollbar
        self.move_log_scrollbar = tk.Scrollbar(self.move_log_frame)

        # Text widget
        self.move_log_text = tk.Text(
            self.move_log_frame,
            width=28,
            height=15,
            font=("Arial", 10),
            state="disabled",
            wrap="word",
            yscrollcommand=self.move_log_scrollbar.set
        )

        # Link scrollbar to text
        self.move_log_scrollbar.config(command=self.move_log_text.yview)

        # resize scrollbar
        self.root.grid_rowconfigure(6, weight=1)
        self.root.grid_columnconfigure(8, weight=1)

        # Layout inside frame
        self.move_log_text.pack(side="left", fill="both", expand=True)
        self.move_log_scrollbar.pack(side="right", fill="y")
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
                btn.grid(row=row + 1, column=col, sticky="nsew")
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

    def format_move_entry(self, move):
        piece = self.board.piece_at(move.from_square)
        if piece is None:
            return "Unknown move"

        piece_name = PIECE_NAMES[piece.symbol()]
        src = chess.square_name(move.from_square).upper()
        dst = chess.square_name(move.to_square).upper()

        return f"{piece_name}: {src} -> {dst}"

    def execute_human_move(self, move):
        src = chess.square_name(move.from_square).upper()
        dst = chess.square_name(move.to_square).upper()

        self.status_label.config(text=f"You played: {src} -> {dst}")
        self.root.update()

        pick_and_place_one_program(HOST, PORT, self.above, self.touch, src, dst)
        captured_piece = self.board.piece_at(move.to_square)
        if captured_piece:
            symbol = UNICODE_PIECES[captured_piece.symbol()]
            if captured_piece.color == chess.WHITE:
                self.captured_white.append(symbol)
            else:
                self.captured_black.append(symbol)

        move_entry = self.format_move_entry(move)
        self.move_log.append(move_entry)
        self.board.push(move)
        self.update_move_log_display()
        self.update_captured_display()
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
        captured_piece = self.board.piece_at(ai_move.to_square)
        if captured_piece:
            symbol = UNICODE_PIECES[captured_piece.symbol()]
            if captured_piece.color == chess.WHITE:
                self.captured_white.append(symbol)
            else:
                self.captured_black.append(symbol)

        move_entry = self.format_move_entry(ai_move)
        self.move_log.append(move_entry)
        self.board.push(ai_move)
        self.update_move_log_display()
        self.update_captured_display()
        self.draw_board()

        time.sleep(MOVE_DELAY)

        if self.board.is_game_over():
            self.status_label.config(text=f"Game over: {self.board.result()}")
        else:
            self.status_label.config(text="Your turn: click a piece, then click destination.")

    def update_captured_display(self):
        white_text = "Captured White: " + " ".join(self.captured_white)
        black_text = "Captured Black: " + " ".join(self.captured_black)

        self.captured_white_label.config(text=white_text)
        self.captured_black_label.config(text=black_text)

    def reset_game(self):
        self.board = chess.Board()
        self.selected_square = None
        self.draw_board()
        self.status_label.config(text="Game reset. Your turn: click a piece, then click destination.")
        self.captured_white = []
        self.captured_black = []
        self.update_captured_display()
        self.move_log = []
        self.update_move_log_display()

        send_urscript(HOST, PORT, NEUTRAL_MOVEJ)
        time.sleep(STARTUP_DELAY)

    def update_move_log_display(self):
        self.move_log_text.config(state="normal")
        self.move_log_text.delete("1.0", tk.END)

        for i, entry in enumerate(self.move_log, start=1):
            self.move_log_text.insert(tk.END, f"{i}. {entry}\n")

        self.move_log_text.see(tk.END) #auto-scroll
        self.move_log_text.config(state="disabled")

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
