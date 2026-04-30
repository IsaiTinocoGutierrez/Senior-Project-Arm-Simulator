import chess


class GameState:
    def __init__(self):
        self.reset()

    def reset(self):
        self.board = chess.Board()
        self.selected_square = None
        self.captured_white = []
        self.captured_black = []
        self.move_log = []