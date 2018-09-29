import random as rnd
import matplotlib.pyplot as plt
import numpy as numpy
import sys as sys

import time as time

from cidade import *
from leitura import *
from Utils import matrix as matrix
from Utils import utils as utils

#Classe apenas para armazenar os dados que serão usados
class Produto():
    def __init__(self, nome, espaco, valor):
        self.nome = nome
        self.espaco = espaco
        self.valor = valor
        
#Classe que representa cada solução gerada. Ela que precisamos mudar.
#Neste problema nós procuramos os produtos a serem levados em um caminhão de
#espaço limitado de forma a maximizar o lucro.
class Individuo():
    def __init__(self, distancias, indice_vertice_inicial, geracao = 1):
        self.distancias = distancias
        self.geracao = geracao
        self.distancia_percorrida = 0
        self.nota_avaliacao = 0
        self.indice_vertice_inicial = indice_vertice_inicial
        self.cromossomo = []
                
    #Função que vai atribuir uma nota pra solução gerada.
    def avaliacao(self):
        soma_distancias = 0
        
        for i in range(len(self.cromossomo) - 1):
            soma_distancias += self.distancias[self.cromossomo[i]][self.cromossomo[i+1]]
            
        self.distancia_percorrida = soma_distancias
        #Divido 1 pela distância pra ser a nota, já que quanto maior a distancia,
        #menor a nota
        self.nota_avaliacao = 1 / soma_distancias
        
    #Algoritmo usado: Ordered Crossover
    def crossover(self, outro_individuo, geracao):
        corte = round(rnd.random() * len(self.cromossomo))
                
        parte1 = self.cromossomo[:corte]
        parte2 = outro_individuo.cromossomo
        
        #Adiciona o elemento à parte 2, caso ele não esteja presente na parte 1.
        #Isto é para impedir que haja repetição de vértices.
        
        idx = sorted([parte2.index(i) for i in list(set(parte2) - set(parte1))])
        parte2 = [parte2[i] for i in idx]
        
        filho1 = parte1[:corte] + parte2
                
        parte1 = outro_individuo.cromossomo[:corte]
        parte2 = self.cromossomo
        
        idx = sorted([parte2.index(i) for i in list(set(parte2) - set(parte1))])
        parte2 = [parte2[i] for i in idx]
        
        filho2 = parte1 + parte2
        
        filhos = [Individuo(self.distancias, self.indice_vertice_inicial, geracao + 1),
                  Individuo(self.distancias, self.indice_vertice_inicial, geracao + 1)]
        
        filhos[0].cromossomo = filho1
        filhos[1].cromossomo = filho2
        
        return filhos
    
    #Função que pode modificar cada gene. O gene só será modificado se o valor 
    #gerado aleatóriamente for maior que a taxa de mutação.
    #Se ocorrer mutação, troca a posição de 2 genes
    def mutacao(self, taxa_mutacao):      
        #Não pode haver mutação no vértice inicial       
        chance_mutacao = taxa_mutacao * len(self.cromossomo) * rnd.random()
        
        if rnd.random() < chance_mutacao:
            qtd_cromossomos_mutados = round(taxa_mutacao * len(self.cromossomo))
            
            for i in range(qtd_cromossomos_mutados):
                #-1 pra ignorar a primeira posicao e -1 já que começa de 0 e +1 para ignorar
                #a posicao 0
                posicao1 = round(rnd.random() * (len(self.cromossomo) - 2)) + 1
                posicao2 = round(rnd.random() * (len(self.cromossomo) - 2)) + 1
                
                temp = self.cromossomo[posicao1]
                self.cromossomo[posicao1] = self.cromossomo[posicao2]
                self.cromossomo[posicao2] = temp
                
        return self
    
#Classe que vai gerenciar todo o procedimento do algoritmo genetico. Acredito 
#que a única coisa que vai precisar mudar nela é a função que inicializa a 
#população.
class AlgoritmoGenetico():
    def __init__(self, tamanho_populacao):
        self.tamanho_populacao = tamanho_populacao
        self.populacao = []
        self.geracao = 0
        self.melhor_solucao = 0
        self.soma_avaliacao = 0
        self.lista_solucoes = []
        
    #Temos que adaptar os parâmetros recebidos para os usados em nosso problema.
    def inicializa_populacao(self, distancias, indice_vertice_inicial):
        for i in range(self.tamanho_populacao):
            self.populacao.append(Individuo(distancias, indice_vertice_inicial))
            self.populacao[i].cromossomo = list(range(len(distancias)))
            rnd.shuffle(self.populacao[i].cromossomo)
            
            #Colocar o vértice inicial na posição 0
            for j in range(len(self.populacao[i].cromossomo)):
                if self.populacao[i].cromossomo[j] == indice_vertice_inicial:
                    temp = self.populacao[i].cromossomo[0]
                    self.populacao[i].cromossomo[0] = indice_vertice_inicial
                    self.populacao[i].cromossomo[j] = temp
                    
                    break
            
        self.melhor_solucao = self.populacao[0]
        
    def ordena_populacao(self):
        self.populacao = sorted(self.populacao,
                                key = lambda populacao: populacao.nota_avaliacao,
                                reverse = True)
        
    def melhor_individuo(self, individuo):
        if individuo.nota_avaliacao > self.melhor_solucao.nota_avaliacao:
            self.melhor_solucao = individuo
            
    #Soma as avaliações dos individuos da geração. É necessária na hora de 
    #selecionar o pai.
    def soma_avaliacoes(self):
        soma = 0
        
        for individuo in self.populacao:
            soma += individuo.nota_avaliacao
            
        return soma
    
    #Seleciona o pai usando o método da roleta viciada.
    def seleciona_pai(self, soma_avaliacao):
        pai = -1
        valor_sorteado = rnd.random() * soma_avaliacao
        soma = 0
        i = 0
        
        while i < len(self.populacao) and soma < valor_sorteado:
            soma += self.populacao[i].nota_avaliacao
            pai += 1
            i += 1
            
        return pai   
    
    #Função apenas pra printar os resultados de cada geração.
    def visualiza_geracao(self):
        print("\nGeracao atual: %s | Melhor solução -> G:%s -> Distancia: %s" % (self.geracao, 
                                                               self.melhor_solucao.geracao,
                                                               self.melhor_solucao.distancia_percorrida))
        
    #Gerencia o funcionamento do algoritmo genético.
    def resolver(self, taxa_mutacao, numero_geracoes, distancias, indice_vertice_inicial):
        self.inicializa_populacao(distancias, indice_vertice_inicial)
        
        for individuo in self.populacao:
            individuo.avaliacao()
            self.soma_avaliacao += individuo.nota_avaliacao
        
        self.ordena_populacao()
        
        self.melhor_solucao = self.populacao[0]
        self.lista_solucoes.append(self.melhor_solucao.distancia_percorrida)
        
        #self.visualiza_geracao()

        self.geracao += 1
        
        for geracao in range(numero_geracoes):
            #soma_avaliacao = self.soma_avaliacoes()
            nova_populacao = []
             
            for individuos_gerados in range(0, self.tamanho_populacao, 2):                 
                pai1 = self.seleciona_pai(self.soma_avaliacao)
                pai2 = self.seleciona_pai(self.soma_avaliacao)
                
                while pai1 == pai2:
                    pai2 = self.seleciona_pai(self.soma_avaliacao)                    
                
                filhos = self.populacao[pai1].crossover(self.populacao[pai2], self.geracao)
                                
                nova_populacao.append(filhos[0].mutacao(taxa_mutacao))
                nova_populacao.append(filhos[1].mutacao(taxa_mutacao))
                
            individuos_mantidos = self.populacao[:round(self.tamanho_populacao * 0.10)]
                
            self.populacao = list(nova_populacao) + individuos_mantidos
            
            #print("Soma avaliacao: %s" % self.soma_avaliacao)
            self.soma_avaliacao = 0
            
            for individuo in self.populacao:
                individuo.avaliacao()
                self.soma_avaliacao += individuo.nota_avaliacao
                
            self.ordena_populacao()

            self.populacao = self.populacao[:self.tamanho_populacao]

            if geracao % 100 == 0:    
                self.visualiza_geracao()

            self.geracao += 1
            
            melhor = self.populacao[0]
            self.lista_solucoes.append(melhor.distancia_percorrida)
            self.melhor_individuo(melhor)
            
            #print("Proximo ciclo")
            
        self.visualiza_geracao()
        print("Cromossomo: %s" % self.melhor_solucao.cromossomo)
        
        return (self.melhor_solucao.cromossomo,self.melhor_solucao.distancia_percorrida)
            
    
#Apenas cria a lista de produtos que serão usados, chama a função que executa
#o algoritmo genético, printa o resultado e printa o gráfico.
if __name__ == '__main__':
    #agrv[1]: caminho dados
    #argv[2]: ponto x V_inicial
    #argv[3]: ponto y V_inicial
    #argv[4]: tamanho pop
    #argv[5]: tx mutacao
    #argv[6]: num geracoes
    
    lista_cidades = []
    
    entrada = "a280.tsp"
    vertice_inicial = (288, 149)
    tamanho_populacao = 20
    taxa_mutacao = 0.025
    numero_geracoes = 100
    
    lista_cidades = getListaCidades(lerEntrada(entrada))

    distancias = matrix.calc_distances(lista_cidades)
    
    '''
    lista_cidades = getListaCidades(lerEntrada(sys.argv[1]))

    distancias = matrix.calc_distances(lista_cidades)
    
    tamanho_populacao = int(sys.argv[4])
    taxa_mutacao = float(sys.argv[5])
    numero_geracoes = int(sys.argv[6])
    vertice_inicial = (float(sys.argv[2]), float(sys.argv[3]))

    print("x: %s  y: %s" % (sys.argv[2], sys.argv[3]))
    '''
    
    
    print(lista_cidades[0].x, lista_cidades[0].y)
    
    indice_vertice_inicial = utils.search_vertex_index(vertice_inicial, lista_cidades)
    
    if indice_vertice_inicial != -1:
        ag = AlgoritmoGenetico(tamanho_populacao)
    
        resultado = ag.resolver(taxa_mutacao, numero_geracoes, distancias, indice_vertice_inicial)
        
        plt.plot(ag.lista_solucoes)
        plt.title("Acompanhamento dos valores")
        plt.show()
    else:
        print("Vertice inexistente!")
    

