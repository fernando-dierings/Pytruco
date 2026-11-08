import pygame

import random

from settings import (
    LARGURA,
    ALTURA,
    BRANCO,
    PRETO,
    DOURADO,
    PONTOS_PARA_VENCER,
    CAMINHO_FONTE,
    CAMINHO_FUNDO_PARTIDA,
    CAMINHO_MUSICA_PARTIDA,
    CAMINHO_TELA_DERROTA,
    CAMINHO_TELA_VITORIA,
    CAMINHO_VERSO_CARTA,
    CAMINHO_SOM_CARTA_JOGADOR,
    CAMINHO_SOM_CARTA_COMPUTADOR,
    CAMINHO_SOM_ROLLOVER,
    CAMINHO_SOM_TOQUE,
    CAMINHO_SOM_CLICK,
    CAMINHO_MUSICA_VITORIA,
    CAMINHO_MUSICA_DERROTA,
    SOM_TRUCO_NOTIFICACAO,
    CAMINHO_VOZ_DERROTA,
    CAMINHO_VOZ_DERROTA_1,
    CAMINHO_VOZ_DERROTA_2,
    CAMINHO_VOZ_VITORIA,
    CAMINHO_VOZ_VITORIA_1,
    CAMINHO_VOZ_VITORIA_2,
    PASTA_CARTAS,
    AMARELO,
)

from logica.partida import Partida
from utils.recursos import desenhar_texto_contornado

# ==================================================
# CAMINHOS E CONFIGURAÇÕES
# ==================================================

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
    return carregar_imagem(CAMINHO_FUNDO_PARTIDA)


def carregar_tela_vitoria():
    return carregar_imagem(CAMINHO_TELA_VITORIA)


def carregar_verso_carta():
    if not CAMINHO_VERSO_CARTA.exists():
        print(f"Verso da carta não encontrado: {CAMINHO_VERSO_CARTA}")
        return None

    return pygame.image.load(str(CAMINHO_VERSO_CARTA)).convert_alpha()

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


def desenhar_verso_carta(
        tela, imagem, x, y, largura=100, altura=145
):
    retangulo = pygame.Rect(x, y, largura, altura)

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
            tela, PRETO, retangulo, 2, border_radius=8
        )

    return retangulo


# ==================================================
# TELA DA PARTIDA
# ==================================================

def iniciar_partida(tela, relogio):
    partida = Partida()
    partida.pontos_jogador = 0

    if CAMINHO_MUSICA_PARTIDA.exists():
        pygame.mixer.music.load(str(CAMINHO_MUSICA_PARTIDA))
        pygame.mixer.music.set_volume(0.10)
        pygame.mixer.music.play(-1)
    else:
        print(f"Música da partida não encontrada: {CAMINHO_MUSICA_PARTIDA}")

    # Efeitos sonoros das cartas
    som_carta_jogador = pygame.mixer.Sound(str(CAMINHO_SOM_CARTA_JOGADOR))
    som_carta_computador = pygame.mixer.Sound(str(CAMINHO_SOM_CARTA_COMPUTADOR))
    som_truco_notificacao = pygame.mixer.Sound(str(SOM_TRUCO_NOTIFICACAO))
    som_rollover = pygame.mixer.Sound(str(CAMINHO_SOM_ROLLOVER))
    som_toque = pygame.mixer.Sound(str(CAMINHO_SOM_TOQUE))
    som_click = pygame.mixer.Sound(str(CAMINHO_SOM_CLICK))
    musica_vitoria = pygame.mixer.Sound(str(CAMINHO_MUSICA_VITORIA))
    musica_derrota = pygame.mixer.Sound(str(CAMINHO_MUSICA_DERROTA))

    falas_derrota = [
        pygame.mixer.Sound(str(CAMINHO_VOZ_DERROTA)),
        pygame.mixer.Sound(str(CAMINHO_VOZ_DERROTA_1)),
        pygame.mixer.Sound(str(CAMINHO_VOZ_DERROTA_2))
    ]

    falas_vitoria = [
        pygame.mixer.Sound(str(CAMINHO_VOZ_VITORIA)),
        pygame.mixer.Sound(str(CAMINHO_VOZ_VITORIA_1)),
        pygame.mixer.Sound(str(CAMINHO_VOZ_VITORIA_2))
    ]

    def parar_falas():
        for fala in falas_vitoria + falas_derrota:
            fala.stop()

    som_rollover.set_volume(0.05)
    som_toque.set_volume(0.05)
    som_click.set_volume(0.5)
    som_truco_notificacao.set_volume(0.5)
    som_carta_jogador.set_volume(0.5)
    som_carta_computador.set_volume(0.5)
    musica_vitoria.set_volume(0.3)
    musica_derrota.set_volume(0.3)

    imagens_cartas = carregar_imagens_cartas()
    fundo_partida = carregar_fundo()
    imagem_verso_carta = carregar_verso_carta()
    imagem_vitoria = carregar_tela_vitoria()
    imagem_derrota = carregar_imagem(CAMINHO_TELA_DERROTA)

    fonte_media = pygame.font.Font(str(CAMINHO_FONTE), 35)
    fonte_pequena = pygame.font.Font(str(CAMINHO_FONTE), 10)
    fonte_vitoria = pygame.font.Font(str(CAMINHO_FONTE), 64)

    musica_derrota_tocada = False
    musica_vitoria_tocada = False
    carta_jogador = None
    carta_computador = None
    computador_ja_comecou = False
    carta_jogador_pendente = None
    carta_computador_pendente = None
    botao_hover_anterior = None
    carta_hover_anterior = None
    carta_jogador_pendente = None
    carta_computador_pendente = None

    tempo_jogada = 0
    computador_ja_comecou = False

    # Guarda a carta enquanto o computador aguarda para jogar.
    carta_jogador_pendente = None

    tempo_jogada = 0

    mensagem = "Clique em uma carta para jogar."

    aguardando_proxima = False
    encerrada = False
    jogador_venceu = False

    botao_truco = pygame.Rect(
        LARGURA - 240, ALTURA - 80, 200, 45
    )

    botao_aceitar = pygame.Rect(
        LARGURA - 240, ALTURA - 132, 200, 45
    )

    botao_correr = pygame.Rect(
        LARGURA - 240, ALTURA - 80, 200, 45
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
                pygame.Rect(x, 445, 100, 145)
            )

        # ------------------------------------------
        # ESPERA PARA O COMPUTADOR JOGAR
        # ------------------------------------------
        # ------------------------------------------
        # COMPUTADOR COMEÇA A RODADA
        # ------------------------------------------

        if (
                partida.quem_comeca_rodada == "computador"
                and not computador_ja_comecou
                and not aguardando_proxima
                and not partida.mao_encerrada
                and not partida.truco_pendente_computador
        ):
            resultado_inicio = partida.iniciar_rodada_computador()

            if isinstance(resultado_inicio, dict):
                carta_computador = resultado_inicio["carta_computador"]

                som_carta_computador.play()

                computador_ja_comecou = True
                tempo_jogada = pygame.time.get_ticks()

                mensagem = "O computador jogou. Sua vez!"

            else:
                mensagem = resultado_inicio

        # ------------------------------------------
        # ESPERA PARA O JOGADOR RESPONDER
        # ------------------------------------------

        if (
                computador_ja_comecou
                and pygame.time.get_ticks() - tempo_jogada >= 1000
        ):
            mensagem = "Sua vez! Escolha uma carta."

        # ------------------------------------------
        # COMPUTADOR RESPONDE QUANDO VOCÊ COMEÇA
        # ------------------------------------------

        if (
                carta_jogador_pendente is not None
                and pygame.time.get_ticks() - tempo_jogada >= 1000
        ):
            resultado = partida.concluir_rodada(
                carta_jogador_pendente
            )

            carta_computador = resultado["carta_computador"]
            som_carta_computador.play()

            carta_jogador_pendente = None

            if resultado["computador_pediu_truco"]:
                som_truco_notificacao.play()
                mensagem = "O computador pediu TRUCO! Aceita ou corre?"

            elif resultado["vencedor_mao"] == "jogador":
                mensagem = "Você venceu a mão! Clique para continuar."
                aguardando_proxima = True

            elif resultado["vencedor_mao"] == "computador":
                mensagem = "Computador venceu a mão! Clique para continuar."
                aguardando_proxima = True

            elif resultado["vencedor_mao"] == "empate":
                mensagem = "Mão empatada! Clique para continuar."
                aguardando_proxima = True

            elif resultado["resultado"] == "jogador":
                mensagem = "Você venceu a rodada! Clique para continuar."
                aguardando_proxima = True

            elif resultado["resultado"] == "computador":
                mensagem = "Computador venceu a rodada! Clique para continuar."
                aguardando_proxima = True

            else:
                mensagem = "Rodada empatada! Clique para continuar."
                aguardando_proxima = True

        # Detectar mouse sobre ACEITAR e CORRER
        botao_hover_atual = None

        if partida.truco_pendente_computador:
            pos_mouse = pygame.mouse.get_pos()

            if botao_aceitar.collidepoint(pos_mouse):
                botao_hover_atual = "aceitar"

            elif botao_correr.collidepoint(pos_mouse):
                botao_hover_atual = "correr"

        if (
                botao_hover_atual is not None
                and botao_hover_atual != botao_hover_anterior
        ):
            som_rollover.play()

        botao_hover_anterior = botao_hover_atual
        # ------------------------------------------
        # DETECTAR FIM DA PARTIDA AUTOMATICAMENTE
        # ------------------------------------------

        if not encerrada and partida.partida_encerrada():
            encerrada = True
            jogador_venceu = (
                    partida.pontos_jogador >= PONTOS_PARA_VENCER
            )

            if jogador_venceu and not musica_vitoria_tocada:
                pygame.mixer.music.stop()
                musica_vitoria.play()
                random.choice(falas_vitoria).play()
                musica_vitoria_tocada = True


            elif not jogador_venceu and not musica_derrota_tocada:
                pygame.mixer.music.stop()
                musica_derrota.play()
                random.choice(falas_derrota).play()
                musica_derrota_tocada = True

            if jogador_venceu:
                mensagem = "Vitória!"
            else:
                mensagem = "Fim de jogo!"

        # ------------------------------------------
        # EVENTOS
        # ------------------------------------------

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.mixer.music.stop()
                musica_vitoria.stop()
                musica_derrota.stop()
                return "sair"

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    parar_falas()
                    musica_vitoria.stop()
                    musica_derrota.stop()
                    pygame.mixer.music.stop()
                    return "menu"

            if (
                    evento.type != pygame.MOUSEBUTTONDOWN
                    or evento.button != 1
            ):
                continue

            # Tela final: clique inicia nova partida.
            if encerrada:
                parar_falas()

                partida = Partida()

                musica_vitoria.stop()
                musica_derrota.stop()

                musica_vitoria_tocada = False
                musica_derrota_tocada = False

                pygame.mixer.music.play(-1)

                carta_jogador = None
                carta_computador = None
                carta_jogador_pendente = None

                mensagem = "Clique em uma carta para jogar."
                aguardando_proxima = False
                encerrada = False
                jogador_venceu = False
                continue

            # Bloqueia outros cliques enquanto o computador aguarda.
            if carta_jogador_pendente is not None:
                continue

            # Responder ao truco do computador.
            if partida.truco_pendente_computador:
                if botao_aceitar.collidepoint(evento.pos):
                    som_click.play()
                    mensagem = partida.responder_truco(True)
                    aguardando_proxima = False
                    continue

                if botao_correr.collidepoint(evento.pos):
                    som_click.play()
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
                som_click.play()
                resultado_truco = partida.pedir_truco()

                if isinstance(resultado_truco, dict):
                    mensagem = resultado_truco["mensagem"]

                    if resultado_truco["status"] == "recusado":
                        aguardando_proxima = True
                else:
                    mensagem = resultado_truco

                continue

            # Jogar uma carta.
            # Jogar uma carta.
            for indice, retangulo in enumerate(botoes_cartas):
                if not retangulo.collidepoint(evento.pos):
                    continue

                # Caso você comece a rodada.
                if partida.quem_comeca_rodada == "jogador":
                    resultado = partida.iniciar_rodada(indice)

                    if not isinstance(resultado, dict):
                        mensagem = resultado
                        break

                    carta_jogador = resultado["carta_jogador"]
                    carta_jogador_pendente = carta_jogador
                    tempo_jogada = pygame.time.get_ticks()

                    som_carta_jogador.play()
                    carta_computador = None

                    mensagem = "Aguardando o computador..."

                # Caso o computador tenha começado.
                else:
                    if (
                            not computador_ja_comecou
                            or pygame.time.get_ticks() - tempo_jogada < 1000
                    ):
                        mensagem = "Aguarde o computador jogar."
                        break

                    resultado = partida.jogar_resposta_jogador(indice)

                    if not isinstance(resultado, dict):
                        mensagem = resultado
                        break

                    carta_jogador = resultado["carta_jogador"]
                    som_carta_jogador.play()

                    resultado = partida.concluir_rodada(
                        carta_jogador,
                        carta_computador,
                    )

                    computador_ja_comecou = False

                    if resultado["computador_pediu_truco"]:
                        som_truco_notificacao.play()
                        mensagem = "O computador pediu TRUCO! Aceita ou corre?"

                    elif resultado["vencedor_mao"] == "jogador":
                        mensagem = "Você venceu a mão! Clique para continuar."
                        aguardando_proxima = True

                    elif resultado["vencedor_mao"] == "computador":
                        mensagem = "Computador venceu a mão! Clique para continuar."
                        aguardando_proxima = True

                    elif resultado["vencedor_mao"] == "empate":
                        mensagem = "Mão empatada! Clique para continuar."
                        aguardando_proxima = True

                    elif resultado["resultado"] == "jogador":
                        mensagem = "Você venceu a rodada! Clique para continuar."
                        aguardando_proxima = True

                    elif resultado["resultado"] == "computador":
                        mensagem = "Computador venceu a rodada! Clique para continuar."
                        aguardando_proxima = True

                    else:
                        mensagem = "Rodada empatada! Clique para continuar."

                        aguardando_proxima = True

                break

        # ------------------------------------------
        # DESENHAR A TELA FINAL
        # ------------------------------------------

        if encerrada:
            imagem_final = (
                imagem_vitoria if jogador_venceu
                else imagem_derrota
            )

            if imagem_final:
                tela.blit(imagem_final, (0, 0))
            elif fundo_partida:
                tela.blit(fundo_partida, (0, 0))
            else:
                tela.fill((20, 90, 45))

            if jogador_venceu:
                desenhar_texto_contornado(
                    tela,
                    fonte_vitoria,
                    "Vitória!",
                    DOURADO,
                    (LARGURA // 2, ALTURA // 2 - 30)
                )
            else:
                desenhar_texto_contornado(
                    tela,
                    fonte_vitoria,
                    "DERROTA!",
                    DOURADO,
                    (LARGURA // 2, ALTURA // 2)
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

        # Título.
        titulo = fonte_media.render("PYTRUCO", True, AMARELO)
        tela.blit(
            titulo,
            titulo.get_rect(center=(LARGURA // 2, 30))
        )

        # Placar.
        placar = fonte_pequena.render(
            f"VOCÊ: {partida.pontos_jogador} | "
            f"COMPUTADOR: {partida.pontos_computador}",
            True,
            BRANCO,
        )

        tela.blit(placar, (35, 35))

        # Valor da mão.
        texto_valor = fonte_pequena.render(
            f"VALOR DA MÃO: {partida.valor_mao}",
            True,
            DOURADO,
        )

        tela.blit(
            texto_valor,
            (35, ALTURA - 35 - texto_valor.get_height())
        )

        # ==========================================
        # CARTAS DO COMPUTADOR
        # ==========================================

        espacamento_versos = 120
        cartas_restantes_computador = len(partida.computador.cartas)

        largura_total = (
                cartas_restantes_computador * 100
                + (cartas_restantes_computador - 1)
                * (espacamento_versos - 100)
        )

        inicio_versos = (LARGURA - largura_total) // 2

        for indice in range(cartas_restantes_computador):
            x = inicio_versos + indice * espacamento_versos

            desenhar_verso_carta(
                tela,
                imagem_verso_carta,
                x,
                120,
            )

        # ==========================================
        # CARTAS JOGADAS NO CENTRO
        # ==========================================

        centro_jogador = LARGURA // 2 - 60
        centro_computador = LARGURA // 2 + 60

        # A carta do jogador aparece imediatamente.
        if carta_jogador is not None:
            desenhar_carta(
                tela,
                carta_jogador,
                centro_jogador - 50,
                320,
                imagens_cartas,
            )

        # A carta do computador aparece após 1 segundo.
        if carta_computador is not None:
            desenhar_carta(
                tela,
                carta_computador,
                centro_computador - 50,
                290,
                imagens_cartas,
            )

        # ==========================================
        # SUAS CARTAS DISPONÍVEIS
        # ==========================================

        pos_mouse = pygame.mouse.get_pos()
        carta_hover_atual = None

        for indice, carta in enumerate(partida.jogador.cartas):
            x = inicio_x + indice * espacamento
            y = 465

            retangulo = pygame.Rect(x, y, 100, 145)

            mouse_sobre_carta = retangulo.collidepoint(pos_mouse)

            carta_disponivel = (
                    not aguardando_proxima
                    and carta_jogador_pendente is None
                    and not partida.truco_pendente_computador
                    and not partida.mao_encerrada
                    and not encerrada
            )

            if mouse_sobre_carta and carta_disponivel:
                carta_hover_atual = indice

            if mouse_sobre_carta and carta_disponivel:
                largura = 110
                altura = 160
                x_desenho = x - 5
                y_desenho = y - 15
            else:
                largura = 100
                altura = 145
                x_desenho = x
                y_desenho = y

            desenhar_carta(
                tela,
                carta,
                x_desenho,
                y_desenho,
                imagens_cartas,
                largura,
                altura,
            )

        if (carta_hover_atual is not None and carta_hover_atual != carta_hover_anterior):
            som_toque.play()

        carta_hover_anterior = carta_hover_atual

        # ==========================================
        # BOTÕES DO TRUCO
        # ==========================================

        if partida.truco_pendente_computador:
            pygame.draw.rect(
                tela,
                (35, 145, 65),
                botao_aceitar,
                border_radius=8
            )

            pygame.draw.rect(
                tela,
                DOURADO,
                botao_aceitar,
                2,
                border_radius=8
            )

            cor_texto = AMARELO if botao_hover_atual == "aceitar" else BRANCO

            texto = fonte_pequena.render(
                "ACEITAR", True, cor_texto
            )

            tela.blit(
                texto,
                texto.get_rect(center=botao_aceitar.center),
            )

            pygame.draw.rect(
                tela,
                (180, 45, 45),
                botao_correr,
                border_radius=8
            )

            pygame.draw.rect(
                tela,
                DOURADO,
                botao_correr,
                2,
                border_radius=8
            )

            cor_texto = AMARELO if botao_hover_atual == "correr" else BRANCO

            texto = fonte_pequena.render(
                "CORRER", True, cor_texto
            )

            tela.blit(
                texto,
                texto.get_rect(center=botao_correr.center),
            )

        else:
            truco_disponivel = (
                    not partida.truco_pedido
                    and not partida.mao_encerrada
                    and not aguardando_proxima
                    and carta_jogador_pendente is None
            )

            cor_botao = (
                (180, 45, 45)
                if truco_disponivel
                else (90, 90, 90)
            )

            pygame.draw.rect(
                tela,
                cor_botao,
                botao_truco,
                border_radius=8
            )

            pygame.draw.rect(
                tela,
                DOURADO,
                botao_truco,
                2,
                border_radius=8
            )

            texto = fonte_pequena.render(
                "PEDIR TRUCO", True, BRANCO
            )

            tela.blit(
                texto,
                texto.get_rect(center=botao_truco.center),
            )

        # Mensagem.
        texto_mensagem = fonte_pequena.render(
            mensagem, True, DOURADO
        )

        tela.blit(
            texto_mensagem,
            texto_mensagem.get_rect(
                center=(LARGURA // 2, 660)
            ),
        )

        # Atalho para voltar ao menu.
        ajuda = fonte_pequena.render(
            "ESC: VOLTAR AO MENU", True, BRANCO
        )

        tela.blit(
            ajuda,
            (35, ALTURA - 7 - ajuda.get_height())
        )

        pygame.display.flip()
        relogio.tick(60)
