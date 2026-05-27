import time
from tkinter import messagebox
import chess
import chess.engine
import threading

from config import (
    HOST,
    PORT,
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

from chess_engine import get_stockfish_move

from robot.connection import send_urscript
from robot.mapping import make_square_maps
from robot.motion import pick_and_place_one_program
from robot.poses import get_neutral_pose_command

from ui.board_view import BoardView
from ui.side_panel import SidePanel

from services.game_state import GameState
from services.capture_logic import record_capture_if_any
from services.move_logger import append_move_log

from robot.manual_jog import (
    jog_x_positive,
    jog_x_negative,
    jog_y_positive,
    jog_y_negative,
    jog_z_positive,
    jog_z_negative,
    stop_motion,
)

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

        self.state = GameState()

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

        self.side_panel.connect_jog_buttons(
            x_neg_callback=self.jog_x_negative,
            x_pos_callback=self.jog_x_positive,
            y_neg_callback=self.jog_y_negative,
            y_pos_callback=self.jog_y_positive,
            z_neg_callback=self.jog_z_negative,
            z_pos_callback=self.jog_z_positive,
            stop_callback=self.stop_robot_motion,
        )

        self.refresh_ui()

        send_urscript(HOST, PORT, get_neutral_pose_command())
        time.sleep(STARTUP_DELAY)

    def refresh_ui(self):
        self.board_view.draw_board(self.state.board, self.state.selected_square)
        self.side_panel.update_captured(
            self.state.captured_white,
            self.state.captured_black,
        )
        self.side_panel.update_move_log(self.state.move_log)

    def on_square_click(self, row, col):
        clicked_square = self.board_view.rowcol_to_square(row, col)

        if self.state.selected_square is None:
            piece = self.state.board.piece_at(clicked_square)
            if piece is None:
                return
            if piece.color != chess.WHITE:
                return

            self.state.selected_square = clicked_square
            self.refresh_ui()
            return

        from_sq = self.state.selected_square
        to_sq = clicked_square
        self.state.selected_square = None
        self.refresh_ui()

        move = chess.Move(from_sq, to_sq)

        if move not in self.state.board.legal_moves:
            messagebox.showerror("Illegal Move", "That move is not legal.")
            return

        self.execute_human_move(move)

    def execute_human_move(self, move):
        src = chess.square_name(move.from_square).upper()
        dst = chess.square_name(move.to_square).upper()

        self.side_panel.update_status(f"You played: {src} -> {dst}")
        self.root.update()

        pick_and_place_one_program(HOST, PORT, self.above, self.touch, src, dst)

        record_capture_if_any(
            self.state.board,
            move,
            self.state.captured_white,
            self.state.captured_black,
        )

        append_move_log(self.state.board, move, self.state.move_log)

        self.state.board.push(move)
        self.refresh_ui()

        time.sleep(MOVE_DELAY)

        if self.state.board.is_game_over():
            self.side_panel.update_status(f"Game over: {self.state.board.result()}")
            return

        self.execute_ai_move()

    def execute_ai_move(self):
        ai_move = get_stockfish_move(self.engine, self.state.board, think_time_s=THINK_TIME)

        src = chess.square_name(ai_move.from_square).upper()
        dst = chess.square_name(ai_move.to_square).upper()

        self.side_panel.update_status(f"Stockfish plays: {src} -> {dst}")
        self.root.update()

        pick_and_place_one_program(HOST, PORT, self.above, self.touch, src, dst)

        record_capture_if_any(
            self.state.board,
            ai_move,
            self.state.captured_white,
            self.state.captured_black,
        )

        append_move_log(self.state.board, ai_move, self.state.move_log)

        self.state.board.push(ai_move)
        self.refresh_ui()

        time.sleep(MOVE_DELAY)

        if self.state.board.is_game_over():
            self.side_panel.update_status(f"Game over: {self.state.board.result()}")
        else:
            self.side_panel.update_status("Your turn: click a piece, then click destination.")

    def run_jog_async(self, jog_function):
        threading.Thread(
            target=jog_function,
            daemon=True
        ).start()

    def reset_game(self):
        self.state.reset()
        self.refresh_ui()
        self.side_panel.update_status("Game reset. Your turn: click a piece, then click destination.")

        send_urscript(HOST, PORT, get_neutral_pose_command())
        time.sleep(STARTUP_DELAY)

    def jog_x_positive(self):
        self.side_panel.update_status("Jogging X+")
        self.run_jog_async(lambda: jog_x_positive(HOST, PORT))

    def jog_x_negative(self):
        self.side_panel.update_status("Jogging X-")
        self.run_jog_async(lambda: jog_x_negative(HOST, PORT))

    def jog_y_positive(self):
        self.side_panel.update_status("Jogging Y+")
        self.run_jog_async(lambda: jog_y_positive(HOST, PORT))

    def jog_y_negative(self):
        self.side_panel.update_status("Jogging Y-")
        self.run_jog_async(lambda: jog_y_negative(HOST, PORT))

    def jog_z_positive(self):
        self.side_panel.update_status("Jogging Z+")
        self.run_jog_async(lambda: jog_z_positive(HOST, PORT))

    def jog_z_negative(self):
        self.side_panel.update_status("Jogging Z-")
        self.run_jog_async(lambda: jog_z_negative(HOST, PORT))

    def stop_robot_motion(self):
        self.side_panel.update_status("Stopping robot motion")
        self.run_jog_async(lambda: stop_motion(HOST, PORT))

    def close(self):
        try:
            self.engine.quit()
        finally:
            self.root.destroy()