import tkinter as tk
import chess

from shared.piece_constants import UNICODE_PIECES
# NOTE:
# In python-chess, uppercase symbols are White and lowercase are Black.


class BoardView:
    def __init__(self, root, click_callback):
        self.root = root
        self.click_callback = click_callback
        self.buttons = {}

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
                    command=lambda r=row, c=col: self.click_callback(r, c),
                )
                btn.grid(row=row + 1, column=col, sticky="nsew")
                self.buttons[(row, col)] = btn

    def draw_board(self, board, selected_square=None):
        for row in range(8):
            for col in range(8):
                square = chess.square(col, 7 - row)
                piece = board.piece_at(square)

                text = UNICODE_PIECES.get(piece.symbol(), "") if piece else ""
                color = "#F0D9B5" if (row + col) % 2 == 0 else "#B58863"

                self.buttons[(row, col)].config(text=text, bg=color)

        if selected_square is not None:
            row, col = self.square_to_rowcol(selected_square)
            self.buttons[(row, col)].config(bg="yellow")

    def square_to_rowcol(self, square):
        col = chess.square_file(square)
        row = 7 - chess.square_rank(square)
        return row, col

    def rowcol_to_square(self, row, col):
        return chess.square(col, 7 - row)