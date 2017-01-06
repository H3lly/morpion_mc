#! /usr/bin/python3
# -*- coding: utf-8 -*-

import socket, sys, struct, os
from io import StringIO
from grid import *

connexions_clients = {} # dictionaire des connexions clients
nombre_clients = 0

# AFFICHAGE

def message_pour_tous(message):
    # Message du serveur vers tous les clients
    for client in connexions_clients:
        envoi_message(connexions_clients[client], message)

def redirection_affichage(grids, grid, current_player):
    sys.stdout = StringIO()
    grids[grid].display()
    s = str(sys.stdout.getvalue())
    envoi_message(connexions_clients[str(current_player)], s)
    for i in range(3, nombre_clients):                              #essai observateur
        envoi_message(connexions_clients[str(i)], s)                #essai observateur

def affichage_observateur(grids, current_player, shot, message):    #essai observateur
    for i in range(3, nombre_clients):
        if shot != -1:
            envoi_message(connexions_clients[str(i)], "Le joueur {} a joué la case {}.\n".format(string(current_player), str(shot)))
        else:
            envoi_message(connexions_clients[str(i)], message)

        
# PROTOCOL

def envoi_message(sock, data):
    length = len(data)
    sock.sendall(struct.pack('!I', length))
    sock.sendall(data.encode())
    
def reception_message(sock):
    lengthbuf = recvall(sock, 4)
    length = struct.unpack('!I', lengthbuf)
    return recvall(sock, length[0]).decode("ascii")

def recvall(sock, count):
    buf = b''
    while count:
        newbuf = sock.recv(count)
        if not newbuf:
            return None
        buf += newbuf
        count -= len(newbuf)
    return buf

def envoi_int(sock, data):
    sock.sendall(struct.pack('!I', data))

def reception_int(sock):
    return struct.unpack('!I', sock.recv(4))[0]


# JEU

def main():
    grids = [grid(), grid(), grid()]
    current_player = J1
    other_player = J2
    envoi_message(connexions_clients[str(other_player)], "clear")
    envoi_message(connexions_clients[str(other_player)], "L'autre joueur est en train de jouer. Veuillez attendre...\n")
    while grids[0].gameOver() == -1:
        shot = -1
        while shot < 0 or shot >= NB_CELLS:
            envoi_message(connexions_clients[str(current_player)], "clear")
            redirection_affichage(grids, current_player, current_player)
            envoi_message(connexions_clients[str(current_player)], "choix")
            shot = reception_int(connexions_clients[str(current_player)])
        if (grids[0].cells[shot]) != EMPTY:
            envoi_message(connexions_clients[str(current_player)], "\nLa case est deja prise !\n")
            grids[current_player].cells[shot] = grids[0].cells[shot]
        else:
            grids[current_player].cells[shot] = current_player
            grids[0].play(current_player, shot)
            redirection_affichage(grids, current_player, current_player)
            current_player = current_player%2+1
            other_player = current_player%2+1
        if grids[0].gameOver() == -1:
            envoi_message(connexions_clients[str(other_player)], "clear")
            envoi_message(connexions_clients[str(other_player)], "L'autre joueur est en train de jouer. Veuillez attendre...\n")
    for client in connexions_clients:
        envoi_message(connexions_clients[client], "clear")
        envoi_message(connexions_clients[client], "Game over !\n")
        redirection_affichage(grids, 0, int(client))
        if grids[0].gameOver() == int(client):
            envoi_message(connexions_clients[client], "You win !\n")
        else:
            envoi_message(connexions_clients[client], "You lose !\n")
    message_pour_tous("rejouer")                                            #marche pour Y, problème pour N
    for client in connexions_clients:
        message = reception_message(connexions_clients[client])
        if message == "Y":
            continue
        elif message == "N":
            connexions_clients[client].close()



# SERVEUR
        
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
        envoi_message(connexion, "Vous etes connecte.\n")
   
        while nombre_clients >= 2:
            message_pour_tous("Le jeu va commencer !\n")
            main()

# CLIENT
            
def client():

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
        message = reception_message(connexion_au_serveur)
        if message == "choix":
            while 1:
                shot = input("Quelle case allez-vous jouer ?\n")
                if shot in ["0","1","2","3","4","5","6","7","8"]:
                    envoi_int(connexion_au_serveur, int(shot))
                    break
        elif message == "clear":
                os.system("clear")
        elif message == "rejouer":
            while 1:
                reponse = input("Voulez-vous rejouer une partie ? 'Y'/'N'\n")
                if reponse == "Y" or reponse == "N":
                    envoi_message(connexion_au_serveur, reponse)
                    break
        else:
            print(message)

    # 4) Fermer la connexion :
    print("Fin de la connexion")
    connexion_au_serveur.close()

 
PORT = 7192
if len(sys.argv) < 2:
    HOTE = ''
    serveur()
else:
    HOTE = sys.argv[1]
    client()


#si le serveur ferme, les clients doivent fermer aussi
#si un client quitte et qu'il revient, le gérer
#si un client quitte trop longtemps, fermer le jeu
#si le joueur A dit Y, sa réponse est envoyée à B