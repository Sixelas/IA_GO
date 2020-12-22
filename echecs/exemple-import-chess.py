import time
import chess
import chess.pgn
from random import randint

# Description des fin de parties de kasparov / deepblue http://www.chesscorner.com/games/deepblue/dblue4.htm

if True:
    pgn = open("kasparov-deepBlue-1997-4.pgn")  
    game = chess.pgn.read_game(pgn)
    game.headers
    board = game.board()
    moves = [move for move in game.main_line()]
    for m in moves[:-1]:
       board.push(m)
else:
    board = chess.Board()

# Ensuite vous mettez ce que vous voulez pour explorer les coups à partir de board

print(board)
