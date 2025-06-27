import numpy as np

def generate_cube(width=1.0, height=1.0, depth=1.0):
    """
    Génère un cube avec des dimensions personnalisées
    
    Args:
        width (float): Largeur du cube (axe X)
        height (float): Hauteur du cube (axe Y) 
        depth (float): Profondeur du cube (axe Z)
    
    Returns:
        tuple: (vertices_cube, indices) - données du cube
    """
    # Calcul des demi-dimensions
    half_width = width / 2.0
    half_height = height / 2.0
    half_depth = depth / 2.0
    
    # Positions des sommets avec les nouvelles dimensions
    positions = [
        # Face avant
        (-half_width, -half_height,  half_depth), ( half_width, -half_height,  half_depth), 
        ( half_width,  half_height,  half_depth), (-half_width,  half_height,  half_depth),
        # Face arrière
        ( half_width, -half_height, -half_depth), (-half_width, -half_height, -half_depth), 
        (-half_width,  half_height, -half_depth), ( half_width,  half_height, -half_depth),
        # Face droite
        ( half_width, -half_height,  half_depth), ( half_width, -half_height, -half_depth), 
        ( half_width,  half_height, -half_depth), ( half_width,  half_height,  half_depth),
        # Face gauche
        (-half_width, -half_height, -half_depth), (-half_width, -half_height,  half_depth), 
        (-half_width,  half_height,  half_depth), (-half_width,  half_height, -half_depth),
        # Face supérieure
        (-half_width,  half_height,  half_depth), ( half_width,  half_height,  half_depth), 
        ( half_width,  half_height, -half_depth), (-half_width,  half_height, -half_depth),
        # Face inférieure
        (-half_width, -half_height, -half_depth), ( half_width, -half_height, -half_depth), 
        ( half_width, -half_height,  half_depth), (-half_width, -half_height,  half_depth),
    ]

    normales = [
        (0, 0, 1)] * 4 + [(0, 0, -1)] * 4 + [(1, 0, 0)] * 4 + \
        [(-1, 0, 0)] * 4 + [(0, 1, 0)] * 4 + [(0, -1, 0)] * 4

    couleurs = [(1, 1, 1)] * 24  # Couleur blanche pour tous les sommets

    # Coordonnées UV adaptées aux dimensions
    if width == 1.0 and height == 1.0 and depth == 1.0:
        # Si le cube est de taille 1, on utilise les UV standards
        uvs = [
            (0, 0), (1, 0), (1, 1), (0, 1),  # Face avant
            (0, 0), (1, 0), (1, 1), (0, 1),  # Face arrière
            (0, 0), (1, 0), (1, 1), (0, 1),  # Face droite
            (0, 0), (1, 0), (1, 1), (0, 1),  # Face gauche
            (0, 0), (1, 0), (1, 1), (0, 1),  # Face supérieure
            (0, 0), (1, 0), (1, 1), (0, 1)   # Face inférieure
        ]
    else:
        uvs = [
            # Face avant (width x height)
            (0, 0), (width/2, 0), (width/2, height/2), (0, height/2),
            # Face arrière (width x height)  
            (0, 0), (width/2, 0), (width/2, height/2), (0, height/2),
            # Face droite (depth x height)
            (0, 0), (depth/2, 0), (depth/2, height/2), (0, height/2),
            # Face gauche (depth x height)
            (0, 0), (depth/2, 0), (depth/2, height/2), (0, height/2),
            # Face supérieure (width x depth)
            (0, 0), (width/2, 0), (width/2, depth/2), (0, depth/2),
            # Face inférieure (width x depth)
            (0, 0), (width/2, 0), (width/2, depth/2), (0, depth/2),
        ]

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