from logica.baralho import (
    criar_baralho,
    embaralhar_baralho,
    distribuir_cartas,
)

from logica.jogador import Jogador
from logica.regras_truco import vencedor_da_rodada


class Partida:
    def __init__(self):
        self.jogador = Jogador("Você")
        self.computador = Jogador("Computador")

        self.pontos_jogador = 0
        self.pontos_computador = 0

        self.baralho = []
        self.rodada = 0
        self.resultados_rodadas = []

        self.nova_mao()

    def nova_mao(self):
        """Distribui novas cartas e prepara outra mão."""
        self.baralho = criar_baralho()
        embaralhar_baralho(self.baralho)

        self.jogador.receber_cartas(
            distribuir_cartas(self.baralho)
        )
        self.computador.receber_cartas(
            distribuir_cartas(self.baralho)
        )

        self.rodada = 0
        self.resultados_rodadas = []

    def determinar_vencedor_mao(self):
        """Determina o vencedor considerando as três rodadas."""
        resultados = self.resultados_rodadas

        vitorias_jogador = resultados.count("jogador")
        vitorias_computador = resultados.count("computador")

        if vitorias_jogador >= 2:
            return "jogador"

        if vitorias_computador >= 2:
            return "computador"

        if len(resultados) < 3:
            return None

        primeira, segunda, terceira = resultados

        # Se a primeira rodada empatou, a segunda
        # rodada não empatada decide a mão.
        if primeira == "empate":
            if segunda != "empate":
                return segunda

            # Se as duas primeiras empataram,
            # a terceira rodada decide.
            return terceira if terceira != "empate" else "empate"

        # Se a primeira venceu e a segunda empatou,
        # vence quem ganhou a primeira.
        if segunda == "empate":
            return primeira

        # Se cada jogador venceu uma rodada,
        # a terceira rodada decide.
        return terceira if terceira != "empate" else "empate"

    def jogar_rodada(self, indice_jogador):
        """Joga uma rodada e atualiza a pontuação da mão."""
        if not self.jogador.tem_cartas():
            return "Você não tem mais cartas."

        if not self.computador.tem_cartas():
            return "O computador não tem mais cartas."

        carta_jogador = self.jogador.jogar_carta(indice_jogador)

        if carta_jogador is None:
            return "Índice de carta inválido."

        import random

        indice_computador = random.randrange(
            len(self.computador.cartas)
        )
        carta_computador = self.computador.jogar_carta(
            indice_computador
        )

        resultado = vencedor_da_rodada(
            carta_jogador,
            carta_computador,
        )

        self.resultados_rodadas.append(resultado)
        self.rodada += 1

        vencedor_mao = None

        # A mão é decidida quando alguém vence duas rodadas
        # ou quando as três rodadas terminam.
        if (
            self.resultados_rodadas.count("jogador") >= 2
            or self.resultados_rodadas.count("computador") >= 2
            or self.rodada == 3
        ):
            vencedor_mao = self.determinar_vencedor_mao()

            if vencedor_mao == "jogador":
                self.pontos_jogador += 1
            elif vencedor_mao == "computador":
                self.pontos_computador += 1

        return {
            "carta_jogador": carta_jogador,
            "carta_computador": carta_computador,
            "resultado": resultado,
            "rodada": self.rodada,
            "vencedor_mao": vencedor_mao,
        }

    def partida_encerrada(self):
        return (
            self.pontos_jogador >= 12
            or self.pontos_computador >= 12
        )
