import pygame

import random

import math

from settings import (
    LARGURA,
    ALTURA,
    BRANCO,
    PRETO,
    DOURADO,
    PONTOS_PARA_VENCER,
    CAMINHO_BOTAO_AVISO,
    CAMINHO_BOTAO1,
    CAMINHO_BOTAO_CONFIRMAR1,
    CAMINHO_FONTE,
    CAMINHO_FUNDO_PARTIDA,
    CAMINHO_LOGO_PLACA,
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

def carregar_imagem_botao(caminho):
    if not caminho.exists():
        print(f"Imagem do botão não encontrada: {caminho}")
        return None

    imagem = pygame.image.load(str(caminho)).convert_alpha()

    return pygame.transform.smoothscale(
        imagem,
        (200, 45)
    )

def alterar_cor_botao(imagem, cor):
    imagem = imagem.copy()

    camada = pygame.Surface(
        imagem.get_size(),
        pygame.SRCALPHA
    )

    camada.fill(cor)

    imagem.blit(
        camada,
        (0, 0),
        special_flags=pygame.BLEND_RGBA_MULT
    )

    return imagem


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


def desenhar_baralho(tela, imagem, x, y, quantidade=6):
    # Cada carta representa uma camada do baralho.
    quantidade = max(0, min(6, quantidade))

    for indice in range(quantidade):
        deslocamento = indice * 2

        desenhar_verso_carta(
            tela,
            imagem,
            x + deslocamento,
            y - deslocamento,
        )


def desenhar_carta_em_movimento(
        tela, imagem, origem, destino, progresso
):
    largura = 100
    altura = 145

    # Suaviza o movimento.
    progresso_suave = 1 - (1 - progresso) ** 3

    # Calcula a posição atual da carta.
    x = origem[0] + (destino[0] - origem[0]) * progresso_suave
    y = origem[1] + (destino[1] - origem[1]) * progresso_suave

    # Pequena rotação durante o movimento.
    angulo = math.sin(progresso * math.pi) * 12

    # Redimensiona e rotaciona o verso da carta.
    carta = pygame.transform.smoothscale(
        imagem,
        (largura, altura)
    )

    carta = pygame.transform.rotate(carta, angulo)

    # Mantém o centro da carta na trajetória.
    retangulo = carta.get_rect(
        center=(int(x), int(y))
    )

    tela.blit(carta, retangulo)


def desenhar_texto_vencedor(
        tela, texto, fonte, centro_x, centro_y, tempo
):
    progresso = min(1.0, tempo / 1200)

    # Movimento suave para cima
    deslocamento_y = int(15 * progresso)

    # Desaparecimento gradual
    opacidade = int(255 * (1 - progresso))

    superficie_texto = fonte.render(
        texto, False, DOURADO
    )

    superficie_sombra = fonte.render(
        texto, False, PRETO
    )

    superficie_texto.set_alpha(opacidade)
    superficie_sombra.set_alpha(opacidade)

    retangulo = superficie_texto.get_rect(
        center=(centro_x, centro_y - deslocamento_y)
    )

    retangulo_sombra = superficie_sombra.get_rect(
        center=(
            centro_x + 2,
            centro_y - deslocamento_y + 2
        )
    )

    tela.blit(superficie_sombra, retangulo_sombra)
    tela.blit(superficie_texto, retangulo)


# ==================================================
# TELA DA PARTIDA
# ==================================================

def iniciar_partida(tela, relogio, nome_jogador="Você"):
    partida = Partida(nome_jogador.upper())
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
    imagem_botao_aviso = carregar_imagem_botao(CAMINHO_BOTAO_AVISO)
    imagem_botao = carregar_imagem_botao(CAMINHO_BOTAO1)
    imagem_botao_confirmar = carregar_imagem_botao(CAMINHO_BOTAO_CONFIRMAR1)

    # Logo da partida
    logo_partida = pygame.image.load(
        str(CAMINHO_LOGO_PLACA)
    ).convert_alpha()

    largura_logo = 240
    altura_logo = int(
        logo_partida.get_height() * largura_logo / logo_partida.get_width()
    )

    logo_partida = pygame.transform.smoothscale(
        logo_partida,
        (largura_logo, altura_logo)
    )

    imagem_vitoria = carregar_tela_vitoria()
    imagem_derrota = carregar_imagem(CAMINHO_TELA_DERROTA)

    fonte_media = pygame.font.Font(str(CAMINHO_FONTE), 35)
    fonte_pequena = pygame.font.Font(str(CAMINHO_FONTE), 10)
    fonte_vitoria = pygame.font.Font(str(CAMINHO_FONTE), 64)
    fonte_texto_vencedor = pygame.font.Font(str(CAMINHO_FONTE), 7)
    fonte_boasorte = pygame.font.Font(str(CAMINHO_FONTE), 36)

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
    truco_aceito_jogador = False

    tempo_jogada = 0
    computador_ja_comecou = False

    # Guarda a carta enquanto o computador aguarda para jogar.
    carta_jogador_pendente = None

    tempo_jogada = 0

    mensagem = "Clique em uma carta para jogar."

    # Animação de distribuição das cartas.
    DURACAO_DISTRIBUICAO = 450
    INTERVALO_DISTRIBUICAO = 250
    DURACAO_REVELACAO = 500

    # Controla a velocidade das distribuições.
    primeira_distribuicao = True

    # Mensagem especial da primeira distribuição.
    mostrar_boasorte = True
    inicio_boasorte = pygame.time.get_ticks()
    DURACAO_BOASORTE = 4500

    duracao_distribuicao_atual = 450
    intervalo_distribuicao_atual = 250
    duracao_revelacao_atual = 500
    distribuicao_ativa = True
    distribuicao_inicio = pygame.time.get_ticks()

    # Etapa da distribuição:
    # 0 = primeira carta do jogador
    # 1 = primeira carta do computador
    # 2 = segunda carta do jogador...
    indice_distribuicao = -1
    etapa_distribuicao = 0
    progresso_distribuicao = 0.0

    # Controle da revelação simultânea.
    revelacao_inicio = None

    # Posição do baralho, à esquerda e centralizado verticalmente.
    BARALHO_X = 45
    BARALHO_Y = (ALTURA - 145) // 2

    # Tamanho das cartas durante a animação.
    LARGURA_CARTA = 100
    ALTURA_CARTA = 145

    mensagem = "Distribuindo as cartas..."

    # Animação da carta do jogador
    DURACAO_ANIMACAO_CARTA = 500
    animacao_carta_jogador_inicio = None
    animacao_carta_jogador_tempo = 0

    # Animação da carta do computador
    animacao_carta_computador_tempo = 0
    animacao_carta_computador_ativa = False
    DURACAO_GIRO_CARTA = 400
    animacao_giro_computador_inicio = None

    # Destaque da carta vencedora
    DURACAO_DESTAQUE_CARTA = 1200
    carta_destaque = None
    tempo_inicio_destaque = None

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

        # ------------------------------------------
        # CONTROLE DA DISTRIBUIÇÃO DAS CARTAS
        # ------------------------------------------

        if distribuicao_ativa:
            agora = pygame.time.get_ticks()

            tempo_decorrido = agora - distribuicao_inicio

            duracao_etapa = (
                    duracao_distribuicao_atual
                    + intervalo_distribuicao_atual
            )

            tempo_total = (
                    5 * duracao_etapa
                    + duracao_distribuicao_atual
            )


            if tempo_decorrido < tempo_total:

                etapa_distribuicao = min(
                    int(tempo_decorrido // duracao_etapa),
                    5
                )

                tempo_etapa = tempo_decorrido % duracao_etapa

                progresso_distribuicao = min(
                    1.0,
                    tempo_etapa / duracao_distribuicao_atual
                )

                # Toca o som apenas quando uma nova carta começa.
                if etapa_distribuicao != indice_distribuicao:

                    indice_distribuicao = etapa_distribuicao

                    if etapa_distribuicao % 2 == 0:
                        som_carta_jogador.play()
                    else:
                        som_carta_computador.play()

            else:
                etapa_distribuicao = 6
                progresso_distribuicao = 1.0

                # Inicia a revelação simultânea.
                if revelacao_inicio is None:
                    revelacao_inicio = agora

                elif agora - revelacao_inicio >= duracao_revelacao_atual:
                    distribuicao_ativa = False
                    mensagem = "Sua vez! Clique em uma carta."

        quantidade = len(partida.jogador.cartas)
        espacamento = 120
        inicio_x = (LARGURA - quantidade * espacamento) // 2

        # Posições finais das cartas.
        posicoes_jogador = [
            (inicio_x + i * espacamento, 480)
            for i in range(3)
        ]

        posicoes_computador = [
            (inicio_x + i * espacamento, 120)
            for i in range(3)
        ]

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
                not distribuicao_ativa
                and partida.quem_comeca_rodada == "computador"
                and not computador_ja_comecou
                and not aguardando_proxima
                and not partida.mao_encerrada
                and not partida.truco_pendente_computador
        ):
            resultado_inicio = partida.iniciar_rodada_computador()

            if isinstance(resultado_inicio, dict):
                carta_computador = resultado_inicio["carta_computador"]

                animacao_carta_computador_tempo = pygame.time.get_ticks()
                animacao_carta_computador_ativa = True
                animacao_giro_computador_inicio = None

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
                and pygame.time.get_ticks() - tempo_jogada >= 300
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
            carta_destaque = resultado["resultado"]
            tempo_inicio_destaque = None
            animacao_giro_computador_inicio = None
            animacao_carta_computador_tempo = pygame.time.get_ticks()
            animacao_carta_computador_ativa = True
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

        # Detectar mouse sobre os botões.
        botao_hover_atual = None
        pos_mouse = pygame.mouse.get_pos()

        if partida.truco_pendente_computador:

            if botao_aceitar.collidepoint(pos_mouse):
                botao_hover_atual = "aceitar"

            elif botao_correr.collidepoint(pos_mouse):
                botao_hover_atual = "correr"

        else:
            truco_disponivel = (
                    not partida.truco_pedido
                    and not partida.mao_encerrada
                    and not aguardando_proxima
                    and carta_jogador_pendente is None
            )

            if truco_disponivel and botao_truco.collidepoint(pos_mouse):
                botao_hover_atual = "truco"

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

            if distribuicao_ativa:
                continue

            if (
                    evento.type != pygame.MOUSEBUTTONDOWN
                    or evento.button != 1
            ):
                continue
                continue

            # Tela final: clique inicia nova partida.
            if encerrada:
                parar_falas()

                partida = Partida()
                truco_aceito_jogador = False

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
                    truco_aceito_jogador = False

                    # A partir da segunda mão, acelera a distribuição.
                    if primeira_distribuicao:
                        primeira_distribuicao = False

                        duracao_distribuicao_atual = 200
                        intervalo_distribuicao_atual = 50
                        duracao_revelacao_atual = 200

                    # Reinicia a animação de distribuição.
                    distribuicao_ativa = True
                    distribuicao_inicio = pygame.time.get_ticks()

                    indice_distribuicao = -1
                    etapa_distribuicao = 0
                    progresso_distribuicao = 0.0

                    revelacao_inicio = None

                    mensagem = "Distribuindo as cartas..."

                    carta_jogador = None
                    carta_computador = None
                    mensagem = "Nova mão! Distribuindo as cartas..."

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

                    if resultado_truco["status"] == "aceito":
                        truco_aceito_jogador = True

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

                    animacao_carta_jogador_inicio = (
                        inicio_x + indice * espacamento,
                        465
                    )

                    animacao_carta_jogador_tempo = pygame.time.get_ticks()

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
                    animacao_carta_jogador_inicio = (
                        inicio_x + indice * espacamento,
                        465
                    )
                    animacao_carta_jogador_tempo = pygame.time.get_ticks()
                    som_carta_jogador.play()

                    resultado = partida.concluir_rodada(
                        carta_jogador,
                        carta_computador,
                    )
                    carta_destaque = resultado["resultado"]
                    tempo_inicio_destaque = None

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

        # Logo do PYTRUCO.
        tela.blit(
            logo_partida,
            logo_partida.get_rect(
                center=(LARGURA // 2, 40)
            )
        )

        # Placar.
        placar_jogador = fonte_pequena.render(
            f"{partida.jogador.nome}: {partida.pontos_jogador}",
            True,
            BRANCO,
        )

        placar_computador = fonte_pequena.render(
            f"COMPUTADOR: {partida.pontos_computador}",
            True,
            BRANCO,
        )

        tela.blit(placar_jogador, (30, 10))
        tela.blit(placar_computador, (30, 35))

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
        # DISTRIBUIÇÃO DAS CARTAS
        # ==========================================

        if distribuicao_ativa:

            # Desenha o baralho à esquerda, no centro vertical.
            cartas_no_baralho = max(
                0,
                5 - etapa_distribuicao,
            )

            desenhar_baralho(
                tela,
                imagem_verso_carta,
                BARALHO_X,
                BARALHO_Y,
                cartas_no_baralho,
            )

            if (etapa_distribuicao < 6 and indice_distribuicao >= 0 and indice_distribuicao < 6):

                # Alterna entre jogador e computador.
                if indice_distribuicao % 2 == 0:
                    indice_destino = indice_distribuicao // 2
                    destino = posicoes_jogador[indice_destino]

                else:
                    indice_destino = indice_distribuicao // 2
                    destino = posicoes_computador[indice_destino]

                # Origem e destino usam o centro da carta.
                origem = (
                    BARALHO_X + 52,
                    BARALHO_Y + 72,
                )

                destino_centro = (
                    destino[0] + 50,
                    destino[1] + 72,
                )

                desenhar_carta_em_movimento(
                    tela,
                    imagem_verso_carta,
                    origem,
                    destino_centro,
                    progresso_distribuicao,
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

        # Quantidade de cartas que já chegaram ao computador.
        if distribuicao_ativa:
            quantidade_exibida = min(
                3,
                etapa_distribuicao // 2
            )
        else:
            quantidade_exibida = cartas_restantes_computador

        for indice in range(quantidade_exibida):
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

        # ==========================================
        # CONTROLE DO DESTAQUE DA CARTA VENCEDORA
        # ==========================================

        if (
                carta_destaque is not None
                and tempo_inicio_destaque is None
                and animacao_carta_jogador_inicio is None
                and not animacao_carta_computador_ativa
                and animacao_giro_computador_inicio is None
        ):
            tempo_inicio_destaque = pygame.time.get_ticks()

        if carta_destaque is not None and tempo_inicio_destaque is not None:

            tempo_destaque = (
                    pygame.time.get_ticks() - tempo_inicio_destaque
            )

            if tempo_destaque >= DURACAO_DESTAQUE_CARTA:
                carta_destaque = None
                tempo_inicio_destaque = None

        # Animação da carta do jogador
        if carta_jogador is not None:

            destino_x = centro_jogador - 50
            destino_y = 320

            if animacao_carta_jogador_inicio is not None:

                tempo_decorrido = (
                        pygame.time.get_ticks()
                        - animacao_carta_jogador_tempo
                )

                progresso = min(
                    1.0,
                    tempo_decorrido / DURACAO_ANIMACAO_CARTA
                )

                # Movimento suavizado
                progresso_suave = 1 - (1 - progresso) ** 3

                origem_x, origem_y = animacao_carta_jogador_inicio

                x_atual = int(
                    origem_x + (destino_x - origem_x) * progresso_suave
                )

                y_atual = int(
                    origem_y + (destino_y - origem_y) * progresso_suave
                )

                desenhar_carta(
                    tela,
                    carta_jogador,
                    x_atual,
                    y_atual,
                    imagens_cartas,
                )

                if progresso >= 1.0:
                    animacao_carta_jogador_inicio = None

            else:
                desenhar_carta(
                    tela,
                    carta_jogador,
                    destino_x,
                    destino_y,
                    imagens_cartas,
                )

        # ==========================================
        # ANIMAÇÃO DA CARTA DO COMPUTADOR
        # ==========================================

        if carta_computador is not None:

            destino_x = centro_computador - 50
            destino_y = 290

            # PRIMEIRA ETAPA: CARTA DESCENDO FECHADA
            if animacao_carta_computador_ativa:

                tempo_decorrido = (
                        pygame.time.get_ticks()
                        - animacao_carta_computador_tempo
                )

                progresso = min(
                    1.0,
                    tempo_decorrido / DURACAO_ANIMACAO_CARTA
                )

                progresso_suave = 1 - (1 - progresso) ** 3

                origem_y = 120

                y_atual = int(
                    origem_y + (destino_y - origem_y) * progresso_suave
                )

                desenhar_verso_carta(
                    tela,
                    imagem_verso_carta,
                    destino_x,
                    y_atual,
                )

                if progresso >= 1.0:
                    animacao_carta_computador_ativa = False
                    animacao_giro_computador_inicio = pygame.time.get_ticks()

            # SEGUNDA ETAPA: VIRAR E REVELAR A CARTA
            elif animacao_giro_computador_inicio is not None:

                tempo_decorrido = (
                        pygame.time.get_ticks()
                        - animacao_giro_computador_inicio
                )

                progresso = min(
                    1.0,
                    tempo_decorrido / DURACAO_GIRO_CARTA
                )

                # A largura diminui até o meio e depois aumenta.
                fator_largura = abs(math.cos(math.pi * progresso))

                largura_atual = max(
                    1,
                    int(100 * fator_largura)
                )

                x_atual = destino_x + (100 - largura_atual) // 2

                # No meio do giro, revela a face da carta.
                if progresso < 0.5:
                    desenhar_verso_carta(
                        tela,
                        imagem_verso_carta,
                        x_atual,
                        destino_y,
                        largura_atual,
                        145,
                    )
                else:
                    desenhar_carta(
                        tela,
                        carta_computador,
                        x_atual,
                        destino_y,
                        imagens_cartas,
                        largura_atual,
                        145,
                    )

                if progresso >= 1.0:
                    animacao_giro_computador_inicio = None

            # TERCEIRA ETAPA: CARTA REVELADA
            else:
                desenhar_carta(
                    tela,
                    carta_computador,
                    destino_x,
                    destino_y,
                    imagens_cartas,
                )

        # ==========================================
        # TEXTO FLUTUANTE DA CARTA VENCEDORA
        # ==========================================

        if carta_destaque is not None and tempo_inicio_destaque is not None:

            tempo_destaque = (
                    pygame.time.get_ticks() - tempo_inicio_destaque
            )

            if carta_destaque == "jogador":

                desenhar_texto_vencedor(
                    tela,
                    "Você venceu!",
                    fonte_texto_vencedor,
                    centro_jogador,
                    305,
                    tempo_destaque
                )

            elif carta_destaque == "computador":

                desenhar_texto_vencedor(
                    tela,
                    "Computador Venceu!",
                    fonte_texto_vencedor,
                    centro_computador + 15,
                    448,
                    tempo_destaque
                )

            elif carta_destaque == "empate":

                desenhar_texto_vencedor(
                    tela,
                    "Empate!",
                    fonte_texto_vencedor,
                    LARGURA // 2,
                    270,
                    tempo_destaque
                )

        # ==========================================
        # SUAS CARTAS DISPONÍVEIS
        # ==========================================

        pos_mouse = pygame.mouse.get_pos()
        carta_hover_atual = None

        for indice, carta in enumerate(partida.jogador.cartas):
            x = inicio_x + indice * espacamento
            y = 480

            retangulo = pygame.Rect(x, y, 100, 145)

            # Durante a distribuição, controla quais cartas já chegaram.
            if distribuicao_ativa:

                if etapa_distribuicao < 6:
                    cartas_distribuidas = (etapa_distribuicao + 1) // 2
                else:
                    cartas_distribuidas = 3

                # Ainda não chegou a vez desta carta.
                if indice >= cartas_distribuidas:
                    continue

                # Durante a revelação, todas viram simultaneamente.
                if etapa_distribuicao == 6:

                    progresso_revelacao = min(
                        1.0,
                        (pygame.time.get_ticks() - revelacao_inicio)
                        / duracao_revelacao_atual,
                    )

                    largura = max(
                        1,
                        int(100 * abs(math.cos(math.pi * progresso_revelacao))),
                    )

                    x_desenho = x + (100 - largura) // 2

                    if progresso_revelacao < 0.5:
                        desenhar_verso_carta(
                            tela,
                            imagem_verso_carta,
                            x_desenho,
                            y,
                            largura,
                            145,
                        )
                    else:
                        desenhar_carta(
                            tela,
                            carta,
                            x_desenho,
                            y,
                            imagens_cartas,
                            largura,
                            145,
                        )

                else:
                    # Carta já distribuída, mas ainda virada para baixo.
                    desenhar_verso_carta(
                        tela,
                        imagem_verso_carta,
                        x,
                        y,
                    )

                continue

            # Exibição normal após a distribuição.
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

            # Botão ACEITAR.
            if imagem_botao_confirmar:
                tela.blit(imagem_botao_confirmar, botao_aceitar)
            else:
                pygame.draw.rect(
                    tela, (35, 145, 65), botao_aceitar,
                    border_radius=8
                )

            cor_texto = (
                AMARELO
                if botao_hover_atual == "aceitar"
                else BRANCO
            )

            texto = fonte_pequena.render(
                "ACEITAR", True, cor_texto
            )

            tela.blit(
                texto,
                texto.get_rect(center=botao_aceitar.center),
            )

            # Botão CORRER.
            if imagem_botao:
                tela.blit(imagem_botao, botao_correr)
            else:
                pygame.draw.rect(
                    tela, (180, 45, 45), botao_correr,
                    border_radius=8
                )

            cor_texto = (
                AMARELO
                if botao_hover_atual == "correr"
                else BRANCO
            )

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

            # Escolhe a imagem e o texto do botão.

            if truco_aceito_jogador:
                imagem_atual = imagem_botao_aviso
                texto_botao = "TRUCO ACEITO!"
            else:
                imagem_atual = imagem_botao
                texto_botao = "PEDIR TRUCO"

            # Desenha o botão.

            if imagem_atual:

                tela.blit(imagem_atual, botao_truco)

            else:

                pygame.draw.rect(

                    tela, (180, 45, 45), botao_truco,

                    border_radius=8

                )

            # Cor do texto.

            cor_texto = (

                BRANCO

                if truco_aceito_jogador

                else AMARELO

                if botao_hover_atual == "truco"

                else BRANCO

            )

            texto = fonte_pequena.render(

                texto_botao, True, cor_texto

            )

            tela.blit(

                texto,

                texto.get_rect(center=botao_truco.center),

            )

        # Atalho para voltar ao menu.
        ajuda = fonte_pequena.render(
            "ESC: VOLTAR AO MENU", True, BRANCO
        )

        tela.blit(
            ajuda,
            (35, ALTURA - 7 - ajuda.get_height())
        )

        # Mensagem de orientação na parte inferior.
        texto_mensagem = fonte_pequena.render(mensagem.upper(), True, DOURADO)

        tela.blit(
            texto_mensagem,
            texto_mensagem.get_rect(
                center=(LARGURA // 2, ALTURA - 42)
            )
        )

        # Mensagem especial da primeira distribuição.
        if mostrar_boasorte:
            tempo_boasorte = pygame.time.get_ticks() - inicio_boasorte

            if tempo_boasorte < DURACAO_BOASORTE:
                texto_boasorte = fonte_boasorte.render(
                    "BOA SORTE!", True, DOURADO
                )

                # Sombra preta.
                sombra_boasorte = fonte_boasorte.render(
                    "BOA SORTE!", True, PRETO
                )

                alpha = int(255 * (1 - tempo_boasorte / DURACAO_BOASORTE))

                texto_boasorte.set_alpha(alpha)
                sombra_boasorte.set_alpha(alpha)

                posicao = texto_boasorte.get_rect(
                    center=(LARGURA // 2, ALTURA // 2)
                )

                tela.blit(sombra_boasorte, (posicao.x + 3, posicao.y + 3))
                tela.blit(texto_boasorte, posicao)

            else:
                mostrar_boasorte = False

        pygame.display.flip()
        relogio.tick(60)
