#! /usr/bin/python3

import socket, sys, random
from grid import *

PORT = 7777
if len(sys.argv) < 2:
    HOTE = ''
    serveur()
else:
    HOTE = sys.argv[1]
    client()


def main():
    grids = [grid(), grid(), grid()]
    current_player = J1
    grids[J1].display()
    while grids[0].gameOver() == -1:
        if current_player == J1:
            shot = -1
            while shot <0 or shot >=NB_CELLS:
                shot = int(input ("quel case allez-vous jouer ?"))
        else:
            shot = random.randint(0,8)
            while grids[current_player].cells[shot] != EMPTY:
                shot = random.randint(0,8)
        if (grids[0].cells[shot] != EMPTY):
            grids[current_player].cells[shot] = grids[0].cells[shot]
        else:
            grids[current_player].cells[shot] = current_player
            grids[0].play(current_player, shot)
            current_player = current_player%2+1
        if current_player == J1:
            grids[J1].display()
    print("game over")
    grids[0].display()
    if grids[0].gameOver() == J1:
        print("You win !")
    else:
        print("you loose !")


def serveur():

    # 1) Création du socket :
    connexion_principale = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 2) Liaison du socket à une adresse précise
    try:
        connexion_principale.bind((HOTE, PORT))
    except socket.error:
        print("La liaison du socket à l'adresse choisie a échoué.")
        sys.exit()
        
    while 1:
        # 3) Attente de la requete de connexion d'un client :
        print("Serveur pret, en attente de requetes ...")
        connexion_principale.listen(5)
        
        # 4) Etablissement de la connexion :
        connexion, adresse = connexion_principale.accept()
    
        # 5) Dialogue avec les clients
        #jouer

        # 6) Fermeture de la connexion
        connexiont.send("Au revoir !")
        print("Connexion interrompue.")
        connexion.close()


def client():
    # 1) création du socket :
    connexion_au_serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 2) Envoi d'une requete de connexion au serveur :
    try:
        connexion_au_serveur.connect((HOST, PORT))
    except socket.error:
        print("La connexion a échoué.")
        sys.exit()
    print("Connexion établie avec le serveur.")

    # 3) Dialogue avec le serveur :
    message_serveur = connexion_au_serveur.recv(1024)
    
    while 1:
        if message_serveur.upper() == "FIN" or message_serveur == "":
            break
        #jouer

    # 4) Fermer la connexion :
    print("Fin de la connexion")
    connexion_au_serveur.close()
