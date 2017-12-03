#!/usr/bin/env python3
"""
Bibliothèque permettant de généré du code svg
"""

import os

def set_scale(largeur, longueur):
    """
    Pour que la taille des images soit suffisante,
    on calcul un facteur par lequel on va multiplier les dimmension des images
    """
    return 1000/((largeur + longueur)/2)


def nouveau_fichier(nom, largeur, longueur, scale):
    """
    Cré un nouveau fichier et y ajoute l'entête
    """
    newpath = './slices/'
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    with open(newpath+"/"+nom, "w") as file:
        file.write("""<svg width="{}" height="{}" xmlns="http://www.w3.org/2000/svg">\n"""\
        .format(largeur*scale, longueur*scale))
    return nom

def pied(fichier):
    """
    Ajoute le pied du svg
    """
    with open("./slices/"+fichier, "a") as file:
        file.write("</svg>\n")

#pylint: disable=too-many-arguments

def ajouter_segment(fichier, point1, point2, x_min, y_min, scale):
    """
    Génère le code svg permettant d'afficher un segment
    Remarque : Les points sont translatés de sorte que le point d'abscisse minimale soit en (0, _)
    et que celui d'ordonnée minimale soit en (_, 0)
    """
    with open("./slices/"+fichier, "a") as file:
        file.write("""<line x1="{}" y1="{}" x2="{}" y2="{}" stroke-width="5" stroke="red" />\n"""\
        .format((point1[0] - x_min)*scale, (point1[1] - y_min)*scale, \
        (point2[0] - x_min)*scale, (point2[1] - y_min)*scale))
