#! /usr/bin/python3

import socket, sys

PORT = 7777
if len(sys.argv) < 2:
    HOTE = ''
    serveur()
else:
    HOTE = sys.argv[1]
    client()

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
