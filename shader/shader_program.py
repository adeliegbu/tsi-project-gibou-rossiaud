import OpenGL.GL as GL
import os

class ShaderProgram:
    def __init__(self, vertex_shader, fragment_shader):
        with open(vertex_shader, 'r') as f:
            vs_src = f.read()
        with open(fragment_shader, 'r') as f:
            fs_src = f.read()
        self.program_id = self.create_program(vs_src, fs_src)

    def use(self):
        GL.glUseProgram(self.program_id)

    def get_id(self):
        return self.program_id

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
        # creation d'un programme GPU
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