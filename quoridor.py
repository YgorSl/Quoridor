import numpy as np
from collections import deque
import copy
import minmax
import random


class Quoridor:

    def __init__(self):        

        self.tabuleiro = self.criar_tabuleiro()
        self.turno = "P"
        self.paredes_p=10
        self.paredes_a=10
        self.acoes = self.acoes_possiveis()
        self.state = self.reset()
        self.max_acoes = 12

    def reset(self):
        self.tabuleiro = self.criar_tabuleiro()
        self.state = self.initial_state()
        self.paredes_p=10
        self.paredes_a=10
        self.done = False
        self.turno = "P"
        return self.state

    def initial_state(self):
        return {
            #1 = P, 0=A
            'player_turn':1,
            'player_positions': [(0, 8), (16, 8)],
            'barriers': [],
            'remaining_barriers': [10, 10]
        }

    def existe_caminho(self, tabuleiro, jogador):
        # Define o objetivo final para cada jogador
        objetivo = 0 if jogador == "P" else 16

        # Encontra a posição inicial do jogador
        posicao_inicial = self.encontrar_posicao(jogador)

        # Cria uma fila para armazenar os caminhos a serem explorados
        fila = deque([posicao_inicial])

        # Cria um conjunto para armazenar as posições já visitadas
        visitados = set()
        visitados.add(posicao_inicial)

        # Realiza uma busca em largura (BFS) para encontrar um caminho até o objetivo
        while fila:
            posicao_atual = fila.popleft()
            linha_atual, coluna_atual = posicao_atual

            # Se o jogador alcançou o objetivo, retorna True
            if linha_atual == objetivo:
                return True

            # Explora as posições adjacentes
            for delta_linha, delta_coluna in [(-2, 0), (2, 0), (0, -2), (0, 2)]:
                nova_linha = linha_atual + delta_linha
                nova_coluna = coluna_atual + delta_coluna

                # Verifica se a nova posição é válida e não foi visitada
                if 0 <= nova_linha < 17 and 0 <= nova_coluna < 17 and (nova_linha, nova_coluna) not in visitados:
                    # Verifica se não há barreira no caminho
                    meio_linha = linha_atual + delta_linha // 2
                    meio_coluna = coluna_atual + delta_coluna // 2
                    if tabuleiro[meio_linha][meio_coluna] not in ['-', '|']:
                        visitados.add((nova_linha, nova_coluna))
                        fila.append((nova_linha, nova_coluna))

        # Se o loop terminar sem encontrar o objetivo, retorna False
        return False
    
    def calculate_distance_to_goal(self, state, player_turn):
        tabuleiro = self.tabuleiro

        if player_turn == 1:
            player_position = self.encontrar_posicao("P")
        else:
            player_position = self.encontrar_posicao("A")
        # player_position = state['player_positions'][player_turn]

        objetivo = 0 if player_turn == 1 else 16

        queue = deque([(player_position, 0)])  # (position, distance)
        visited = set()
        visited.add(player_position)

        while queue:
            (current_position, current_distance) = queue.popleft()
            
            x, y = current_position
            
            if x == objetivo:
                return current_distance

            # Check all possible moves

            for delta_linha, delta_coluna in [(-2, 0), (2, 0), (0, -2), (0, 2)]:
                nova_linha = x + delta_linha
                nova_coluna = y + delta_coluna
                # Verifica se a nova posição é válida e não foi visitada
                if 0 <= nova_linha < 17 and 0 <= nova_coluna < 17 and (nova_linha, nova_coluna) not in visited:
                    # Verifica se não há barreira no caminho
                    if tabuleiro[x + delta_linha // 2][y + delta_coluna // 2] not in ['-', '|']:
                        visited.add((nova_linha,nova_coluna))
                        queue.append(((nova_linha, nova_coluna), current_distance + 1))

            

            # available_moves = self.mov_possiveis()

            # for move in available_moves:
            #     if move not in visited:
            #         visited.add((move[2][1], move[2][2]))
            #         queue.append(((move[2][1], move[2][2]), current_distance + 1))

        return float('inf') 
    
    def reduzir_parede(self):

        if self.turno == "P":
            self.paredes_p -=1
        elif self.turno =="A":
            self.paredes_a -=1

    def qtd_paredes(self, turno):

        if turno == "P":
            return self.paredes_p
        elif turno =="A":
            return self.paredes_a

    def oposto(self, turno):

        if turno == "P":
            return "A"
        else:
            return "P"
        
    def acoes_possiveis(self):
        acoes = []

        # Encontre a posição atual do jogador
        posicao_atual = self.encontrar_posicao(self.turno)

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
                
                if self.tabuleiro[posicao_intermediaria[0]][posicao_intermediaria[1]] not in ('-', '|'):
                    prox = copy.deepcopy(self)
                    acoes.append((prox, "M", (direcao, nova_linha, nova_coluna)))  # Ação de mover

        # Verifique as posições para adicionar barreiras
        posicao_jogador = self.encontrar_posicao(self.turno)  # Peça do jogador
        posicao_oponente = self.encontrar_posicao(self.oposto(self.turno))
        # Pontuação: quanto menor a distância da IA até o objetivo, melhor


        #So começa a tentar colocar barreira se for menor = 5 a distancia do oponente
        #if distancia_jogador_ate_objetivo <= 10:
        for linha in range(posicao_oponente[0] - 1,  posicao_oponente[0] + 2):
            for coluna in range( posicao_oponente[1] - 1, posicao_oponente[1] + 2):
                if linha >= 17 or coluna >= 17:
                    continue
                if self.tabuleiro[linha][coluna] == ' ':
                    # Verifique se é possível adicionar uma barreira horizontal
                    if self.verifica_parede(linha, coluna, 'H', self.tabuleiro, self.turno):
                        prox = copy.deepcopy(self)
                        acoes.append((prox, "P", (linha, coluna, 'H')))  # Ação de adicionar barreira horizontal
                    # Verifique se é possível adicionar uma barreira vertical
                    if self.verifica_parede(linha, coluna, 'V', self.tabuleiro, self.turno):
                        prox = copy.deepcopy(self)
                        acoes.append((prox, "P", (linha, coluna, 'V')))  # Ação de adicionar barreira vertical

        return acoes
    
    def step(self, action):
        next_state, reward, done = self.transition(action)
        self.state = next_state
        self.done = done
        return next_state, reward, done
    
    def check_if_done(self):
        return self.game_end()

    def is_done(self):
        return self.done
    
    def heuristic_opponent(self, state):
        acoes = self.acoes_possiveis()
        state_copy = copy.deepcopy(self)

        # Escolher o movimento que minimiza a distância até o objetivo
        best_move = None
        min_distance = float('inf')
        max_distance = 0
        best_parede = None
        for acao in acoes:
            jogo, tipo_acao, parametros = acao
            if tipo_acao == "M":
                state_copy.tabuleiro = state_copy.aplicar_acao(acao,"A")
                distance = state_copy.calculate_distance_to_goal(state_copy.state, 0)
                if distance < min_distance:
                    min_distance = distance
                    best_move = acao
                state_copy = copy.deepcopy(self)
            elif tipo_acao == "P":
                state_copy.tabuleiro = state_copy.aplicar_acao(acao,"A")
                distance_enemy = state_copy.calculate_distance_to_goal(state_copy.state, 1)
                if distance_enemy > max_distance:
                    max_distance = distance_enemy
                    best_parede = acao
                state_copy = copy.deepcopy(self)

        acao_escolhida = random.randint(0,1)
        if acao_escolhida == 0:
            best_move = best_move
        elif acao_escolhida == 1 and best_parede != None:
            best_move = best_parede

        
        return best_move

    def transition(self, action):
        env_before = copy.deepcopy(self)
        state_before = copy.deepcopy(self.state)
        self.tabuleiro = self.aplicar_acao(action,"P")
        #self.state['player_turn'] = 1 - self.state['player_turn']

        next_state = self.state
        reward = self.calculate_reward(state_before, next_state, env_before)
        done = self.check_if_done()
        return next_state, reward, done
    
    def calculate_reward(self, state, next_state, env_before, player_turn = 1):
        reward = 0

        # Calcular a distância ao objetivo para o jogador atual
        current_distance = env_before.calculate_distance_to_goal(state, player_turn)
        next_distance = self.calculate_distance_to_goal(next_state, player_turn)

        # Recompensa para o jogador diminuir a distância ao objetivo
        if next_distance < current_distance:
            reward += (current_distance - next_distance) * 10  # Valor positivo se a distância diminuiu
        else:
            reward -= (next_distance - current_distance) * 5  # Valor negativo se a distância aumentou

        # Calcular a distância ao objetivo para o adversário
        opponent_turn = 1 - player_turn
        current_opponent_distance = env_before.calculate_distance_to_goal(state, opponent_turn)
        next_opponent_distance = self.calculate_distance_to_goal(next_state, opponent_turn)

        # Recompensa para aumentar a distância do adversário ao objetivo
        if next_opponent_distance > current_opponent_distance:
            reward += (next_opponent_distance - current_opponent_distance) * 10  # Valor positivo se a distância aumentou

        # Penalizar o uso de barreiras sem efeito
        if state['remaining_barriers'][player_turn] > next_state['remaining_barriers'][player_turn]:
            if next_opponent_distance <= current_opponent_distance:
                reward -= 10  # Penalizar se a barreira não aumentou a distância do adversário

        # Recompensa adicional por ganhar o jogo
        if self.is_goal_reached(next_state, 1):
            reward += 1000  # Grande recompensa por alcançar o objetivo
        if self.is_goal_reached(next_state, 0):
            reward -= 1000  # Grande penalidade por permitir que o adversário alcance o objetivo

        return reward
    
    def is_goal_reached(self, state, player_turn):
        player_position = state['player_positions'][player_turn]
        goal_row = 16 if player_turn == 0 else 0
        return player_position[1] == goal_row
            
    def criar_tabuleiro(self):
        # Cria um tabuleiro 9x9 com espaços vazios ('.') e espaços para barreiras (' ')
        self.tabuleiro = [['.' if (linha % 2 == 0 and coluna % 2 == 0) else ' ' for coluna in range(17)] for linha in range(17)]
        
        # Adiciona as peças dos jogadores no tabuleiro
        self.tabuleiro[0][8] = 'A'  # Posição inicial do jogador 1
        self.tabuleiro[16][8] = 'P'  # Posição inicial do jogador 2
        
        return self.tabuleiro

    def adicionar_barreira(self, linha, coluna, orientacao):
        # Adiciona uma barreira no tabuleiro na posição e orientação especificadas
        # 'H' para horizontal e 'V' para vertical

        #ptabuleiro_antigo = tabuleiro


        if orientacao == 'H':
            for offset in range(-1, 2):
                self.tabuleiro[linha][coluna + offset] = '-'
        elif orientacao == 'V':
            for offset in range(-1, 2):
                self.tabuleiro[linha + offset][coluna] = '|'

        # if self.existe_caminho(tabuleiro, posicao_p1, chegada_p1):
        #     print("Ainda existe um caminho após adicionar a barreira.")
            
        # else:
        #     print("A barreira bloqueia todos os caminhos. Movimento inválido.")
        #     return tabuleiro_antigo

        # if self.existe_caminho(tabuleiro, posicao_p2, chegada_p2):
        #     print("Ainda existe um caminho após adicionar a barreira.")
        # else:
        #     print("A barreira bloqueia todos os caminhos. Movimento inválido.")
        #     return tabuleiro_antigo
        self.reduzir_parede()
        self.turno = self.oposto(self.turno)
        return self.tabuleiro
    
    # def reward(self):
    #     if self.turno == "A":
    #         #tabuleiro pontos para A
    #     elif self.turno  == "P":
    #         #TABULERIRO PONTOS PARA P
        
    def game_end(self):
        pos_p1 = self.encontrar_posicao("P")
        pos_p2 = self.encontrar_posicao("A")
        if pos_p1[0] == 0:
            return True

        elif pos_p2[0] == 16:
            return True
        
        else: return False


    def is_end(self):
        pos_p1 = self.encontrar_posicao("P")
        pos_p2 = self.encontrar_posicao("A")
        if self.turno == "A":
            return pos_p1[0] == 0
    
        else:
            return pos_p2[0] == 16
        
    def get_winner(self):
        if self.encontrar_posicao("A")[0] == 16:
            return "A"
        else:
            return "P"

    def imprimir_tabuleiro(self):
    # Imprime os números das colunas
        print("    ", end="")
        for coluna in range(1, 18, 2):  # Começa em 1 e incrementa de 2 em 2
            print(f"{coluna // 1:2}", end="  ")
        print()

        # Imprime o tabuleiro com números de linha e conteúdo
        for linha, linha_tabuleiro in enumerate(self.tabuleiro):
            # Ajusta o número da linha para começar em 1
            print(f"{linha if linha % 2 != 0 else ' ':2}", end=" ")
            for celula in linha_tabuleiro:
                print(celula, end=" ")
            print()
        print()

    def mover_peca(self, posicao_atual, movimento):
        # Mapeia os movimentos para as mudanças correspondentes no índice do tabuleiro
        direcoes = {'C': (-2, 0), 'B': (2, 0), 'E': (0, -2), 'D': (0, 2)}
        delta = direcoes[movimento]
        
        # Calcula a posição intermediária (onde uma barreira pode estar)
        posicao_intermediaria = (posicao_atual[0] + delta[0]//2, posicao_atual[1] + delta[1]//2)
        
        # Verifica se a nova posição é válida
        nova_posicao = (posicao_atual[0] + delta[0], posicao_atual[1] + delta[1])
        if not (0 <= nova_posicao[0] < 17 and 0 <= nova_posicao[1] < 17):
            return False, "Movimento inválido: fora do tabuleiro."
        
         # Verifica se ha um jogador na posi;'ao escolhida
        
         # Verifica se a próxima posição está ocupada por outro jogador
        if self.tabuleiro[nova_posicao[0]][nova_posicao[1]] in ('P', 'A'):
            # Pula para a próxima posição válida
            nova_posicao = (nova_posicao[0] + delta[0], nova_posicao[1] + delta[1])
            if not (0 <= nova_posicao[0] < 17 and 0 <= nova_posicao[1] < 17):
                return False, "Movimento inválido: fora do tabuleiro."
        # Verifica se há uma barreira no caminho
        if self.tabuleiro[posicao_intermediaria[0]][posicao_intermediaria[1]] in ('-', '|'):
            return False, "Movimento inválido: há uma barreira no caminho."

        # Move a peça
        self.tabuleiro[posicao_atual[0]][posicao_atual[1]] = '.'
        self.tabuleiro[nova_posicao[0]][nova_posicao[1]] = self.turno  # 'P' ou 'A'
        
        self.turno = self.oposto(self.turno)
        return True, nova_posicao
    
    def verifica_parede(self, linha, coluna, orientacao, tabuleiro, turno):
        # Verifica se a posição está dentro dos limites do tabuleiro para paredes
        if orientacao not in ['H', 'V']:
            return False

        if self.qtd_paredes(turno) == 0:
            #print("Paredes Esotadas")
            return False

        if orientacao == 'H' and (linha <= 0 or linha > 14 or coluna < 1 or coluna > 14):
            return False
        if orientacao == 'V' and (linha < 1 or linha > 14 or coluna <= 0 or coluna > 14):
            return False

        # Verifica se a posição já está ocupada por outra parede ou casa
        if tabuleiro[linha][coluna] != ' ' or tabuleiro[linha][coluna] == '.':
            return False

        # Verifica se a parede não cruza ou toca outra parede na mesma orientação
        if orientacao == 'H':
            if tabuleiro[linha][coluna-1] == '-' or tabuleiro[linha][coluna+1] == '-':
                return False
        if orientacao == 'V':
            if tabuleiro[linha-1][coluna] == '|' or tabuleiro[linha+1][coluna] == '|':
                return False

        # Verifica se a parede não cobre as casas adjacentes
        if orientacao == 'H':
            if tabuleiro[linha-1][coluna] in ['.', "P","A"] or tabuleiro[linha+1][coluna] in['.',"P","A"]:
                return False
            if tabuleiro[linha][coluna-1] in ['.', "P","A"] or tabuleiro[linha][coluna+1] in['.',"P","A"]:
                return False
        if orientacao == 'V':
            if tabuleiro[linha][coluna-1] in ['.', "P","A"] or tabuleiro[linha][coluna+1] in ['.', "P","A"]:
                return False
            if tabuleiro[linha+1][coluna] in ['.', "P","A"] or tabuleiro[linha-1][coluna] in ['.', "P","A"]:
                return False
            
        tabuleiro_simulado = [linha[:] for linha in tabuleiro]
        if orientacao == 'H':
            for offset in range(-1, 2):
                tabuleiro_simulado[linha][coluna + offset] = '-'
        elif orientacao == 'V':
            for offset in range(-1, 2):
                tabuleiro_simulado[linha + offset][coluna] = '|'

        # Verifica se ainda há caminho para o jogador P1
        if not self.existe_caminho(tabuleiro_simulado, "P"):
            return False
        # Verifica se ainda há caminho para o jogador P2
        if not self.existe_caminho(tabuleiro_simulado, "A"):
            return False


        # Se passar por todas as verificações, a posição é válida
        return True
    
    def is_wall_blocking(self):
        from astar import astar
        #self.turno = self.oposto(self.turno)
        return not astar(self, True)

    def encontrar_posicao(self, jogador):
        # Converte o tabuleiro para um array NumPy
        tabuleiro_np = np.array(self.tabuleiro)
        
        # Usa np.where para encontrar a posição do jogador
        posicao = np.where(tabuleiro_np == jogador)

        # np.where retorna uma tupla com arrays, pegamos o primeiro elemento de cada array
        return (posicao[0][0], posicao[1][0])
    
    def turn(self):
        return self.turno
    
    def avalia_mov(self):
        available_moves = self.mov_possiveis()
        children = []
        for move in available_moves:
            child = copy.copy(self)
            #fazer o objeto alterar si mesmo
            child.tabuleiro = child.aplicar_acao(move, child.turno)
            cost = 1000
            if child.turno == "P":
                pos = child.encontrar_posicao("P")
            else:
                pos = child.encontrar_posicao("A")
            simplified_child_state = ((pos[0], pos[1]), (move[2][1], move[2][2]), cost)

            children.append((child, simplified_child_state))
        return children

    def mov_possiveis(self):
        acoes = []

        # Encontre a posição atual do jogador########################################
        posicao_atual = self.encontrar_posicao(self.turno)

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
                if self.tabuleiro[posicao_intermediaria[0]][posicao_intermediaria[1]] not in ('-', '|'):
                    prox = copy.copy(self)
                    acoes.append((prox, "M", (direcao, nova_linha, nova_coluna)))  # Ação de mover
        return acoes   

    def aplicar_acao(self, acao, turno):
        jogo, tipo_acao, parametros = acao

        turn = self.state['player_turn']
        
        if tipo_acao == "M":
            # Ação de mover

            posicao_atual = self.encontrar_posicao(turno)
            direcao, nova_linha, nova_coluna = parametros

            novo_estado = [linha[:] for linha in jogo.tabuleiro]  # Crie uma cópia do estado atual

            direcoes = {'C': (-2, 0), 'B': (2, 0), 'E': (0, -2), 'D': (0, 2)}
            delta = direcoes[direcao]
            nova_posicao = (posicao_atual[0] + delta[0], posicao_atual[1] + delta[1])

            # Pula para a próxima posição válida
            if novo_estado[nova_posicao[0]][nova_posicao[1]] in ('P', 'A'):
                
                nova_posicao = (nova_posicao[0] + delta[0], nova_posicao[1] + delta[1])
                if nova_posicao[0] > 17 or nova_posicao[1] > 17:
                    return jogo.tabuleiro
                novo_estado[posicao_atual[0]][posicao_atual[1]] = '.'
                novo_estado[nova_posicao[0]][nova_posicao[1]] = turno  # 'P' ou 'A'
                self.state['player_positions'][turn] = nova_posicao

            else:
                novo_estado[posicao_atual[0]][posicao_atual[1]] = '.'  # Limpe a posição atual
                novo_estado[nova_linha][nova_coluna] = turno  # Atualize a nova posição 
                self.state['player_positions'][turn] = nova_posicao

            tabuleiro_np = np.array(jogo.tabuleiro)
        
            # Usa np.where para encontrar a posição do 'P'
            posicao = np.where(tabuleiro_np == 'P')
            if posicao is None:
                print('')
            return novo_estado
        
        elif tipo_acao == "P":
            # Ação de adicionar barreira
            linha, coluna, orientacao = parametros
            if self.verifica_parede(linha, coluna, orientacao, jogo.tabuleiro, turno):
                novo_estado = [linha[:] for linha in jogo.tabuleiro]  # Crie uma cópia do estado atual
                if orientacao == 'H':
                    for offset in range(-1, 2):
                        novo_estado[linha][coluna + offset] = '-'
                        self.state['barriers'].append({'x': linha, 'y': coluna, 'orientation': orientacao})
                    self.state['remaining_barriers'][turn] -= 1
                    self.reduzir_parede()

                elif orientacao == 'V':
                    for offset in range(-1, 2):
                        novo_estado[linha + offset][coluna] = '|'
                        self.state['barriers'].append({'x': linha, 'y': coluna, 'orientation': orientacao})
                    self.state['remaining_barriers'][turn] -= 1
                    self.reduzir_parede()
                return novo_estado
            else:
                # A posição não é válida para adicionar uma barreira
                return jogo.tabuleiro
        else:
            # Ação desconhecida (trate conforme necessário)
            return jogo.tabuleiro
        
    def caminho_livre(self, posicao1, posicao2, tabuleiro):
        linha1, coluna1 = posicao1
        linha2, coluna2 = posicao2

        # Verifique se não há paredes no caminho direto
        for linha in range(min(linha1, linha2) + 1, max(linha1, linha2)):
            if tabuleiro[linha][coluna1] == '|' or tabuleiro[linha][coluna2] == '|':
                return False
        return True
    def jogarMinimax(self):
        while(True):

            if self.turno == "A":
                self.turno_mm = self.turno
                jogo_prox = copy.copy(self)
                proxima_jogada = minmax.melhor_jogada(jogo_prox)  # Chame a função da IA para obter a próxima jogada
                game, tipo_acao, parametros = proxima_jogada
                posicao_da_vez = self.encontrar_posicao(self.turno)

                if tipo_acao == "M":
                    sucesso, resultado = self.mover_peca(posicao_da_vez, parametros[0])  # Aplicação do movimento
                elif tipo_acao == "P":
                    x, y, orientacao = parametros
                    self.adicionar_barreira(x, y, orientacao)  # Aplicação da barreira


                self.imprimir_tabuleiro()  # Imprima o tabuleiro atualizado
                    # Alterne o turno para o jogador (P1)
                    #self.turno = "P"
            else:
                posicao_da_vez = self.encontrar_posicao(self.turno)
                print("Jogador:", self.turn())
                jogada = input("Escolha: Mover(M), ou Parede(P): ")
                if(jogada == "M"):
                    movimento = input("Selecione o Movimento(B,C,E,D): ")
                    if movimento not in ["B","C","E","D"]:
                        print("Movimento inválidoM")
                    else:
                        sucesso, resultado = self.mover_peca(posicao_da_vez, movimento)
                        if sucesso:
                            self.imprimir_tabuleiro()
                            print("")
                        else:
                            print(resultado)
                elif(jogada == "P"):

                    x = int(input("Digite a Linha: "))
                    y = int(input("Digite a Coluna: "))
                    orientacao = input("Digite a Orientação(H,V): ")
                    if self.verifica_parede(x, y, orientacao, self.tabuleiro, self.turno):
                        self.adicionar_barreira( x, y, orientacao)
                    else:
                        print("Posição inválida para a parede.")

                    #tabuleiro_quoridor = self.adicionar_barreira(x, y, orientacao)  # Exemplo de adição de barreira horizontal
                    self.imprimir_tabuleiro()
                else:
                    print("Selecione uma jogada valida: ")

            if self.is_end():
                break

            print("")

        print("Jogador", self.get_winner(), "venceu")
