import numpy as np
from collections import deque

def acoes_possiveis(self, estado, turno):
    acoes = []

    # Encontre a posição atual do jogador
    posicao_atual = self.encontrar_posicao(turno, estado)

    direcoes = {'C': (-2, 0), 'B': (2, 0), 'E': (0, -2), 'D': (0, 2)}
    #delta = direcoes[movimento]
    for direcao in direcoes:

        delta = direcoes[direcao]

        nova_linha, nova_coluna = (posicao_atual[0] + delta[0], posicao_atual[1] + delta[1])
        posicao_intermediaria = (posicao_atual[0] + delta[0]//2, posicao_atual[1] + delta[1]//2)
        nova_posicao = (posicao_atual[0] + delta[0], posicao_atual[1] + delta[1])

        # Verifique se a nova posição é válida
        if (0 <= nova_posicao[0] < 17 and 0 <= nova_posicao[1] < 17):
            # Verifique se não há barreira no caminho
            if estado[posicao_intermediaria[0]][posicao_intermediaria[1]] not in ('-', '|'):
                acoes.append(("M", (direcao, nova_linha, nova_coluna)))  # Ação de mover

    # Verifique as posições para adicionar barreiras
    posicao_jogador = self.encontrar_posicao(turno, estado)  # Peça do jogador
    distancia_jogador_ate_objetivo = 16 - posicao_jogador[0]

    # Pontuação: quanto menor a distância da IA até o objetivo, melhor

    #So começa a tentar colocar barreira se for menor = 5 a distancia do oponente
    if distancia_jogador_ate_objetivo <= 10:
            for linha in range(posicao_jogador[0] - 1,  posicao_jogador[0] + 1):
                for coluna in range( posicao_jogador[1] - 1, posicao_jogador[1] + 1):
                    if estado[linha][coluna] == ' ':
                        # Verifique se é possível adicionar uma barreira horizontal
                        if self.verifica_parede(linha, coluna, 'H', estado, turno):
                            acoes.append(("P", (linha, coluna, 'H')))  # Ação de adicionar barreira horizontal
                        # Verifique se é possível adicionar uma barreira vertical
                        if self.verifica_parede(linha, coluna, 'V', estado, turno):
                            acoes.append(("P", (linha, coluna, 'V')))  # Ação de adicionar barreira vertical

    return acoes

def aplicar_acao(self, estado, acao, turno):
    tipo_acao, parametros = acao
    
    if tipo_acao == "M":
        # Ação de mover

        posicao_atual = self.encontrar_posicao(turno, estado)
        direcao, nova_linha, nova_coluna = parametros

    

        novo_estado = [linha[:] for linha in estado]  # Crie uma cópia do estado atual

        direcoes = {'C': (-2, 0), 'B': (2, 0), 'E': (0, -2), 'D': (0, 2)}
        delta = direcoes[direcao]
        nova_posicao = (posicao_atual[0] + delta[0], posicao_atual[1] + delta[1])

        if novo_estado[nova_posicao[0]][nova_posicao[1]] in ('P', 'A'):
        # Pula para a próxima posição válida
            nova_posicao = (nova_posicao[0] + delta[0], nova_posicao[1] + delta[1])
            novo_estado[posicao_atual[0]][posicao_atual[1]] = '.'
            novo_estado[nova_posicao[0]][nova_posicao[1]] = turno  # 'P' ou 'A'
        else:
            novo_estado[posicao_atual[0]][posicao_atual[1]] = '.'  # Limpe a posição atual
            novo_estado[nova_linha][nova_coluna] = turno  # Atualize a nova posição

        tabuleiro_np = np.array(estado)
    
        # Usa np.where para encontrar a posição do 'P'
        posicao = np.where(tabuleiro_np == 'P')
        if posicao is None:
            print('')
        return novo_estado
    
    elif tipo_acao == "P":
        # Ação de adicionar barreira
        linha, coluna, orientacao = parametros
        if self.verifica_parede(linha, coluna, orientacao, estado, turno):
            novo_estado = [linha[:] for linha in estado]  # Crie uma cópia do estado atual
            if orientacao == 'H':
                for offset in range(-1, 2):
                    novo_estado[linha][coluna + offset] = '-'
            elif orientacao == 'V':
                for offset in range(-1, 2):
                    novo_estado[linha + offset][coluna] = '|'
            return novo_estado
        else:
            # A posição não é válida para adicionar uma barreira
            return estado
    else:
        # Ação desconhecida (trate conforme necessário)
        return estado
    
# def avaliar_estado(self, tabuuleiro):

#     minha_posicao = self.encontrar_posicao('A', tabuuleiro)  # Peça da IA
#     objetivo_linha = 0  # Linha oposta (objetivo)
#     distancia_ate_objetivo = objetivo_linha - minha_posicao[0]

#     # Verifique a posição do jogador
#     posicao_jogador = self.encontrar_posicao('P', tabuuleiro)  # Peça do jogador
#     distancia_jogador_ate_objetivo = objetivo_linha - posicao_jogador[0]

#     # Pontuação: quanto menor a distância da IA até o objetivo, melhor
#     pontuacao = 10 - distancia_ate_objetivo

#     # Bloqueie o jogador se ele estiver próximo do objetivo
#     if distancia_jogador_ate_objetivo <= 5:
#         pontuacao += 5

#     # Penalize se houver paredes no caminho direto da IA
#     if not self.caminho_livre(minha_posicao, posicao_jogador, tabuuleiro):
#         pontuacao -= 3

#     return pontuacao

def avaliar_estado(self, estado, turno):
    pontuacao = 0
    if turno == "P":
        #return 10 * abs(self.encontrar_posicao("P", estado)[0])
    


        # Define o objetivo final para cada jogador
        objetivo = 16 if turno == "P" else 0

        # Encontra a posição inicial do jogador
        posicao_inicial = self.encontrar_posicao(turno, estado)

        # Calcula a distância até o objetivo
        distancia_ate_objetivo = abs(objetivo - posicao_inicial[0])

        # Inicializa a pontuação
        pontuacao = 0

        # Nas primeiras jogadas, priorize o movimento em direção ao objetivo
        if distancia_ate_objetivo > 12:  # Considera que o jogo está no início
            pontuacao -= (16 - distancia_ate_objetivo)

        # Evite colocar barreiras inicialmente
        if self.qtd_paredes(turno)> 8:  # Se o self.turno_mm ainda tem muitas barreiras
            pontuacao += 1  # Penaliza a colocação de barreiras

        # Se o adversário estiver próximo do objetivo, considere bloquear seu caminho
        posicao_adversario = self.encontrar_posicao("A", estado)
        if posicao_adversario[0] < 16 and posicao_adversario[1] < 16:
            if estado[posicao_adversario[0]+1][posicao_adversario[1]+1] == "|":
                pontuacao -=8
            
            if estado[posicao_adversario[0]+1][posicao_adversario[1]+1] == "-":
                pontuacao +=1
        if posicao_adversario[0] > 0 and posicao_adversario[1] > 0:
            if estado[posicao_adversario[0]-1][posicao_adversario[1]-1] == "|":
                pontuacao -=8
            
            if estado[posicao_adversario[0]-1][posicao_adversario[1]-1] == "-":
                pontuacao -=8

        distancia_adversario_ate_objetivo = abs(objetivo - posicao_adversario[0])
        if distancia_adversario_ate_objetivo <= 9:
            pontuacao -= 5  # Incentiva a colocação de barreiras para bloquear o adversário

        if self.is_end(estado):
            if self.get_winner(estado) == "P":
                return float("-inf")
            else:
                return float("inf")
    else:
            # Define o objetivo final para cada jogador
        objetivo = 16 if turno == "P" else 0

        # Encontra a posição inicial do jogador
        posicao_inicial = self.encontrar_posicao(turno, estado)

        # Calcula a distância até o objetivo
        distancia_ate_objetivo = abs(objetivo - posicao_inicial[0])

        # Inicializa a pontuação
        pontuacao = 0

        # Nas primeiras jogadas, priorize o movimento em direção ao objetivo
        if distancia_ate_objetivo > 12:  # Considera que o jogo está no início
            pontuacao += (16 - distancia_ate_objetivo)

        # Evite colocar barreiras inicialmente
        if self.qtd_paredes(turno)> 8:  # Se o self.turno_mm ainda tem muitas barreiras
            pontuacao -= 1  # Penaliza a colocação de barreiras

        # Se o adversário estiver próximo do objetivo, considere bloquear seu caminho
        posicao_adversario = self.encontrar_posicao("P", estado)
        if posicao_adversario[0] < 16 and posicao_adversario[1] < 16:
            if estado[posicao_adversario[0]+1][posicao_adversario[1]+1] == "|":
                pontuacao +=6
            
            if estado[posicao_adversario[0]+1][posicao_adversario[1]+1] == "-":
                pontuacao +=8
        if posicao_adversario[0] > 0 and posicao_adversario[1] > 0:
            if estado[posicao_adversario[0]-1][posicao_adversario[1]-1] == "|":
                pontuacao +=8
            
            if estado[posicao_adversario[0]-1][posicao_adversario[1]-1] == "-":
                pontuacao -=3

        distancia_adversario_ate_objetivo = abs(objetivo - posicao_adversario[0])
        if distancia_adversario_ate_objetivo <= 9:
            pontuacao += 5  # Incentiva a colocação de barreiras para bloquear o adversário
        #return 10 * (abs(self.encontrar_posicao("A", estado)[0] - 16))

    # Retorna a pontuação avaliada
        if self.is_end(estado):
            if self.get_winner(estado) == "P":
                return float("-inf")
            else:
                return float("inf")
    return pontuacao

def caminho_livre(self, posicao1, posicao2, tabuleiro):
    linha1, coluna1 = posicao1
    linha2, coluna2 = posicao2

    # Verifique se não há paredes no caminho direto
    for linha in range(min(linha1, linha2) + 1, max(linha1, linha2)):
        if tabuleiro[linha][coluna1] == '|' or tabuleiro[linha][coluna2] == '|':
            return False
    return True
    
def minimax(self, estado,turno, profundidade, alfa, beta, maximizando):
    if profundidade == 0 or self.is_end(estado):
        return self.avaliar_estado(estado, turno)

    if maximizando:
        melhor_valor = float("-inf")
        acaoo = self.acoes_possiveis(estado, turno)
        acaoo.__len__()
        for acao in self.acoes_possiveis(estado, turno):
            novo_estado = self.aplicar_acao(estado, acao, turno)
            turnomin = self.oposto(turno)
            valor = self.minimax(novo_estado,turnomin, profundidade - 1, alfa, beta, False)
            melhor_valor = max(melhor_valor, valor)
            alfa = max(melhor_valor, alfa)
            if beta <= alfa:
                break  # Poda alfa-beta
        return melhor_valor
    else:
        melhor_valor = float("inf")
        for acao in self.acoes_possiveis(estado,turno):
            novo_estado = self.aplicar_acao(estado, acao, turno)
            turno_max = self.oposto(turno)
            valor = self.minimax(novo_estado,turno_max, profundidade - 1, alfa, beta, True)
            melhor_valor = min(melhor_valor, valor)
            beta = min(melhor_valor, beta)
            if beta <= alfa:
                break  # Poda alfa-beta
        return melhor_valor

def melhor_jogada(self, turno):
    melhor_pontuacao = float("-inf")
    melhor_acao = None
    turno = self.turno
    for acao in self.acoes_possiveis(self.tabuleiro, turno):
        novo_estado = self.aplicar_acao(self.tabuleiro, acao, turno)
    
        # Avalie o estado usando a heurística
        #pontuacao = self.avaliar_estado(novo_estado)
        
        # Chame o Minimax para avaliar os estados sucessores
        pontuacao = self.minimax(novo_estado,turno, profundidade=3, alfa=float("-inf"), beta=float("inf") ,maximizando=False)
        if pontuacao > melhor_pontuacao:
            melhor_pontuacao = pontuacao
            melhor_acao = acao
    return melhor_acao