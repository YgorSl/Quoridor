
def heuristica_simples(jogo):
    if jogo.turno == "P":
        return 100 * abs(jogo.encontrar_posicao("P")[0])
    else:
        return 100 * (abs(jogo.encontrar_posicao("A")[0] - 16))