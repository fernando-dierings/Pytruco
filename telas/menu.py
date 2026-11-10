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
    CAMINHO_FUNDO_PARTIDA2,
    CAMINHO_BOTAO,
    CAMINHO_MUSICA_MENU,
    CAMINHO_SOM_ROLLOVER,
    CAMINHO_SOM_CLICK,
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

def carregar_fundo_identificacao():
    if not CAMINHO_FUNDO_PARTIDA2.exists():
        print(
            f"Fundo de identificação não encontrado: "
            f"{CAMINHO_FUNDO_PARTIDA2}"
        )
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
# TELA DE IDENTIFICAÇÃO DO JOGADOR
# ==================================================

def mostrar_tela_nome(
    tela,
    relogio,
    fundo,
    fonte_titulo,
    fonte_texto,
    fonte_botao,
    imagem_botao,
    som_click,
):
    nome = ""


    campo_nome = pygame.Rect(
        LARGURA // 2 - 250,
        330,
        500,
        60,
    )

    botao_confirmar = pygame.Rect(
        LARGURA // 2 - 210,
        440,
        200,
        55,
    )

    botao_voltar = pygame.Rect(
        LARGURA // 2 + 10,
        440,
        200,
        55,
    )

    pygame.key.start_text_input()

    executando = True

    while executando:
        mouse_pos = pygame.mouse.get_pos()

        for evento in pygame.event.get():

            if evento.type == pygame.QUIT:
                pygame.key.stop_text_input()
                return None, True

            elif evento.type == pygame.TEXTINPUT:
                nome += evento.text
                nome = nome[:16]

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


        # Título.
        titulo = fonte_titulo.render(
            "BUENAS, VIVENTE!",
            True,
            DOURADO,
        )

        tela.blit(
            titulo,
            titulo.get_rect(
                center=(LARGURA // 2, 220)
            ),
        )

        # Instrução.
        instrucao = fonte_texto.render(
            "COMO DEVEMOS TE CHAMAR?",
            True,
            BRANCO,
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

        pygame.draw.rect(
            tela,
            DOURADO,
            campo_nome,
            2,
        )

        texto_nome = nome if nome else "DIGITE SEU NOME"

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
            imagem_botao,
        )

        desenhar_botao(
            tela,
            "VOLTAR",
            botao_voltar,
            fonte_botao,
            mouse_pos,
            imagem_botao,
        )

        pygame.display.flip()
        relogio.tick(FPS)

    pygame.key.stop_text_input()
    return None, False


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
    fundo_menu = carregar_fundo_menu()
    fundo_identificacao = carregar_fundo_identificacao()
    imagem_botao = carregar_imagem_botao()

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

                        # Solicita o nome somente na primeira vez.
                        if nome_jogador is None:

                            nome_escolhido, fechar_jogo = mostrar_tela_nome(
                                tela,
                                relogio,
                                fundo_identificacao,
                                fonte_titulo,
                                fonte_texto,
                                fonte_botao,
                                imagem_botao,
                                som_click,
                            )

                            if fechar_jogo:
                                executando = False
                                continue

                            # Se voltar, retorna ao menu sem iniciar a partida.
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
                        else:
                            iniciar_musica_menu()

                        if not transicao_concluida:
                            executando = False
                            continue

                        parar_musica_menu()

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
