import pygame
from .piece import Piece
from .constants import DARK_BROWN, ROWS, COLS, LIGHT_BROWN, SQUARE_SIZE, PIECES_IMG, LIGHT_BLUE, BLACK, WHITE, GRAY


class Board:
    def __init__(self, window) -> None:
        self.board = [[None for _ in range(COLS)] for _ in range(ROWS)]
        self.window = window
        self.set_pieces()
        self.current_piece = None
        self.possible_moves = set()
        self.blocked = False
        self.first_white_king_move = True
        self.first_white_rook_move = True
        self.first_black_king_move = True
        self.first_black_rook_move = True
        self.checkmate = False
        self.white_score = 0
        self.black_score = 0
        self.white_team, self.black_team = self.separate_teams()
        self.redraw_board(white_pieces = self.white_team, black_pieces = self.black_team)

    def draw_squares(self):
        self.window.fill(DARK_BROWN)
        for row in range(ROWS):
            for col in range(row % 2, ROWS, 2):
                pygame.draw.rect(self.window, LIGHT_BROWN, (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def set_pieces(self):
        for row in range(ROWS):
            for col in range(COLS):
                if row == 1:
                    self.board[row][col] = Piece(row, col, 'pawn', 'black', 1, PIECES_IMG['bp'], self.window)
                elif row == 6:
                    self.board[row][col] = Piece(row, col, 'pawn', 'white', 1, PIECES_IMG['wp'], self.window)
                elif row == 0 and (col == 0 or col == 7):
                    self.board[row][col] = Piece(row, col, 'rook', 'black', 5, PIECES_IMG['br'], self.window)
                elif row == 0 and (col == 1 or col == 6):
                    self.board[row][col] = Piece(row, col, 'knight', 'black', 3, PIECES_IMG['bk'], self.window)
                elif row == 0 and (col == 2 or col == 5):
                    self.board[row][col] = Piece(row, col, 'bishop', 'black', 3, PIECES_IMG['bb'], self.window)
                elif row == 0 and col == 3:
                    self.board[row][col] = Piece(row, col, 'queen', 'black', 9, PIECES_IMG['bq'], self.window)
                elif row == 0 and col == 4:
                    self.board[row][col] = Piece(row, col, 'king', 'black', 100, PIECES_IMG['bking'], self.window)
                elif row == 7 and (col == 0 or col == 7):
                    self.board[row][col] = Piece(row, col, 'rook', 'white', 5, PIECES_IMG['wr'], self.window)
                elif row == 7 and (col == 1 or col == 6):
                    self.board[row][col] = Piece(row, col, 'knight', 'white', 3, PIECES_IMG['wk'], self.window)
                elif row == 7 and (col == 2 or col == 5):
                    self.board[row][col] = Piece(row, col, 'bishop', 'white', 3, PIECES_IMG['wb'], self.window)
                elif row == 7 and col == 3:
                    self.board[row][col] = Piece(row, col, 'queen', 'white', 9, PIECES_IMG['wq'], self.window)
                elif row == 7 and col == 4:
                    self.board[row][col] = Piece(row, col, 'king', 'white', 100, PIECES_IMG['wking'], self.window)
                else:
                    self.board[row][col] = None

    def get_checkmate(self):
        return self.checkmate   

    def draw_pieces(self):
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece is not None:
                    Piece.draw_pieces(piece)

    def selected_piece(self, selected_row, selected_col):
        for row in range(ROWS):
            for col in range(COLS):
                if row == selected_row and col == selected_col:
                    self.current_piece = self.board[row][col]
                    if self.current_piece is not None:
                        self.current_piece = Piece.selected_piece(self.current_piece)
                        self.redraw_board(selected_piece = True, col = selected_col, row = selected_row)
                        return self.current_piece

    def redraw_board(self, **kwargs):
        selected_piece = kwargs.get("selected_piece", False)
        col = kwargs.get("col", None)
        row = kwargs.get("row", None)
        self.draw_squares()
        if selected_piece:
            pygame.draw.rect(self.window, LIGHT_BLUE, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))  
        self.draw_pieces()
        text = self.check_check()
        self.white_team, self.black_team = self.separate_teams()
        self.update_score(self.white_team, self.black_team, text)

    def _clear_piece(self):
        self.possible_moves = set()

    def move(self, selected_piece, piece_x, piece_y):
        temp_row, temp_col = selected_piece.row, selected_piece.col

        if selected_piece.piece_type == 'king':
            self.short_castle(selected_piece, piece_x, piece_y)
            self.long_castle(selected_piece, piece_x, piece_y)
        elif selected_piece.piece_type == 'pawn' and selected_piece.color == 'white' and piece_y == 0:
            selected_piece.piece_type = 'queen'
            selected_piece.img = PIECES_IMG['wq']
            selected_piece.value = 9
        elif selected_piece.piece_type == 'pawn' and selected_piece.color == 'black' and piece_y == 7:
            selected_piece.piece_type = 'queen'
            selected_piece.img = PIECES_IMG['bq']
            selected_piece.value = 9
            
        self.board[piece_y][piece_x] = None  # Clear the destination square
        self.board[piece_y][piece_x] = selected_piece  # Move the piece to the destination square
        Piece.move_piece(selected_piece, piece_y, piece_x)  # Update the piece's internal position
        self.board[temp_row][temp_col] = None  # Clear the original square

        # Update the score after the move
        self.redraw_board(score_update=True, white_pieces=self.white_team, black_pieces=self.black_team)

    def update_score(self, white_pieces, black_pieces, text = None):
        self.white_score, self.black_score = 0, 0
        for piece in white_pieces:
            self.white_score += piece.value
        for piece in black_pieces:
            self.black_score += piece.value
        
        if self.white_score < 100:
            text = "CHECKMATE BLACK WINS"
            self.checkmate = True
        elif self.black_score < 100:
            text = "CHECKMATE WHITE WINS"
            self.checkmate = True
        elif text == "CHECK!!!":
            text = "CHECK!!!"
        elif self.white_score > self.black_score and self.black_score > 100:
            text = f"White +{self.white_score - self.black_score}"
        elif self.black_score > self.white_score and self.white_score > 100:
            text = f"Black +{self.black_score - self.white_score}"
        
        self.display_score(text)

    def display_score(self, text = None):
        font = pygame.font.Font(pygame.font.get_default_font(), 36)
        text_color = (255, 255, 255)
        text_surface = font.render(text, True, text_color)
        self.window.blit(text_surface, (25, 813))

    def draw_calc_pos(self):     
        for coordinates in self.possible_moves:
                for x, y in self.possible_moves:
                    self.possible_x = SQUARE_SIZE * x + SQUARE_SIZE // 2
                    self.possible_y = SQUARE_SIZE * y + SQUARE_SIZE // 2
                    pygame.draw.circle(self.window, GRAY, (self.possible_x, self.possible_y), 10)


    def check_blocking(self, selected_piece):
        positions_to_remove = set()

        for x, y in self.possible_moves:
            if x < 0 or x >= 8 or y < 0 or y >= 8:
                positions_to_remove.add((x, y))
            else:
                if self.board[y][x] is not None:
                    blocking_piece = self.board[y][x]
                    if blocking_piece.color == selected_piece.color:
                        positions_to_remove.add((x, y))
                        
        self.possible_moves -= positions_to_remove    

    def find_non_none_elements(self):
        non_none_elements = [element for row in self.board for element in row if element is not None]
        return non_none_elements

    def check_check(self):
        non_none_elements = self.find_non_none_elements()
        for piece in non_none_elements:
            if piece != None:
                self.possible_move(piece, True)
                for x, y in piece.possible_moves:
                    self.attacking_piece = piece
                    if self.board[y][x] != None:
                        hitting_piece = self.board[y][x]
                        if hitting_piece.piece_type == 'king' and hitting_piece.color != piece.color:
                            return "CHECK!!!"
    
    def separate_teams(self):
        white_pieces = []
        black_pieces = []
        for piece in self.find_non_none_elements():
            if piece.color == "white":
                white_pieces.append(piece)
            else:
                black_pieces.append(piece)
        return white_pieces, black_pieces

    def short_castle(self, selected_piece, piece_x, piece_y, short_white_castle = False, short_black_castle = False):
        if selected_piece.piece_type == 'king':
            if selected_piece.color == 'white' and piece_x == 6 and piece_y == 7 and not short_white_castle:
                self.board[7][5] = self.board[7][7]
                Piece.move_piece(self.board[7][7], 7, 5)
                self.board[7][7] = None
            elif selected_piece.color == 'black' and piece_x == 6 and piece_y == 0 and not short_black_castle:
                self.board[0][5] = self.board[0][7]
                Piece.move_piece(self.board[0][7], 0, 5)
                self.board[0][7] = None

        if (selected_piece.piece_type == 'king' or selected_piece.piece_type == 'rook' and piece_x == 7) and selected_piece.color == 'white' and not short_white_castle:
            short_white_castle = True
        if (selected_piece.piece_type == 'king' or selected_piece.piece_type == 'rook' and piece_x == 7) and selected_piece.color == 'black' and not short_black_castle:
            short_black_castle = True

    def long_castle(self, selected_piece, piece_x, piece_y, long_white_castle = False, long_black_castle = False):
        if selected_piece.piece_type == 'king' and selected_piece.color == 'white' and piece_x == 2 and piece_y == 7 and not long_white_castle:
            self.board[7][3] = self.board[7][0]
            Piece.move_piece(self.board[7][0], 7, 3)
            self.board[7][0] = None
        elif selected_piece.piece_type == 'king' and selected_piece.color == 'black' and piece_x == 2 and piece_y == 0 and not long_black_castle:
            self.board[0][3] = self.board[0][0]
            Piece.move_piece(self.board[0][0], 0, 3)
            self.board[0][0] = None

        if (selected_piece.piece_type == 'king' or selected_piece.piece_type == 'rook' and piece_x == 2) and selected_piece.color == 'white' and not long_white_castle:
            long_white_castle = True
        if (selected_piece.piece_type == 'king' or selected_piece.piece_type == 'rook' and piece_x == 2) and selected_piece.color == 'black' and not long_black_castle:
            long_black_castle = True   

    def col_cross(self, selected_piece):
        movement = True
        i = 1
        flip = 1
        kill_piece = False
        while movement:
            if 0 <= (selected_piece.row) <= 7 and 0 <= (selected_piece.col - (i * flip)) <= 7 and not kill_piece:
                check_opening = self.board[selected_piece.row][selected_piece.col - (i * flip)]
                if check_opening == None or check_opening.color != selected_piece.color:
                    if check_opening != None and not kill_piece:
                        self.possible_moves.add((selected_piece.col - (i * flip), selected_piece.row))
                        kill_piece = True
                    else:
                        self.possible_moves.add((selected_piece.col - (i * flip), selected_piece.row))
                        i += 1
                elif check_opening != None and check_opening.color == selected_piece.color:
                    kill_piece = True
            elif flip == 1:
                i = 1
                flip = -1
                kill_piece = False
            else:
                movement = False

    def row_cross(self, selected_piece):
        movement = True
        i = 1
        flip = 1
        kill_piece = False
        while movement:
            if 0 <= (selected_piece.row + (i * flip)) <= 7 and 0 <= (selected_piece.col) <= 7 and not kill_piece:
                check_opening = self.board[selected_piece.row + (i * flip)][selected_piece.col]
                if check_opening == None or check_opening.color != selected_piece.color:
                    if check_opening != None and not kill_piece:
                        self.possible_moves.add((selected_piece.col, selected_piece.row + (i * flip)))
                        kill_piece = True
                    else:
                        self.possible_moves.add((selected_piece.col, selected_piece.row + (i * flip)))
                        i += 1
                elif check_opening != None and check_opening.color == selected_piece.color:
                    kill_piece = True
            elif flip == 1:
                i = 1
                flip = -1
                kill_piece = False
            else:
                movement = False

    def diagonal_up(self, selected_piece):
        movement = True
        i = 1
        flip = 1
        kill_piece = False
        while movement:
            if 0 <= (selected_piece.row - i) <= 7 and 0 <= (selected_piece.col + (i * flip)) <= 7 and not kill_piece:
                check_opening = self.board[selected_piece.row - i][selected_piece.col + (i * flip)]
                if check_opening == None or check_opening.color != selected_piece.color:
                    if check_opening != None and not kill_piece:
                        self.possible_moves.add((selected_piece.col + (i * flip), selected_piece.row - i))
                        kill_piece = True
                    else:
                        self.possible_moves.add((selected_piece.col + (i * flip), selected_piece.row - i))
                        i += 1
                elif check_opening != None and check_opening.color == selected_piece.color:
                    kill_piece = True
            elif flip == 1:
                i = 1
                flip = -1
                kill_piece = False
            else:
                movement = False
    
    def diagonal_down(self, selected_piece):
        movement = True
        i = 1
        flip = 1
        kill_piece = False
        while movement:
            if 0 <= (selected_piece.row + i) <= 7 and 0 <= (selected_piece.col - (i * flip)) <= 7 and not kill_piece:
                check_opening = self.board[selected_piece.row + i][selected_piece.col - (i * flip)]
                if check_opening == None or check_opening.color != selected_piece.color:
                    if check_opening != None and not kill_piece:
                        self.possible_moves.add((selected_piece.col - (i * flip), selected_piece.row + i))
                        kill_piece = True
                    else:
                        self.possible_moves.add((selected_piece.col - (i * flip), selected_piece.row + i))
                        i += 1
                elif check_opening != None and check_opening.color == selected_piece.color:
                    kill_piece = True
            elif flip == 1:
                i = 1
                flip = -1
                kill_piece = False
            else:
                movement = False

    def king_movement(self, selected_piece):
        self.possible_moves.add((selected_piece.col + 1, selected_piece.row))
        self.possible_moves.add((selected_piece.col - 1, selected_piece.row))
        self.possible_moves.add((selected_piece.col + 1, selected_piece.row + 1))
        self.possible_moves.add((selected_piece.col - 1, selected_piece.row - 1))
        self.possible_moves.add((selected_piece.col, selected_piece.row + 1))
        self.possible_moves.add((selected_piece.col, selected_piece.row - 1))
        self.possible_moves.add((selected_piece.col - 1, selected_piece.row + 1))
        self.possible_moves.add((selected_piece.col + 1, selected_piece.row - 1))
        if selected_piece.color == 'white' and self.board[7][5] == None and self.board[7][6] == None:
            self.possible_moves.add((6, 7))
        if selected_piece.color == 'white' and self.board[7][1] == None and self.board[7][3] == None:
            self.possible_moves.add((2, 7))
        if selected_piece.color == 'black' and self.board[0][5] == None and self.board[0][6] == None:
            self.possible_moves.add((6, 0))
        if selected_piece.color == 'black' and self.board[0][1] == None and self.board[0][3] == None:
            self.possible_moves.add((2, 0))

        self.check_blocking(selected_piece)
            
    def possible_move(self, selected_piece, possible_check = False):
        self._clear_piece()
        if selected_piece.color == 'white':
            direction_multiplier = 1
        else:
            direction_multiplier = -1

        if selected_piece.piece_type == 'pawn':
            if self.board[selected_piece.row - (1 * direction_multiplier)][selected_piece.col] == None:
                self.possible_moves.add((selected_piece.col, selected_piece.row - (1 * direction_multiplier)))
            if selected_piece.col != 7:
                if self.board[selected_piece.row - (1 * direction_multiplier)][selected_piece.col + 1]:
                    self.possible_moves.add((selected_piece.col + 1, selected_piece.row - (1 * direction_multiplier)))
            if selected_piece.col != 0:
                if self.board[selected_piece.row - (1 * direction_multiplier)][selected_piece.col - 1]:
                    self.possible_moves.add((selected_piece.col - 1, selected_piece.row - (1 * direction_multiplier)))
            if selected_piece.color == 'white' and selected_piece.row == 6 and self.board[selected_piece.row - 1][selected_piece.col] == None and self.board[selected_piece.row - 2][selected_piece.col] == None:
                self.possible_moves.add((selected_piece.col, selected_piece.row - 2))
            elif selected_piece.color == 'black' and selected_piece.row == 1 and self.board[selected_piece.row + 1][selected_piece.col] == None and self.board[selected_piece.row + 2][selected_piece.col] == None:
                self.possible_moves.add((selected_piece.col, selected_piece.row + 2))
        elif selected_piece.piece_type == 'knight':
            self.possible_moves.add((selected_piece.col + 1, selected_piece.row - 2))
            self.possible_moves.add((selected_piece.col - 1, selected_piece.row - 2))
            self.possible_moves.add((selected_piece.col + 1, selected_piece.row + 2))
            self.possible_moves.add((selected_piece.col - 1, selected_piece.row + 2))
            self.possible_moves.add((selected_piece.col - 2, selected_piece.row + 1))
            self.possible_moves.add((selected_piece.col - 2, selected_piece.row - 1))
            self.possible_moves.add((selected_piece.col + 2, selected_piece.row + 1))
            self.possible_moves.add((selected_piece.col + 2, selected_piece.row - 1))
        elif selected_piece.piece_type == 'rook':
            self.col_cross(selected_piece)
            self.row_cross(selected_piece)
        elif selected_piece.piece_type == 'bishop':
            self.diagonal_up(selected_piece)
            self.diagonal_down(selected_piece)
        elif selected_piece.piece_type == 'queen':
            self.col_cross(selected_piece)
            self.row_cross(selected_piece)
            self.diagonal_up(selected_piece)
            self.diagonal_down(selected_piece)
        elif selected_piece.piece_type == 'king':
            self.king_movement(selected_piece)

        self.check_blocking(selected_piece)
        Piece.update_possible_moves(selected_piece, self.possible_moves)

        if not possible_check:
            self.draw_calc_pos()

 