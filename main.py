#!/usr/bin/env python3
import OpenGL.GL as GL
import glfw
import numpy as np
import time
import os 
import pyrr
from PIL import Image
import ctypes
class Game(object):
    """ fenêtre GLFW avec openGL """

    def __init__(self):
        self.window = self.init_window()
        self.init_context()
        self.init_programs()
        self.init_data()

        #faie bouger le cube
        self.translation_matrix = pyrr.matrix44.create_identity(dtype=np.float32)
        self.rotation_matrix = pyrr.matrix44.create_identity(dtype=np.float32)
        self.projection_matrix = pyrr.matrix44.create_perspective_projection(
            fovy=50.0, aspect=1.0, near=0.5, far=10.0, dtype=np.float32)
        
        #assure une bonne fluidité dans les mouvements
        t_init = pyrr.matrix44.create_from_translation([0.0, 0.0, -3.0], dtype=np.float32)
        self.translation_matrix = pyrr.matrix44.multiply(t_init, self.translation_matrix)
        self.translation_velocity = np.array([0.0, 0.0, 0.0], dtype=np.float32)
        self.rotation_velocity = np.array([0.0, 0.0], dtype=np.float32)  # [x, y]


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
        self.program = self.create_program_from_file('phong.vert', 'phong.frag')
        GL.glUseProgram(self.program)

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
        self.vao = GL.glGenVertexArrays(1)
        GL.glBindVertexArray(self.vao)

        self.vbo = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.vbo)
        GL.glBufferData(GL.GL_ARRAY_BUFFER, self.vertices_cube.nbytes, self.vertices_cube, GL.GL_STATIC_DRAW)

        self.ebo = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, self.ebo)
        GL.glBufferData(GL.GL_ELEMENT_ARRAY_BUFFER, self.indices.nbytes, self.indices, GL.GL_STATIC_DRAW)

        stride = 11 * 4  # 11 floats * 4 bytes

        # position (location = 0)
        GL.glEnableVertexAttribArray(0)
        GL.glVertexAttribPointer(0, 3, GL.GL_FLOAT, GL.GL_FALSE, stride, ctypes.c_void_p(0))

        # normale (location = 1)
        GL.glEnableVertexAttribArray(1)
        GL.glVertexAttribPointer(1, 3, GL.GL_FLOAT, GL.GL_FALSE, stride, ctypes.c_void_p(3 * 4))

        # couleur (location = 2)
        GL.glEnableVertexAttribArray(2)
        GL.glVertexAttribPointer(2, 3, GL.GL_FLOAT, GL.GL_FALSE, stride, ctypes.c_void_p(6 * 4))

        # texture UV (location = 3)
        GL.glEnableVertexAttribArray(3)
        GL.glVertexAttribPointer(3, 2, GL.GL_FLOAT, GL.GL_FALSE, stride, ctypes.c_void_p(9 * 4))


    def generate_sphere(radius=1.0, lat_segments=16, lon_segments=32):
        vertices = []
        indices = []
        for i in range(lat_segments + 1):
            theta = np.pi * i / lat_segments
            sin_theta = np.sin(theta)
            cos_theta = np.cos(theta)
            for j in range(lon_segments + 1):
                phi = 2 * np.pi * j / lon_segments
                sin_phi = np.sin(phi)
                cos_phi = np.cos(phi)
                # Position (x, y, z)
                x = radius * sin_theta * cos_phi
                y = radius * cos_theta
                z = radius * sin_theta * sin_phi
                # Normale (norm´ee car sph`ere unitaire)
                nx = sin_theta * cos_phi
                ny = cos_theta
                nz = sin_theta * sin_phi
                # Texture coordinates (u, v)
                u = j / lon_segments
                v = i / lat_segments
                r, g, b = 1.0, 1.0, 1.0
                # Interlaced vertex: position, normal, color, uv
                vertex = [x, y, z, nx, ny, nz, r, g, b, u, v]
                vertices.append(vertex)
        # Faces
        for i in range(lat_segments):
            for j in range(lon_segments):
                a = i * (lon_segments + 1) + j
                b = a + lon_segments + 1
                indices.append((a, b, a + 1))
                indices.append((a + 1, b, b + 1))
        return {
        'interlaced': np.array(vertices, dtype=np.float32), # [pos, norm, color]
        'faces': np.array(indices, dtype=np.int32) # (i0, i1, i2)
        }


    def run(self):

        start = time.time()
        frames = 0
        previous_time = time.time()
        # boucle d'affichage
        while not glfw.window_should_close(self.window):
            # choix de la couleur de fond
            GL.glClearColor(0.5, 0.6, 0.9, 1.0)
            # nettoyage de la fenêtre : fond et profondeur
            GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

            # Envoi des matrices uniforms
            loc_translation = GL.glGetUniformLocation(self.program, "translation")
            if loc_translation != -1:
                GL.glUniformMatrix4fv(loc_translation, 1, GL.GL_FALSE, self.translation_matrix)

            loc_rotation = GL.glGetUniformLocation(self.program, "rotation")
            if loc_rotation != -1:
                GL.glUniformMatrix4fv(loc_rotation, 1, GL.GL_FALSE, self.rotation_matrix)

            loc_projection = GL.glGetUniformLocation(self.program, "projection")
            if loc_projection != -1:
                GL.glUniformMatrix4fv(loc_projection, 1, GL.GL_FALSE, self.projection_matrix)


            # changement de buffer d'affichage pour éviter un effet de scintillement
            glfw.swap_buffers(self.window)
            # gestion des évènements
            glfw.poll_events()

            frames += 1
            current_time = time.time()
            dt = current_time - previous_time
            previous_time = current_time

            # Appliquer la translation
            if np.linalg.norm(self.translation_velocity) > 0:
                t = pyrr.matrix44.create_from_translation(self.translation_velocity * dt, dtype=np.float32)
                self.translation_matrix = pyrr.matrix44.multiply(t, self.translation_matrix)

            # Appliquer la rotation
            rx, ry = self.rotation_velocity
            if rx != 0:
                r = pyrr.matrix44.create_from_x_rotation(rx * dt, dtype=np.float32)
                self.rotation_matrix = pyrr.matrix44.multiply(r, self.rotation_matrix)
            if ry != 0:
                r = pyrr.matrix44.create_from_y_rotation(ry * dt, dtype=np.float32)
                self.rotation_matrix = pyrr.matrix44.multiply(r, self.rotation_matrix)
            
        glfw.terminate()
                
    
    def key_callback(self, win, key, scancode, action, mods):
        # sortie du programme si appui sur la touche 'echap'
        if action == glfw.PRESS:
            if key == glfw.KEY_ESCAPE:
                glfw.set_window_should_close(win, True)
            elif key == glfw.KEY_W:
                self.translation_velocity[2] = -1.0
            elif key == glfw.KEY_S:
                self.translation_velocity[2] = 1.0
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

        elif action == glfw.RELEASE:
            if key in (glfw.KEY_W, glfw.KEY_S):
                self.translation_velocity[2] = 0.0
            elif key in (glfw.KEY_A, glfw.KEY_D):
                self.translation_velocity[0] = 0.0
            elif key in (glfw.KEY_UP, glfw.KEY_DOWN):
                self.rotation_velocity[0] = 0.0
            elif key in (glfw.KEY_LEFT, glfw.KEY_RIGHT):
                self.rotation_velocity[1] = 0.0

    def compile_shader(self, shader_content, shader_type):
        # compilation d'un shader donne selon son type ´
        shader_id = GL.glCreateShader(shader_type)
        GL.glShaderSource(shader_id, shader_content)
        GL.glCompileShader(shader_id)
        success = GL.glGetShaderiv(shader_id, GL.GL_COMPILE_STATUS)
        if not success:
            log = GL.glGetShaderInfoLog(shader_id).decode('ascii')
            print(f'{25*"-"}\nError compiling shader: \n\
                {shader_content}\n{5*"-"}\n{log}\n{25*"-"}')
        return shader_id
        
    def create_program(self, vertex_source, fragment_source):
        # creation d'un programme GPU ´
        vs_id = self.compile_shader(vertex_source, GL.GL_VERTEX_SHADER)
        fs_id = self.compile_shader(fragment_source, GL.GL_FRAGMENT_SHADER)
        if vs_id and fs_id:
            program_id = GL.glCreateProgram()
            GL.glAttachShader(program_id, vs_id)
            GL.glAttachShader(program_id, fs_id)
            GL.glLinkProgram(program_id)
            success = GL.glGetProgramiv(program_id, GL.GL_LINK_STATUS)
            if not success:
                log = GL.glGetProgramInfoLog(program_id).decode('ascii')
                print(f'{25*"-"}\nError linking program:\n{log}\n{25*"-"}')
            GL.glDeleteShader(vs_id)
            GL.glDeleteShader(fs_id)
        return program_id

    def create_program_from_file(self, vs_file, fs_file):
        # creation d'un programme GPU à partir de fichiers
        vs_content = open(vs_file, 'r').read() if os.path.exists(vs_file)\
            else print(f'{25*"-"}\nError reading file:\n{vs_file}\n{25*"-"}')
        fs_content = open(fs_file, 'r').read() if os.path.exists(fs_file)\
            else print(f'{25*"-"}\nError reading file:\n{fs_file}\n{25*"-"}')
        return self.create_program(vs_content, fs_content)



def main():
    g = Game()
    g.run()
    glfw.terminate()

if __name__ == '__main__':
    main()