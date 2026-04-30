import chess

from shared.piece_constants import PIECE_NAMES

def format_move_entry(board, move):
    """
    Returns a readable move log entry like:
    White pawn: E2 -> E4
    """
    piece = board.piece_at(move.from_square)
    if piece is None:
        return "Unknown move"

    piece_name = PIECE_NAMES[piece.symbol()]
    src = chess.square_name(move.from_square).upper()
    dst = chess.square_name(move.to_square).upper()

    return f"{piece_name}: {src} -> {dst}"


def append_move_log(board, move, move_log):
    entry = format_move_entry(board, move)
    move_log.append(entry)