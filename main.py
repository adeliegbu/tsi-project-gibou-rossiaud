#!/usr/bin/env python3

import OpenGL.GL as GL
import glfw
import numpy as np

class Game(object):
    """ fenêtre GLFW avec openGL """

    def __init__(self):
        self.window = self.init_window()
        self.init_context()
        self.init_programs()
        self.init_data()


    def init_window(self):
        # initialisation de la librairie glfw et du context opengl associé
        glfw.init()
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL.GL_TRUE)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
        # création et parametrage de la fenêtre
        glfw.window_hint(glfw.RESIZABLE, False)
        window = glfw.create_window(800, 800, 'OpenGL', None, None)
        # parametrage de la fonction de gestion des évènements
        glfw.set_key_callback(window, self.key_callback)
        return window

    def init_context(self):
        # activation du context OpenGL pour la fenêtre
        glfw.make_context_current(self.window)
        glfw.swap_interval(1)
        # activation de la gestion de la profondeur
        GL.glEnable(GL.GL_DEPTH_TEST)

    def init_programs(self):
        pass
        
    def init_data(self):
        pass

    def run(self):
        # boucle d'affichage
        while not glfw.window_should_close(self.window):
            # choix de la couleur de fond
            GL.glClearColor(0.5, 0.6, 0.9, 1.0)
            # nettoyage de la fenêtre : fond et profondeur
            GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
            # changement de buffer d'affichage pour éviter un effet de scintillement
            glfw.swap_buffers(self.window)
            # gestion des évènements
            glfw.poll_events()
    
    def key_callback(self, win, key, scancode, action, mods):
        # sortie du programme si appui sur la touche 'echap'
        if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
            glfw.set_window_should_close(win, glfw.TRUE)

def main():
    g = Game()
    g.run()
    glfw.terminate()

if __name__ == '__main__':
    main()