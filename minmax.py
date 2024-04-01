from collections import deque


def minimax_alfabeta(self, jogo, turno_max, jogador, profundidade_maxima=8, alfa=float("-inf"), beta=float("inf")):
        if jogo.venceu() or jogo.empate() or profundidade_maxima == 0:
            return jogo.calcular_utilidade(jogador)

        if turno_max:  # turno do MAX
            for proximo_jogo in jogo.jogos_validos():
                utilidade = self.minimax_alfabeta(jogo.jogar(proximo_jogo), False, jogador, profundidade_maxima - 1, alfa, beta)
                alfa = max(utilidade, alfa)
                if beta <= alfa:
                    break
            return alfa
        else:  # turno no MIN
            for proximo_jogo in jogo.jogos_validos():
                utilidade = self.minimax_alfabeta(jogo.jogar(proximo_jogo), True, jogador, profundidade_maxima - 1, alfa, beta)
                beta = min(utilidade, beta)
                if beta <= alfa:
                    break
            return beta

def melhor_jogada_agente_poda(self, profundidade_maxima=8):
    melhor_valor = float("-inf")
    melhor_jogada = -1
    for proximo_jogo in self.jogos_validos():
        utilidade = self.minimax_alfabeta(self.jogar(proximo_jogo), False, self.turno(), profundidade_maxima)
        if utilidade > melhor_valor:
            melhor_valor = utilidade
            melhor_jogada = proximo_jogo
    return melhor_jogada

def existe_caminho(self, tabuleiro, posicao_inicial, linha_final):
        # Converte o tabuleiro para um formato que facilite a verificação de barreiras
        tabuleiro_convertido = [[' ' for _ in range(9)] for _ in range(9)]
        for i in range(17):
            for j in range(17):
                if tabuleiro[i][j] == '.':
                    tabuleiro_convertido[i // 2][j // 2] = '.'

        # Inicializa a fila para BFS e adiciona a posição inicial
        fila = deque([posicao_inicial])
        visitados = set([posicao_inicial])

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