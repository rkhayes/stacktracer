import sys
import glfw
from OpenGL.GL import *

from stacktracer import TextPane


def main():
    width, height = 1200, 860

    # Try to create the game window and check for errors on glfw.init() and glfw.create_window()
    if not glfw.init():
        sys.exit(1)

    window = glfw.create_window(width, height, "STACKTRACER", None, None)
    if not window:
        glfw.terminate()
        sys.exit(1)

    glfw.make_context_current(window)

    # Instantiate the pane to fill the entire window
    terminal = TextPane(0, 0, width, height)

    last_time = glfw.get_time()

    while not glfw.window_should_close(window):
        # NOTE: Need to understand better how delta time works and how it will affect other functionalities of the game.
        current_time = glfw.get_time()
        dt = current_time - last_time
        last_time = current_time

        # NOTE: Here I also use the * Python operator to unpack the individual RGB
        # color values into the glClearColor red, green, blue arguments.
        glClearColor(*terminal.bg_color, 1.0)
        # Clear the screen by drawing pixels of the defined color to the entire screen.
        glClear(GL_COLOR_BUFFER_BIT)

        # Define standard 2D projection
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        # Map OpenGL coordinates directly to window pixels
        glOrtho(0, width, 0, height, -1, 1)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        # Run the internal pane object logic
        terminal.update(dt)
        terminal.render()
        terminal.draw_borders()

        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()


if __name__ == "__main__":
    main()
