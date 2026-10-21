# Hierarquia do Truco Gaúcho
# Quanto maior o número, mais forte é a carta.

HIERARQUIA = {
    (1, "Espadas"): 14,
    (1, "Bastos"): 13,
    (7, "Espadas"): 12,
    (7, "Ouros"): 11,

    (3, "Copas"): 10,
    (3, "Bastos"): 10,
    (3, "Ouros"): 10,
    (3, "Espadas"): 10,

    (2, "Copas"): 9,
    (2, "Bastos"): 9,
    (2, "Ouros"): 9,
    (2, "Espadas"): 9,

    (1, "Copas"): 8,
    (1, "Ouros"): 8,

    (12, "Copas"): 7,
    (12, "Bastos"): 7,
    (12, "Ouros"): 7,
    (12, "Espadas"): 7,

    (11, "Copas"): 6,
    (11, "Bastos"): 6,
    (11, "Ouros"): 6,
    (11, "Espadas"): 6,

    (10, "Copas"): 5,
    (10, "Bastos"): 5,
    (10, "Ouros"): 5,
    (10, "Espadas"): 5,

    (7, "Copas"): 4,
    (7, "Bastos"): 4,

    (6, "Copas"): 3,
    (6, "Bastos"): 3,
    (6, "Ouros"): 3,
    (6, "Espadas"): 3,

    (5, "Copas"): 2,
    (5, "Bastos"): 2,
    (5, "Ouros"): 2,
    (5, "Espadas"): 2,

    (4, "Copas"): 1,
    (4, "Bastos"): 1,
    (4, "Ouros"): 1,
    (4, "Espadas"): 1,
}


def forca_carta(carta):
    """Retorna a força de uma carta."""
    chave = (carta["valor"], carta["naipe"])
    return HIERARQUIA[chave]


def comparar_cartas(carta1, carta2):
    """Retorna 1 se a primeira vence, -1 se perde e 0 se empata."""
    forca1 = forca_carta(carta1)
    forca2 = forca_carta(carta2)

    if forca1 > forca2:
        return 1

    if forca1 < forca2:
        return -1

    return 0


def vencedor_da_rodada(carta_jogador, carta_computador):
    """Determina quem venceu a rodada."""
    resultado = comparar_cartas(carta_jogador, carta_computador)

    if resultado == 1:
        return "jogador"

    if resultado == -1:
        return "computador"

    return "empate"
