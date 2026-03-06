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

def movej_cmd(pose_str: str, a: float = 0.4, v: float = 0.2) -> str:
    return f"movej({pose_str}, a={a}, v={v})"

def movel_cmd(pose_str: str, a: float = 0.2, v: float = 0.05) -> str:
    return f"movel({pose_str}, a={a}, v={v})"

def make_square_maps(
    xA1: float, yA1: float,
    square: float = 0.057,
    z_above: float = 0.22,
    z_touch: float = 0.12,
    rx: float = 0.0, ry: float = 3.14, rz: float = 0.0
):
    above = {}
    touch = {}

    for r_idx, r in enumerate(RANKS):
        for f_idx, f in enumerate(FILES):
            name = f + r
            x = xA1 + f_idx * square
            y = yA1 + r_idx * square

            above[name] = f"p[{x:.3f}, {y:.3f}, {z_above:.3f}, {rx:.3f}, {ry:.3f}, {rz:.3f}]"
            touch[name] = f"p[{x:.3f}, {y:.3f}, {z_touch:.3f}, {rx:.3f}, {ry:.3f}, {rz:.3f}]"

    return above, touch

def pick_and_place_one_program(host, port, above, touch, src, dst):
    script = f"""
def chess_pick_place():
  movej({above[src]}, a=0.4, v=0.2)
  movel({touch[src]}, a=0.15, v=0.04)
  movel({above[src]}, a=0.15, v=0.04)

  movej({above[dst]}, a=0.4, v=0.2)
  movel({touch[dst]}, a=0.15, v=0.04)
  movel({above[dst]}, a=0.15, v=0.04)
end
chess_pick_place()
"""
    send_urscript(host, port, script)

def get_stockfish_move(engine, board, think_time_s=0.2):
    result = engine.play(board, chess.engine.Limit(time=think_time_s))
    return result.move

def main():
    host = "127.0.0.1"
    port = 30002

    # Safe neutral pose
    send_urscript(host, port,
                  "movej([0, -1.2, 1.8, -1.0, -1.57, 0], a=0.8, v=0.15)")
    time.sleep(3)

    # Safer test board placement
    xA1 = 0.52
    yA1 = -0.20

    above, touch = make_square_maps(
        xA1=xA1,
        yA1=yA1,
        square=0.057,
        z_above=0.22,
        z_touch=0.12,
        rx=0.0,
        ry=3.14,
        rz=0.0
    )

    board = chess.Board()

    stockfish_path = r"C:\Users\isait\OneDrive\Desktop\senior project\stockfish\stockfish-windows-x86-64-avx2.exe"

    with chess.engine.SimpleEngine.popen_uci(stockfish_path) as engine:
        print("Stockfish connected. You are White. Enter moves like e2e4, g1f3, etc.")

        while not board.is_game_over():
            uci = input("Your move (uci): ").strip().lower()

            try:
                human_move = chess.Move.from_uci(uci)
            except ValueError:
                print("Invalid UCI format. Example: e2e4")
                continue

            if human_move not in board.legal_moves:
                print("Illegal move for this position.")
                continue

            src = chess.square_name(human_move.from_square).upper()
            dst = chess.square_name(human_move.to_square).upper()
            print(f"Robot executes YOU: {src} -> {dst}")
            pick_and_place_one_program(host, port, above, touch, src, dst)

            board.push(human_move)
            print(board)
            time.sleep(4)

            if board.is_game_over():
                break

            ai_move = get_stockfish_move(engine, board, think_time_s=0.2)
            ai_uci = ai_move.uci()
            print(f"Stockfish plays: {ai_uci}")

            ai_src = chess.square_name(ai_move.from_square).upper()
            ai_dst = chess.square_name(ai_move.to_square).upper()
            print(f"Robot executes AI: {ai_src} -> {ai_dst}")
            pick_and_place_one_program(host, port, above, touch, ai_src, ai_dst)

            board.push(ai_move)
            print(board)
            time.sleep(4)

        print("Game over:", board.result())

if __name__ == "__main__":
    main()
