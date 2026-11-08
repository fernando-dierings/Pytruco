from PIL import Image, ImageSequence, ImageOps

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
    CAMINHO_TELA_CARREGAMENTO,
    CAMINHO_BOTAO,
    CAMINHO_MUSICA_MENU,
    CAMINHO_SOM_ROLLOVER,
    CAMINHO_SOM_CLICK,
    CAMINHO_VOZ_CARREGAMENTO
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


# ==================================================
# TELA DE CARREGAMENTO ANIMADA
# ==================================================

def carregar_gif_carregamento():
    if not CAMINHO_TELA_CARREGAMENTO.exists():
        print(
            f"GIF não encontrado: {CAMINHO_TELA_CARREGAMENTO}"
        )
        return []

    quadros = []

    with Image.open(CAMINHO_TELA_CARREGAMENTO) as gif:
        for quadro in ImageSequence.Iterator(gif):
            imagem = ImageOps.fit(
                quadro.convert("RGBA"),
                (LARGURA, ALTURA),
                method=Image.Resampling.LANCZOS
            )

            superficie = pygame.image.fromstring(
                imagem.tobytes(),
                imagem.size,
                "RGBA"
            ).convert_alpha()

            duracao = max(
                20,
                int(quadro.info.get("duration", 100))
            )

            quadros.append((superficie, duracao))

    return quadros


def mostrar_transicao(tela, relogio, quadros, fonte_titulo):
    if not quadros:
        return True

    # Guarda uma imagem do menu atual.
    imagem_menu = tela.copy()

    duracao_fade = 1200
    duracao_gif = 11000

    def desenhar_legenda(tela, fonte, tempo):
        legendas = [
            (0.0, 2.0, "Senta aí, vivente!"),
            (2.0, 4.0, "Puxa teu banquinho,"),
            (4.0, 6.0, "pega o teu mate e vamos ver"),
            (6.0, 9.0, "se o teu baralho é bom mesmo... ou se tu só fala fiado!")
        ]

        texto_atual = ""
        inicio_trecho = 0

        for inicio, fim, texto in legendas:
            if inicio <= tempo < fim:
                texto_atual = texto
                inicio_trecho = inicio
                break

        if not texto_atual:
            return

        # Efeito de digitação
        progresso = min(1.0, (tempo - inicio_trecho) / 0.8)
        quantidade_letras = int(len(texto_atual) * progresso)
        texto_parcial = texto_atual[:quantidade_letras]

        # Fonte da legenda
        fonte_legenda = pygame.font.Font(CAMINHO_FONTE, 14)

        texto_renderizado = fonte_legenda.render(
            texto_parcial,
            True,
            DOURADO
        )

        # Dimensões do fundo conforme o texto
        largura_caixa = texto_renderizado.get_width() + 40
        altura_caixa = texto_renderizado.get_height() + 25

        caixa = pygame.Surface(
            (largura_caixa, altura_caixa),
            pygame.SRCALPHA
        )
        caixa.fill((0, 0, 0, 180))

        pos_x = (LARGURA - largura_caixa) // 2
        pos_y = ALTURA - 100

        tela.blit(caixa, (pos_x, pos_y))

        # Centraliza o texto no fundo
        texto_rect = texto_renderizado.get_rect(
            center=(LARGURA // 2, pos_y + altura_caixa // 2)
        )

        tela.blit(texto_renderizado, texto_rect)

    # ------------------------------------------
    # 1. ESCURECER O MENU
    # ------------------------------------------

    inicio = pygame.time.get_ticks()

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

        sombra = pygame.Surface(
            (LARGURA, ALTURA)
        )
        sombra.fill((0, 0, 0))
        sombra.set_alpha(transparencia)

        tela.blit(sombra, (0, 0))

        pygame.display.flip()
        relogio.tick(FPS)

    voz_carregamento = pygame.mixer.Sound(
        str(CAMINHO_VOZ_CARREGAMENTO)
    )

    voz_carregamento.set_volume(1.0)
    voz_carregamento.play()
    # ------------------------------------------
    # 2. EXIBIR O GIF ANIMADO
    # ------------------------------------------

    inicio_audio = pygame.time.get_ticks()
    duracao_total_quadros = sum(
        duracao for _, duracao in quadros
    )

    inicio = pygame.time.get_ticks()

    while True:
        tempo = pygame.time.get_ticks() - inicio

        if tempo >= duracao_gif:
            break

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return False

        # Descobrir qual quadro do GIF deve aparecer.
        tempo_gif = tempo % duracao_total_quadros

        quadro_atual = quadros[0][0]

        for imagem, duracao in quadros:
            if tempo_gif < duracao:
                quadro_atual = imagem
                break

            tempo_gif -= duracao

        tela.blit(quadro_atual, (0, 0))
        tempo_audio = (pygame.time.get_ticks() - inicio_audio) / 1000

        desenhar_legenda(
            tela,
            fonte_titulo,
            tempo_audio
        )

        # Fade de entrada e saída do GIF.
        if tempo < duracao_fade:
            transparencia = int(
                255 * (1 - tempo / duracao_fade)
            )

        elif tempo > duracao_gif - duracao_fade:
            progresso = (
                                tempo - (duracao_gif - duracao_fade)
                        ) / duracao_fade

            transparencia = int(255 * progresso)

        else:
            transparencia = 0

        if transparencia > 0:
            sombra = pygame.Surface(
                (LARGURA, ALTURA)
            )
            sombra.fill((0, 0, 0))
            sombra.set_alpha(transparencia)

            tela.blit(sombra, (0, 0))

        pygame.display.flip()
        relogio.tick(FPS)

    return True


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

    painel = pygame.Surface((550, 470), pygame.SRCALPHA)
    painel.fill((15, 30, 18, 150))

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
        "Receba três cartas.",
        "Clique em uma carta para jogar.",
        "O computador será seu adversário.",
        "Cada rodada pode valer um ponto,",
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
# TELA DE CRÉDITOS
# ==================================================

def mostrar_creditos(tela, fonte_titulo, fonte_texto, fundo):
    if fundo:
        tela.blit(fundo, (0, 0))
    else:
        tela.fill(VERDE_MESA)

    painel = pygame.Surface((550, 470), pygame.SRCALPHA)
    painel.fill((15, 30, 18, 150))

    tela.blit(
        painel,
        painel.get_rect(
            center=(LARGURA // 2, ALTURA // 2)
        ),
    )

    titulo = fonte_titulo.render(
        "créditos",
        True,
        DOURADO,
    )

    tela.blit(
        titulo,
        titulo.get_rect(center=(LARGURA // 2, 180)),
    )

    creditos = [
        "DESENVOLVIMENTO",
        "Fernando Dierings",
        "",
        "TECNOLOGIAS",
        "Python e Pygame",
        "",
        "OBRIGADO POR JOGAR!",
        "",
        "Pressione ESC para voltar ao menu.",
    ]

    for indice, texto in enumerate(creditos):
        cor = DOURADO if texto.isupper() and texto else BRANCO

        linha = fonte_texto.render(
            texto,
            True,
            cor,
        )

        tela.blit(
            linha,
            linha.get_rect(
                center=(LARGURA // 2, 245 + indice * 34)
            ),
        )


# ==================================================
# MÚSICA DO MENU
# ==================================================

def iniciar_musica_menu():
    if not CAMINHO_MUSICA_MENU.exists():
        print(f"Música não encontrada: {CAMINHO_MUSICA_MENU}")
        return

    pygame.mixer.music.load(str(CAMINHO_MUSICA_MENU))
    pygame.mixer.music.set_volume(0.10)
    pygame.mixer.music.play(-1)


def parar_musica_menu():
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


# ==================================================
# MENU PRINCIPAL
# ==================================================

def iniciar_jogo():
    pygame.init()
    iniciar_musica_menu()
    som_rollover, som_click = carregar_sons_menu()

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
    quadros_carregamento = carregar_gif_carregamento()

    # Posições dos botões.
    botao_jogar = pygame.Rect(
        LARGURA // 2 - 150, 300, 300, 55
    )

    botao_regras = pygame.Rect(
        LARGURA // 2 - 150, 370, 300, 55
    )

    botao_creditos = pygame.Rect(
        LARGURA // 2 - 150, 440, 300, 55
    )

    botao_sair = pygame.Rect(
        LARGURA // 2 - 150, 510, 300, 55
    )

    tela_atual = "menu"
    executando = True
    mouse_sobre_botao = None

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
            elif botao_sair.collidepoint(mouse_pos):
                botao_atual = "sair"

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
                    ):
                        som_click.play()

                    if botao_jogar.collidepoint(evento.pos):

                        # Exibir a transição antes da partida.
                        transicao_concluida = mostrar_transicao(
                            tela,
                            relogio,
                            quadros_carregamento,
                            fonte_titulo
                        )

                        if not transicao_concluida:
                            executando = False
                            continue

                        # A música do menu termina após a transição.
                        parar_musica_menu()

                        # Agora a partida começa normalmente.
                        resultado = iniciar_partida(tela, relogio)

                        if resultado == "sair":
                            executando = False
                        else:
                            iniciar_musica_menu()

                    elif botao_regras.collidepoint(evento.pos):
                        tela_atual = "regras"
                    elif botao_creditos.collidepoint(evento.pos):
                        tela_atual = "creditos"
                    elif botao_sair.collidepoint(evento.pos):
                        executando = False


            elif evento.type == pygame.KEYDOWN:

                if (
                        evento.key == pygame.K_ESCAPE
                        and tela_atual in ("regras", "creditos")
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
                fundo_menu,
            )

        elif tela_atual == "creditos":
            mostrar_creditos(
                tela,
                fonte_titulo,
                fonte_texto,
                fundo_menu,
            )

        pygame.display.flip()
        relogio.tick(FPS)

    pygame.mixer.music.stop()
    pygame.quit()


if __name__ == "__main__":
    iniciar_jogo()
