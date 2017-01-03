import socket, pickle, select, sys

def client(port, host):
	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server.connect(('127.0.0.1', port)) #host

	while True:
	    data = "I'm logged"
	    data = pickle.dumps(data)
	    server.send(data)
	    data = server.recv(1024)
	    data = pickle.loads(data)
	    print(data)

	server.close()

def server(port, host):
	# 1) création du socket
	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	# 2) Liaison du socket à une adresse précise
	try:
        server.bind((HOTE, PORT))
    except socket.error:
        print("La liaison du socket à l'adresse choisie a échoué.")
        sys.exit()

	# 3) Attente de la requete de connexion d'un client :
	while 1:
        print("Serveur pret, en attente de requetes ...")
        server.listen(5)

	clients = []
	while True:
	    Connections, _, _ = select.select([server], [], [], 0.05)

	    for Connection in Connections:
	    	client, Informations = Connection.accept()
	    	clients.append(client)

	    clientsList = []
	    try:
	        clientsList, wlist, xlist = select.select(clients, [], [], 0.05)
	    except select.error:
	        pass
	    else:
	        for clientInList in clientsList:
	            data = clientInList.recv(1024)
	            data = pickle.loads(data)
	            print(data)
	            data = "Welcome"
	            data = pickle.dumps(data)
	            clientInList.send(data)

	clientInList.close()
	server.close()


PORT = 7777
if len(sys.argv) < 2:
    HOTE = ''
    server(PORT, HOTE)
else:
    HOTE = sys.argv[1]
    client(PORT, HOTE)