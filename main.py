from game import Game
import OpenGL.GL as GL
import glfw 
import numpy as np
import time
import os 
import pyrr
from PIL import Image
import ctypes

from object._3d_object import Object 
from binds.binds import Binds


def main():
    g = Game()
    g.run()
    glfw.terminate()

if __name__ == '__main__':
    main() 