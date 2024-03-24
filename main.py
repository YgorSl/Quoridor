import numpy as np
from collections import deque

class Quoridor:

    def __init__(self):        

        self.tabuleiro = self.criar_tabuleiro()
        self.turno = "P1"

    def existe_caminho(tabuleiro, posicao_inicial, linha_final):
        # Converte o tabuleiro para um formato que facilite a verificação de barreiras
        tabuleiro_convertido = [[' ' for _ in range(9)] for _ in range(9)]
        for i in range(17):
            for j in range(17):
                if tabuleiro[i][j] == '.':
                    tabuleiro_convertido[i//2][j//2] = '.'

        # Inicializa a fila para BFS e adiciona a posição inicial
        fila = deque([posicao_inicial])
        visitados = set(posicao_inicial)

        # Executa a busca em largura
        while fila:
            posicao_atual = fila.popleft()
            linha, coluna = posicao_atual

            # Verifica se alcançou a linha final
            if linha == linha_final:
                return True

            # Verifica movimentos possíveis (Cima, Baixo, Esquerda, Direita)
            for delta_linha, delta_coluna in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nova_linha = linha + delta_linha
                nova_coluna = coluna + delta_coluna

                # Verifica se a nova posição é válida e não foi visitada
                if 0 <= nova_linha < 9 and 0 <= nova_coluna < 9 and (nova_linha, nova_coluna) not in visitados:
                    # Verifica se não há barreira no caminho
                    if tabuleiro[linha * 2 + delta_linha][coluna * 2 + delta_coluna] == ' ':
                        fila.append((nova_linha, nova_coluna))
                        visitados.add((nova_linha, nova_coluna))

        # Se a fila esvaziar e a linha final não for alcançada, não há caminho
        return False
    def oposto(self):

        if self.turno == "P1":
            return "P2"
        else:
            return "P1"

    def criar_tabuleiro(self):
        # Cria um tabuleiro 9x9 com espaços vazios ('.') e espaços para barreiras (' ')
        self.tabuleiro = [['.' if (linha % 2 == 0 and coluna % 2 == 0) else ' ' for coluna in range(17)] for linha in range(17)]
        
        # Adiciona as peças dos jogadores no tabuleiro
        self.tabuleiro[0][8] = 'P1'  # Posição inicial do jogador 1
        self.tabuleiro[16][8] = 'P2'  # Posição inicial do jogador 2
        
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
        self.turno = self.oposto()
        return self.tabuleiro

    def imprimir_tabuleiro(self):
        # Imprime o tabuleiro
        for linha in self.tabuleiro:
            print(' '.join(linha))
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
    #     tabuleiro[nova_posicao[0]][nova_posicao[1]] = jogador  # ou 'P2', dependendo do jogador
        
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
        
        # Verifica se há uma barreira no caminho
        if self.tabuleiro[posicao_intermediaria[0]][posicao_intermediaria[1]] in ('-', '|'):
            return False, "Movimento inválido: há uma barreira no caminho."
        
        # Move a peça
        self.tabuleiro[posicao_atual[0]][posicao_atual[1]] = '.'
        self.tabuleiro[nova_posicao[0]][nova_posicao[1]] = self.turno  # 'P1' ou 'P2'
        
        self.turno = self.oposto()
        return True, nova_posicao



    def encontrar_posicao(self):
        # Converte o tabuleiro para um array NumPy
        tabuleiro_np = np.array(self.tabuleiro)
        
        # Usa np.where para encontrar a posição do 'P1'
        posicao = np.where(tabuleiro_np == self.turno)
        
        # np.where retorna uma tupla com arrays, pegamos o primeiro elemento de cada array
        return (posicao[0][0], posicao[1][0])
    
    def jogada_humano():
        jogada = -1
        while jogada not in jogo.jogos_validos():
            jogada = int(input("Escolha um quadrado (0-8):"))
        return jogada
    
    def turn(self):
        return self.turno

# Cria e imprime o tabuleiro
    
    
jogo = Quoridor()
#tabuleiro_quoridor = jogo.criar_tabuleiro()

vez_atual = "P1"

#posicao_atual_p1 = jogo.encontrar_posicao(tabuleiro_quoridor, "P1")  # Posição inicial do jogador 1(Ta chu)
#posicao_atual_p2 = jogo.encontrar_posicao(tabuleiro_quoridor, "P2")  # Posição inicial do jogador 1(Ta chu)

while(True):


    posicao_da_vez = jogo.encontrar_posicao()
    print("Jogador:", jogo.turn())
    jogada = input("Escolha: Mover(M), ou Parede(P): ")
    if(jogada == "M"):
        movimento = input("Selecione o Movimento(B,C,E,D): ")
        sucesso, resultado = jogo.mover_peca(posicao_da_vez, movimento)
        if sucesso:
            jogo.imprimir_tabuleiro()
            print("")
        else:
            print(resultado)
    elif(jogada == "P"):
        x = int(input("Digite a Linha: "))
        y = int(input("Digite a Coluna: "))
        orientacao = input("Digite a Orientação(H,V): ")
        tabuleiro_quoridor = jogo.adicionar_barreira(x, y, orientacao)  # Exemplo de adição de barreira horizontal
        jogo.imprimir_tabuleiro()
    else:
        print("Selecione uma jogada valida: ")



    # tabuleiro_quoridor = adicionar_barreira(tabuleiro_quoridor, 1, 7, 'V',posicao_atual_p1,posicao_atual_p2)  # Exemplo de adição de barreira horizontal
    # tabuleiro_quoridor = adicionar_barreira(tabuleiro_quoridor, 3, 9, 'H', posicao_atual_p1,posicao_atual_p2)  # Exemplo de adição de barreira horizontal
    #tabuleiro_quoridor = adicionar_barreira(tabuleiro_quoridor, 3, 9, 'H', posicao_atual_p1,posicao_atual_p2)  # Exemplo de adição de barreira horizontal

    #jogo.imprimir_tabuleiro(tabuleiro_quoridor)
    print("")
    
# Exemplo de uso da função
#tabuleiro_quoridor = criar_tabuleiro()


#movimento = 'E'  # Movimento para baixo
 # Lista de barreiras (ainda não implementada)

# sucesso, resultado = mover_peca(tabuleiro_quoridor, posicao_atual_p1, movimento, barreiras)

# if sucesso:
#     imprimir_tabuleiro(tabuleiro_quoridor)
# else:
#     print(resultado)

# print("")

# posicao_atual_p1 = encontrar_posicao(tabuleiro_quoridor, "P1")  # Posição inicial do jogador 1(Ta chu)
# posicao_atual_p2 = encontrar_posicao(tabuleiro_quoridor, "P2")  # Posição inicial do jogador 1(Ta chu)
# sucesso, resultado = mover_peca(tabuleiro_quoridor, posicao_atual_p1, movimento)
# if sucesso:
#     imprimir_tabuleiro(tabuleiro_quoridor)
# else:
#     print(resultado)