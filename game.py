#!/usr/bin/env python3
import OpenGL.GL as GL
import glfw
import numpy as np
import pyrr
from PIL import Image
import ctypes
import os

from object._3d_object import Object_3d 
from binds.binds import Binds
from shader.shader_program import ShaderProgram
from object.sol import generate_sol
from object.cube import generate_cube
from object.sphere import generate_sphere
from object.mur import generate_mur
from collision.collision import Collision
import tools
from camera import Camera

class Game(object):
    """ fenêtre GLFW avec openGL """

    def __init__(self):

        self.binds = Binds(self.start, self.reset)

        self.window = self.init_window()
        self.init_context()
        width, height = glfw.get_window_size(self.window)


        self.shader = ShaderProgram('shader/phong.vert', 'shader/phong.frag')
        self.shader.use()

        self.init_data()

        self.projection_matrix = pyrr.matrix44.create_perspective_projection(
            fovy=50.0, aspect=1.0, near=0.5, far=100.0, dtype=np.float32)
        
        self.camera = Camera(
        position=np.array([0.0, 2.5, 6.0], dtype=np.float32),
        target=np.array([0.0, 0.0, 0.0], dtype=np.float32)
        )
        
        loc_projection = GL.glGetUniformLocation(self.shader.get_id(), "projection")
        if loc_projection != -1:
            GL.glUniformMatrix4fv(loc_projection, 1, GL.GL_FALSE, self.projection_matrix)


        

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
        self.vertices_sol, self.indices_sol, self.size_sol = generate_sol(45.0)

        self.vertices_platform, self.indices_platform = generate_cube(width=10.0, height=0.5, depth=10.0)
        self.vertices_bouton, self.indices_button = generate_cube(width=0.8, height=0.1, depth=0.8)

        # Création des données pour le cube
        self.vertices_cube, self.indices_cube = generate_cube()

        #création de murs selon axe z (verticaux)
        self.vertices_wall_vertical, self.indices_wall_vertical = generate_mur(taille=(1, 7.0, 5.0))
        #création du vao pour le mur
        self.vao_wall_vertical = tools.load_to_gpu(self.vertices_wall_vertical, self.indices_wall_vertical)

        #création de murs selon axe x (horizontaux)
        self.vertices_wall_horizontal, self.indices_wall_horizontal = generate_mur(taille=(5, 7.0, 1.0))
        #création du vao pour le mur
        self.vao_wall_horizontal = tools.load_to_gpu(self.vertices_wall_horizontal, self.indices_wall_horizontal)

        walls_info_vertical = []

        walls_info_horizontal = []

        # Création des données pour la sphère
        sphere_data = generate_sphere(radius=0.65, lat_segments=32, lon_segments=64)
        self.sphere_vertices = sphere_data['interlaced']
        self.sphere_indices = sphere_data['faces'].reshape(-1)

        # Création des VAOs
        self.vao_sol = tools.load_to_gpu(self.vertices_sol, self.indices_sol)
        self.vao_platform = tools.load_to_gpu(self.vertices_platform, self.indices_platform)
        self.vao_bouton = tools.load_to_gpu(self.vertices_bouton, self.indices_button)
        self.vao_cube = tools.load_to_gpu(self.vertices_cube, self.indices_cube)
        self.vao_sphere = tools.load_to_gpu(self.sphere_vertices, self.sphere_indices)


        self.texture_sol = tools.load_texture('texture/grass.jpg')
        self.texture_cube = tools.load_texture('texture/fox.jpg')
        self.texture_bouton = tools.load_texture('texture/stone.jpg')  
        self.texture_watermelon = tools.load_texture('texture/watermelon.jpg')
        self.texture_apple = tools.load_texture('texture/apple.jpg')
        self.texture_orange = tools.load_texture('texture/orange.jpg')
        self.texture_strawberry = tools.load_texture('texture/strawberry.jpg')
        self.texture_lemon = tools.load_texture('texture/lemon.jpg')
        self.texture_platform = tools.load_texture('texture/brick.jpg')
        self.texture_mur = tools.load_texture('texture/wall_texture.png')


        self.sol1 = Object_3d(
            vao=self.vao_sol,
            position=np.array([-27.5, 0.0, -27.5, 1.0], dtype=np.float32),
            angle=np.array([0.0, 0.0, 0.0], dtype=np.float32),
            shader_program=self.shader.get_id(),
            texture=self.texture_sol,
            nb_sommets=len(self.indices_sol)*3,
            taille=np.array([self.size_sol, 0.0, self.size_sol], dtype=np.float32),
            window=self.window
        )

        self.sol2 = Object_3d(
            vao=self.vao_sol,
            position=np.array([27.5, 0.0, 27.5, 1.0], dtype=np.float32),
            angle=np.array([0.0, 0.0, 0.0], dtype=np.float32),
            shader_program=self.shader.get_id(),
            texture=self.texture_sol,
            nb_sommets=len(self.indices_sol)*3,
            taille=np.array([self.size_sol, 0.0, self.size_sol], dtype=np.float32),
            window=self.window
        )

        self.sol3 = Object_3d(
            vao=self.vao_sol,
            position=np.array([-27.5, 0.0, 27.5, 1.0], dtype=np.float32),
            angle=np.array([0.0, 0.0, 0.0], dtype=np.float32),
            shader_program=self.shader.get_id(),
            texture=self.texture_sol,
            nb_sommets=len(self.indices_sol)*3,
            taille=np.array([self.size_sol, 0.0, self.size_sol], dtype=np.float32),
            window=self.window
        )

        self.sol4 = Object_3d(
            vao=self.vao_sol,
            position=np.array([27.5, 0.0, -27.5, 1.0], dtype=np.float32),
            angle=np.array([0.0, 0.0, 0.0], dtype=np.float32),
            shader_program=self.shader.get_id(),
            texture=self.texture_sol,
            nb_sommets=len(self.indices_sol)*3,
            taille=np.array([self.size_sol, 0.0, self.size_sol], dtype=np.float32),
            window=self.window
        )

        self.cube = Object_3d(
            vao=self.vao_cube,
            position=np.array([0.0, 3.0, 3.0, 1.0], dtype=np.float32),
            angle=np.array([0.0, np.pi, 0.0], dtype=np.float32),
            shader_program=self.shader.get_id(),
            texture=self.texture_cube,
            nb_sommets=len(self.indices_cube)*3,
            taille=np.array([1.0, 1.0, 1.0], dtype=np.float32),
            window=self.window

        )

        self.binds.send_cube(self.cube)

        self.watermelon = Object_3d(
            vao=self.vao_sphere,
            position=np.array([4.0, 2.0, -4.0, 1.0], dtype=np.float32),
            angle=np.array([0.0, 0.0, 0.0], dtype=np.float32),
            shader_program=self.shader.get_id(),
            texture=self.texture_watermelon,
            nb_sommets=len(self.sphere_indices)*3,
            taille=np.array([0.65, 0.65, 0.65], dtype=np.float32),
            window=self.window,
            radius=0.5
        )

        self.apple = Object_3d(
            vao=self.vao_sphere,
            position=np.array([2.0, 2.0, -4.0, 1.0], dtype=np.float32),
            angle=np.array([0.0, 0.0, 0.0], dtype=np.float32),
            shader_program=self.shader.get_id(),
            texture=self.texture_apple,
            nb_sommets=len(self.sphere_indices)*3,
            taille=np.array([0.65, 0.65, 0.65], dtype=np.float32),
            window=self.window,
            radius=0.5
        )

        self.orange = Object_3d(
            vao=self.vao_sphere,
            position=np.array([0.0, 2.0, -4.0, 1.0], dtype=np.float32),
            angle=np.array([0.0, 0.0, 0.0], dtype=np.float32),
            shader_program=self.shader.get_id(),
            texture=self.texture_orange,
            nb_sommets=len(self.sphere_indices)*3,
            taille=np.array([0.65, 0.65, 0.65], dtype=np.float32),
            window=self.window,
            radius=0.5
        )

        self.strawberry = Object_3d(
            vao=self.vao_sphere,
            position=np.array([-2.0, 2.0, -4.0, 1.0], dtype=np.float32),
            angle=np.array([0.0, 0.0, 0.0], dtype=np.float32),
            shader_program=self.shader.get_id(),
            texture=self.texture_strawberry,
            nb_sommets=len(self.sphere_indices)*3,
            taille=np.array([0.65, 0.65, 0.65], dtype=np.float32),
            window=self.window,
            radius=0.5
        )

        self.lemon = Object_3d(
            vao=self.vao_sphere,
            position=np.array([-4.0, 2.0, -4.0, 1.0], dtype=np.float32),
            angle=np.array([0.0, 0.0, 0.0], dtype=np.float32),
            shader_program=self.shader.get_id(),
            texture=self.texture_lemon,
            nb_sommets=len(self.sphere_indices)*3,
            taille=np.array([0.65, 0.65, 0.65], dtype=np.float32),
            window=self.window,
            radius=0.5
        )

        self.platform = Object_3d(
            vao=self.vao_platform,
            position=np.array([0.0, 1.0, 0.0, 1.0], dtype=np.float32),
            angle=np.array([0.0, 0.0, 0.0], dtype=np.float32),
            shader_program=self.shader.get_id(),
            texture=self.texture_platform,
            nb_sommets=len(self.indices_platform)*3,
            taille=np.array([10.0, 0.5, 10.0], dtype=np.float32),
            window=self.window
        )

        self.button = Object_3d(
            vao=self.vao_bouton,
            position=np.array([0.0, 1.30, 0.0, 1.0], dtype=np.float32),
            angle=np.array([0.0, 0.0, 0.0], dtype=np.float32),
            shader_program=self.shader.get_id(),
            texture=self.texture_bouton,
            nb_sommets=len(self.indices_button)*3,
            taille=np.array([0.5, 0.2, 0.5], dtype=np.float32),
            window=self.window
        )

        self.walls = []
        for wall_info in walls_info_vertical:
            wall = Object_3d(
                vao=self.vao_wall_vertical,
                position = np.array(wall_info["position"] + [1.0], dtype=np.float32),
                angle=np.array([0.0, 0.0, 0.0], dtype=np.float32),
                shader_program=self.shader.get_id(),
                texture=self.texture_mur,
                nb_sommets=len(self.indices_wall_vertical)*3,
                taille=np.array([1,4,5], dtype=np.float32),
                window=self.window
                )
            self.walls.append(wall)

        for wall_info in walls_info_horizontal:
            wall = Object_3d(
                vao=self.vao_wall_horizontal,
                position = np.array(wall_info["position"] + [1.0], dtype=np.float32),
                angle=np.array([0.0, 0.0, 0.0], dtype=np.float32),
                shader_program=self.shader.get_id(),
                texture=self.texture_mur,
                nb_sommets=len(self.indices_wall_horizontal)*3,
                taille=np.array([5,4,1], dtype=np.float32),
                window=self.window
                )
            self.walls.append(wall)
        self.collision = Collision()
        self.started = False
        self.move_timer = 0.0
        self.sols = [self.sol1, self.sol2, self.sol3, self.sol4, self.platform]

    def start(self):
        """ Démarre le jeu """
        if not self.started:
            self.started = True
            self.respawn_cube()
            self.random_place_fruits()
            self.random_place_walls()  
            self.timer = glfw.get_time()
    
    def reset(self):
        """ Réinitialise le jeu """
        if self.started:
            self.started = False
            self.respawn_cube()
            for fruit in self.fruits:
                fruit.picked = False
                fruit.position = fruit.base_position.copy()
            for wall in self.walls:
                wall.position[1] = 100.0
        
    def random_place_fruits(self):
        """ Place les fruits à des positions aléatoires dans la scène """
        self.fruits = [self.watermelon, self.apple, self.orange, self.strawberry, self.lemon]
        self.binds.send_fruits(self.fruits)
        for fruit in self.fruits:
            if np.random.choice([True, False]):

                x = np.random.choice([
                    np.random.uniform(-50.0, -5.0),
                    np.random.uniform(5.0, 50.0)
                ])
                z = np.random.uniform(-50, 50) 
            else:
                x = np.random.uniform(-50, 50) 
                z = np.random.choice([
                    np.random.uniform(-50.0, -5.0),
                    np.random.uniform(5.0, 50.0)
                ])
            
            y = np.random.uniform(1.5, 2.5)  # Hauteur aléatoire pour les fruits
            fruit.position = np.array([x, y, z, 1.0], dtype=np.float32)

    def is_position_valid(self, x, z, fruits, exclusion_radius):
        if -5<= x <= 5 and -5 <= z <= 5:
            return False
        for fruit in fruits:
            fruit_x, fruit_z = fruit.position[0], fruit.position[2]
            dist = np.sqrt((x - fruit_x)**2 + (z - fruit_z)**2)
            if dist < exclusion_radius:
                return False
        return True


    def random_place_walls(self):
        """Place les murs à des positions aléatoires dans la scène"""
        self.walls = []

        num_walls = 70

        for _ in range(num_walls):
            if np.random.choice([True, False]):
                vao = self.vao_wall_vertical
                taille = np.array([1, 7, 5], dtype=np.float32)
            else:
                vao = self.vao_wall_horizontal
                taille = np.array([5, 7, 1], dtype=np.float32)
            while True:
                x = np.random.uniform(-45, 45)
                z = np.random.uniform(-45, 45)
                if self.is_position_valid(x, z, self.fruits, exclusion_radius=1.0):
                    break            
            y = 3.5  # Hauteur fixe pour les murs

            wall = Object_3d(
                vao=vao,
                position=np.array([x, y, z, 1.0], dtype=np.float32),
                angle=np.array([0.0, 0.0, 0.0], dtype=np.float32),
                shader_program=self.shader.get_id(),
                texture=self.texture_mur,
                nb_sommets=len(self.indices_wall_vertical)*3 if vao == self.vao_wall_vertical else len(self.indices_wall_horizontal)*3,
                taille=taille,
                window=self.window
            )

            self.walls.append(wall)

        
    def check_win(self):
        """ Vérifie si le joueur a ramassé tous les fruits et est revenu à la base """
        if self.started:
                for fruit in self.fruits:
                    if self.collision.check_collision_cc(self.cube, fruit):
                        if not fruit.picked:
                            fruit.picked = True
                            fruit.position = fruit.base_position.copy()
                            if sum(not f.picked for f in self.fruits) == 0:
                                print("Tous les fruits ont été ramassés il faut maintenant revenir à la base !")
                            else:
                                print(f"Il ne reste plus que {sum(not f.picked for f in self.fruits)} fruits à ramasser !")
                    if sum(not f.picked for f in self.fruits) == 0:
                        if self.collision.check_collision_cc(self.cube, self.button):
                            print(f"Tous les fruits ont été ramassés en {glfw.get_time() - self.timer:.2f} secondes !")
                            self.respawn_cube()
                            self.started = False
        
    def respawn_cube(self):
        """Remet le cube à sa position de départ"""
        self.cube.position = self.cube.base_position.copy()
        self.cube.angle = np.array([0.0, np.pi, 0.0], dtype=np.float32)
        self.cube.velocity = np.array([0.0, 0.0, 0.0, 1.0], dtype=np.float32)
        self.cube.move_allowed = False
        self.move_timer = glfw.get_time()  
        self.cube.jump_allowed = False


    def run(self):

        frames = 0
        previous_time = glfw.get_time()
        # boucle d'affichage
        while not glfw.window_should_close(self.window):
            frames += 1
            current_time = glfw.get_time()
            dt = current_time - previous_time
            previous_time = current_time


            # choix de la couleur de fond
            GL.glClearColor(0.5, 0.6, 0.9, 1.0)
            # nettoyage de la fenêtre : fond et profondeur
            GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

            pos3 = np.array(self.cube.position[:3], dtype=np.float32)
            dir3 = np.array(self.cube.dir[:3], dtype=np.float32)
            self.camera.update(pos3, dir3, self.walls, self.collision)

            """            view = pyrr.matrix44.create_look_at(
                eye=camera_pos,
                target=pos3,
                up=np.array([0.0, 1.0, 0.0], dtype=np.float32),
                dtype=np.float32
            )"""

            GL.glUseProgram(self.shader.get_id())
            loc_view = GL.glGetUniformLocation(self.shader.get_id(), "view")
            GL.glUniformMatrix4fv(loc_view, 1, GL.GL_FALSE, self.camera.view_matrix)

            if glfw.get_time() - self.move_timer > 0.5:
                self.cube.move_allowed = True
            
            self.cube.move_object(dt, speed=10.0, rotation_speed=2.0)
            self.watermelon.fruit_animation(dt)
            self.apple.fruit_animation(dt)
            self.orange.fruit_animation(dt)
            self.strawberry.fruit_animation(dt)
            self.lemon.fruit_animation(dt)

            for sol in self.sols:
                if self.collision.check_collision_cc(self.cube, sol):
                    self.cube.jump_allowed = True
                    self.collision.resolve_collision_cc(self.cube, sol)

            for wall in self.walls:
                if self.collision.check_collision_cc(self.cube, wall):
                    self.collision.resolve_collision_cc(self.cube, wall)

            if self.cube.position[1] < -8.0:
                self.respawn_cube()

            self.check_win()



            for sol in self.sols:
                sol.show_object()

            self.cube.show_object()
            self.watermelon.show_object()
            self.apple.show_object()
            self.orange.show_object()
            self.strawberry.show_object()
            self.lemon.show_object()
            self.button.show_object()

            for wall in self.walls:
                wall.show_object()


            # changement de buffer d'affichage pour éviter un effet de scintillement
            glfw.swap_buffers(self.window)
            # gestion des évènements
            glfw.poll_events()


            #print(self.cube.jump_allowed)
            # print(self.cube.velocity[1], self.cube.position[1])

        glfw.terminate()

                
    def create_program_from_file(self, vs_file, fs_file):
        # creation d'un programme GPU à partir de fichiers
        vs_content = open(vs_file, 'r').read() if os.path.exists(vs_file)\
            else print(f'{25*"-"}\nError reading file:\n{vs_file}\n{25*"-"}')
        fs_content = open(fs_file, 'r').read() if os.path.exists(fs_file)\
            else print(f'{25*"-"}\nError reading file:\n{fs_file}\n{25*"-"}')
        return self.create_program(vs_content, fs_content)
