import numpy as np
from collections import deque

class Quoridor:

    def __init__(self):        

        self.tabuleiro = self.criar_tabuleiro()
        self.turno = "P"
        self.paredes_p=10
        self.paredes_a=10
        self.turno_mm = None
        self.itercao =0

    def existe_caminho(self, tabuleiro, jogador):
        # Define o objetivo final para cada jogador
        objetivo = 16 if jogador == "P" else 0

        # Encontra a posição inicial do jogador
        posicao_inicial = encontrar_posicao(jogador, tabuleiro)

        # Cria uma fila para armazenar os caminhos a serem explorados
        fila = deque([posicao_inicial])

        # Cria um conjunto para armazenar as posições já visitadas
        visitados = set()

        # Realiza uma busca em largura (BFS) para encontrar um caminho até o objetivo
        while fila:
            posicao_atual = fila.popleft()
            linha_atual, coluna_atual = posicao_atual

            # Se o jogador alcançou o objetivo, retorna True
            if linha_atual == objetivo:
                return True

            # Adiciona a posição atual aos visitados
            visitados.add(posicao_atual)

            # Explora as posições adjacentes
            for delta_linha, delta_coluna in [(-2, 0), (2, 0), (0, -2), (0, 2)]:
                nova_linha = linha_atual + delta_linha
                nova_coluna = coluna_atual + delta_coluna

                # Verifica se a nova posição é válida e não foi visitada
                if 0 <= nova_linha < 17 and 0 <= nova_coluna < 17 and (nova_linha, nova_coluna) not in visitados:
                    # Verifica se não há barreira no caminho
                    if tabuleiro[linha_atual + delta_linha // 2][coluna_atual + delta_coluna // 2] not in ['-', '|']:
                        fila.append((nova_linha, nova_coluna))

        # Se não encontrar um caminho até o objetivo, retorna False
        return False
    def reduzir_parede(self):

        if self.turno == "P":
            self.paredes_p -=1
        elif self.turno =="A":
            self.paredes_a -=1

    def oposto(self, turno):

        if turno == "P":
            return "A"
        else:
            return "P"

    def criar_tabuleiro(self):
        # Cria um tabuleiro 9x9 com espaços vazios ('.') e espaços para barreiras (' ')
        self.tabuleiro = [['.' if (linha % 2 == 0 and coluna % 2 == 0) else ' ' for coluna in range(17)] for linha in range(17)]
        
        # Adiciona as peças dos jogadores no tabuleiro
        self.tabuleiro[0][8] = 'P'  # Posição inicial do jogador 1
        self.tabuleiro[16][8] = 'A'  # Posição inicial do jogador 2
        
        return self.tabuleiro

    def adicionar_barreira(self, linha, coluna, orientacao):
        # Adiciona uma barreira no tabuleiro na posição e orientação especificadas
        # 'H' para horizontal e 'V' para vertical

        chegada_p1 = 8
        chegada_p2 = 0 

        #ptabuleiro_antigo = tabuleiro


        if orientacao == 'H':
            for offset in range(-1, 2):
                self.tabuleiro[linha][coluna + offset] = '-'
        elif orientacao == 'V':
            for offset in range(-1, 2):
                self.tabuleiro[linha + offset][coluna] = '|'

        # if self.existe_caminho(tabuleiro, posicao_p1, chegada_p1):
        #     print("Ainda existe um caminho após adicionar a barreira.")
            
        # else:
        #     print("A barreira bloqueia todos os caminhos. Movimento inválido.")
        #     return tabuleiro_antigo

        # if self.existe_caminho(tabuleiro, posicao_p2, chegada_p2):
        #     print("Ainda existe um caminho após adicionar a barreira.")
        # else:
        #     print("A barreira bloqueia todos os caminhos. Movimento inválido.")
        #     return tabuleiro_antigo
        self.reduzir_parede()
        self.turno = self.oposto(self.turno)
        return self.tabuleiro


    def is_end(self, tabuleiro):
        pos_p1 = encontrar_posicao("P", tabuleiro)
        if pos_p1[0] == 16:
            return True
    
        pos_p2 = encontrar_posicao("A", tabuleiro)
        if pos_p2[0] == 0:
            return True
        
        return False
        
    def get_winner(self, tabuleiro):
        if self.encontrar_posicao("A", tabuleiro)[0] == 0:
            return "A"
        else:
            return "P"

    def imprimir_tabuleiro(self):
    # Imprime os números das colunas
        print("    ", end="")
        for coluna in range(1, 18, 2):  # Começa em 1 e incrementa de 2 em 2
            print(f"{coluna // 1:2}", end="  ")
        print()

        # Imprime o tabuleiro com números de linha e conteúdo
        for linha, linha_tabuleiro in enumerate(self.tabuleiro):
            # Ajusta o número da linha para começar em 1
            print(f"{linha if linha % 2 != 0 else ' ':2}", end=" ")
            for celula in linha_tabuleiro:
                print(celula, end=" ")
            print()
        print()

    # def mover_peca(tabuleiro, posicao_atual, movimento, jogador):
    #     # Calcula a nova posição baseada no movimento
    #     direcoes = {'C': (-2, 0), 'B': (2, 0), 'E': (0, -2), 'D': (0, 2)}
    #     delta = direcoes[movimento]
    #     nova_posicao = (posicao_atual[0] + delta[0], posicao_atual[1] + delta[1])
        
    #     # Verifica se a nova posição é válida
    #     if not (0 <= nova_posicao[0] < 17 and 0 <= nova_posicao[1] < 17):
    #         return False, "Movimento inválido: fora do tabuleiro."
        
    #     # Verifica se há uma barreira no caminho
    #     posicao_barreira = (posicao_atual[0] + delta[0]//2, posicao_atual[1] + delta[1]//2)
    #     if tabuleiro[posicao_barreira[0]][posicao_barreira[1]] in ('-', '|'):
    #         return False, "Movimento inválido: há uma barreira no caminho."
        
    #     # Move a peça
    #     tabuleiro[posicao_atual[0]][posicao_atual[1]] = '.'
    #     tabuleiro[nova_posicao[0]][nova_posicao[1]] = jogador  # ou 'A', dependendo do jogador
        
    #     return True, nova_posicao

    def mover_peca(self, posicao_atual, movimento):
        # Mapeia os movimentos para as mudanças correspondentes no índice do tabuleiro
        direcoes = {'C': (-2, 0), 'B': (2, 0), 'E': (0, -2), 'D': (0, 2)}
        delta = direcoes[movimento]
        
        # Calcula a posição intermediária (onde uma barreira pode estar)
        posicao_intermediaria = (posicao_atual[0] + delta[0]//2, posicao_atual[1] + delta[1]//2)
        
        # Verifica se a nova posição é válida
        nova_posicao = (posicao_atual[0] + delta[0], posicao_atual[1] + delta[1])
        if not (0 <= nova_posicao[0] < 17 and 0 <= nova_posicao[1] < 17):
            return False, "Movimento inválido: fora do tabuleiro."
        
         # Verifica se ha um jogador na posi;'ao escolhida
        
         # Verifica se a próxima posição está ocupada por outro jogador
        if self.tabuleiro[nova_posicao[0]][nova_posicao[1]] in ('P', 'A'):
            # Pula para a próxima posição válida
            nova_posicao = (nova_posicao[0] + delta[0], nova_posicao[1] + delta[1])
        
        # Verifica se há uma barreira no caminho
        if self.tabuleiro[posicao_intermediaria[0]][posicao_intermediaria[1]] in ('-', '|'):
            return False, "Movimento inválido: há uma barreira no caminho."
        
        # Move a peça
        self.tabuleiro[posicao_atual[0]][posicao_atual[1]] = '.'
        self.tabuleiro[nova_posicao[0]][nova_posicao[1]] = self.turno  # 'P' ou 'A'
        
        self.turno = self.oposto(self.turno)
        return True, nova_posicao
    
    def verifica_parede(self, linha, coluna, orientacao, tabuleiro, turno):
        # Verifica se a posição está dentro dos limites do tabuleiro para paredes
        if orientacao not in ['H', 'V']:
            return False

        if self.qtd_paredes(turno) == 0:
            print("Paredes Esgotadas")
            return False

        if orientacao == 'H' and (linha <= 0 or linha > 14 or coluna < 1 or coluna > 14):
            return False
        if orientacao == 'V' and (linha < 1 or linha > 14 or coluna <= 0 or coluna > 14):
            return False

        # Verifica se a posição já está ocupada por outra parede ou casa
        if tabuleiro[linha][coluna] != ' ' or tabuleiro[linha][coluna] == '.':
            return False

        # Verifica se a parede não cruza ou toca outra parede na mesma orientação
        if orientacao == 'H':
            if tabuleiro[linha][coluna-1] == '-' or tabuleiro[linha][coluna+1] == '-':
                return False
        if orientacao == 'V':
            if tabuleiro[linha-1][coluna] == '|' or tabuleiro[linha+1][coluna] == '|':
                return False

        # Verifica se a parede não cobre as casas adjacentes
        if orientacao == 'H':
            if tabuleiro[linha-1][coluna] in ['.', "P","A"] or tabuleiro[linha+1][coluna] in['.',"P","A"]:
                return False
            if tabuleiro[linha][coluna-1] in ['.', "P","A"] or tabuleiro[linha][coluna+1] in['.',"P","A"]:
                return False
        if orientacao == 'V':
            if tabuleiro[linha][coluna-1] in ['.', "P","A"] or tabuleiro[linha][coluna+1] in ['.', "P","A"]:
                return False
            if tabuleiro[linha+1][coluna] in ['.', "P","A"] or tabuleiro[linha-1][coluna] in ['.', "P","A"]:
                return False
            
        tabuleiro_simulado = [linha[:] for linha in tabuleiro]
        if orientacao == 'H':
            for offset in range(-1, 2):
                tabuleiro_simulado[linha][coluna + offset] = '-'
        elif orientacao == 'V':
            for offset in range(-1, 2):
                tabuleiro_simulado[linha + offset][coluna] = '|'

        # Verifica se ainda há caminho para o jogador P1
        if not self.existe_caminho(tabuleiro_simulado, "P"):
            return False
        # Verifica se ainda há caminho para o jogador P2
        if not self.existe_caminho(tabuleiro_simulado, "A"):
            return False

        # Se passar por todas as verificações, a posição é válida
        return True
    
    def jogada_humano():
        jogada = -1
        while jogada not in jogo.jogos_validos():
            jogada = int(input("Escolha um quadrado (0-8):"))
        return jogada
    
    def turn(self):
        return self.turno

def encontrar_posicao(jogador, tabuleiro):
    # Converte o tabuleiro para um array NumPy
    tabuleiro_np = np.array(tabuleiro)
    
    # Usa np.where para encontrar a posição do 'P'
    posicao = np.where(tabuleiro_np == jogador)

    # np.where retorna uma tupla com arrays, pegamos o primeiro elemento de cada array
    return (posicao[0][0], posicao[1][0])

def qtd_paredes(self, turno):

        if turno == "P":
            return self.paredes_p
        elif turno =="A":
            return self.paredes_a