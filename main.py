from game import Game
import glfw
import numpy as np
import time
import os 
import pyrr
from PIL import Image
import ctypes

from object._3d_object import Object 
from binds.binds import Binds

class Game(object):
    """ fenêtre GLFW avec openGL """

    def __init__(self):
        self.translation_velocity = np.array([0.0, 0.0, 0.0], dtype=np.float32)
        self.rotation_velocity = np.array([0.0, 0.0], dtype=np.float32)

        self.binds = Binds(self.translation_velocity, self.rotation_velocity)
        
        self.window = self.init_window()
        self.init_context()
        self.init_programs()
        self.init_data()

        #faire bouger le cube
        self.model_matrix = pyrr.matrix44.create_from_translation([0.0,0.0,-3.0], dtype=np.float32)
        self.projection_matrix = pyrr.matrix44.create_perspective_projection(
            fovy=50.0, aspect=1.0, near=0.5, far=10.0, dtype=np.float32)
        
        self.sphere_model_matrix = pyrr.matrix44.create_from_translation([2.0, 0.0, -3.0], dtype=np.float32)

        #assure une bonne fluidité dans les mouvements
        
        self.translation_matrix = pyrr.matrix44.create_from_translation([0.0, 0.0, -3.0], dtype=np.float32)

   

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
        glfw.set_key_callback(window, self.binds.key_callback)
        return window

    def init_context(self):
        # activation du context OpenGL pour la fenêtre
        glfw.make_context_current(self.window)
        glfw.swap_interval(1)
        # activation de la gestion de la profondeur
        GL.glEnable(GL.GL_DEPTH_TEST)

    def init_programs(self):
        self.program = self.create_program_from_file('shader.vert', 'shader.frag')
        GL.glUseProgram(self.program)

    def init_data(self):
        obj = Object()
        obj.cube()
        self.vertices_cube = obj.vertices_cube
        self.indices = obj.indices

        sphere_data = generate_sphere(radius=1.0, lat_segments=32, lon_segments=64)
        self.sphere_vertices = sphere_data['interlaced']
        self.sphere_indices = sphere_data['faces'].reshape(-1)
        self.sphere_nb_indices = len(self.sphere_indices)


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

        self.nb_indices = len(self.indices)

        #VAO VBO VEO et maillage pour sphère
        self.sphere_vao = GL.glGenVertexArrays(1)
        GL.glBindVertexArray(self.sphere_vao)

        self.sphere_vbo = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.sphere_vbo)
        GL.glBufferData(GL.GL_ARRAY_BUFFER, self.sphere_vertices.nbytes, self.sphere_vertices, GL.GL_STATIC_DRAW)

        self.sphere_ebo = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, self.sphere_ebo)
        GL.glBufferData(GL.GL_ELEMENT_ARRAY_BUFFER, self.sphere_indices.nbytes, self.sphere_indices, GL.GL_STATIC_DRAW)

        stride = 11 * 4  # float size

        # position
        GL.glEnableVertexAttribArray(0)
        GL.glVertexAttribPointer(0, 3, GL.GL_FLOAT, False, stride, ctypes.c_void_p(0))

        # normal
        GL.glEnableVertexAttribArray(1)
        GL.glVertexAttribPointer(1, 3, GL.GL_FLOAT, False, stride, ctypes.c_void_p(3 * 4))

        # color
        GL.glEnableVertexAttribArray(2)
        GL.glVertexAttribPointer(2, 3, GL.GL_FLOAT, False, stride, ctypes.c_void_p(6 * 4))

        # uv
        GL.glEnableVertexAttribArray(3)
        GL.glVertexAttribPointer(3, 2, GL.GL_FLOAT, False, stride, ctypes.c_void_p(9 * 4))


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
            loc_model = GL.glGetUniformLocation(self.program, "model")
            if loc_model != -1:
                GL.glUniformMatrix4fv(loc_model, 1, GL.GL_FALSE, self.model_matrix)

            loc_projection = GL.glGetUniformLocation(self.program, "projection")
            if loc_projection != -1:
                GL.glUniformMatrix4fv(loc_projection, 1, GL.GL_FALSE, self.projection_matrix)

            GL.glBindVertexArray(self.vao)
            GL.glDrawElements(GL.GL_TRIANGLES, self.nb_indices, GL.GL_UNSIGNED_INT, None)
            
            # Dessiner la sphère avec sa propre matrice modèle fixe
            sphere_model = pyrr.matrix44.create_from_translation([2.0, 0.0, -3.0], dtype=np.float32)
            GL.glUniformMatrix4fv(loc_model, 1, GL.GL_FALSE, sphere_model)
            GL.glBindVertexArray(self.sphere_vao)
            GL.glDrawElements(GL.GL_TRIANGLES, self.sphere_nb_indices, GL.GL_UNSIGNED_INT, None)


            # changement de buffer d'affichage pour éviter un effet de scintillement
            glfw.swap_buffers(self.window)
            # gestion des évènements
            glfw.poll_events()

            frames += 1
            current_time = time.time()
            dt = current_time - previous_time
            previous_time = current_time

            # Calculer la direction avant (Z négatif dans le repère objet)
            forward = np.array([0, 0, -1, 0], dtype=np.float32)
            # Appliquer la rotation actuelle pour obtenir la direction orientée
            oriented_forward = pyrr.matrix44.apply_to_vector(self.model_matrix, forward)[:3]

            # Calculer la direction droite (X positif dans le repère objet)
            right = np.array([1, 0, 0, 0], dtype=np.float32)
            oriented_right = pyrr.matrix44.apply_to_vector(self.model_matrix, right)[:3]

            # Normaliser les vecteurs
            oriented_forward = oriented_forward / np.linalg.norm(oriented_forward)
            oriented_right = oriented_right / np.linalg.norm(oriented_right)

            # Calcul du mouvement en fonction des inputs
            movement = np.zeros(3, dtype=np.float32)
            if self.translation_velocity[2] != 0:  # Avant/arrière
                movement += oriented_forward * self.translation_velocity[2] * dt
            if self.translation_velocity[0] != 0:  # Gauche/droite
                movement += oriented_right * self.translation_velocity[0] * dt

            # Appliquer le mouvement si nécessaire
            if np.linalg.norm(movement) > 0:
                translation = pyrr.matrix44.create_from_translation(movement, dtype=np.float32)
                self.model_matrix = pyrr.matrix44.multiply(translation, self.model_matrix)
                
            # Gestion des rotations
            if self.rotation_velocity[0] != 0:  # Rotation horizontale (Y)
                # Créer la rotation autour du centre de l'objet
                rot_y = pyrr.matrix44.create_from_y_rotation(self.rotation_velocity[0] * dt, dtype=np.float32)
                self.model_matrix = pyrr.matrix44.multiply(self.model_matrix, rot_y)
            if self.rotation_velocity[1] != 0:  # Rotation verticale (X)
                rot_x = pyrr.matrix44.create_from_x_rotation(self.rotation_velocity[1] * dt, dtype=np.float32)
                self.model_matrix = pyrr.matrix44.multiply(self.model_matrix, rot_x)
        glfw.terminate()
                


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
            # Normale (normée car sphère unitaire)
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


def main():
    g = Game()
    g.run()
    glfw.terminate()

if __name__ == '__main__':
    main() 