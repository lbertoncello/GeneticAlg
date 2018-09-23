import random as rnd
import matplotlib.pyplot as plt
import numpy as numpy

from cidade import *
from Utils import *

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
    def __init__(self, distancias, geracao = 0):
        self.distancias = distancias
        self.geracao = geracao
        self.distancia_percorrida = 0
        self.nota_avaliacao = 0
        
        self.cromossomo = list(range(len(self.distancias)))
        rnd.shuffle(self.cromossomo)

                
    #Função que vai atribuir uma nota pra solução gerada.
    def avaliacao(self):
        soma_distancias = 0
        
        for i in range(len(self.cromossomo) - 1):
            soma_distancias += self.distancias[self.cromossomo[i]][self.cromossomo[i+1]]
            
        self.distancia_percorrida = soma_distancias
        #Inverto o sinal para atribuir como nota, já que quanto maior a distancia,
        #menor a nota
        self.nota_avaliacao = 1 / soma_distancias
        
    #Função que faz o cruzamento entre 2 indivíduos. O método de cruzamento 
    #é aquele em que você divide o cromossomo de ambos os pais em alguma parte
    #aleatória, e aí cada filho vai receber o lado esquerdo de um pai e o lado
    #direito do outro.
    def crossover(self, outro_individuo):
        corte = round(rnd.random() * len(self.cromossomo))
        
        filho1 = outro_individuo.cromossomo[0:corte] + self.cromossomo[corte::]
        filho2 = self.cromossomo[0:corte] + outro_individuo.cromossomo[corte::]
        
        filhos = [Individuo(self.distancias, self.geracao + 1),
                  Individuo(self.distancias, self.geracao + 1)]
        
        filhos[0].cromossomo = filho1
        filhos[1].cromossomo = filho2
        
        return filhos
    
    #Função que pode modificar cada gene. O gene só será modificado se o valor 
    #gerado aleatóriamente for maior que a taxa de mutação.
    #Se ocorrer mutação, troca a posição de 2 genes
    def mutacao(self, taxa_mutacao):      
        for i in range(len(self.cromossomo)):
            if rnd.random() < taxa_mutacao:
                posicao = round(rnd.random() * (len(self.cromossomo) - 1))
                
                temp = self.cromossomo[posicao]
                self.cromossomo[posicao] = self.cromossomo[i]
                self.cromossomo[i] = temp
                
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
        self.lista_solucoes = []
        
    #Temos que adaptar os parâmetros recebidos para os usados em nosso problema.
    def inicializa_populacao(self, distancias):
        for i in range(self.tamanho_populacao):
            self.populacao.append(Individuo(distancias))
            
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
        melhor = self.populacao[0]
        print("G:%s -> Distancia: %s" % (self.populacao[0].geracao,
                                                               melhor.distancia_percorrida))
        
    #Gerencia o funcionamento do algoritmo genético.
    def resolver(self, taxa_mutacao, numero_geracoes, distancias):
        self.inicializa_populacao(distancias)
        
        for individuo in self.populacao:
            individuo.avaliacao()
        
        self.ordena_populacao()
        
        self.melhor_solucao = self.populacao[0]
        self.lista_solucoes.append(self.melhor_solucao.nota_avaliacao)
        
        self.visualiza_geracao()
        
        for geracao in range(numero_geracoes):
            soma_avaliacao = self.soma_avaliacoes()
            nova_populacao = []
            
            for individuos_gerados in range(0, self.tamanho_populacao, 2):
                pai1 = self.seleciona_pai(soma_avaliacao)
                pai2 = self.seleciona_pai(soma_avaliacao)
                
                filhos = self.populacao[pai1].crossover(self.populacao[pai2])
                
                nova_populacao.append(filhos[0].mutacao(taxa_mutacao))
                nova_populacao.append(filhos[1].mutacao(taxa_mutacao))
                
            self.populacao = list(nova_populacao)
            
            for individuo in self.populacao:
                individuo.avaliacao()
            
            self.ordena_populacao()
            self.visualiza_geracao()
            
            melhor = self.populacao[0]
            self.lista_solucoes.append(melhor.nota_avaliacao)
            self.melhor_individuo(melhor)
            
        print("\nMelhor solução -> G:%s -> Distancia: %s" % (self.melhor_solucao.geracao,
                                                               self.melhor_solucao.distancia_percorrida))
        print("Cromossomo: %s" % self.melhor_solucao.cromossomo)
        
        return self.melhor_solucao.cromossomo
            
    
#Apenas cria a lista de produtos que serão usados, chama a função que executa
#o algoritmo genético, printa o resultado e printa o gráfico.
if __name__ == '__main__':
    lista_cidades = []
    lista_cidades.append(Cidade("1", 1.0, 1.0))
    lista_cidades.append(Cidade("2", 2.0, 2.0))
    lista_cidades.append(Cidade("3", 3.0, 3.0))
    lista_cidades.append(Cidade("4", 4.0, 4.0))
    lista_cidades.append(Cidade("5", 5.0, 5.0))
    lista_cidades.append(Cidade("6", 6.0, 6.0))
    lista_cidades.append(Cidade("7", 7.0, 7.0))
    lista_cidades.append(Cidade("8", 8.0, 8.0))
    lista_cidades.append(Cidade("9", 9.0, 9.0))
    lista_cidades.append(Cidade("10", 10.0, 10.0))
    lista_cidades.append(Cidade("11", 11.0, 11.0))
    lista_cidades.append(Cidade("12", 12.0, 12.0))
    
    distancias = calc_distances(lista_cidades)
    
    tamanho_populacao = 50
    taxa_mutacao = 0.01
    numero_geracoes = 1000
    
    ag = AlgoritmoGenetico(tamanho_populacao)
    
    resultado = ag.resolver(taxa_mutacao, numero_geracoes, distancias)
    
    '''
    lista_produtos = []
    lista_produtos.append(Produto("Geladeira Dako", 0.751, 999.90))
    lista_produtos.append(Produto("Iphone 6", 0.0000899, 2911.12))
    lista_produtos.append(Produto("TV 55' ", 0.400, 4346.99))
    lista_produtos.append(Produto("TV 50' ", 0.290, 3999.90))
    lista_produtos.append(Produto("TV 42' ", 0.200, 2999.00))
    lista_produtos.append(Produto("Notebook Dell", 0.00350, 2499.90))
    lista_produtos.append(Produto("Ventilador Panasonic", 0.496, 199.90))
    lista_produtos.append(Produto("Microondas Electrolux", 0.0424, 308.66))
    lista_produtos.append(Produto("Microondas LG", 0.0544, 429.90))
    lista_produtos.append(Produto("Microondas Panasonic", 0.0319, 299.29))
    lista_produtos.append(Produto("Geladeira Brastemp", 0.635, 849.00))
    lista_produtos.append(Produto("Geladeira Consul", 0.870, 1199.89))
    lista_produtos.append(Produto("Notebook Lenovo", 0.498, 1999.90))
    lista_produtos.append(Produto("Notebook Asus", 0.527, 3999.00))
    
    nomes = []
    espacos = []
    valores = []
    
    for produto in lista_produtos:
        nomes.append(produto.nome)
        espacos.append(produto.espaco)
        valores.append(produto.valor)
        
    limite_espaco = 3
    tamanho_populacao = 20
    taxa_mutacao = 0.01
    numero_geracoes = 100
    
    ag = AlgoritmoGenetico(tamanho_populacao)
    
    resultado = ag.resolver(taxa_mutacao, numero_geracoes, espacos, valores, limite_espaco)
    
    for i in range(len(lista_produtos)):
        if resultado[i] == '1':
            print("Nome: %s R$ %s" % (lista_produtos[i].nome,
                                      lista_produtos[i].valor))
    
    plt.plot(ag.lista_solucoes)
    plt.title("Acompanhamento dos valores")
    plt.show()
    '''

