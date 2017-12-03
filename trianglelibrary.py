#! /usr/bin/env python3

"""
Bibliothèque définissant la classe Triangle et quelques méthodes
"""

class Triangle():
    """
    Classe Triangle
    """
    def __init__(self):
        self.sommets = []
        self.nombre_de_points = 0
    def ajouter(self, point):
        """
        Lorsque le triangle n'a pas reçu tous ces sommets, on peut lui ajouter un sommmet.
        Les sommets du triangles sont classés par hauteur croissante
        """
        if self.nombre_de_points < 3:
            self.sommets.append(point)
            self.sommets.sort(key=lambda point: point[2])
            self.nombre_de_points += 1

    def coordonnees_intersection(self, plan):
        """
        Renvoie les coordonnées [x, y] des points du segment
        d'intersection entre le triangle et le plan
        """
        [x_1, y_1, z_1] = self.sommets[0]
        [x_2, y_2, z_2] = self.sommets[1]
        [x_3, y_3, z_3] = self.sommets[2]
        plan = plan

        abscisse1 = (plan - z_1)*(x_3 - x_1)/(z_3 - z_1) + x_1
        ordonnee1 = (plan - z_1)*(y_3 - y_1)/(z_3 - z_1) + y_1
        if z_2 >= plan:
            abscisse2 = (plan - z_1)*(x_2 - x_1)/(z_2 - z_1) + x_1
            ordonnee2 = (plan - z_1)*(y_2 - y_1)/(z_2 - z_1) + y_1
        else:
            abscisse2 = (plan - z_2)*(x_3 - x_2)/(z_3 - z_2) + x_2
            ordonnee2 = (plan - z_2)*(y_3 - y_2)/(z_3 - z_2) + y_2
        return [[abscisse1, ordonnee1], [abscisse2, ordonnee2]]
    def extreme(self, max_ou_min, coordonnee):
        """
        Retourne l'abscisse ou l'ordonnee ou la hauteur
        maximale ou minimale parmis les points du triangle
        """
        return max_ou_min(self.sommets, key=lambda point: point[coordonnee])[coordonnee]

    def intersecte(self, plan):
        """
        Test renvoyant True si le triangle intersecte le plan et False sinon
        """
        return self.extreme(max, 2) >= plan and self.extreme(min, 2) <= plan
