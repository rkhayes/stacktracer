"""
STACKTRACER // MINIGAME 00 - LOGIC TREES (BST) - V2 (7 NÓS)
Módulo refatorado com progressão automática de nós (Auto-Targeting).
"""

from OpenGL.GL import *
import math
import glfw

PHOSPHOR_GREEN = (0.2, 0.9, 0.2)

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

nos = [
    {"id": 1, "valor": 50, "x": 0.0, "y": 0.6, "escala": 1.0, "rotacao": 0.0, "alvo_x": 0.0, "alvo_y": 0.6, "pai": None, "fixo": True},
    {"id": 2, "valor": 30, "x": -0.8, "y": -0.8, "escala": 1.0, "rotacao": 0.0, "alvo_x": -0.4, "alvo_y": 0.2, "pai": 1, "fixo": False},
    {"id": 3, "valor": 70, "x": 0.8, "y": -0.8, "escala": 1.0, "rotacao": 0.0, "alvo_x": 0.4, "alvo_y": 0.2, "pai": 1, "fixo": False},
    {"id": 4, "valor": 20, "x": -0.5, "y": -0.8, "escala": 1.0, "rotacao": 0.0, "alvo_x": -0.6, "alvo_y": -0.2, "pai": 2, "fixo": False},
    {"id": 5, "valor": 40, "x": -0.2, "y": -0.8, "escala": 1.0, "rotacao": 0.0, "alvo_x": -0.2, "alvo_y": -0.2, "pai": 2, "fixo": False},
    {"id": 6, "valor": 60, "x": 0.2, "y": -0.8, "escala": 1.0, "rotacao": 0.0, "alvo_x": 0.2, "alvo_y": -0.2, "pai": 3, "fixo": False},
    {"id": 7, "valor": 80, "x": 0.5, "y": -0.8, "escala": 1.0, "rotacao": 0.0, "alvo_x": 0.6, "alvo_y": -0.2, "pai": 3, "fixo": False},
]

# NOVO SISTEMA DE SEQUÊNCIA
NODE_SEQUENCE = [30, 20, 40, 60, 80, 70]
sequence_idx = 0

def get_node_idx_by_value(val):
    for i, n in enumerate(nos):
        if n["valor"] == val:
            return i
    return 1

no_ativo_idx = get_node_idx_by_value(NODE_SEQUENCE[sequence_idx])
global_text_pane = None

def init_game(main_text_pane):
    global global_text_pane
    global_text_pane = main_text_pane

def verificar_arvore_completa():
    for no in nos:
        if not no["fixo"]: return False
    return True

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

def process_input(key, action, glfw_module):
    global no_ativo_idx, global_text_pane, sequence_idx
    
    if action == glfw_module.PRESS or action == glfw_module.REPEAT:
        
        no_atual = nos[no_ativo_idx]
        
        if not no_atual["fixo"]:
            if key == glfw_module.KEY_RIGHT: no_atual["x"] += 0.05
            elif key == glfw_module.KEY_LEFT: no_atual["x"] -= 0.05
            elif key == glfw_module.KEY_UP: no_atual["y"] += 0.05
            elif key == glfw_module.KEY_DOWN: no_atual["y"] -= 0.05
            elif key == glfw_module.KEY_Q: no_atual["rotacao"] += 10.0
            elif key == glfw_module.KEY_E: no_atual["rotacao"] -= 10.0
            elif key == glfw_module.KEY_W: no_atual["escala"] += 0.1
            elif key == glfw_module.KEY_S: no_atual["escala"] = max(0.2, no_atual["escala"] - 0.1)
            
            elif key == glfw_module.KEY_SPACE:
                distancia = math.sqrt((no_atual["x"] - no_atual["alvo_x"])**2 + (no_atual["y"] - no_atual["alvo_y"])**2)
                
                if distancia < 0.15:
                    no_atual["x"], no_atual["y"], no_atual["escala"], no_atual["rotacao"] = no_atual["alvo_x"], no_atual["alvo_y"], 1.0, 0.0
                    no_atual["fixo"] = True
                    global_text_pane.clear()
                    
                    if verificar_arvore_completa():
                        global_text_pane.write_new_sequence([f"> NODE {no_atual['valor']} ALIGNED.", "> ALL LOGIC TREES RESTORED.", "> PRESS ENTER TO FINISH."])
                    else:
                        # PROGRESSÃO AUTOMÁTICA
                        sequence_idx += 1
                        if sequence_idx < len(NODE_SEQUENCE):
                            next_val = NODE_SEQUENCE[sequence_idx]
                            no_ativo_idx = get_node_idx_by_value(next_val)
                            global_text_pane.write_new_sequence([
                                f"> NODE {no_atual['valor']} ALIGNED.", 
                                f"> AUTO-TARGETING NODE {next_val}..."
                            ])
                else:
                    global_text_pane.clear()
                    global_text_pane.write_new_sequence(["> CALIBRATION FAILED.", "> INVALID BST POSITION."])

def render(fb_width, top_h):
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-1.0, 1.0, -1.0, 1.0, -1.0, 1.0) 
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    
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
            glPushMatrix()
            glTranslatef(no["alvo_x"], no["alvo_y"], 0.0)
            desenhar_silhueta()
            glPopMatrix()
    
    for no in nos:
        if no["fixo"] and no["pai"] is not None:
            pai = next(p for p in nos if p["id"] == no["pai"])
            desenhar_linha_conexao(no["x"], no["y"], pai["x"], pai["y"])

    for i, no in enumerate(nos):
        glPushMatrix() 
        glTranslatef(no["x"], no["y"], 0.0)
        glRotatef(no["rotacao"], 0.0, 0.0, 1.0)
        escala = no["escala"] * 1.2 if (i == no_ativo_idx and not no["fixo"]) else no["escala"]
        glScalef(escala, escala, 1.0)
        desenhar_hexagono()
        desenhar_numero(no["valor"])
        glPopMatrix()