import numpy as np

class Collision:
    def __init__(self):
        pass

    def check_collision(self, obj1, obj2):
        if (obj1.position[0] < obj2.position[0] + obj2.taille[0] and # axe X
            obj1.position[0] + obj1.taille[0] > obj2.position[0] and
            obj1.position[1] < obj2.position[1] + obj2.taille[1] and # axe Y
            obj1.position[1] + obj1.taille[1] > obj2.position[1] and
            obj1.position[2] < obj2.position[2] + obj2.taille[2] and # axe Z
            obj1.position[2] + obj1.taille[2] > obj2.position[2]):
            return True
        return False
    
    def find_collision(self, obj1, obj2):
        center1 = [obj1.position[i] + obj1.taille[i] / 2 for i in range(3)]
        center2 = [obj2.position[i] + obj2.taille[i] / 2 for i in range(3)]
        direction = None
        dx = (obj1.taille[0] + obj2.taille[0]) / 2 - abs(center1[0] - center2[0])
        dy = (obj1.taille[1] + obj2.taille[1]) / 2 - abs(center1[1] - center2[1])
        dz = (obj1.taille[2] + obj2.taille[2]) / 2 - abs(center1[2] - center2[2])
        if self.check_collision(obj1, obj2):
            if dx < dy and dx < dz:
                direction = 0
            elif dy < dx and dy < dz:
                direction = 1
            else:
                direction = 2
        return direction
    
    def resolve_collision(self, obj1, obj2):        # Empêche l'objet 1 de traverser l'objet 2
        direction = self.find_collision(obj1, obj2)
        if direction is not None:
            if direction == 0:
                obj1.velocity[0] = 0
                obj1.position[0] = obj2.position[0] + obj2.taille[0]
            elif direction == 1:
                obj1.velocity[1] = 0
                obj1.position[1] = obj2.position[1] + obj2.taille[1]
            elif direction == 2:
                obj1.velocity[2] = 0
                obj1.position[2] = obj2.position[2] + obj2.taille[2]