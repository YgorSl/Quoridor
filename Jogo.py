class Jogador:
    def oposto(self):
        raise NotImplementedError("Deve ser implementado")

    def __str__(self):
        return self.value

class Jogo():
    def turno(self):
        pass

    def jogar(self, localizacao):
        pass

    def jogos_validos(self):
        pass

    def venceu(self):
        pass

    def avaliar(self, player):
        pass