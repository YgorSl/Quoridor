def criar_tabuleiro():
    # Cria um tabuleiro 9x9 com espaços vazios ('.') e espaços para barreiras (' ')
    tabuleiro = [['.' if (linha % 2 == 0 and coluna % 2 == 0) else ' ' for coluna in range(17)] for linha in range(17)]
    
    # Adiciona as peças dos jogadores no tabuleiro
    tabuleiro[0][8] = 'P1'  # Posição inicial do jogador 1
    tabuleiro[16][8] = 'P2'  # Posição inicial do jogador 2
    
    return tabuleiro

def adicionar_barreira(tabuleiro, linha, coluna, orientacao):
    # Adiciona uma barreira no tabuleiro na posição e orientação especificadas
    # 'H' para horizontal e 'V' para vertical
    if orientacao == 'H':
        for offset in range(-1, 2):
            tabuleiro[linha][coluna + offset] = '-'
    elif orientacao == 'V':
        for offset in range(-1, 2):
            tabuleiro[linha + offset][coluna] = '|'

def imprimir_tabuleiro(tabuleiro):
    # Imprime o tabuleiro
    for linha in tabuleiro:
        print(' '.join(linha))
    print()

# Cria e imprime o tabuleiro
tabuleiro_quoridor = criar_tabuleiro()
adicionar_barreira(tabuleiro_quoridor, 1, 7, 'V')  # Exemplo de adição de barreira horizontal
adicionar_barreira(tabuleiro_quoridor, 8, 7, 'V')  # Exemplo de adição de barreira horizontal

imprimir_tabuleiro(tabuleiro_quoridor)