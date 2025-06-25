import numpy as np

def generate_cube():
    # On place ici tous les sommets en une seule liste, centrés autour de l'origine
    positions = [
        # Face avant
        (-0.5, -0.5,  0.5), ( 0.5, -0.5,  0.5), ( 0.5,  0.5,  0.5), (-0.5,  0.5,  0.5),
        # Face arrière
        ( 0.5, -0.5, -0.5), (-0.5, -0.5, -0.5), (-0.5,  0.5, -0.5), ( 0.5,  0.5, -0.5),
        # Face droite
        ( 0.5, -0.5,  0.5), ( 0.5, -0.5, -0.5), ( 0.5,  0.5, -0.5), ( 0.5,  0.5,  0.5),
        # Face gauche
        (-0.5, -0.5, -0.5), (-0.5, -0.5,  0.5), (-0.5,  0.5,  0.5), (-0.5,  0.5, -0.5),
        # Face supérieure
        (-0.5,  0.5,  0.5), ( 0.5,  0.5,  0.5), ( 0.5,  0.5, -0.5), (-0.5,  0.5, -0.5),
        # Face inférieure
        (-0.5, -0.5, -0.5), ( 0.5, -0.5, -0.5), ( 0.5, -0.5,  0.5), (-0.5, -0.5,  0.5),
    ]

    normales = [
        (0, 0, 1)] * 4 + [(0, 0, -1)] * 4 + [(1, 0, 0)] * 4 + \
        [(-1, 0, 0)] * 4 + [(0, 1, 0)] * 4 + [(0, -1, 0)] * 4

    couleurs = [(1, 1, 1)] * 24  # Couleur blanche pour tous les sommets

    uvs = [(0, 0), (1, 0), (1, 1), (0, 1)] * 6

    # Fusion de tous les attributs pour chaque sommet
    vertices_cube = np.array([
        positions[i] + normales[i] + couleurs[i] + uvs[i]
        for i in range(24)
    ], dtype=np.float32)

    # Indexation des triangles : 2 triangles par face
    indices = np.array([
        0, 1, 2, 0, 2, 3,        # Face avant
        4, 5, 6, 4, 6, 7,        # Face arrière
        8, 9,10, 8,10,11,        # Face droite
        12,13,14,12,14,15,       # Face gauche
        16,17,18,16,18,19,       # Face supérieure
        20,21,22,20,22,23        # Face inférieure
    ], dtype=np.uint32)

    return vertices_cube, indices