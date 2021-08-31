Welcome to Olivarius's Puzzle Maker!
There are two programs that build the puzzle. 
1. piece_maker.py 
	piece_maker.py takes in an image file containing all of the pieces and splits them, saving it in the "./pieces/" directory. This file need only been run once before making any puzzles from a group of pieces. Will work with "./31x31_pieces_together.png" by default.
	
2. puzzle_maker.py
	puzzle_maker.py uses the pieces in "./pieces/" to build a puzzle from the "./input_image.png" and will save it to "./output_image.png". The default dimensions are 20x20 pieces.