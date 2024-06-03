from copy import copy
from heuristica_simples import heuristica_simples
from fila import PriorityQueueItem
from queue import PriorityQueue



def astar(jogo , check_blockage, heuristic=heuristica_simples):
    visited = set()

    def cost_function(path):
        actions = []
        current_cost = 0
        for state in path:
            current_cost += state[1][2]
        current_cost += len(actions)
        current_cost += heuristic(path[-1][0])
        return current_cost

    queue = PriorityQueue()
    if jogo.turno == "P":
        pos = jogo.encontrar_posicao("P")
    else:
        pos = jogo.encontrar_posicao("A")

    queue.put(PriorityQueueItem(0, [(jogo, ((pos[0], pos[1]), (0, 0), 0))]))

    while not queue.empty():
        item = queue.get()
        path = item.item
        current_state = path[-1][0]
        current_simplified_state = path[-1][1]
        if current_state.game_end():
            if check_blockage:
                return True
            final_path = []
            for state in path:
                final_path.append(state[1][1])
            return len(final_path[1:])
        if current_simplified_state not in visited:
            visited.add(current_simplified_state)
            for successor in current_state.avalia_mov():
                if successor[1] not in visited:
                    successor_path = copy(path)
                    successor_path.append(successor)
                    queue.put(PriorityQueueItem(cost_function(successor_path), successor_path))
    if check_blockage:
        return False
    return 0
