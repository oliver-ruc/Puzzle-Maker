#Left, Down, Right, Up   (Up is least significant bit)
from random import randrange
from PIL import Image
import numpy as np
rows=20    #choose
columns=20 #choose

PIECE_OUTER_WIDTH  = 31
PIECE_OUTER_HEIGHT = 31
PIECE_INNER_WIDTH  = 19
PIECE_INNER_HEIGHT = 19

input_image_path = "./input_image.png"
output_image_path = "./puzzle_img.png"

PIECE_WIDTH_EXTEND  = (PIECE_OUTER_WIDTH  - PIECE_INNER_WIDTH ) // 2
PIECE_HEIGHT_EXTEND = (PIECE_OUTER_HEIGHT - PIECE_INNER_HEIGHT) // 2

board = []
for i in range(rows):
    line = []
    for j in range(columns):
        line.append(randrange(16))
    board.append(line)
for i in range(rows):
    for j in range(columns-1):
        board[i][j+1] &= 0b0111
        board[i][j+1] |= ((~board[i][j]) & 0b0010) << 2
for i in range(rows-1):
    for j in range(columns):
        board[i+1][j] &= 0b1110
        board[i+1][j] |= ((~board[i][j]) & 0b0100)  >> 2
def check(homies):
    for i in range(len(homies)-1):
        for j in range(len(homies[0])-1):
            if (bool(homies[i][j] & 0b0010) == bool(homies[i][j+1] & 0b1000)) or\
               (bool(homies[i][j] & 0b0100) == bool(homies[i+1][j] & 0b0001)):
                return False
    return True
print(check(board))
#Left, Down, Right, Up   (Up is least significant bit)
convert = ["4x0", "3x1", "3x1", "2x2 next", "3x1", "2x2 across", "2x2 next", "1x3", "3x1", "2x2 next", "2x2 across", "1x3", "2x2 next", "1x3", "1x3", "0x4"]
counter = {}
for i in convert:
    counter[i] = 0
for row in board:
    for piece in row:
        counter[convert[piece]] += 1
print(counter)

# PIECE_DIMENSION = 31
PIECE_OUTER_WIDTH  = 31
PIECE_OUTER_HEIGHT = 31
PIECE_INNER_WIDTH  = 19
PIECE_INNER_HEIGHT = 19
MAX_WIDTH_NOISE  = 2
MAX_HEIGHT_NOISE = 2
PIECE_WIDTH_EXTEND  = (PIECE_OUTER_WIDTH  - PIECE_INNER_WIDTH ) // 2
PIECE_HEIGHT_EXTEND = (PIECE_OUTER_HEIGHT - PIECE_INNER_HEIGHT) // 2



WIDTH = columns * PIECE_OUTER_WIDTH
HEIGHT = rows * PIECE_OUTER_HEIGHT
puzzle_image = Image.new("RGBA", (WIDTH, HEIGHT))

input_image = Image.open(input_image_path)
input_image = input_image.resize((columns * PIECE_INNER_WIDTH, rows * PIECE_INNER_HEIGHT))
width, height = input_image.size
padded_image = Image.new("RGBA", (width + PIECE_WIDTH_EXTEND * 2, height + PIECE_HEIGHT_EXTEND * 2))
padded_image.paste(input_image, (PIECE_WIDTH_EXTEND, PIECE_HEIGHT_EXTEND))
padded_image.show()

black_pieces = [[0] * columns for _ in range(rows)]
#CORNERS
UL_num = (board[0][0] >> 1) & 0b0011
UL_img = Image.open(f"./pieces/UL_{UL_num}.png")
black_pieces[0][0] = UL_img

UR_num = (board[0][-1] >> 2) & 0b0011
UR_img = Image.open(f"./pieces/UR_{UR_num}.png")
black_pieces[0][-1] = UR_img

BR_num = ((board[-1][-1] & 0b1000) >> 3) | ((board[-1][-1] &0b0001) << 1)
BR_img = Image.open(f"./pieces/BR_{BR_num}.png")
black_pieces[-1][-1] = BR_img

BL_num = board[-1][0] & 0b0011
BL_img = Image.open(f"./pieces/BL_{BL_num}.png")
black_pieces[-1][0] = BL_img

#UPPER AND BOTTOM ROWS
for i in range(1, columns-1):
    UP_num = (board[0][i] >> 1) & 0b0111
    UP_img = Image.open(f"./pieces/UP_{UP_num}.png")
    black_pieces[0][i] = UP_img
    BT_num = ((board[-1][i] & 0b1000) >> 3) | ((board[-1][i] & 0b0011) << 1)
    BT_img = Image.open(f"./pieces/BT_{BT_num}.png")
    black_pieces[-1][i] = BT_img

#LEFT AND RIGHT COLUMNS
for i in range(1, rows-1):
    RT_num = ((board[i][-1] & 0b1100) >> 2) | ((board[i][-1] & 0b0001) << 2)
    RT_img = Image.open(f"./pieces/RT_{RT_num}.png")
    black_pieces[i][-1] = RT_img
    LT_num = board[i][0] & 0b0111
    LT_img = Image.open(f"./pieces/LT_{LT_num}.png")
    black_pieces[i][0] = LT_img

#MIDDLE OF THE PUZZLE
for i in range(1, rows-1):
    for j in range(1, columns-1):
        MD_num = board[i][j]
        MD_img = Image.open(f"./pieces/MD_{MD_num}.png")
        black_pieces[i][j] = MD_img

for i, y in enumerate(range(0, HEIGHT, PIECE_OUTER_HEIGHT)):
    for j, x in enumerate(range(0, WIDTH, PIECE_OUTER_WIDTH)):
        black_piece = black_pieces[i][j]
        cropped_rect = (j * PIECE_INNER_WIDTH, i * PIECE_INNER_HEIGHT, j * PIECE_INNER_WIDTH + PIECE_OUTER_WIDTH, i * PIECE_INNER_HEIGHT + PIECE_OUTER_HEIGHT)
        cropped_piece = padded_image.crop(cropped_rect)
        black_array = np.asarray(black_piece)
        cropped_array = np.asarray(cropped_piece)
        final_piece=Image.fromarray(np.append(np.maximum(black_array[:,:,:3], cropped_array[:,:,:3]), np.minimum(black_array[...,3], cropped_array[...,3])[:,:,np.newaxis], axis=2))
        puzzle_image.paste(final_piece, (x, y, x + PIECE_OUTER_WIDTH, y + PIECE_OUTER_HEIGHT))

puzzle_image.save(output_image_path)
puzzle_image.show()