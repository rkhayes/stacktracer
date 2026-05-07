import math
import glfw
from OpenGL.GL import *

PHOSPHOR_GREEN = (0.2, 0.9, 0.2)

# Três distribuições diferentes de pontos simulando "setores corrompidos"
DATASETS = [
    # Stage 1: Tendência Positiva (A reta sobe)
    [(0.15, 0.30), (0.30, 0.45), (0.45, 0.50), (0.60, 0.70), (0.70, 0.60), (0.85, 0.85)],
    # Stage 2: Tendência Negativa (A reta desce)
    [(0.10, 0.85), (0.25, 0.65), (0.45, 0.55), (0.65, 0.40), (0.85, 0.20)],
    # Stage 3: Tendência Íngreme (Maior variação)
    [(0.20, 0.20), (0.35, 0.30), (0.40, 0.60), (0.65, 0.70), (0.80, 0.90)]
]

current_dataset = DATASETS[0]

# Variáveis de Estado da Reta
line_cx_norm = 0.5
line_cy_norm = 0.5
line_angle = 0.0

# Variáveis de Estado do Jogo
is_cleared = False
feedback_msg = ""
panel_w, panel_h = 800.0, 420.0 

def load_stage(stage_index):
    """Reseta o estado do minigame e carrega os novos pontos."""
    global current_dataset, line_cx_norm, line_cy_norm, line_angle, is_cleared, feedback_msg
    if stage_index < len(DATASETS):
        current_dataset = DATASETS[stage_index]
    
    line_cx_norm = 0.5
    line_cy_norm = 0.5
    line_angle = 0.0
    is_cleared = False
    feedback_msg = ""

def get_optimal_mse():
    """Calcula a reta perfeita usando OLS (Mínimos Quadrados)."""
    n = len(current_dataset)
    sx = sum(p[0] * panel_w for p in current_dataset)
    sy = sum(p[1] * panel_h for p in current_dataset)
    sxy = sum((p[0] * panel_w) * (p[1] * panel_h) for p in current_dataset)
    sxx = sum((p[0] * panel_w) ** 2 for p in current_dataset)
    
    den = (n * sxx - sx * sx)
    if den == 0: return 0.0

    m_opt = (n * sxy - sx * sy) / den
    b_opt = (sy - m_opt * sx) / n
    
    opt_mse = 0.0
    for nx, ny in current_dataset:
        px = nx * panel_w
        py = ny * panel_h
        y_pred = m_opt * px + b_opt
        opt_mse += (py - y_pred) ** 2
        
    return opt_mse / n

def calculate_current_metrics():
    """Calcula o erro atual da reta ajustada pelo jogador."""
    angle_rad = math.radians(line_angle)
    slope = 1e6 if abs(math.cos(angle_rad)) < 1e-6 else math.tan(angle_rad)
    
    mse = 0.0
    euclidean_total = 0.0
    abs_cx = line_cx_norm * panel_w
    abs_cy = line_cy_norm * panel_h

    A = -slope
    B = 1.0
    C = slope * abs_cx - abs_cy

    for nx, ny in current_dataset:
        px = nx * panel_w
        py = ny * panel_h
        
        y_pred = slope * (px - abs_cx) + abs_cy
        mse += (py - y_pred) ** 2
        
        dist_orto = abs(A * px + B * py + C) / math.sqrt(A**2 + B**2)
        euclidean_total += dist_orto
        
    return mse / len(current_dataset), euclidean_total

def verify_solution():
    """Valida se o erro do jogador é satisfatório ao apertar SPACE."""
    global is_cleared, feedback_msg
    current_mse, _ = calculate_current_metrics()
    opt_mse = get_optimal_mse()
    
    # Tolerância: Aceita até 2.5x o erro da reta matemática perfeita
    tolerance_threshold = opt_mse * 2.5
    
    if current_mse <= tolerance_threshold:
        is_cleared = True
        feedback_msg = "> ALIGNMENT VERIFIED. PRESS [ENTER] FOR NEXT SECTOR."
    else:
        feedback_msg = "> ERROR: LOSS TOO HIGH. ADJUST WEIGHTS."

def process_input(key, action, glfw_module):
    global line_cy_norm, line_angle, feedback_msg

    if action == glfw_module.PRESS or action == glfw_module.REPEAT:
        if is_cleared: return # Trava o movimento se venceu

        if key == glfw_module.KEY_SPACE:
            verify_solution()
            return
            
        if key in [glfw_module.KEY_UP, glfw_module.KEY_DOWN, glfw_module.KEY_LEFT, glfw_module.KEY_RIGHT]:
            feedback_msg = "" # Limpa a mensagem de erro ao voltar a mover
            
        if key == glfw_module.KEY_UP: line_cy_norm += 0.02
        elif key == glfw_module.KEY_DOWN: line_cy_norm -= 0.02
        elif key == glfw_module.KEY_LEFT: line_angle += 2.0
        elif key == glfw_module.KEY_RIGHT: line_angle -= 2.0

def get_metrics_string():
    """Entrega a string que o terminal inferior vai renderizar."""
    if feedback_msg != "":
        return feedback_msg
        
    mse, euclidean_total = calculate_current_metrics()
    return f"> MSE: {mse/1000:05.1f} | EUCLID DIST: {euclidean_total:05.1f}"

def render(width, height):
    global panel_w, panel_h
    panel_w, panel_h = float(width), float(height)

    abs_cx = line_cx_norm * panel_w
    abs_cy = line_cy_norm * panel_h

    # Feedback visual na reta ao vencer
    if is_cleared: glColor3f(0.5, 1.0, 0.5)
    else: glColor3f(*PHOSPHOR_GREEN)

    for nx, ny in current_dataset:
        px = nx * panel_w
        py = ny * panel_h
        
        glBegin(GL_LINE_LOOP)
        for i in range(30):
            theta = 2.0 * math.pi * float(i) / 30.0
            glVertex2f(8 * math.cos(theta) + px, 8 * math.sin(theta) + py)
        glEnd()

    glPushMatrix()
    glTranslatef(abs_cx, abs_cy, 0.0)
    glRotatef(line_angle, 0.0, 0.0, 1.0)
    glBegin(GL_LINES)
    glVertex2f(-2000, 0)
    glVertex2f(2000, 0)
    glEnd()
    glPopMatrix()
