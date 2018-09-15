#funcao objetiva
#P: vertices
#M: matriz
#verificar se o indice das matrizes lendo comeca em zero ou em 1
def fobj(P, M):
    s = 0
    c_ant = P[0]
    for c in P[1:]:
        s+=M[c_ant-1][c-1]
        c_ant = c
    s+=M[P[-1]-1][P[0]-1]
    return s
