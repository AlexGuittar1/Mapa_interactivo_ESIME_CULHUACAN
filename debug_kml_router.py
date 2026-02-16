import sys
import os

# Add backend directory to sys.path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

try:
    from kml_router import KMLRouter
except ImportError:
    print("Could not import KMLRouter. Make sure you are running from project root.")
    sys.exit(1)

def test_kml_loading():
    base_dir = os.path.join(os.getcwd(), 'backend')
    kml_path = os.path.join(base_dir, "..", "Camino ESIME caminable")
    
    print(f"Testing KML path: {kml_path}")
    print(f"Path exists: {os.path.exists(kml_path)}")
    
    try:
        router = KMLRouter(kml_path)
        print(f"Success! Graph has {len(router.graph.nodes)} nodes and {len(router.graph.edges)} edges.")
    except Exception as e:
        print(f"ERROR initializing KMLRouter: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_kml_loading()
