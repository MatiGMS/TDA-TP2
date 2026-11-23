from collections import deque

grafo_global = {}
total_esp_global = 0
bandas_global = []
plataformas_global = []
servidores_global = []
banda_servidor_global = []
servidor_plataforma_global = []
flujo_actual_global = 0



def bfs(g, s, t, parent):
    vis = set([s])
    q = deque([s])
    while q:
        u = q.popleft()
        for v, cap in g[u].items():
            if v not in vis and cap > 0:
                vis.add(v)
                parent[v] = u
                q.append(v)
                if v == t:
                    return True
    return False



def ejecutar_ff(g, s, t):
    parent = {}
    f_max = 0
    while bfs(g, s, t, parent):
        path_flow = float('inf')
        v = t
        while v != s:
            u = parent[v]
            path_flow = min(path_flow, g[u][v])
            v = u
        v = t
        while v != s:
            u = parent[v]
            g[u][v] -= path_flow
            g[v][u] += path_flow
            v = u
        f_max += path_flow
    return f_max




def calcular_asignacion(g, servidores):
    asignaciones_totales = {}

    for s_id, _ in servidores:
        in_node = s_id + '_in'
        out_node = s_id + '_out'

        entradas = []
        for nodo, flujo in g[in_node].items():
            if nodo != out_node and flujo > 0:
                entradas.append([nodo, flujo])

        salidas = []
        for nodo in g[out_node]:
            if nodo != in_node:
                flujo = g[nodo].get(out_node, 0)
                if flujo > 0:
                    salidas.append([nodo, flujo])

        i, j = 0, 0
        while i < len(entradas) and j < len(salidas):
            b, flujo_in = entradas[i]
            p, flujo_out = salidas[j]

            cant = min(flujo_in, flujo_out)
            asignaciones_totales[(b, p)] = asignaciones_totales.get((b, p), 0) + cant

            entradas[i][1] -= cant
            salidas[j][1] -= cant

            if entradas[i][1] == 0:
                i += 1
            if salidas[j][1] == 0:
                j += 1

    return [(b, p, cant) for (b, p), cant in asignaciones_totales.items() if cant > 0]



def devolver_flujo(g, origen, destino, cantidad):
    restante = cantidad
    parent = {}
    while restante > 0 and bfs(g, origen, destino, parent):
        cuello = restante
        v = destino
        while v != origen:
            u = parent[v]
            cuello = min(cuello, g[u][v])
            v = u

        v = destino
        while v != origen:
            u = parent[v]
            g[u][v] -= cuello
            g[v][u] += cuello
            v = u

        restante -= cuello
        parent = {}



def reducir_flujo_residual(g, in_node, out_node, exceso):
    devolver_flujo(g, in_node, 's', exceso)
    devolver_flujo(g, 't', out_node, exceso)



def actualizar_servidor(id_servidor, nueva_capacidad):
    global grafo_global, total_esp_global, servidores_global, flujo_actual_global
    g = grafo_global
    in_node = id_servidor + '_in'
    out_node = id_servidor + '_out'

    flujo_usado = g[out_node][in_node]
    cap_actual = g[in_node][out_node] + flujo_usado

    if nueva_capacidad > cap_actual:
        g[in_node][out_node] = nueva_capacidad - flujo_usado
        flujo_actual_global += ejecutar_ff(g, 's', 't')
    elif nueva_capacidad >= flujo_usado:
        g[in_node][out_node] = nueva_capacidad - flujo_usado
    else:
        exceso = flujo_usado - nueva_capacidad
        g[out_node][in_node] = nueva_capacidad
        g[in_node][out_node] = 0
        reducir_flujo_residual(g, in_node, out_node, exceso)
        flujo_actual_global -= exceso
        flujo_actual_global += ejecutar_ff(g, 's', 't')

    posible = (flujo_actual_global == total_esp_global)
    asignacion = calcular_asignacion(g, servidores_global)
    return (posible, flujo_actual_global, asignacion)



def main(bandas, servidores, plataformas, banda_servidor, servidor_plataforma):
    global grafo_global, total_esp_global, flujo_actual_global, bandas_global, plataformas_global, servidores_global, banda_servidor_global, servidor_plataforma_global
    bandas_global = bandas
    servidores_global = servidores
    plataformas_global = plataformas
    banda_servidor_global = banda_servidor
    servidor_plataforma_global = servidor_plataforma

    g = {'s': {}, 't': {}}
    def add_edge(u, v, c):
        if u not in g: g[u] = {}
        if v not in g: g[v] = {}
        g[u][v] = g[u].get(v, 0) + c
        if u not in g[v]: g[v][u] = 0

    total_esp = 0
    for b, bx in bandas:
        add_edge('s', b, bx)
        total_esp += bx
    total_esp_global = total_esp

    for s_id, sx in servidores:
        add_edge(s_id + '_in', s_id + '_out', sx)

    for b, s_id in banda_servidor:
        add_edge(b, s_id + '_in', float('inf'))

    for s_id, p in servidor_plataforma:
        add_edge(s_id + '_out', p, float('inf'))

    for p, px in plataformas:
        add_edge(p, 't', px)

    grafo_global = g
    f_max = ejecutar_ff(g, 's', 't')
    flujo_actual_global = f_max
    posible = (f_max == total_esp)
    asignacion = calcular_asignacion(g, servidores_global)
    return (posible, f_max, asignacion)
