from quoridor import Quoridor
from Qlearning import QLearningAgent
import random
import csv
    
jogo = Quoridor()
#jogo.jogarMinimax()

agent = QLearningAgent()




print("Bem Vindo Ao Quoridor")
print("Regras: Voce Pode escolher entre colocar barreiras(P), ou se mover(M)")
print("Regras: Voce Só Pode se mover em quatro direções Cima(C), Baixo(B), Esquerda(E), Direita(D)")
print("Você tambem pode colocar barreiras para atrapalhar o inimigo, Basta Escolher o movimento P, e as cordenadas da parede")
agente = input("Por Favor Escolha contra qual agente Deseja Joga, Minimax(M), ou Qlearning(Q)")

if agente == "M":
    print("Voce sera o jogador P")
    jogo.imprimir_tabuleiro()
    jogo.jogarMinimax()
elif agente == "Q":

    print("Voce Sera o jogador A")
    agent.jogar(jogo, agent)
else:
    print("Por Favor Selecione um Agente Valido")
    

#jogo.jogar()

# def run_episode(env, agent, log_filename, episode):
        
#         state = env.reset()
#         total_reward = 0

        

#         while not env.check_if_done():
#             if state['player_turn'] == 1:  # Turno do agente
#                 action = agent.choose_action(state, env)
#                 next_state, reward, done = env.step(action)
#                 agent.update_q_table(state, action, reward, next_state, env)
#                 state = next_state
#                 total_reward += reward

#             # Opponent's turn (assuming the environment handles the opponent's move)
#             else:
#                 opponent_action = env.heuristic_opponent(state)
#                 env.tabuleiro = env.aplicar_acao(opponent_action,"A")
#                 state = env.state

#                 # random_oponent = env.acoes_possiveis()
#                 # rand_action = random.randint(0,len(random_oponent)-1)
#                 # action = random_oponent[rand_action]
#                 # env.tabuleiro = env.aplicar_acao(action,"A")
#                 # state = env.state

#             env.state['player_turn'] = 1 - env.state['player_turn']
#             env.turno = env.oposto(env.turno)
# #2,8 16,8
#         with open(log_filename, 'a', newline='') as csvfile:
#             log_writer = csv.writer(csvfile)
#             log_writer.writerow([episode , env.get_winner(), total_reward])
#         agent.decay_exploration_rate()
#         return total_reward

# ambiente = Quoridor()
# agent = QLearningAgent() 
# log_filename = 'training_heuristic_oponent.csv'
# log_writer = None

# agent.treinar(5000, log_filename, ambiente, agent)



# with open(log_filename, 'a', newline='') as csvfile:
#     log_writer = csv.writer(csvfile)
#     log_writer.writerow(['Episode', 'Winner', 'Reward'])

# for episode in range(10000):
#     try: 
        
#         total_reward = run_episode(env, agent, log_filename,episode)
#         print(f"Episode {episode} - Total Reward: {total_reward}")
#         if episode %100 == 0:
#              agent.save_q_table('q_table3.pkl')
#     except Exception as e:
#         print(f"Ocorreu um erro: {e}")
#         agent.save_q_table('q_table3.pkl')
#         print("Q-Table salva após erro.")
#         continue
#     else:

#         agent.save_q_table('q_table3.pkl')
# agent.save_q_table('q_table3.pkl')


# print(ambiente.imprimir_tabuleiro())

# q_learning = Qlearning(ambiente)



