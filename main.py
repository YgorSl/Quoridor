import numpy as np
from collections import deque

class Quoridor:

    def __init__(self):        

        self.tabuleiro = self.criar_tabuleiro()
        self.turno = "P1"

    def existe_caminho(tabuleiro, posicao_inicial, linha_final):
        # Converte o tabuleiro para um formato que facilite a verificação de barreiras
        tabuleiro_convertido = [[' ' for _ in range(9)] for _ in range(9)]
        for i in range(17):
            for j in range(17):
                if tabuleiro[i][j] == '.':
                    tabuleiro_convertido[i//2][j//2] = '.'

        # Inicializa a fila para BFS e adiciona a posição inicial
        fila = deque([posicao_inicial])
        visitados = set(posicao_inicial)

        # Executa a busca em largura
        while fila:
            posicao_atual = fila.popleft()
            linha, coluna = posicao_atual

            # Verifica se alcançou a linha final
            if linha == linha_final:
                return True

            # Verifica movimentos possíveis (Cima, Baixo, Esquerda, Direita)
            for delta_linha, delta_coluna in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nova_linha = linha + delta_linha
                nova_coluna = coluna + delta_coluna

                # Verifica se a nova posição é válida e não foi visitada
                if 0 <= nova_linha < 9 and 0 <= nova_coluna < 9 and (nova_linha, nova_coluna) not in visitados:
                    # Verifica se não há barreira no caminho
                    if tabuleiro[linha * 2 + delta_linha][coluna * 2 + delta_coluna] == ' ':
                        fila.append((nova_linha, nova_coluna))
                        visitados.add((nova_linha, nova_coluna))

        # Se a fila esvaziar e a linha final não for alcançada, não há caminho
        return False
    def oposto(self):

        if self.turno == "P1":
            return "P2"
        else:
            return "P1"

    def criar_tabuleiro(self):
        # Cria um tabuleiro 9x9 com espaços vazios ('.') e espaços para barreiras (' ')
        self.tabuleiro = [['.' if (linha % 2 == 0 and coluna % 2 == 0) else ' ' for coluna in range(17)] for linha in range(17)]
        
        # Adiciona as peças dos jogadores no tabuleiro
        self.tabuleiro[0][8] = 'P1'  # Posição inicial do jogador 1
        self.tabuleiro[16][8] = 'P2'  # Posição inicial do jogador 2
        
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
        self.turno = self.oposto()
        return self.tabuleiro


    def is_end(self):
        pos_p1 = self.encontrar_posicao("P1")
        if pos_p1[0] == 16:
            return True
    
        pos_p2 = self.encontrar_posicao("P2")
        if pos_p2[0] == 0:
            return True
        
        return False
        
    def get_winner(self):
        if self.player_one_pos[0] == 0:
            return "P1"
        else:
            return "P2"

    def imprimir_tabuleiro(self):
        # Imprime o tabuleiro
        for linha in self.tabuleiro:
            print(' '.join(linha))
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
    #     tabuleiro[nova_posicao[0]][nova_posicao[1]] = jogador  # ou 'P2', dependendo do jogador
        
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
        if self.tabuleiro[nova_posicao[0]][nova_posicao[1]] in ('P1', 'P2'):
            # Pula para a próxima posição válida
            nova_posicao = (nova_posicao[0] + delta[0], nova_posicao[1] + delta[1])
        
        # Verifica se há uma barreira no caminho
        if self.tabuleiro[posicao_intermediaria[0]][posicao_intermediaria[1]] in ('-', '|'):
            return False, "Movimento inválido: há uma barreira no caminho."
        
        # Move a peça
        self.tabuleiro[posicao_atual[0]][posicao_atual[1]] = '.'
        self.tabuleiro[nova_posicao[0]][nova_posicao[1]] = self.turno  # 'P1' ou 'P2'
        
        self.turno = self.oposto()
        return True, nova_posicao
    
    def verifica_parede(self, linha, coluna, orientacao):
        # Verifica se a posição está dentro dos limites do tabuleiro para paredes
        if orientacao == 'H' and (linha <= 0 or linha > 14 or coluna < 1 or coluna > 14):
            return False
        if orientacao == 'V' and (linha < 1 or linha > 14 or coluna <= 0 or coluna > 14):
            return False

        # Verifica se a posição já está ocupada por outra parede ou casa
        if self.tabuleiro[linha][coluna] != ' ' or self.tabuleiro[linha][coluna] == '.':
            return False

        # Verifica se a parede não cruza ou toca outra parede na mesma orientação
        if orientacao == 'H':
            if self.tabuleiro[linha][coluna-1] == '-' or self.tabuleiro[linha][coluna+1] == '-':
                return False
        if orientacao == 'V':
            if self.tabuleiro[linha-1][coluna] == '|' or self.tabuleiro[linha+1][coluna] == '|':
                return False

        # Verifica se a parede não cobre as casas adjacentes
        if orientacao == 'H':
            if self.tabuleiro[linha-1][coluna] in ['.', "P1","P2"] or self.tabuleiro[linha+1][coluna] in['.',"P1","P2"]:
                return False
            if self.tabuleiro[linha][coluna-1] in ['.', "P1","P2"] or self.tabuleiro[linha][coluna+1] in['.',"P1","P2"]:
                return False
        if orientacao == 'V':
            if self.tabuleiro[linha][coluna-1] in ['.', "P1","P2"] or self.tabuleiro[linha][coluna+1] in ['.', "P1","P2"]:
                return False
            if self.tabuleiro[linha+1][coluna] in ['.', "P1","P2"] or self.tabuleiro[linha-1][coluna] in ['.', "P1","P2"]:
                return False
            

        # Se passar por todas as verificações, a posição é válida
        return True




    def encontrar_posicao(self, jogador):
        # Converte o tabuleiro para um array NumPy
        tabuleiro_np = np.array(self.tabuleiro)
        
        # Usa np.where para encontrar a posição do 'P1'
        posicao = np.where(tabuleiro_np == jogador)
        
        # np.where retorna uma tupla com arrays, pegamos o primeiro elemento de cada array
        return (posicao[0][0], posicao[1][0])
    
    def jogada_humano():
        jogada = -1
        while jogada not in jogo.jogos_validos():
            jogada = int(input("Escolha um quadrado (0-8):"))
        return jogada
    
    def turn(self):
        return self.turno

    def acoes_possiveis(self, estado):
        acoes = []

        # Encontre a posição atual do jogador
        posicao_atual = self.encontrar_posicao(self.turno)

        direcoes = {'C': (-2, 0), 'B': (2, 0), 'E': (0, -2), 'D': (0, 2)}
        #delta = direcoes[movimento]

        # Verifique os movimentos possíveis (Cima, Baixo, Esquerda, Direita)
        #for delta_linha, delta_coluna in [(-2, 0), (2, 0), (0, -2), (0, 2)]:
        for direcao in direcoes:

            delta = direcoes[direcao]

            # nova_linha = posicao_atual[0] + delta_linha
            # nova_coluna = posicao_atual[1] + delta_coluna

            nova_linha, nova_coluna = (posicao_atual[0] + delta[0], posicao_atual[1] + delta[1])

            posicao_intermediaria = (posicao_atual[0] + delta[0]//2, posicao_atual[1] + delta[1]//2)

            nova_posicao = (posicao_atual[0] + delta[0], posicao_atual[1] + delta[1])

            # Verifique se a nova posição é válida
            #if 0 <= nova_linha < 17 and 0 <= nova_coluna < 17:
            if (0 <= nova_posicao[0] < 17 and 0 <= nova_posicao[1] < 17):
                # Verifique se não há barreira no caminho
                #if estado[nova_linha][nova_coluna] == ' ':
                if self.tabuleiro[posicao_intermediaria[0]][posicao_intermediaria[1]] not in ('-', '|'):
                    acoes.append(("M", (direcao, nova_linha, nova_coluna)))  # Ação de mover

        # Verifique as posições para adicionar barreiras
        for linha in range(17):
            for coluna in range(17):
                if estado[linha][coluna] == ' ':
                    # Verifique se é possível adicionar uma barreira horizontal
                    if self.verifica_parede(linha, coluna, 'H'):
                        acoes.append(("P", (linha, coluna, 'H')))  # Ação de adicionar barreira horizontal
                    # Verifique se é possível adicionar uma barreira vertical
                    if self.verifica_parede(linha, coluna, 'V'):
                        acoes.append(("P", (linha, coluna, 'V')))  # Ação de adicionar barreira vertical

        return acoes

    def aplicar_acao(self, estado, acao):
        tipo_acao, parametros = acao

        if tipo_acao == "M":
            # Ação de mover
            posicao_atual = self.encontrar_posicao(self.turno)
            direcao, nova_linha, nova_coluna = parametros
            novo_estado = [linha[:] for linha in estado]  # Crie uma cópia do estado atual
            novo_estado[posicao_atual[0]][posicao_atual[1]] = '.'  # Limpe a posição atual
            novo_estado[nova_linha][nova_coluna] = self.turno  # Atualize a nova posição
            return novo_estado
        
        elif tipo_acao == "P":
            # Ação de adicionar barreira
            linha, coluna, orientacao = parametros
            if self.verifica_parede(linha, coluna, orientacao):
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



    # def avaliar_estado(self, estado):
    #     # Exemplo de função de avaliação
    #     pos_p1 = self.encontrar_posicao("P1")
    #     pos_p2 = self.encontrar_posicao("P2")

    #     # Distância vertical até a vitória
    #     dist_p1 = 16 - pos_p1[0]
    #     dist_p2 = pos_p2[0]

    #     # Penalização por barreiras
    #     num_barreiras = sum(linha.count('-') + linha.count('|') for linha in estado)
    #     penalizacao_barreiras = -num_barreiras

    #     # Pontuação total (ajuste conforme necessário)
    #     pontuacao_p1 = dist_p1 + penalizacao_barreiras
    #     pontuacao_p2 = dist_p2 + penalizacao_barreiras

    #     # Retorne a pontuação para o jogador atual
    #     if self.turno == "P1":
    #         return pontuacao_p1
    #     else:
    #         return pontuacao_p2

    # def avaliar_estado(self):
    #     minha_posicao = self.encontrar_posicao("P2")  # Peça da IA
    #     objetivo_linha = 0  # Linha oposta (objetivo)
    #     distancia_ate_objetivo = objetivo_linha - minha_posicao[0]

    #     # Verifique se há paredes no caminho direto até o objetivo
    #     caminho_livre = True
    #     for linha in range(min(minha_posicao[0], objetivo_linha) + 1, max(minha_posicao[0], objetivo_linha)):
    #         if self.tabuleiro[linha][minha_posicao[1]] == '|':
    #             caminho_livre = False
    #             break

    #     # Pontuação: quanto menor a distância da IA até o objetivo, melhor
    #     pontuacao = 10 - distancia_ate_objetivo

    #     # Penalize se houver paredes no caminho direto
    #     if not caminho_livre:
    #         pontuacao -= 5

    #     return pontuacao
        
    def avaliar_estado(self):
        minha_posicao = self.encontrar_posicao("P2")  # Peça da IA
        objetivo_linha = 0  # Linha oposta (objetivo)
        distancia_ate_objetivo = objetivo_linha - minha_posicao[0]

        # Verifique a posição do jogador
        posicao_jogador = self.encontrar_posicao("P1")  # Peça do jogador
        distancia_jogador_ate_objetivo = objetivo_linha - posicao_jogador[0]

        # Pontuação: quanto menor a distância da IA até o objetivo, melhor
        pontuacao = 10 - distancia_ate_objetivo

        # Bloqueie o jogador se ele estiver próximo do objetivo
        if distancia_jogador_ate_objetivo <= 2:
            pontuacao += 5

        # Penalize se houver paredes no caminho direto da IA
        if not self.caminho_livre(minha_posicao, posicao_jogador):
            pontuacao -= 3

        return pontuacao

    def caminho_livre(self, posicao1, posicao2):
        linha1, coluna1 = posicao1
        linha2, coluna2 = posicao2

        # Verifique se não há paredes no caminho direto
        for linha in range(min(linha1, linha2) + 1, max(linha1, linha2)):
            if self.tabuleiro[linha][coluna1] == '|' or self.tabuleiro[linha][coluna2] == '|':
                return False
        return True


    # def minimax(self, estado, profundidade, maximizador):
    #     if profundidade == 0 or self.is_end():
    #         # Avalie o estado atual usando a função de avaliação
    #         return self.avaliar_estado(estado)

    #     if maximizador:
    #         melhor_pontuacao = float("-inf")
    #         for acao in self.acoes_possiveis(estado):
    #             novo_estado = self.aplicar_acao(estado, acao)
    #             pontuacao = self.minimax(novo_estado, profundidade - 1, False)
    #             melhor_pontuacao = max(melhor_pontuacao, pontuacao)
    #         return melhor_pontuacao
    #     else:
    #         melhor_pontuacao = float("inf")
    #         for acao in self.acoes_possiveis(estado):
    #             novo_estado = self.aplicar_acao(estado, acao)
    #             pontuacao = self.minimax(novo_estado, profundidade - 1, True)
    #             melhor_pontuacao = min(melhor_pontuacao, pontuacao)
    #         return melhor_pontuacao
        
    def minimax(self, estado, profundidade, alfa, beta, maximizando):
        if profundidade == 0 or self.is_end():
            return self.avaliar_estado()

        if maximizando:
            melhor_valor = float("-inf")
            for acao in self.acoes_possiveis(estado):
                novo_estado = self.aplicar_acao(estado, acao)
                valor = self.minimax(novo_estado, profundidade - 1, alfa, beta, False)
                melhor_valor = max(melhor_valor, valor)
                alfa = max(alfa, melhor_valor)
                if beta <= alfa:
                    break  # Poda alfa-beta
            return melhor_valor
        else:
            melhor_valor = float("inf")
            for acao in self.acoes_possiveis(estado):
                novo_estado = self.aplicar_acao(estado, acao)
                valor = self.minimax(novo_estado, profundidade - 1, alfa, beta, True)
                melhor_valor = min(melhor_valor, valor)
                beta = min(beta, melhor_valor)
                if beta <= alfa:
                    break  # Poda alfa-beta
            return melhor_valor

    def melhor_jogada(self):
        melhor_pontuacao = float("-inf")
        melhor_acao = None
        for acao in self.acoes_possiveis(self.tabuleiro):
            novo_estado = self.aplicar_acao(self.tabuleiro, acao)
        
            # Avalie o estado usando a heurística
            pontuacao = self.avaliar_estado()
            
            # Chame o Minimax para avaliar os estados sucessores
            pontuacao += self.minimax(novo_estado, profundidade=3, alfa=float("-inf"), beta=float("inf"), maximizando=False)
            if pontuacao > melhor_pontuacao:
                melhor_pontuacao = pontuacao
                melhor_acao = acao
        return melhor_acao


    # def melhor_jogada(self):
    #     melhor_pontuacao = float("-inf")
    #     melhor_acao = None
    #     for acao in self.acoes_possiveis(self.tabuleiro):
    #         novo_estado = self.aplicar_acao(self.tabuleiro, acao)
    #         pontuacao = self.minimax(novo_estado, profundidade=1, maximizador=False)
    #         if pontuacao > melhor_pontuacao:
    #             melhor_pontuacao = pontuacao
    #             melhor_acao = acao
    #     return melhor_acao
# Cria e imprime o tabuleiro
    
    
jogo = Quoridor()
#  tabuleiro_quoridor = jogo.criar_tabuleiro()
jogo.imprimir_tabuleiro()
vez_atual = "P1"

#posicao_atual_p1 = jogo.encontrar_posicao(tabuleiro_quoridor, "P1")  # Posição inicial do jogador 1(Ta chu)
#posicao_atual_p2 = jogo.encontrar_posicao(tabuleiro_quoridor, "P2")  # Posição inicial do jogador 1(Ta chu)


while(True):

    if jogo.turno == "P2":
        proxima_jogada = jogo.melhor_jogada()  # Chame a função da IA para obter a próxima jogada
        tipo_acao, parametros = proxima_jogada
        posicao_da_vez = jogo.encontrar_posicao(jogo.turno)

        if tipo_acao == "M":
            sucesso, resultado = jogo.mover_peca(posicao_da_vez, parametros[0])  # Aplicação do movimento
        elif tipo_acao == "P":
            x, y, orientacao = parametros
            jogo.adicionar_barreira(x, y, orientacao)  # Aplicação da barreira


        jogo.imprimir_tabuleiro()  # Imprima o tabuleiro atualizado
            # Alterne o turno para o jogador (P1)
            #jogo.turno = "P1"
    else:
        posicao_da_vez = jogo.encontrar_posicao(jogo.turno)
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
            if jogo.verifica_parede(x, y, orientacao):
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

def jogada_humano():


    if jogo.turno == "P2":
        proxima_jogada = melhor_jogada()  # Chame a função da IA para obter a próxima jogada
        tipo_acao, parametros = proxima_jogada

        if tipo_acao == "M":
            sucesso, resultado = jogo.mover_peca(parametros)  # Aplicação do movimento
        elif tipo_acao == "P":
            x, y, orientacao = parametros
            sucesso, resultado = jogo.adicionar_barreira(x, y, orientacao)  # Aplicação da barreira

        if sucesso:
            jogo.imprimir_tabuleiro()  # Imprima o tabuleiro atualizado
            # Alterne o turno para o jogador (P1)
            #jogo.turno = "P1"
    else:
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
            if jogo.verifica_parede(x, y, orientacao):
                jogo.adicionar_barreira( x, y, orientacao)
            else:
                print("Posição inválida para a parede.")

            #tabuleiro_quoridor = jogo.adicionar_barreira(x, y, orientacao)  # Exemplo de adição de barreira horizontal
            jogo.imprimir_tabuleiro()
        else:
            print("Selecione uma jogada valida: ")

# while True:
#     humano = jogada_humano()
#     jogo = jogo.jogar(humano)
#     if jogo.venceu():
#       print("Humano Venceu!")
#       break
#     elif jogo.empate():
#       print("Empate!")
#       break
#     computador = melhor_jogada_agente(jogo)
#     print(f"Jogada do Computador é {computador}")
#     jogo = jogo.jogar(computador)
#     print(jogo)
#     if jogo.venceu():
#       print("Computador venceu!")
#       break
#     elif jogo.empate():
#       print("Empate!")
#       break


    # tabuleiro_quoridor = adicionar_barreira(tabuleiro_quoridor, 1, 7, 'V',posicao_atual_p1,posicao_atual_p2)  # Exemplo de adição de barreira horizontal
    # tabuleiro_quoridor = adicionar_barreira(tabuleiro_quoridor, 3, 9, 'H', posicao_atual_p1,posicao_atual_p2)  # Exemplo de adição de barreira horizontal
    #tabuleiro_quoridor = adicionar_barreira(tabuleiro_quoridor, 3, 9, 'H', posicao_atual_p1,posicao_atual_p2)  # Exemplo de adição de barreira horizontal

    #jogo.imprimir_tabuleiro(tabuleiro_quoridor)
    
# Exemplo de uso da função
#tabuleiro_quoridor = criar_tabuleiro()

print("Jogador", jogo.turno, "venceu")
#movimento = 'E'  # Movimento para baixo
 # Lista de barreiras (ainda não implementada)

# sucesso, resultado = mover_peca(tabuleiro_quoridor, posicao_atual_p1, movimento, barreiras)

# if sucesso:
#     imprimir_tabuleiro(tabuleiro_quoridor)
# else:
#     print(resultado)

# print("")

# posicao_atual_p1 = encontrar_posicao(tabuleiro_quoridor, "P1")  # Posição inicial do jogador 1(Ta chu)
# posicao_atual_p2 = encontrar_posicao(tabuleiro_quoridor, "P2")  # Posição inicial do jogador 1(Ta chu)
# sucesso, resultado = mover_peca(tabuleiro_quoridor, posicao_atual_p1, movimento)
# if sucesso:
#     imprimir_tabuleiro(tabuleiro_quoridor)
# else:
#     print(resultado)




# ... (restante do seu código)
