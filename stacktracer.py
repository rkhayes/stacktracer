import glfw
from OpenGL.GL import *


class Pane:
    """Base class for the mainframe screens."""
    def __init__(self, x, y, w, h, bg_color=(0.05, 0.05, 0.05)):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.bg_color = bg_color

    def update(self, dt):
        pass

    def render(self):
        """Override this to draw the panel contents."""
        pass

    def draw_borders(self):
        """Draw panel borders."""
        glColor3f(0.3, 0.3, 0.3)
        glBegin(GL_LINE_LOOP)
        glVertex2f(1, 1)
        glVertex2f(self.w-1, 1)
        glVertex2f(self.w-1, self.h-1)
        glVertex2f(1, self.h-1)
        glEnd()


MINI_FONT = {
    'A': ["010","101","111","101","101"], 'B': ["110","101","110","101","110"],
    'C': ["011","100","100","100","011"], 'D': ["110","101","101","101","110"],
    'E': ["111","100","111","100","111"], 'F': ["111","100","110","100","100"],
    'G': ["011","100","101","101","011"], 'H': ["101","101","111","101","101"],
    'I': ["111","010","010","010","111"], 'J': ["001","001","001","101","011"],
    'K': ["101","110","100","110","101"], 'L': ["100","100","100","100","111"],
    'M': ["101","111","101","101","101"], 'N': ["110","101","101","101","101"],
    'O': ["010","101","101","101","010"], 'P': ["110","101","110","100","100"],
    'Q': ["010","101","101","110","001"], 'R': ["110","101","110","101","101"],
    'S': ["011","100","010","001","110"], 'T': ["111","010","010","010","010"],
    'U': ["101","101","101","101","011"], 'V': ["101","101","101","101","010"],
    'W': ["101","101","101","111","101"], 'X': ["101","101","010","101","101"],
    'Y': ["101","101","010","010","010"], 'Z': ["111","001","010","100","111"],
    '.': ["000","000","000","000","010"], ' ': ["000","000","000","000","000"],
    '>': ["100","010","001","010","100"], '-': ["000","000","111","000","000"],
}


class TextPane(Pane):
    def __init__(self, x, y, w, h, bg_color=(0.02, 0.05, 0.02)):
        super().__init__(x, y, w, h, bg_color)

        self.lines = [
            "> INIT STACKTRACER OS...",
            "> MEMORY SECTORS CORRUPTED.",
            "> LINEAR CLASSIFIER OFFLINE.",
            "> OPERATOR. REALIGN THE WEIGHTS."
        ]

        self.pixel_size = 3
        self.char_spacing = 2
        self.line_spacing = 10

        # TYPEWRITTER EFFECT STATE
        self.visible_chars = 0
        self.timer = 0.0
        self.speed = 0.05

    def update(self, dt):
        # REVEAL TEXT CHAR BY CHAR
        total_chars = sum(len(line) for line in self.lines)
        if self.visible_chars < total_chars:
            self.timer += dt
            if self.timer >= self.speed:
                self.visible_chars += 1
                self.timer = 0.0

    def draw_char(self, char, x, y):
        """Draws a single character using GL_QUADS as 'pixels'."""
        if char not in MINI_FONT:
            return

        matrix = MINI_FONT[char]
        glBegin(GL_QUADS)
        for row_idx, row in enumerate(matrix):
            for col_idx, pixel in enumerate(row):
                if pixel == '1':
                    px = x + (col_idx * self.pixel_size)
                    # Y subtracts because standard orthographic projection usually
                    # maps 0 to the bottom of the screen. We draw top-down.
                    py = y - (row_idx * self.pixel_size)

                    glVertex2f(px, py)
                    glVertex2f(px + self.pixel_size, py)
                    glVertex2f(px + self.pixel_size, py - self.pixel_size)
                    glVertex2f(px, py - self.pixel_size)
        glEnd()

    def render(self):
        # DEFINE TEXT COLOR
        glColor3f(0.8, 0.8, 0.8)

        start_x = 20
        # DRAW FROM TOP TO BOTTOM
        current_y = self.h - 30

        chars_drawn = 0

        for line in self.lines:
            current_x = start_x
            for char in line:
                if chars_drawn >= self.visible_chars:
                    return # Stop rendering if we've hit the typewriter limit

                self.draw_char(char, current_x, current_y)

                # Advance X cursor (3 pixels wide + spacing) * scale
                current_x += (3 * self.pixel_size) + (self.char_spacing * self.pixel_size)
                chars_drawn += 1

            # Move down for the next line (5 pixels tall + spacing) * scale
            current_y -= (5 * self.pixel_size) + (self.line_spacing * self.pixel_size)
