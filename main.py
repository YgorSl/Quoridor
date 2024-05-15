from copy import copy
from quoridor import Quoridor
import minmax
    
jogo = Quoridor()
jogo.imprimir_tabuleiro()
vez_atual = "P"




while(True):

    if jogo.turno == "A":
        jogo.turno_mm = jogo.turno
        jogo_prox = copy(jogo)
        proxima_jogada = minmax.melhor_jogada(jogo_prox)  # Chame a função da IA para obter a próxima jogada
        game, tipo_acao, parametros = proxima_jogada
        posicao_da_vez = jogo.encontrar_posicao(jogo.turno)

        if tipo_acao == "M":
            sucesso, resultado = jogo.mover_peca(posicao_da_vez, parametros[0])  # Aplicação do movimento
        elif tipo_acao == "P":
            x, y, orientacao = parametros
            jogo.adicionar_barreira(x, y, orientacao)  # Aplicação da barreira


        jogo.imprimir_tabuleiro()  # Imprima o tabuleiro atualizado
            # Alterne o turno para o jogador (P1)
            #jogo.turno = "P"
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

print("Jogador", jogo.get_winner(jogo.tabuleiro), "venceu")

