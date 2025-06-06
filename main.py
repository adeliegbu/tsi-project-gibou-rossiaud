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
        p0 = (0, 0, 0) # Coin inf´erieur gauche
        p1 = (1, 0, 0) # Coin inf´erieur droit
        p2 = (1, 1, 0) # Coin sup´erieur droit
        p3 = (0, 1, 0) # Coin sup´erieur gauche

        n0 = (0, 0, 1) # Normale pour le plan sur l'axe Z
        n1 = (0, 0, 1) # Normale pour le plan sur l'axe Z
        n2 = (0, 0, 1) # Normale pour le plan sur l'axe Z
        n3 = (0, 0, 1) # Normale pour le plan sur l'axe Z

        c0 = (1, 0, 0) # Rouge
        c1 = (0, 1, 0) # Vert
        c2 = (0, 0, 1) # Bleu
        c3 = (1, 1, 0) # Jaune

        uv0 = (0, 0) # Coordonn´ees de texture pour le coin inf´erieur gauche
        uv1 = (1, 0) # Coordonn´ees de texture pour le coin inf´erieur droit
        uv2 = (1, 1) # Coordonn´ees de texture pour le coin sup´erieur droit
        uv3 = (0, 1) # Coordonn´ees de texture pour le coin sup´erieur gauche

        sommets = np.concatenate((p0, n0, c0, uv0, p1, n1, c1, uv1, p2, n2, c2, uv2, p3, n3, c3, uv3))
        


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