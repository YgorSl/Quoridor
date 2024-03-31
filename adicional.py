
from enum import Enum
from jogo import Jogador, Jogo
from minmax import melhor_jogada_agente, melhor_jogada_agente_poda

class Peca(Jogador, Enum):
    p1 = "P1"
    p2 = "P2"
    V = "." # vazio

    def oposto(self):
        if self == Peca.p1:
            return Peca.p2
        elif self == Peca.p2:
            return Peca.p1
        else:
            return Peca.V

    def __str__(self):
        return self.value

class JogoVelha(Jogo):
    def __init__(self, posicao = [Peca.V] * 9, turno = Peca.P1):
        self.posicao = posicao
        self._turno = turno
        self.tabuleiro = ""

    def criar_tabuleiro(self):
        # Cria um tabuleiro 9x9 com espaços vazios ('.') e espaços para barreiras (' ')
        self.tabuleiro = [['.' if (linha % 2 == 0 and coluna % 2 == 0) else ' ' for coluna in range(17)] for linha in range(17)]
        
        # Adiciona as peças dos jogadores no tabuleiro
        self.tabuleiro[0][8] = 'P1'  # Posição inicial do jogador 1
        self.tabuleiro[16][8] = 'P2'  # Posição inicial do jogador 2
        return self.tabuleiro

    def turno(self):
        return self._turno
    
    def jogar(self, local):
        temp = self.posicao.copy()
        temp[local] = self._turno
        return JogoVelha(temp, self.turno().oposto())
  
    def jogos_validos(self, tabuleiro):
        
        return [] 
    
    def venceu(self):
        return self._venceu_linhas(self.posicao) or self._venceu_colunas(self.posicao) or self._venceu_diagonal(self.posicao) 


    def calcular_utilidade(self, jogador):
        if self.venceu() and self._turno == jogador:
            return -1
        elif self.venceu() and self._turno != jogador:
            return 1
        else:
            return 0

    def __str__(self):
        return f"""{self.posicao[0]}|{self.posicao[1]}|{self.posicao[2]}
-----
{self.posicao[3]}|{self.posicao[4]}|{self.posicao[5]}
-----
{self.posicao[6]}|{self.posicao[7]}|{self.posicao[8]}"""

jogo = JogoVelha()

def jogada_humano():
    jogada = -1
    while jogada not in jogo.jogos_validos():
        jogada = int(input("Escolha um quadrado (0-8):"))
    return jogada

if __name__ == "__main__":
    while True:
        humano = jogada_humano()
        jogo = jogo.jogar(humano)
        if jogo.venceu():
            print("Humano Venceu!")
            break
        computador = melhor_jogada_agente(jogo)
        print(f"Jogada do Computador é {computador}")
        jogo = jogo.jogar(computador)
        print(jogo)
        if jogo.venceu():
            print("Computador venceu!")
            break
        