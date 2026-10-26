from collections import deque

grafo_global = {}
total_esp_global = 0
bandas_global = []
plataformas_global = []
servidores_global = []
banda_servidor_global = []
servidor_plataforma_global = []

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

def calcular_asignacion(g, bandas, plataformas, banda_servidor, servidor_plataforma, servidores):
    flujo_entrada = {}
    for b, s_id in banda_servidor:
        val = g[s_id + '_in'].get(b, 0)
        if val > 0:
            if b not in flujo_entrada: flujo_entrada[b] = {}
            flujo_entrada[b][s_id] = val

    flujo_salida = {}
    for s_id, p in servidor_plataforma:
        val = g[p].get(s_id + '_out', 0)
        if val > 0:
            if s_id not in flujo_salida: flujo_salida[s_id] = {}
            flujo_salida[s_id][p] = val

    servidor_entrada_total = {}
    for b in flujo_entrada:
        for s_id, v in flujo_entrada[b].items():
            servidor_entrada_total[s_id] = servidor_entrada_total.get(s_id, 0) + v

    servidor_salida_total = {}
    for s_id in flujo_salida:
        servidor_salida_total[s_id] = sum(flujo_salida[s_id].values())

    flujos_pares = {}
    for s_id in flujo_salida:
        total_entrada = servidor_entrada_total.get(s_id, 0)
        total_salida = servidor_salida_total.get(s_id, 0)
        if total_entrada == 0 or total_salida == 0:
            continue
        for b in flujo_entrada:
            if s_id in flujo_entrada[b]:
                valor_entrada = flujo_entrada[b][s_id]
                for p, valor_salida in flujo_salida[s_id].items():
                    fraccion = (valor_entrada * valor_salida) / total_entrada
                    clave = (b, p)
                    flujos_pares[clave] = flujos_pares.get(clave, 0) + fraccion

    asignacion = []
    for (b, p), cant in flujos_pares.items():
        c_int = round(cant)
        if c_int > 0:
            asignacion.append((b, p, c_int))
    return asignacion

def main(bandas, servidores, plataformas, banda_servidor, servidor_plataforma):
    global grafo_global, total_esp_global, bandas_global, plataformas_global, servidores_global, banda_servidor_global, servidor_plataforma_global
    bandas_global = bandas
    servidores_global = servidores
    plataformas_global = plataformas
    banda_servidor_global = banda_servidor
    servidor_plataforma_global = servidor_plataforma

    g = {}
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
    posible = (f_max == total_esp)
    asignacion = calcular_asignacion(g, bandas, plataformas, banda_servidor, servidor_plataforma, servidores)
    return (posible, f_max, asignacion)

def actualizar_servidor(id_servidor, nueva_capacidad):
    global grafo_global, total_esp_global, bandas_global, plataformas_global, servidores_global, banda_servidor_global, servidor_plataforma_global
    in_node = id_servidor + '_in'
    out_node = id_servidor + '_out'
    g = grafo_global
    
    current_cap = g[in_node][out_node] + g[out_node][in_node]
    diff = nueva_capacidad - current_cap
    g[in_node][out_node] += diff
    if g[in_node][out_node] < 0:
        g[in_node][out_node] = 0
        g[out_node][in_node] = nueva_capacidad

    f_max = ejecutar_ff(g, 's', 't')
    posible = (f_max == total_esp_global)
    asignacion = calcular_asignacion(g, bandas_global, plataformas_global, banda_servidor_global, servidor_plataforma_global, servidores_global)
    return (posible, f_max, asignacion)