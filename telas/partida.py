import pygame

from settings import (
    LARGURA,
    ALTURA,
    VERDE_MESA,
    BRANCO,
    DOURADO,
    PONTOS_PARA_VENCER,
)
from logica.partida import Partida


def desenhar_carta(tela, carta, x, y, largura=100, altura=145):
    retangulo = pygame.Rect(x, y, largura, altura)

    pygame.draw.rect(tela, BRANCO, retangulo, border_radius=8)
    pygame.draw.rect(tela, (30, 30, 30), retangulo, 2, border_radius=8)

    fonte = pygame.font.Font(None, 30)
    texto = fonte.render(str(carta["valor"]), True, (20, 20, 20))
    tela.blit(texto, (x + 10, y + 10))

    naipes = {
        "Copas": "♥",
        "Ouros": "♦",
        "Espadas": "♠",
        "Bastos": "♣",
    }

    cor = (
        (190, 30, 30)
        if carta["naipe"] in ("Copas", "Ouros")
        else (20, 20, 20)
    )

    fonte_naipe = pygame.font.Font(None, 40)
    simbolo = fonte_naipe.render(naipes[carta["naipe"]], True, cor)
    tela.blit(simbolo, simbolo.get_rect(center=retangulo.center))

    return retangulo


def iniciar_partida(tela, relogio):
    partida = Partida()

    fonte = pygame.font.Font(None, 32)
    fonte_pequena = pygame.font.Font(None, 25)

    carta_jogador = None
    carta_computador = None
    mensagem = "Clique em uma carta para jogar."
    aguardando_proxima = False
    encerrada = False
    executando = True

    while executando:
        quantidade = len(partida.jogador.cartas)
        espacamento = 120
        inicio_x = (LARGURA - quantidade * espacamento) // 2

        botoes_cartas = []

        for indice, carta in enumerate(partida.jogador.cartas):
            x = inicio_x + indice * espacamento
            botoes_cartas.append(pygame.Rect(x, 410, 100, 145))

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return "sair"

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    return "menu"

            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                if encerrada:
                    partida = Partida()
                    carta_jogador = None
                    carta_computador = None
                    mensagem = "Nova partida! Clique em uma carta."
                    aguardando_proxima = False
                    encerrada = False
                    continue

                if aguardando_proxima:
                    if partida.partida_encerrada():
                        encerrada = True
                        mensagem = (
                            "Voce venceu! Clique para nova partida."
                            if partida.pontos_jogador >= PONTOS_PARA_VENCER
                            else "Computador venceu! Clique para jogar novamente."
                        )

                    elif not partida.jogador.tem_cartas():
                        partida.nova_mao()
                        carta_jogador = None
                        carta_computador = None
                        mensagem = "Nova mao! Clique em uma carta."

                    else:
                        carta_jogador = None
                        carta_computador = None
                        mensagem = "Clique em uma carta para jogar."

                    aguardando_proxima = False
                    continue

                for indice, retangulo in enumerate(botoes_cartas):
                    if retangulo.collidepoint(evento.pos):
                        resultado = partida.jogar_rodada(indice)

                        if isinstance(resultado, dict):
                            carta_jogador = resultado["carta_jogador"]
                            carta_computador = resultado["carta_computador"]

                            if resultado["vencedor_mao"] == "jogador":
                                mensagem = "Voce venceu a mao! Clique para continuar."

                            elif resultado["vencedor_mao"] == "computador":
                                mensagem = "Computador venceu a mao! Clique para continuar."

                            elif resultado["vencedor_mao"] == "empate":
                                mensagem = "Mao empatada! Clique para continuar."

                            elif resultado["resultado"] == "jogador":
                                mensagem = "Voce venceu a rodada! Clique para continuar."

                            elif resultado["resultado"] == "computador":
                                mensagem = "Computador venceu a rodada! Clique para continuar."

                            else:
                                mensagem = "Rodada empatada! Clique para continuar."

                            aguardando_proxima = True
                        else:
                            mensagem = resultado

                        break

        # Desenha a mesa
        tela.fill(VERDE_MESA)

        titulo = fonte.render("PYTRUCO", True, DOURADO)
        tela.blit(titulo, titulo.get_rect(center=(LARGURA // 2, 35)))

        placar = fonte_pequena.render(
            f"Voce: {partida.pontos_jogador}  |  "
            f"Computador: {partida.pontos_computador}",
            True,
            BRANCO,
        )
        tela.blit(placar, placar.get_rect(center=(LARGURA // 2, 80)))

        # Posições centrais das duas cartas jogadas
        centro_jogador = LARGURA // 2 - 70
        centro_computador = LARGURA // 2 + 70

        # Cada título fica centralizado sobre sua carta
        texto_jogador_jogado = fonte_pequena.render(
            "SUA CARTA", True, BRANCO
        )
        tela.blit(
            texto_jogador_jogado,
            texto_jogador_jogado.get_rect(
                center=(centro_jogador, 145)
            ),
        )

        texto_cpu = fonte_pequena.render(
            "COMPUTADOR", True, BRANCO
        )
        tela.blit(
            texto_cpu,
            texto_cpu.get_rect(
                center=(centro_computador, 145)
            ),
        )

        # Mostra as duas cartas jogadas lado a lado
        if carta_jogador and carta_computador:
            desenhar_carta(
                tela,
                carta_jogador,
                centro_jogador - 50,
                165,
            )

            desenhar_carta(
                tela,
                carta_computador,
                centro_computador - 50,
                165,
            )

        # Cartas que ainda estão na mão do jogador
        texto_mao = fonte_pequena.render(
            "SUAS CARTAS", True, BRANCO
        )
        tela.blit(
            texto_mao,
            texto_mao.get_rect(center=(LARGURA // 2, 370)),
        )

        for indice, carta in enumerate(partida.jogador.cartas):
            x = inicio_x + indice * espacamento

            desenhar_carta(
                tela,
                carta,
                x,
                410
            )

        texto_mensagem = fonte_pequena.render(
            mensagem, True, DOURADO
        )
        tela.blit(
            texto_mensagem,
            texto_mensagem.get_rect(center=(LARGURA // 2, 610)),
        )

        ajuda = fonte_pequena.render(
            "ESC: voltar ao menu", True, BRANCO
        )
        tela.blit(
            ajuda,
            ajuda.get_rect(center=(LARGURA // 2, 665)),
        )

        pygame.display.flip()
        relogio.tick(60)

