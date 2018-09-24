def char_search(char, l):
    for e in l:
        if e == char:
            return True
        
    return False

def search_vertex_index(v, lista_cidades):
    for i in range(len(lista_cidades)):
        if (lista_cidades[i].x, lista_cidades[i].y) == v:
            return i
        
    return -1