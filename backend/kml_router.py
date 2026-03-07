"""
ARCHIVO: kml_router.py

Este archivo implementa el motor de enrutamiento y búsqueda de caminos
cortos utilizando la estructura de grafos de NetworkX. Carga coordenadas de un KML,
construye el grafo, resuelve problemas de topologías inconexas (como uniones en T)
y calcula distancias para rutas. También integra manejo en caché y simplificación por Douglas-Peucker.
"""

# IMPORTACIONES
import xml.etree.ElementTree as ET
import networkx as nx
import math
import os
import time
from functools import lru_cache

# FUNCIONES AUXILIARES

def haversine_distance(coord1, coord2):
    """
    CALCULAR DISTANCIA HAVERSINE
    
    Calcula la distancia aproximada sobre la superficie terrestre en metros
    entre dos puntos geográficos (latitud y longitud).
    """
    R = 6371000  # Radio de la Tierra en metros
    lat1, lon1 = math.radians(coord1[0]), math.radians(coord1[1])
    lat2, lon2 = math.radians(coord2[0]), math.radians(coord2[1])

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c

def simplify_path(path, tolerance=1.5):
    """
    SIMPLIFICAR RUTA
    
    Rebaja la cantidad de nodos de una ruta mediante el algoritmo Douglas-Peucker.
    Descarta puntos que están a una distancia menor de la "tolerancia"
    respecto al segmento trazado por sus vecinos adyacentes.
    
    Args:
        path: Lista de coordenadas del camino.
        tolerance: Distancia máxima en metros para marginar redundancia de puntos.
    """
    if len(path) <= 2:
        return path
    
    def perpendicular_distance(point, line_start, line_end):
        """Distancia lateral entre vértice interno y el segmento principal"""
        # Formatear paramétros a tupla pura
        p = tuple(point)
        a = tuple(line_start)
        b = tuple(line_end)
        
        # Geometría analítica plana proyectar vector
        px, py = p
        ax, ay = a
        bx, by = b
        dx, dy = bx - ax, by - ay
        
        if dx == 0 and dy == 0:
            return haversine_distance(p, a)
        
        t = ((px - ax) * dx + (py - ay) * dy) / (dx*dx + dy*dy)
        t = max(0, min(1, t))
        proj = (ax + t * dx, ay + t * dy)
        
        return haversine_distance(p, proj)
    
    # Identificar el punto de inflexión más alejado a la recta
    dmax = 0
    index = 0
    end = len(path) - 1
    
    for i in range(1, end):
        d = perpendicular_distance(path[i], path[0], path[end])
        if d > dmax:
            index = i
            dmax = d
    
    # Evaluar si la máxima distensión supera los criterios visuales paramétricos
    if dmax > tolerance:
        # Simplificación recursiva binaria
        left = simplify_path(path[:index + 1], tolerance)
        right = simplify_path(path[index:], tolerance)
        
        # Amalgama deduplicando pivote fusionado
        result = left[:-1] + right
    else:
        # Recta perfecta, marginando intermedios redundantes
        result = [path[0], path[end]]
    
    return result

# CLASES PRINCIPALES

class KMLRouter:
    """
    ENRUTADOR KML
    
    Clase principal que orquesta el grafo topológico desde un recurso .kml
    para poder inferir trayectos a través del campus.
    """
    def __init__(self, kml_path):
        """
        CONSTRUCTOR
        
        Inicializa variables, instancia de grafo y métricas de desempeño.
        """
        self.graph = nx.Graph()
        self.kml_path = kml_path
        self.route_cache = {}  # Caché para rutas frecuentes
        self.cache_hits = 0
        self.cache_misses = 0
        self.total_queries = 0
        self._build_graph()

    def _build_graph(self):
        """
        CONSTRUIR GRAFO
        
        Procesa el archivo estructurado KML para ubicar los elementos LineString 
        y convertirlos en tensores formales listos para el grafo algebraico.
        """
        if not os.path.exists(self.kml_path):
            print(f"Advertencia: Archivo KML no encontrado en {self.kml_path}")
            return

        tree = ET.parse(self.kml_path)
        root = tree.getroot()
        namespace = {'kml': 'http://www.opengis.net/kml/2.2'}

        # Escanear objetos tipo LineStrings
        for placemark in root.findall('.//kml:Placemark', namespace):
            line_string = placemark.find('.//kml:LineString/kml:coordinates', namespace)
            if line_string is not None and line_string.text:
                coords_text = line_string.text.strip()
                # Configurar las coordenadas: "lon,lat,z lon,lat,z ..."
                points = []
                for part in coords_text.split():
                    try:
                        lon, lat, *_ = map(float, part.split(','))
                        points.append((lat, lon))
                    except ValueError:
                        continue
                
                # Relacionar puntos subsecuentes validando su distancia
                for i in range(len(points) - 1):
                    u = points[i]
                    v = points[i + 1]
                    dist = haversine_distance(u, v)
                    
                    # Redondear valores posicionales a aproximadamente 11 centímetros
                    # de precisión (6 lugares tras el punto) y así forzar colisión entre nodos convergentes.
                    u_key = (round(u[0], 6), round(u[1], 6))
                    v_key = (round(v[0], 6), round(v[1], 6))
                    
                    self.graph.add_edge(u_key, v_key, weight=dist)

        self._fix_topology()

    def _fix_topology(self):
        """
        REPARAR TOPOLOGIA
        
        Escanea nodos geográficamente próximos a aristas disolutamente sin conectar
        creando derivaciones perfectas (T-junctions) insertados como atajos temporales
        del grafo solucionando ineficiencias del trazo inicial del plano virtual.
        """
        import time
        threshold = 2.0  # en metros
        
        # Necesario crear lista paralela porque se iteran al mismo tiempo que se modifican
        nodes = list(self.graph.nodes)
        edges = list(self.graph.edges(data=True))
        
        new_edges = []
        edges_to_remove = []

        # Proyecto de ayudante para iterar propecciones ortogonales
        def project(p, a, b):
            px, py = p
            ax, ay = a
            bx, by = b
            dx, dy = bx - ax, by - ay
            if dx == 0 and dy == 0: return a
            t = ((px - ax) * dx + (py - ay) * dy) / (dx*dx + dy*dy)
            t = max(0, min(1, t))
            return (ax + t * dx, ay + t * dy)

        count = 0
        for node in nodes:
            for u, v, data in edges:
                if node == u or node == v:
                    continue
                
                proj = project(node, u, v)
                dist = haversine_distance(node, proj)
                
                if dist < threshold:
                    # Encontró una falla estructural virtual que debe corregir
                    # Estrategia simplificada: insertar sub-nodo colindante
                    
                    # Redondear y adaptar
                    proj_key = (round(proj[0], 6), round(proj[1], 6))
                    
                    if proj_key == u or proj_key == v:
                        # Si coincide con un extremo, se traza al mismo objetivo
                        target = u if proj_key == u else v
                        self.graph.add_edge(node, target, weight=haversine_distance(node, target))
                    else:
                        # Corrección radical del vértice fracturado en el KML
                        # Crea un puente al romper el segmento general e incrustando el atajo central.
                        try:
                            self.graph.remove_edge(u, v)
                            weight_u = haversine_distance(u, proj_key)
                            weight_v = haversine_distance(v, proj_key)
                            weight_n = haversine_distance(node, proj_key)
                            
                            self.graph.add_edge(u, proj_key, weight=weight_u)
                            self.graph.add_edge(v, proj_key, weight=weight_v)
                            self.graph.add_edge(node, proj_key, weight=weight_n)
                            count += 1
                            # Interrumpir bucle redundante al fragmentarse
                            break 
                        except nx.NetworkXError:
                            # Arista previamente eliminada por solapamiento de intercepción
                            pass

    def find_shortest_path(self, start_coords, end_coords):
        """
        ENCONTRAR RUTA MAS CORTA
        
        Descubre el sendero algorítmico y geográfico entre los dos puntos requeridos,
        empleando abstracción matemática de grafos con Dijkstra's algorithm.
        Ofrece aceleración mediante caché e inyecciones de nodos temporales.
        """
        start_time = time.time()
        self.total_queries += 1
        
        if not self.graph.nodes:
            print("Enrutador: El grafo base se encuentra sin nodos activos.")
            return [], 0
        
        # Validar caché mapeando 5 cifras (alrededor de ~1m)
        cache_key = (
            round(start_coords[0], 5), round(start_coords[1], 5),
            round(end_coords[0], 5), round(end_coords[1], 5)
        )
        
        # Si la consulta existe de antes, devolver inmediatamente
        if cache_key in self.route_cache:
            self.cache_hits += 1
            cached_path, cached_dist = self.route_cache[cache_key]
            elapsed = (time.time() - start_time) * 1000
            print(f"Enrutador: Caché EXISTOSO ({elapsed:.1f}ms) - Tasa efectividad: {self.cache_hits}/{self.total_queries}")
            return cached_path, cached_dist
        
        self.cache_misses += 1

        # Función geométrica ad-hoc
        def project_point(p, a, b):
            px, py = p
            ax, ay = a
            bx, by = b
            dx, dy = bx - ax, by - ay
            if dx == 0 and dy == 0: return a
            t = ((px - ax) * dx + (py - ay) * dy) / (dx*dx + dy*dy)
            t = max(0, min(1, t))
            return (ax + t * dx, ay + t * dy)

        # Buscar el conector más congruente del grafo a la petición viva
        def get_nearest_edge_point(target_point):
            best_point = None
            min_dist = float('inf')
            best_edge = None
            
            # Comprobar alineación o fijación hacia todos los nodos orgánicos
            for node in self.graph.nodes:
                dist = haversine_distance(target_point, node)
                if dist < min_dist:
                    min_dist = dist
                    best_point = node
                    # Buscar relación o conectores contiguos de este mismo
                    neighbors = list(self.graph.neighbors(node))
                    if neighbors:
                        best_edge = (node, neighbors[0])
            
            # Probar penalizando colisiones artificiales con lineas medias del borde
            # versus anclaje directo de un vértice de intereseccion
            for u, v, data in self.graph.edges(data=True):
                proj = project_point(target_point, u, v)
                dist_to_proj = haversine_distance(target_point, proj)
                
                # Penalización: Es preferible chocar con un nodo conector a uniones ficticias
                # Evita fallos semánticos si la dif es baja.
                penalized_dist = dist_to_proj * 1.1 
                
                if penalized_dist < min_dist:
                    min_dist = penalized_dist
                    best_point = proj
                    best_edge = (u, v)
                    
            return best_point, best_edge

        # OPTIMIZACION: Trazar temporales directamente contra memoria para ahorrar costo clonacion
        temp_nodes = []
        temp_edges = []
        
        try:
            # 1. Anexar e intercalar origen solicitado como un anclaje foráneo
            s_proj, s_edge = get_nearest_edge_point(start_coords)
            if s_proj:
                self.graph.add_node(start_coords)
                temp_nodes.append(start_coords)
                
                s_proj_rounded = (round(s_proj[0], 6), round(s_proj[1], 6))
                if s_proj_rounded not in self.graph.nodes:
                    self.graph.add_node(s_proj_rounded)
                    temp_nodes.append(s_proj_rounded)
                
                self.graph.add_edge(start_coords, s_proj_rounded, weight=haversine_distance(start_coords, s_proj_rounded))
                temp_edges.append((start_coords, s_proj_rounded))
                
                u, v = s_edge
                self.graph.add_edge(s_proj_rounded, u, weight=haversine_distance(s_proj_rounded, u))
                self.graph.add_edge(s_proj_rounded, v, weight=haversine_distance(s_proj_rounded, v))
                temp_edges.append((s_proj_rounded, u))
                temp_edges.append((s_proj_rounded, v))
            else:
                print("Enrutador: Incapacidad para anclar y encontrar origen en la malla de polígonos.")
                return [], 0
                
            # 2. Anexar e intercalar destino invocado como pin foráneo
            e_proj, e_edge = get_nearest_edge_point(end_coords)
            if e_proj:
                self.graph.add_node(end_coords)
                temp_nodes.append(end_coords)
                
                e_proj_rounded = (round(e_proj[0], 6), round(e_proj[1], 6))
                if e_proj_rounded not in self.graph.nodes:
                    self.graph.add_node(e_proj_rounded)
                    temp_nodes.append(e_proj_rounded)
                
                self.graph.add_edge(end_coords, e_proj_rounded, weight=haversine_distance(end_coords, e_proj_rounded))
                temp_edges.append((end_coords, e_proj_rounded))
                
                u, v = e_edge
                self.graph.add_edge(e_proj_rounded, u, weight=haversine_distance(e_proj_rounded, u))
                self.graph.add_edge(e_proj_rounded, v, weight=haversine_distance(e_proj_rounded, v))
                temp_edges.append((e_proj_rounded, u))
                temp_edges.append((e_proj_rounded, v))
            else:
                print("Enrutador: Incapacidad para anclar coordenadas remotas para llegar al destino central.")
                return [], 0

            # Cálculos internos abstractos a traves de NetworkX (Formula Dijkstra)
            path_nodes = nx.dijkstra_path(self.graph, start_coords, end_coords, weight='weight')
            total_dist = nx.dijkstra_path_length(self.graph, start_coords, end_coords, weight='weight')
            
            # Reestructurar como iterador estándar de matriz geo
            path_list = [[node[0], node[1]] for node in path_nodes]
            
            # OPTIMIZACION: Eliminar puntos basura antes de despachar visualización (Algoritmo DP)
            original_points = len(path_list)
            if len(path_list) > 3:
                path_list = simplify_path(path_list, tolerance=1.5)
            
            # Empujar rutas a contenedor de sesiones recurrentes de memoria caché
            if len(self.route_cache) >= 100:
                # Quitar viejo índice dict FIFO
                self.route_cache.pop(next(iter(self.route_cache)))
            self.route_cache[cache_key] = (path_list, total_dist)
            
            elapsed = (time.time() - start_time) * 1000
            print(f"Enrutador: Análisis topológico completo en {elapsed:.1f}ms | Reducción nodos: {original_points}→{len(path_list)} | Distancia M: {total_dist:.1f}m")
            
            return path_list, total_dist
            
        except nx.NetworkXNoPath:
            return [], 0
        except Exception as e:
            print(f"Error interpretando malla lógica: {e}")
            return [], 0
        finally:
            # CRITICO: Remover parásitos temporales de la gráfica maestra o arruinará el algoritmo
            for edge in temp_edges:
                try:
                    self.graph.remove_edge(*edge)
                except:
                    pass
            for node in temp_nodes:
                try:
                    self.graph.remove_node(node)
                except:
                    pass
    
    def get_cache_stats(self):
        """
        OBTENER ESTADISTICAS DE CACHE
        
        Devuelve porcentajes y cifras numéricas informando cuánta
        potencia se ha aliviado gracias al reciclaje en memoria secundaria.
        """
        hit_rate = (self.cache_hits / self.total_queries * 100) if self.total_queries > 0 else 0
        return {
            'total_queries': self.total_queries,
            'cache_hits': self.cache_hits,
            'cache_misses': self.cache_misses,
            'hit_rate': f"{hit_rate:.1f}%",
            'cache_size': len(self.route_cache)
        }
    
    def clear_cache(self):
        """
        LIMPIAR CACHE
        
        Suprime todos los registros temporales del historial.
        """
        self.route_cache.clear()
        print("Enrutador: Caché limpiada eficientemente.")
