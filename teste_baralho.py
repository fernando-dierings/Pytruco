
from logica.baralho import (
    criar_baralho,
    embaralhar_baralho,
    distribuir_cartas
)

baralho = criar_baralho()

print("Total de cartas:", len(baralho))

embaralhar_baralho(baralho)

jogador = distribuir_cartas(baralho)
computador = distribuir_cartas(baralho)

print("Cartas do jogador:", jogador)
print("Cartas do computador:", computador)
print("Cartas restantes:", len(baralho))


from logica.jogador import Jogador

jogador = Jogador("Você")
jogador.receber_cartas(distribuir_cartas(baralho))

print("Mão inicial:", jogador.cartas)

carta = jogador.jogar_carta(0)
print("Carta jogada:", carta)
print("Cartas restantes:", jogador.cartas)


from logica.regras_truco import vencedor_da_rodada

carta_jogador = {"valor": 7, "naipe": "Copas"}
carta_computador = {"valor": 5, "naipe": "Espadas"}

resultado = vencedor_da_rodada(
    carta_jogador,
    carta_computador
)

print("Vencedor da rodada:", resultado)

