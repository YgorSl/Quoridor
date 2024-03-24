import numpy as np
from collections import deque

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
def oposto(jogador):

    if jogador == "P1":
      return "P2"
    else:
      return "P1"

def criar_tabuleiro():
    # Cria um tabuleiro 9x9 com espaços vazios ('.') e espaços para barreiras (' ')
    tabuleiro = [['.' if (linha % 2 == 0 and coluna % 2 == 0) else ' ' for coluna in range(17)] for linha in range(17)]
    
    # Adiciona as peças dos jogadores no tabuleiro
    tabuleiro[0][8] = 'P1'  # Posição inicial do jogador 1
    tabuleiro[16][8] = 'P2'  # Posição inicial do jogador 2
    
    return tabuleiro

def adicionar_barreira(tabuleiro, linha, coluna, orientacao,posicao_p1, posicao_p2):
    # Adiciona uma barreira no tabuleiro na posição e orientação especificadas
    # 'H' para horizontal e 'V' para vertical

    chegada_p1 = 8
    chegada_p2 = 0 

    tabuleiro_antigo = tabuleiro


    if orientacao == 'H':
        for offset in range(-1, 2):
            tabuleiro[linha][coluna + offset] = '-'
    elif orientacao == 'V':
        for offset in range(-1, 2):
            tabuleiro[linha + offset][coluna] = '|'

    if existe_caminho(tabuleiro, posicao_p1, chegada_p1):
        print("Ainda existe um caminho após adicionar a barreira.")
        
    else:
        print("A barreira bloqueia todos os caminhos. Movimento inválido.")
        return tabuleiro_antigo

    if existe_caminho(tabuleiro, posicao_p2, chegada_p2):
        print("Ainda existe um caminho após adicionar a barreira.")
    else:
        print("A barreira bloqueia todos os caminhos. Movimento inválido.")
        return tabuleiro_antigo
    
    return tabuleiro

def imprimir_tabuleiro(tabuleiro):
    # Imprime o tabuleiro
    for linha in tabuleiro:
        print(' '.join(linha))
    print()



def mover_peca(tabuleiro, posicao_atual, movimento, jogador):
    # Calcula a nova posição baseada no movimento
    direcoes = {'C': (-2, 0), 'B': (2, 0), 'E': (0, -2), 'D': (0, 2)}
    delta = direcoes[movimento]
    nova_posicao = (posicao_atual[0] + delta[0], posicao_atual[1] + delta[1])
    
    # Verifica se a nova posição é válida
    if not (0 <= nova_posicao[0] < 17 and 0 <= nova_posicao[1] < 17):
        return False, "Movimento inválido: fora do tabuleiro."
    
    # Verifica se há uma barreira no caminho
    posicao_barreira = (posicao_atual[0] + delta[0]//2, posicao_atual[1] + delta[1]//2)
    if tabuleiro[posicao_barreira[0]][posicao_barreira[1]] in ('-', '|'):
        return False, "Movimento inválido: há uma barreira no caminho."
    
    # Move a peça
    tabuleiro[posicao_atual[0]][posicao_atual[1]] = '.'
    tabuleiro[nova_posicao[0]][nova_posicao[1]] = jogador  # ou 'P2', dependendo do jogador
    
    return True, nova_posicao


def encontrar_posicao(tabuleiro, jogador):
    # Converte o tabuleiro para um array NumPy
    tabuleiro_np = np.array(tabuleiro)
    
    # Usa np.where para encontrar a posição do 'P1'
    posicao = np.where(tabuleiro_np == jogador)
    
    # np.where retorna uma tupla com arrays, pegamos o primeiro elemento de cada array
    return (posicao[0][0], posicao[1][0])

# Cria e imprime o tabuleiro
tabuleiro_quoridor = criar_tabuleiro()

vez_atual = "P1"

posicao_atual_p1 = encontrar_posicao(tabuleiro_quoridor, "P1")  # Posição inicial do jogador 1(Ta chu)
posicao_atual_p2 = encontrar_posicao(tabuleiro_quoridor, "P2")  # Posição inicial do jogador 1(Ta chu)

while(True):


    posicao_da_vez = encontrar_posicao(tabuleiro_quoridor, vez_atual)
    print("Jogador:", vez_atual)
    jogada = input("Escolha: Mover: M, ou Parede: P")
    if(jogada == "M"):
        movimento = input("Selecione o Movimento(B,C,E,D)")
        sucesso, resultado = mover_peca(tabuleiro_quoridor, posicao_da_vez, movimento, vez_atual)
        if sucesso:
            imprimir_tabuleiro(tabuleiro_quoridor)
        else:
            print(resultado)
    elif(jogada == "P"):
        x = int(input("Digite a Linha"))
        y = int(input("Digite a Coluna"))
        tabuleiro_quoridor = adicionar_barreira(tabuleiro_quoridor, x, y, 'V', posicao_atual_p1,posicao_atual_p2)  # Exemplo de adição de barreira horizontal



    # tabuleiro_quoridor = adicionar_barreira(tabuleiro_quoridor, 1, 7, 'V',posicao_atual_p1,posicao_atual_p2)  # Exemplo de adição de barreira horizontal
    # tabuleiro_quoridor = adicionar_barreira(tabuleiro_quoridor, 3, 9, 'H', posicao_atual_p1,posicao_atual_p2)  # Exemplo de adição de barreira horizontal
    #tabuleiro_quoridor = adicionar_barreira(tabuleiro_quoridor, 3, 9, 'H', posicao_atual_p1,posicao_atual_p2)  # Exemplo de adição de barreira horizontal

    imprimir_tabuleiro(tabuleiro_quoridor)
    print("")
    vez_atual = oposto(vez_atual)
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