import glfw
import numpy as np



class Binds:
    def __init__(self, start, reset):
        self.start = start
        self.reset = reset

    def key_callback(self, win, key, scancode, action, mods):
        # sortie du programme si appui sur la touche 'echap'
        if action == glfw.PRESS:
            if key == glfw.KEY_ESCAPE:
                glfw.set_window_should_close(win, True)

        if action == glfw.PRESS:
            if key == glfw.KEY_SPACE and self.cube.jump_allowed:
                self.cube.position[1] += 0.1
                self.cube.velocity[1] += 5.0
                self.cube.jump_allowed = False

        if action == glfw.PRESS:
            if key == glfw.KEY_R:
                self.reset()

        if action == glfw.PRESS:
            if key == glfw.KEY_ENTER:
                self.start()


    def send_cube(self, cube):
        self.cube = cube

    def send_fruits(self, fruits):
        self.fruits = fruits