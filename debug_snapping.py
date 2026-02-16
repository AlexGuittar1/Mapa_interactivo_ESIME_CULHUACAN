import xml.etree.ElementTree as ET
import networkx as nx
import math
import os
import sys
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from kml_router import KMLRouter, haversine_distance

# Coordinates from key_points.json
points = {
    "Edificio 3 Lado de Cafeteria": (19.32971697148389, -99.11149889230731),
    "Cafeteria Principal": (19.32942843594261, -99.11115020513536)
}


try:
    router = KMLRouter("Camino ESIME caminable.kml")
    print(f"Graph loaded with {len(router.graph.nodes)} nodes")
    print(f"Graph connected? {nx.is_connected(router.graph)}")
    print(f"Number of connected components: {nx.number_connected_components(router.graph)}")

    snapped_nodes = []

    for name, coords in points.items():
        nearest_node = None
        min_dist = float('inf')
        
        for node in router.graph.nodes:
            dist = haversine_distance(coords, node)
            if dist < min_dist:
                min_dist = dist
                nearest_node = node
        
        snapped_nodes.append(nearest_node)
        print(f"Point '{name}':")
        print(f"  Coords: {coords}")
        print(f"  Nearest Node: {nearest_node}")
        print(f"  Distance: {min_dist:.2f} meters")

    if len(snapped_nodes) == 2 and snapped_nodes[0] and snapped_nodes[1]:
        u, v = snapped_nodes[0], snapped_nodes[1]
        has_path = nx.has_path(router.graph, u, v)
        print(f"Path exists between {u} and {v}? {has_path}")
        if not has_path:
             # Find which component they belong to
             c1 = next(iter([c for c in nx.connected_components(router.graph) if u in c]), None)
             c2 = next(iter([c for c in nx.connected_components(router.graph) if v in c]), None)
             print(f"Node 1 component size: {len(c1)}")
             print(f"Node 2 component size: {len(c2)}")

except Exception as e:
    print(f"Error: {e}")
