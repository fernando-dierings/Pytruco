import pygame

from settings import COR_CONTORNO, ESPESSURA_CONTORNO


def desenhar_texto_contornado(
    tela,
    fonte,
    texto,
    cor_texto,
    posicao,
    cor_contorno=COR_CONTORNO,
    espessura=ESPESSURA_CONTORNO
):
    # Renderiza o texto principal
    texto_renderizado = fonte.render(texto, True, cor_texto)

    # Define a posição centralizada
    retangulo = texto_renderizado.get_rect(center=posicao)

    # Renderiza o contorno
    contorno = fonte.render(texto, True, cor_contorno)

    # Desenha o contorno ao redor do texto
    for dx in range(-espessura, espessura + 1):
        for dy in range(-espessura, espessura + 1):
            if dx != 0 or dy != 0:
                tela.blit(contorno, retangulo.move(dx, dy))

    # Desenha o texto principal por cima
    tela.blit(texto_renderizado, retangulo)

    return retangulo