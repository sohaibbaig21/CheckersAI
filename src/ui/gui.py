import pygame
from pygame.locals import *
from typing import Tuple, Optional
from src.game.board import Board, Piece, get_valid_moves, is_in_warp_zone

WINDOW_SIZE = 600
SQUARE_SIZE = WINDOW_SIZE // 10
BOARD_SIZE = 10
LIGHT_SQUARE = (255, 255, 255)
DARK_SQUARE = (0, 0, 0)
WARP_ZONE_COLOR = (0, 0, 255)  # Blue for warp zone
WARP_ZONE_BORDER = (0, 0, 0)  # Black border for warp zone

class GUI:
    def __init__(self, screen: pygame.Surface, board: Board):
        self.screen = screen
        self.board = board
        self.font = pygame.font.SysFont("Arial", 24)
        self.animating_piece = None
        self.animation_start = None
        self.animation_end = None
        self.animation_progress = 0
        self.ANIMATION_DURATION = 500  # Animation duration in milliseconds

    def draw_board(self):
        self.screen.fill(LIGHT_SQUARE)
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if (row + col) % 2 != 0:
                    if is_in_warp_zone(row, col):
                        # Draw warp zone tile (blue with black border)
                        pygame.draw.rect(
                            self.screen,
                            WARP_ZONE_COLOR,
                            (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE),
                        )
                        pygame.draw.rect(
                            self.screen,
                            WARP_ZONE_BORDER,
                            (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE),
                            2,  # Border thickness
                        )
                    else:
                        pygame.draw.rect(
                            self.screen,
                            DARK_SQUARE,
                            (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE),
                        )
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                piece = self.board.get_piece(row, col)
                if piece != 0 and (self.animating_piece is None or piece != self.animating_piece):
                    self.draw_piece(piece)
        if self.animating_piece:
            self.draw_animating_piece()

    def draw_piece(self, piece: Piece):
        radius = SQUARE_SIZE // 2 - 10
        x = piece.col * SQUARE_SIZE + SQUARE_SIZE // 2
        y = piece.row * SQUARE_SIZE + SQUARE_SIZE // 2
        color = (255, 255, 255) if piece.color == "white" else (255, 0, 0)
        pygame.draw.circle(self.screen, color, (x, y), radius)
        if piece.king:
            pygame.draw.circle(self.screen, (255, 215, 0), (x, y), radius // 2)

    def draw_animating_piece(self):
        if not self.animating_piece:
            return
        radius = SQUARE_SIZE // 2 - 10
        start_x = self.animation_start[1] * SQUARE_SIZE + SQUARE_SIZE // 2
        start_y = self.animation_start[0] * SQUARE_SIZE + SQUARE_SIZE // 2
        end_x = self.animation_end[1] * SQUARE_SIZE + SQUARE_SIZE // 2
        end_y = self.animation_end[0] * SQUARE_SIZE + SQUARE_SIZE // 2
        # Linear interpolation for smooth movement
        x = start_x + (end_x - start_x) * self.animation_progress
        y = start_y + (end_y - start_y) * self.animation_progress
        color = (255, 255, 255) if self.animating_piece.color == "white" else (255, 0, 0)
        pygame.draw.circle(self.screen, color, (x, y), radius)
        if self.animating_piece.king:
            pygame.draw.circle(self.screen, (255, 215, 0), (x, y), radius // 2)

    def start_animation(self, piece: Piece, start_pos: Tuple[int, int], end_pos: Tuple[int, int]):
        self.animating_piece = piece
        self.animation_start = start_pos
        self.animation_end = end_pos
        self.animation_progress = 0

    def update_animation(self, current_time: int):
        if not self.animating_piece:
            return False
        elapsed = current_time - self.animation_start_time
        self.animation_progress = min(elapsed / self.ANIMATION_DURATION, 1.0)
        if self.animation_progress >= 1.0:
            self.animating_piece = None
            return False
        return True

    def draw_message(self, message: str, color: Tuple[int, int, int] = (139, 0, 0)):
        text = self.font.render(message, True, color)
        text_rect = text.get_rect()
        padding = 10
        text_rect.topright = (WINDOW_SIZE - padding, padding)
        background_rect = text_rect.inflate(padding * 2, padding * 2)
        pygame.draw.rect(self.screen, (255, 255, 0), background_rect)
        self.screen.blit(text, text_rect)

def get_tile_at_mouse_pos(mouse_pos: Tuple[int, int]) -> Tuple[int, int]:
    row = mouse_pos[1] // SQUARE_SIZE
    col = mouse_pos[0] // SQUARE_SIZE
    return row, col

def highlight_valid_moves(screen: pygame.Surface, board: Board, selected_piece: Optional[Tuple[int, int]]):
    if not selected_piece:
        return
    row, col = selected_piece
    valid_moves = get_valid_moves(board, row, col)
    for move_row, move_col in valid_moves:
        pygame.draw.rect(
            screen,
            (0, 255, 0),
            (move_col * SQUARE_SIZE, move_row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE),
            3,
        )
