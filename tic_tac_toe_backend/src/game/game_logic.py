from typing import Optional, List


def check_winner(board: str) -> Optional[str]:
    """
    Check if there's a winner on the board.
    Returns 'X' or 'O' if there's a winner, None if no winner.
    """
    # Define winning combinations
    winning_combinations = [
        (0, 1, 2),
        (3, 4, 5),
        (6, 7, 8),  # Rows
        (0, 3, 6),
        (1, 4, 7),
        (2, 5, 8),  # Columns
        (0, 4, 8),
        (2, 4, 6),  # Diagonals
    ]

    for combo in winning_combinations:
        if (
            board[combo[0]] != " "
            and board[combo[0]] == board[combo[1]] == board[combo[2]]
        ):
            return board[combo[0]]
    return None


def is_board_full(board: str) -> bool:
    """Check if the board is full."""
    return " " not in board


def is_valid_move(board: str, position: int) -> bool:
    """Check if a move is valid."""
    if position < 0 or position > 8:
        return False
    return board[position] == " "


def get_available_moves(board: str) -> List[int]:
    """Get list of available moves."""
    return [i for i, spot in enumerate(board) if spot == " "]


def make_move(board: str, position: int, player_symbol: str) -> str:
    """Make a move on the board."""
    if not is_valid_move(board, position):
        raise ValueError("Invalid move")
    return board[:position] + player_symbol + board[position + 1:]
