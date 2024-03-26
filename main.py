import pygame
import sys
import json
import os
import random
import time
from config import Config

from pygame.locals import *

from datetime import datetime


def quit():
    pygame.quit()
    sys.exit()


def difference_en_secondes(date1, date2):
    # Conversion des chaînes de caractères en objets datetime

    date1 = datetime.strptime(date1, "%Y-%m-%d %H:%M:%S")
    date2 = datetime.strptime(date2, "%Y-%m-%d %H:%M:%S")

    # Calcul de la différence en secondes

    difference = abs((date2 - date1).total_seconds())

    return int(difference)


def attente(date):
    while True:
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")

        if difference_en_secondes(date, current_time) == 0:
            print("départ")
            break
        time.sleep(0.05)


difference_secondes = difference_en_secondes(Config.date1, Config.date2)


def main():
    # Create a clock object

    clock = pygame.time.Clock()
    pygame.init()
    display = pygame.display.set_mode(Config.SCREEN_SIZE)
    try:
        imagefile1 = os.path.join("data", "image1.png")
        imagefile2 = os.path.join("data", "image2.png")
        surf1 = pygame.image.load(imagefile1)
        surf2 = pygame.image.load(imagefile2)
    except IOError as e:
        print(f"{str(e)}")
        quit()
        
    if os.path.exists("pixels.json") :
        print("Le fichier existe déjà")
         #récupérer l'ordre des pixels
        pixels = 
        
    else : 
        # fabriquer liste coordonnées possibles
        pixels = [
            (x, y) for x in range(Config.SCREEN_WIDTH) for y in range(Config.SCREEN_HEIGHT)
        ]

        # mélanger cette liste

        random.shuffle(pixels)
        json_liste = json.dumps(pixels)
        filename: str = "pixels.json"
        file = open(filename, "w")
        file.write(json_liste)q
        file.close()

        nb_pixels = Config.SCREEN_HEIGHT * Config.SCREEN_WIDTH
        print("nb pixels", nb_pixels)
    # Start the main loop

    attente(Config.date1)
    
    index = 0

    while True:

        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        temps_restant = difference_en_secondes(current_time, Config.date2)
        if temps_restant <= 0 :
            break
        pixels_etape = (nb_pixels - index) // temps_restant

        # Get events from the event queue

        for event in pygame.event.get():
            # Check for the quit event

            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYUP:
                # quit when Q is pressed

                if event.key == K_q:
                    quit()
        for i in range(pixels_etape):
            x, y = pixels[i + index]
            color = surf2.get_at((x, y))
            surf1.set_at((x, y), color)
            
        index += pixels_etape
        # Update the game state

        display.blit(surf1, (0, 0))
        # Draw the game screen

        pygame.display.update()

        # Limit the FPS by sleeping for the remainder of the frame time

        clock.tick(Config.desired_fps)
        
        


main()

