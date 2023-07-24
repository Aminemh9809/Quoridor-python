from game import Game
from Reseau import Reseau
import tkinter as tk
import pygame
 
    
root = tk.Tk()
root.title("QUORIDOR")

v = tk.IntVar()
#v.set()  # initializing the choice, i.e. Python

languages = [
   	     ("Jouer en Local", 1),
    	     ("Jouer sur le Réseau", 2) ]

def ShowChoice():
    selection = v.get()
    print(selection)
    if (selection == 1):
            root.quit  
            Game() 
    else:
            root.quit  
            print("Reseau")  
            Reseau()
def play():
        pygame.init()
        pygame.mixer.init()
     
        pygame.mixer.music.load('1.mp3')
        pygame.mixer.music.play(loops=0)
    
def stop():
      pygame.mixer.music.stop()

tk.Label(root, 
         text="""Choisissez votre mode de jeu:""",
         justify = tk.LEFT,
         padx = 20).pack()

for language, val in languages:
    tk.Radiobutton(root, 
                   text=language,
                   padx = 20, 
                   variable=v, 
                   command=ShowChoice,
                   value=val).pack(anchor=tk.W)

# making a button which trigger the function so sound can be playeed
play_button = tk.Button(root, text="Play Song", font=("Helvetica", 10),
                     relief=tk.GROOVE, command=play)
play_button.pack(pady=5)
 
stop_button = tk.Button(root, text="Stop Song", font=("Helvetica", 10),
                        relief=tk.GROOVE, command=stop)
                        
stop_button.pack(pady=5)

root.mainloop()
      