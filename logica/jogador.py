class Jogador:
    def __init__(self, nome):
        self.nome = nome
        self.cartas = []
        self.cartas_jogadas = []

    def receber_cartas(self, cartas):
        self.cartas = cartas

    def jogar_carta(self, indice):
        if 0 <= indice < len(self.cartas):
            carta = self.cartas.pop(indice)
            self.cartas_jogadas.append(carta)
            return carta

        return None

    def tem_cartas(self):
        return len(self.cartas) > 0

    def nova_mao(self):
        self.cartas = []
        self.cartas_jogadas = []
