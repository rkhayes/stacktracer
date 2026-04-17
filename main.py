import sys
import glfw
from OpenGL.GL import *

from stacktracer import TextPane

def main():
    width, height = 800, 600

    if not glfw.init():
        sys.exit(1)

    window = glfw.create_window(width, height, "STACKTRACER", None, None)
    if not window:
        glfw.terminate()
        sys.exit(1)

    glfw.make_context_current(window)

    # Instantiate the pane to fill the entire window for this test
    # (x, y, width, height)
    terminal = TextPane(0, 0, width, height)

    last_time = glfw.get_time()

    while not glfw.window_should_close(window):
        # Calculate delta time for the typewriter effect
        current_time = glfw.get_time()
        dt = current_time - last_time
        last_time = current_time

        # Clear screen with the pane's background color
        glClearColor(*terminal.bg_color, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)

        # Setup standard 2D projection
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        # Map OpenGL coordinates directly to window pixels
        glOrtho(0, width, 0, height, -1, 1)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        # RUN PANE LOGIC
        terminal.update(dt)
        terminal.render()
        terminal.draw_borders()

        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()

if __name__ == "__main__":
    main()
