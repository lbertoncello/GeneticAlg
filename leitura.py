from cidade import *

def lerEntrada(file):
    arq = open(file)
    
    texto = arq.readlines()
    texto = texto[6:]
    texto = texto[:len(texto) - 1]
    
    arq.close()
    return texto

# ARQ_ENTRADA = "./Dados/att532.tsp"

# arq = open(ARQ_ENTRADA)
# texto = arq.readlines()

# texto = texto[6:]
# texto = texto[:len(texto) - 1]

def getListaCidades(texto):

    lista_cidades = []

    for linha in texto:
        linha = linha.strip()
        aux = linha.split(' ')
        lista_cidades.append(Cidade(aux[0], float(aux[1]), float(aux[2])))

    return lista_cidades