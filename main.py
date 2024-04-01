import numpy as np
from collections import deque

class Quoridor:

    def __init__(self):        

        self.tabuleiro = self.criar_tabuleiro()
        self.turno = "P"
        self.paredes_p=10
        self.paredes_a=10
        self.turno_mm = None
        self.itercao =0

    def existe_caminho(self, tabuleiro, jogador):
        # Define o objetivo final para cada jogador
        objetivo = 16 if jogador == "P" else 0

        # Encontra a posição inicial do jogador
        posicao_inicial = self.encontrar_posicao(jogador, tabuleiro)

        # Cria uma fila para armazenar os caminhos a serem explorados
        fila = deque([posicao_inicial])

        # Cria um conjunto para armazenar as posições já visitadas
        visitados = set()

        # Realiza uma busca em largura (BFS) para encontrar um caminho até o objetivo
        while fila:
            posicao_atual = fila.popleft()
            linha_atual, coluna_atual = posicao_atual

            # Se o jogador alcançou o objetivo, retorna True
            if linha_atual == objetivo:
                return True

            # Adiciona a posição atual aos visitados
            visitados.add(posicao_atual)

            # Explora as posições adjacentes
            for delta_linha, delta_coluna in [(-2, 0), (2, 0), (0, -2), (0, 2)]:
                nova_linha = linha_atual + delta_linha
                nova_coluna = coluna_atual + delta_coluna

                # Verifica se a nova posição é válida e não foi visitada
                if 0 <= nova_linha < 17 and 0 <= nova_coluna < 17 and (nova_linha, nova_coluna) not in visitados:
                    # Verifica se não há barreira no caminho
                    if tabuleiro[linha_atual + delta_linha // 2][coluna_atual + delta_coluna // 2] not in ['-', '|']:
                        fila.append((nova_linha, nova_coluna))

        # Se não encontrar um caminho até o objetivo, retorna False
        return False
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

    def criar_tabuleiro(self):
        # Cria um tabuleiro 9x9 com espaços vazios ('.') e espaços para barreiras (' ')
        self.tabuleiro = [['.' if (linha % 2 == 0 and coluna % 2 == 0) else ' ' for coluna in range(17)] for linha in range(17)]
        
        # Adiciona as peças dos jogadores no tabuleiro
        self.tabuleiro[0][8] = 'P'  # Posição inicial do jogador 1
        self.tabuleiro[16][8] = 'A'  # Posição inicial do jogador 2
        
        return self.tabuleiro

    def adicionar_barreira(self, linha, coluna, orientacao):
        # Adiciona uma barreira no tabuleiro na posição e orientação especificadas
        # 'H' para horizontal e 'V' para vertical

        chegada_p1 = 8
        chegada_p2 = 0 

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


    def is_end(self):
        pos_p1 = self.encontrar_posicao("P", self.tabuleiro)
        if pos_p1[0] == 16:
            return True
    
        pos_p2 = self.encontrar_posicao("A", self.tabuleiro)
        if pos_p2[0] == 0:
            return True
        
        return False
        
    def get_winner(self):
        if self.player_one_pos[0] == 0:
            return "P"
        else:
            return "A"

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

    # def mover_peca(tabuleiro, posicao_atual, movimento, jogador):
    #     # Calcula a nova posição baseada no movimento
    #     direcoes = {'C': (-2, 0), 'B': (2, 0), 'E': (0, -2), 'D': (0, 2)}
    #     delta = direcoes[movimento]
    #     nova_posicao = (posicao_atual[0] + delta[0], posicao_atual[1] + delta[1])
        
    #     # Verifica se a nova posição é válida
    #     if not (0 <= nova_posicao[0] < 17 and 0 <= nova_posicao[1] < 17):
    #         return False, "Movimento inválido: fora do tabuleiro."
        
    #     # Verifica se há uma barreira no caminho
    #     posicao_barreira = (posicao_atual[0] + delta[0]//2, posicao_atual[1] + delta[1]//2)
    #     if tabuleiro[posicao_barreira[0]][posicao_barreira[1]] in ('-', '|'):
    #         return False, "Movimento inválido: há uma barreira no caminho."
        
    #     # Move a peça
    #     tabuleiro[posicao_atual[0]][posicao_atual[1]] = '.'
    #     tabuleiro[nova_posicao[0]][nova_posicao[1]] = jogador  # ou 'A', dependendo do jogador
        
    #     return True, nova_posicao

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
            print("Paredes Esotadas")
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

    def encontrar_posicao(self, jogador, tabuleiro):
        # Converte o tabuleiro para um array NumPy
        tabuleiro_np = np.array(tabuleiro)
        
        # Usa np.where para encontrar a posição do 'P'
        self.itercao = self.itercao
        posicao = np.where(tabuleiro_np == jogador)
        oi =  posicao[0][0]
        ola = posicao[1][0]
        # np.where retorna uma tupla com arrays, pegamos o primeiro elemento de cada array
        return (posicao[0][0], posicao[1][0])
    
    def jogada_humano():
        jogada = -1
        while jogada not in jogo.jogos_validos():
            jogada = int(input("Escolha um quadrado (0-8):"))
        return jogada
    
    def turn(self):
        return self.turno

    def acoes_possiveis(self, estado, turno):
        acoes = []

        self.itercao +=1
        if self.itercao == 233:
            print("oi")

        # Encontre a posição atual do jogador
        posicao_atual = self.encontrar_posicao(turno, estado)

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
                    acoes.append(("M", (direcao, nova_linha, nova_coluna)))  # Ação de mover

        # Verifique as posições para adicionar barreiras
        posicao_jogador = self.encontrar_posicao('P', estado)  # Peça do jogador
        distancia_jogador_ate_objetivo = 16 - posicao_jogador[0]

        # Pontuação: quanto menor a distância da IA até o objetivo, melhor

        #So começa a tentar colocar barreira se for menor = 5 a distancia do oponente
        if distancia_jogador_ate_objetivo <= 10:
             for linha in range(max(1, posicao_jogador[0] - 3), min(16, posicao_jogador[0] + 4)):
                for coluna in range(max(1, posicao_jogador[1] - 3), min(16, posicao_jogador[1] + 4)):
                    if estado[linha][coluna] == ' ':
                        # Verifique se é possível adicionar uma barreira horizontal
                        if self.verifica_parede(linha, coluna, 'H', estado, turno):
                            acoes.append(("P", (linha, coluna, 'H')))  # Ação de adicionar barreira horizontal
                        # Verifique se é possível adicionar uma barreira vertical
                        if self.verifica_parede(linha, coluna, 'V', estado, turno):
                            acoes.append(("P", (linha, coluna, 'V')))  # Ação de adicionar barreira vertical

        return acoes

    def aplicar_acao(self, estado, acao, turno):
        tipo_acao, parametros = acao
       
        if tipo_acao == "M":
            # Ação de mover

            posicao_atual = self.encontrar_posicao(turno, estado)
            direcao, nova_linha, nova_coluna = parametros

        

            novo_estado = [linha[:] for linha in estado]  # Crie uma cópia do estado atual

            direcoes = {'C': (-2, 0), 'B': (2, 0), 'E': (0, -2), 'D': (0, 2)}
            delta = direcoes[direcao]
            nova_posicao = (posicao_atual[0] + delta[0], posicao_atual[1] + delta[1])

            if novo_estado[nova_posicao[0]][nova_posicao[1]] in ('P', 'A'):
            # Pula para a próxima posição válida
                nova_posicao = (nova_posicao[0] + delta[0], nova_posicao[1] + delta[1])
                novo_estado[posicao_atual[0]][posicao_atual[1]] = '.'
                novo_estado[nova_posicao[0]][nova_posicao[1]] = turno  # 'P' ou 'A'
            else:
                novo_estado[posicao_atual[0]][posicao_atual[1]] = '.'  # Limpe a posição atual
                novo_estado[nova_linha][nova_coluna] = turno  # Atualize a nova posição

            tabuleiro_np = np.array(estado)
        
            # Usa np.where para encontrar a posição do 'P'
            posicao = np.where(tabuleiro_np == 'P')
            if posicao is None:
                print('')
            return novo_estado
        
        elif tipo_acao == "P":
            # Ação de adicionar barreira
            linha, coluna, orientacao = parametros
            if self.verifica_parede(linha, coluna, orientacao, estado, turno):
                novo_estado = [linha[:] for linha in estado]  # Crie uma cópia do estado atual
                if orientacao == 'H':
                    for offset in range(-1, 2):
                        novo_estado[linha][coluna + offset] = '-'
                elif orientacao == 'V':
                    for offset in range(-1, 2):
                        novo_estado[linha + offset][coluna] = '|'
                return novo_estado
            else:
                # A posição não é válida para adicionar uma barreira
                return estado
        else:
            # Ação desconhecida (trate conforme necessário)
            return estado
        
    # def avaliar_estado(self, tabuuleiro):

    #     minha_posicao = self.encontrar_posicao('A', tabuuleiro)  # Peça da IA
    #     objetivo_linha = 0  # Linha oposta (objetivo)
    #     distancia_ate_objetivo = objetivo_linha - minha_posicao[0]

    #     # Verifique a posição do jogador
    #     posicao_jogador = self.encontrar_posicao('P', tabuuleiro)  # Peça do jogador
    #     distancia_jogador_ate_objetivo = objetivo_linha - posicao_jogador[0]

    #     # Pontuação: quanto menor a distância da IA até o objetivo, melhor
    #     pontuacao = 10 - distancia_ate_objetivo

    #     # Bloqueie o jogador se ele estiver próximo do objetivo
    #     if distancia_jogador_ate_objetivo <= 5:
    #         pontuacao += 5

    #     # Penalize se houver paredes no caminho direto da IA
    #     if not self.caminho_livre(minha_posicao, posicao_jogador, tabuuleiro):
    #         pontuacao -= 3

    #     return pontuacao
    
    def avaliar_estado(self, estado, turno):

        if turno == "P":
            return 10 * abs(self.encontrar_posicao("P", estado)[0])
        else:
            return 10 * (abs(self.encontrar_posicao("A", estado)[0] - 16))


        # # Define o objetivo final para cada jogador
        # objetivo = 16 if self.turno_mm == "P" else 0

        # # Encontra a posição inicial do jogador
        # posicao_inicial = self.encontrar_posicao(self.turno_mm, estado)

        # # Calcula a distância até o objetivo
        # distancia_ate_objetivo = abs(objetivo - posicao_inicial[0])

        # # Inicializa a pontuação
        # pontuacao = 0

        # # Nas primeiras jogadas, priorize o movimento em direção ao objetivo
        # if distancia_ate_objetivo > 12:  # Considera que o jogo está no início
        #     pontuacao += (16 - distancia_ate_objetivo)

        # # Evite colocar barreiras inicialmente
        # if self.qtd_paredes(self.turno_mm)> 8:  # Se o self.turno_mm ainda tem muitas barreiras
        #     pontuacao -= 1  # Penaliza a colocação de barreiras

        # # Se o adversário estiver próximo do objetivo, considere bloquear seu caminho
        # posicao_adversario = self.encontrar_posicao("P", estado)
        # distancia_adversario_ate_objetivo = abs(objetivo - posicao_adversario[0])
        # if distancia_adversario_ate_objetivo <= 4:
        #     pontuacao += 5  # Incentiva a colocação de barreiras para bloquear o adversário

        # # Retorna a pontuação avaliada
        # return pontuacao

    def caminho_livre(self, posicao1, posicao2, tabuleiro):
        linha1, coluna1 = posicao1
        linha2, coluna2 = posicao2

        # Verifique se não há paredes no caminho direto
        for linha in range(min(linha1, linha2) + 1, max(linha1, linha2)):
            if tabuleiro[linha][coluna1] == '|' or tabuleiro[linha][coluna2] == '|':
                return False
        return True
        
    def minimax(self, estado,turno, profundidade, alfa, beta, maximizando):
        if profundidade == 0 or self.is_end():
            return self.avaliar_estado(estado, turno)

        if maximizando:
            melhor_valor = float("-inf")
            acaoo = self.acoes_possiveis(estado, turno)
            acaoo.__len__()
            for acao in self.acoes_possiveis(estado, turno):
                novo_estado = self.aplicar_acao(estado, acao, turno)
                turnomin = self.oposto(turno)
                valor = self.minimax(novo_estado,turnomin, profundidade - 1, alfa, beta, False)
                melhor_valor = max(melhor_valor, valor)
                alfa = max(melhor_valor, alfa)
                if beta <= alfa:
                    break  # Poda alfa-beta
            return melhor_valor
        else:
            melhor_valor = float("inf")
            for acao in self.acoes_possiveis(estado,turno):
                novo_estado = self.aplicar_acao(estado, acao, turno)
                turno_max = self.oposto(turno)
                valor = self.minimax(novo_estado,turno_max, profundidade - 1, alfa, beta, True)
                melhor_valor = min(melhor_valor, valor)
                beta = min(melhor_valor, beta)
                if beta <= alfa:
                    break  # Poda alfa-beta
            return melhor_valor

    def melhor_jogada(self, turno):
        melhor_pontuacao = float("-inf")
        melhor_acao = None
        turno = self.turno
        for acao in self.acoes_possiveis(self.tabuleiro, turno):
            novo_estado = self.aplicar_acao(self.tabuleiro, acao, turno)
        
            # Avalie o estado usando a heurística
            #pontuacao = self.avaliar_estado(novo_estado)
            
            # Chame o Minimax para avaliar os estados sucessores
            pontuacao = self.minimax(novo_estado,turno, profundidade=3, alfa=float("-inf"), beta=float("inf") ,maximizando=False)
            if pontuacao > melhor_pontuacao:
                melhor_pontuacao = pontuacao
                melhor_acao = acao
        return melhor_acao
    
jogo = Quoridor()
jogo.imprimir_tabuleiro()
vez_atual = "P"




while(True):

    if jogo.turno == "A":
        jogo.turno_mm = jogo.turno
        proxima_jogada = jogo.melhor_jogada(jogo.turno)  # Chame a função da IA para obter a próxima jogada
        tipo_acao, parametros = proxima_jogada
        posicao_da_vez = jogo.encontrar_posicao(jogo.turno, jogo.tabuleiro)

        if tipo_acao == "M":
            sucesso, resultado = jogo.mover_peca(posicao_da_vez, parametros[0])  # Aplicação do movimento
        elif tipo_acao == "P":
            x, y, orientacao = parametros
            jogo.adicionar_barreira(x, y, orientacao)  # Aplicação da barreira


        jogo.imprimir_tabuleiro()  # Imprima o tabuleiro atualizado
            # Alterne o turno para o jogador (P1)
            #jogo.turno = "P"
    else:
        posicao_da_vez = jogo.encontrar_posicao(jogo.turno, jogo.tabuleiro)
        print("Jogador:", jogo.turn())
        jogada = input("Escolha: Mover(M), ou Parede(P): ")
        if(jogada == "M"):
            movimento = input("Selecione o Movimento(B,C,E,D): ")
            if movimento not in ["B","C","E","D"]:
                print("Movimento inválidoM")
            else:
                sucesso, resultado = jogo.mover_peca(posicao_da_vez, movimento)
                if sucesso:
                    jogo.imprimir_tabuleiro()
                    print("")
                else:
                    print(resultado)
        elif(jogada == "P"):

            x = int(input("Digite a Linha: "))
            y = int(input("Digite a Coluna: "))
            orientacao = input("Digite a Orientação(H,V): ")
            if jogo.verifica_parede(x, y, orientacao, jogo.tabuleiro, jogo.turno):
                jogo.adicionar_barreira( x, y, orientacao)
            else:
                print("Posição inválida para a parede.")

            #tabuleiro_quoridor = jogo.adicionar_barreira(x, y, orientacao)  # Exemplo de adição de barreira horizontal
            jogo.imprimir_tabuleiro()
        else:
            print("Selecione uma jogada valida: ")

        if jogo.is_end():
            break

        print("")

print("Jogador", jogo.turno, "venceu")

