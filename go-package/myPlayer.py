# -*- coding: utf-8 -*-
''' This is the file you have to modify for the tournament. Your default AI player must be called by this module, in the
myPlayer class.

Right now, this class contains the copy of the randomPlayer. But you have to change this!
'''

import Goban
import os.path
import json
import time
import Goban 
from random import choice
from playerInterface import *
tmpCoupPlayer = []
games_dict = {}
gamesPossiblesJson = []
nbMove = 0
choixStrat = 0
triggerPartiePro = True
triggerWinPass = False


#On regarde la pierre a jouer au coup n°numMove de la partie n°partie
def jsonCoupAJouer(self, board, numMove):
    global triggerPartiePro, choixStrat, gamesPossiblesJson, games_dict
    if self._mycolor == 1:#Black   
        moveName = games_dict[choixStrat]['moves'][numMove]
        return board.flatten(board.name_to_coord(moveName))
    else:#White
        partie = choice(gamesPossiblesJson)
        moveName = games_dict[partie]['moves'][numMove]
        return board.flatten(board.name_to_coord(moveName))
        

def updateJson(self, move):
    global gamesPossiblesJson, games_dict, nbMove, triggerPartiePro
    if self._mycolor == 2:#white
        for i in gamesPossiblesJson:
            try:
                if games_dict[i]['moves'][nbMove] != move:#Le coup joué ne correspond pas a une partie du json
                    gamesPossiblesJson.remove(i)
            except IndexError:
                triggerPartiePro = False
        if not(gamesPossiblesJson):#Pas de stratégie copiée
            triggerPartiePro = False



def checkWinPass(self):
    global triggerWinPass
    if self._mycolor == 1:
        if boardValue(self, self._board) > 0:
            triggerWinPass = True
    else:
        if boardValue(self, self._board) < 0:
            triggerWinPass = True

#Compte les pierres du plateau
def compterPierres(self, board):
    score = [0, 0]
    for i in range (1,9):
        for j in range (1,9):
            tmpColor = board[board.flatten((i,j))]
            if tmpColor == 1:#black
                score[0] += 1 
            elif tmpColor == 2:#white
                score[1] += 1
    return score


#Donne une value a un plateau (score du plateau pour le minimax)
def boardValue(self, board):
    test = board._count_areas()
    return test[0] - test[1]



#Minimax alphabeta classique
def minimaxAB(self, board, profondeur, maximizing, maxP, alpha, beta):
    global tmpCoupPlayer, tmpCoupNotPlayer
    if((profondeur==maxP) or (self._board.is_game_over())):
        return boardValue(self, board)
    if(not maximizing):
        value = 1000
        for i in self._board.legal_moves():
            self._board.push(i)
            value = min(value, minimaxAB(self, board, profondeur+1, maximizing, maxP, alpha, beta))
            self._board.pop()
            if alpha > value:
                return value
            beta = min(beta, value)
    else:
        value = -1000
        for i in self._board.legal_moves():
            self._board.push(i)
            value = max(value, minimaxAB(self, board, profondeur+1, maximizing, maxP, alpha, beta))
            self._board.pop()
            if value > beta:
                return value
            alpha = max(alpha,value)
    return value



class myPlayer(PlayerInterface):
    ''' Example of a random player for the go. The only tricky part is to be able to handle
    the internal representation of moves given by legal_moves() and used by push() and 
    to translate them to the GO-move strings "A1", ..., "J8", "PASS". Easy!

    '''

    def __init__(self):###INTERFACE
        self._board = Goban.Board()
        self._mycolor = None
        self._timer = 300#secondes

    def getPlayerName(self):###INTERFACE
        return "GO-u-L@g"

    def getPlayerMove(self):###INTERFACE
        global nbMove, choixStrat, triggerPartiePro, triggerWinPass
        start = time.time()
        if nbMove==20:
            triggerPartiePro = False
        if self._board.is_game_over() or triggerWinPass:
            print("Referee told me to play but the game is over!")
            return "PASS" 
        move = None
        finTimer = time.time() + self._timer/len(self._board.legal_moves())
        while time.time() < finTimer:

            ###ALGO 1 : Copie/Test Copie partie Json
            if nbMove<20 and triggerPartiePro:    #Si la partie est pas trop avancée et que l'adversaire copie une partie du json pour l'ouverture
                if self._mycolor == 1:#Black      #Ou qu'on ouvre et qu'on peut déployer la stratégie professionelle
                    move = jsonCoupAJouer(self, self._board, nbMove+1)
                else:#White
                    move = jsonCoupAJouer(self, self._board, nbMove+1)
                if move not in self._board.legal_moves():
                    triggerPartiePro = False

            ###ALGO 2 : On fait tourner normalement notre jeu (minimax)
            if triggerPartiePro == False:
                profMinimax = 1
                meilleurCoup = []
                moves = self._board.legal_moves()

                #Choix totalement arbitraire
                if len(moves)<20:
                    profMinimax = 2
                if len(moves)<12:
                    profMinimax = 3
                if len(moves)<3:
                    profMinimax = 2
                if len(moves)<2:
                    profMinimax = 1

                if self._mycolor == 1:#Black
                    maximizing = True
                    scoreMeilleurCoup = -1000
                else:
                    maximizing = False
                    scoreMeilleurCoup = 1000

                for j in moves:
                    self._board.push(j)
                    testCoup = minimaxAB(self, self._board, 0, maximizing, profMinimax, -100, +100)
                    self._board.pop()
                    if maximizing:#black
                        if scoreMeilleurCoup<testCoup:
                            scoreMeilleurCoup = testCoup
                            meilleurCoup.clear()
                            meilleurCoup.append(j)
                        elif scoreMeilleurCoup==testCoup:
                            meilleurCoup.append(j)
                    else:#white
                        if scoreMeilleurCoup>testCoup:
                            scoreMeilleurCoup = testCoup
                            meilleurCoup.clear()
                            meilleurCoup.append(j)
                        elif scoreMeilleurCoup==testCoup:
                            meilleurCoup.append(j)
                move = choice(meilleurCoup)


                if len(tmpCoupPlayer)==1:#Que le pass dedans, pas sensé arriver
                    print("Etrange monsieur l'arbitre, demande de VAR")
                    self._board.push(move)
                else:
                    while move=='PASS':#On a prit un des coups au hasard, mais on va éviter de passer
                        move = choice(tmpCoupPlayer)
        if time.time() < finTimer:
            move = choice(tmpCoupPlayer)
        ###FIN DES ALGOS : renvoi du coup
        
        nbMove += 1
        self._board.push(move)
        end = time.time()
        print("Durée du tour : ",end-start, "s")
        self._timer -= (end-start)

        # New here: allows to consider internal representations of moves
        print("I am playing ", self._board.move_to_str(move))
        print("My current board :")
        self._board.prettyPrint()
        # move is an internal representation. To communicate with the interface I need to change if to a string
        return Goban.Board.flat_to_name(move) 

    def playOpponentMove(self, move):###INTERFACE
        global nbMove
        print("Opponent played ", move) # New here
        # the board needs an internal represetation to push the move.  Not a string
        nbMove += 1
        updateJson(self, move)
        self._board.push(Goban.Board.name_to_flat(move))
        if move == -1:#Adversaire a pass
            checkWinPass(self)

    def newGame(self, color):###INTERFACE
        global gamesPossiblesJson, games_dict, choixStrat, triggerPartiePro
        self._mycolor = color
        self._opponent = Goban.Board.flip(color)
        try :
            with open(os.path.dirname(__file__) + '/../games.json') as json_games:
                games_dict = json.load(json_games)
                for i in range(len(games_dict)):
                    gamesPossiblesJson.append(i)
        except:
            #Pas de json pour la bagarre :'(
            triggerPartiePro = False
            
        if self._mycolor == 1:#Black
            choixStrat = choice(gamesPossiblesJson)



    def endGame(self, winner):###INTERFACE
        if self._mycolor == winner:
            print("I won!!!")
        else:
            print("I lost :(!!")



