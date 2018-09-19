import numpy as np
from random import randint
from random import random
from operator import itemgetter


#v_inicial: verticie de inicio
#dim: dimensao (quantidade de cidades)
def gerar_individuo(v_inicial, dim):
    individuo = []
    individuo.append(v_inicial)

    while(len(individuo) != dim-1):
        r = randint(1, dim-1)
        if r not in individuo:
            individuo.append(r)

    #a proxima insercao eh para ter uma ultima coluna que sera a fitness
    r = randint(1, dim)
    individuo.append(r)
    return individuo


#num_pop: numero de individuos na populacao
def gerar_populacao(v_inicial, dim, num_pop):
    #populacao
    pop = np.empty(shape = [0, dim+1])

    for i in range(num_pop):
        x = np.array(gerar_individuo(v_inicial, dim+1))
        print(x)
        pop = np.append(pop, [x], axis=0)
    
    return pop


#pop: populacao
def calcular_fitness(pop, mat_dist, fobj):
    dim = len(pop[0])
    #pos_fit eh a coluna que se encontra a fitness do individuo
    pos_fit = dim-1
    for i in range(len(pop)):
        fit = fobj(pop[i][0:pos_fit], mat_dist)
        pop[i][pos_fit] = fit
    
    #retorna a populacao de forma ordenada aonde a ultima coluna contem a fitness de cada individuo (cada linha)
    return sorted(pop, key=itemgetter(pos_fit))


#funcao que faz a selecao dos individuos atraves do elitismo
def selecao(pop, taxa_elitismo = 0.1):
    #calcula quantos individuos serao selecionados
    num_selecionados = int(round(len(pop)*taxa_elitismo))
    print(num_selecionados)

    if num_selecionados == 0:
        num_selecionados = 1
    
    #como a populacao foi ordenada por fitness em calcular_fitness, entao, retornamos os num_selecinados primeiros individuos
    return pop[0:num_selecionados]

# troca duas posicoes do individuo
def troca(ind_i,n1,n2):
    aux = ind_i[n1]
    ind_i[n1] = ind_i[n2]
    ind_i[n2] = aux
    return ind_i

def mutacao(pop,num_mutacao,fobj,matriz_dist):
    inicio = len(pop) - num_mutacao # vai sofrer mutacao apenas os individuos que foram criados pelo crossover
    dim = len(pop[0])-2
	
    for i in range(inicio,len(pop)):
	for j in range(2): # duas mutacoes serao feitas nos individuos, isso é apenas um valor podendo depois ser alterado
	    n1 = randint(1,dim)
	    n2 = randint(1,dim)
	    ind_i = np.copy(pop[i])
	    ind_i = troca(ind_i,n1,n2)
	    copied = np.copy(ind_i[0:dim+1].astype(np.int64)) # foi necessario a conversao pois quando insere algum
            #individuo na populacao o numpy converte os valores para float64
	    ind_i[dim+1] = fobj(copied,matriz_dist)
            
	    if ind_i[dim] < pop[i][dim]:
		pop[i] = np.copy(ind_i)
    return pop

def selec_Aleator_Dois_Pontos_De_Corte_Do(Pai1):
    lim = len(Pai1) - 2

    while True:
	limite_inferior = randint(1,lim)
	limite_superior = randint(1,lim)

	if limite_inferior < limite_superior:
	   return (limite_inferior,limite_superior)
		

def elemento_repetido(individuo,limite_inferior,limite_superior):
    tam = len(individuo) - 1

    for i in range(1,tam):
	for j in range(i+1,tam):
	    if individuo[i] == individuo[j]:
		if j >= limite_inferior and j <= limite_superior:
		   return i
		else:
		   return j

     return -1

def acabar_repeticao(filho,pai,limite_inferior,limite_superior):

    while True:
	indice_repeticao = elemento_repetido(filho,limite_inferior,limite_superior)

	if indice_repeticao == -1:
	   break
	else:
	    filho[indice_repeticao] = np.copy(pai[indice_repeticao])

     return filho

def PMX(pai_1,pai_2): #PMX e o nome do algoritmo de crossover que usei
    filho1 = np.copy(pai_1)
    filho2 = np.copy(pai_2)

    limite_inferior,limite_superior = selec_Aleator_Dois_Pontos_De_Corte_Do(pai_1)

    filho1[limite_inferior:(limite_superior+1)] = np.copy(pai_2[limite_inferior:(limite_superior+1)])
    filho2[limite_inferior:(limite_superior+1)] = np.copy(pai_1[limite_inferior:(limite_superior+1)])

    filho1 = acabar_repeticao(filho1,pai_2,limite_inferior,limite_superior)

    filho2 = acabar_repeticao(filho2,pai_1,limite_inferior,limite_superior)

    return (filho1,filho2)



def crossover(pop,taxa_crossover,tam_pop):
    tamanho_inicial = len(pop)

    while len(pop) < tam_pop:
	  prob = random()
	  n1 = randint(0,tamanho_inicial)
	  n2 = randint(0,tamanho_inicial)

	  if prob <= taxa_crossover:
	     f1,f2 = PMX(pop[n1],pop[n2])
	     pop = np.append(pop,[f1],axis=0)
	     pop = np.append(pop,[f2],axis=0)
     return pop

