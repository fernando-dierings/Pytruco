import pygame

from pathlib import Path

from settings import (
    LARGURA,
    ALTURA,
    TITULO,
    FPS,
    VERDE_MESA,
    BRANCO,
    DOURADO,
    CAMINHO_FONTE,
)
from telas.partida import iniciar_partida


# Caminho da imagem de fundo
CAMINHO_FUNDO = (
    Path(__file__).resolve().parent.parent
    / "assets"
    / "imagens"
    / "fundo_menu.png"
)


def carregar_fundo():
    if not CAMINHO_FUNDO.exists():
        print(f"Imagem de fundo não encontrada: {CAMINHO_FUNDO}")
        return None

    imagem = pygame.image.load(str(CAMINHO_FUNDO))
    return pygame.transform.scale(imagem, (LARGURA, ALTURA))


def desenhar_botao(tela, texto, retangulo, fonte, mouse_pos):
    selecionado = retangulo.collidepoint(mouse_pos)

    cor = DOURADO if selecionado else BRANCO
    cor_fundo = (65, 35, 25) if selecionado else (25, 35, 22)

    # Fundo e contorno do botão
    pygame.draw.rect(tela, cor_fundo, retangulo, border_radius=5)
    pygame.draw.rect(tela, cor, retangulo, 2, border_radius=5)

    superficie = fonte.render(texto, True, cor)
    tela.blit(superficie, superficie.get_rect(center=retangulo.center))


def mostrar_regras(tela, fonte_titulo, fonte_texto, fundo):
    if fundo:
        tela.blit(fundo, (0, 0))
    else:
        tela.fill(VERDE_MESA)

    painel = pygame.Surface((700, 470), pygame.SRCALPHA)
    painel.fill((15, 30, 18, 225))
    tela.blit(painel, painel.get_rect(center=(LARGURA // 2, ALTURA // 2)))

    titulo = fonte_titulo.render("COMO JOGAR", True, DOURADO)
    tela.blit(titulo, titulo.get_rect(center=(LARGURA // 2, 180)))

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
        linha = fonte_texto.render(texto, True, BRANCO)
        tela.blit(
            linha,
            linha.get_rect(center=(LARGURA // 2, 260 + indice * 38)),
        )


def iniciar_jogo():
    pygame.init()

    tela = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption(TITULO)

    relogio = pygame.time.Clock()

    fonte_titulo = pygame.font.Font(CAMINHO_FONTE, 36)
    fonte_botao = pygame.font.Font(CAMINHO_FONTE, 14)
    fonte_texto = pygame.font.Font(CAMINHO_FONTE, 12)

    fundo_menu = carregar_fundo()

    # Posições dos botões
    botao_jogar = pygame.Rect(LARGURA // 2 - 150, 330, 300, 55)
    botao_regras = pygame.Rect(LARGURA // 2 - 150, 405, 300, 55)
    botao_sair = pygame.Rect(LARGURA // 2 - 150, 480, 300, 55)

    tela_atual = "menu"
    executando = True

    while executando:
        mouse_pos = pygame.mouse.get_pos()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                executando = False

            elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
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
                if evento.key == pygame.K_ESCAPE and tela_atual == "regras":
                    tela_atual = "menu"

        if tela_atual == "menu":
            # Desenha o fundo
            if fundo_menu:
                tela.blit(fundo_menu, (0, 0))
            else:
                tela.fill(VERDE_MESA)

            # Painel central translúcido
            painel = pygame.Surface((430, 430), pygame.SRCALPHA)
            painel.fill((15, 30, 18, 205))
            tela.blit(
                painel,
                painel.get_rect(center=(LARGURA // 2, 390)),
            )

            # Título
            titulo = fonte_titulo.render("PYTRUCO", True, DOURADO)
            sombra = fonte_titulo.render("PYTRUCO", True, (25, 20, 12))

            tela.blit(
                sombra,
                sombra.get_rect(center=(LARGURA // 2 + 3, 245 + 3)),
            )
            tela.blit(
                titulo,
                titulo.get_rect(center=(LARGURA // 2, 245)),
            )

            # Botões
            desenhar_botao(
                tela, "JOGAR", botao_jogar, fonte_botao, mouse_pos
            )
            desenhar_botao(
                tela, "COMO JOGAR", botao_regras, fonte_botao, mouse_pos
            )
            desenhar_botao(
                tela, "SAIR", botao_sair, fonte_botao, mouse_pos
            )

        elif tela_atual == "regras":
            mostrar_regras(
                tela, fonte_titulo, fonte_texto, fundo_menu
            )

        pygame.display.flip()
        relogio.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    iniciar_jogo()
