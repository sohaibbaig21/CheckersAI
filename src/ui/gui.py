import pygame
from pygame.locals import *
from typing import Tuple, Optional
from src.game.board import Board, Piece, get_valid_moves

WINDOW_SIZE = 600
SQUARE_SIZE = WINDOW_SIZE // 10
BOARD_SIZE = 10
LIGHT_SQUARE = (255, 255, 255)
DARK_SQUARE = (0, 0, 0)

class GUI:
    def __init__(self, screen: pygame.Surface, board: Board):
        self.screen = screen
        self.board = board
        self.font = pygame.font.SysFont("Arial", 24)

    def draw_board(self):
        self.screen.fill(LIGHT_SQUARE)
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if (row + col) % 2 != 0:
                    pygame.draw.rect(
                        self.screen,
                        DARK_SQUARE,
                        (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE),
                    )
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                piece = self.board.get_piece(row, col)
                if piece != 0:
                    self.draw_piece(piece)

    def draw_piece(self, piece: Piece):
        radius = SQUARE_SIZE // 2 - 10
        x = piece.col * SQUARE_SIZE + SQUARE_SIZE // 2
        y = piece.row * SQUARE_SIZE + SQUARE_SIZE // 2
        color = (255, 255, 255) if piece.color == "white" else (255, 0, 0)
        pygame.draw.circle(self.screen, color, (x, y), radius)
        if piece.king:
            pygame.draw.circle(self.screen, (255, 215, 0), (x, y), radius // 2)

    def draw_message(self, message: str, color: Tuple[int, int, int] = (139, 0, 0)):
        text = self.font.render(message, True, color)
        # Get the size of the text
        text_rect = text.get_rect()
        # Position in top-right corner with padding
        padding = 10
        text_rect.topright = (WINDOW_SIZE - padding, padding)
        # Draw a yellow background rectangle with padding
        background_rect = text_rect.inflate(padding * 2, padding * 2)  # Add padding around text
        pygame.draw.rect(self.screen, (255, 255, 0), background_rect)  # Yellow background
        # Draw the text on top
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