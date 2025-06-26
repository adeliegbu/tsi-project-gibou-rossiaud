import numpy as np

def generate_sol(size_sol):
    half_size = size_sol / 2.0
    p0 = (-half_size, 0.0, -half_size) # Coin inférieur gauche
    p1 = (half_size, 0.0, -half_size)  # Coin inférieur droit
    p2 = (half_size, 0.0, half_size)   # Coin supérieur droit
    p3 = (-half_size, 0.0, half_size)  # Coin supérieur gauche

    n0 = (0, 1, 0) # Normale pour le plan sur l'axe Z
    n1 = (0, 1, 0) # Normale pour le plan sur l'axe Z
    n2 = (0, 1, 0) # Normale pour le plan sur l'axe Z
    n3 = (0, 1, 0) # Normale pour le plan sur l'axe Z

    c = (1, 1, 1)


    uv0 = (0, 0) # Coordonnées de texture pour le coin inférieur gauche
    uv1 = (size_sol/2, 0) # Coordonnées de texture pour le coin inférieur droit
    uv2 = (size_sol/2, size_sol/2) # Coordonnées de texture pour le coin supérieur droit
    uv3 = (0, size_sol/2) # Coordonnées de texture pour le coin supérieur gauche

    sommets_sol = np.array([
                *p0, *n0, *c, *uv0,
                *p1, *n1, *c, *uv1,
                *p2, *n2, *c, *uv2,
                *p3, *n3, *c, *uv3,
            ], dtype=np.float32)

    f0 = (0, 1, 2) # Triangle inférieur droit
    f1 = (0, 2, 3) # Triangle supérieur gauche
    index_sol = np.array((f0, f1), np.uint32)

    positions_sol = np.array([
        p0, p1, p2, p3
    ], dtype=np.float32)

    return sommets_sol, index_sol, size_sol