import pygame
from .board import Board
from .constants import WHITE


class Game():
    def __init__(self, window) -> None:
        self.win = window
        self.board = Board(window)

    def update(self):
        pygame.display.update()

    def selected_piece(self, row, col):
        return self.board.selected_piece(row, col)
    
    def move(self, selected_piece, piece_x, piece_y):
        self.board.move(selected_piece, piece_x, piece_y)

    def possible_moves(self, selected_piece):
        self.board.possible_move(selected_piece)

    def get_checkmate(self):
        return self.board.get_checkmate()