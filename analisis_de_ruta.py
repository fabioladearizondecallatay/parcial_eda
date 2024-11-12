import heapq

# Definición del grafo de localidades y distancias
localidades = {
    "Madrid": [("Alcorcón", 13), ("Villaviciosa de Odón", 22), ("Alcalá de Henares", 35)],
    "Villanueva de la Cañada": [("Villaviciosa de Odón", 11), ("Boadilla del Monte", 7)],
    "Alcorcón": [("Madrid", 13), ("Móstoles", 5)],
    "Móstoles": [("Alcorcón", 5), ("Fuenlabrada", 8)],
    "Fuenlabrada": [("Móstoles", 8), ("Getafe", 10)],
    "Getafe": [("Fuenlabrada", 10), ("Madrid", 16)],
    "Villaviciosa de Odón": [("Madrid", 22), ("Villanueva de la Cañada", 11)],
    "Boadilla del Monte": [("Villanueva de la Cañada", 7), ("Madrid", 15)],
    "Alcalá de Henares": [("Madrid", 35), ("Torrejón de Ardoz", 15)],
    "Torrejón de Ardoz": [("Alcalá de Henares", 15), ("Madrid", 20)]
}

def ruta_mas_corta(origen, destino):
    distancias = {localidad: float('inf') for localidad in localidades}
    distancias[origen] = 0
    predecesores = {localidad: None for localidad in localidades}
    cola_prioridad = [(0, origen)]

    while cola_prioridad:
        distancia_actual, actual = heapq.heappop(cola_prioridad)

        if actual == destino:
            break

        for vecino, distancia in localidades[actual]:
            nueva_distancia = distancia_actual + distancia
            if nueva_distancia < distancias[vecino]:
                distancias[vecino] = nueva_distancia
                predecesores[vecino] = actual
                heapq.heappush(cola_prioridad, (nueva_distancia, vecino))

    ruta = []
    while destino:
        ruta.insert(0, destino)
        destino = predecesores[destino]

    return ruta, distancias[ruta[-1]]

def localidades_con_conexiones_cortas():
    resultado = []
    for localidad, conexiones in localidades.items():
        if all(distancia < 15 for _, distancia in conexiones):
            resultado.append(localidad)
    return resultado

def es_conexo():
    visitados = set()
    
    def dfs(localidad):
        visitados.add(localidad)
        for vecino, _ in localidades[localidad]:
            if vecino not in visitados:
                dfs(vecino)

    inicio = next(iter(localidades))
    dfs(inicio)

    return len(visitados) == len(localidades)

def rutas_sin_ciclos(origen, destino):
    rutas = []
    cola = [(origen, [origen])]

    while cola:
        actual, camino = cola.pop(0)

        if actual == destino:
            rutas.append(camino)
            continue

        for vecino, _ in localidades[actual]:
            if vecino not in camino:
                cola.append((vecino, camino + [vecino]))

    return rutas

def ruta_mas_larga(origen, destino):
    ruta_larga = []
    distancia_maxima = 0

    def dfs(actual, camino, distancia_total):
        nonlocal ruta_larga, distancia_maxima
        if actual == destino:
            if distancia_total > distancia_maxima:
                distancia_maxima = distancia_total
                ruta_larga = camino[:]
            return

        for vecino, distancia in localidades[actual]:
            if vecino not in camino:
                camino.append(vecino)
                dfs(vecino, camino, distancia_total + distancia)
                camino.pop()

    dfs(origen, [origen], 0)
    return ruta_larga, distancia_maxima

def main():
    print("Localidades disponibles:", ", ".join(localidades.keys()))
    origen = input("\nIngrese la localidad de origen: ")
    destino = input("Ingrese la localidad de destino: ")

    if origen not in localidades or destino not in localidades:
        print("\nError: Una o ambas localidades no existen en el grafo.")
        return

    #ruta más corta
    ruta, distancia_total = ruta_mas_corta(origen, destino)
    print(f"\nLa ruta más corta entre {origen} y {destino} es: {' -> '.join(ruta)} con una distancia de {distancia_total} km")

    #localidades con conexiones cortas
    localidades_cortas = localidades_con_conexiones_cortas()
    print("\nLocalidades con conexiones cortas:", localidades_cortas)

    #Conectividad del grafo
    conexo = es_conexo()
    print("\n¿Es el grafo conexo?", "Sí" if conexo else "No")

    #Rutas sin ciclos
    rutas = rutas_sin_ciclos(origen, destino)
    print(f"\nRutas sin ciclos entre {origen} y {destino}:")
    for i, ruta in enumerate(rutas, 1):
        print(f"{i}. {' -> '.join(ruta)}")

    #Ruta más larga
    ruta_larga, distancia_larga = ruta_mas_larga(origen, destino)
    if ruta_larga:
        print(f"\nLa ruta más larga entre {origen} y {destino} es: {' -> '.join(ruta_larga)} con una distancia de {distancia_larga} km")
    else:
        print(f"\nNo hay ruta posible sin ciclos entre {origen} y {destino}.")

#Ejecutar el programa principal
if __name__ == "__main__":
    main()
