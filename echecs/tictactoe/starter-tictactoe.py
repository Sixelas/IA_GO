# -*- coding: utf-8 -*-

import time
import timeit
import Tictactoe 
from random import randint,choice
nb_games = 0
nb_nodes = 0
nb_gagne = 0
nb_perd = 0
nb_egal = 0


def RandomMove(b):
    '''Renvoie un mouvement au hasard sur la liste des mouvements possibles'''
    return choice(b.legal_moves())

def deroulementRandom(b):
    '''Effectue un déroulement aléatoire du jeu de morpion.'''
    print("----------")
    print(b)
    if b.is_game_over():
        res = getresult(b)
        if res == 1:
            print("Victoire de X")
        elif res == -1:
            print("Victoire de O")
        else:
            print("Egalité")
        return
    b.push(RandomMove(b))
    deroulementRandom(b)
    b.pop()


def getresult(b):
    '''Fonction qui évalue la victoire (ou non) en tant que X. Renvoie 1 pour victoire, 0 pour 
       égalité et -1 pour défaite. '''
    if b.result() == b._X:
        return 1
    elif b.result() == b._O:
        return -1
    else:
        return 0

def explore(b):
    '''Fonction qui retourne le nombre de parties possibles'''
    if b.is_game_over():
        global nb_games, nb_egal, nb_gagne, nb_perd
        nb_games = nb_games+1
        
        res = getresult(b)
        if res == 1:
            #print("Victoire de X")
            nb_gagne = nb_gagne+1
        elif res == -1:
            #print("Défaite")
            nb_perd = nb_perd+1
        else:
            #print("Egalité")
            nb_egal = nb_egal+1
        return
    else:
        for i in range (len(b.legal_moves())):
            b.push(b.legal_moves()[i])
            explore(b)
            global nb_nodes
            nb_nodes = nb_nodes+1
            b.pop()

def strategie(b, estX = True):
    '''Fonction qui cherche une startegie'''
    if b.is_game_over():
        global nb_games, nb_egal, nb_gagne, nb_perd
        nb_games = nb_games+1
        res = getresult(b)
        if res == 1:
            nb_gagne = nb_gagne+1
            return 1
            #print("Victoire de X")
        elif res == -1:
            nb_perd = nb_perd+1
            return -1
            #print("Defaite")
        else:
            nb_egal = nb_egal+1
            return 0
            #print("Egalite")
    else:
        for i in b.legal_moves():
            b.push(i)
            ret = strategie(b, not estX)
            if ret == 1 and estX:
                print("salut bg")
                b.pop()
                return 1
            if ret == -1 and not estX:  
                b.pop()
                return -1
            b.pop()

board = Tictactoe.Board()
print(board)

### Deroulement d'une partie aléatoire
'''deroulementRandom(board)'''
start = time.time()
#explore(board)
strategie(board, True)
end = time.time()

print("Nombre de parties/noeuds au total : ", nb_games, "/", nb_nodes, " Duree : ", end-start)
print("Parties gagnees : ", nb_gagne, " | Perdues : ", nb_perd, " | Egalite : ", nb_egal, " | Ratio : ", nb_gagne*100/nb_games, "%")

print("Apres le match, chaque coup est defait (grâce aux pop()): on retrouve le plateau de depart :")
print(board)

