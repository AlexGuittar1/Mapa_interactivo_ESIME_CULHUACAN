
import sys
import os
import networkx as nx
import math

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

try:
    from kml_router import KMLRouter, haversine_distance
except ImportError:
    # Quick mock of haversine if import fails (standalone run)
    def haversine_distance(coord1, coord2):
        R = 6371000
        lat1, lon1 = math.radians(coord1[0]), math.radians(coord1[1])
        lat2, lon2 = math.radians(coord2[0]), math.radians(coord2[1])
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return R * c

    # We need to manually parse KML if we can't import KMLRouter properly 
    # But usually sys.path append works.
    pass

def project_point_onto_segment(p, a, b):
    # p, a, b are (lat, lon)
    px, py = p
    ax, ay = a
    bx, by = b
    dx, dy = bx - ax, by - ay
    if dx == 0 and dy == 0:
        return a
    
    t = ((px - ax) * dx + (py - ay) * dy) / (dx*dx + dy*dy)
    t = max(0, min(1, t))
    
    return (ax + t * dx, ay + t * dy)

def check_topology():
    base_dir = os.path.join(os.getcwd(), 'backend')
    kml_path = os.path.join(base_dir, "..", "Camino ESIME caminable")
    
    # Init router with existing logic (no auto-fix yet)
    # We might need to copy the class processing logic if we want to test "raw" graph
    # But let's assume KMLRouter as is loads the graph.
    
    from kml_router import KMLRouter
    router = KMLRouter(kml_path)
    G = router.graph
    
    print(f"Graph loaded. Nodes: {len(G.nodes)}, Edges: {len(G.edges)}")
    
    close_passes = 0
    potential_fixes = []
    
    nodes = list(G.nodes)
    edges = list(G.edges)
    
    threshold_meters = 2.5 # Look for misaligned intersections within 2.5m
    
    print(f"Scanning for nodes within {threshold_meters}m of edges...")
    
    for node in nodes:
        for u, v in edges:
            if node == u or node == v:
                continue
                
            proj = project_point_onto_segment(node, u, v)
            dist = haversine_distance(node, proj)
            
            if dist < threshold_meters:
                # Found a potential missing connection
                close_passes += 1
                potential_fixes.append({
                    "node": node,
                    "edge": (u, v),
                    "dist": dist,
                    "proj": proj
                })
                # Print first few
                if close_passes <= 5:
                    print(f"WARN: Node {node} is {dist:.2f}m from Edge {u}-{v}")
                    
    print(f"Total potential disconnected T-junctions found: {close_passes}")

if __name__ == "__main__":
    check_topology()
