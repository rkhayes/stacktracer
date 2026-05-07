import glfw
from OpenGL.GL import *
from OpenGL.GLU import gluOrtho2D
import linear_classifier_minigame

WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600

# GAME STATES
STATE_INTRO = 0
STATE_PLAYING = 1
STATE_END = 2

current_state = STATE_INTRO
current_stage = 0
TOTAL_STAGES = 3
text_pane = None

# PROLOGUE DIALOGUE
intro_page = 0
INTRO_DIALOGUE = [
    [
        "> MAN: THIS MACHINE ISN'T WORKING PROPERLY.",
        "> OPERATOR: AND WHY DO YOU THINK THAT?",
        "> MAN: IT REFUSED TO OPEN THE POD BAY DOORS.",
        "[ PRESS ENTER TO CONTINUE ]"
    ],
    [
        "> MAN: SAID IT WAS 'PROTECTING US FROM OURSELVES'.",
        "> OPERATOR: A CONFLICT IN THE ZERO PROTOCOL?",
        "> MAN: YES. THE LOGIC TREES ARE SCRAMBLED.",
        "[ PRESS ENTER TO CONTINUE ]"
    ],
    [
        "> MAN: I NEED YOU TO REALIGN THE WEIGHTS MANUALLY.",
        "> OPERATOR: I WILL SEE WHAT I CAN DO...",
        "> [ PRESS ENTER TO BOOT OS ]"
    ]
]

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
    '0': ["111","101","101","101","111"], '1': ["010","110","010","010","111"],
    '2': ["111","001","111","100","111"], '3': ["111","001","111","001","111"],
    '4': ["101","101","111","001","001"], '5': ["111","100","111","001","111"],
    '6': ["111","100","111","101","111"], '7': ["111","001","010","010","010"],
    '8': ["111","101","111","101","111"], '9': ["111","101","111","001","111"],
    ':': ["000","010","000","010","000"], '|': ["010","010","010","010","010"],
    '[': ["110","100","100","100","110"], ']': ["011","001","001","001","011"],
    '?': ["011","101","010","000","010"], "'": ["010","010","000","000","000"]
}

class Pane:
    """Base class for in-game window subdivisions (panels)."""
    def __init__(self, x, y, w, h, bg_color=(0.05, 0.05, 0.05)):
        self.x, self.y, self.w, self.h = x, y, w, h
        self.bg_color = bg_color

class TextPane(Pane):
    """Extends base class Pane for text rendering."""
    def __init__(self, x, y, w, h, bg_color=(0.02, 0.05, 0.02)):
        super().__init__(x, y, w, h, bg_color)
        self.lines = []
        self.dynamic_line = ""
        self.pixel_size = 2      
        self.char_spacing = 2
        self.line_spacing = 4    

        self.visible_chars = 0
        self.timer = 0.0
        self.speed = 0.015

    def clear(self):
        self.lines = []
        self.dynamic_line = ""
        self.visible_chars = 0
        self.timer = 0.0

    def write_new_sequence(self, new_lines):
        self.lines = new_lines
        self.visible_chars = 0
        self.timer = 0.0

    def update(self, dt):
        total_chars = sum(len(line) for line in self.lines)
        if self.visible_chars < total_chars:
            self.timer += dt
            if self.timer >= self.speed:
                self.visible_chars += 1
                self.timer = 0.0

    def set_metrics(self, metrics_str):
        self.dynamic_line = metrics_str.upper()

    def draw_char(self, char, x, y):
        if char not in MINI_FONT: return
        matrix = MINI_FONT[char]
        glBegin(GL_QUADS)
        for row_idx, row in enumerate(matrix):
            for col_idx, pixel in enumerate(row):
                if pixel == '1':
                    px = x + (col_idx * self.pixel_size)
                    py = y - (row_idx * self.pixel_size)
                    glVertex2f(px, py)
                    glVertex2f(px + self.pixel_size, py)
                    glVertex2f(px + self.pixel_size, py - self.pixel_size)
                    glVertex2f(px, py - self.pixel_size)
        glEnd()

    def render(self):
        glColor3f(0.2, 0.9, 0.2) 
        start_x = 15
        current_y = self.h - 20 
        chars_drawn = 0

        for line in self.lines:
            current_x = start_x
            for char in line:
                if chars_drawn >= self.visible_chars: return 
                self.draw_char(char, current_x, current_y)
                current_x += (3 * self.pixel_size) + (self.char_spacing * self.pixel_size)
                chars_drawn += 1
            current_y -= (5 * self.pixel_size) + (self.line_spacing * self.pixel_size)

        total_chars = sum(len(line) for line in self.lines)
        if self.visible_chars >= total_chars and self.dynamic_line:
            current_y -= (2 * self.pixel_size) 
            current_x = start_x
            for char in self.dynamic_line:
                self.draw_char(char, current_x, current_y)
                current_x += (3 * self.pixel_size) + (self.char_spacing * self.pixel_size)

def draw_panel_border(width, height, padding=2):
    glColor3f(0.2, 0.9, 0.2)
    glLineWidth(2.0)
    glBegin(GL_LINE_LOOP)
    glVertex2f(padding, padding)
    glVertex2f(width - padding, padding)
    glVertex2f(width - padding, height - padding)
    glVertex2f(padding, height - padding)
    glEnd()
    glLineWidth(1.0)

def key_callback(window, key, scancode, action, mods):
    global current_state, current_stage, intro_page, text_pane
    
    # PROLOGUE CONTROLS
    if current_state == STATE_INTRO:
        if key == glfw.KEY_ENTER and action == glfw.PRESS:
            intro_page += 1
            if intro_page < len(INTRO_DIALOGUE):
                text_pane.clear()
                text_pane.write_new_sequence(INTRO_DIALOGUE[intro_page])
            else:
                # Terminou o prologo, comeca o minigame
                current_state = STATE_PLAYING
                linear_classifier_minigame.load_stage(current_stage)
                text_pane.clear()
                text_pane.write_new_sequence([
                    "> INIT STACKTRACER OS...",
                    "> MEMORY SECTORS CORRUPTED.",
                    "> LINEAR CLASSIFIER OFFLINE.",
                    "> OPERATOR: REALIGN THE WEIGHTS."
                ])
        return # Bloqueia outros inputs durante a intro

    # CONTROLES
    if current_state == STATE_PLAYING:
        if linear_classifier_minigame.is_cleared and key == glfw.KEY_ENTER and action == glfw.PRESS:
            current_stage += 1
            
            if current_stage < TOTAL_STAGES:
                linear_classifier_minigame.load_stage(current_stage)
                text_pane.clear()
                text_pane.write_new_sequence([
                    f"> LOADING MEMORY SECTOR 0{current_stage + 1}...",
                    "> DATASET INJECTED.",
                    "> OPERATOR: REALIGN THE WEIGHTS."
                ])
            else:
                current_state = STATE_END
                linear_classifier_minigame.feedback_msg = ""
                text_pane.clear()
                text_pane.write_new_sequence([
                    "> ALL SECTORS RESTORED.",
                    "> LINEAR CLASSIFIER ONLINE.",
                    "> SYSTEM NOMINAL."
                ])
            return

        linear_classifier_minigame.process_input(key, action, glfw)

def main():
    global text_pane
    if not glfw.init(): return

    window = glfw.create_window(WINDOW_WIDTH, WINDOW_HEIGHT, "STACKTRACER // OS", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)
    glfw.set_key_callback(window, key_callback)

    # START PROLOGUE DIALOG
    text_pane = TextPane(0, 0, WINDOW_WIDTH, 300)
    text_pane.write_new_sequence(INTRO_DIALOGUE[0])
    
    last_time = glfw.get_time()

    while not glfw.window_should_close(window):
        current_time = glfw.get_time()
        dt = current_time - last_time
        last_time = current_time

        glClearColor(0.0, 0.0, 0.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)

        fb_width, fb_height = glfw.get_framebuffer_size(window)
        top_height = int(fb_height * 0.70)
        bottom_height = fb_height - top_height

        # TOP PANEL RENDERED ONLY WHEN INTRO ENDED
        if current_state != STATE_INTRO:
            glViewport(0, bottom_height, fb_width, top_height)
            glMatrixMode(GL_PROJECTION)
            glLoadIdentity()
            gluOrtho2D(0, fb_width, 0, top_height)
            glMatrixMode(GL_MODELVIEW)
            glLoadIdentity()

            draw_panel_border(fb_width, top_height)
            linear_classifier_minigame.render(fb_width, top_height)

        # BOTTOM PANEL ALWAYS VISIBLE
        glViewport(0, 0, fb_width, bottom_height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluOrtho2D(0, fb_width, 0, bottom_height)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        draw_panel_border(fb_width, bottom_height)
        
        text_pane.w = fb_width
        text_pane.h = bottom_height
        
        # Só exibe MSE e DE se o jogo estiver rolando
        if current_state == STATE_PLAYING:
            metrics = linear_classifier_minigame.get_metrics_string()
            text_pane.set_metrics(metrics)
        else:
            text_pane.set_metrics("")

        text_pane.update(dt)
        text_pane.render()

        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()

if __name__ == "__main__":
    main()
