import numpy as np

class Object:
    def __init__(self):
        pass
    
    def cube(self):
                # On place ici tous les sommets en une seule liste
        positions = [
            # Face avant
            (0, 0, 1), (1, 0, 1), (1, 1, 1), (0, 1, 1),
            # Face arrière
            (1, 0, 0), (0, 0, 0), (0, 1, 0), (1, 1, 0),
            # Face droite
            (1, 0, 1), (1, 0, 0), (1, 1, 0), (1, 1, 1),
            # Face gauche
            (0, 0, 0), (0, 0, 1), (0, 1, 1), (0, 1, 0),
            # Face supérieure
            (0, 1, 1), (1, 1, 1), (1, 1, 0), (0, 1, 0),
            # Face inférieure
            (0, 0, 0), (1, 0, 0), (1, 0, 1), (0, 0, 1),
        ]

        normales = [
            (0, 0, 1)] * 4 + [(0, 0, -1)] * 4 + [(1, 0, 0)] * 4 + \
            [(-1, 0, 0)] * 4 + [(0, 1, 0)] * 4 + [(0, -1, 0)] * 4

        couleurs = [
            (1, 0, 0)] * 4 + [(0, 1, 0)] * 4 + [(0, 0, 1)] * 4 + \
            [(1, 1, 0)] * 4 + [(0, 1, 1)] * 4 + [(1, 0, 1)] * 4

        uvs = [(0, 0), (1, 0), (1, 1), (0, 1)] * 6

        # Fusion de tous les attributs pour chaque sommet
        self.vertices_cube = np.array([  # Fixed: Assign to self.vertices_cube
            positions[i] + normales[i] + couleurs[i] + uvs[i]
            for i in range(24)
        ], dtype=np.float32)

        # Indexation des triangles : 2 triangles par face
        self.indices = np.array([  # Fixed: Assign to self.indices
            0, 1, 2, 0, 2, 3,        # Face avant
            4, 5, 6, 4, 6, 7,        # Face arrière
            8, 9,10, 8,10,11,        # Face droite
            12,13,14,12,14,15,        # Face gauche
            16,17,18,16,18,19,        # Face supérieure
            20,21,22,20,22,23         # Face inférieure
        ], dtype=np.uint32)