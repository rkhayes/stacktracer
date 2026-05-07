# STACKTRACER
Stacktracer é um puzzle game educativo baseado em texto e gráficos 2D minimalistas, renderizado com PyOpenGL e GLFW. A estética do jogo emula monitores CRT monocromáticos (fósforo verde) de mainframes antigos.

## STACKTRACER // MINIGAME 01: Linear Classifier
Regressão Linear: O objetivo é encontrar a melhor linha de ajuste para um conjunto de dados bidimensional. A reta obedece à equação fundamental $y = wx + b$, onde $w$ é o Peso (rotação/inclinação) e $b$ é o Viés (translação vertical).

O jogo possui um Sistema de Progressão contendo 3 setores de memória (fases). Cada fase injeta um novo dataset com distribuições de dados variadas (tendência positiva, negativa e íngreme).

### Função de Perda (Loss Function)
O terminal inferior exibe em tempo real o cálculo do erro do jogador usando duas métricas:
- **MSE (Mean Squared Error):** Calcula a média dos quadrados das diferenças verticais entre os pontos reais e a predição da reta.
- **Distância Euclidiana Ortogonal:** Calcula a distância mais curta (perpendicular) entre cada ponto e a reta atual.

### Otimização e Condição de Vitória (OLS)
O jogo utiliza o método dos Mínimos Quadrados Ordinários (Ordinary Least Squares) para calcular matematicamente a reta perfeita no momento em que a fase é carregada. Para vencer, o MSE do jogador deve atingir um limite de tolerância aceitável (2.5x o MSE ótimo), ensinando que modelos de ML buscam generalização satisfatória, e não necessariamente precisão absoluta (overfitting).

### Interface
- **Top Panel (Viewport Visual - 70%):** Exibe a representação espacial dos dados normalizados. Os pontos e a reta escalam dinamicamente com a resolução da janela.
- **Bottom Panel (Terminal Log - 30%):** Renderiza texto customizado usando uma matriz de fontes construída do zero com quadriláteros (`GL_QUADS`). Exibe a sequência de boot e os valores de perda em tempo real.

### Modelagem
- **Espaço de Coordenadas:** Utiliza coordenadas normalizadas ($0.0$ a $1.0$) para os datasets, facilitando a portabilidade entre resoluções, com conversão para o espaço de pixels apenas no cálculo de erro e renderização.
- **A Reta (O Modelo):** Definida por um par ordenado de translação e um escalar de rotação ($line\_angle$), permitindo que o jogador a manipule como um objeto físico.

#### SRO (Sistema de Referência do Objeto)
- `DATASETS`, `load_stage`: Repositório de níveis e reset de estado.
- `calculate_current_metrics`: Cálculo geométrico puro (MSE e Distância Euclidiana).
- `get_optimal_mse`, `verify_solution`: Validação da solução baseada em limites teóricos de regressão.
- `process_input`: Mapeamento de comandos para alterações incrementais.

#### SRU (Sistema de Referência do Universo)
A Unidade Unificada é o Pipeline de Feedback Visual. Integra os estados lógicos em uma interface coesa:
- A função `get_metrics_string` unifica os cálculos de erro em telemetria de sistema operacional.
- Desenho dos pontos (loops circulares) e da reta utilizando `glTranslatef` e `glRotatef`.

### Controles
- **↑ / ↓:** Aumenta/Diminui o Viés (Bias). Translada a reta verticalmente.
- **← / →:** Altera o Peso (Weight). Rotaciona a reta.
- **SPACE:** Submeter Calibração (Validação OLS).
- **ENTER:** Próximo Setor (Avança após validação).

---

## STACKTRACER // MINIGAME 02: Logic Trees
**Binary Search Tree (Fase 1):** O objetivo é organizar uma estrutura de dados de árvore binária de busca. Todos os elementos visuais são desenhados programaticamente através de vértices geométricos, sem o uso de imagens prontas.

### Renderização de Componentes
- **Hexágonos (Nodos):** O formato hexagonal é calculado via trigonometria (seno e cosseno), gerando 6 pontos ao redor de um centro. Utiliza `GL_POLYGON` para preenchimento e `GL_LINE_LOOP` para a borda.
- **Números (Dados):** Modelados do zero como displays de 7 segmentos usando linhas (`GL_LINES`) para imitar o visual de dispositivos digitais antigos.

### Interface e Proporção
- **Correção de Aspecto:** Como a janela é retangular (800x600) e o universo OpenGL é quadrado (-1 a 1), a Matriz de Projeção é ajustada via `glOrtho`. O sistema calcula a proporção da tela e expande as bordas do eixo X, garantindo que as formas geométricas mantenham proporções perfeitas.

### Mecânica de Progressão (Auto-Targeting)
A lógica de seleção manual foi substituída por um sistema de progressão automática de nós (Auto-Targeting) para reforçar a regra de inserção de uma Árvore Binária de Busca. O sistema gerencia uma sequência rigorosa de calibração baseada em valores (`30, 20, 40, 60, 80, 70`). Quando o jogador alinha um nó perfeitamente com seu alvo correspondente, a posição do nó é fixada na estrutura da árvore, e o sistema transfere o controle automaticamente para a próxima peça corrompida na memória.

### Modelagem
#### SRO (Sistema de Referência do Objeto)
Cada hexágono ou número é desenhado na coordenada (0,0), seu próprio centro geométrico. Isso permite aplicar transformações de escala e rotação local sem distorcer o resto da tela. O estado do sistema é preservado com `glPushMatrix()` e restaurado com `glPopMatrix()` após o desenho de cada peça.

#### SRU (Sistema de Referência do Universo)
As coordenadas do SRU são utilizadas para o gerenciamento de posicionamento global e movimentação das peças pelo cenário, garantindo que a distância entre os nodos da árvore seja exata.

### Controles
- **Setas do Teclado (↑ ↓ ← →):** Translação (Move a peça ativa livremente pelo cenário no SRU).
- **W / S:** Ajusta a Escala (Aumenta ou diminui a peça ativa).
- **Q / E:** Ajusta a Rotação (Gira a peça ativa em torno de seu próprio eixo).
- **SPACE:** Submeter Calibração (Valida a posição atual do nó ativo. Em caso de sucesso, aciona o travamento do eixo e o pulo automático para o próximo alvo).
