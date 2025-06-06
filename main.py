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
        # On place ici tous les sommets en une seule liste
        positions = [
            # Face avant
            (0, 0, 1), (1, 0, 1), (1, 1, 1), (0, 1, 1),
            # Face arrière
            (1, 0, 0), (0, 0, 0), (0, 1, 0), (1, 1, 0),
            # Face droite
            (1, 0, 1), (1, 0, 0), (1, 1, 0), (1, 1, 1),
            # Face gauche
            (0, 0, 0), (0, 0, 1), (0, 1, 1), (0, 1, 0),
            # Face supérieure
            (0, 1, 1), (1, 1, 1), (1, 1, 0), (0, 1, 0),
            # Face inférieure
            (0, 0, 0), (1, 0, 0), (1, 0, 1), (0, 0, 1),
        ]

        normales = [
            (0, 0, 1)] * 4 + [(0, 0, -1)] * 4 + [(1, 0, 0)] * 4 + \
            [(-1, 0, 0)] * 4 + [(0, 1, 0)] * 4 + [(0, -1, 0)] * 4

        couleurs = [
            (1, 0, 0)] * 4 + [(0, 1, 0)] * 4 + [(0, 0, 1)] * 4 + \
            [(1, 1, 0)] * 4 + [(0, 1, 1)] * 4 + [(1, 0, 1)] * 4

        uvs = [(0, 0), (1, 0), (1, 1), (0, 1)] * 6

        # Fusion de tous les attributs pour chaque sommet
        vertices_cube = np.array([
            positions[i] + normales[i] + couleurs[i] + uvs[i]
            for i in range(24)
        ], dtype=np.float32)

        # Indexation des triangles : 2 triangles par face
        indices_cube = np.array([
            0, 1, 2, 0, 2, 3,        # Face avant
            4, 5, 6, 4, 6, 7,        # Face arrière
            8, 9,10, 8,10,11,        # Face droite
        12,13,14,12,14,15,        # Face gauche
        16,17,18,16,18,19,        # Face supérieure
        20,21,22,20,22,23         # Face inférieure
        ], dtype=np.uint32)



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