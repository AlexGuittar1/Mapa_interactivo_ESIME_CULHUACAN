import sys
import os
import networkx as nx

# Add current directory to path so we can import KMLRouter
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from kml_router import KMLRouter

# Initialize router
kml_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "Camino ESIME caminable.kml")
router = KMLRouter(kml_path)

print(f"Graph loaded: {len(router.graph.nodes)} nodes, {len(router.graph.edges)} edges")

pts = {
    "Entrada": (19.328499550519272, -99.11288827657701),
    "Gimnasio": (19.330855214041132, -99.11059902641019),
    "Cafeteria": (19.32942843594261, -99.11115020513536),
    "Edificio 2 (Lado Cafeteria)": (19.329223423537776, -99.11153912544252)
}

test_cases = [
    ("Entrada", "Gimnasio"),
    ("Entrada", "Cafeteria"),
    ("Entrada", "Edificio 2 (Lado Cafeteria)")
]

import json

for origin_name, dest_name in test_cases:
    origin = pts[origin_name]
    dest = pts[dest_name]
    
    # 1. Snap End
    def project_point(p, a, b):
        px, py = p
        ax, ay = a
        bx, by = b
        dx, dy = bx - ax, by - ay
        if dx == 0 and dy == 0: return a
        t = ((px - ax) * dx + (py - ay) * dy) / (dx*dx + dy*dy)
        t = max(0, min(1, t))
        return (ax + t * dx, ay + t * dy)

    # Helper to find nearest edge point
    def get_nearest_edge_point(target_point):
        best_point = None
        min_dist = float('inf')
        best_edge = None
        
        for u, v, data in router.graph.edges(data=True):
            proj = project_point(target_point, u, v)
            
            # Local haversine inline
            import math
            R = 6371000
            lat1, lon1 = math.radians(target_point[0]), math.radians(target_point[1])
            lat2, lon2 = math.radians(proj[0]), math.radians(proj[1])
            dlat = lat2 - lat1
            dlon = lon2 - lon1
            a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
            c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
            dist = R * c

            if dist < min_dist:
                min_dist = dist
                best_point = proj
                best_edge = (u, v)
        return best_point, best_edge, min_dist

    if origin_name == "Entrada" and dest_name == "Edificio 2 (Lado Cafeteria)":
        print(f"\n[DEBUG] Snapping for {dest_name}:")
        proj, edge, dist = get_nearest_edge_point(dest)
        print(f"Nearest edge: {edge}")
        print(f"Projection point: {proj}")
        print(f"Distance to edge: {dist:.2f}m")

    # Inject projection into router graph to test exact Dijkstra path
    proj, edge, _ = get_nearest_edge_point(dest)
    s_proj, s_edge, _ = get_nearest_edge_point(origin)
    
    # Temporarily add nodes/edges to graph for pure Dijkstra
    router.graph.add_node(origin)
    router.graph.add_node(dest)
    
    import math
    def dist(a,b):
        R = 6371000
        lat1, lon1 = math.radians(a[0]), math.radians(a[1])
        lat2, lon2 = math.radians(b[0]), math.radians(b[1])
        c = 2 * math.atan2(math.sqrt(math.sin((lat2-lat1)/2)**2 + math.cos(lat1)*math.cos(lat2)*math.sin((lon2-lon1)/2)**2), math.sqrt(1 - (math.sin((lat2-lat1)/2)**2 + math.cos(lat1)*math.cos(lat2)*math.sin((lon2-lon1)/2)**2)))
        return R * c

    # Assume we snap correctly (ignoring exact projection point logic to avoid edge splits, just link to nearest graph nodes directly for debug)
    u_d, v_d = edge
    router.graph.add_edge(dest, u_d, weight=dist(dest, u_d))
    router.graph.add_edge(dest, v_d, weight=dist(dest, v_d))
    
    u_s, v_s = s_edge
    router.graph.add_edge(origin, u_s, weight=dist(origin, u_s))
    router.graph.add_edge(origin, v_s, weight=dist(origin, v_s))
    
    try:
        raw_path = nx.dijkstra_path(router.graph, origin, dest, weight='weight')
        raw_dist = nx.dijkstra_path_length(router.graph, origin, dest, weight='weight')
        print(f"\n--- Unsimplified Route: {origin_name} -> {dest_name} ---")
        print(f"Nodes in Dijkstra: {len(raw_path)}")
        print(f"Total distance: {raw_dist:.2f} meters")
        if dest_name == "Edificio 2 (Lado Cafeteria)":
            print(json.dumps(raw_path, indent=2))
    except BaseException as e:
        print(e)
        
    router.graph.remove_node(origin)
    router.graph.remove_node(dest)
        
# Let's inspect weights and connectivity
print(f"\nIs graph connected? {nx.is_connected(router.graph)}")
if not nx.is_connected(router.graph):
        components = list(nx.connected_components(router.graph))
        print(f"Number of connected components: {len(components)}")
        sizes = [len(c) for c in components]
        print(f"Component sizes: {sizes}")

from collections import deque

print("\n[DEBUG] Snapping for GYM ENTRANCE vs GYM BUILDING:")
gim_bldg_coord = (19.33075215181887, -99.11175370216371)
gim_ent_coord = (19.330711655889946, -99.11205142736436)

proj_gim_bldg, _, dist_bldg = get_nearest_edge_point(gim_bldg_coord)
proj_gim_ent, _, dist_ent = get_nearest_edge_point(gim_ent_coord)

print(f"Gimnasio Building snaps {dist_bldg:.2f}m away to: {proj_gim_bldg}")
print(f"Gimnasio Entrance snaps {dist_ent:.2f}m away to: {proj_gim_ent}")

try:
    p_bldg_cafe, d_bldg_cafe = router.find_shortest_path(proj_gim_bldg, pts["Cafeteria"])
    print(f"Distance from Gimnasio BUILDING to Cafeteria: {d_bldg_cafe:.1f}m")
except BaseException as e: print(e)

try:
    p_ent_cafe, d_ent_cafe = router.find_shortest_path(proj_gim_ent, pts["Cafeteria"])
    print(f"Distance from Gimnasio ENTRANCE to Cafeteria: {d_ent_cafe:.1f}m")
except BaseException as e: print(e)
