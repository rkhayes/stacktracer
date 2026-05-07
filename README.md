# STACKTRACER
Stacktracer é um puzzle game educativo baseado em texto e gráficos 2D minimalistas, renderizado com PyOpenGL e GLFW. A estética do jogo emula monitores CRT monocromáticos (fósforo verde) de mainframes antigos.

## STACKTRACER // MINIGAME 01: Linear Classifier
Regressão Linear: O objetivo é encontrar a melhor linha de ajuste para um conjunto de dados bidimensional. A reta obedece à equação fundamental $y = wx + b$, onde $w$ é o Peso (rotação/inclinação) e $b$ é o Viés (translação vertical).

O jogo possui um Sistema de Progressão contendo 3 setores de memória (fases). Cada fase injeta um novo dataset com distribuições de dados variadas (tendência positiva, negativa e íngreme).

### Função de Perda (Loss Function)
O terminal inferior exibe em tempo real o cálculo do erro do jogador usando duas métricas:
- MSE (Mean Squared Error): Calcula a média dos quadrados das diferenças verticais entre os pontos reais e a predição da reta.
- Distância Euclidiana Ortogonal: Calcula a distância mais curta (perpendicular) entre cada ponto e a reta atual.

### Otimização e Condição de Vitória (OLS)
O jogo utiliza o método dos Mínimos Quadrados Ordinários (Ordinary Least Squares) para calcular matematicamente a reta perfeita no momento em que a fase é carregada. Para vencer, o MSE do jogador deve atingir um limite de tolerância aceitável (2.5x o MSE ótimo), ensinando que modelos de ML buscam generalização satisfatória, e não necessariamente precisão absoluta (overfitting).

### Interface
- Top Panel (Viewport Visual - 70%): Exibe a representação espacial dos dados normalizados. Os pontos e a reta escalam dinamicamente com a resolução da janela, mantendo a precisão visual e matemática.
- Bottom Panel (Terminal Log - 30%): Renderiza texto customizado usando uma matriz de fontes construída do zero com quadriláteros (GL_QUADS). Ele exibe a sequência de boot do sistema e atualiza os valores de perda (Loss) a cada frame.

### Modelagem
- Espaço de Coordenadas: O sistema utiliza coordenadas normalizadas ($0.0$ a $1.0$) para os datasets, facilitando a portabilidade entre diferentes resoluções de tela, com conversão para o espaço de pixels (abs_cx, abs_cy) apenas no momento do cálculo de erro e renderização.
- A Reta (O Modelo): Ao contrário de uma regressão linear tradicional definida por $y = ax + b$, aqui o modelo é definido por um par ordenado de translação e um escalar de rotação ($line\_angle$). Isso permite que o jogador manipule a reta como um objeto físico no espaço 2D.

#### SRO
- `DATASETS`, `load_stage`: Atuam como o repositório de níveis. Sua única responsabilidade é fornecer a distribuição de pontos e resetar o estado do ambiente.
- `calculate_current_metrics`: Responsável estritamente pelo cálculo geométrico. Ele transforma o ângulo e a posição da reta em coeficientes lineares para medir o MSE e a distância euclidiana ortogonal.
- `get_optimal_mse`, `verify_solution`: Contém a "inteligência" do jogo. Ele decide se o esforço do jogador é estatisticamente aceitável comparando o MSE atual com o limite teórico.
- `process_input`: Mapeia os comandos do teclado para alterações incrementais no estado da reta.

#### SRU
A Unidade Unificada é o Pipeline de Feedback Visual. Ela integra os estados lógicos em uma interface coesa de terminal 2D:
- A função get_metrics_string unifica os cálculos de erro em uma string formatada que simula a telemetria de um sistema operacional.
- Utiliza o estado global para desenhar os pontos (como loops de linhas circulares) e a reta (utilizando transformações de matriz glTranslatef e glRotatef). A mudança de cor para 0.5, 1.0, 0.5 ao vencer serve como o sinalizador visual de convergência do modelo.

### Controles
O jogador interage diretamente com as variáveis da equação linear através do teclado:
- ↑ Seta para Cima: Aumenta o Viés (Bias). Translada a reta para cima.
- ↓ Seta para Baixo: Diminui o Viés (Bias). Translada a reta para baixo.
- ← Seta para Esquerda: Altera o Peso (Weight). Rotaciona a reta no sentido anti-horário em torno do seu centroide.
- → Seta para Direita: Altera o Peso (Weight). Rotaciona a reta no sentido horário.
- SPACE: Submeter Calibração. Aciona o cálculo de verificação (Validação OLS). Se o erro for baixo o suficiente, o módulo é destravado.
- ENTER: Próximo Setor. Avança para a próxima fase após submeter uma calibração válida.
