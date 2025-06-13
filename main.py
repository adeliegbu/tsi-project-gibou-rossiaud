from game import Game
import glfw

def main():
    g = Game()
    g.run()
    glfw.terminate()

if __name__ == '__main__':
    main() 