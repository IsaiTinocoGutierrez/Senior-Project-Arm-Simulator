import chess
import chess.engine


def get_stockfish_move(engine, board, think_time_s=0.2):
    result = engine.play(board, chess.engine.Limit(time=think_time_s))
    return result.move


def parse_uci_move(uci: str, board: chess.Board):
    try:
        move = chess.Move.from_uci(uci)
    except ValueError:
        return None, "Invalid UCI format. Example: e2e4"

    if move not in board.legal_moves:
        return None, "Illegal move for this position."

    return move, None