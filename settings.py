
# Configurações gerais do jogo
from pathlib import Path


# ==================================================
# CAMINHOS DO PROJETO
# ==================================================

RAIZ_PROJETO = Path(__file__).resolve().parent

PASTA_ASSETS = RAIZ_PROJETO / "assets"
PASTA_IMAGENS = PASTA_ASSETS / "imagens"
PASTA_FONTES = PASTA_ASSETS / "fontes"
PASTA_SONS = PASTA_ASSETS / "sons"
PASTA_CARTAS = PASTA_ASSETS / "cartas"


# ==================================================
# CAMINHOS DOS RECURSOS
# ==================================================

CAMINHO_FONTE = (
    PASTA_FONTES
    / "Press_Start_2P"
    / "PressStart2P-Regular.ttf"
)

CAMINHO_LOGO = PASTA_IMAGENS / "logo_pytruco.png"
CAMINHO_FUNDO_MENU = PASTA_IMAGENS / "fundo_menu.png"
CAMINHO_FUNDO_PARTIDA = PASTA_IMAGENS / "fundo_partida.png"
CAMINHO_TELA_VITORIA = PASTA_IMAGENS / "tela_vitoria.png"
CAMINHO_BOTAO = PASTA_IMAGENS / "botao1.png"


# ==================================================
# CONFIGURAÇÕES DA JANELA
# ==================================================

LARGURA = 1000
ALTURA = 700
TITULO = "PYTRUCO"
FPS = 60


# ==================================================
# CORES (RGB)
# ==================================================

VERDE_MESA = (35, 110, 65)
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERMELHO = (200, 40, 40)
DOURADO = (230, 190, 80)


# ==================================================
# CONFIGURAÇÕES DA PARTIDA
# ==================================================

PONTOS_PARA_VENCER = 12
CARTAS_POR_JOGADOR = 3



