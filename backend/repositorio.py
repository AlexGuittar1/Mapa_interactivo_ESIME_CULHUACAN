from grafo_ESIME import GrafoCampus
from models import CaminoDB


def cargar_sistema():
    grafo = GrafoCampus()

    caminos = CaminoDB.query.all()
    for c in caminos:
        grafo.agregar_camino(c.origen, c.destino, c.distancia)

    return grafo

