from quoridor import Quoridor
from copy import copy
from astar import astar

def acoes_possiveis(jogo:Quoridor):
    acoes = []

    # Encontre a posição atual do jogador
    posicao_atual = jogo.encontrar_posicao(jogo.turno, jogo.tabuleiro)

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
            
            if jogo.tabuleiro[posicao_intermediaria[0]][posicao_intermediaria[1]] not in ('-', '|'):
                prox = copy(jogo)
                acoes.append((prox, "M", (direcao, nova_linha, nova_coluna)))  # Ação de mover

    # Verifique as posições para adicionar barreiras
    posicao_jogador = jogo.encontrar_posicao(jogo.turno, jogo.tabuleiro)  # Peça do jogador
    posicao_oponente = jogo.encontrar_posicao(jogo.oposto(jogo.turno), jogo.tabuleiro)
    if jogo.turno == "P":  
        distancia_jogador_ate_objetivo = posicao_jogador[0]
    else:
        distancia_jogador_ate_objetivo = 16 - posicao_jogador[0]

    # Pontuação: quanto menor a distância da IA até o objetivo, melhor


    #So começa a tentar colocar barreira se for menor = 5 a distancia do oponente
    #if distancia_jogador_ate_objetivo <= 10:
    for linha in range(posicao_jogador[0] - 1,  posicao_jogador[0] + 1):
        for coluna in range( posicao_jogador[1] - 1, posicao_jogador[1] + 1):
            if jogo.tabuleiro[linha][coluna] == ' ':
                # Verifique se é possível adicionar uma barreira horizontal
                if jogo.verifica_parede(linha, coluna, 'H', jogo.tabuleiro, jogo.turno):
                    prox = copy(jogo)
                    acoes.append((prox, "P", (linha, coluna, 'H')))  # Ação de adicionar barreira horizontal
                # Verifique se é possível adicionar uma barreira vertical
                if jogo.verifica_parede(linha, coluna, 'V', jogo.tabuleiro, jogo.turno):
                    prox = copy(jogo)
                    acoes.append((prox, "P", (linha, coluna, 'V')))  # Ação de adicionar barreira vertical

    return acoes

def avaliar_estado(jogo : Quoridor):
    player_one_pos = jogo.encontrar_posicao("P",jogo.tabuleiro)
    player_two_pos = jogo.encontrar_posicao("A",jogo.tabuleiro)

    player_one_distance = player_one_pos[0] // 2
    player_two_distance = (16 - player_two_pos[0]) // 2
    result = 0

    if jogo.turno == "P":

        opponent_path_len, player_path_len = player_two_distance, player_one_distance
        if jogo.qtd_paredes("P") != 10 and jogo.qtd_paredes("A") != 10:
            previous = jogo.turno
            jogo.turno = jogo.oposto()
            player_path_len = astar(jogo,player_one_pos,player_two_pos, False)
            jogo.turno = previous

        result += opponent_path_len
        result -= player_one_distance
        num = 100
        if player_path_len != 0:
            num = player_path_len
        result += round(100 / num, 2)

        num_1 = 50
        if player_two_distance != 0:
            num_1 = player_two_distance
        result -= round(50 / num_1, 2)

        result += (jogo.paredes_p - jogo.paredes_a)
        if jogo.encontrar_posicao("P",jogo.tabuleiro)[0] == 0:
            result += 100
        if player_path_len == 0 and jogo.encontrar_posicao("P",jogo.tabuleiro)[0] != 0:
            result -= 500
        return result

    else:
        opponent_path_len, player_path_len = player_one_distance, player_two_distance
        if jogo.qtd_paredes("P") != 10 and jogo.qtd_paredes("A") != 10:
            previous = jogo.turno
            jogo.turno = jogo.oposto()
            player_path_len = astar(jogo,player_one_pos,player_two_pos, False)
            jogo.turno = previous
        
        result += opponent_path_len
        
        result -= player_two_distance
        num = 100
        if player_path_len != 0:
            num = player_path_len
        result += round(100 / num, 2)

        num_1 = 50
        if player_one_distance != 0:
            num_1 = player_one_distance
        result -= round(50 / num_1, 2)

        result += (jogo.paredes_a - jogo.paredes_p)
        if jogo.encontrar_posicao("A",jogo.tabuleiro)[0] == 16:
            result += 100
        if player_path_len == 0 and jogo.encontrar_posicao("A",jogo.tabuleiro)[0] != 16:
            result -= 500
        return result
        
def minimax(jogo : Quoridor ,turno, profundidade, alfa, beta, maximizando):
    if profundidade == 0:
        return avaliar_estado(jogo)

    # if jogo.is_end():
    #     return avaliar_estado(jogo)
    if maximizando:
        melhor_valor = float("-inf")
        for acao in acoes_possiveis(jogo): #AS AÇÕES POSSIVEIS TAO LEVANDO O OBJETO JOGO QUE TEM COMO TURNO O A
            acao[0].tabuleiro = acao[0].aplicar_acao(acao, turno)
            acao[0].turno = jogo.oposto(turno)
            valor = minimax(acao[0],acao[0].turno, profundidade - 1, alfa, beta, False)
            melhor_valor = max(melhor_valor, valor)
            alfa = max(valor, alfa)
            if beta <= alfa:
                break  # Poda alfa-beta
        return melhor_valor
    else:
        melhor_valor = float("inf")
        for acao in acoes_possiveis(jogo):
            acao[0].tabuleiro = acao[0].aplicar_acao(acao, turno)
            acao[0].turno = jogo.oposto(turno)
            valor = minimax(acao[0],acao[0].turno, profundidade - 1, alfa, beta, True)
            melhor_valor = min(melhor_valor, valor)
            beta = min(valor, beta)
            if beta <= alfa:
                break  # Poda alfa-beta
        return melhor_valor

def melhor_jogada(jogo : Quoridor):
    melhor_pontuacao = float("-inf")
    melhor_acao = None
    turno = jogo.turno
    for acao in acoes_possiveis(jogo):
        acao[0].tabuleiro = jogo.aplicar_acao(acao, turno)
    
        # Avalie o estado usando a heurística
        #pontuacao = jogo.avaliar_estado(novo_estado)
        
        # Chame o Minimax para avaliar os estados sucessores
        pontuacao = minimax(acao[0],jogo.oposto(turno), profundidade=3, alfa=float("-inf"), beta=float("inf"),maximizando=True)
        if pontuacao > melhor_pontuacao:
            melhor_pontuacao = pontuacao
            melhor_acao = acao
    return melhor_acao