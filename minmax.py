
from copy import copy
from astar import astar

def avaliar_estado(jogo ):
    player_one_pos = jogo.encontrar_posicao("P")
    player_two_pos = jogo.encontrar_posicao("A")

    player_one_distance = player_one_pos[0] // 2
    player_two_distance = (16 - player_two_pos[0]) // 2
    result = 0

    if jogo.turno == "P":

        opponent_path_len, player_path_len = player_two_distance, player_one_distance
        if jogo.qtd_paredes("P") != 10 and jogo.qtd_paredes("A") != 10:
            previous = jogo.turno
            jogo.turno = jogo.oposto(jogo.turno)
            player_path_len = astar(jogo, False)
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
        if jogo.encontrar_posicao("P")[0] == 0:
            result += 100
        if player_path_len == 0 and jogo.encontrar_posicao("P")[0] != 0:
            result -= 500
        return result

    else:
        opponent_path_len, player_path_len = player_one_distance, player_two_distance
        if jogo.qtd_paredes("P") != 10 and jogo.qtd_paredes("A") != 10:
            previous = jogo.turno
            jogo.turno = jogo.oposto(jogo.turno)
            player_path_len = astar(jogo, False)
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
        if jogo.encontrar_posicao("A")[0] == 16:
            result += 100
        if player_path_len == 0 and jogo.encontrar_posicao("A")[0] != 16:
            result -= 500
        return result
        
def minimax(jogo,turno, profundidade, alfa, beta, maximizando):
    if profundidade == 0:
        return avaliar_estado(jogo)

    # if jogo.is_end():
    #     return avaliar_estado(jogo)
    if maximizando:
        melhor_valor = float("-inf")
        for acao in jogo.acoes_possiveis(): #AS AÇÕES POSSIVEIS TAO LEVANDO O OBJETO JOGO QUE TEM COMO TURNO O A
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
        for acao in jogo.acoes_possiveis():
            acao[0].tabuleiro = acao[0].aplicar_acao(acao, turno)
            acao[0].turno = jogo.oposto(turno)
            valor = minimax(acao[0],acao[0].turno, profundidade - 1, alfa, beta, True)
            melhor_valor = min(melhor_valor, valor)
            beta = min(valor, beta)
            if beta <= alfa:
                break  # Poda alfa-beta
        return melhor_valor

def melhor_jogada(jogo):
    melhor_pontuacao = float("-inf")
    melhor_acao = None
    turno = jogo.turno
    for acao in jogo.acoes_possiveis():
        acao[0].tabuleiro = jogo.aplicar_acao(acao, turno)
    
        # Avalie o estado usando a heurística
        #pontuacao = jogo.avaliar_estado(novo_estado)
        
        # Chame o Minimax para avaliar os estados sucessores
        pontuacao = minimax(acao[0],jogo.oposto(turno), profundidade=3, alfa=float("-inf"), beta=float("inf"),maximizando=True)
        if pontuacao > melhor_pontuacao:
            melhor_pontuacao = pontuacao
            melhor_acao = acao
    return melhor_acao