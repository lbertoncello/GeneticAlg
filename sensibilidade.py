def sensibilidade(lista_params,matrix_dist,v_inicial):
    num_individuos,num_geracoes,taxa_mutacao = lista_params
    melhores_param = [-1,-1,-1]
    melhor_fitness = 999999999

    for ind in num_individuos:
        for ger in num_geracoes:
            for tx in taxa_mutacao:
                ag = AlgoritmoGenetico(ind)
                solucao = ag.resolver(tx, ger, matrix_dist, v_inicial)

                if solucao.distancia_percorrida < melhor_fitness:
                    melhor_fitness = solucao.distancia_percorrida
                    melhores_param[0] = ind
                    melhores_param[1] = ger
                    melhores_param[2] = tx

                del ag

    return melhores_param
