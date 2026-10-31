
from pathlib import Path
import pygame

from settings import (
    LARGURA,
    ALTURA,
    TITULO,
    FPS,
    VERDE_MESA,
    BRANCO,
    DOURADO,
    CAMINHO_FONTE,
    CAMINHO_LOGO,
    CAMINHO_FUNDO_MENU,
    CAMINHO_BOTAO
)
from telas.partida import iniciar_partida

# ==================================================
# CARREGAMENTO DAS IMAGENS
# ==================================================

def carregar_logo():
    if not CAMINHO_LOGO.exists():
        print(f"Logo não encontrada: {CAMINHO_LOGO}")
        return None

    imagem = pygame.image.load(str(CAMINHO_LOGO)).convert_alpha()

    # Mantém a proporção original da logo.
    largura_original, altura_original = imagem.get_size()
    largura = 560
    altura = int(altura_original * largura / largura_original)

    return pygame.transform.scale(imagem, (largura, altura))


def carregar_fundo():
    if not CAMINHO_FUNDO_MENU.exists():
        print(f"Imagem de fundo não encontrada: {CAMINHO_FUNDO_MENU}")
        return None

    imagem = pygame.image.load(str(CAMINHO_FUNDO_MENU))
    return pygame.transform.scale(imagem, (LARGURA, ALTURA))

def carregar_imagem_botao():
    if not CAMINHO_BOTAO.exists():
        print(f"Botão não encontrado: {CAMINHO_BOTAO}")
        return None

    return pygame.image.load(
        str(CAMINHO_BOTAO)
    ).convert_alpha()

# ==================================================
# BOTÕES
# ==================================================

def desenhar_botao(
    tela, texto, retangulo, fonte, mouse_pos, imagem_botao
):
    selecionado = retangulo.collidepoint(mouse_pos)

    if imagem_botao:
        imagem = pygame.transform.scale(
            imagem_botao,
            retangulo.size,
        )
        tela.blit(imagem, retangulo)

    else:
        cor = DOURADO if selecionado else BRANCO
        cor_fundo = (
            (85, 50, 25) if selecionado else (25, 35, 22)
        )

        pygame.draw.rect(
            tela, cor_fundo, retangulo, border_radius=5
        )
        pygame.draw.rect(
            tela, cor, retangulo, 2, border_radius=5
        )

    cor_texto = DOURADO if selecionado else BRANCO
    superficie = fonte.render(texto, True, cor_texto)

    tela.blit(
        superficie,
        superficie.get_rect(center=retangulo.center),
    )

# ==================================================
# TELA DE REGRAS
# ==================================================

def mostrar_regras(tela, fonte_titulo, fonte_texto, fundo):
    if fundo:
        tela.blit(fundo, (0, 0))
    else:
        tela.fill(VERDE_MESA)

    painel = pygame.Surface((700, 470), pygame.SRCALPHA)
    painel.fill((15, 30, 18, 225))

    tela.blit(
        painel,
        painel.get_rect(
            center=(LARGURA // 2, ALTURA // 2)
        ),
    )

    titulo = fonte_titulo.render(
        "COMO JOGAR",
        True,
        DOURADO,
    )

    tela.blit(
        titulo,
        titulo.get_rect(center=(LARGURA // 2, 180)),
    )

    instrucoes = [
        "Receba tres cartas.",
        "Clique em uma carta para jogar.",
        "O computador sera seu adversario.",
        "Cada rodada pode valer um ponto.",
        "O primeiro a chegar a 12 pontos vence.",
        "",
        "Pressione ESC para voltar ao menu.",
    ]

    for indice, texto in enumerate(instrucoes):
        linha = fonte_texto.render(
            texto,
            True,
            BRANCO,
        )

        tela.blit(
            linha,
            linha.get_rect(
                center=(LARGURA // 2, 260 + indice * 38)
            ),
        )


# ==================================================
# MENU PRINCIPAL
# ==================================================

def iniciar_jogo():
    pygame.init()

    tela = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption(TITULO)

    relogio = pygame.time.Clock()

    fonte_botao = pygame.font.Font(CAMINHO_FONTE, 14)
    fonte_titulo = pygame.font.Font(CAMINHO_FONTE, 36)
    fonte_texto = pygame.font.Font(CAMINHO_FONTE, 12)

    # Carregar imagens.
    logo = carregar_logo()
    fundo_menu = carregar_fundo()
    imagem_botao = carregar_imagem_botao()

    # Posições dos botões.
    botao_jogar = pygame.Rect(
        LARGURA // 2 - 150, 330, 300, 55
    )

    botao_regras = pygame.Rect(
        LARGURA // 2 - 150, 405, 300, 55
    )

    botao_sair = pygame.Rect(
        LARGURA // 2 - 150, 480, 300, 55
    )

    tela_atual = "menu"
    executando = True

    while executando:
        mouse_pos = pygame.mouse.get_pos()

        # ------------------------------------------
        # EVENTOS
        # ------------------------------------------

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                executando = False

            elif (
                evento.type == pygame.MOUSEBUTTONDOWN
                and evento.button == 1
            ):
                if tela_atual == "menu":

                    if botao_jogar.collidepoint(evento.pos):
                        resultado = iniciar_partida(tela, relogio)

                        if resultado == "sair":
                            executando = False

                    elif botao_regras.collidepoint(evento.pos):
                        tela_atual = "regras"

                    elif botao_sair.collidepoint(evento.pos):
                        executando = False

            elif evento.type == pygame.KEYDOWN:
                if (
                    evento.key == pygame.K_ESCAPE
                    and tela_atual == "regras"
                ):
                    tela_atual = "menu"

        # ------------------------------------------
        # DESENHAR MENU
        # ------------------------------------------

        if tela_atual == "menu":

            if fundo_menu:
                tela.blit(fundo_menu, (0, 0))
            else:
                tela.fill(VERDE_MESA)

            # Logo do PYTRUCO.
            if logo:
                tela.blit(
                    logo,
                    logo.get_rect(
                        center=(LARGURA // 2, 230)
                    ),
                )
            else:
                # Título alternativo caso a logo não exista.
                titulo = fonte_titulo.render(
                    "PYTRUCO",
                    True,
                    DOURADO,
                )

                tela.blit(
                    titulo,
                    titulo.get_rect(
                        center=(LARGURA // 2, 230)
                    ),
                )

            # Botões.
            # Botões
            desenhar_botao(
                tela, "JOGAR", botao_jogar,
                fonte_botao, mouse_pos, imagem_botao
            )

            desenhar_botao(
                tela, "COMO JOGAR", botao_regras,
                fonte_botao, mouse_pos, imagem_botao
            )

            desenhar_botao(
                tela, "SAIR", botao_sair,
                fonte_botao, mouse_pos, imagem_botao
            )

        # ------------------------------------------
        # DESENHAR REGRAS
        # ------------------------------------------

        elif tela_atual == "regras":
            mostrar_regras(
                tela,
                fonte_titulo,
                fonte_texto,
                fundo_menu,
            )

        pygame.display.flip()
        relogio.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    iniciar_jogo()

