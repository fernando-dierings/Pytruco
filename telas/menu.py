import pygame

from settings import (
    LARGURA,
    ALTURA,
    TITULO,
    FPS,
    VERDE_MESA,
    BRANCO,
    DOURADO,
    CAMINHO_FONTE
)
from telas.partida import iniciar_partida


def desenhar_botao(tela, texto, retangulo, fonte, mouse_pos):
    cor = DOURADO if retangulo.collidepoint(mouse_pos) else BRANCO

    pygame.draw.rect(tela, cor, retangulo, 2, border_radius=8)

    superficie = fonte.render(texto, True, cor)
    tela.blit(superficie, superficie.get_rect(center=retangulo.center))


def mostrar_regras(tela, fonte_titulo, fonte_texto):
    tela.fill(VERDE_MESA)

    titulo = fonte_titulo.render("COMO JOGAR", True, DOURADO)
    tela.blit(titulo, titulo.get_rect(center=(LARGURA // 2, 120)))

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
            linha.get_rect(center=(LARGURA // 2, 230 + indice * 45)),
        )


def iniciar_jogo():
    pygame.init()

    tela = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption(TITULO)

    relogio = pygame.time.Clock()

    fonte_titulo = pygame.font.Font(CAMINHO_FONTE, 28)
    fonte_botao = pygame.font.Font(CAMINHO_FONTE, 12)
    fonte_texto = pygame.font.Font(CAMINHO_FONTE, 9)

    botao_jogar = pygame.Rect(LARGURA // 2 - 190, 290, 380, 60)
    botao_regras = pygame.Rect(LARGURA // 2 - 190, 370, 380, 60)
    botao_sair = pygame.Rect(LARGURA // 2 - 190, 450, 380, 60)

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
            tela.fill(VERDE_MESA)

            titulo = fonte_titulo.render("PYTRUCO", True, DOURADO)
            tela.blit(
                titulo,
                titulo.get_rect(center=(LARGURA // 2, 180)),
            )

            desenhar_botao(tela, "JOGAR", botao_jogar, fonte_botao, mouse_pos)
            desenhar_botao(tela, "COMO JOGAR", botao_regras, fonte_botao, mouse_pos)
            desenhar_botao(tela, "SAIR", botao_sair, fonte_botao, mouse_pos)

        elif tela_atual == "regras":
            mostrar_regras(tela, fonte_titulo, fonte_texto)

        pygame.display.flip()
        relogio.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    iniciar_jogo()
