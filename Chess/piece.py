import pygame
from .constants import SQUARE_SIZE, BLACK


class Piece:
    def __init__(self, row, col, piece_type, color, value, img, window) -> None:
        self.window = window
        self.row = row
        self.col = col
        self.piece_type = piece_type
        self.color = color
        self.x = 0
        self.y = 0
        self.img = img
        self.value = value
        self._piece_init_()

    def _piece_init_(self):
        self.possible_x = self.x
        self.possible_y = self.y
        self.possible_moves = set()

    def calc_pos(self):
        self.x = SQUARE_SIZE * self.col + SQUARE_SIZE // 2
        self.y = SQUARE_SIZE * self.row + SQUARE_SIZE // 2
        
    def draw_pieces(self):
        self.calc_pos()
        self.window.blit(self.img, (self.x - self.img.get_width() // 2, self.y - self.img.get_height() // 2))

    def move_piece(self, piece_y, piece_x):
        self.row = piece_y
        self.col = piece_x

    def selected_piece(self):
        return self

    def update_possible_moves(self, possible_moves):
        self.possible_moves = possible_moves
            