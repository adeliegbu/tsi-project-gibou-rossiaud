import numpy as np

def generate_mur(taille=(1.0, 1.0, 1.0)):
    # Définir les positions des sommets pour un mur (pavé)
    positions = [
        # Face avant
        (-taille[0] / 2, -taille[1] / 2, taille[2] / 2), (taille[0] / 2, -taille[1] / 2, taille[2] / 2),
        (taille[0] / 2, taille[1] / 2, taille[2] / 2), (-taille[0] / 2, taille[1] / 2, taille[2] / 2),
        # Face arrière
        (taille[0] / 2, -taille[1] / 2, -taille[2] / 2), (-taille[0] / 2, -taille[1] / 2, -taille[2] / 2),
        (-taille[0] / 2, taille[1] / 2, -taille[2] / 2), (taille[0] / 2, taille[1] / 2, -taille[2] / 2),
        # Face droite
        (taille[0] / 2, -taille[1] / 2, taille[2] / 2), (taille[0] / 2, -taille[1] / 2, -taille[2] / 2),
        (taille[0] / 2, taille[1] / 2, -taille[2] / 2), (taille[0] / 2, taille[1] / 2, taille[2] / 2),
        # Face gauche
        (-taille[0] / 2, -taille[1] / 2, -taille[2] / 2), (-taille[0] / 2, -taille[1] / 2, taille[2] / 2),
        (-taille[0] / 2, taille[1] / 2, taille[2] / 2), (-taille[0] / 2, taille[1] / 2, -taille[2] / 2),
        # Face supérieure
        (-taille[0] / 2, taille[1] / 2, taille[2] / 2), (taille[0] / 2, taille[1] / 2, taille[2] / 2),
        (taille[0] / 2, taille[1] / 2, -taille[2] / 2), (-taille[0] / 2, taille[1] / 2, -taille[2] / 2),
        # Face inférieure
        (-taille[0] / 2, -taille[1] / 2, -taille[2] / 2), (taille[0] / 2, -taille[1] / 2, -taille[2] / 2),
        (taille[0] / 2, -taille[1] / 2, taille[2] / 2), (-taille[0] / 2, -taille[1] / 2, taille[2] / 2)
    ]

    normales = [
        (0, 0, 1)] * 4 + [(0, 0, -1)] * 4 + [(1, 0, 0)] * 4 + \
        [(-1, 0, 0)] * 4 + [(0, 1, 0)] * 4 + [(0, -1, 0)] * 4

    couleurs = [(1, 1, 1)] * 24  # Couleur blanche pour tous les sommets

    uvs = [(0, 0), (1, 0), (1, 1), (0, 1)] * 6

    # Fusionner tous les attributs pour chaque sommet
    vertices = np.array([
        positions[i] + normales[i] + couleurs[i] + uvs[i]
        for i in range(24)
    ], dtype=np.float32)

    # Indexation des triangles : 2 triangles par face
    indices = np.array([
        0, 1, 2, 0, 2, 3,  # Face avant
        4, 5, 6, 4, 6, 7,  # Face arrière
        8, 9, 10, 8, 10, 11,  # Face droite
        12, 13, 14, 12, 14, 15,  # Face gauche
        16, 17, 18, 16, 18, 19,  # Face supérieure
        20, 21, 22, 20, 22, 23  # Face inférieure
    ], dtype=np.uint32)

    return vertices, indices
