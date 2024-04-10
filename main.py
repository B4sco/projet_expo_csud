# Ce code à été écrit completement en duo


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


# Cette fonction a été demandé à chatgpt avec le prompt : "Donne moi une code python qui calcul le nombre de seconde entre des dates et heures différentes"


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
            print(f"Départ à : {current_time}")
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
    # vérifier si la liste de pixel existe déjà

    if os.path.exists("pixels.json"):
        print("La liste des pixels (pixels.json) a déjà été définie")
        # récupérer l'ordre des pixels

        with open("pixels.json", "r") as fichier:
            pixels = json.load(fichier)

            # vérifier que le fichier json contient le bon nombre de pixel pour la résolution indiqué dans la config

            if len(pixels) == Config.SCREEN_HEIGHT * Config.SCREEN_WIDTH:
                nb_pixels = len(pixels)
                print("Le nombre de pixel correspond à la résolution")
            else:
                print(
                    "Le fichier json n'est pas adapté à la résolution indiqué dans config.py, merci de modifier la config ou de supprimer le fichier pixels.json afin qu'un nouveau fichier adapté soit créer au prochain lancement"
                )
                quit()
    else:
        print(
            "La liste des pixels n'a pas encore été définie, création de cette liste dans un nouveau fichier nommé : pixels.json"
        )
        # fabriquer liste coordonnées possibles

        pixels = [
            (x, y)
            for x in range(Config.SCREEN_WIDTH)
            for y in range(Config.SCREEN_HEIGHT)
        ]

        # mélanger cette liste

        random.shuffle(pixels)
        json_liste = json.dumps(pixels)
        filename: str = "pixels.json"
        file = open(filename, "w")
        file.write(json_liste)
        file.close()

        print("Liste créée avec succès")

        nb_pixels = Config.SCREEN_HEIGHT * Config.SCREEN_WIDTH
    # Start the main loop

    current_time = time.strftime("%Y-%m-%d %H:%M:%S")
    # Si on est entre date1 et date2 (le départ à été retardé), on modifie les pixels déjà passés

    if Config.date1 <= current_time < Config.date2:

        print("Le programme a été lancé en retard")
        temps_ecoule = difference_en_secondes(Config.date1, current_time)
        index2 = temps_ecoule * (
            nb_pixels // difference_en_secondes(Config.date1, Config.date2)
        )
        for i in range(index2):
            x, y = pixels[i]
            color = surf2.get_at((x, y))
            surf1.set_at((x, y), color)
        index = index2
        print(f"Départ en retard à : {current_time} au lieu de : {Config.date1}")
    else:
        print(
            f"Le programme est prêt, départ prévu à : {Config.date1}, fin prévue à : {Config.date2}"
        )
        attente(Config.date1)
        index = 0
    while True:

        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        temps_restant = difference_en_secondes(current_time, Config.date2)
        if temps_restant <= 0:
            break
        pixels_etape = (nb_pixels - index) // temps_restant

        # Get events from the event queue

        for event in pygame.event.get():
            # Check for the quit event

            if event.type == pygame.QUIT:
                print(
                    f"Le programe s'est arrêté à : {current_time}, fin du programme prévu à : {Config.date2}"
                )
                quit()
            if event.type == pygame.KEYUP:
                # quit when Q is pressed

                if event.key == K_q:
                    print(
                        f"Le programe à été arrêté manuellement un appuyant sur la touche q à : {current_time}, fin du programme prévu à : {Config.date2}"
                    )
                    quit()
        # modification des pixels de l'étape

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
    print(
        f"Le programe s'est arrêté à : {current_time}, fin du programme prévu à : {Config.date2}"
    )


main()
