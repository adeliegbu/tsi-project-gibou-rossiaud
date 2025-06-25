import OpenGL.GL as GL
from ctypes import c_float, c_void_p, sizeof
import os
from PIL import Image
import numpy as np

def load_to_gpu(sommets, index):
    vao = GL.glGenVertexArrays(1)
    # affectation de la liste d'état courante
    GL.glBindVertexArray(vao)
    # attribution d’un buffer de données (1 indique la création d’un seul buffer)
    vbo = GL.glGenBuffers(1)
    # affectation du buffer courant
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, vbo)

    # copie des donnees des sommets sur la carte graphique
    GL.glBufferData(GL.GL_ARRAY_BUFFER, sommets, GL.GL_STATIC_DRAW)

    # Les deux commandes suivantes sont stockées dans l'état du vao courant
    # Active l'utilisation des données de positions
    # (le 0 correspond à la location dans le vertex shader)
    GL.glEnableVertexAttribArray(0)
    GL.glEnableVertexAttribArray(1)
    GL.glEnableVertexAttribArray(2)
    GL.glEnableVertexAttribArray(3)
    # Indique comment le buffer courant (dernier vbo "bindé")
    # est utilisé pour les positions des sommets
    sizefloat = sizeof(c_float())
    stride = 11*sizefloat
    GL.glVertexAttribPointer(0, 3, GL.GL_FLOAT, GL.GL_FALSE, stride, None)
    GL.glVertexAttribPointer(1, 3, GL.GL_FLOAT, GL.GL_FALSE, stride, c_void_p(3*sizefloat))
    GL.glVertexAttribPointer(2, 3, GL.GL_FLOAT, GL.GL_FALSE, stride, c_void_p(6*sizefloat))
    GL.glVertexAttribPointer(3, 2, GL.GL_FLOAT, GL.GL_FALSE, stride, c_void_p(9*sizefloat))


    # attribution d’un autre buffer de donnees
    vboi = GL.glGenBuffers(1)
    # affectation du buffer courant (buffer d’indice)
    GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER,vboi)
    # copie des indices sur la carte graphique
    GL.glBufferData(GL.GL_ELEMENT_ARRAY_BUFFER,index,GL.GL_STATIC_DRAW)

    return vao


def load_texture(filename):
    if not os.path.exists(filename):
        print(f'{25*"-"}\nError reading file:\n{filename}\n{25*"-"}')
    im = Image.open(filename).transpose(Image.Transpose.FLIP_TOP_BOTTOM).convert('RGBA')

    texture_id = GL.glGenTextures(1)
    # selection de la texture courante à partir de son identifiant
    GL.glBindTexture(GL.GL_TEXTURE_2D, texture_id)
    # parametrisation de la texture
    GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_S, GL.GL_REPEAT)
    GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_T, GL.GL_REPEAT)
    GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MAG_FILTER, GL.GL_LINEAR)
    GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, GL.GL_LINEAR)
    GL.glTexImage2D(GL.GL_TEXTURE_2D, 0, GL.GL_RGBA, im.width, im.height, 0, GL.GL_RGBA, GL.GL_UNSIGNED_BYTE, im.tobytes())
    return texture_id
