from pathlib import Path
import pygame
import numpy as np
import sounddevice as sd

from PIL import Image

from pedalboard import Pedalboard, Reverb
from pedalboard.io import AudioFile

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
    CAMINHO_FUNDO_PARTIDA,
    CAMINHO_FUNDO_ANIMADO,
    CAMINHO_FUNDO_PARTIDA2,
    CAMINHO_FUNDO_PARTIDA6,
    CAMINHO_FUNDO_PARTIDA1,
    CAMINHO_BOTAO,
    CAMINHO_BOTAO1,
    CAMINHO_BOTAO_CONFIRMAR,
    CAMINHO_MUSICA_MENU,
    CAMINHO_SOM_ROLLOVER,
    CAMINHO_SOM_CLICK,
    CAMINHO_SOM_TECLADO,
    CAMINHO_TELA_SCORE
)

from telas.partida import iniciar_partida

from logica.score import (
    inicializar_banco,
    buscar_melhores_partidas,
    buscar_melhores_sessoes
)

# ==================================================
# CONFIGURAÇÃO DO REVERB
# ==================================================

efeito_reverb = Pedalboard([
    Reverb(
        room_size=0.90,
        damping=0.35,
        wet_level=0.60,
        dry_level=0.40,
        width=1.0,
    )
])

# ==================================================
# REPRODUÇÃO DA MÚSICA COM REVERB
# ==================================================

_arquivo_creditos = None
_stream_creditos = None


def iniciar_musica_creditos_reverb():

    global _arquivo_creditos, _stream_creditos

    if not CAMINHO_MUSICA_MENU.exists():
        print(f"Música não encontrada: {CAMINHO_MUSICA_MENU}")
        return

    _arquivo_creditos = AudioFile(str(CAMINHO_MUSICA_MENU))
    _arquivo_creditos.seek(
        int(posicao_musica_menu * _arquivo_creditos.samplerate)
    )

    taxa_amostragem = _arquivo_creditos.samplerate
    canais = _arquivo_creditos.num_channels

    efeito_reverb.reset()

    def reproduzir_audio(outdata, frames, tempo, status):

        blocos = []
        restantes = frames

        while restantes > 0:

            bloco = _arquivo_creditos.read(restantes)

            if bloco.shape[1] == 0:
                _arquivo_creditos.seek(0)
                continue

            blocos.append(bloco)
            restantes -= bloco.shape[1]

        audio = np.concatenate(blocos, axis=1)

        audio_processado = efeito_reverb(
            audio,
            taxa_amostragem,
            reset=False
        )

        audio_processado *= 0.10

        outdata[:] = audio_processado.T

    _stream_creditos = sd.OutputStream(
        samplerate=taxa_amostragem,
        channels=canais,
        dtype="float32",
        blocksize=1024,
        callback=reproduzir_audio
    )

    _stream_creditos.start()


def parar_musica_creditos_reverb():

    global _arquivo_creditos, _stream_creditos, posicao_musica_menu

    if _stream_creditos is not None:
        _stream_creditos.stop()
        _stream_creditos.close()
        _stream_creditos = None

    if _arquivo_creditos is not None:
        posicao_musica_menu = (
                _arquivo_creditos.tell() / _arquivo_creditos.samplerate
        )

    if _arquivo_creditos is not None:
        _arquivo_creditos.close()
        _arquivo_creditos = None

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


def carregar_fundo_menu():
    if not CAMINHO_FUNDO_MENU.exists():
        print(f"Fundo do menu não encontrado: {CAMINHO_FUNDO_MENU}")
        return None

    imagem = pygame.image.load(
        str(CAMINHO_FUNDO_MENU)
    ).convert()

    return pygame.transform.scale(
        imagem,
        (LARGURA, ALTURA)
    )

def carregar_fundo_score():
    if not CAMINHO_TELA_SCORE.exists():
        print(f"Fundo do SCORE não encontrado: {CAMINHO_TELA_SCORE}")
        return None

    imagem = pygame.image.load(
        str(CAMINHO_TELA_SCORE)
    ).convert()

    return pygame.transform.scale(
        imagem,
        (LARGURA, ALTURA)
    )

def carregar_fundo_identificacao():
    if not CAMINHO_FUNDO_PARTIDA1.exists():
        print(
            f"Fundo de identificação não encontrado: "
            f"{CAMINHO_FUNDO_PARTIDA1}"
        )
        return None

    imagem = pygame.image.load(
        str(CAMINHO_FUNDO_PARTIDA1)
    ).convert()

    return pygame.transform.scale(
        imagem,
        (LARGURA, ALTURA)
    )

def carregar_fundo_regras():
    if not CAMINHO_FUNDO_PARTIDA6.exists():
        print(
            f"Fundo das regras não encontrado: "
            f"{CAMINHO_FUNDO_PARTIDA6}"
        )
        return None

    imagem = pygame.image.load(
        str(CAMINHO_FUNDO_PARTIDA6)
    ).convert()

    return pygame.transform.scale(
        imagem,
        (LARGURA, ALTURA)
    )

def carregar_fundo_credits():
    if not CAMINHO_FUNDO_PARTIDA2.exists():
        print(f"Fundo do SCORE não encontrado: {CAMINHO_FUNDO_PARTIDA2}")
        return None

    imagem = pygame.image.load(
        str(CAMINHO_FUNDO_PARTIDA2)
    ).convert()

    return pygame.transform.scale(
        imagem,
        (LARGURA, ALTURA)
    )


def mostrar_fade_transicao(tela, relogio):
    imagem_menu = tela.copy()

    duracao_fade = 1000
    inicio = pygame.time.get_ticks()

    sombra = pygame.Surface((LARGURA, ALTURA))
    sombra.fill((0, 0, 0))

    while True:
        tempo = pygame.time.get_ticks() - inicio

        if tempo >= duracao_fade:
            break

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return False

        progresso = tempo / duracao_fade
        transparencia = int(255 * progresso)

        tela.blit(imagem_menu, (0, 0))

        sombra.set_alpha(transparencia)
        tela.blit(sombra, (0, 0))

        pygame.display.flip()
        relogio.tick(FPS)

    tela.blit(imagem_menu, (0, 0))
    sombra.set_alpha(255)
    tela.blit(sombra, (0, 0))
    pygame.display.flip()

    return True


def animar_tela_deslizante(
        tela, relogio, imagem_origem, imagem_destino,
        direcao=1, duracao=400
):

    inicio = pygame.time.get_ticks()

    while True:

        tempo = pygame.time.get_ticks() - inicio
        progresso = min(tempo / duracao, 1)

        deslocamento = int(LARGURA * progresso)

        tela.blit(
            imagem_origem,
            (-direcao * deslocamento, 0)
        )

        tela.blit(
            imagem_destino,
            (direcao * (LARGURA - deslocamento), 0)
        )

        pygame.display.flip()
        relogio.tick(FPS)

        if progresso >= 1:
            break


def carregar_imagem_botao():
    if not CAMINHO_BOTAO.exists():
        print(f"Botão não encontrado: {CAMINHO_BOTAO}")
        return None

    return pygame.image.load(
        str(CAMINHO_BOTAO)
    ).convert_alpha()

def carregar_imagem_botao1():
    if not CAMINHO_BOTAO1.exists():
        print(f"Botão 1 não encontrado: {CAMINHO_BOTAO1}")
        return None

    return pygame.image.load(
        str(CAMINHO_BOTAO1)
    ).convert_alpha()

def carregar_imagem_botao_confirmar():
    if not CAMINHO_BOTAO_CONFIRMAR.exists():
        print(
            f"Botão confirmar não encontrado: "
            f"{CAMINHO_BOTAO_CONFIRMAR}"
        )
        return None

    return pygame.image.load(
        str(CAMINHO_BOTAO_CONFIRMAR)
    ).convert_alpha()



def carregar_gif_creditos():
    if not CAMINHO_FUNDO_ANIMADO.exists():
        print(f"GIF dos créditos não encontrado: {CAMINHO_FUNDO_ANIMADO}")
        return []

    gif = Image.open(str(CAMINHO_FUNDO_ANIMADO))

    quadros = []

    for indice in range(gif.n_frames):
        gif.seek(indice)

        imagem = gif.convert("RGBA")

        quadro = pygame.image.fromstring(
            imagem.tobytes(),
            imagem.size,
            "RGBA"
        )

        quadro = pygame.transform.scale(
            quadro,
            (LARGURA, ALTURA)
        )

        duracao = gif.info.get("duration", 100)

        quadros.append((quadro, duracao))

    return quadros




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

def desenhar_texto_justificado(
        tela, texto, fonte, cor, area, espacamento_linhas=20
):

    paragrafos = texto.split("\n\n")
    y = area.y

    for paragrafo in paragrafos:

        palavras = paragrafo.split()
        linhas = []
        linha_atual = []

        for palavra in palavras:

            teste = linha_atual + [palavra]
            largura = fonte.size(" ".join(teste))[0]

            if largura <= area.width:
                linha_atual.append(palavra)
            else:
                if linha_atual:
                    linhas.append(linha_atual)

                linha_atual = [palavra]

        if linha_atual:
            linhas.append(linha_atual)

        for indice, linha in enumerate(linhas):

            largura_palavras = sum(
                fonte.size(palavra)[0]
                for palavra in linha
            )

            if indice < len(linhas) - 1 and len(linha) > 1:
                espaco = (
                    area.width - largura_palavras
                ) / (len(linha) - 1)
            else:
                espaco = fonte.size(" ")[0]

            x = area.x

            for palavra in linha:

                imagem = fonte.render(
                    palavra,
                    True,
                    cor
                )

                tela.blit(imagem, (int(x), y))
                x += fonte.size(palavra)[0] + espaco

            y += espacamento_linhas

        y += espacamento_linhas


def mostrar_regras(tela, fonte_titulo, fonte_texto, fundo):

    if fundo:
        tela.blit(fundo, (0, 0))
    else:
        tela.fill(VERDE_MESA)



    # Título principal.
    titulo = fonte_titulo.render(
        "COMO JOGAR?",
        True,
        DOURADO
    )

    tela.blit(
        titulo,
        titulo.get_rect(center=(LARGURA // 2, 110))
    )

    # Títulos das duas colunas.
    titulo_instrucoes = fonte_texto.render(
        "REGRAS BÁSICAS",
        True,
        DOURADO
    )

    titulo_hierarquia = fonte_texto.render(
        "HIERARQUIA DAS CARTAS",
        True,
        DOURADO
    )

    tela.blit(titulo_instrucoes, (110, 190))
    tela.blit(titulo_hierarquia, (620, 190))

    # Instruções básicas em texto corrido.

    texto_regras = (
        "O objetivo do PYTRUCO é ser o primeiro a "
        "alcançar 12 pontos. Para isso, você enfrentará "
        "o computador em uma disputa de cartas que exige "
        "estratégia e boas escolhas.\n\n"

        "Cada jogador recebe três cartas por mão. Em "
        "cada rodada, ambos escolhem uma carta. A carta "
        "mais forte vence, seguindo a hierarquia ao lado.\n\n"

        "Uma mão pode ter até três rodadas. O vencedor "
        "das disputas conquista os pontos da mão.\n\n"

        "Você também pode pedir TRUCO para aumentar "
        "o valor da mão. O adversário poderá aceitar "
        "a aposta ou correr. Quanto maior a "
        "aposta aceita, maior será a pontuação em jogo."
    )

    area_texto = pygame.Rect(
        100,
        230,
        490,
        350
    )

    desenhar_texto_justificado(
        tela,
        texto_regras,
        fonte_texto,
        BRANCO,
        area_texto,
        18
    )

    # Hierarquia das cartas.
    hierarquia = [
        (14, "1 de Espadas"),
        (13, "1 de Bastos"),
        (12, "7 de Espadas"),
        (11, "7 de Ouros"),
        (10, "Todos os 3"),
        (9, "Todos os 2"),
        (8, "1 de Copas e Ouros"),
        (7, "Todos os Reis (12)"),
        (6, "Todos os Valetes (11)"),
        (5, "Todos os 10"),
        (4, "7 de Copas e Bastos"),
        (3, "Todos os 6"),
        (2, "Todos os 5"),
        (1, "Todos os 4"),
    ]

    for indice, (forca, descricao) in enumerate(hierarquia):

        texto = f"{forca:02d} - {descricao}"

        linha = fonte_texto.render(
            texto,
            True,
            BRANCO
        )

        tela.blit(
            linha,
            (620, 225 + indice * 26)
        )

    # Instrução para voltar.
    voltar = fonte_texto.render(
        "Pressione ESC para voltar ao menu.",
        True,
        DOURADO
    )

    tela.blit(
        voltar,
        voltar.get_rect(center=(LARGURA // 2, 676))
    )


# ==================================================
# TELA DE CRÉDITOS
# ==================================================



def mostrar_creditos(tela, fonte_titulo, fonte_texto, fundo, quadros_gif):
    if quadros_gif:

        tempo_atual = pygame.time.get_ticks()

        duracao_total = sum(
            duracao for _, duracao in quadros_gif
        )

        tempo_gif = tempo_atual % duracao_total

        tempo_acumulado = 0

        for quadro, duracao in quadros_gif:

            tempo_acumulado += duracao

            if tempo_gif < tempo_acumulado:
                tela.blit(quadro, (0, 0))
                break

    else:
        tela.fill(VERDE_MESA)

    painel = pygame.Surface(
        (LARGURA, ALTURA),
        pygame.SRCALPHA
    )

    painel.fill((15, 30, 18, 110))

    tela.blit(painel, (0, 0))



    titulo = fonte_titulo.render(
        "Créditos",
        True,
        DOURADO,
    )

    tela.blit(
        titulo,
        titulo.get_rect(center=(LARGURA // 2, 75)),
    )

    secoes = [
        (
            "SOBRE O PROJETO",
            [
                "O PYTRUCO é um projeto desenvolvido por",
                "Fernando Dierings, como parte dos estudos",
                "em Programação Aplicada. Foi idealizado",
                "para unir o aprendizado do desenvolvimento",
                "de software à tradição gaúcha, trazendo",
                "personalidade e cultura do Rio Grande do Sul.",
            ],
        ),
        (
            "TECNOLOGIAS UTILIZADAS",
            [
                "Python, Pygame e SQLite.",
            ],
        ),
        (
            "AGRADECIMENTOS",
            [
                "O desenvolvimento deste projeto foi uma",
                "oportunidade de transformar conhecimentos",
                "em uma experiência divertida, unindo",
                "programação, criatividade e interatividade.",
                "",
                "Agradeço também aos professores que, por",
                "meio de seus ensinamentos, incentivo e",
                "dedicação, motivam-nos a buscar a realização",
                "dos nossos sonhos!",
            ],
        ),
        (
            "AGRADECIMENTOS ESPECIAIS",
            [
                "À comunidade do Discord DOGELAND,",
                "pela amizade, convivência e inspiração.",
                "",
                "À minha amada Laissa, pelo companheirismo,",
                "apoio e por fazer parte desta caminhada.",
            ],
        ),
        (
            "",
            [
                "",
                "OBRIGADO POR JOGAR PYTRUCO!",
                "Que não faltem boas cartas e boas disputas!",
            ],
        ),
    ]

    linhas = []

    for titulo_secao, textos in secoes:
        if titulo_secao:
            linhas.append((titulo_secao, DOURADO, 30))

        for texto in textos:
            cor = (
                DOURADO
                if texto == "OBRIGADO POR JOGAR PYTRUCO!"
                else BRANCO
            )

            linhas.append((texto, cor, 25))

        linhas.append(("", BRANCO, 18))

    altura_total = sum(espaco for _, _, espaco in linhas)

    area = pygame.Rect(0, 120, LARGURA, 490)

    tempo = pygame.time.get_ticks() / 1000

    velocidade = 25

    deslocamento = (
        tempo * velocidade
    ) % (area.height + altura_total)

    y = area.bottom - deslocamento

    tela.set_clip(area)

    for texto, cor, espaco in linhas:

        if texto:
            linha = fonte_texto.render(
                texto,
                True,
                cor,
            )

            tela.blit(
                linha,
                linha.get_rect(
                    center=(LARGURA // 2, int(y))
                ),
            )

        y += espaco

    tela.set_clip(None)

    aviso = fonte_texto.render(
        "Pressione ESC para voltar ao menu.",
        True,
        DOURADO,
    )

    tela.blit(
        aviso,
        aviso.get_rect(
            center=(LARGURA // 2, 676)
        ),
    )


def mostrar_score(tela, fonte_titulo, fonte_texto, fundo):

    if fundo:
        tela.blit(fundo, (0, 0))
    else:
        tela.fill(VERDE_MESA)



    partidas = buscar_melhores_partidas()
    sessoes = buscar_melhores_sessoes()



    # Título principal.
    titulo = fonte_titulo.render("SCORE", True, DOURADO)

    tela.blit(
        titulo,
        titulo.get_rect(center=(LARGURA // 2, 65))
    )

    # Títulos dos rankings.
    titulo_partidas = fonte_texto.render(
        "TOP 10 PARTIDAS",
        True,
        DOURADO
    )

    titulo_sessoes = fonte_texto.render(
        "TOP 10 SESSOES",
        True,
        DOURADO
    )

    tela.blit(
        titulo_partidas,
        titulo_partidas.get_rect(center=(300, 145))
    )

    tela.blit(
        titulo_sessoes,
        titulo_sessoes.get_rect(center=(700, 145))
    )

    # Ranking de partidas individuais.
    if not partidas:
        texto = fonte_texto.render(
            "NENHUMA VITORIA REGISTRADA",
            True,
            BRANCO
        )
        tela.blit(texto, (65, 200))

    else:
        for indice, (nome, score, data) in enumerate(partidas):

            y = 190 + indice * 40

            linha = f"{indice + 1}. {nome[:12]}  {score} PTS"

            texto = fonte_texto.render(
                linha,
                True,
                BRANCO
            )

            tela.blit(
                texto,
                texto.get_rect(center=(300, y + 8))
            )

            data_texto = fonte_texto.render(
                data,
                True,
                (190, 190, 190)
            )

            tela.blit(
                data_texto,
                data_texto.get_rect(center=(300, y + 25))
            )

    # Ranking de sessões.
    if not sessoes:
        texto = fonte_texto.render(
            "NENHUMA SESSAO REGISTRADA",
            True,
            BRANCO
        )
        tela.blit(texto, (550, 200))

    else:
        for indice, (
            nome,
            score_total,
            quantidade_vitorias,
            media_score,
            data_inicio,
            data_fim
        ) in enumerate(sessoes):

            y = 190 + indice * 40

            linha = (
                f"{indice + 1}. {nome[:10]} "
                f"{score_total} PTS"
            )

            texto = fonte_texto.render(
                linha,
                True,
                BRANCO
            )

            tela.blit(
                texto,
                texto.get_rect(center=(700, y + 8))
            )

            detalhes = (
                f"{quantidade_vitorias} VIT. "
                f"MEDIA: {media_score:.0f}"
            )

            texto_detalhes = fonte_texto.render(
                detalhes,
                True,
                (190, 190, 190)
            )

            tela.blit(
                texto_detalhes,
                texto_detalhes.get_rect(center=(700, y + 25))
            )


# ==================================================
# TELA DE IDENTIFICAÇÃO DO JOGADOR
# ==================================================

def mostrar_tela_nome(
    tela,
    relogio,
    fundo,
    logo,
    fonte_texto,
    fonte_botao,
    imagem_botao,
    imagem_botao_confirmar,
    som_click,
    som_teclado,
    imagem_origem
):
    nome = ""


    campo_nome = pygame.Rect(
        LARGURA // 2 - 250,
        330,
        500,
        60,
    )

    botao_confirmar = pygame.Rect(
        LARGURA // 2 + 15,
        440,
        190,
        55,
    )

    botao_voltar = pygame.Rect(
        LARGURA // 2 - 205,
        440,
        190,
        55,
    )

    pygame.key.start_text_input()

    executando = True
    transicao_iniciada = False

    while executando:
        mouse_pos = pygame.mouse.get_pos()

        for evento in pygame.event.get():

            if evento.type == pygame.QUIT:
                pygame.key.stop_text_input()
                return None, True


            elif evento.type == pygame.TEXTINPUT:

                if len(nome) < 16:
                    nome += evento.text

                    som_teclado.play()

            elif evento.type == pygame.KEYDOWN:

                if evento.key == pygame.K_BACKSPACE:
                    nome = nome[:-1]

                elif evento.key == pygame.K_RETURN and nome.strip():
                    pygame.key.stop_text_input()
                    return nome.strip(), False

                elif evento.key == pygame.K_ESCAPE:
                    pygame.key.stop_text_input()
                    return None, False

            elif (
                evento.type == pygame.MOUSEBUTTONDOWN
                and evento.button == 1
            ):

                if botao_confirmar.collidepoint(evento.pos):
                    if nome.strip():
                        som_click.play()
                        pygame.key.stop_text_input()
                        return nome.strip(), False

                elif botao_voltar.collidepoint(evento.pos):
                    som_click.play()
                    pygame.key.stop_text_input()
                    return None, False

        # Fundo.
        if fundo:
            tela.blit(fundo, (0, 0))
        else:
            tela.fill(VERDE_MESA)

        # Logo centralizada.
        tela.blit(
            logo,
            logo.get_rect(
                center=(LARGURA // 2, 220)
            ),
        )

        # Instrução.
        instrucao = fonte_texto.render(
            "",
            True,
            DOURADO,
        )

        tela.blit(
            instrucao,
            instrucao.get_rect(
                center=(LARGURA // 2, 285)
            ),
        )

        # Campo de nome com fundo preto transparente.
        campo_transparente = pygame.Surface(
            (campo_nome.width, campo_nome.height),
            pygame.SRCALPHA
        )

        campo_transparente.fill((0, 0, 0, 150))

        tela.blit(campo_transparente, campo_nome.topleft)

        pygame.draw.rect(
            tela,
            DOURADO,
            campo_nome,
            2,
        )


        texto_nome = nome if nome else "DIGITE SEU NOME:"

        cor_nome = BRANCO if nome else (150, 150, 150)

        superficie_nome = fonte_botao.render(
            texto_nome,
            True,
            cor_nome,
        )

        tela.blit(
            superficie_nome,
            superficie_nome.get_rect(
                center=campo_nome.center
            ),
        )

        # Botões.
        desenhar_botao(
            tela,
            "CONFIRMAR",
            botao_confirmar,
            fonte_botao,
            mouse_pos,
            imagem_botao_confirmar,
        )

        desenhar_botao(
            tela,
            "VOLTAR",
            botao_voltar,
            fonte_botao,
            mouse_pos,
            imagem_botao,
        )

        # Transição de entrada na identificação.
        if not transicao_iniciada:
            imagem_destino = tela.copy()

            animar_tela_deslizante(
                tela,
                relogio,
                imagem_origem,
                imagem_destino,
                direcao=1
            )

            transicao_iniciada = True

        pygame.display.flip()
        relogio.tick(FPS)

    pygame.key.stop_text_input()
    return None, False


# ==================================================
# MÚSICA DO MENU
# ==================================================
posicao_musica_menu = 0


def iniciar_musica_menu(posicao=0):
    if not CAMINHO_MUSICA_MENU.exists():
        print(f"Música não encontrada: {CAMINHO_MUSICA_MENU}")
        return

    pygame.mixer.music.load(str(CAMINHO_MUSICA_MENU))
    pygame.mixer.music.set_volume(0.10)
    pygame.mixer.music.play(-1, start=posicao)


def parar_musica_menu():
    global posicao_musica_menu

    posicao_atual = pygame.mixer.music.get_pos()

    if posicao_atual >= 0:
        posicao_musica_menu += posicao_atual / 1000

    pygame.mixer.music.stop()


# ==================================================
# EFEITOS SONOROS DO MENU
# ==================================================

def carregar_sons_menu():
    som_rollover = pygame.mixer.Sound(
        str(CAMINHO_SOM_ROLLOVER)
    )

    som_click = pygame.mixer.Sound(
        str(CAMINHO_SOM_CLICK)
    )

    som_rollover.set_volume(0.03)
    som_click.set_volume(0.5)

    return som_rollover, som_click

def carregar_som_teclado():
    som = pygame.mixer.Sound(str(CAMINHO_SOM_TECLADO))
    som.set_volume(0.15)
    return som


# ==================================================
# MENU PRINCIPAL
# ==================================================

def iniciar_jogo():
    inicializar_banco()
    pygame.init()

    iniciar_musica_menu()
    som_teclado = carregar_som_teclado()
    som_rollover, som_click = carregar_sons_menu()

    tela = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption(TITULO)

    relogio = pygame.time.Clock()

    fonte_botao = pygame.font.Font(CAMINHO_FONTE, 14)
    fonte_titulo = pygame.font.Font(CAMINHO_FONTE, 36)
    fonte_texto = pygame.font.Font(CAMINHO_FONTE, 12)

    # Carregar imagens.
    logo = carregar_logo()
    fundo_menu = carregar_fundo_menu()
    fundo_score = carregar_fundo_score()
    fundo_credits = carregar_fundo_credits()
    quadros_gif_creditos = carregar_gif_creditos()
    fundo_identificacao = carregar_fundo_identificacao()
    fundo_regras = carregar_fundo_regras()
    imagem_botao = carregar_imagem_botao()
    imagem_botao1 = carregar_imagem_botao1()
    imagem_botao_confirmar = carregar_imagem_botao_confirmar()

    # Posições dos botões.
    botao_jogar = pygame.Rect(
        LARGURA // 2 - 150, 300, 300, 50
    )

    botao_regras = pygame.Rect(
        LARGURA // 2 - 150, 360, 300, 50
    )

    botao_score = pygame.Rect(
        LARGURA // 2 - 150, 420, 300, 50
    )

    botao_creditos = pygame.Rect(
        LARGURA // 2 - 150, 480, 300, 50
    )

    botao_sair = pygame.Rect(
        LARGURA // 2 - 150, 540, 300, 50
    )

    botao_voltar_score = pygame.Rect(
        LARGURA // 2 - 110, 630, 220, 50
    )

    tela_atual = "menu"
    executando = True
    mouse_sobre_botao = None

    # Controle da transição entre telas.
    imagem_transicao_origem = None
    imagem_transicao_destino = None
    inicio_transicao = 0
    direcao_transicao = 1
    duracao_transicao = 300

    nome_jogador = None

    while executando:
        mouse_pos = pygame.mouse.get_pos()

        # Verifica em qual botão o mouse está.
        botao_atual = None

        if tela_atual == "menu":
            if botao_jogar.collidepoint(mouse_pos):
                botao_atual = "jogar"
            elif botao_regras.collidepoint(mouse_pos):
                botao_atual = "regras"
            elif botao_creditos.collidepoint(mouse_pos):
                botao_atual = "creditos"
            elif botao_score.collidepoint(mouse_pos):
                botao_atual = "score"
            elif botao_sair.collidepoint(mouse_pos):
                botao_atual = "sair"

        elif tela_atual == "score":
            if botao_voltar_score.collidepoint(mouse_pos):
                botao_atual = "voltar_score"

        if botao_atual != mouse_sobre_botao:
            if botao_atual is not None:
                som_rollover.play()

            mouse_sobre_botao = botao_atual

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

                    if (
                            botao_jogar.collidepoint(evento.pos)
                            or botao_regras.collidepoint(evento.pos)
                            or botao_sair.collidepoint(evento.pos)
                            or botao_creditos.collidepoint(evento.pos)
                            or botao_score.collidepoint(evento.pos)
                    ):
                        som_click.play()

                    if botao_jogar.collidepoint(evento.pos):

                        # Solicita o nome somente na primeira vez.
                        if nome_jogador is None:

                            nome_escolhido, fechar_jogo = mostrar_tela_nome(
                                tela,
                                relogio,
                                fundo_identificacao,
                                logo,
                                fonte_texto,
                                fonte_botao,
                                imagem_botao,
                                imagem_botao_confirmar,
                                som_click,
                                som_teclado,
                                tela.copy()
                            )

                            if fechar_jogo:
                                executando = False
                                continue

                            if nome_escolhido is None:
                                continue

                            nome_jogador = nome_escolhido

                        transicao_concluida = mostrar_fade_transicao(
                            tela,
                            relogio
                        )

                        if not transicao_concluida:
                            executando = False
                            continue

                        parar_musica_menu()

                        resultado = iniciar_partida(
                            tela,
                            relogio,
                            nome_jogador
                        )

                        if resultado == "sair":
                            executando = False
                            break
                        else:
                            iniciar_musica_menu()



                    elif botao_regras.collidepoint(evento.pos):

                        imagem_transicao_origem = tela.copy()

                        inicio_transicao = pygame.time.get_ticks()

                        direcao_transicao = 1

                        tela_atual = "regras"



                    elif botao_creditos.collidepoint(evento.pos):

                        parar_musica_menu()

                        iniciar_musica_creditos_reverb()

                        imagem_transicao_origem = tela.copy()

                        inicio_transicao = pygame.time.get_ticks()

                        direcao_transicao = 1

                        tela_atual = "creditos"


                    elif botao_score.collidepoint(evento.pos):

                        imagem_transicao_origem = tela.copy()

                        inicio_transicao = pygame.time.get_ticks()

                        direcao_transicao = 1

                        tela_atual = "score"


                    elif botao_sair.collidepoint(evento.pos):
                        executando = False


                elif tela_atual == "score":

                    if botao_voltar_score.collidepoint(evento.pos):
                        som_click.play()

                        imagem_transicao_origem = tela.copy()

                        inicio_transicao = pygame.time.get_ticks()

                        direcao_transicao = -1

                        tela_atual = "menu"



            elif evento.type == pygame.KEYDOWN:

                if (

                        evento.key == pygame.K_ESCAPE

                        and tela_atual in ("regras", "creditos", "score")

                ):

                    if tela_atual == "creditos":
                        parar_musica_creditos_reverb()
                        iniciar_musica_menu(posicao_musica_menu)

                    imagem_transicao_origem = tela.copy()

                    inicio_transicao = pygame.time.get_ticks()

                    direcao_transicao = -1

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
                tela, "PLAY", botao_jogar,
                fonte_botao, mouse_pos, imagem_botao
            )

            desenhar_botao(
                tela, "HOW TO PLAY", botao_regras,
                fonte_botao, mouse_pos, imagem_botao
            )

            desenhar_botao(
                tela, "CREDITS", botao_creditos,
                fonte_botao, mouse_pos, imagem_botao
            )

            desenhar_botao(
                tela, "SCORE", botao_score,
                fonte_botao, mouse_pos, imagem_botao
            )

            desenhar_botao(
                tela, "EXIT", botao_sair,
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
                fundo_regras,
            )



        elif tela_atual == "creditos":

            mostrar_creditos(
                tela,
                fonte_titulo,
                fonte_texto,
                fundo_credits,
                quadros_gif_creditos,

            )


        elif tela_atual == "score":

            mostrar_score(
                tela,
                fonte_titulo,
                fonte_texto,
                fundo_score,
            )

            desenhar_botao(
                tela,
                "VOLTAR",
                botao_voltar_score,
                fonte_botao,
                mouse_pos,
                imagem_botao1,
            )

        # ------------------------------------------
        # ANIMAÇÃO DE TRANSIÇÃO ENTRE TELAS
        # ------------------------------------------

        if imagem_transicao_origem is not None:

            tempo_atual = pygame.time.get_ticks()
            progresso = (
                                tempo_atual - inicio_transicao
                        ) / duracao_transicao

            progresso = min(progresso, 1)

            imagem_transicao_destino = tela.copy()

            deslocamento = int(LARGURA * progresso)

            tela.fill((0, 0, 0))

            tela.blit(
                imagem_transicao_origem,
                (-direcao_transicao * deslocamento, 0)
            )

            tela.blit(
                imagem_transicao_destino,
                (
                    direcao_transicao * (LARGURA - deslocamento),
                    0
                )
            )

            if progresso >= 1:
                imagem_transicao_origem = None

        pygame.display.flip()
        relogio.tick(FPS)

    parar_musica_creditos_reverb()
    pygame.mixer.music.stop()
    pygame.quit()


if __name__ == "__main__":
    iniciar_jogo()
