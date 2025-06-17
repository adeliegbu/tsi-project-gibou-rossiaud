import numpy as np
import glfw

class Collision:
    def __init__(self):
        pass

    def check_collision_cc(self, cube1, cube2):   # Check collision beetween two cubes
        if (cube1.position[0] < cube2.position[0] + cube2.taille[0] and # axe X
            cube1.position[0] + cube1.taille[0] > cube2.position[0] and
            cube1.position[1] < cube2.position[1] + cube2.taille[1] and # axe Y
            cube1.position[1] + cube1.taille[1] > cube2.position[1] and
            cube1.position[2] < cube2.position[2] + cube2.taille[2] and # axe Z
            cube1.position[2] + cube1.taille[2] > cube2.position[2]):
            return True
        return False
  

    
    def check_collision_ss(self, sphere1, sphere2):   # Check collision beetween two spheres
        distance = np.sqrt((sphere2.position[0] - sphere1.position[0])**2 + (sphere2.position[1] - sphere1.position[1])**2 + (sphere2.position[2] - sphere1.position[2])**2)
        if distance <= sphere1.radius + sphere2.radius:
            return True
        return False
    
    def check_collision_cs(self, cube, sphere):   # Check collision beetween a cube and a sphere
        center = [cube.position[i] + cube.taille[i] / 2 for i in range(3)]
        distance = np.sqrt((sphere.position[0] - center[0])**2 + (sphere.position[1] - center[1])**2 + (sphere.position[2] - center[2])**2)
        if distance <= cube.taille[0] / 2 + sphere.radius:
            return True
        return False

    
    def find_collision_cc(self, obj1, obj2):
        if self.check_collision_cc(obj1, obj2):
            center1 = [obj1.position[i] + obj1.taille[i] / 2 for i in range(3)]
            center2 = [obj2.position[i] + obj2.taille[i] / 2 for i in range(3)]
            direction = -1
            dx = (obj1.taille[0] + obj2.taille[0]) / 2 - abs(center1[0] - center2[0])
            dy = (obj1.taille[1] + obj2.taille[1]) / 2 - abs(center1[1] - center2[1])
            dz = (obj1.taille[2] + obj2.taille[2]) / 2 - abs(center1[2] - center2[2])
            if dx < dy and dx < dz:
                direction = 0 
            elif dy < dx and dy < dz:
                direction = 1
            else:
                direction = 2
            return direction
    
    def find_collision_ss(self, sphere1, sphere2):
        if self.check_collision_ss(sphere1, sphere2):
            delta = [sphere2.position[i] - sphere1.position[i] for i in range(3)]
            abs_delta = [abs(d) for d in delta]
            direction = abs_delta.index(max(abs_delta))
            return direction  # 0 = X, 1 = Y, 2 = Z
        
    def find_collision_cs(self, cube, sphere):
        if self.check_collision_cs(cube, sphere):
            # Trouver le point le plus proche du centre de la sphère sur l’AABB (cube)
            closest_point = [0, 0, 0]
            for i in range(3):
                min_face = cube.position[i]
                max_face = cube.position[i] + cube.taille[i]
                closest_point[i] = max(min_face, min(sphere.position[i], max_face))

            # Calculer le vecteur de collision
            delta = [sphere.position[i] - closest_point[i] for i in range(3)]
            abs_delta = [abs(d) for d in delta]

            # Détermine l’axe principal de la collision
            direction = abs_delta.index(max(abs_delta))
            return direction  # 0 = X, 1 = Y, 2 = Z
        

    def resolve_collision_cc(self, cube1, cube2):        # Empêche le cube 1 de traverser le cube 2
        direction = self.find_collision_cc(cube1, cube2)
        if direction == 0:
            cube1.velocity[0] = 0
            cube1.position[0] = cube2.position[0] + cube2.taille[0]
        elif direction == 1 and glfw.get_key(cube1.window, glfw.KEY_SPACE) != glfw.PRESS:
            cube1.velocity[1] = 0
            cube1.position[1] = cube2.position[1] + cube2.taille[1]
        elif direction == 2:
            cube1.velocity[2] = 0
            cube1.position[2] = cube2.position[2] + cube2.taille[2]
        return direction

    def resolve_collision_ss(self, sphere1, sphere2):
        direction = self.find_collision_ss(sphere1, sphere2)
        if direction == 0:
            sphere1.velocity[0] = 0
            sphere1.position[0] = sphere2.position[0] + sphere2.radius + sphere1.radius
        elif direction == 1:
            sphere1.velocity[1] = 0
            sphere1.position[1] = sphere2.position[1] + sphere2.radius + sphere1.radius
        elif direction == 2:
            sphere1.velocity[2] = 0
            sphere1.position[2] = sphere2.position[2] + sphere2.radius + sphere1.radius
        return direction
    
    def resolve_collision_cs_sphere_to_stop(self, cube, sphere):
        direction = self.find_collision_cs(cube, sphere)
        if direction == 0:
            sphere.velocity[0] = 0
            sphere.position[0] = cube.position[0] + cube.taille[0] / 2 + sphere.radius
        elif direction == 1:
            sphere.velocity[1] = 0
            sphere.position[1] = cube.position[1] + cube.taille[1] / 2 + sphere.radius
        elif direction == 2:
            sphere.velocity[2] = 0
            sphere.position[2] = cube.position[2] + cube.taille[2] / 2 + sphere.radius
        return direction
    
    def resolve_collision_cs_cube_to_stop(self, cube, sphere):
        direction = self.find_collision_cs(cube, sphere)
        if direction == 0:
            cube.velocity[0] = 0
            cube.position[0] = sphere.position[0] - sphere.radius - cube.taille[0] / 2
        elif direction == 1:
            cube.velocity[1] = 0
            cube.position[1] = sphere.position[1] - sphere.radius - cube.taille[1] / 2
        elif direction == 2:
            cube.velocity[2] = 0
            cube.position[2] = sphere.position[2] - sphere.radius - cube.taille[2] / 2
        return direction