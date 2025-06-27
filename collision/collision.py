import numpy as np
import glfw

class Collision:
    def __init__(self):
        pass

    def check_collision_cc(self, cube1, cube2):   # Check collision beetween two cubes
        min1 = [cube1.position[i] - cube1.taille[i] / 2 for i in range(3)]
        max1 = [cube1.position[i] + cube1.taille[i] / 2 for i in range(3)]
        min2 = [cube2.position[i] - cube2.taille[i] / 2 for i in range(3)]
        max2 = [cube2.position[i] + cube2.taille[i] / 2 for i in range(3)]

        # Détection de collision AABB
        return (min1[0] < max2[0] and max1[0] > min2[0] and
                min1[1] < max2[1] and max1[1] > min2[1] and
                min1[2] < max2[2] and max1[2] > min2[2])
    

        
    def find_collision_cc(self, obj1, obj2):
        # Calcul des overlaps sur chaque axe
        overlaps = []
        for i in range(3):
            min1 = obj1.position[i] - obj1.taille[i] / 2
            max1 = obj1.position[i] + obj1.taille[i] / 2
            min2 = obj2.position[i] - obj2.taille[i] / 2
            max2 = obj2.position[i] + obj2.taille[i] / 2
            overlap = min(max1, max2) - max(min1, min2)
            overlaps.append(overlap)
        # Trouver l'axe avec le plus petit overlap (collision la plus faible)
        min_overlap = min(overlaps)
        axe_index = overlaps.index(min_overlap)
        axe = [0, 1, 2][axe_index]
        return axe
        

    def resolve_collision_cc(self, cube1, cube2):        # Empêche le cube 1 de traverser le cube 2
        direction = self.find_collision_cc(cube1, cube2)
        if direction == 0:
            cube1.velocity[0] = 0
            if cube1.position[0] < cube2.position[0]:
                cube1.position[0] = cube2.position[0] - (cube2.taille[0] + cube1.taille[0]) / 2
            else:
                cube1.position[0] = cube2.position[0] + (cube2.taille[0] + cube1.taille[0]) / 2

        elif direction == 1:
            cube1.velocity[1] = 0
            if cube1.position[1] < cube2.position[1]:
                cube1.position[1] = cube2.position[1] - (cube2.taille[1] + cube1.taille[1]) / 2
            else:
                cube1.position[1] = cube2.position[1] + (cube2.taille[1] + cube1.taille[1]) / 2

        elif direction == 2:
            cube1.velocity[2] = 0
            if cube1.position[2] < cube2.position[2]:
                cube1.position[2] = cube2.position[2] - (cube2.taille[2] + cube1.taille[2]) / 2
            else:
                cube1.position[2] = cube2.position[2] + (cube2.taille[2] + cube1.taille[2]) / 2

   