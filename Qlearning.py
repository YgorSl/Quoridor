import numpy as np
import random
import pickle
import csv

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

    def treinar(self, num_episodes, log_filename,env,agent):
        self.load_q_table('q_table3.pkl')


        with open(log_filename, 'a', newline='') as csvfile:
            log_writer = csv.writer(csvfile)
            log_writer.writerow(['Episode', 'Winner', 'Reward'])

        for episode in range(num_episodes):
            try:
                
                total_reward = self.run_episode(env, agent, log_filename,episode)
                print(f"Episode {episode} - Total Reward: {total_reward}")
                if episode %100 == 0:
                    agent.save_q_table('q_table3.pkl')
            except Exception as e:
                print(f"Ocorreu um erro: {e}")
                agent.save_q_table('q_table3.pkl')
                print("Q-Table salva após erro.")
                continue
            else:

                agent.save_q_table('q_table3.pkl')
        agent.save_q_table('q_table3.pkl')

    def run_episode(self, env, agent, log_filename, episode):
        
        state = env.reset()
        total_reward = 0

        

        while not env.check_if_done():
            if state['player_turn'] == 1:  # Turno do agente
                action = agent.choose_action(state, env)
                next_state, reward, done = env.step(action)
                agent.update_q_table(state, action, reward, next_state, env)
                state = next_state
                total_reward += reward

            # Opponent's turn (assuming the environment handles the opponent's move)
            else:
                opponent_action = env.heuristic_opponent(state)
                env.tabuleiro = env.aplicar_acao(opponent_action,"A")
                state = env.state

                # random_oponent = env.acoes_possiveis()
                # rand_action = random.randint(0,len(random_oponent)-1)
                # action = random_oponent[rand_action]
                # env.tabuleiro = env.aplicar_acao(action,"A")
                # state = env.state

            env.state['player_turn'] = 1 - env.state['player_turn']
            env.turno = env.oposto(env.turno)
#2,8 16,8
        with open(log_filename, 'a', newline='') as csvfile:
            log_writer = csv.writer(csvfile)
            log_writer.writerow([episode , env.get_winner(), total_reward])
        agent.decay_exploration_rate()
        return total_reward
    
    def jogar(self, env, agent):

        self.load_q_table('q_table3.pkl')
        env.imprimir_tabuleiro()
        state = env.reset()
        total_reward = 0

        

        while not env.check_if_done():
            
            if state['player_turn'] == 1:  # Turno do agente
                action = agent.choose_action_play(state, env)
                next_state, reward, done = env.step(action)
                env.turno = env.oposto(env.turno)
                env.imprimir_tabuleiro()

            # Opponent's turn (assuming the environment handles the opponent's move)
            else:
                posicao_da_vez = env.encontrar_posicao(env.turno)
                print("Jogador:", env.turn())
                jogada = input("Escolha: Mover(M), ou Parede(P): ")
                if(jogada == "M"):
                    movimento = input("Selecione o Movimento(B,C,E,D): ")
                    if movimento not in ["B","C","E","D"]:
                        print("Movimento inválidoM")
                    else:
                        sucesso, resultado = env.mover_peca(posicao_da_vez, movimento)
                        if sucesso:
                            env.imprimir_tabuleiro()
                            print("")
                        else:
                            print(resultado)

                elif(jogada == "P"):

                    x = int(input("Digite a Linha: "))
                    y = int(input("Digite a Coluna: "))
                    orientacao = input("Digite a Orientação(H,V): ")
                    if env.verifica_parede(x, y, orientacao, env.tabuleiro, env.turno):
                        env.adicionar_barreira( x, y, orientacao)
                    else:
                        print("Posição inválida para a parede.")

                    #tabuleiro_quoridor = env.adicionar_barreira(x, y, orientacao)  # Exemplo de adição de barreira horizontal
                    env.imprimir_tabuleiro()
                else:
                    print("Selecione uma jogada valida: ")

                #opponent_action = env.heuristic_opponent(state)
                state = env.state

                # random_oponent = env.acoes_possiveis()
                # rand_action = random.randint(0,len(random_oponent)-1)
                # action = random_oponent[rand_action]
                # env.tabuleiro = env.aplicar_acao(action,"A")
                # state = env.state

            env.state['player_turn'] = 1 - env.state['player_turn']
        

    def choose_action_play(self, state, env):
        state_index = self.state_to_index(state)
        possible_actions = env.acoes_possiveis()
        possible_actions = self.expand_actions(possible_actions)
        self.ALL_ACTIONS = possible_actions
        self.ACTION_INDEX_MAP = {action: index for index, action in enumerate(self.ALL_ACTIONS)}


        
        if state_index not in self.q_table:
            self.q_table[state_index] = np.zeros(self.action_space_size)
            action_index = random.randint(0, self.action_space_size - 1)  # Explore
        else:
            action_index = np.argmax(self.q_table[state_index])  # Exploit
        
        selected_action = self.index_to_action(action_index)
        while selected_action is None:
            action_index = random.randint(0, self.action_space_size - 1)
            selected_action = self.index_to_action(action_index)
        
        return selected_action

#Exemplo de uso:

