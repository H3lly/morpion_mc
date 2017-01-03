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
    current_player = 1
    other_player = 2
    connexions_clients[str(current_player)].send(bytes(str(current_player), "utf8"))
    connexions_clients[str(other_player)].send(bytes("L'autre joueur est en train de jouer. Veuillez attendre...", "utf8"))
        
def serveur():

    global nombre_clients

    # Création du socket :
    connexion_principale = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connexion_principale.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Liaison du socket à une adresse précise
    try:
        connexion_principale.bind((HOTE, PORT))
    except socket.error:
        print("La liaison du socket à l'adresse choisie a échoué.")
        sys.exit()

    # Attente de la requete de connexion d'un client :
    print("Serveur pret, en attente de requetes ...")
    connexion_principale.listen(5)

    # Prise en charge des connexions demandées par les clients :
    while 1:        
        # Etablissement de la connexion :
        connexion, adresse = connexion_principale.accept()
        
        # Mémoriser la connexion dans le dictionnaire :
        nombre_clients = nombre_clients + 1
        connexions_clients[str(nombre_clients)] = connexion
        print("Client {} connecté, adresse IP {}, port {}.".format(str(nombre_clients), adresse[0], adresse[1]))
 
        # Dialogue avec les clients
        message_client = "Vous etes connecte. Envoyez vos messages."
        message_client_bytes = message_client.encode()
        connexion.send(message_client_bytes)

        if(nombre_clients) >= 2:
            message_pour_tous("Le jeu va commencer !")
            main()
            
            
def client():
    # 1) création du socket :
    connexion_au_serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 2) Envoi d'une requete de connexion au serveur :
    try:
        connexion_au_serveur.connect((HOTE, PORT))
    except socket.error:
        print("La connexion a échoué.")
        sys.exit()
    print("Connexion établie avec le serveur.")

    # 3) Dialogue avec le serveur :    
    while 1:
        message_serveur_bytes = connexion_au_serveur.recv(1024)
        message_serveur = message_serveur_bytes.decode()
        if message_serveur == "1":
            grids[1].display()
        elif message_serveur == "2":
            grids[2].display()
        else:
            print(message_serveur)


    # 4) Fermer la connexion :
    print("Fin de la connexion")
    connexion_au_serveur.close()

PORT = 7000
if len(sys.argv) < 2:
    HOTE = ''
    serveur()
else:
    HOTE = sys.argv[1]
    client()


#si le serveur ferme, les clients doivent fermer aussi
#si un client quitte et qu'il revient, le gérer
#si un client quitte trop longtemps, fermer le jeu