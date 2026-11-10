

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

    def __init__(self, nome_jogador="Você"):
        self.jogador = Jogador(nome_jogador)
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

        # Alternância de quem começa cada nova mão.
        self.proximo_a_comecar_mao = "jogador"

        self.quem_comeca_mao = None
        self.quem_comeca_rodada = None

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

        # Define quem começa esta mão.
        self.quem_comeca_mao = self.proximo_a_comecar_mao
        self.quem_comeca_rodada = self.quem_comeca_mao

        # Alterna o jogador que começará a próxima mão.
        if self.proximo_a_comecar_mao == "jogador":
            self.proximo_a_comecar_mao = "computador"
        else:
            self.proximo_a_comecar_mao = "jogador"

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

    # Jogador começa a rodada.
    def iniciar_rodada(self, indice_jogador):
        if self.mao_encerrada:
            return "A mão já terminou."

        if self.quem_comeca_rodada != "jogador":
            return "O computador deve jogar primeiro."

        if not self.jogador.tem_cartas():
            return "Você não tem mais cartas."

        if not self.computador.tem_cartas():
            return "O computador não tem mais cartas."

        carta_jogador = self.jogador.jogar_carta(
            indice_jogador
        )

        if carta_jogador is None:
            return "Índice de carta inválido."

        return {
            "carta_jogador": carta_jogador,
            "quem_jogou_primeiro": "jogador",
        }

    # Jogador responde quando o computador começa.
    def jogar_resposta_jogador(self, indice_jogador):
        if self.mao_encerrada:
            return "A mão já terminou."

        if self.quem_comeca_rodada != "computador":
            return "Você não está respondendo ao computador."

        if not self.jogador.tem_cartas():
            return "Você não tem mais cartas."

        carta_jogador = self.jogador.jogar_carta(
            indice_jogador
        )

        if carta_jogador is None:
            return "Índice de carta inválido."

        return {
            "carta_jogador": carta_jogador,
        }

    # Computador começa a rodada.
    def iniciar_rodada_computador(self):
        if self.mao_encerrada:
            return "A mão já terminou."

        if self.quem_comeca_rodada != "computador":
            return "Você deve jogar primeiro."

        if not self.computador.tem_cartas():
            return "O computador não tem mais cartas."

        indice = self.escolher_carta_inicial_computador()

        carta_computador = self.computador.jogar_carta(indice)

        return {
            "carta_computador": carta_computador,
            "quem_jogou_primeiro": "computador",
        }

    # Computador escolhe uma carta para iniciar a rodada.
    def escolher_carta_inicial_computador(self):
        cartas = self.computador.cartas

        return min(
            range(len(cartas)),
            key=lambda i: self.forca_da_carta(cartas[i])
        )

    # Resolve a rodada depois que os dois jogaram.
    def concluir_rodada(
        self,
        carta_jogador,
        carta_computador=None
    ):
        # Se o jogador começou, o computador responde agora.
        if carta_computador is None:
            indice_computador = self.escolher_carta_computador(
                carta_jogador
            )

            carta_computador = self.computador.jogar_carta(
                indice_computador
            )

        # Compara as cartas.
        resultado = vencedor_da_rodada(
            carta_jogador,
            carta_computador,
        )

        self.resultados_rodadas.append(resultado)
        self.rodada += 1

        # Define quem começa a próxima rodada.
        if resultado == "jogador":
            self.quem_comeca_rodada = "jogador"

        elif resultado == "computador":
            self.quem_comeca_rodada = "computador"

        else:
            # Em caso de empate, começa quem jogou em segundo.
            if self.quem_comeca_rodada == "jogador":
                self.quem_comeca_rodada = "computador"
            else:
                self.quem_comeca_rodada = "jogador"

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
            "carta_computador": carta_computador,
            "resultado": resultado,
            "rodada": self.rodada,
            "vencedor_mao": vencedor_mao,
            "valor_mao": self.valor_mao,
            "computador_pediu_truco": computador_pediu_truco,
            "quem_comeca_proxima_rodada": self.quem_comeca_rodada,
        }

    def escolher_carta_computador(self, carta_jogador):
        cartas = self.computador.cartas

        if not cartas:
            return 0

        vencedoras = [
            i
            for i, carta in enumerate(cartas)
            if comparar_cartas(carta, carta_jogador) == 1
        ]

        if vencedoras:
            return min(
                vencedoras,
                key=lambda i: self.forca_da_carta(cartas[i])
            )

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
