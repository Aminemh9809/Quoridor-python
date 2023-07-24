


import socket
from threading import Thread 
from Reseau import Reseau
from board import Board
adresse=Reseau()
adresse.config()

liste=Board()

# Configuration du serveur
HOST =adresse.ip
PORT = 8888


def send(clientSocket):
    while True:
       
        message=liste.board
        message=message.encode('utf-8')
        clientSocket.send(message)
        if message == b'exit':  # Condition pour terminer la boucle
            break
        
def reception(clientSocket):
    while True:
       
        requeteServer=clientSocket.recv(1024)
        requeteServer=requeteServer.decode('utf-8')
        print(requeteServer)
        if requeteServer == 'exit':  # Condition pour terminer la boucle
           break
        
        
    


# Création du socket
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect((HOST, PORT))
print('Connecté au serveur')

envoie=Thread(target=send,args=[clientSocket])
recep=Thread(target=reception,args=[clientSocket])

envoie.start()
recep.start()
