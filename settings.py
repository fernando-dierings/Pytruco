
# Configurações gerais do jogo
from pathlib import Path
import pygame


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

CAMINHO_LOGO = PASTA_IMAGENS / "logo_pytruco6.png"
CAMINHO_LOGO_PLACA= PASTA_IMAGENS / "logo_pytruco_placa2.png"
CAMINHO_FUNDO_MENU = PASTA_IMAGENS / "fundo_menu4.png"
CAMINHO_FUNDO_PARTIDA = PASTA_IMAGENS / "fundo_partida.png"
CAMINHO_FUNDO_PARTIDA2 = PASTA_IMAGENS / "fundo_partida2.png"
CAMINHO_TELA_CARREGAMENTO = PASTA_IMAGENS / "tela_gaucho_animada.gif"
CAMINHO_TELA_DERROTA = PASTA_IMAGENS / "tela_derrota.png"
CAMINHO_TELA_VITORIA = PASTA_IMAGENS / "tela_vitoria.png"
CAMINHO_BOTAO = PASTA_IMAGENS / "botao1.png"
CAMINHO_VERSO_CARTA = PASTA_CARTAS / "verso_carta.png"

CAMINHO_MUSICA_MENU = PASTA_SONS / "musica_menu.mp3"
CAMINHO_MUSICA_PARTIDA = PASTA_SONS / "musica_partida.mp3"
CAMINHO_MUSICA_VITORIA = PASTA_SONS / "musica_vitoria.mp3"
CAMINHO_MUSICA_DERROTA = PASTA_SONS / "musica_derrota.mp3"

CAMINHO_SOM_TOQUE = PASTA_SONS / "touching_card.mp3"
CAMINHO_SOM_CARTA_JOGADOR = PASTA_SONS / "card_place1.mp3"
CAMINHO_SOM_CARTA_COMPUTADOR = PASTA_SONS / "card_place2.mp3"
SOM_TRUCO_NOTIFICACAO = PASTA_SONS / "truco_notificacao.mp3"

CAMINHO_SOM_ROLLOVER = PASTA_SONS / "rollover1.mp3"
CAMINHO_SOM_CLICK = PASTA_SONS / "click1.mp3"

CAMINHO_VOZ_DERROTA = "assets/sons/voz_derrota.mp3"
CAMINHO_VOZ_DERROTA_1 = "assets/sons/voz_derrota1.mp3"
CAMINHO_VOZ_DERROTA_2 = "assets/sons/voz_derrota2.mp3"

CAMINHO_VOZ_VITORIA = "assets/sons/voz_vitoria.mp3"
CAMINHO_VOZ_VITORIA_1 = "assets/sons/voz_vitoria1.mp3"
CAMINHO_VOZ_VITORIA_2 = "assets/sons/voz_vitoria2.mp3"

CAMINHO_VOZ_CARREGAMENTO = "assets/sons/voz_carregamento.mp3"

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
AMARELO = (255, 215, 0)

# ==================================================
# CORES (RGB)
# ==================================================
COR_CONTORNO = PRETO
ESPESSURA_CONTORNO = 3


# ==================================================
# CONFIGURAÇÕES DE CONTORNO
# ==================================================


PONTOS_PARA_VENCER = 12
CARTAS_POR_JOGADOR = 3



