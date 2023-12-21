import pygame
from os import listdir
from os.path import isfile, join

pygame.init()

# Window dimensions
WIDTH = 800
HEIGHT = 800

pygame.display.set_mode((WIDTH, HEIGHT))

# Board dimensions
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH//COLS

# RGB
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (105,105,105)
DARK_BROWN = (209, 139, 71)
LIGHT_BROWN = (255, 206, 158)
LIGHT_BLUE = (176,224,230)

# Pictures of Pieces
spritesheet = pygame.image.load('assets/ChessPieces.png')



sprite_width = 60
sprite_height = 60

sprites = []

rows_in_spritesheet = spritesheet.get_height() // sprite_height
cols_in_spritesheet = spritesheet.get_width() // sprite_width

# Extract individual sprites from the spritesheet
for row_index in range(rows_in_spritesheet):
    for col_index in range(cols_in_spritesheet):
        left = col_index * sprite_width
        upper = row_index * sprite_height
        right = left + sprite_width
        lower = upper + sprite_height
        sprite = spritesheet.subsurface(pygame.Rect(left, upper, sprite_width, sprite_height))
        sprites.append(sprite)


PIECES_IMG = {
    'wp': pygame.transform.scale(sprites[11].convert_alpha(), (75, 75)),
    'wr': pygame.transform.scale(sprites[8].convert_alpha(), (75, 75)),
    'wk': pygame.transform.scale(sprites[9].convert_alpha(), (75, 75)),
    'wb': pygame.transform.scale(sprites[10].convert_alpha(), (75, 75)),
    'wq': pygame.transform.scale(sprites[6].convert_alpha(), (75, 75)),
    'wking': pygame.transform.scale(sprites[7].convert_alpha(), (75, 75)),
    'bp': pygame.transform.scale(sprites[5].convert_alpha(), (75, 75)),
    'br': pygame.transform.scale(sprites[2].convert_alpha(), (75, 75)),
    'bk': pygame.transform.scale(sprites[3].convert_alpha(), (75, 75)),
    'bb': pygame.transform.scale(sprites[4].convert_alpha(), (75, 75)),
    'bq': pygame.transform.scale(sprites[0].convert_alpha(), (75, 75)),
    'bking': pygame.transform.scale(sprites[1].convert_alpha(), (75, 75))
}