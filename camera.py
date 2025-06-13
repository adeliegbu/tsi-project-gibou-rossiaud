import pyrr
import numpy as np

class Camera:
    def __init__(self):
        self.eye = np.array([0.0, 0.0, 3.0], dtype=np.float32)
        self.target = np.array([0.0, 0.0, 0.0], dtype=np.float32)
        self.up = np.array([0.0, 1.0, 0.0], dtype=np.float32)
    
    def create_view_matrix(self):
        return pyrr.matrix44.create_look_at(self.eye, self.target, self.up, dtype=None)