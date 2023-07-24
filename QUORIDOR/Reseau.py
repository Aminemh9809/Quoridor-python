from board import Board
import tkinter as tk
from tkinter.simpledialog import *
from tkinter import messagebox
import random
import math
from pawn import Pawn
from tile import Tile
from player import Player
import socket

class Reseau:
    #constructeur
    def __init__(self):
        
        # self._create_gui()
        app = tk.Tk()
        self.app=app   
        self.renitialiser()     
        self.start()
        self.app.mainloop()


# rénitialisation des paramètres  xx
    def renitialiser(self):
        self.nbLigne = 0
        self.nbPlayers = 0  
        self.nbTiles = 0
        self.cpu=False    
        self.gagner=False   
        self.players = [] 
        self.board = []
        self.screen = 500
        self.scrennBoard = 400
        self.curentPlayer = 0
        self.xBoard = 0    
        self.espaceVide=40    
        self.lenBoard=0
        self.ip=socket.gethostbyname(socket.gethostname())
         

#démarrer une nouvelle partie, vider tout les paramètres et supprimer le canvas
    def newPartie(self):
        self.txt.configure(text='  '  )
        self.renitialiser()    
        self.can.delete(tk.ALL)

#création de l'interface
    def start( self):       
        posBt1 = self.screen +20
        posBt2 = self.screen +90

        self.app.title("QUORIDOR")
        self.can = tk.Canvas(self.app, width =self.screen, height =self.screen, bg ='white')        
        self.can.bind("<Button-1>", self.on_click)
        #self.can.bind('<Enter>', self.on_start_hover)
        self.can.pack(side =tk.TOP, padx =3, pady =3)
        self.can.create_text(self.screen // 2,self.screen // 2 , text="THE QUORIDOR GAME  !", font=("Comic Sans MS", 25), fill="black", anchor="center") 

        
  

        b1 = tk.Button(self.app, text ='Démarrer le jeu',  command =self.config)
        b1.place(x=390,y=posBt1)   

        b2 = tk.Button(self.app, text ='Quitter', command = quit)
        b2.pack(side =tk.BOTTOM, padx =3, pady =3)         
        b3 = tk.Button(self.app, text ='Regles de jeu', command =self.regles)
        b3.pack(side =tk.BOTTOM, padx =3, pady =3) 
        b4 = tk.Button(self.app, text ='Nouvelle Partie', command =self.newPartie)
        b4.pack(side =tk.BOTTOM, padx =3, pady =3)
 
        
        self.txt = tk.Label(self.app, text='....')      
        self.txt.pack()

   

#fenetre Regles des jeux        
    def regles(self):
        messagebox.showinfo(" Regles ", "Il n’y a qu’une action par tour. Le joueur a le choix entre : Faire avancer son pion : verticalement ou horizontalement, une case à la fois et en contournant les barrières.  Poser une barrière entre deux cases\n"+
                        "Un joueur pose une barrière pour ralentir son adversaireou sSe créer un passage sécurisé.\n"
                        " Notez cependant qu’il est interdit de bloquer complètement son adversaire en l’empêchant d’aller au mur de l’autre côté !\n" 
                        " Un joueur ne peux pas prendre la place d'un déja posionné.\n" 
                        " Vous pouvez choisir un nombre de joueur 2 ou 4, plateau 5x5 ou 7x7 ou 9x9 ou 11x11, et  nombre de barrière multiple de 4 maximum 40 .\n"
                        " Chaque joueur a une  couleur et lettre différente \n")

     #verifier min et max colonne et nb player    
    def verfiParametreConf(self):   
        if ( self.nbPlayers != 2 and self.nbPlayers != 4):
            messagebox.showerror("Erreur", "Il faut entre 2 et 4 jours")    
            return False
        if ( self.nbLigne!= 5 and self.nbLigne!= 7 and self.nbLigne != 9 and self.nbLigne != 11):
            messagebox.showerror("Erreur", "Il faut 5 ou 7 ou 9 ou 11 lignes/colonnes.")    
            return False
        
        if ( self.nbTiles>40 ):
            messagebox.showerror("Erreur", "Il faut  maxi 40 barrières")    
            return False
        if((self.nbTiles % self.nbPlayers) != 0 ):
            messagebox.showerror("Erreur", "Il faut pourvoir partagé le meme nombre de barrières sur les joeurs")  
            return False
        # changement de plan, calcul des x et Y, les paramètre du canvas 500X500 alors que le Tableau reel Ligne X Colonne
        return True
       
# parametrez le jeu   ( )
    def config( self):
        self.newPartie()       
        self.nbPlayers = askinteger("Nombre de joueur..", "Nombre de joueur:",initialvalue=4)
        self.ip = askstring("Adresse IP..", "Adresse IP du joueur:",initialvalue=self.ip)        # par défaut 8lignes et 5 colonnes
        self.nbLigne = askinteger("Nombre de lignesXcolonnes...", "Nombre de lignesXcolonnes:",initialvalue=9)
        if(self.nbLigne == 5):
            self.scrennBoard = 300
        self.nbTiles = askinteger("Nombre de barrières...", "Nombre de barrières:",initialvalue=20)
        # vérifier les paramètres
        
        if (self.verfiParametreConf() == True ):            
            # une fois les parèmtres configurés et sont bons, choisir les couleurs et  lancer le jeu
            # self.defineColors()
            self.lancerJeu()
          
            return True
     
    # intialiser players
    def definePlayers(self):
        n = self.lenBoard
        nbTilesByPlayer= (int)(self.nbTiles/self.nbPlayers)
        y1 = self.espaceVide/2
        y2 = self.xBoard *(1+n)+ self.espaceVide

        x1 =  self.espaceVide/2
        x2=self.xBoard *(1+n)+ self.espaceVide
        
        dim = self.scrennBoard/nbTilesByPlayer
        dim2 = self.espaceVide/4
        if(self.nbPlayers == 2):
            tilesP1 = []
            tilesP2 = []
            for i in range(nbTilesByPlayer):
                x0 = i*dim+ self.espaceVide 
                tile1 = Tile(x0,y1,x0+(dim-dim2),y1,'blue')
                tile2 = Tile(x0,y2,x0+(dim-dim2),y2,'green')   
                tilesP1 += [tile1]
                tilesP2 += [tile2]
            player1=Player(nbTilesByPlayer,'blue',tilesP1,'A')
            self.players +=[player1]
            player2=Player(nbTilesByPlayer,'green',tilesP2,'B')
            self.players +=[player2]   
        else:
            tilesP1 = []
            tilesP2 = []
            tilesP3 = []
            tilesP4 = []
           
            for i in range(nbTilesByPlayer):
                x0 = i*dim+ self.espaceVide 
                y0 = i*dim+ self.espaceVide  
                tile1 = Tile(x0,y1,x0+(dim-dim2),y1,'blue')
                tile2 = Tile(x0,y2,x0+(dim-dim2),y2,'green')   
                tile3 = Tile(x1,y0,x1,y0+(dim-dim2) ,'red')
                tile4 = Tile(x2,y0,x2,y0+(dim-dim2),'yellow')   
                tilesP1 += [tile1]
                tilesP2 += [tile2]
                tilesP3 += [tile3]
                tilesP4 += [tile4]
            player1=Player(nbTilesByPlayer,'blue',tilesP1,'A')
            self.players +=[player1]
            player2=Player(nbTilesByPlayer,'green',tilesP2,'B')
            self.players +=[player2]   
            player3=Player(nbTilesByPlayer,'red',tilesP3,'C')
            self.players +=[player3]
            player4=Player(nbTilesByPlayer,'yellow',tilesP4,'D')
            self.players +=[player4]    
    
    #************************************* Game **********************************
    #Demarrer le jeu
    def lancerJeu(self):
        self.board = Board(self.nbLigne, self.nbPlayers)
        self.board.initBoard()
        self.lenBoard = self.nbLigne*2-1
        self.xBoard =  self.scrennBoard/self.lenBoard
        self.definePlayers() 
        self.afficher() 
        self.curentPlayer = 1
        self.displayBoard()
        self.displayPlayers()
        self.txt.configure(text=' Au tour du joueur '+str(self.curentPlayer)+' : ', fg=self.players[self.curentPlayer-1].color)
        print(' Au tour du joueur ', self.curentPlayer )
        #print("lancerJeu select Pawn  : ",self.PawnSlect.ligne)
    
    #"Dessinee les barrieres "
    def displayPlayers(self):
            print('******* displayPlayers ******** ',self.nbPlayers)


            for i in range(self.nbPlayers):    
                player= self.players[i]  
                #print('player : ',i)
                #print('player : ', i , ' - player nbTiles ',player.nbTiles)
                for j in range(player.nbTilesDefault):
                    #effacer tiles
                    tile=player.tiles[j]       
                    self.can.create_rectangle(tile.x1,tile.y1,tile.x2,tile.y2, fill= 'white',outline = 'white' , width = 7)  

                for j in range(player.nbTiles):
                    tile=player.tiles[j]       
                    self.can.create_rectangle(tile.x1,tile.y1,tile.x2,tile.y2, fill= player.color,outline = player.color , width = 7)                 
                 
        
    #"Dessinee l'interface de jeu "
    def displayBoard(self):
        n =  self.lenBoard  
        x=y =self.xBoard 
        
        for i in range(n):
            for j in range(n):
              
                y0 = i*y+self.espaceVide
                x0 = j*x+self.espaceVide
                #print('x0:',x0,' y0: ',y0, ' x1 : ',x0+x, ' y1 ',y0+y)
                
                #self.colorsPlayer[self.curentPlayer -1 ]
                player= self.board.board[i][j].getValeur()  
                if(player < 5 ):
                    # dessiner les cases
                    self.can.create_rectangle( x0,y0, x0+x,y0+y , fill='#ccc',outline ='#ccc' , width = 7)
                else:
                    # dessiner les barrières
                    if(player  >  5 ):
                        nColor= player-5
                        
                        if(i%2 == 0):# vertical
                            self.can.create_rectangle( x0+x/2,y0 ,x0+x/2,y0+y , fill=self.players[nColor -1].color,outline =self.players[nColor -1] .color, width = 2)
                        else:
                            if(j%2 == 0):  # horz                      
                                self.can.create_rectangle( x0 ,y0+y/2 ,x0+x,y0+y/2, fill=self.players[nColor -1].color,outline =self.players[nColor -1] .color, width = 2)
                            else:  #milieu
                                self.can.create_rectangle( x0 ,y0+y/2 ,x0+x,y0+y/2, fill=self.players[nColor -1].color,outline =self.players[nColor -1] .color, width = 2)
                    
                       
                if(player > 0 and player < 5):
                        x1=x/6
                        y1=y/6
                        ligney0 =y0+y1
                        lignex0 =x0+x1
                        lignex1=x0+x1*5
                        ligney1 =y0+y1*5
                        self.can.create_oval( lignex0,ligney0,lignex1,ligney1  , fill=self.players[player -1].color,outline = self.players[player-1 ].color)
                        self.can.create_text( lignex0+x1*2,ligney0+x1*2 ,text= self.players[player -1].lettre, fill="#ccc",font='blod' )
        #if(self.again() == False)  :
            #self.win()

     
    def on_start_hover(self,event):     
        x=y =self.xBoard  
        print('Mousse over')
        #40 ==> pnt 0
        #x = 66 y = 37 dernier pnt case 1   jusqu'a 68 ligne 00
        # de 71 à 82 ,37 à 69 barieere 1 case 01

        #case 2 :85,40--114,40 ---83,65 ---111,65
        #ex = event.x - 14
        #ey = event.y - 14
        #ligne = math.floor(ey/y) -1
        #colonne = math.floor(ex/x)-1
        #if(ligne>=0 and ligne < self.lenBoard and colonne>=0 and colonne < self.lenBoard ):
            #y0 = ligne*y+self.espaceVide
            #x0 = colonne*x+self.espaceVide
            #if(ligne%2 == 0):#ver
                #if(colonne%2 != 0):#ver        
                   # print('Mousse over','ligne =',ligne,'  , colonne :  ',colonne)
                    #self.can.create_rectangle( x0+10,y0 ,x0+x/2,y0+y+10 , fill='green',outline ='green' , width = 3)
            #else:
                #if(colonne%2 == 0):
                   # print('Mousse over','ligne =',ligne,'  , colonne :  ',colonne)
                    #self.can.create_rectangle( x0 ,y0+10 ,x0+20,y0+10, fill='green',outline ='green' , width = 1)

# effacer posiotion si case 2 de la barrière n'est pas possible
    def effacerAnciennePosition(self,player):
        n =  self.lenBoard        
        for i in range(n):
            for j in range(n):                
                if(self.board.board[i][j].getValeur()==player):
                    self.board.board[i][j].valeur = 0
                    break
    # récupéréer la position actuel du joeur
    def recupPositionACtuel(self,player):
        n =  self.lenBoard        
        for i in range(n):
            for j in range(n):                
                if(self.board.board[i][j].getValeur()==player):
                    return i,j
    
    # mis à jour du nombre de barrière du  du joeur                 
    def updateTile(self,player):
        nb =  self.players[player -1].nbTiles
        self.players[player -1].nbTiles = nb-1

    # vérifier si il y a un gagant    
    def win(self,player,ligne, colonne):      
        n =  self.lenBoard        
        # player 1 a commencer à la ligne 0 il doit arrivé a la ligne n-1
        # player 2 doit arrivé a la ligne 0
        # player 3 a commencer à la colonne 0 il doit arrivé a la colonne n-1
        # player 4 doit arrivé a la colonne 0
           
        
        if( ligne%2 == 0 and colonne%2 == 0 ):
            if(player == 1):
                if(ligne==n-1):
                    self.gagner = True
                    return True
            else:
                if(player == 2):
                    if(ligne == 0):
                        self.gagner = True
                        return True
                else:
                    if(player == 3):
                        if(colonne==n-1):
                            self.gagner = True
                            return True
                    else:
                        if(player == 4):
                            if(colonne == 0):
                                self.gagner = True
                                return True
        return False
            
              

    # afficher le tableau dans le terminal pour controle   
    def afficher(self):
        n =  self.lenBoard
        
        for i in range(n):
            for j in range(n):
                
                if(j==0):
                    if(i<9):
                        print(i+1 , '  |', end=" ")   
                    else :  
                        print(i+1 , ' |', end=" ")           
                print(self.board.board[i][j].getValeur() , end=" ")
                     
            print()
        
        print( '   ', end=" ")
        #for l in range(n):
        print( '-----------', end=" ")
        print()
        print( '    ', end=" ")
        for l in range(n):
            print( l+1, end=" ")
        print()

# ajouter une case barrière 
    def addTile(self, ligne, colonne):
        nb =  self.players[self.curentPlayer -1].nbTiles
        if(nb > 0 ):
            self.board.board[ligne][colonne].valeur =   self.curentPlayer+5
            #self.updateTile(self.curentPlayer)
        else:
            if(self.cpu == True and self.curentPlayer == 2):
                self.cpuChoixCase()
            else:
                messagebox.showinfo("Erreur", " Vous n'avez plus de barrières")
            
   
     # verifier si chemin fermé pour un joueur
         
    def joueurFerme(self, player ):
        # dés qu'on affiche un ebarriere hor on remonte pour verifier si verticalement tout est ferme
        # et dés qu'on affiche une barriere verticale on va horz pour vérifier si tout est fermé
        n =  self.lenBoard
        
        i,j = self.recupPositionACtuel(player)
        
        if(player == 0  or player == 1):            
            # s'il peut descendnre
            debBar = -1
            finBar = -1
            for s in range(n):
                if(s%2 !=0 and debBar == -1 and finBar == -1):
                    if(self.board.board[s][j].valeur > 5) : # barrière trouvé sur la colonne du user
                        # parcourer la ligne pour voir si elle est fermée
                           
                        for r in range(n):
                            if(r%2 == 0):
                                if(self.board.board[s][r].valeur > 5) : # barrière trouvé
                                    if(debBar == -1):
                                        debBar = r
                                    if(finBar <= r):
                                        finBar = r
                                else:
                                    debBar = -1
                                    finBar = -1
                if(debBar == 0 and finBar == n-1):
                    # fermeture avec ligne complete
                    return True
            if(debBar == 0 and finBar == n-1):
                # fermeture avec ligne complete
                return True
            if(debBar  == finBar ): # soit 0 ou une barr a la fin
                # fermeture avec ligne complete
                return False
        else: 
        
            if(player == 2  or player == 3):
                
                # s'il peut descendnre
                debBar = -1
                finBar = -1
                for s in range(n):
                    if(s%2 != 0 and debBar == -1 and finBar == -1):
                        if(self.board.board[i][s].valeur > 5) : # barrière trouvé
                            # parcourer la colonne pour voir si elle est fermée                            
                            for r in range(n):
                                if(r%2 == 0):
                                    if(self.board.board[r][s].valeur > 5) : # barrière trouvé
                                        if(debBar == -1):
                                            debBar = r
                                        if(finBar <= r):
                                            finBar = r
                                    else:
                                        debBar = -1
                                        finBar = -1                                       
                                        
                    if(debBar == 0 and finBar == n-1):
                        # fermeture avec ligne complete
                        return True
                if(debBar == 0 and finBar == n-1):
                    # fermeture avec ligne complete
                    return True
                if(debBar  == finBar ): # soit 0 ou une barr a la fin
                    # fermeture avec ligne complete
                    return False
        return False

    # effacer une case barrière
    def effacerBarriere(self,i,j):
        self.board.board[0][1].valeur = 5

# vérifier si ajout d'une case de  barrière est possible 
    def possibleBarriere(self,ligne,colonne):
        if(self.board.board[ligne][colonne].valeur > 5 ):
            return False
         
        #Provisoire 
        self.board.board[ligne][colonne].valeur = 10
        for i in range(self.nbPlayers):
            
            if(self.joueurFerme(i) == True):
                messagebox.showinfo("Erreur", " barrière ferme le trajet")
                #Provesoir
                self.board.board[ligne][colonne].valeur = 5
                return False
            # remettre la valeur 5
        self.board.board[ligne][colonne].valeur = 5
        nb =  self.players[self.curentPlayer -1].nbTiles
        #print('pos tile : ',ligne,',',colonne , '  ') 
        if(nb > 0 ):
            #pas fermer sur un joueur
            n =  self.lenBoard
            if (ligne == 1 and colonne == 0) :
                if( self.board.board[0][1].valeur == 5):
                    return True
                else:
                    return False
            else:
                if (ligne == 0 and colonne == 1) :
                    if( self.board.board[1][0].valeur == 5):
                        return True
                    else:
                        return False
                else:
                    if (ligne == n-2 and colonne == 0) :
                        if( self.board.board[n-1][1].valeur ==5):
                            return True
                        else:
                            return False
                    else:
                        if (ligne == n-1 and colonne == 1) :
                            if( self.board.board[n-2][0].valeur == 5):
                                return True
                            else:
                                return False
                        else:
                            if (ligne == 0 and colonne == n-2) :
                                if( self.board.board[1][n-1].valeur == 5):
                                    return True
                                else:
                                    return False
                            else:
                                if (ligne == 1 and colonne == n-1) :
                                    if( self.board.board[0][n-2].valeur == 5):
                                        return True
                                    else:
                                        return False
                                else:                                 
                                    if (ligne == n-2 and colonne == n-1) :
                                        if( self.board.board[n-1][n-2].valeur == 5):
                                            return True
                                        else:
                                            return False
                                    else:
                                        if (ligne == n-1 and colonne == n-2) :
                                            if( self.board.board[n-2][n-1].valeur == 5):
                                                return True
                                            else:
                                                return False
                                        else:
                                            if(colonne == 0):
                                                if( (( self.board.board[ligne-2][colonne].valeur == 5) or (self.board.board[ligne-1][colonne+1].valeur == 5)) and (( self.board.board[ligne+2][colonne].valeur == 5) or (self.board.board[ligne+1][colonne+1].valeur == 5))):
                                                    return True
                                                else:
                                                    return False
                                            else:
                                                if(colonne == n-1):
                                                    if( (( self.board.board[ligne][colonne-2].valeur == 5) or (self.board.board[ligne-1][colonne-1].valeur == 5)) and (( self.board.board[ligne+2][colonne].valeur == 5) or (self.board.board[ligne-1][colonne-1].valeur == 5))):
                                                        return True
                                                    else:
                                                        return False
                                            if(ligne == 0):
                                                    if( (( self.board.board[ligne][colonne+2].valeur == 5) or (self.board.board[ligne+1][colonne+1].valeur == 5)) and (( self.board.board[ligne][colonne-2].valeur == 5) or (self.board.board[ligne+1][colonne+1].valeur == 5))):
                                                        return True
                                                    else:
                                                        return False
                                            else:
                                                    if(ligne == n-1):
                                                        if( (( self.board.board[ligne][colonne+2].valeur == 5) or (self.board.board[ligne-1][colonne+1].valeur == 5)) and (( self.board.board[ligne][colonne-2].valeur == 5) or (self.board.board[ligne-1][colonne-1].valeur == 5))):
                                                            return True
                                                        else:
                                                            return False

                                                    else:  
                                                         
                                                        if(ligne%2 == 0) :    #ver      
                                                            if(colonne == 1): 
                                                                if((( self.board.board[ligne-1][colonne-1].valeur == 5) or (self.board.board[ligne+1][colonne-1].valeur == 5)  )
                                                                and (( self.board.board[ligne-1][colonne+1].valeur == 5) or (self.board.board[ligne+1][colonne+1].valeur == 5)or (self.board.board[ligne][colonne+2].valeur == 5) ) ):
                                                                    return True
                                                                else:
                                                                    return False
                                                            else:
                                                                if(colonne == n-2): 
                                                                    if((( self.board.board[ligne-1][colonne-1].valeur == 5) or (self.board.board[ligne+1][colonne-1].valeur == 5)or (self.board.board[ligne][colonne-2].valeur == 5)   )
                                                                    and (( self.board.board[ligne-1][colonne+1].valeur == 5) or (self.board.board[ligne+1][colonne+1].valeur == 5) ) ):
                                                                        return True
                                                                    else:
                                                                        return False
                                                                else:
                                                                    if((( self.board.board[ligne-1][colonne-1].valeur == 5) or (self.board.board[ligne+1][colonne-1].valeur == 5)or (self.board.board[ligne][colonne-2].valeur == 5)   )
                                                                    and (( self.board.board[ligne-1][colonne+1].valeur == 5) or (self.board.board[ligne+1][colonne+1].valeur == 5)or (self.board.board[ligne][colonne+2].valeur == 5) )):
                                                                        return True
                                                                    else:
                                                                        return False
                                                        else:
                                                            if(ligne == 1):
                                                                if(((self.board.board[ligne-1][colonne-1].valeur == 5)or (self.board.board[ligne-1][colonne+1].valeur == 5)   )
                                                               and (( self.board.board[ligne+2][colonne].valeur == 5) or (self.board.board[ligne+1][colonne-1].valeur == 5)or (self.board.board[ligne+1][colonne+1].valeur == 5)   )):
                                                                    return True
                                                                else:
                                                                    return False
                                                            else:
                                                                if(ligne == n-2):
                                                                    if((( self.board.board[ligne-2][colonne].valeur == 5) or (self.board.board[ligne-1][colonne-1].valeur == 5)or (self.board.board[ligne-1][colonne+1].valeur == 5)   )
                                                                and ( (self.board.board[ligne+1][colonne-1].valeur == 5)or (self.board.board[ligne+1][colonne+1].valeur == 5)   )):
                                                                        return True
                                                                    else:
                                                                        return False
                                                                else:
                                                                    if((( self.board.board[ligne-2][colonne].valeur == 5) or (self.board.board[ligne-1][colonne-1].valeur == 5)or (self.board.board[ligne-1][colonne+1].valeur == 5)   )
                                                                    and (( self.board.board[ligne+2][colonne].valeur == 5) or (self.board.board[ligne+1][colonne-1].valeur == 5)or (self.board.board[ligne+1][colonne+1].valeur == 5)   )):
                                                                        return True
                                                                    else:
                                                                        return False

        else:
            if(self.cpu == True and self.curentPlayer == 2):
                self.cpuChoixCase()
            else:
                messagebox.showinfo("Erreur", " Vous n'avez plus de barrières")
            return False

        return True

     # veifier s'il y a une  barriere  
    def barriere(self,i,j, ligne, colonne):
        # veifier si pas barriere 
        
        if(ligne == i+2):
            if(self.board.board[i+1][colonne].valeur !=5):
                return True
        else:
            if(ligne == i-2):
                if(self.board.board[i-1][colonne].valeur !=5):
                        return True
            else:
                if(colonne == j+2):
                    if(self.board.board[ligne][j+1].valeur !=5):
                            return True
                else:
                    if(colonne == j-2):
                        if(self.board.board[ligne][j-1].valeur !=5):
                            return True

        return False
    
    # vérifier si la position  libre dans une Pawn correpond au meme joeur avoir déja choisi une position dans la meme Pawn
    def possibleSquare(self, ligne, colonne ,player):
        
        if( ligne%2 == 0 and colonne%2 == 0 ):
            n =  self.lenBoard          
            i,j = self.recupPositionACtuel(player)
            #cas1 les 4 points  d'extrémité ==>  que deux position possible
            #print('i,j : ', i, ' , ', j,'l,c : ', ligne, ' , ', colonne )
        
            if( (ligne == i +2 and colonne == j) or (colonne == j +2 and ligne == i)  or (ligne == i -2 and colonne == j)  or   (colonne ==j  -2 and ligne == i)) :
                if(self.barriere(i,j, ligne, colonne)):           
                    print('pos impossible cause barrière') 
                    #messagebox.showinfo('erreur', 'case impossible cause barrière')
                    return False
                else:
                    return True
            else:
                #print('pos : ',ligne,',',colonne , ' choix impossible ')                 
                return False

       
        return True
  
        
    # selection d'une case sur le jeu, event click
    def on_click(self,event):        
       
        # on détermine la Pawn ou s'est passé la selection + debut vide + width
        x=y =self.xBoard  
              
        #40 ==> pnt 0
        #x = 66 y = 37 dernier pnt case 1   jusqu'a 68 ligne 00
        # de 71 à 82 ,37 à 69 barieere 1 case 01

        #case 2 :85,40--114,40 ---83,65 ---111,65
        ex = event.x - 14
        ey = event.y - 14
        ligne = math.floor(ey/y) -1
        colonne = math.floor(ex/x)-1
        self.jouer(ligne,colonne)

    def rechoisir(self):
        if(self.cpu == True and self.curentPlayer == 2):
            self.cpuChoixCase()
        else:
            messagebox.showinfo('erreur', 'selection impossible')
        #return

    # algo jouer
    def jouer(self,ligne,colonne):
        if(ligne%2 != 0 and colonne%2 !=0):#impossible
            self.rechoisir()
    
     
        n =  self.lenBoard  
        if(self.gagner == False):
            if(ligne>=0 and ligne < self.lenBoard and colonne>=0 and colonne < self.lenBoard ):
                # verifier si la case séléctionnée est bonne (pas prise)
                if(self.possibleSquare(ligne,colonne , self.curentPlayer)):
                
                    if(self.win(self.curentPlayer, ligne, colonne) == False):
                    #print('ON CLICK secreen ', self.scrennBoard, 'len bord ', self.lenBoard,' XBoard = ',x,' Ma selection x,y :',event.x,'  , ',event.y , 'equivaelent : ','ligne =',ligne,'  , colonne :  ',colonne)
                    
                        if(ligne%2 == 0):#ver
                            #print(' l, c', ligne, ' : ',colonne, ' player : ', self.curentPlayer)

                            if(colonne%2 != 0):#ver  pas mileu
                                if(self.board.board[ligne][colonne].valeur == 5 ): 
                                    if(self.possibleBarriere(ligne, colonne)):
                                        self.addTile( ligne, colonne)  
                                        self.updateTile(self.curentPlayer)
                                        if(ligne == 0 or (ligne < n-1 and self.curentPlayer == 1) ):
                                            if( (self.possibleBarriere(ligne+2, colonne) == True ) and (self.board.board[ligne+2][colonne].valeur == 5 )):
                                                self.addTile( ligne+2, colonne)   
                                            else:
                                                if( (self.possibleBarriere(ligne-2, colonne) == True ) and (self.board.board[ligne-2][colonne].valeur == 5 )):
                                                    self.addTile( ligne-2, colonne)   
                                                else:
                                                    self.effacerBarriere(ligne,colonne)
                                                    if(self.cpu == True and self.curentPlayer == 2):
                                                        self.cpuChoixCase()
                                                        print('erreur', 'selection impossible', ' ligne-2')
                                                    else:                                                        
                                                        messagebox.showinfo('erreur', 'selection impossible 1')
                                                    return

                                        else:
                                            if( (self.possibleBarriere(ligne-2, colonne) == True ) and (self.board.board[ligne-2][colonne].valeur == 5 )):
                                                self.addTile( ligne-2, colonne)   
                                            else:
                                                if( (self.possibleBarriere(ligne+2, colonne) == True ) and (self.board.board[ligne+2][colonne].valeur == 5 )):
                                                    self.addTile( ligne+2, colonne)   
                                                else:
                                                    self.effacerBarriere(ligne,colonne)
                                                    if(self.cpu == True and self.curentPlayer == 2):
                                                        self.cpuChoixCase()
                                                        print('erreur', 'selection impossible', ' ligne+2')
                                                    else:   
                                                        messagebox.showinfo('erreur', 'selection impossible 2')
                                                    return
                                    else:
                                        if(self.cpu == True and self.curentPlayer == 2):
                                            self.cpuChoixCase()
                                            print('erreur', 'selection impossible', ' ligne pas possible')
                                        else:                                                        
                                            print('erreur', 'selection impossible 3')
                                        return
                                else:
                                    if(self.cpu == True and self.curentPlayer == 2):
                                        self.cpuChoixCase()
                                        print('erreur', 'selection impossible', '  pas 5')
                                    else:                                                        
                                        messagebox.showinfo('erreur', 'selection impossible 4')
                                    return
                                        
                            else:  #case
                                if(self.board.board[ligne][colonne].valeur == 0): 
                                    #print('pos : ',ligne,',',colonne , ' possible') 
                                    self.effacerAnciennePosition(self.curentPlayer )
                                    self.board.board[ligne][colonne].valeur = self.curentPlayer  
                                else:
                                    if(self.cpu == True and self.curentPlayer == 2):
                                        self.cpuChoixCase()
                                        print('erreur', 'selection impossible', 'case prise')
                                    else:    
                                        messagebox.showinfo('erreur', 'case prise')
                                        print('pos : ',ligne,',',colonne , ' prise') 
                                    return
                        else:
                            if(colonne%2 == 0): #horz
                                if(self.board.board[ligne][colonne].valeur == 5): 
                                    if(self.possibleBarriere(ligne, colonne)):
                                        self.addTile( ligne, colonne)
                                        self.updateTile(self.curentPlayer)
                                        if(colonne == 0  or (colonne < n-1 and self.curentPlayer == 3)  ):
                                            print('colonne+ 2 ',colonne, ' val :',self.board.board[ligne][colonne+2].valeur)
                                            if((self.possibleBarriere(ligne, colonne+2) == True) and (self.board.board[ligne][colonne+2].valeur == 5 ) ):
                                                self.addTile( ligne, colonne+2)
                                            else:
                                                if((self.possibleBarriere(ligne, colonne-2) == True) and(self.board.board[ligne][colonne-2].valeur == 5 ) ):
                                                    self.addTile( ligne, colonne-2)
                                                else:
                                                    self.effacerBarriere(ligne,colonne)
                                                    if(self.cpu == True and self.curentPlayer == 2):
                                                        self.cpuChoixCase()
                                                        print('erreur', 'selection impossible', 'colonne-2')
                                                    else:
                                                        messagebox.showinfo('erreur', 'selection impossible 5')
                                                    return
                                        else:
                                            if((self.possibleBarriere(ligne, colonne-2) == True) and(self.board.board[ligne][colonne-2].valeur == 5 ) ):
                                                self.addTile( ligne, colonne-2)
                                            else:
                                                if((self.possibleBarriere(ligne, colonne+2) == True) and(self.board.board[ligne][colonne+2].valeur == 5 ) ):
                                                    self.addTile( ligne, colonne+2)
                                                else:
                                                    self.effacerBarriere(ligne,colonne)
                                                    if(self.cpu == True and self.curentPlayer == 2):
                                                        self.cpuChoixCase()
                                                        print('erreur', 'selection impossible', ' ligne+2')
                                                    else:                                                        
                                                        messagebox.showinfo('erreur', 'selection impossible 6')
                                                    return
                                    else:
                                        if(self.cpu == True and self.curentPlayer == 2):
                                            self.cpuChoixCase()
                                            print('erreur', 'selection impossible', ' valeur')
                                        else:  
                                            print('erreur', 'selection impossible', ' 7')                                                      
                                            #messagebox.showinfo('erreur', 'selection impossible 7')
                                        return
                                else:
                                    if(self.cpu == True and self.curentPlayer == 2):
                                        self.cpuChoixCase()
                                        print('erreur', 'selection impossible', 'colonne %2')
                                    else:                                                        
                                        messagebox.showinfo('erreur', 'selection impossible 8')
                                    return

                            else:
                                if(self.cpu == True and self.curentPlayer == 2):
                                    self.cpuChoixCase()
                                    print('erreur', 'selection impossible', ' ')
                                   
                                return     
                                
                        #self.afficher()
                        self.displayBoard()
                        self.displayPlayers()
                         
                        if(self.curentPlayer  < self.nbPlayers ):
                            self.curentPlayer +=1
                        else:
                            self.curentPlayer = 1
                        #print('player :',self.curentPlayer )
                        if(self.cpu == False):
                            self.txt.configure(text=' Au tour du joueur '+str(self.curentPlayer)+' : ', fg=self.players[self.curentPlayer -1 ].color)
                        else:
                            if(self.curentPlayer == 2):
                                self.txt.configure(text=' Au tour du CPU, joeur '+str(self.curentPlayer)+' : ', fg=self.players[self.curentPlayer -1 ].color)
                                self.cpuChoixCase()
                            else:
                                self.txt.configure(text=' Au tour du joueur '+str(self.curentPlayer)+' : ', fg=self.players[self.curentPlayer -1 ].color)
               
                        # 
                 
                    else:
                        print(' Game Over  Player ', self.curentPlayer , ' win')
                        self.effacerAnciennePosition(self.curentPlayer )
                        self.board.board[ligne][colonne].valeur = self.curentPlayer  
                        self.afficher()
                        self.displayBoard()
                        messagebox.showinfo("Game Over", "joueur "+(str)(self.curentPlayer) + "  a gagné")
                else:
                    self.rechoisir()
                    # dans le cas d'un cpu selection automatique de la cse
                    #if(self.cpu == True and self.curentPlayer == 2):
                        #self.cpuChoixCase()
                    #else:
                        #messagebox.showinfo("  erreur "  ," Position impossible")
           
# choix alétoire de la case du CPU
    def cpuChoixCase(self):
        #i,j = self.recupPositionACtuel(2)
        n  =  self.lenBoard  
        ligne = random.randint(0,(n-1)) 
        colonne =  random.randint(0,(n-1)) 
        print('cpu :', ligne , ' : ',colonne)
        self.jouer(ligne,colonne)
         
    #Jouer avec la machine
    def jouerVsCpu(self):
        self.newPartie()
        self.nbPlayers = 2
        # par défaut 8lignes et 5 colonnes
        self.nbLigne = 9
        self.nbTiles = 20
        
        # vérifier les paramètres
        if (self.verfiParametreConf() == True ):
            # une fois les parèmtres configurés et sont bons, choisir les couleurs et  lancer le jeu
            
            self.cpu = True
            self.lancerJeu()           
       