#!/usr/bin/env python3
import OpenGL.GL as GL
import glfw
import numpy as np
import time
import os 
import pyrr
from PIL import Image
import ctypes

from object._3d_object import Object_3d 
from binds.binds import Binds
from shader.shader_program import ShaderProgram
from camera import Camera
from object.sol import generate_sol
from object.cube import generate_cube
from object.sphere import generate_sphere
from collision.collision import Collision
import tools
class Game(object):
    """ fenêtre GLFW avec openGL """

    def __init__(self):

        self.binds = Binds()

        self.window = self.init_window()
        self.init_context()
        width, height = glfw.get_window_size(self.window)


        self.shader = ShaderProgram('shader/phong.vert', 'shader/phong.frag')
        self.shader.use()

        self.init_data()

        #faire bouger le cube
        self.projection_matrix = pyrr.matrix44.create_perspective_projection(
            fovy=50.0, aspect=1.0, near=0.5, far=100.0, dtype=np.float32)
        

    def init_window(self):
        # initialisation de la librairie glfw et du context opengl associé
        glfw.init()
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL.GL_TRUE)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
        # création et parametrage de la fenêtre
        glfw.window_hint(glfw.RESIZABLE, True)
        window = glfw.create_window(1920, 1080, 'OpenGL', None, None)  # Augmenté à 1920x1080
        # parametrage de la fonction de gestion des évènements
        glfw.set_key_callback(window, self.binds.key_callback)
        return window
    
        
    def init_context(self):
        # activation du context OpenGL pour la fenêtre
        glfw.make_context_current(self.window)
        glfw.swap_interval(1)
        # activation de la gestion de la profondeur
        GL.glEnable(GL.GL_DEPTH_TEST)


    def init_data(self):
        self.vertices_sol, self.indices_sol, self.size_sol = generate_sol(100.0)

        # Création des données pour le cube
        self.vertices_cube, self.indices_cube = generate_cube()

        sphere_data = generate_sphere(radius=1.0, lat_segments=32, lon_segments=64)
        self.sphere_vertices = sphere_data['interlaced']
        self.sphere_indices = sphere_data['faces'].reshape(-1)

        # Création du VAO pour le sol   
        self.vao_sol = tools.load_to_gpu(self.vertices_sol, self.indices_sol)
        # Création du VAO pour le cube
        self.vao_cube = tools.load_to_gpu(self.vertices_cube, self.indices_cube)
        # Création du VAO pour la sphère
        self.vao_sphere = tools.load_to_gpu(self.sphere_vertices, self.sphere_indices)

        self.texture_sol = tools.load_texture('texture/grass.png')
        self.texture_cube = tools.load_texture('texture/cube_texture.png')
        self.texture_sphere = tools.load_texture('texture/sphere_texture.png')

        self.sol = Object_3d(
            vao=self.vao_sol,
            position=np.array([0.0, -0.05, 0.0, 1.0], dtype=np.float32),
            angle=np.array([0.0, 0.0, 0.0], dtype=np.float32),
            shader_program=self.shader.get_id(),
            texture=self.texture_sol,
            nb_sommets=len(self.indices_sol)*3,
            taille=np.array([self.size_sol, 0.0, self.size_sol], dtype=np.float32),
            window=self.window
        )

        self.cube = Object_3d(
            vao=self.vao_cube,
            position=np.array([5.0,80.0, 5.0, 1.0], dtype=np.float32),
            angle=np.array([0.0, 0.0, 0.0], dtype=np.float32),
            shader_program=self.shader.get_id(),
            texture=self.texture_cube,
            nb_sommets=len(self.indices_cube)*3,
            taille=np.array([1.0, 1.0, 1.0], dtype=np.float32),
            window=self.window
        )

        self.binds.send_cube(self.cube)

        self.sphere = Object_3d(
            vao=self.vao_sphere,
            position=np.array([10.0, 0.5, 5.0, 1.0], dtype=np.float32),
            angle=np.array([0.0, 0.0, 0.0], dtype=np.float32),
            shader_program=self.shader.get_id(),
            texture=self.texture_sphere,
            nb_sommets=len(self.sphere_indices)*3,
            taille=np.array([1.0, 2.0, 1.0], dtype=np.float32),
            window=self.window,
            radius=1.0
        )

        self.collision = Collision()

    def run(self):

        frames = 0
        previous_time = time.time()
        # boucle d'affichage
        while not glfw.window_should_close(self.window):
            frames += 1
            current_time = time.time()
            dt = current_time - previous_time
            previous_time = current_time


            # choix de la couleur de fond
            GL.glClearColor(0.5, 0.6, 0.9, 1.0)
            # nettoyage de la fenêtre : fond et profondeur
            GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)


            loc_projection = GL.glGetUniformLocation(self.shader.get_id(), "projection")
            if loc_projection != -1:
                GL.glUniformMatrix4fv(loc_projection, 1, GL.GL_FALSE, self.projection_matrix)

            pos3 = np.array(self.cube.position[:3], dtype=np.float32)
            dir3 = np.array(self.cube.dir[:3], dtype=np.float32)
            camera_pos = pos3 - dir3 * 5.0 + np.array([0.0, 2.0, 0.0], dtype=np.float32)

            view = pyrr.matrix44.create_look_at(
                eye=camera_pos,
                target=pos3,
                up=np.array([0.0, 1.0, 0.0], dtype=np.float32),
                dtype=np.float32
            )

            GL.glUseProgram(self.shader.get_id())
            loc_view = GL.glGetUniformLocation(self.shader.get_id(), "view")
            GL.glUniformMatrix4fv(loc_view, 1, GL.GL_FALSE, view)

            # if self.collision.find_collision_cc(self.cube, self.sol) == 1:
            #     self.cube.jump(jump_speed=5.0)

            self.collision.resolve_collision_cc(self.cube, self.sol)
            # self.collision.resolve_collision_cs_cube_to_stop(self.cube, self.sphere)

            self.cube.move_object(dt, speed=5.0, rotation_speed=2.0)

            self.sol.show_object()
            self.cube.show_object()
            self.sphere.show_object()

            # changement de buffer d'affichage pour éviter un effet de scintillement
            glfw.swap_buffers(self.window)
            # gestion des évènements
            glfw.poll_events()


            print(self.cube.jump_allowed)
            # print(self.cube.velocity[1], self.cube.position[1])

        glfw.terminate()

                
    def create_program_from_file(self, vs_file, fs_file):
        # creation d'un programme GPU à partir de fichiers
        vs_content = open(vs_file, 'r').read() if os.path.exists(vs_file)\
            else print(f'{25*"-"}\nError reading file:\n{vs_file}\n{25*"-"}')
        fs_content = open(fs_file, 'r').read() if os.path.exists(fs_file)\
            else print(f'{25*"-"}\nError reading file:\n{fs_file}\n{25*"-"}')
        return self.create_program(vs_content, fs_content)

