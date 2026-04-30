from shared.piece_constants import UNICODE_PIECES

def record_capture_if_any(board, move, captured_white, captured_black):
    """
    Checks whether a move captures a piece and updates the captured lists.
    """
    captured_piece = board.piece_at(move.to_square)

    if captured_piece:
        symbol = UNICODE_PIECES[captured_piece.symbol()]
        if captured_piece.color:  # True = White
            captured_white.append(symbol)
        else:  # False = Black
            captured_black.append(symbol)