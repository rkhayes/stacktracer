"""
STACKTRACER // MINIGAME 00 - LOGIC TREES (BST) - V2 (7 NÓS)
Projeto de Computação Gráfica.

Fase 1 expandida com 7 nós, integrando a engine de 
texto Retro-Terminal eViewports divididos.
"""

import glfw
from OpenGL.GL import *
from OpenGL.GLU import gluOrtho2D
import math
import sys

WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
PHOSPHOR_GREEN = (0.2, 0.9, 0.2)

# ==============================================================================
# DICIONÁRIO DE FONTES RETRO
# ==============================================================================
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
    '?': ["011","101","010","000","010"], "'": ["010","010","000","000","000"],
    ',': ["000","000","000","010","100"]
}

# ==============================================================================
# CLASSES DE INTERFACE
# ==============================================================================
class Pane:
    def __init__(self, x, y, w, h, bg_color=(0.0, 0.0, 0.0)):
        self.x, self.y, self.w, self.h = x, y, w, h
        self.bg_color = bg_color

class TextPane(Pane):
    def __init__(self, x, y, w, h, bg_color=(0.0, 0.0, 0.0)):
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
        glColor3f(*PHOSPHOR_GREEN) 
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
    glColor3f(*PHOSPHOR_GREEN)
    glLineWidth(2.0)    
    glBegin(GL_LINE_LOOP)
    glVertex2f(padding, padding)
    glVertex2f(width - padding, padding)
    glVertex2f(width - padding, height - padding)
    glVertex2f(padding, height - padding)
    glEnd()
    glLineWidth(1.0)

# ==============================================================================
# ESTADO DA ÁRVORE (BST) - EXPANDIDO PARA 7 NÓS
# ==============================================================================
text_pane = None

nos = [
    # id, valor, x, y inicial, escala, rotacao, alvo_x, alvo_y, pai, fixo
    {"id": 1, "valor": 50, "x": 0.0, "y": 0.6, "escala": 1.0, "rotacao": 0.0, "alvo_x": 0.0, "alvo_y": 0.6, "pai": None, "fixo": True},
    {"id": 2, "valor": 30, "x": -0.8, "y": -0.8, "escala": 1.0, "rotacao": 0.0, "alvo_x": -0.4, "alvo_y": 0.2, "pai": 1, "fixo": False},
    {"id": 3, "valor": 70, "x": 0.8, "y": -0.8, "escala": 1.0, "rotacao": 0.0, "alvo_x": 0.4, "alvo_y": 0.2, "pai": 1, "fixo": False},
    {"id": 4, "valor": 20, "x": -0.5, "y": -0.8, "escala": 1.0, "rotacao": 0.0, "alvo_x": -0.6, "alvo_y": -0.2, "pai": 2, "fixo": False},
    {"id": 5, "valor": 40, "x": -0.2, "y": -0.8, "escala": 1.0, "rotacao": 0.0, "alvo_x": -0.2, "alvo_y": -0.2, "pai": 2, "fixo": False}, # Novo
    {"id": 6, "valor": 60, "x": 0.2, "y": -0.8, "escala": 1.0, "rotacao": 0.0, "alvo_x": 0.2, "alvo_y": -0.2, "pai": 3, "fixo": False},
    {"id": 7, "valor": 80, "x": 0.5, "y": -0.8, "escala": 1.0, "rotacao": 0.0, "alvo_x": 0.6, "alvo_y": -0.2, "pai": 3, "fixo": False}, # Novo
]
no_ativo_idx = 1 # Começa no nó 30

def verificar_arvore_completa():
    for no in nos:
        if not no["fixo"]: return False
    return True

# ==============================================================================
# FUNÇÕES DE DESENHO
# ==============================================================================
def desenhar_hexagono():
    glColor3f(0.0, 0.0, 0.0)
    glBegin(GL_POLYGON)
    for i in range(6):
        angulo = 2 * math.pi * i / 6
        glVertex2f(0.15 * math.cos(angulo), 0.15 * math.sin(angulo))
    glEnd()
    glColor3f(*PHOSPHOR_GREEN)
    glLineWidth(2.0)
    glBegin(GL_LINE_LOOP)
    for i in range(6):
        angulo = 2 * math.pi * i / 6
        glVertex2f(0.15 * math.cos(angulo), 0.15 * math.sin(angulo))
    glEnd()

def desenhar_linha_conexao(x1, y1, x2, y2):
    glColor3f(*PHOSPHOR_GREEN)
    glLineWidth(2.0)
    glBegin(GL_LINES)
    glVertex2f(x1, y1)
    glVertex2f(x2, y2)
    glEnd()

def desenhar_silhueta():
    glColor3f(0.05, 0.3, 0.05) 
    glLineWidth(2.0)
    glEnable(GL_LINE_STIPPLE)
    glLineStipple(1, 0x0F0F)
    glBegin(GL_LINE_LOOP)
    for i in range(6):
        angulo = 2 * math.pi * i / 6
        glVertex2f(0.15 * math.cos(angulo), 0.15 * math.sin(angulo))
    glEnd()
    glDisable(GL_LINE_STIPPLE)

def desenhar_digito(d):
    segmentos = {
        'T':  ((-0.04,  0.08), ( 0.04,  0.08)),  'M':  ((-0.04,  0.00), ( 0.04,  0.00)),
        'B':  ((-0.04, -0.08), ( 0.04, -0.08)),  'TL': ((-0.04,  0.08), (-0.04,  0.00)),
        'BL': ((-0.04,  0.00), (-0.04, -0.08)),  'TR': (( 0.04,  0.08), ( 0.04,  0.00)),
        'BR': (( 0.04,  0.00), ( 0.04, -0.08)),
    }
    mapa_digitos = {
        '0': ['T','B','TL','BL','TR','BR'], '1': ['TR','BR'], '2': ['T','M','B','TR','BL'],
        '3': ['T','M','B','TR','BR'], '4': ['M','TL','TR','BR'], '5': ['T','M','B','TL','BR'],
        '6': ['T','M','B','TL','BL','BR'], '7': ['T','TR','BR'], '8': ['T','M','B','TL','BL','TR','BR'],
        '9': ['T','M','B','TL','TR','BR']
    }
    glBegin(GL_LINES)
    for seg in mapa_digitos[str(d)]:
        p1, p2 = segmentos[seg]
        glVertex2f(p1[0], p1[1])
        glVertex2f(p2[0], p2[1])
    glEnd()

def desenhar_numero(numero):
    texto = str(numero)
    espacamento = 0.12 
    inicio_x = -(len(texto) * espacamento) / 2.0 + (espacamento / 2.0)
    glColor3f(*PHOSPHOR_GREEN) 
    glLineWidth(2.0)
    glPushMatrix()
    glTranslatef(inicio_x, 0.0, 0.0)
    for char in texto:
        desenhar_digito(char)
        glTranslatef(espacamento, 0.0, 0.0)
    glPopMatrix() 

# ==============================================================================
# INPUT E LÓGICA
# ==============================================================================
def key_callback(window, key, scancode, action, mods):
    global no_ativo_idx, text_pane
    
    if action == glfw.PRESS or action == glfw.REPEAT:
        # SELEÇÃO (TECLAS 1 A 7)
        if glfw.KEY_1 <= key <= glfw.KEY_7:
            idx = key - glfw.KEY_1
            if not nos[idx]["fixo"]:
                no_ativo_idx = idx
                text_pane.clear()
                text_pane.write_new_sequence([f"> TARGET: NODE {nos[idx]['valor']}"])
            else:
                text_pane.clear()
                text_pane.write_new_sequence([f"> NODE {nos[idx]['valor']} IS LOCKED."])

        no_atual = nos[no_ativo_idx]
        
        if not no_atual["fixo"]:
            if key == glfw.KEY_RIGHT: no_atual["x"] += 0.05
            elif key == glfw.KEY_LEFT: no_atual["x"] -= 0.05
            elif key == glfw.KEY_UP: no_atual["y"] += 0.05
            elif key == glfw.KEY_DOWN: no_atual["y"] -= 0.05
            elif key == glfw.KEY_Q: no_atual["rotacao"] += 10.0
            elif key == glfw.KEY_E: no_atual["rotacao"] -= 10.0
            elif key == glfw.KEY_W: no_atual["escala"] += 0.1
            elif key == glfw.KEY_S: no_atual["escala"] = max(0.2, no_atual["escala"] - 0.1)
            
            elif key == glfw.KEY_SPACE:
                distancia = math.sqrt((no_atual["x"] - no_atual["alvo_x"])**2 + (no_atual["y"] - no_atual["alvo_y"])**2)
                
                if distancia < 0.15:
                    no_atual["x"], no_atual["y"], no_atual["escala"], no_atual["rotacao"] = no_atual["alvo_x"], no_atual["alvo_y"], 1.0, 0.0
                    no_atual["fixo"] = True
                    text_pane.clear()
                    if verificar_arvore_completa():
                        text_pane.write_new_sequence([f"> NODE {no_atual['valor']} ALIGNED.", "> ALL LOGIC TREES RESTORED.", "> PRESS ENTER."])
                    else:
                        text_pane.write_new_sequence([f"> NODE {no_atual['valor']} ALIGNED."])
                else:
                    text_pane.clear()
                    text_pane.write_new_sequence(["> CALIBRATION FAILED.", "> INVALID BST POSITION."])

# ==============================================================================
# MAIN
# ==============================================================================
def main():
    global text_pane
    if not glfw.init(): return

    window = glfw.create_window(800, 600, "STACKTRACER // BST V2", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)
    glfw.set_key_callback(window, key_callback)

    text_pane = TextPane(0, 0, WINDOW_WIDTH, 300)
    text_pane.write_new_sequence([
        "> SYSTEM FAILURE: 7 MEMORY SECTORS CORRUPTED.",
        "> BOOTING BST CALIBRATION PROTOCOL...",
        "> SELECT NODES 1-7. SPACE TO SUBMIT."
    ])
    
    last_time = glfw.get_time()

    while not glfw.window_should_close(window):
        dt = glfw.get_time() - last_time
        last_time = glfw.get_time()

        glClearColor(0.0, 0.0, 0.0, 1.0); glClear(GL_COLOR_BUFFER_BIT)

        fb_width, fb_height = glfw.get_framebuffer_size(window)
        top_h, bot_h = int(fb_height * 0.70), fb_height - int(fb_height * 0.70)

        # VIEWPORT JOGO
        glViewport(0, bot_h, fb_width, top_h)
        glMatrixMode(GL_PROJECTION); glLoadIdentity()
        glOrtho(-1.0, 1.0, -1.0, 1.0, -1.0, 1.0) 
        glMatrixMode(GL_MODELVIEW); glLoadIdentity()
        
        #faz a borda corretamente
        glColor3f(*PHOSPHOR_GREEN)
        glLineWidth(2.0)
        glBegin(GL_LINE_LOOP)
        glVertex2f(-0.99, -0.99)
        glVertex2f( 0.99, -0.99)
        glVertex2f( 0.99,  0.99)
        glVertex2f(-0.99,  0.99)
        glEnd()
        glLineWidth(1.0)

        
        glScalef(1.0 / (fb_width/float(top_h)), 1.0, 1.0)

        for no in nos:
            if not no["fixo"]:
                glPushMatrix(); glTranslatef(no["alvo_x"], no["alvo_y"], 0.0); desenhar_silhueta(); glPopMatrix()
        
        for no in nos:
            if no["fixo"] and no["pai"] is not None:
                pai = next(p for p in nos if p["id"] == no["pai"])
                desenhar_linha_conexao(no["x"], no["y"], pai["x"], pai["y"])

        for i, no in enumerate(nos):
            glPushMatrix() 
            glTranslatef(no["x"], no["y"], 0.0); glRotatef(no["rotacao"], 0.0, 0.0, 1.0)
            escala = no["escala"] * 1.2 if (i == no_ativo_idx and not no["fixo"]) else no["escala"]
            glScalef(escala, escala, 1.0)
            desenhar_hexagono(); desenhar_numero(no["valor"]); glPopMatrix()

        # VIEWPORT TERMINAL
        glViewport(0, 0, fb_width, bot_h)
        glMatrixMode(GL_PROJECTION); glLoadIdentity(); gluOrtho2D(0, fb_width, 0, bot_h)
        glMatrixMode(GL_MODELVIEW); glLoadIdentity()

        draw_panel_border(fb_width, bot_h)
        text_pane.w, text_pane.h = fb_width, bot_h
        
        if not verificar_arvore_completa():
            no_at = nos[no_ativo_idx]
            text_pane.set_metrics(f"> TARGET: {no_at['valor']} | X: {no_at['x']:.2f} | Y: {no_at['y']:.2f}")

        text_pane.update(dt); text_pane.render()
        glfw.swap_buffers(window); glfw.poll_events()

    glfw.terminate()

if __name__ == "__main__":
    main()