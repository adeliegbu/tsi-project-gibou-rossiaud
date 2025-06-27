import pyrr
import numpy as np


class Camera:
    def __init__(self, position, target, up=np.array([0.0, 1.0, 0.0])):
        self.position = np.array(position, dtype=np.float32)
        self.target = np.array(target, dtype=np.float32)
        self.up = np.array(up, dtype=np.float32)
        self.view_matrix = pyrr.matrix44.create_look_at(self.position, self.target, self.up)

    def update(self, cube_position, cube_direction, walls, collision):
        desired_position = cube_position - cube_direction * 6.0 + np.array([0.0, 2.5, 0.0], dtype=np.float32)

        for wall in walls:
            if self.is_colliding(desired_position, wall, collision):
                desired_position = self.resolve_collision(desired_position, cube_position, cube_direction)

        self.position = desired_position
        self.view_matrix = pyrr.matrix44.create_look_at(self.position, cube_position, self.up)

    def is_colliding(self, camera_pos, wall, collision):
        class Object_temp:
            def __init__(self, position, taille):
                self.position = position
                self.taille = taille

        camera_obj = Object_temp(camera_pos, np.array([0.5, 0.5, 0.5], dtype=np.float32))
        return collision.check_collision_cc(camera_obj, wall)

    def resolve_collision(self, desired_position, cube_position, cube_direction):
        direction_to_cube = cube_position - desired_position
        distance_to_cube = np.linalg.norm(direction_to_cube)
        normalized_direction = direction_to_cube / distance_to_cube

        return cube_position - normalized_direction * 3.0 + np.array([0.0, 2.5, 0.0], dtype=np.float32)
