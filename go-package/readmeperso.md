Nous avons plusieurs variables globales:
- tmpCoupPlayer -> Stocke temporairement le coup de notre joueur (utile 
pour minimax)
- tmpCoupNotPlayer -> La même chose pour le coup adverse
- games_dict -> Contient toutes les parties en json
- gamesPossiblesJson -> Contient un index des parties potentiellement
jouées par notre adversaire dans le cas où celui ci reproduirait
une stratégie préparée contenue dans le json
- nbMove -> Pour traquer plus efficacement à quel coup on est de facon
à itérer sur notre dictionnaire et choisir quelle stratégie (entre partie
préfaite et minimax) adopter.
- choixStrat -> Le choix de la partie à imiter en tant que joueur noir pour
une ouverture efficace à moindre cout
- triggerPartiePro -> Reste a True tant que l'adversaire joue 
potentiellement une partie du json. Passe a False si plus de correspondance.

Nous avons ajouté 2 bibliotheques : os et json

Fonctions de l'interface :

    newGame:
    Va initialiser un dictionnaire contenant toutes les parties du json en
    vue de nos stratégies futures. Si l'on est noir, on choisit une stratégie
    à suivre au hasard parmi celles du json.

    getPlayerName : Bienvenue à GO-u-L@g

    endGame : Pas modifié

    playOpponentMove : La seule différence est qu'on augmente notre compteur
    de coups joués

    __init__ : Ajout du timer.

    getPlayerMove : Evidemment beaucoup modifié. Ajout du timer pour 
    chronometrer les tours, ajout d'une premiere itération du minimax (et de
    l'appel récurssif), choix du coup si plusieurs équivalent.

Fonctions hors interface:

    minimaxAB : explicite, heuristique sur le nombre de pierres pour le 
    moment (plus tard en zones de controle).

    boardValue : renvoie le score du tableau (appelé dans minimax)

    compterPierres : Compte le nombre de chaque pierres score (appelé dans
    boardValue)

    commpterZones : NIY -> Comptera les zones de controle

    jsonCoupAJouer : Renvoie le coup a jouer selon la partie choisie
    et le numero de coup si noir. Si blanc renvoie le coup a jouer selon
    une des parties possibles choisie au hasard.

