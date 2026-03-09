"""
ARCHIVO: services/routing_service.py

SERVICIO DE ENRUTAMIENTO

Encapsula la logica de calculo de rutas usando KMLRouter y NetworkX.
Los endpoints de app.py llaman a este servicio en vez de acceder
al router directamente, facilitando el mantenimiento y las pruebas.
"""

import os


class RoutingService:
    """
    SERVICIO DE ENRUTAMIENTO

    Gestiona la inicializacion del router KML y proporciona metodos
    para calcular rutas dentro del campus.
    """

    def __init__(self):
        """Inicializa el servicio sin router. Se debe llamar a initialize() despues."""
        self.kml_router = None
        self.is_initialized = False

    def initialize(self, kml_path=None):
        """
        INICIALIZAR ROUTER

        Carga el archivo KML y construye el grafo de navegacion.

        Argumentos:
            kml_path: Ruta al archivo KML. Si no se proporciona, usa la ruta por defecto.
        """
        from kml_router import KMLRouter

        if kml_path is None:
            # Buscar el archivo KML en multiples ubicaciones posibles
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            possible_paths = [
                os.path.join(base_dir, "Camino ESIME caminable.kml"),           # backend/
                os.path.join(os.path.dirname(base_dir), "Camino ESIME caminable.kml"),  # raiz del proyecto
                os.path.join(os.getcwd(), "Camino ESIME caminable.kml"),        # directorio de ejecucion
            ]
            kml_path = None
            for p in possible_paths:
                if os.path.exists(p):
                    kml_path = p
                    break
            if kml_path is None:
                print(f"Advertencia: Archivo KML no encontrado en ninguna ubicacion conocida")
                kml_path = possible_paths[0]  # Fallback para que KMLRouter muestre su propio error

        try:
            self.kml_router = KMLRouter(kml_path)
            self.is_initialized = True
            node_count = len(self.kml_router.graph.nodes)
            print(f"[ROUTING] Grafo cargado con {node_count} nodos")
            return True
        except Exception as e:
            print(f"[ROUTING] Error al cargar KML: {e}")
            self.is_initialized = False
            return False

    def calculate_route(self, start_lat, start_lon, end_lat, end_lon):
        """
        CALCULAR RUTA

        Calcula la ruta mas corta entre dos coordenadas usando Dijkstra.

        Argumentos:
            start_lat, start_lon: Coordenadas del punto de origen
            end_lat, end_lon: Coordenadas del punto de destino

        Retorna:
            Diccionario con path (lista de coordenadas), distance (metros)
            y eta_minutes (tiempo estimado caminando).
            Retorna None si el router no esta inicializado.
        """
        if not self.is_initialized or not self.kml_router:
            return None

        path, distance = self.kml_router.find_shortest_path(
            (start_lat, start_lon),
            (end_lat, end_lon)
        )

        return {
            "path": path,
            "distance": distance,
            "eta_minutes": round(distance / 83.3, 1)
        }

    def get_graph_info(self):
        """
        OBTENER INFORMACION DEL GRAFO

        Retorna estadisticas basicas del grafo de navegacion.
        """
        if not self.is_initialized or not self.kml_router:
            return {"initialized": False}

        return {
            "initialized": True,
            "nodes": len(self.kml_router.graph.nodes),
            "edges": len(self.kml_router.graph.edges),
        }
