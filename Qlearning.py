import numpy as np
import random
import pickle

class QLearningAgent:
    def __init__(self, action_space_size = 12, state_space_size=None, learning_rate=0.1, discount_factor=0.99, exploration_rate=1.0, exploration_decay=0.995, min_exploration_rate=0.01):
        self.action_space_size = action_space_size
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.exploration_rate = exploration_rate
        self.exploration_decay = exploration_decay
        self.min_exploration_rate = min_exploration_rate
        self.ALL_ACTIONS = []
        self.ACTION_INDEX_MAP = {}

        
        if state_space_size:
            self.q_table = np.zeros((state_space_size, action_space_size))
        else:
            self.q_table = {}

    def state_to_index(self, state):
        player1_pos = state['player_positions'][0]
        player2_pos = state['player_positions'][1]
        barriers_tuple = tuple([(barrier['x'], barrier['y'], barrier['orientation']) for barrier in state['barriers']])
        remaining_barriers = tuple(state['remaining_barriers'])

        state_tuple = (player1_pos, player2_pos, barriers_tuple, remaining_barriers)
        state_index = hash(state_tuple)
        return state_index
    
    def action_to_index(self, action):
        return self.ACTION_INDEX_MAP[action]

    def index_to_action(self, index):
        return self.ALL_ACTIONS[index]

    def expand_actions(self, possible_actions):
        if len(possible_actions) < self.action_space_size:
            possible_actions.extend([None] * (self.action_space_size - len(possible_actions)))
        return possible_actions[:self.action_space_size]  # Garantir que a lista não exceda o tamanho máximo

    def choose_action(self, state, env):
        state_index = self.state_to_index(state)
        possible_actions = env.acoes_possiveis()
        possible_actions = self.expand_actions(possible_actions)
        self.ALL_ACTIONS = possible_actions
        self.ACTION_INDEX_MAP = {action: index for index, action in enumerate(self.ALL_ACTIONS)}


        
        if state_index not in self.q_table:
            self.q_table[state_index] = np.zeros(self.action_space_size)
        
        if random.uniform(0, 1) < self.exploration_rate:
            action_index = random.randint(0, self.action_space_size - 1)  # Explore
        else:
            action_index = np.argmax(self.q_table[state_index])  # Exploit
        
        selected_action = self.index_to_action(action_index)
        while selected_action is None:
            action_index = random.randint(0, self.action_space_size - 1)
            selected_action = self.index_to_action(action_index)
        
        return selected_action

    def update_q_table(self, state, action, reward, next_state, env):
        state_index = self.state_to_index(state)
        next_state_index = self.state_to_index(next_state)

        if state_index not in self.q_table:
            self.q_table[state_index] = np.zeros(self.action_space_size)
        if next_state_index not in self.q_table:
            self.q_table[next_state_index] = np.zeros(self.action_space_size)

        action_index = self.get_action_index(state, action, env)  # Você precisa de uma função para converter ação para índice
        best_next_action = np.argmax(self.q_table[next_state_index])
        td_target = reward + self.discount_factor * self.q_table[next_state_index][best_next_action]
        td_error = td_target - self.q_table[state_index][action_index]
        self.q_table[state_index][action_index] += self.learning_rate * td_error

    def get_action_index(self, state, action, env):
        # possible_actions = env.acoes_possiveis()
        # possible_actions = self.expand_actions(possible_actions)
        # return possible_actions.index(action)
        return self.action_to_index(action)


    def decay_exploration_rate(self):
        self.exploration_rate = max(self.min_exploration_rate, self.exploration_rate * self.exploration_decay)

    
    def save_q_table(self, filename):
        with open(filename, 'wb') as f:
            pickle.dump(self.q_table, f)

    def load_q_table(self, filename):
        with open(filename, 'rb') as f:
            self.q_table = pickle.load(f)
#Exemplo de uso:

