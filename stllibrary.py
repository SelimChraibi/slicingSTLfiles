#! /usr/bin/env python3

"""
Bibliothèque de lecture des fichier stl
"""

import struct
from trianglelibrary import Triangle

def read_stl(name_of_file):
    """
    Lit le fichier stl binaire et renvoie
    un tableau contenant tous les triangles.

    Les triangles sont classés selon
    la hauteur de leur sommet de hauteur maximale.
    """
    with open(name_of_file, "rb") as file:
        file.read(80) # On lit l'entête
        file.read(4) # On lit le nombre de triangle
        data = []
        while True:
            try:
                file.read(3*4) # On lit les coordonnées du vecteur normal au triangle
                triangle = Triangle()
                for _ in range(3):
                    point = []
                    for _ in range(3):
                        coordonnee = struct.unpack('<f', file.read(4))[0]
                        point.append(coordonnee)
                    triangle.ajouter(point)
                data.append(triangle)
                file.read(2*1) # On lit le 'Attribute byte count'
            except struct.error: # On arrive au bout du fichier
                break
    data.sort(key=lambda triangle: triangle.sommets[2])
    return data


# from stl import mesh
# MESH = mesh.Mesh.from_file('Tux_printable.stl')
# print(MESH.data[1])
