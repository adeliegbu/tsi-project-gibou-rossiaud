import glfw
import numpy as np



class Binds:
    def __init__(self):
        pass

    def key_callback(self, win, key, scancode, action, mods):
        # sortie du programme si appui sur la touche 'echap'
        if action == glfw.PRESS:
            if key == glfw.KEY_ESCAPE:
                glfw.set_window_should_close(win, True)
        if action == glfw.PRESS:
            if key == glfw.KEY_SPACE and self.cube.jump_allowed:
                self.cube.position[1] += 5.0
                self.cube.velocity[1] += 5.0
                self.cube.jump_allowed = False

    def send_cube(self, cube):
        self.cube = cube