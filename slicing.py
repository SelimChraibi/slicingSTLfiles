#! /usr/bin/env python3

"""
Decoupage d'une figure 3D en n plans (n choisi par l'utilisateur)
Chaque plan est déssinée dans un fichier svg
"""

from pathlib import Path
import argparse
import re
from stllibrary import read_stl


import svglibrary

def main():
    """
    Récupère le nombre de plan
    Récupère les données depuis le fichier
    Récupère les dimensions
    Récupère l'échelle
    Pour chaque plan
        Cré un fichier svg
        Cré un générateur de triangles
        Récupere le premier triangle de triangles
        Pour chaque triangle
            Si le triangle intersecte le plan
                Ajoute un point d'intersection entre le triangle et le plan au fichier svg
        Termine le fichier svg
    """
    nombre_de_plans, nom_du_fichier = get_entries()
    data = read_stl(nom_du_fichier)
    x_min, y_min, largeur, longueur = get_dimensions(data)
    scale = svglibrary.set_scale(largeur, longueur)
    for (indice_plan, plan) in enumerate(plans(nombre_de_plans, data)):
        generateurs_de_triangles = triangles(data)
        fichier_svg = svglibrary.nouveau_fichier("""{}-{}.svg"""\
        .format(nom_du_fichier[:-4], indice_plan+1), largeur, longueur, scale)
        for triangle in generateurs_de_triangles:
            if triangle.intersecte(plan):
                [point1, point2] = triangle.coordonnees_intersection(plan)
                svglibrary.ajouter_segment(fichier_svg, point1, point2, x_min, y_min, scale)
        svglibrary.pied(fichier_svg)

def get_entries():
    """
    Récupère les entrées et gère les exeptions
    """
    def pos_int(variable):
        """
        Type 'entier strictement positif' qui sera utilisé dans le parseur
        """
        try:
            entier = int(variable)
            assert entier > 0
            return entier
        except (ValueError, AssertionError):
            raise argparse.ArgumentTypeError("{} n'est pas un entier strictement positif".\
            format(variable))

    def svg_file(nom_du_fichier):
        """
        Type 'fichier svg' qui sera utilisé dans le parseur
        """
        if not (Path(nom_du_fichier).is_file() and re.compile(".*(.stl)$").match(nom_du_fichier)):
            raise argparse.ArgumentTypeError("{} n'est pas un fichier stl ou n'a pas été trouvé".\
            format(nom_du_fichier))
        return nom_du_fichier

    parser = argparse.ArgumentParser(description='Slicing 3D STL files.\
    The slices are saved in the "slices" directory')

    parser.add_argument('-s', '--slices', type=pos_int, help='Number of slices \
    (equals 4 by default)', default=4)
    parser.add_argument('file', type=svg_file, help='Name of the stl file. \
    Must be in the same directory as the python programm.')
    nombre_de_plans, nom_du_fichier = parser.parse_args().slices, parser.parse_args().file

    return nombre_de_plans, nom_du_fichier

def triangles(data):
    """
    Itérateur sur des le tableau de triangle, renvoyant les triangles un par un
    """
    for triangle in data:
        yield triangle

def plans(nombre_de_plans, data):
    """
    Itérateur renvoyant les ordonnées des plans horizontaux
    """
    z_max = max(data, key=lambda triangle: triangle.extreme(max, 2)).extreme(max, 2)
    z_min = min(data, key=lambda triangle: triangle.extreme(min, 2)).extreme(min, 2)

    ecart_entre_plans = (z_max - z_min)/nombre_de_plans

    for indice in range(nombre_de_plans):
        yield z_min + ecart_entre_plans*(indice + 1)

def get_dimensions(data):
    """
    Récupère l'abscisse maximale, l'abscisse minimale, la largeur et la longueur du l'image 3D
    """
    x_max = max(data, key=lambda triangle: triangle.extreme(max, 0)).extreme(max, 0)
    x_min = min(data, key=lambda triangle: triangle.extreme(min, 0)).extreme(min, 0)
    y_max = max(data, key=lambda triangle: triangle.extreme(max, 1)).extreme(max, 1)
    y_min = min(data, key=lambda triangle: triangle.extreme(min, 1)).extreme(min, 1)

    largeur = x_max - x_min
    longueur = y_max - y_min

    return x_min, y_min, largeur, longueur

main()
