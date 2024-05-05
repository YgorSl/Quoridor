from astar import astar
from quoridor import encontrar_posicao, qtd_paredes

def heuristica(game_state, player_one_maximizer):
    player_one_pos = encontrar_posicao("P",game_state)
    player_two_pos = encontrar_posicao("A",game_state)

    player_one_distance = player_one_pos[0] // 2
    player_two_distance = (16 - player_two_pos[0]) // 2
    result = 0

    if player_one_maximizer:

        opponent_path_len, player_path_len = player_two_distance, player_one_distance
        if qtd_paredes("P") != 10 and qtd_paredes("A") != 10:
            previous = game_state.player_one
            game_state.player_one = True
            player_path_len = astar(game_state, False)
            game_state.player_one = previous

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

        result += (game_state.player_one_walls_num - game_state.player_two_wall_num)  # mozda ovo promijeni
        if game_state.player_one_pos[0] == 0:
            result += 100
        if player_path_len == 0 and game_state.player_one_pos[0] != 0:
            result -= 500
        return result




    else:
        opponent_path_len, player_path_len = player_one_distance, player_two_distance
        if game_state.player_one_walls_num != 10 and game_state.player_two_wall_num != 10:
            previous = game_state.player_one
            game_state.player_one = False
            player_path_len = astar(game_state, False)
            game_state.player_one = previous

        
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

        result += (game_state.player_two_wall_num - game_state.player_one_walls_num)  # mozda ovo promijeni
        if game_state.player_two_pos[0] == 16:
            result += 100
        if player_path_len == 0 and game_state.player_two_pos[0] != 16:
            result -= 500
        return result
