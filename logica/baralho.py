import random


NAIPES = ["Copas", "Bastos", "Ouros", "Espadas"]
VALORES = [1, 2, 3, 4, 5, 6, 7, 10, 11, 12]


def criar_baralho():
    #Cria um baralho de 40 cartas
    baralho = []

    for naipe in NAIPES:
        for valor in VALORES:
            carta = {
                "valor": valor,
                "naipe": naipe
            }
            baralho.append(carta)

    return baralho


def embaralhar_baralho(baralho):
    #Embaralha as cartas.
    random.shuffle(baralho)
    return baralho


def distribuir_cartas(baralho, quantidade=3):
    #Retira cartas do baralho para um jogador.
    cartas = []

    for _ in range(quantidade):
        if baralho:
            cartas.append(baralho.pop())

    return cartas
