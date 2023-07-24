import tkinter as tk
from pawn import Pawn


class Board(tk.Frame): # tableau

    #constructeur
    def __init__(self,nbLigne, nbPlayers):
        self.nbLigne = nbLigne
        self.nbPlayers = nbPlayers       
        self.currentPawn = [] 
        
        self.board = []
 
    # déclaration du tableau Bord avec nbr ligne et colonne et nb  Pawn selon les regles de jeu
    def initBoard(self):
        n = self.nbLigne*2-1
        
        if(self.nbPlayers == 2):
            pc = Pawn(1,0,(int)(n/2))
            self.currentPawn +=[pc]
            pc = Pawn(2,(n-1),(int)(n/2))
            self.currentPawn +=[pc]
        else:
            pc  = Pawn(1,0,(int)(n/2))
            self.currentPawn +=[pc]
            
            pc = Pawn(2,(n-1),(int)(n/2))
            self.currentPawn +=[pc]
           
            pc = Pawn(3,(int)(n/2),0)
            self.currentPawn +=[pc]
            
            pc = Pawn(4,(int)(n/2),(n-1))
            self.currentPawn +=[pc]
            
        for i in range(n):
                ligne = []
                if(i%2 !=0):
                    for j in range(n): 
                        p = Pawn(5,i,j)
                        ligne += [p] 
                else:
                    for j in range(n): 
                        for s in range(self.nbPlayers): 
                            if(i == self.currentPawn[s].ligne and j == self.currentPawn[s].colonne):                       
                                p = Pawn(self.currentPawn[s].valeur,i,j) 
                                break
                            else:    
                                if(j%2 !=0):
                                    p = Pawn(5,i,j)
                                else:
                                    p = Pawn(0,i,j)
                        
                        ligne += [p] 
                 
                self.board += [ligne]
              
    
# mettre à jour le Board aprés choix et validation d'une case
    def updateBoard(self ,curentPlayer):
        i=self.currentPawn.ligne
        j=self.currentPawn.colonne
      
        self.board[i][j].setValeur(curentPlayer) 
        #print("updateBoard ",i,', ',j, ' ,',s,' : ',self.curentPlayer)