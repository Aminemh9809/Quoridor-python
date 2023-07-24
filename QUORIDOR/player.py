from tile import Tile
class Player: # joueur
    def __init__(self,nb,color,tiles,lettre):
        self.tiles = tiles
        self.color = color
        self.lettre = lettre
        self.nbTilesDefault=nb
        self.nbTiles=nb
        
    
  