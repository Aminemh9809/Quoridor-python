import socket
from threading import Thread
from Reseau import Reseau

adresse=Reseau()
adresse.config()
# Variables de configuration du serveur
IP = adresse.ip
PORT = 8888
maxClients = 4

# Liste des connexions clients
clientConnections = []


def send(client):
    while True:

        message =liste.board
        message = message.encode("utf-8")
        client.send(message)


def reception(client):
    while True:
        for i in clientConnections:
            i=i%4+1
        requeteClient = client.recv(1024)
        requeteClient = requeteClient.decode("utf-8")
        print(requeteClient)
        if not requeteClient:
            print("connexion perdue")
            break

    # Création du socket serveur
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind((IP, PORT))
serverSocket.listen(maxClients)
print("Serveur en attente de connexion...")



client, addr = serverSocket.accept()
clientConnections.append(client)
print("Nouvelle connexion de", addr)

envoie=Thread(target=send,args=[client])
recept=Thread(target=reception,args=[client])


envoie.start()
recept.start()

recept.join()

client.close()
server_socket.close()
