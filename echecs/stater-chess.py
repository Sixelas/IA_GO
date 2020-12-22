# -*- coding: utf-8 -*-

import time
import chess
import chess.svg
from PIL import Image
import cairosvg
import subprocess
from random import randint, choice

nb_nodes = 0
t_turn = 0
tmpCoupPlayer = 0
tmpCoupNotPlayer = 0
import os
running = True

def randomMove(b):
    '''Renvoie un mouvement au hasard sur la liste des mouvements possibles. Pour avoir un choix au hasard, il faut
    construire explicitement tous les mouvements. Or, generate_legal_moves() nous donne un itérateur.'''
    return choice([m for m in b.generate_legal_moves()])

def choose_lvl(board, t, lvl):
    nb_pieces = len(board.piece_map())  
    if(nb_pieces<=6):
        lvl = 5
    if(nb_pieces<=16):
        lvl = 4
    if(t>100):
        lvl = 5
    if(nb_pieces<=4):
        lvl = 6
    return lvl

def server_command(cmd):

    if(cmd == ""):
        print("Test Mode")
        fun = chess.Board('K7/8/8/8/8/1R6/R7/7k')
        testBoard = chess.Board('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR')
        start = time.time()
        launcher_cmd(fun, True,0, 3, 0, True)
        end = time.time()
        print("Durée de la partie : ",end-start, "s")
        return

    graphismes = False
    commandes = cmd.split('-')
    if(len(commandes)!= 3):
        print("Mauvaise commande")
        return

    lvl1 = int(commandes[0])
    if(lvl1<1):
        print("Ça fait peu quand même du lvl ",lvl1," non ?")
        return
    elif(lvl1>6):
        print("Ça fait beaucoup quand même du lvl ",lvl1," non ?")
        return

    lvl2 = int(commandes[1])
    if(lvl2>6):
        print("Ça fait beaucoup quand même du lvl ", lvl2," non ?")
        return

    if(commandes[2] != '0' and commandes[2] != '1'):
        print("Le mode graphique ", commandes[2], " n'existe pas")
        return  

    if(commandes[2] == '1'):
        graphismes = True

    print("Commande : <",lvl1,",",lvl2,",",graphismes,">")
    board = chess.Board()
    start = time.time()
    launcher_cmd(board, True,0, lvl1, lvl2, graphismes)
    end = time.time()
    print("Durée de la partie : ",end-start, "s")


def Bvalue(b):#On renvoie une valeur qui est la meme quelque soit le joueur, C'est a lui de traiter l'information
    value = 0
    tab = {'p':1, 'b':3, 'n':3, 'r':5, 'q':9, 'k':9}
    pieces = [p.symbol() for p in b.piece_map().values()]
    pos = [p for p in b.piece_map()]
    for i, j in zip(pieces, pos):
        Bonus = 1
        if(i == i.lower()):
            if i == 'p':
                Bonus = (64-j)//8
            value = value-(tab[i]*Bonus)
        else:
            if i == 'P':
                Bonus = j//8
                if (Bonus < 4):
                    Bonus = 1
                elif (Bonus == 4):
                    Bonus = 3
            value = value+(tab[i.lower()]*Bonus)
    if b.is_checkmate() :
        if b.turn:
            value -= 3000
        else:
            value += 3000
    return value

#version alpha beta
def minmaxAB(b, profondeur, player, maxP, alpha, beta):
    global tmpCoup
    if((profondeur==maxP) or (b.is_game_over())):
        return Bvalue(b)
    if(player):
        maxEval = -10000
        for i in b.generate_legal_moves():
            b.push(i)
            tmpcoupPlayer = i
            r = minmaxAB(b, profondeur+1, not player, maxP, alpha, beta)
            b.pop()
            maxEval = max(maxEval,r)
            alpha = max(alpha, r)
            if (r>1500):
                return maxEval
            if (beta <= alpha):
                break
        return maxEval
    else:
        minEval = 10000
        for i in b.generate_legal_moves():
            b.push(i)
            tmpcoupNotPlayer = i
            r = minmaxAB(b, profondeur+1, not player, maxP, alpha, beta)
            b.pop()
            minEval = min(minEval,r)
            beta = min(beta, r)
            if (r<-1500):
                return minEval
            if(beta <= alpha):
                break
        return minEval

def PlayerTurn(board, maxP, player):
    if board.is_game_over():
        res = b.result()
        print(res)
    if player:
        opti = -10000
    else:
        opti = 10000
    coups = []
    for i in board.generate_legal_moves():
        board.push(i)
        res = minmaxAB(board,0,player,maxP,-10000,+10000)    #Ici pour choisir alpha beta ou non
        tmpsave = i
        board.pop()
        if player:
            if res>1500 : #MAT TROUVÉ
                return tmpsave
            elif res>opti :
                opti = res
                coups.clear()
                coups.append(i)
            elif(res == opti):
                coups.append(i)
        else:
            if res>1500 : #MAT TROUVÉ
                return tmpsave
            if res<opti :
                opti = res
                coups.clear()
                coups.append(i)
            elif(res == opti):
                coups.append(i)
    return choice(coups)

def launcher_cmd(board, player, t, lvl1, lvl2, graphismes ):
    global t_turn
    if (lvl2 != 0):
        lvl1 = choose_lvl(board, t, lvl1)
        lvl2 = choose_lvl(board, t, lvl2)
    else : 
        lvl1 = choose_lvl(board, t, lvl1)

    if(graphismes):
        boardsvg = chess.svg.board(board=board)
        f = open("BoardVisu.svg", "w")
        f.write(boardsvg)
        f.close()
        cairosvg.svg2png(url='BoardVisu.svg', write_to='BoardVisu.png')
        p = subprocess.Popen(["display", "BoardVisu.png"])
        time.sleep(1)
        p.kill()
    
    print(" ")
    print("------Turn ",t, " | Lvl1/lvl2 ",lvl1,"/",lvl2," | player ",not player," | durée tour : ",t_turn,"s ------")
    print(board)
    if(board.is_game_over()):
        print("Resultat : ", board.result())
        return
    if(player):
        start = time.time()
        board.push(PlayerTurn(board, lvl1, True))
        end = time.time()
        t_turn = round(end-start,2)
        
    else:
        start = time.time()
        if(lvl2 == 0):
            board.push(randomMove(board))
        else :
            board.push(PlayerTurn(board, lvl2, False)) #ICI à voir si PlayerTurn est good ou pas, ça dépend de son appel à minmaxAB
        end = time.time()
        t_turn = round(end-start,2)

    launcher_cmd(board, not player, t+1, lvl1, lvl2, graphismes)
    board.pop()

print('------------------------')
print('|     Chess Starter     |')
print('------------------------')
 

while running:
    print("Choisissez le mode de jeu sous cette forme : <x-y-g>")   
    print("<x> = lvl ia Blancs (entre 1 et 6 maximum) ")
    print("<y> = lvl ia Noirs (entre 0 et 6 maximum) 0=random ")
    print("<g> = graphismes ou non, 0=non, 1=oui")
    command = input()
    server_command(command)
    break
