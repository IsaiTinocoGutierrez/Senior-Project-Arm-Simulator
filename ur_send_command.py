import socket
import time
import chess
import chess.engine

FILES = "ABCDEFGH"
RANKS = "12345678"

def send_urscript(host: str, port: int, command: str):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
            if not command.endswith("\n"):
                command += "\n"
            s.sendall(command.encode("utf-8"))
            print(f">> Sent: {command.strip()}")
            time.sleep(0.2)
    except Exception as e:
        print(f"[ERROR] {e}")

def movel_cmd(pose_str: str, a: float = 0.3, v: float = 0.1) -> str:
    return f"movel({pose_str}, a={a}, v={v})"

def make_square_maps(
    xA1: float, yA1: float,
    square: float = 0.057,
    z_above: float = 0.15,
    z_touch: float = 0.05,
    rx: float = 0.0, ry: float = 3.14, rz: float = 0.0
):
    above = {}
    touch = {}

    for r_idx, r in enumerate(RANKS):      # 1..8
        for f_idx, f in enumerate(FILES):  # A..H
            name = f + r
            x = xA1 + f_idx * square
            y = yA1 + r_idx * square

            above[name] = f"p[{x:.3f}, {y:.3f}, {z_above:.3f}, {rx:.3f}, {ry:.3f}, {rz:.3f}]"
            touch[name] = f"p[{x:.3f}, {y:.3f}, {z_touch:.3f}, {rx:.3f}, {ry:.3f}, {rz:.3f}]"

    return above, touch

def pick_and_place(host: str, port: int, above: dict, touch: dict,
                   src: str, dst: str, a: float = 0.3, v: float = 0.1):

    # Approach source
    send_urscript(host, port, movel_cmd(above[src], a, v)); time.sleep(1.5)
    # Dip down (“pick”)
    send_urscript(host, port, movel_cmd(touch[src], a, v)); time.sleep(1.0)
    # Lift
    send_urscript(host, port, movel_cmd(above[src], a, v)); time.sleep(1.0)

    # Travel to destination
    send_urscript(host, port, movel_cmd(above[dst], a, v)); time.sleep(1.5)
    # Dip down (“place”)
    send_urscript(host, port, movel_cmd(touch[dst], a, v)); time.sleep(1.0)
    # Lift
    send_urscript(host, port, movel_cmd(above[dst], a, v)); time.sleep(1.0)

def uci_to_squares(uci: str):
    """
    Converts 'e2e4' -> ('E2','E4')
    """
    move = chess.Move.from_uci(uci)
    src = chess.square_name(move.from_square).upper()
    dst = chess.square_name(move.to_square).upper()
    return src, dst

def get_stockfish_move(engine, board, think_time_s=0.2):
    """
    Ask Stockfish for the best move for the current board position.
    Returns a chess.Move object.
    """
    result = engine.play(board, chess.engine.Limit(time=think_time_s))
    return result.move

def main():
    host = "127.0.0.1"
    port = 30002

    # Start robot safely
    send_urscript(host, port,
                  "movej([0, -1.2, 1.8, -1.0, -1.57, 0], a=1.0, v=0.1)")
    time.sleep(2)

    # --- CALIBRATE THESE (A1 center in meters) ---
    xA1 = 0.421
    yA1 = -0.081

    above, touch = make_square_maps(
        xA1=xA1, yA1=yA1,
        square=0.057,
        z_above=0.15,
        z_touch=0.05,
        rx=0.0, ry=3.14, rz=0.0
    )

    # Create chess board
    board = chess.Board()

    # ---- POINT THIS TO YOUR STOCKFISH EXE ----
    stockfish_path = r"C:\Users\isait\OneDrive\Desktop\senior project\stockfish\stockfish-windows-x86-64-avx2.exe"

    engine = chess.engine.SimpleEngine.popen_uci(stockfish_path)
    print("Stockfish connected!")
    with chess.engine.SimpleEngine.popen_uci(stockfish_path) as engine:
        print("Stockfish connected. You are White. Enter moves like e2e4, g1f3, etc.")

        while not board.is_game_over():
            # 1) Human move
            uci = input("Your move (uci): ").strip().lower()

            # Basic validation
            try:
                human_move = chess.Move.from_uci(uci)
            except ValueError:
                print("Invalid UCI format. Example: e2e4")
                continue

            if human_move not in board.legal_moves:
                print("Illegal move for this position.")
                continue

            # Execute human move on robot
            src = chess.square_name(human_move.from_square).upper()
            dst = chess.square_name(human_move.to_square).upper()
            print(f"Robot executes YOU: {src} -> {dst}")
            pick_and_place(host, port, above, touch, src, dst, a=0.3, v=0.1)

            board.push(human_move)
            print(board)

            if board.is_game_over():
                break

            # 2) Stockfish reply
            ai_move = get_stockfish_move(engine, board, think_time_s=0.2)
            ai_uci = ai_move.uci()
            print(f"Stockfish plays: {ai_uci}")

            # Execute AI move on robot
            ai_src = chess.square_name(ai_move.from_square).upper()
            ai_dst = chess.square_name(ai_move.to_square).upper()
            print(f"Robot executes AI: {ai_src} -> {ai_dst}")
            pick_and_place(host, port, above, touch, ai_src, ai_dst, a=0.3, v=0.1)

            board.push(ai_move)
            print(board)

        print("Game over:", board.result())

if __name__ == "__main__":
    main()
