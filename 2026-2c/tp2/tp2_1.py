def contar_avenidas(edificios, cantidad_visibles):
    n= edificios
    k= cantidad_visibles


    # Inicilizamos Matriz (n+1) x (k+1)
    OPT = []
    for i in range(n + 1):
        fila = []
        for j in range(k + 1):
            fila.append(0)
        OPT.append(fila)


    # Caso base: 0 edificios y 0 visibles tiene una sola permutacion
    OPT[0][0] = 1


    for i in range(1, n + 1):          
        for j in range(1, k + 1):  
            ubicado_al_principio = OPT[i - 1][j - 1]          
            ubicado_en_el_resto_de_las_posiciones = (i - 1) * OPT[i - 1][j]
            OPT[i][j] = ubicado_al_principio + ubicado_en_el_resto_de_las_posiciones


    return OPT[n][k]


def main(n_edificios: int, k_visibles: int) -> int:
    return contar_avenidas(n_edificios , k_visibles )