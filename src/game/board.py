import random
from typing import List, Tuple, Optional
from copy import deepcopy

BOARD_SIZE = 10

class Piece:
    def __init__(self, row: int, col: int, color: str, king: bool = False):
        self.row = row
        self.col = col
        self.color = color
        self.king = king

class Board:
    def __init__(self):
        self.grid = [[0] * BOARD_SIZE for _ in range(BOARD_SIZE)]
        for row in range(4):
            for col in range(BOARD_SIZE):
                if (row + col) % 2 != 0:
                    self.grid[row][col] = Piece(row, col, "black")
        for row in range(6, BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if (row + col) % 2 != 0:
                    self.grid[row][col] = Piece(row, col, "white")

    def get_piece(self, row: int, col: int) -> Optional[Piece]:
        if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE:
            return self.grid[row][col]
        return 0

    def move_piece(self, piece: Piece, new_row: int, new_col: int):
        self.grid[piece.row][piece.col] = 0
        piece.row, piece.col = new_row, new_col
        self.grid[new_row][new_col] = piece
        if piece.color == "white" and new_row == 0:
            piece.king = True
        elif piece.color == "black" and new_row == BOARD_SIZE - 1:
            piece.king = True

    def remove_piece(self, row: int, col: int):
        self.grid[row][col] = 0

def get_valid_moves(board: Board, row: int, col: int, only_captures: bool = False) -> List[Tuple[int, int]]:
    moves = []
    capture_moves = []
    piece = board.get_piece(row, col)
    if not piece or piece == 0:
        return moves
    directions = [(-1, -1), (-1, 1)] if piece.color == "white" else [(1, -1), (1, 1)]
    if piece.king:
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
    if not only_captures:
        for drow, dcol in directions:
            new_row, new_col = row + drow, col + dcol
            if is_valid_square(new_row, new_col) and board.get_piece(new_row, new_col) == 0:
                moves.append((new_row, new_col))
    for drow, dcol in directions:
        new_row, new_col = row + 2 * drow, col + 2 * dcol
        intermediate_row, intermediate_col = row + drow, col + dcol
        if (
            is_valid_square(new_row, new_col)
            and is_valid_square(intermediate_row, intermediate_col)
        ):
            intermediate_piece = board.get_piece(intermediate_row, intermediate_col)
            if (
                intermediate_piece != 0
                and is_opponent(intermediate_piece, piece)
                and board.get_piece(new_row, new_col) == 0
                and not is_in_warp_zone(intermediate_row, intermediate_col)
            ):
                capture_moves.append((new_row, new_col))
    return capture_moves if capture_moves else moves

def is_valid_square(row: int, col: int) -> bool:
    return 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE

def is_opponent(piece1: Piece, piece2: Piece) -> bool:
    return piece1.color != piece2.color

def is_valid_move(board: Board, piece: Piece, new_row: int, new_col: int, player_color: str) -> bool:
    if piece.color != player_color:
        return False
    valid_moves = get_valid_moves(board, piece.row, piece.col)
    return (new_row, new_col) in valid_moves

def execute_move(board: Board, piece: Piece, new_row: int, new_col: int, allow_multi_jump: bool = False) -> Tuple[bool, bool, Optional[Tuple[int, int]], bool]:
    valid_moves = get_valid_moves(board, piece.row, piece.col)
    if (new_row, new_col) not in valid_moves:
        return False, False, None, False
    is_capture = False
    dr, dc = new_row - piece.row, new_col - piece.col
    if abs(dr) == 2 and abs(dc) == 2:
        captured_row, captured_col = (piece.row + new_row) // 2, (piece.col + new_col) // 2
        board.remove_piece(captured_row, captured_col)
        is_capture = True
    board.move_piece(piece, new_row, new_col)
    can_jump_again = False
    bonus_move_triggered = False
    if allow_multi_jump:  # Only check for multi-jumps if allowed
        more_captures = get_valid_moves(board, new_row, new_col, only_captures=True)
        if more_captures:
            can_jump_again = True
            return is_capture, can_jump_again, (new_row, new_col), False
    # Warp zone logic: Grant bonus move if landing on a warp zone square
    if is_in_warp_zone(new_row, new_col):
        bonus_move_triggered = True
    return is_capture, can_jump_again, None, bonus_move_triggered

def is_piece_at_position(board: Board, row: int, col: int, player_color: str) -> bool:
    piece = board.get_piece(row, col)
    return piece != 0 and piece.color == player_color

def get_all_valid_moves_for_player(board: Board, player_color: str) -> List[Tuple[Piece, Tuple[int, int]]]:
    moves = []
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            piece = board.get_piece(row, col)
            if piece != 0 and piece.color == player_color:
                valid_moves = get_valid_moves(board, row, col)
                for move in valid_moves:
                    moves.append((piece, move))
    return moves

def evaluate_board(board: Board, player_color: str) -> float:
    """Evaluate the board state from the AI's perspective."""
    score = 0
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            piece = board.get_piece(row, col)
            if piece != 0:
                if piece.color == player_color:
                    score += 1  # +1 for each AI piece
                    if piece.king:
                        score += 2  # +2 for each AI king (total +3)
                    if is_in_warp_zone(piece.row, piece.col):
                        score += 1
                else:
                    score -= 1  # -1 for each opponent piece
                    if piece.king:
                        score -= 2  # -2 for each opponent king (total -3)
                    if is_in_warp_zone(piece.row, piece.col):
                        score -= 1
    return score

def minimax_with_alpha_beta(board: Board, depth: int, maximizing_player: bool, player_color: str, alpha: float, beta: float, allow_multi_jump: bool = False) -> Tuple[float, Optional[Tuple[Piece, Tuple[int, int]]]]:
    """Minimax algorithm with alpha-beta pruning to find the best move."""
    if depth == 0:
        return evaluate_board(board, player_color), None

    valid_moves = get_all_valid_moves_for_player(board, player_color if maximizing_player else ("white" if player_color == "black" else "black"))
    if not valid_moves:
        return (-float('inf') if maximizing_player else float('inf')), None

    best_move = None
    if maximizing_player:  # AI's turn (maximizing)
        max_eval = -float('inf')
        for piece, (new_row, new_col) in valid_moves:
            board_copy = deepcopy(board)
            piece_copy = board_copy.get_piece(piece.row, piece.col)
            is_capture, can_jump_again, new_selection, _ = execute_move(board_copy, piece_copy, new_row, new_col, allow_multi_jump)
            if is_capture and can_jump_again and allow_multi_jump:  # Handle multi-jumps
                sub_eval = max_eval
                while can_jump_again:
                    piece_copy = board_copy.get_piece(new_selection[0], new_selection[1])
                    sub_moves = get_valid_moves(board_copy, new_selection[0], new_selection[1], only_captures=True)
                    if not sub_moves:
                        break
                    new_row, new_col = sub_moves[0]  # Take the first capture for simplicity
                    is_capture, can_jump_again, new_selection, _ = execute_move(board_copy, piece_copy, new_row, new_col, allow_multi_jump)
                    eval_score, _ = minimax_with_alpha_beta(board_copy, depth - 1, maximizing_player, player_color, alpha, beta, allow_multi_jump)
                    sub_eval = max(sub_eval, eval_score)
                eval_score = sub_eval
            else:
                eval_score, _ = minimax_with_alpha_beta(board_copy, depth - 1, False, player_color, alpha, beta, allow_multi_jump)
            if eval_score > max_eval:
                max_eval = eval_score
                best_move = (piece, (new_row, new_col))
            alpha = max(alpha, max_eval)
            if beta <= alpha:
                break  # Alpha-beta pruning
        return max_eval, best_move
    else:  # Player's turn (minimizing)
        min_eval = float('inf')
        for piece, (new_row, new_col) in valid_moves:
            board_copy = deepcopy(board)
            piece_copy = board_copy.get_piece(piece.row, piece.col)
            is_capture, can_jump_again, new_selection, _ = execute_move(board_copy, piece_copy, new_row, new_col, allow_multi_jump)
            if is_capture and can_jump_again and allow_multi_jump:
                sub_eval = min_eval
                while can_jump_again:
                    piece_copy = board_copy.get_piece(new_selection[0], new_selection[1])
                    sub_moves = get_valid_moves(board_copy, new_selection[0], new_selection[1], only_captures=True)
                    if not sub_moves:
                        break
                    new_row, new_col = sub_moves[0]
                    is_capture, can_jump_again, new_selection, _ = execute_move(board_copy, piece_copy, new_row, new_col, allow_multi_jump)
                    eval_score, _ = minimax_with_alpha_beta(board_copy, depth - 1, maximizing_player, player_color, alpha, beta, allow_multi_jump)
                    sub_eval = min(sub_eval, eval_score)
                eval_score = sub_eval
            else:
                eval_score, _ = minimax_with_alpha_beta(board_copy, depth - 1, True, player_color, alpha, beta, allow_multi_jump)
            min_eval = min(min_eval, eval_score)
            beta = min(beta, min_eval)
            if beta <= alpha:
                break  # Alpha-beta pruning
        return min_eval, best_move

def make_ai_move(board: Board, player_color: str, depth: int = 3, allow_multi_jump: bool = False) -> Tuple[bool, bool]:
    """Make the AI's move using minimax with alpha-beta pruning. Returns (move_made, bonus_move_triggered)."""
    _, best_move = minimax_with_alpha_beta(board, depth, True, player_color, -float('inf'), float('inf'), allow_multi_jump)
    if best_move:
        piece, (new_row, new_col) = best_move
        is_capture, can_jump_again, _, bonus_move_triggered = execute_move(board, piece, new_row, new_col, allow_multi_jump)
        return True, bonus_move_triggered
    return False, False

def is_in_warp_zone(row: int, col: int) -> bool:
    warp_zone_coords = [(4, 4), (4, 5), (5, 4), (5, 5)]
    return (row, col) in warp_zone_coords