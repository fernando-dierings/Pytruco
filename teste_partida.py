
from logica.partida import Partida

partida = Partida()

print("Suas cartas:", partida.jogador.cartas)

resultado = partida.jogar_rodada(0)

print("Resultado:", resultado)
print("Placar:", partida.pontos_jogador, "-", partida.pontos_computador)
