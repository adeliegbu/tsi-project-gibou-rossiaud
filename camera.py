import pyrr
import numpy as np

class Camera:
    def __init__(self, target_object):
        self.offset = np.array([0.0, 2.0, 5.0], dtype=np.float32)  # Position relative à l'objet
        self.eye = np.array([0.0, 0.0, 3.0], dtype=np.float32)  # Position initiale de la caméra
        self.target = np.array([0.0, 0.0, 0.0], dtype=np.float32)  # Position cible
        self.up = np.array([0.0, 1.0, 0.0], dtype=np.float32)  # Vecteur "up" de la caméra
        self.target_object = target_object  # Objet suivi (le cube)

    def update(self):
        # Récupérer la position actuelle du cube
        if self.target_object is not None:
            self.target = self.target_object.get_cube_position()
        else:
            self.target = np.array([0.0, 0.0, 0.0], dtype=np.float32)

        # Calculer la position de la caméra en fonction de l'offset
        self.eye = self.target + self.offset

    def create_view_matrix(self):
        # Créer la matrice de vue (look-at)
        return pyrr.matrix44.create_look_at(
            eye=self.eye, target=self.target, up=self.up, dtype=np.float32
        )