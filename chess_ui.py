import time
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
from ui.board_view import BoardView
from ui.side_panel import SidePanel


PIECE_NAMES = {
    "P": "White pawn",
    "N": "White knight",
    "B": "White bishop",
    "R": "White rook",
    "Q": "White queen",
    "K": "White king",
    "p": "Black pawn",
    "n": "Black knight",
    "b": "Black bishop",
    "r": "Black rook",
    "q": "Black queen",
    "k": "Black king",
}

# Used for captured-piece display in the side panel.
UNICODE_PIECES = {
    "P": "♙", "N": "♘", "B": "♗", "R": "♖", "Q": "♕", "K": "♔",
    "p": "♟", "n": "♞", "b": "♝", "r": "♜", "q": "♛", "k": "♚",
}


class GameController:
    def __init__(self, root):
        self.root = root
        self.root.title("Robot Chess")
        self.root.resizable(True, True)
        self.root.geometry("900x600")

        for i in range(8):
            self.root.grid_rowconfigure(i + 1, weight=1)
            self.root.grid_columnconfigure(i, weight=1)

        self.root.grid_columnconfigure(8, weight=1)
        self.root.grid_rowconfigure(6, weight=1)

        self.board = chess.Board()
        self.selected_square = None
        self.captured_white = []
        self.captured_black = []
        self.move_log = []

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

        self.board_view = BoardView(root, self.on_square_click)
        self.board_view.build_board()

        self.side_panel = SidePanel(root, self.reset_game)

        self.refresh_ui()

        send_urscript(HOST, PORT, NEUTRAL_MOVEJ)
        time.sleep(STARTUP_DELAY)

    def refresh_ui(self):
        self.board_view.draw_board(self.board, self.selected_square)
        self.side_panel.update_captured(self.captured_white, self.captured_black)
        self.side_panel.update_move_log(self.move_log)

    def on_square_click(self, row, col):
        clicked_square = self.board_view.rowcol_to_square(row, col)

        if self.selected_square is None:
            piece = self.board.piece_at(clicked_square)
            if piece is None:
                return
            if piece.color != chess.WHITE:
                return

            self.selected_square = clicked_square
            self.refresh_ui()
            return

        from_sq = self.selected_square
        to_sq = clicked_square
        self.selected_square = None
        self.refresh_ui()

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

    def record_capture_if_any(self, move):
        captured_piece = self.board.piece_at(move.to_square)
        if captured_piece:
            symbol = UNICODE_PIECES[captured_piece.symbol()]
            if captured_piece.color == chess.WHITE:
                self.captured_white.append(symbol)
            else:
                self.captured_black.append(symbol)

    def execute_human_move(self, move):
        src = chess.square_name(move.from_square).upper()
        dst = chess.square_name(move.to_square).upper()

        self.side_panel.update_status(f"You played: {src} -> {dst}")
        self.root.update()

        pick_and_place_one_program(HOST, PORT, self.above, self.touch, src, dst)

        self.record_capture_if_any(move)

        move_entry = self.format_move_entry(move)
        self.move_log.append(move_entry)

        self.board.push(move)
        self.refresh_ui()

        time.sleep(MOVE_DELAY)

        if self.board.is_game_over():
            self.side_panel.update_status(f"Game over: {self.board.result()}")
            return

        self.execute_ai_move()

    def execute_ai_move(self):
        ai_move = get_stockfish_move(self.engine, self.board, think_time_s=THINK_TIME)

        src = chess.square_name(ai_move.from_square).upper()
        dst = chess.square_name(ai_move.to_square).upper()

        self.side_panel.update_status(f"Stockfish plays: {src} -> {dst}")
        self.root.update()

        pick_and_place_one_program(HOST, PORT, self.above, self.touch, src, dst)

        self.record_capture_if_any(ai_move)

        move_entry = self.format_move_entry(ai_move)
        self.move_log.append(move_entry)

        self.board.push(ai_move)
        self.refresh_ui()

        time.sleep(MOVE_DELAY)

        if self.board.is_game_over():
            self.side_panel.update_status(f"Game over: {self.board.result()}")
        else:
            self.side_panel.update_status("Your turn: click a piece, then click destination.")

    def reset_game(self):
        self.board = chess.Board()
        self.selected_square = None
        self.captured_white = []
        self.captured_black = []
        self.move_log = []

        self.refresh_ui()
        self.side_panel.update_status("Game reset. Your turn: click a piece, then click destination.")

        send_urscript(HOST, PORT, NEUTRAL_MOVEJ)
        time.sleep(STARTUP_DELAY)

    def close(self):
        try:
            self.engine.quit()
        finally:
            self.root.destroy()
