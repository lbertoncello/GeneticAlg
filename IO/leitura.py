ARQ_ENTRADA = "att532.tsp"

arq = open(ARQ_ENTRADA)
texto = arq.readlines()

texto = texto[6:]
texto = texto[:len(texto) - 1]

for linha in texto:
    linha = linha.strip()
    print(linha)

arq.close()
