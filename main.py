import pygame
import sys
import random
from copy import deepcopy
from src.ui.gui import GUI, get_tile_at_mouse_pos, highlight_valid_moves
from src.game.board import Board, Piece, is_piece_at_position, is_valid_move, execute_move, get_valid_moves, get_all_valid_moves_for_player, is_in_warp_zone, make_ai_move, BOARD_SIZE

# Updated window size
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 650  # Increased height to accommodate the timer
BOARD_SIZE_PX = 600  # The board still occupies a 600x600 area

def handle_mouse_click(board: Board, selected_piece: tuple[int, int] | None, player_color: str) -> tuple[str, tuple[int, int] | None] | tuple[str, Piece, tuple[int, int]]:
    mouse_pos = pygame.mouse.get_pos()
    row, col = get_tile_at_mouse_pos(mouse_pos)
    if selected_piece:
        piece = board.get_piece(selected_piece[0], selected_piece[1])
        if piece and is_valid_move(board, piece, row, col, player_color):
            return ("move", piece, (row, col))
        else:
            return ("none", None)
    else:
        if is_piece_at_position(board, row, col, player_color):
            return ("select", (row, col))
        return ("none", None)

def switch_turns(current_turn: str) -> str:
    return "black" if current_turn == "white" else "white"

def count_pieces(board: Board, color: str) -> int:
    count = 0
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            piece = board.get_piece(row, col)
            if piece != 0 and piece.color == color:
                count += 1
    return count

def reset_game() -> tuple[Board, None, str, int, bool, str, int, int, bool, bool, bool, bool]:
    board = Board()
    selected_piece = None
    current_turn = "white"
    moves_without_capture = 0
    draw_prompt = False
    message = ""
    message_timer = 0
    turn_start_time = pygame.time.get_ticks()
    bonus_move_active = False
    player_multi_jump_used = False
    ai_multi_jump_used = False
    multi_jump_active = False
    return (board, selected_piece, current_turn, moves_without_capture, draw_prompt, message, message_timer,
            turn_start_time, bonus_move_active, player_multi_jump_used, ai_multi_jump_used, multi_jump_active)

def draw_timer(screen, remaining_time):
    """Draw the remaining time in the bottom-right corner with yellow text and white background."""
    font = pygame.font.Font(None, 36)
    seconds = max(0, remaining_time // 1000)  # Convert milliseconds to seconds
    timer_text = font.render(f"Time: {seconds}s", True, (255, 255, 0))  # Yellow text
    text_rect = timer_text.get_rect()
    # Position in bottom-right corner, within the extra 50px height
    text_rect.bottomright = (WINDOW_WIDTH - 10, WINDOW_HEIGHT - 10)
    # Draw a white background rectangle slightly larger than the text
    background_rect = text_rect.inflate(10, 5)  # Add padding around the text
    pygame.draw.rect(screen, (0, 0, 139), background_rect)  # Dark blue background
    screen.blit(timer_text, text_rect)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('Checkers AI')

    board = Board()
    gui = GUI(screen, board)
    clock = pygame.time.Clock()

    selected_piece = None
    current_turn = "white"
    running = True
    moves_without_capture = 0
    DRAW_THRESHOLD = 20
    draw_prompt = False
    message = ""
    message_timer = 0
    game_over = False
    bonus_move_active = False
    last_moved_piece_pos = None
    turn_start_time = pygame.time.get_ticks()
    TURN_DURATION = 5000
    player_multi_jump_used = False
    ai_multi_jump_used = False
    multi_jump_active = False

    while running:
        clock.tick(60)
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - turn_start_time
        remaining_time = max(0, TURN_DURATION - elapsed_time)

        if remaining_time <= 0 and not game_over:
            message = f"{current_turn.capitalize()} took too long! Turn switched."
            message_timer = 90
            current_turn = switch_turns(current_turn)
            turn_start_time = pygame.time.get_ticks()
            selected_piece = None
            bonus_move_active = False
            last_moved_piece_pos = None
            multi_jump_active = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if game_over:
                    (board, selected_piece, current_turn, moves_without_capture, draw_prompt, message, message_timer,
                     turn_start_time, bonus_move_active, player_multi_jump_used, ai_multi_jump_used, multi_jump_active) = reset_game()
                    gui.board = board
                    game_over = False
                    last_moved_piece_pos = None
                    continue
                if current_turn == "white":
                    result = handle_mouse_click(board, selected_piece, current_turn)
                    if result[0] == "move":
                        _, piece, (new_row, new_col) = result
                        board_before = deepcopy(board)
                        is_capture, can_jump_again, new_selection, bonus_move_triggered = execute_move(board, piece, new_row, new_col, multi_jump_active)
                        if is_capture:
                            captured_row, captured_col = (piece.row + new_row) // 2, (piece.col + new_col) // 2
                            if is_in_warp_zone(captured_row, captured_col) and board_before.get_piece(captured_row, captured_col) != 0:
                                message = "Warp Zone: Capture Prevented!"
                                message_timer = 90
                                board.grid = board_before.grid
                                continue
                            moves_without_capture = 0
                            if can_jump_again and multi_jump_active:
                                message = "Multi-Jump Available!"
                                message_timer = 90
                                selected_piece = new_selection
                                continue
                        else:
                            moves_without_capture += 1
                        if bonus_move_triggered:
                            message = "Warp Zone: Bonus Move!"
                            message_timer = 90
                            bonus_move_active = True
                            last_moved_piece_pos = (new_row, new_col)
                            selected_piece = last_moved_piece_pos
                            turn_start_time = pygame.time.get_ticks()
                            continue
                        if draw_prompt:
                            draw_prompt = False
                        selected_piece = None
                        bonus_move_active = False
                        last_moved_piece_pos = None
                        current_turn = switch_turns(current_turn)
                        turn_start_time = pygame.time.get_ticks()
                        multi_jump_active = False
                    elif result[0] == "select":
                        if bonus_move_active:
                            _, pos = result
                            if pos == last_moved_piece_pos:
                                selected_piece = pos
                            else:
                                continue
                        else:
                            _, selected_piece = result
                    else:
                        selected_piece = None

            elif event.type == pygame.KEYDOWN and draw_prompt and not game_over:
                if event.key == pygame.K_d:
                    print("Game ended in a draw!")
                    message = "Draw! Play Again?"
                    message_timer = 0
                    game_over = True

        if not game_over and not bonus_move_active and elapsed_time < 100:
            if current_turn == "white" and not player_multi_jump_used:
                if random.random() < 0.1:
                    multi_jump_active = True
                    player_multi_jump_used = True
                    message = "Player Multi-Jump Activated!"
                    message_timer = 90
            elif current_turn == "black" and not ai_multi_jump_used:
                if random.random() < 0.1:
                    multi_jump_active = True
                    ai_multi_jump_used = True
                    message = "AI Multi-Jump Activated!"
                    message_timer = 90

        if current_turn == "black" and not game_over:
            board_before = deepcopy(board)
            move_made, bonus_move_triggered = make_ai_move(board, "black", depth=3, allow_multi_jump=multi_jump_active)
            if not move_made:
                print("AI has no valid moves. Player wins!")
                message = "Player Wins! Play Again?"
                message_timer = 0
                game_over = True
            else:
                captures_occurred = False
                captured_on_warp_zone = False
                captured_row, captured_col = None, None
                for row in range(BOARD_SIZE):
                    for col in range(BOARD_SIZE):
                        piece_before = board_before.get_piece(row, col)
                        piece_after = board.get_piece(row, col)
                        if piece_before != 0 and piece_after == 0 and piece_before.color == "white":
                            captures_occurred = True
                            captured_row, captured_col = row, col
                            if is_in_warp_zone(row, col):
                                captured_on_warp_zone = True
                            break
                    if captures_occurred:
                        break
                if captures_occurred:
                    if captured_on_warp_zone:
                        message = "Warp Zone: Capture Prevented!"
                        message_timer = 90
                        board.grid = board_before.grid
                        continue
                    moves_without_capture = 0
                    can_jump_again = False
                    for row in range(BOARD_SIZE):
                        for col in range(BOARD_SIZE):
                            piece = board.get_piece(row, col)
                            if piece and piece.color == "black":
                                if multi_jump_active and get_valid_moves(board, row, col, only_captures=True):
                                    can_jump_again = True
                                    break
                        if can_jump_again:
                            break
                    if can_jump_again and multi_jump_active:
                        message = "AI Multi-Jump Available!"
                        message_timer = 90
                        continue
                else:
                    moves_without_capture += 1
                if bonus_move_triggered:
                    message = "Warp Zone: Bonus Move!"
                    message_timer = 90
                    for row in range(BOARD_SIZE):
                        for col in range(BOARD_SIZE):
                            if board_before.get_piece(row, col) == 0 and board.get_piece(row, col) != 0:
                                last_moved_piece_pos = (row, col)
                                break
                        if last_moved_piece_pos:
                            break
                    board_before_bonus = deepcopy(board)
                    move_made, bonus_move_triggered = make_ai_move(board, "black", depth=3, allow_multi_jump=False)
                    if move_made:
                        captures_occurred = False
                        captured_on_warp_zone = False
                        for row in range(BOARD_SIZE):
                            for col in range(BOARD_SIZE):
                                piece_before = board_before_bonus.get_piece(row, col)
                                piece_after = board.get_piece(row, col)
                                if piece_before != 0 and piece_after == 0 and piece_before.color == "white":
                                    captures_occurred = True
                                    if is_in_warp_zone(row, col):
                                        captured_on_warp_zone = True
                                    break
                            if captures_occurred:
                                break
                        if captures_occurred and captured_on_warp_zone:
                            message = "Warp Zone: Capture Prevented!"
                            message_timer = 90
                            board.grid = board_before_bonus.grid
                            last_moved_piece_pos = None
                    else:
                        last_moved_piece_pos = None
                else:
                    last_moved_piece_pos = None
                current_turn = switch_turns(current_turn)
                turn_start_time = pygame.time.get_ticks()
                multi_jump_active = False

        if not game_over:
            white_pieces = count_pieces(board, "white")
            black_pieces = count_pieces(board, "black")
            if white_pieces == 0:
                print("No white pieces left. AI wins!")
                message = "AI Wins! Play Again?"
                message_timer = 0
                game_over = True
            elif black_pieces == 0:
                print("No black pieces left. Player wins!")
                message = "Player Wins! Play Again?"
                message_timer = 0
                game_over = True

            if not game_over:
                if current_turn == "white":
                    white_moves = get_all_valid_moves_for_player(board, "white")
                    if not white_moves:
                        print("Player has no valid moves. AI wins!")
                        message = "AI Wins! Play Again?"
                        message_timer = 0
                        game_over = True

        if moves_without_capture >= DRAW_THRESHOLD and not draw_prompt and not game_over:
            draw_prompt = True
            message = "Game heading toward a draw. Press D to draw."
            message_timer = 0

        if message_timer > 0:
            message_timer -= 1
            if message_timer == 0 and not draw_prompt and not game_over:
                message = ""

        # Fill the screen with a background color to clear the extra area
        screen.fill((0, 0, 0))  # Black background for the extra 50px at the bottom
        gui.draw_board()
        if current_turn == "white" and not game_over:
            highlight_valid_moves(screen, board, selected_piece)
        if message:
            gui.draw_message(message)
        draw_timer(screen, remaining_time)
        pygame.display.update()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()