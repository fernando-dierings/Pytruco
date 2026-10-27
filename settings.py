# Configurações gerais do jogo
from pathlib import Path

# Assets
RAIZ_PROJETO = Path(__file__).resolve().parent.parent
CAMINHO_FONTE = "assets/fontes/Press_Start_2P/PressStart2P-Regular.ttf" #Fonte do jogo

CAMINHO_LOGO = (
    RAIZ_PROJETO
    / "assets"
    / "imagens"
    / "logo_pytruco.png") # Logo do Pytruco


# Configurações da janela
LARGURA = 1000
ALTURA = 700
TITULO = "PYTRUCO"
FPS = 60

# Cores (RGB)
VERDE_MESA = (35, 110, 65)
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERMELHO = (200, 40, 40)
DOURADO = (230, 190, 80)

# Configurações da partida
PONTOS_PARA_VENCER = 12
CARTAS_POR_JOGADOR = 3


