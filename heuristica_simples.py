def heuristica_simples(game_state):
    if game_state.player_one:
        return 100 * abs(game_state.player_one_pos[0])
    else:
        return 100 * (abs(game_state.player_two_pos[0] - 16))