# -*- coding: utf-8 -*-
''' This is the file you have to modify for the tournament. Your default AI player must be called by this module, in the
myPlayer class.

Right now, this class contains the copy of the randomPlayer. But you have to change this!
'''

import time
import Goban 
from random import choice
from playerInterface import *

def compterPierres(self, board):
    score = [0, 0]
    for i in range (1,9):
        for j in range (1,9):
            tmpColor = board.flatten((i,j))
            if tmpColor == 1:#black
                score[0] += 1 
            elif tmpColor == 2:#white
                score[1] += 1
    return score

def boardValue(self, board):
    test = compterPierres(self, board)
    return test[0] - test[1]


def minimax(self, board, profondeur, joueurMax):
    if profondeur == 0:
        return boardValue(self, board)
    moves = board.legal_moves()
    if joueurMax:#Black
        scoreBoard = -1000
        for i in moves:
            self._board.push(i)
            testCoup = max(scoreBoard, minimax(self, board, profondeur-1, False))
            self._board.pop()
        return scoreBoard
    else:#White
        scoreBoard = 1000
        for i in moves:
            self._board.push(i)
            testCoup = min(scoreBoard, minimax(self, board, profondeur-1, True))
            self._board.pop()
        return scoreBoard
    print("pas normal d'etre la")
    return


class myPlayer(PlayerInterface):
    ''' Example of a random player for the go. The only tricky part is to be able to handle
    the internal representation of moves given by legal_moves() and used by push() and 
    to translate them to the GO-move strings "A1", ..., "J8", "PASS". Easy!

    '''

    def __init__(self):###INTERFACE
        self._board = Goban.Board()
        self._mycolor = None

    def getPlayerName(self):###INTERFACE
        return "PogChamp l'incroyable"

    def getPlayerMove(self):###INTERFACE
        if self._board.is_game_over():
            print("Referee told me to play but the game is over!")
            return "PASS" 

        #A PARTIR D'ICI ALGO
        profMinimax = 2
        moves = self._board.legal_moves() #Ajouter le weak et faire liste d'attente de coups
        scoreBoard = -1000
        meilleurCoup = []
        a = self._mycolor
        print(a)

        for i in moves:
            self._board.push(i)
            testCoup = minimax(self, self._board, profMinimax-1, self._mycolor)
            self._board.pop()
            if scoreBoard<testCoup:
                scoreBoard = testCoup
                meilleurCoup.clear()
                meilleurCoup.append(i)
            elif scoreBoard==testCoup:
                meilleurCoup.append(i)

        move = choice(meilleurCoup) 
        self._board.push(move)

        # New here: allows to consider internal representations of moves
        print("I am playing ", self._board.move_to_str(move))
        print("My current board :")
        self._board.prettyPrint()
        # move is an internal representation. To communicate with the interface I need to change if to a string
        return Goban.Board.flat_to_name(move) 

    def playOpponentMove(self, move):###INTERFACE
        print("Opponent played ", move) # New here
        # the board needs an internal represetation to push the move.  Not a string
        self._board.push(Goban.Board.name_to_flat(move)) 

    def newGame(self, color):###INTERFACE
        self._mycolor = color
        self._opponent = Goban.Board.flip(color)

    def endGame(self, winner):###INTERFACE
        if self._mycolor == winner:
            print("I won!!!")
        else:
            print("I lost :(!!")



