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
        # Face avant (z = 1), couleur rouge :
        p0 = (0, 0, 0) # Coin inférieur gauche
        p1 = (1, 0, 0) # Coin inférieur droit
        p2 = (1, 1, 0) # Coin supérieur droit
        p3 = (0, 1, 0) # Coin supérieur gauche

        n0 = (0, 0, 1) # Normale pour le plan sur l'axe Z
        n1 = (0, 0, 1) # Normale pour le plan sur l'axe Z
        n2 = (0, 0, 1) # Normale pour le plan sur l'axe Z
        n3 = (0, 0, 1) # Normale pour le plan sur l'axe Z

        c0 = (1, 0, 0) # Rouge
        c1 = (0, 1, 0) # Vert
        c2 = (0, 0, 1) # Bleu
        c3 = (1, 1, 0) # Jaune

        uv0 = (0, 0) # Coordonnées de texture pour le coin inférieur gauche
        uv1 = (1, 0) # Coordonnées de texture pour le coin inférieur droit
        uv2 = (1, 1) # Coordonnées de texture pour le coin supérieur droit
        uv3 = (0, 1) # Coordonnées de texture pour le coin supérieur gauche

        sommets = np.concatenate((p0, n0, c0, uv0, p1, n1, c1, uv1, p2, n2, c2, uv2, p3, n3, c3, uv3))
        
        # Face arrière (z = 0), couleur vert :
        p4 = (1, 0, 0)
        p5 = (0, 0, 0)
        p6 = (0, 1, 0)
        p7 = (1, 1, 0)

        n4 = (0, 0, -1)
        n5 = (0, 0, -1)
        n6 = (0, 0, -1)
        n7 = (0, 0, -1)

        c4 = (0, 1, 0) # Vert
        c5 = (0, 1, 0)
        c6 = (0, 1, 0)
        c7 = (0, 1, 0)

        uv4 = (0, 0)
        uv5 = (1, 0)
        uv6 = (1, 1)
        uv7 = (0, 1)


        # Face droite (x = 1), couleur bleu :
        p8 = (1, 0, 1)
        p9 = (1, 0, 0)
        p10 = (1, 1, 0)
        p11 = (1, 1, 1)

        n8 = (1, 0, 0)
        n9 = (1, 0, 0)
        n10 = (1, 0, 0)
        n11 = (1, 0, 0)

        c8 = (0, 0, 1) # Bleu
        c9 = (0, 0, 1)
        c10 = (0, 0, 1)
        c11 = (0, 0, 1)

        uv8 = (0, 0)
        uv9 = (1, 0)
        uv10 = (1, 1)
        uv11 = (0, 1)



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