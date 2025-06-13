import glfw
import numpy as np

class Binds:
    def __init__(self, translation_velocity, rotation_velocity):
        self.translation_velocity = translation_velocity
        self.rotation_velocity = rotation_velocity

    def key_callback(self, win, key, scancode, action, mods):
        # sortie du programme si appui sur la touche 'echap'
        if action == glfw.PRESS:
            if key == glfw.KEY_ESCAPE:
                glfw.set_window_should_close(win, True)
            elif key == glfw.KEY_W:
                self.translation_velocity[1] = 1.0
            elif key == glfw.KEY_S:
                self.translation_velocity[1] = -1.0
            elif key == glfw.KEY_A:
                self.translation_velocity[0] = -1.0
            elif key == glfw.KEY_D:
                self.translation_velocity[0] = 1.0
            elif key == glfw.KEY_UP:
                self.rotation_velocity[0] = 1.0
            elif key == glfw.KEY_DOWN:
                self.rotation_velocity[0] = -1.0
            elif key == glfw.KEY_LEFT:
                self.rotation_velocity[1] = 1.0
            elif key == glfw.KEY_RIGHT:
                self.rotation_velocity[1] = -1.0
            elif key == glfw.KEY_E:
                self.translation_velocity[2] = 1.0
            elif key == glfw.KEY_R:
                self.translation_velocity[2] = -1.0

        elif action == glfw.RELEASE:
            if key in (glfw.KEY_W, glfw.KEY_S):
                self.translation_velocity[1] = 0.0
            elif key in (glfw.KEY_A, glfw.KEY_D):
                self.translation_velocity[0] = 0.0
            elif key in (glfw.KEY_UP, glfw.KEY_DOWN):
                self.rotation_velocity[0] = 0.0
            elif key in (glfw.KEY_LEFT, glfw.KEY_RIGHT):
                self.rotation_velocity[1] = 0.0
            if key in (glfw.KEY_E, glfw.KEY_R):
                self.translation_velocity[2] = 0.0


