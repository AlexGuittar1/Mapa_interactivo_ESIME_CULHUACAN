
import networkx as nx
import math

# Haversine and geometry helpers
def haversine_distance(coord1, coord2):
    R = 6371000
    lat1, lon1 = math.radians(coord1[0]), math.radians(coord1[1])
    lat2, lon2 = math.radians(coord2[0]), math.radians(coord2[1])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def project_point_onto_segment(p, a, b):
    # p, a, b are (lat, lon) tuples
    # Treat as flat cartesian for projection (valid for small distances)
    # x = lat, y = lon
    px, py = p
    ax, ay = a
    bx, by = b
    
    # Vector AB
    dx = bx - ax
    dy = by - ay
    
    if dx == 0 and dy == 0:
        return a
        
    # Project AP onto AB (dot product)
    t = ((px - ax) * dx + (py - ay) * dy) / (dx*dx + dy*dy)
    
    # Clamp t to segment [0, 1]
    t = max(0, min(1, t))
    
    # Closest point
    closest_x = ax + t * dx
    closest_y = ay + t * dy
    
    return (closest_x, closest_y)

def find_nearest_edge_point(graph, target_point):
    best_point = None
    min_dist = float('inf')
    best_edge = None
    
    # Check all edges (undirected)
    for u, v, data in graph.edges(data=True):
        # Get start/end coords of edge
        # Nodes in graph are (lat, lon)
        proj = project_point_onto_segment(target_point, u, v)
        dist = haversine_distance(target_point, proj)
        
        if dist < min_dist:
            min_dist = dist
            best_point = proj
            best_edge = (u, v)
            
    return best_point, best_edge, min_dist

# Router Class Mock behavior
class EnhancedRouter:
    def __init__(self):
        self.graph = nx.Graph()
        # Mock Graph: Line A -- B -- C
        self.graph.add_edge((0, 0), (0, 10), weight=1000) # Edge 1
        self.graph.add_edge((0, 10), (0, 20), weight=1000) # Edge 2
        
    def find_path(self, start, end):
        G = self.graph.copy()
        
        # 1. Snap Start
        s_proj, s_edge, _ = find_nearest_edge_point(G, start)
        s_node = start # Use actual start as node? Or proj?
        # User wants "from selected point" so use start.
        # But we connect start -> proj. And proj connects to edge endpoints.
        
        G.add_node(start)
        
        if s_edge:
            u, v = s_edge
            # Calculate dists
            d_s_u = haversine_distance(start, u) # Direct? Or via proj?
            # Geometry: Start -> Proj -> U/V
            # But wait, if Proj is "on the line", Proj->U + Proj->V = dist(U,V) (approx)
            
            # Add Proj Node?
            # Or just edges Start->U and Start->V?
            # If we just add Start->U and Start->V with proper weights, Dijkstra handles it?
            # Weight(Start, U) should be dist(Start, U).
            # This is simpler. We don't need the projection point IN the graph unless we want the path to visually bend there.
            # Visual bend is nicer.
            # Let's add Proj node.
            
            G.add_node(s_proj)
            G.add_edge(start, s_proj, weight=haversine_distance(start, s_proj))
            G.add_edge(s_proj, u, weight=haversine_distance(s_proj, u))
            G.add_edge(s_proj, v, weight=haversine_distance(s_proj, v))
            
        # 2. Snap End
        e_proj, e_edge, _ = find_nearest_edge_point(G, end)
        G.add_node(end)
        
        if e_edge:
            u, v = e_edge
            G.add_node(e_proj)
            G.add_edge(end, e_proj, weight=haversine_distance(end, e_proj))
            G.add_edge(e_proj, u, weight=haversine_distance(e_proj, u))
            G.add_edge(e_proj, v, weight=haversine_distance(e_proj, v))
            
        try:
            path = nx.dijkstra_path(G, start, end, weight='weight')
            return path
        except:
            return []

if __name__ == "__main__":
    router = EnhancedRouter()
    # User at (0, 5) which is midday on first edge
    # Dest at (0, 15) midday on second edge
    path = router.find_path((0, 5), (0, 15))
    print("Path:", path)
    # Expected: (0,5) -> (0,5)_proj -> (0,10) -> (0,15)_proj -> (0,15)
