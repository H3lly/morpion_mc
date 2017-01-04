#! /usr/bin/python3
# -*- coding: utf-8 -*-

import socket, sys, struct
from grid import *

connexions_clients = {} # dictionaire des connexions clients
nombre_clients = 0
grids = [grid(), grid(), grid()]

def message_pour_tous(message):
    # Message du serveur vers tous les clients
    for client in connexions_clients:
        envoi_message(connexions_clients[client], message)

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
           
def main():
    global grids
    current_player = J1
    other_player = J2
    envoi_message(connexions_clients[str(other_player)], "L'autre joueur est en train de jouer. Veuillez attendre...\n")
    while grids[0].gameOver() == -1:
        shot = -1
        while shot < 0 or shot >= NB_CELLS:
            envoi_message(connexions_clients[str(current_player)], str(current_player))
            envoi_message(connexions_clients[str(current_player)], "choix")
            unpacker = struct.Struct('I')
            data = connexions_clients[str(current_player)].recv(unpacker.size)
            unpacked_data = unpacker.unpack(data)
            shot = unpacked_data[0]
        if (grids[0].cells[shot]) != EMPTY:
            grids[current_player].cells[shot] = grids[0].cells[shot]
        else:
            grids[current_player].cells[shot] = current_player
            grids[0].play(current_player, shot)
            current_player = current_player%2+1
            other_player = current_player%2+1
        envoi_message(connexions_clients[str(other_player)], str(other_player))
        envoi_message(connexions_clients[str(other_player)], "L'autre joueur est en train de jouer. Veuillez attendre...\n") # TODO : gérer le cas où c'est la fin du jeu et l'autre n'aura pas à jouer
    for client in connexions_clients:
        envoi_message(connexions_clients[client], "game over\n")
        envoi_message(connexions_clients[client], "0")
        
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
        message = reception_message(connexion_au_serveur)
        if message == "1":
            grids[1].display()
        elif message == "2":
            grids[2].display()
        elif message == "0":
            grids[0].display()
        elif message == "choix":
            shot = int(input("Quelle case allez-vous jouer ?\n"))
            packer = struct.Struct('I')
            packed_data = packer.pack(shot)
            connexion_au_serveur.sendall(packed_data)
        else:
            print(message)

    # 4) Fermer la connexion :
    print("Fin de la connexion")
    connexion_au_serveur.close()


    
PORT = 7125
if len(sys.argv) < 2:
    HOTE = ''
    serveur()
else:
    HOTE = sys.argv[1]
    client()


#si le serveur ferme, les clients doivent fermer aussi
#si un client quitte et qu'il revient, le gérer
#si un client quitte trop longtemps, fermer le jeu
