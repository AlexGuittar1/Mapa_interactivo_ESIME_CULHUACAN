import heapq

class GrafoCampus:
    def __init__(self):
        self.adyacencia = {}

    def agregar_edificio(self, nombre):
        if nombre not in self.adyacencia:
            self.adyacencia[nombre] = []

    def agregar_camino(self, origen, destino, distancia):
        self.agregar_edificio(origen)
        self.agregar_edificio(destino)

        self.adyacencia[origen].append((destino, distancia))
        self.adyacencia[destino].append((origen, distancia))

# Implementación del algoritmo de Dijkstra

    def ruta_mas_corta(self, inicio, fin):
        if inicio not in self.adyacencia or fin not in self.adyacencia:
            return None, None

        distancias = {nodo: float("inf") for nodo in self.adyacencia}
        anteriores = {nodo: None for nodo in self.adyacencia}

        distancias[inicio] = 0
        cola = [(0, inicio)]

        while cola:
            distancia_actual, actual = heapq.heappop(cola)

            if actual == fin:
                break

            if distancia_actual > distancias[actual]:
                continue

            for vecino, peso in self.adyacencia[actual]:
                nueva_distancia = distancia_actual + peso
                if nueva_distancia < distancias[vecino]:
                    distancias[vecino] = nueva_distancia
                    anteriores[vecino] = actual
                    heapq.heappush(cola, (nueva_distancia, vecino))

        camino = []
        actual = fin
        while actual:
            camino.insert(0, actual)
            actual = anteriores[actual]

        return camino, distancias[fin]
