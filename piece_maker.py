from PIL import Image
import os
try:
	os.mkdir("./pieces")
except FileExistsError:
	pass

PIECE_OUTER_WIDTH  = 31
PIECE_OUTER_HEIGHT = 31

pieces_together_path = f".\\{PIECE_OUTER_WIDTH}x{PIECE_OUTER_HEIGHT}_pieces_together.png"

#Upper Left, Upper Right, Bottom Right, Bottom Left, Upper, Right, Bottom, Left, Middle
piece_names_for_rows = ["UL", "UR", "BR", "BL", "UP", "RT", "BT", "LT", "MD"]
num_of_pieces_in_rows = [4, 4, 4, 4, 8, 8, 8, 8, 16]

pieces_together = Image.open(pieces_together_path)
width, height = pieces_together.size

for name, num, i in zip(piece_names_for_rows, num_of_pieces_in_rows, range(0, height, PIECE_OUTER_HEIGHT)):
    for j in range(0, num*PIECE_OUTER_WIDTH, PIECE_OUTER_WIDTH):
        piece = pieces_together.crop((j, i, j+PIECE_OUTER_WIDTH, i+PIECE_OUTER_HEIGHT))
        piece.save(f"pieces/{name}_{j//PIECE_OUTER_HEIGHT}.png")