
import pygame
from pathlib import Path

from settings import (
    LARGURA,
    ALTURA,
    BRANCO,
    DOURADO,
    PONTOS_PARA_VENCER,
    CAMINHO_FONTE,
)

from logica.partida import Partida


# ==================================================
# CAMINHOS E CONFIGURAÇÕES
# ==================================================

RAIZ_PROJETO = Path(__file__).resolve().parent.parent
PASTA_CARTAS = RAIZ_PROJETO / "assets" / "cartas"
PASTA_IMAGENS = RAIZ_PROJETO / "assets" / "imagens"

CAMINHO_FUNDO = PASTA_IMAGENS / "fundo_partida.png"
CAMINHO_VITORIA = PASTA_IMAGENS / "tela_vitoria.png"

NAIPES_ARQUIVOS = {
    "Copas": ("copas", "copas"),
    "Bastos": ("bastos", "bastos"),
    "Ouros": ("ouros", "oro"),
    "Espadas": ("espadas", "espadas"),
}

VALORES_CARTAS = [1, 2, 3, 4, 5, 6, 7, 10, 11, 12]


# ==================================================
# CARREGAMENTO DAS IMAGENS
# ==================================================

def carregar_imagens_cartas():
    imagens = {}

    for naipe, (pasta, prefixo) in NAIPES_ARQUIVOS.items():
        for valor in VALORES_CARTAS:
            caminho = PASTA_CARTAS / pasta / f"{prefixo}{valor}.png"

            if not caminho.exists():
                print(f"Imagem não encontrada: {caminho}")
                continue

            imagem = pygame.image.load(str(caminho))
            imagens[(valor, naipe)] = imagem

    return imagens


def carregar_imagem(caminho):
    if not caminho.exists():
        print(f"Imagem não encontrada: {caminho}")
        return None

    imagem = pygame.image.load(str(caminho))
    return pygame.transform.scale(imagem, (LARGURA, ALTURA))


def carregar_fundo():
    return carregar_imagem(CAMINHO_FUNDO)


def carregar_tela_vitoria():
    return carregar_imagem(CAMINHO_VITORIA)


# ==================================================
# DESENHO DAS CARTAS
# ==================================================

def desenhar_carta(
    tela, carta, x, y, imagens, largura=100, altura=145
):
    retangulo = pygame.Rect(x, y, largura, altura)

    chave = (carta["valor"], carta["naipe"])
    imagem = imagens.get(chave)

    if imagem:
        imagem_redimensionada = pygame.transform.smoothscale(
            imagem, (largura, altura)
        )
        tela.blit(imagem_redimensionada, retangulo)

    else:
        pygame.draw.rect(
            tela, BRANCO, retangulo, border_radius=8
        )
        pygame.draw.rect(
            tela, (30, 30, 30), retangulo, 2, border_radius=8
        )

        fonte_carta = pygame.font.Font(str(CAMINHO_FONTE), 10)
        texto = fonte_carta.render(
            f'{carta["valor"]} {carta["naipe"]}',
            True,
            (20, 20, 20),
        )

        tela.blit(texto, (x + 5, y + 10))

    return retangulo


# ==================================================
# TELA DA PARTIDA
# ==================================================

def iniciar_partida(tela, relogio):
    partida = Partida()
    partida.pontos_jogador = 11
    partida.pontos_computador = 0

    imagens_cartas = carregar_imagens_cartas()
    fundo_partida = carregar_fundo()
    imagem_vitoria = carregar_tela_vitoria()

    fonte = pygame.font.Font(str(CAMINHO_FONTE), 20)
    fonte_pequena = pygame.font.Font(str(CAMINHO_FONTE), 10)
    fonte_vitoria = pygame.font.Font(str(CAMINHO_FONTE), 64)

    carta_jogador = None
    carta_computador = None

    mensagem = "Clique em uma carta para jogar."

    aguardando_proxima = False
    encerrada = False
    jogador_venceu = False

    botao_truco = pygame.Rect(
        LARGURA // 2 - 100, 570, 200, 45
    )
    botao_aceitar = pygame.Rect(
        LARGURA // 2 - 210, 570, 200, 45
    )
    botao_correr = pygame.Rect(
        LARGURA // 2 + 10, 570, 200, 45
    )

    # ==================================================
    # LOOP PRINCIPAL
    # ==================================================

    while True:
        quantidade = len(partida.jogador.cartas)
        espacamento = 120
        inicio_x = (LARGURA - quantidade * espacamento) // 2

        botoes_cartas = []

        for indice, carta in enumerate(partida.jogador.cartas):
            x = inicio_x + indice * espacamento
            botoes_cartas.append(
                pygame.Rect(x, 410, 100, 145)
            )

        # ------------------------------------------
        # DETECTAR FIM DA PARTIDA AUTOMATICAMENTE
        # ------------------------------------------

        if not encerrada and partida.partida_encerrada():
            encerrada = True
            jogador_venceu = (
                partida.pontos_jogador >= PONTOS_PARA_VENCER
            )

            if jogador_venceu:
                mensagem = "Vitória!"
            else:
                mensagem = "Fim de jogo!"

        # ------------------------------------------
        # EVENTOS
        # ------------------------------------------

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return "sair"

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    return "menu"

            if (
                evento.type != pygame.MOUSEBUTTONDOWN
                or evento.button != 1
            ):
                continue

            # Tela final: clique inicia nova partida.
            if encerrada:
                partida = Partida()

                carta_jogador = None
                carta_computador = None

                mensagem = "Clique em uma carta para jogar."
                aguardando_proxima = False
                encerrada = False
                jogador_venceu = False
                continue

            # Responder ao truco do computador.
            if partida.truco_pendente_computador:
                if botao_aceitar.collidepoint(evento.pos):
                    mensagem = partida.responder_truco(True)
                    aguardando_proxima = False
                    continue

                if botao_correr.collidepoint(evento.pos):
                    mensagem = partida.responder_truco(False)
                    aguardando_proxima = True
                    continue

                continue

            # Continuar após uma rodada ou mão.
            if aguardando_proxima:
                if partida.partida_encerrada():
                    encerrada = True
                    jogador_venceu = (
                        partida.pontos_jogador >= PONTOS_PARA_VENCER
                    )

                    mensagem = (
                        "Vitória!" if jogador_venceu
                        else "Fim de jogo!"
                    )

                elif (
                    partida.mao_encerrada
                    or not partida.jogador.tem_cartas()
                ):
                    partida.nova_mao()
                    carta_jogador = None
                    carta_computador = None
                    mensagem = "Nova mão! Clique em uma carta."

                else:
                    carta_jogador = None
                    carta_computador = None
                    mensagem = "Clique em uma carta para jogar."

                aguardando_proxima = False
                continue

            # Pedir truco.
            if (
                botao_truco.collidepoint(evento.pos)
                and not partida.truco_pedido
                and not partida.mao_encerrada
            ):
                resultado_truco = partida.pedir_truco()

                if isinstance(resultado_truco, dict):
                    mensagem = resultado_truco["mensagem"]

                    if resultado_truco["status"] == "recusado":
                        aguardando_proxima = True
                else:
                    mensagem = resultado_truco

                continue

            # Jogar uma carta.
            for indice, retangulo in enumerate(botoes_cartas):
                if not retangulo.collidepoint(evento.pos):
                    continue

                resultado = partida.jogar_rodada(indice)

                if not isinstance(resultado, dict):
                    mensagem = resultado
                    break

                carta_jogador = resultado["carta_jogador"]
                carta_computador = resultado["carta_computador"]

                if resultado["computador_pediu_truco"]:
                    mensagem = (
                        "O computador pediu TRUCO! Aceita ou corre?"
                    )

                elif resultado["vencedor_mao"] == "jogador":
                    mensagem = "Você venceu a mão! Clique para continuar."
                    aguardando_proxima = True

                elif resultado["vencedor_mao"] == "computador":
                    mensagem = (
                        "Computador venceu a mão! Clique para continuar."
                    )
                    aguardando_proxima = True

                elif resultado["vencedor_mao"] == "empate":
                    mensagem = "Mão empatada! Clique para continuar."
                    aguardando_proxima = True

                elif resultado["resultado"] == "jogador":
                    mensagem = (
                        "Você venceu a rodada! Clique para continuar."
                    )
                    aguardando_proxima = True

                elif resultado["resultado"] == "computador":
                    mensagem = (
                        "Computador venceu a rodada! Clique para continuar."
                    )
                    aguardando_proxima = True

                else:
                    mensagem = "Rodada empatada! Clique para continuar."
                    aguardando_proxima = True

                break

        # ------------------------------------------
        # DESENHAR A TELA FINAL
        # ------------------------------------------

        if encerrada:
            if jogador_venceu and imagem_vitoria:
                tela.blit(imagem_vitoria, (0, 0))
            elif fundo_partida:
                tela.blit(fundo_partida, (0, 0))
            else:
                tela.fill((20, 90, 45))

            if jogador_venceu:
                texto_vitoria = fonte_vitoria.render(
                    "Vitória!",
                    True,
                    DOURADO,
                )

                retangulo_vitoria = texto_vitoria.get_rect(
                    center=(LARGURA // 2, ALTURA // 2 - 30)
                )

                # Contorno preto
                for dx in range(-3, 4):
                    for dy in range(-3, 4):
                        if dx != 0 or dy != 0:
                            contorno = fonte_vitoria.render(
                                "Vitória!",
                                True,
                                (0, 0, 0),
                            )
                            tela.blit(
                                contorno,
                                retangulo_vitoria.move(dx, dy),
                            )

                # Texto dourado por cima do contorno
                tela.blit(texto_vitoria, retangulo_vitoria)

                texto_ajuda = fonte_pequena.render(
                    "CLIQUE PARA JOGAR NOVAMENTE",
                    True,
                    BRANCO,
                )

            else:
                texto_derrota = fonte.render(
                    "FIM DE JOGO",
                    True,
                    DOURADO,
                )

                tela.blit(
                    texto_derrota,
                    texto_derrota.get_rect(
                        center=(LARGURA // 2, ALTURA // 2)
                    ),
                )

                texto_ajuda = fonte_pequena.render(
                    "CLIQUE PARA JOGAR NOVAMENTE",
                    True,
                    BRANCO,
                )

            tela.blit(
                texto_ajuda,
                texto_ajuda.get_rect(
                    center=(LARGURA // 2, ALTURA - 50)
                ),
            )

            pygame.display.flip()
            relogio.tick(60)
            continue

        # ------------------------------------------
        # DESENHAR A INTERFACE NORMAL
        # ------------------------------------------

        if fundo_partida:
            tela.blit(fundo_partida, (0, 0))
        else:
            tela.fill((20, 90, 45))

        titulo = fonte.render("PYTRUCO", True, DOURADO)
        tela.blit(
            titulo,
            titulo.get_rect(center=(LARGURA // 2, 35)),
        )

        placar = fonte_pequena.render(
            f"Você: {partida.pontos_jogador} | "
            f"Computador: {partida.pontos_computador}",
            True,
            BRANCO,
        )
        tela.blit(
            placar,
            placar.get_rect(center=(LARGURA // 2, 80)),
        )

        texto_valor = fonte_pequena.render(
            f"Valor da mão: {partida.valor_mao}",
            True,
            DOURADO,
        )
        tela.blit(
            texto_valor,
            texto_valor.get_rect(center=(LARGURA // 2, 110)),
        )

        centro_jogador = LARGURA // 2 - 70
        centro_computador = LARGURA // 2 + 70

        texto = fonte_pequena.render("SUA CARTA", True, BRANCO)
        tela.blit(
            texto,
            texto.get_rect(center=(centro_jogador, 145)),
        )

        texto = fonte_pequena.render("COMPUTADOR", True, BRANCO)
        tela.blit(
            texto,
            texto.get_rect(center=(centro_computador, 145)),
        )

        if carta_jogador and carta_computador:
            desenhar_carta(
                tela,
                carta_jogador,
                centro_jogador - 50,
                165,
                imagens_cartas,
            )
            desenhar_carta(
                tela,
                carta_computador,
                centro_computador - 50,
                165,
                imagens_cartas,
            )

        texto = fonte_pequena.render("SUAS CARTAS", True, BRANCO)
        tela.blit(
            texto,
            texto.get_rect(center=(LARGURA // 2, 370)),
        )

        for indice, carta in enumerate(partida.jogador.cartas):
            x = inicio_x + indice * espacamento
            desenhar_carta(
                tela, carta, x, 410, imagens_cartas
            )

        # Botões do truco.
        if partida.truco_pendente_computador:
            pygame.draw.rect(
                tela, (35, 145, 65), botao_aceitar, border_radius=8
            )
            pygame.draw.rect(
                tela, DOURADO, botao_aceitar, 2, border_radius=8
            )

            texto = fonte_pequena.render("ACEITAR", True, BRANCO)
            tela.blit(
                texto,
                texto.get_rect(center=botao_aceitar.center),
            )

            pygame.draw.rect(
                tela, (180, 45, 45), botao_correr, border_radius=8
            )
            pygame.draw.rect(
                tela, DOURADO, botao_correr, 2, border_radius=8
            )

            texto = fonte_pequena.render("CORRER", True, BRANCO)
            tela.blit(
                texto,
                texto.get_rect(center=botao_correr.center),
            )

        else:
            truco_disponivel = (
                not partida.truco_pedido
                and not partida.mao_encerrada
                and not aguardando_proxima
            )

            cor_botao = (
                (180, 45, 45)
                if truco_disponivel
                else (90, 90, 90)
            )

            pygame.draw.rect(
                tela, cor_botao, botao_truco, border_radius=8
            )
            pygame.draw.rect(
                tela, DOURADO, botao_truco, 2, border_radius=8
            )

            texto = fonte_pequena.render(
                "PEDIR TRUCO", True, BRANCO
            )
            tela.blit(
                texto,
                texto.get_rect(center=botao_truco.center),
            )

        texto_mensagem = fonte_pequena.render(
            mensagem, True, DOURADO
        )
        tela.blit(
            texto_mensagem,
            texto_mensagem.get_rect(center=(LARGURA // 2, 630)),
        )

        ajuda = fonte_pequena.render(
            "ESC: voltar ao menu", True, BRANCO
        )
        tela.blit(
            ajuda,
            ajuda.get_rect(center=(LARGURA // 2, 675)),
        )

        pygame.display.flip()
        relogio.tick(60)

