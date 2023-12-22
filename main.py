import pygame
from Chess.game import Game
from Chess.constants import SQUARE_SIZE, HEIGHT, WIDTH
from Chess.piece import Piece

FPS = 60

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT + 50))
pygame.display.set_caption('Chess')

def get_pos(x, y):
    col = x // SQUARE_SIZE
    row = y // SQUARE_SIZE
    return row, col

def main():
    run = True
    clock = pygame.time.Clock()
    pygame.font.init()
    game = Game(WINDOW)
    selected_piece = None
    showing_possible_moves = False
    white_turn = True
    

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if game.get_checkmate():
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN and selected_piece == None:
                x, y = pygame.mouse.get_pos()
                row, col = get_pos(x, y)
                selected_piece = game.selected_piece(row, col)
                if selected_piece != None and selected_piece.color == 'white' and white_turn:
                    game.possible_moves(selected_piece)
                    showing_possible_moves = True
                elif selected_piece != None and selected_piece.color == 'black' and not white_turn:
                    game.possible_moves(selected_piece)
                    showing_possible_moves = True
                else:
                    selected_piece = None
            elif event.type == pygame.MOUSEBUTTONDOWN and showing_possible_moves:
                x, y = pygame.mouse.get_pos()
                row, col = get_pos(x, y)
                for piece_x, piece_y in selected_piece.possible_moves:
                    if col == piece_x and row == piece_y:
                        selected_piece = Piece.selected_piece(selected_piece)
                        game.move(selected_piece, piece_x, piece_y)
                        if selected_piece.color == 'black':
                            white_turn = True
                        else:
                            white_turn = False
                showing_possible_moves = False
                selected_piece = None
            
        game.update()
    pygame.quit()
main()