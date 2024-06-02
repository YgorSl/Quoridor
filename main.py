from quoridor import Quoridor
from qlearn import Qlearning
from Qlearning import QLearningAgent
    
jogo = Quoridor()
# jogo.imprimir_tabuleiro()
# vez_atual = "P"

#jogo.jogar()

def run_episode(env, agent):
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
                opponent_action = env.heuristic_opponent(state)  # Define esta função no seu ambiente
                env.tabuleiro = env.aplicar_acao(opponent_action,"A")
                state = env.state

            env.state['player_turn'] = 1 - env.state['player_turn']
            env.turno = env.oposto(env.turno)
#2,8 16,8
        agent.decay_exploration_rate()
        return total_reward

ambiente = Quoridor()
env = Quoridor()
agent = QLearningAgent()
for episode in range(1000):
    total_reward = run_episode(env, agent)
    print(f"Episode {episode} - Total Reward: {total_reward}")

agent.save_q_table('q_table.pkl')


# print(ambiente.imprimir_tabuleiro())

# q_learning = Qlearning(ambiente)

# print("Treinando ambiente...")

# Q, PI = q_learning.calcular_tabela_q()

# print("\nImprimindo Valores por estado:")
# print(ambiente.imprimir_q(Q))
# print("\nImprimindo Polítca ótima por estado:")
# print(ambiente.imprimir_politica(PI))


# while(True):

#     if jogo.turno == "A":
#         jogo.turno_mm = jogo.turno
#         jogo_prox = copy(jogo)
#         proxima_jogada = minmax.melhor_jogada(jogo_prox)  # Chame a função da IA para obter a próxima jogada
#         game, tipo_acao, parametros = proxima_jogada
#         posicao_da_vez = jogo.encontrar_posicao(jogo.turno)

#         if tipo_acao == "M":
#             sucesso, resultado = jogo.mover_peca(posicao_da_vez, parametros[0])  # Aplicação do movimento
#         elif tipo_acao == "P":
#             x, y, orientacao = parametros
#             jogo.adicionar_barreira(x, y, orientacao)  # Aplicação da barreira


#         jogo.imprimir_tabuleiro()  # Imprima o tabuleiro atualizado
#             # Alterne o turno para o jogador (P1)
#             #jogo.turno = "P"
#     else:
#         posicao_da_vez = jogo.encontrar_posicao(jogo.turno)
#         print("Jogador:", jogo.turn())
#         jogada = input("Escolha: Mover(M), ou Parede(P): ")
#         if(jogada == "M"):
#             movimento = input("Selecione o Movimento(B,C,E,D): ")
#             if movimento not in ["B","C","E","D"]:
#                 print("Movimento inválidoM")
#             else:
#                 sucesso, resultado = jogo.mover_peca(posicao_da_vez, movimento)
#                 if sucesso:
#                     jogo.imprimir_tabuleiro()
#                     print("")
#                 else:
#                     print(resultado)
#         elif(jogada == "P"):

#             x = int(input("Digite a Linha: "))
#             y = int(input("Digite a Coluna: "))
#             orientacao = input("Digite a Orientação(H,V): ")
#             if jogo.verifica_parede(x, y, orientacao, jogo.tabuleiro, jogo.turno):
#                 jogo.adicionar_barreira( x, y, orientacao)
#             else:
#                 print("Posição inválida para a parede.")

#             #tabuleiro_quoridor = jogo.adicionar_barreira(x, y, orientacao)  # Exemplo de adição de barreira horizontal
#             jogo.imprimir_tabuleiro()
#         else:
#             print("Selecione uma jogada valida: ")

#     if jogo.is_end():
#         break

#     print("")

# print("Jogador", jogo.get_winner(jogo.tabuleiro), "venceu")

