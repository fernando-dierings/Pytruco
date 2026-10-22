import random

from logica.baralho import (
    criar_baralho,
    embaralhar_baralho,
    distribuir_cartas,
)

from logica.jogador import Jogador

from logica.regras_truco import (
    vencedor_da_rodada,
    comparar_cartas,
)

class Partida:
    def __init__(self):
        self.jogador = Jogador("Você")
        self.computador = Jogador("Computador")

        self.pontos_jogador = 0
        self.pontos_computador = 0

        self.valor_mao = 1
        self.truco_pedido = False
        self.truco_pendente_computador = False
        self.mao_encerrada = False

        self.baralho = []
        self.rodada = 0
        self.resultados_rodadas = []

        self.nova_mao()

    def nova_mao(self):
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

        self.valor_mao = 1
        self.truco_pedido = False
        self.truco_pendente_computador = False
        self.mao_encerrada = False

    def pedir_truco(self):
        if self.mao_encerrada:
            return "A mão já terminou."

        if self.truco_pedido:
            return "O truco já foi pedido nesta mão."

        if self.rodada >= 3:
            return "Não é possível pedir truco agora."

        self.truco_pedido = True

        aceita = random.choice([True, True, False])

        if aceita:
            self.valor_mao = 2
            return {
                "status": "aceito",
                "mensagem": (
                    "Computador aceitou o truco! "
                    "A mão vale 2 pontos."
                ),
            }

        self.pontos_jogador += self.valor_mao
        self.mao_encerrada = True

        return {
            "status": "recusado",
            "mensagem": "Computador recusou! Você ganhou a mão.",
        }

    def responder_truco(self, aceitar):
        if not self.truco_pendente_computador:
            return "Não há truco pendente."

        self.truco_pendente_computador = False

        if aceitar:
            self.valor_mao = 2
            return "Você aceitou! A mão agora vale 2 pontos."

        self.pontos_computador += self.valor_mao
        self.mao_encerrada = True

        return "Você correu! O computador ganhou os pontos da mão."

    def determinar_vencedor_mao(self):
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

        if primeira == "empate":
            if segunda != "empate":
                return segunda

            return (
                terceira
                if terceira != "empate"
                else "empate"
            )

        if segunda == "empate":
            return primeira

        return (
            terceira
            if terceira != "empate"
            else "empate"
        )

    def jogar_rodada(self, indice_jogador):
        if self.mao_encerrada:
            return "A mão já terminou."

        if not self.jogador.tem_cartas():
            return "Você não tem mais cartas."

        if not self.computador.tem_cartas():
            return "O computador não tem mais cartas."

        carta_jogador = self.jogador.jogar_carta(
            indice_jogador
        )

        if carta_jogador is None:
            return "Índice de carta inválido."

        indice_computador = self.escolher_carta_computador(
            carta_jogador
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

        if (
            self.resultados_rodadas.count("jogador") >= 2
            or self.resultados_rodadas.count("computador") >= 2
            or self.rodada == 3
        ):
            vencedor_mao = self.determinar_vencedor_mao()

            if vencedor_mao == "jogador":
                self.pontos_jogador += self.valor_mao
                self.mao_encerrada = True

            elif vencedor_mao == "computador":
                self.pontos_computador += self.valor_mao
                self.mao_encerrada = True

            elif vencedor_mao == "empate":
                self.mao_encerrada = True

        computador_pediu_truco = False

        if (
            not self.mao_encerrada
            and not self.truco_pedido
            and self.rodada >= 1
            and random.random() < 0.25
        ):
            self.truco_pendente_computador = True
            self.truco_pedido = True
            computador_pediu_truco = True

        return {
            "carta_jogador": carta_jogador,
            "carta_computador": carta_computador,
            "resultado": resultado,
            "rodada": self.rodada,
            "vencedor_mao": vencedor_mao,
            "valor_mao": self.valor_mao,
            "computador_pediu_truco": computador_pediu_truco,
        }

    def escolher_carta_computador(self, carta_jogador):
        cartas = self.computador.cartas

        if not cartas:
            return 0

        # Identifica as cartas que vencem a carta do jogador.
        vencedoras = [
            i
            for i, carta in enumerate(cartas)
            if comparar_cartas(carta, carta_jogador) == 1
        ]

        if vencedoras:
            # Vence gastando a carta mais fraca possível.
            return min(
                vencedoras,
                key=lambda i: self.forca_da_carta(cartas[i])
            )

        # Se não puder vencer, descarta a carta mais fraca.
        return min(
            range(len(cartas)),
            key=lambda i: self.forca_da_carta(cartas[i])
        )

    def forca_da_carta(self, carta):
        from logica.regras_truco import forca_carta

        return forca_carta(carta)

    def partida_encerrada(self):
        return (
            self.pontos_jogador >= 12
            or self.pontos_computador >= 12
        )
