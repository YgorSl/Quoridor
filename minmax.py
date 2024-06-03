
from copy import deepcopy
from astar import astar

        
def minimax(jogo,turno, profundidade, alfa, beta, maximizando):
    if profundidade == 0 or jogo.game_end():
        return avaliar_estado(jogo, maximizando)

    # if jogo.is_end():
    #     return avaliar_estado(jogo)
    if maximizando:
        melhor_valor = float("-inf")
        for acao in jogo.acoes_possiveis(): #AS AÇÕES POSSIVEIS TAO LEVANDO O OBJETO JOGO QUE TEM COMO TURNO O A
            copia_jogo = deepcopy(jogo)
            copia_jogo.tabuleiro = copia_jogo.aplicar_acao(acao, turno)
            copia_jogo.turno = copia_jogo.oposto(turno)
            copia_jogo.state['player_turn'] = 1 - copia_jogo.state['player_turn']
            valor = minimax(copia_jogo, copia_jogo.turno, profundidade - 1, alfa, beta, False)
            melhor_valor = max(melhor_valor, valor)
            alfa = max(valor, alfa)
            if beta <= alfa:
                break  # Poda alfa-beta
        return alfa
    else:
        melhor_valor = float("inf")
        for acao in jogo.acoes_possiveis():
            copia_jogo = deepcopy(jogo)
            copia_jogo.tabuleiro = copia_jogo.aplicar_acao(acao, turno)
            copia_jogo.turno = copia_jogo.oposto(turno)
            copia_jogo.state['player_turn'] = 1 - copia_jogo.state['player_turn']
            valor = minimax(copia_jogo,copia_jogo.turno, profundidade - 1, alfa, beta, True)
            melhor_valor = min(melhor_valor, valor)
            beta = min(valor, beta)
            if beta <= alfa:
                break  # Poda alfa-beta
        return beta

def melhor_jogada(jogo):
    melhor_pontuacao = float("inf")
    melhor_acao = None
    turno = jogo.turno
    for acao in jogo.acoes_possiveis():
        copia_jogo = deepcopy(jogo)
        copia_jogo.tabuleiro = copia_jogo.aplicar_acao(acao, turno)
        copia_jogo.turno = copia_jogo.oposto(turno)
       
        # Chame o Minimax para avaliar os estados sucessores
        pontuacao = minimax(copia_jogo ,jogo.oposto(turno), profundidade=3, alfa=float("-inf"), beta=float("inf"),maximizando=True)
        #print(f"Ação {acao}, Pontuação {pontuacao}")  # Debug
        if pontuacao < melhor_pontuacao:
            melhor_pontuacao = pontuacao
            melhor_acao = acao
    #print(f"Melhor ação {melhor_acao}, Melhor pontuação {melhor_pontuacao}")  # Debug
    return melhor_acao


def avaliar_estado(game_state, player_one_maximizer):
    # Encontrar as posições dos jogadores
    player_one_pos = game_state.encontrar_posicao("P")
    player_two_pos = game_state.encontrar_posicao("A")

    # Calcular a distância até a meta para cada jogador usando A*
 
    # Inicializar a pontuação
    result = 0

    if player_one_maximizer:
        player_path_len = game_state.calculate_distance_to_goal(game_state.state, 1)
        opponent_path_len = game_state.calculate_distance_to_goal(game_state.state, 0)

        player_one_pos = game_state.encontrar_posicao("P")
        player_two_pos = game_state.encontrar_posicao("A")

        # Diferença de caminhos
        result += (opponent_path_len - player_path_len) * 10

        # Valorizar o controle de barreiras
        result += (game_state.paredes_p - game_state.paredes_a) * 5

        # Recompensa pela vitória
        if player_one_pos[0] == 0:
            result += 100

        # Recompensa por avanço
        if player_one_pos[0] < player_two_pos[0]:
            result += 20  # Bonus for moving closer to the goal
        else:
            result -= 10  # Penalty for moving away from the goal

    else:
        player_one_pos = game_state.encontrar_posicao("A")
        player_two_pos = game_state.encontrar_posicao("P")


        player_path_len = game_state.calculate_distance_to_goal(game_state.state, 0)
        opponent_path_len = game_state.calculate_distance_to_goal(game_state.state, 1)

        #Diferença de caminhos
        result += (player_path_len - opponent_path_len) * 10
        result += player_path_len * 10
        
        #
        #Valorizar o controle de barreiras
        result += (game_state.paredes_a - game_state.paredes_p) * 5

        # Recompensa pela vitória
        # if player_two_pos[0] == 16:
        #     result += 100

        # Recompensa por avanço
        if player_path_len > player_path_len:
            result -= 20  # Bonus for moving closer to the goal
        else:
            result += 30  # Penalty for moving away from the goal

    return float(result)  # Certifique-se de retornar um valor numérico