import pygame
import sys
import os
import random
import time
 
from pygame.locals import *

from datetime import datetime

 
class Config:
    SCREEN_WIDTH = 3840
    SCREEN_HEIGHT = 2160
    SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
    desired_fps = 1
    date1 = '2024-03-05 12:00:00'
    date2 = '2024-03-05 12:01:00'
    
def quit():
    pygame.quit()
    sys.exit()
    
def difference_en_secondes(date1, date2):
    # Conversion des chaînes de caractères en objets datetime
    date1 = datetime.strptime(date1, '%Y-%m-%d %H:%M:%S')
    date2 = datetime.strptime(date2, '%Y-%m-%d %H:%M:%S')
    
    # Calcul de la différence en secondes
    difference = abs((date2 - date1).total_seconds())
    
    return int(difference)
 
difference_secondes = difference_en_secondes(Config.date1,Config.date2)
 
def main():
    # Create a clock object
    clock = pygame.time.Clock()
    pygame.init()
    display = pygame.display.set_mode(Config.SCREEN_SIZE)
    try:
        imagefile1 = os.path.join('data', 'image1.png')
        imagefile2 = os.path.join('data', 'image2.png')
        surf1 = pygame.image.load(imagefile1)
        surf2 = pygame.image.load(imagefile2)
    except IOError as e:
        print(f"{str(e)}")
        quit()
    
    #fabriquer liste coordonnées possibles    
    pixels = [(x,y) for x in range(Config.SCREEN_WIDTH) for y in range(Config.SCREEN_HEIGHT)]

    #mélanger cette liste
    random.shuffle(pixels)
    
    nb_pixels = Config.SCREEN_HEIGHT * Config.SCREEN_WIDTH
    print("nb pixels", nb_pixels)
    # Start the main loop
    while True:
        # Get events from the event queue
        for event in pygame.event.get():
            # Check for the quit event
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYUP:
                # quit when Q is pressed
                if event.key == K_q:
                    quit()
         
        for i in range(nb_pixels//difference_secondes):
            x,y = pixels[i]
            color = surf2.get_at((x, y))
            surf1.set_at((x, y), color)

 
        # Update the game state
        display.blit(surf1, (0, 0))
        # Draw the game screen
        pygame.display.update()
 
        # Limit the FPS by sleeping for the remainder of the frame time
        clock.tick(Config.desired_fps)
main()
