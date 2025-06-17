import numpy as np
import OpenGL.GL as GL
import pyrr
import glfw

class Object_3d:
    def __init__(self, vao, position, angle, shader_program, texture, nb_sommets, taille, window, radius = None):
        self.vao = vao
        self.position = position
        self.angle = angle
        self.shader_program = shader_program
        self.texture = texture
        self.nb_sommets = nb_sommets
        self.taille = taille
        self.dir = np.array([0.0, 0.0, 1.0, 0.0], dtype=np.float32)  # Direction initiale
        self.velocity = np.array([0.0, 0.0, 0.0, 1.0], dtype=np.float32)  # Vitesse initiale
        self.window = window
        self.gravity = np.array([0.0, -9.81, 0.0, 0.0], dtype=np.float32)
        self.radius = radius

    def show_object(self):
        
        GL.glUseProgram(self.shader_program)

        rot4x = pyrr.matrix44.create_from_x_rotation(self.angle[0])
        rot4y = pyrr.matrix44.create_from_y_rotation(self.angle[1])
        rot4z = pyrr.matrix44.create_from_z_rotation(self.angle[2])
        rot4 = pyrr.matrix44.multiply(rot4x,rot4y)
        rot4 = pyrr.matrix44.multiply(rot4, rot4z)

        self.dir = pyrr.matrix44.apply_to_vector(rot4, np.array([0.0, 0.0, 1.0, 0.0], dtype=np.float32))

        trans = pyrr.matrix44.create_from_translation(self.position)

        self.model_matrix = rot4 @ trans

        if self.texture is not None:
            GL.glBindTexture(GL.GL_TEXTURE_2D, self.texture) 

        prog = GL.glGetIntegerv(GL.GL_CURRENT_PROGRAM)

        loc = GL.glGetUniformLocation(prog, "model")
        if loc == -1:
            print("Uniform 'model' not found in shader program.")
            return
        GL.glUniformMatrix4fv(loc, 1, GL.GL_FALSE, self.model_matrix)

        GL.glBindVertexArray(self.vao)
        GL.glDrawElements(GL.GL_TRIANGLES, self.nb_sommets, GL.GL_UNSIGNED_INT, None)
    
    def move_object(self, dt, speed, rotation_speed):
        if glfw.get_key(self.window, glfw.KEY_W) == glfw.PRESS or glfw.get_key(self.window, glfw.KEY_UP) == glfw.PRESS:
            self.position += self.dir * speed * dt
        if glfw.get_key(self.window, glfw.KEY_S) == glfw.PRESS or glfw.get_key(self.window, glfw.KEY_DOWN) == glfw.PRESS:
            self.position -= self.dir * speed * dt
        if glfw.get_key(self.window, glfw.KEY_A) == glfw.PRESS or glfw.get_key(self.window, glfw.KEY_LEFT) == glfw.PRESS:
            self.angle[1] -= rotation_speed * dt
        if glfw.get_key(self.window, glfw.KEY_D) == glfw.PRESS or glfw.get_key(self.window, glfw.KEY_RIGHT) == glfw.PRESS:
            self.angle[1] += rotation_speed * dt

        self.velocity += self.gravity * dt
        self.position += self.velocity * dt

    def jump(self, jump_speed):
        if glfw.get_key(self.window, glfw.KEY_SPACE) == glfw.PRESS:
            self.velocity[1] += jump_speed