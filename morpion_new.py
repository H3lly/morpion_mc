#! /usr/bin/python3
# -*- coding: utf-8 -*-

import socket, sys
from grid import *

connexions_clients = {} # dictionaire des connexions clients
nombre_clients = 0
grids = [grid(), grid(), grid()]

def message_pour_tous(message):
    # Message du serveur vers tous les clients
    message_bytes = message.encode()
    for client in connexions_clients:
        connexions_clients[client].send(message_bytes)

def main():
    current_player = J1
    other_player = J2
    connexions_clients[str(other_player)].send(bytes("L'autre joueur est en train de jouer. Veuillez attendre...", "utf8"))
    while grids[0].gameOver() == -1:
        shot = -1
        while shot < 0 or shot >= NB_CELLS:
            connexions_clients[str(current_player)].send(bytes(str(current_player)+"\n", "utf8"))
            connexions_clients[str(current_player)].send(bytes("choix\n", "utf8"))
            # TODO : Recevoir le choix du joueur et on le place dans la variable shot
        if (grids[0].cells[shot]) != EMPTY:
            grids[current_player].cells[shot] = grids[0].cells[shot]
        else:
            grids[current_player].cells[shot] = current_player
            grids[0].play(current_player, shot)
            current_player = current_player%2+1
            other_player = current_player%2+1
        connexions_clients[str(other_player)].send(bytes(str(other_player)+"\n", "utf8"))
        connexions_clients[str(other_player)].send(bytes("L'autre joueur est en train de jouer. Veuillez attendre...", "utf8")) # TODO : gérer le cas où c'est la fin du jeu et l'autre n'aura pas à jouer
    print("game over")
    message_pour_tous("grids[0].display()\n")

        
def serveur():

    global nombre_clients

    # Création du socket :
    connexion_principale = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connexion_principale.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Liaison du socket à une adresse précise
    try:
        connexion_principale.bind((HOTE, PORT))
    except socket.error:
        print("La liaison du socket à l'adresse choisie a échoué.\n")
        sys.exit()

    # Attente de la requete de connexion d'un client :
    print("Serveur pret, en attente de requetes ...\n")
    connexion_principale.listen(5)

    # Prise en charge des connexions demandées par les clients :
    while 1:        
        # Etablissement de la connexion :
        connexion, adresse = connexion_principale.accept()
        
        # Mémoriser la connexion dans le dictionnaire :
        nombre_clients = nombre_clients + 1
        connexions_clients[str(nombre_clients)] = connexion
        print("Client {} connecté, adresse IP {}, port {}.\n".format(str(nombre_clients), adresse[0], adresse[1]))
 
        # Dialogue avec les clients
        message_client = "Vous êtes connecté."
        message_client_bytes = message_client.encode()
        connexion.send(message_client_bytes)

        if(nombre_clients) >= 2:
            message_pour_tous("Le jeu va commencer !\n")
            main()
            
            
def client():
    global grids

    # 1) création du socket :
    connexion_au_serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 2) Envoi d'une requete de connexion au serveur :
    try:
        connexion_au_serveur.connect((HOTE, PORT))
    except socket.error:
        print("La connexion a échoué.\n")
        sys.exit()
    print("Connexion établie avec le serveur.\n")

    # 3) Dialogue avec le serveur :
    while 1:
        message_list = connexion_au_serveur.recv(1024).decode().split("\n")
        for i in range(len(message_list)):
            if message_list[i] == "1":
                grids[1].display()
            elif message_list[i] == "2":
                grids[2].display()
            elif message_list[i] == "choix":
                shot = int(input("Quelle case allez-vous jouer ?\n"))
                # TODO : renvoyer l'int au serveur, afin de transmettre le choix du joueur au serveur
            else:
                print(message_list[i]+"\n")

    # 4) Fermer la connexion :
    print("Fin de la connexion")
    connexion_au_serveur.close()


    
PORT = 7071
if len(sys.argv) < 2:
    HOTE = ''
    serveur()
else:
    HOTE = sys.argv[1]
    client()


#si le serveur ferme, les clients doivent fermer aussi
#si un client quitte et qu'il revient, le gérer
#si un client quitte trop longtemps, fermer le jeu
