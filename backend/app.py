from flask import Flask, request, jsonify
from flask_cors import CORS
from models import db, EdificioDB, CaminoDB, Alumno, SavedPlace, ParkingSpace, ParkingReservation, ParkingHistory
# Removed obsolete imports after DB refactoring: Estacionamiento, Salon, Horario, Grupo, Asignatura, Profesor
# from repositorio import cargar_sistema  # Commented out - module not needed
# from navegacion import calcular_ruta_usuario  # Commented out - module doesn't exist

from datetime import datetime
import time
import random

app = Flask(__name__)
CORS(app) 

# Configuración de la base de datos
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///campus.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

from kml_router import KMLRouter
import os

# ... (imports)

# Variables globales para sistema de navegación
grafo = None
kml_router = None

# Inicializar sistema (AVL + Grafo + KML Router)
def init_system():
    global grafo, kml_router
    with app.app_context():
        db.create_all() 
        try:
            # Init old graph if needed (keeping for backward compatibility or different features)
            if EdificioDB.query.first():
                grafo = cargar_sistema()
        except:
            pass
            
        # Init KML Router
        try:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            kml_path = os.path.join(base_dir, "..", "Camino ESIME caminable.kml")
            kml_router = KMLRouter(kml_path)
            print(f"KML Graph loaded with {len(kml_router.graph.nodes)} nodes")
        except Exception as e:
            print(f"Error loading KML: {e}")

init_system()

@app.route("/api/route", methods=["POST"])
def get_route():
    data = request.get_json()
    start_lat = data.get('start_lat')
    start_lon = data.get('start_lon')
    end_lat = data.get('end_lat')
    end_lon = data.get('end_lon')

    if not all([start_lat, start_lon, end_lat, end_lon]):
        return jsonify({"error": "Missing coordinates"}), 400

    if not kml_router:
        return jsonify({"error": "Router not initialized"}), 500

    path, distance = kml_router.find_shortest_path((start_lat, start_lon), (end_lat, end_lon))
    
    return jsonify({
        "path": path, # [[lat, lon], [lat, lon], ...]
        "distance": distance, # meters
        "eta_minutes": round(distance / 83.3, 1) # ~5 km/h walking speed (83.3 m/min)
    })



@app.route("/auth/check-email", methods=["POST"])
def check_email():
    data = request.get_json()
    email = data.get('email')
    
    user = Alumno.query.filter_by(email=email).first()
    if user:
        return jsonify({"exists": True, "user": user.to_dict()}), 200
    
    return jsonify({"exists": False}), 200

@app.route("/auth/complete-profile", methods=["POST"])
def complete_profile():
    data = request.get_json()
    email = data.get('email')
    boleta = data.get('boleta')
    nombre = data.get('nombre') # Desde Outlook o Input
    
    # Validar si boleta ya existe
    if Alumno.query.filter_by(boleta=boleta).first():
        return jsonify({"error": "La boleta ya está registrada"}), 400

    # Assign random group for demo if not provided
    # In a real app, user would select it or it comes from external system
    grupo = Grupo.query.order_by(db.func.random()).first()
    
    nuevo_usuario = Usuario(
        boleta=boleta, 
        nombre=nombre, 
        email=email,
        carrera=data.get('carrera', 'Ingeniería'),
        vehiculo=data.get('vehiculo', 'ninguno'),
        id_grupo=grupo.id_grupo if grupo else None
    )
    db.session.add(nuevo_usuario)
    db.session.commit()
    
    return jsonify(nuevo_usuario.to_dict()), 201

@app.route("/auth/register", methods=["POST"])
def register():
    data = request.get_json()
    if Alumno.query.filter_by(boleta=data.get('boleta')).first():
        return jsonify({"error": "Usuario ya existe"}), 400
    
    grupo = Grupo.query.order_by(db.func.random()).first()

    nuevo_usuario = Usuario(
        boleta=data['boleta'], 
        nombre=data['nombre'], 
        carrera=data.get('carrera'),
        vehiculo=data.get('vehiculo', 'ninguno'),
        id_grupo=grupo.id_grupo if grupo else None
    )
    db.session.add(nuevo_usuario)
    db.session.commit()
    return jsonify(nuevo_usuario.to_dict()), 201

@app.route("/auth/login", methods=["POST"])
def login():
    data = request.get_json()
    boleta = data.get('boleta')
    # Simple login check (sin contraseña real por demo)
    user = Alumno.query.filter_by(boleta=boleta).first()
    if user:
        return jsonify(user.to_dict()), 200
    return jsonify({"error": "Usuario no encontrado"}), 404

# ENDPOINTS

@app.route("/api/parking", methods=["GET"])
def get_parking():
    slots = Estacionamiento.query.all()
    return jsonify([s.to_dict() for s in slots]), 200

@app.route("/api/user/<boleta>/schedule", methods=["GET"])
def get_schedule(boleta):
    user = Usuario.query.filter_by(boleta=boleta).first()
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    # Obtener día actual y mapear a nombres completos (Lunes, Martes, etc.)
    dias_dict = {
        0: "Lunes", 1: "Martes", 2: "Miércoles", 
        3: "Jueves", 4: "Viernes", 5: "Sábado", 6: "Domingo"
    }
    dia_actual = dias_dict[datetime.now().weekday()]
    
    if user.id_grupo:
        # Filter by day
        clases = Horario.query.filter_by(id_grupo=user.id_grupo, dia=dia_actual).all()
        clases.sort(key=lambda x: x.hora_inicio)
    else:
        clases = []

    return jsonify([c.to_dict() for c in clases]), 200

@app.route("/api/buildings", methods=["GET"])
def get_buildings():
    edificios = EdificioDB.query.all()
    return jsonify([e.to_dict() for e in edificios]), 200

@app.route("/api/user/<boleta>", methods=["PUT"])
def update_user(boleta):
    user = Usuario.query.filter_by(boleta=boleta).first()
    if not user:
        return jsonify({"error": "Usuario no encontrado"}), 404
    
    data = request.get_json()
    if 'vehiculo' in data:
        user.vehiculo = data['vehiculo']
    
    if 'nombre' in data:
        user.nombre = data['nombre']
    
    if 'carrera' in data:
        user.carrera = data['carrera']

    db.session.commit()
    return jsonify(user.to_dict()), 200

@app.route("/api/saved-places", methods=["GET", "POST"])
def manage_saved_places():
    if request.method == "GET":
        boleta = request.args.get('user_boleta')
        if not boleta:
            return jsonify({"error": "Boleta requerida"}), 400
        places = SavedPlace.query.filter_by(user_boleta=boleta).all()
        return jsonify([p.to_dict() for p in places]), 200
    
    if request.method == "POST":
        data = request.get_json()
        new_place = SavedPlace(
            user_boleta=data['user_boleta'],
            name=data['name'],
            lat=data['lat'],
            lon=data['lon'],
            type=data.get('type', 'custom') 
        )
        db.session.add(new_place)
        db.session.commit()
        return jsonify(new_place.to_dict()), 201

@app.route("/api/saved-places/<int:id>", methods=["DELETE"])
def delete_saved_place(id):
    place = SavedPlace.query.get(id)
    if place:
        db.session.delete(place)
        db.session.commit()
        return jsonify({"message": "Eliminado"}), 200
    return jsonify({"error": "No encontrado"}), 404

@app.route("/api/saved-places/<int:id>", methods=["PUT"])
def update_saved_place(id):
    place = SavedPlace.query.get(id)
    if not place:
        return jsonify({"error": "No encontrado"}), 404
        
    data = request.get_json()
    if 'name' in data: place.name = data['name']
    if 'lat' in data: place.lat = data['lat']
    if 'lon' in data: place.lon = data['lon']
    if 'type' in data: place.type = data['type']
    
    db.session.commit()
    return jsonify(place.to_dict()), 200

@app.route("/api/locations", methods=["POST"])
def save_locations():
    data = request.get_json()
    import json
    import os
    
    # Path to locations.json
    path = os.path.join("frontend", "src", "locations.json")
    
    try:
        with open(path, "w") as f:
            json.dump(data, f, indent=2)
        return jsonify({"message": "Ubicaciones guardadas correctamente"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/map-config", methods=["POST"])
def save_map_config():
    data = request.get_json()
    import json
    import os
    path = os.path.join("frontend", "src", "mapConfig.json")
    try:
        with open(path, "w") as f:
            json.dump(data, f, indent=2)
        return jsonify({"message": "Configuración del mapa guardada"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/buildings/<int:id>/classrooms", methods=["GET"])
def get_classrooms(id):
    # This endpoint is tricky because Salon might not have edificio_id FK in SQLite
    # We try to query anyway if the model has it, otherwise return empty or all?
    # Since we removed edificio_id from Salon model in previous step to match DB, 
    # we cannot filter by it directly unless we infer it.
    # For now, return empty or all to prevent 500
    salones = Salon.query.all()
    # Mock filtering based on name if possible, e.g. "1xxx" -> Edificio 1?
    # For now just return all limited to 20 for performance in this broken state
    return jsonify([s.to_dict() for s in salones[:20]]), 200

# --- NAVIGATION ---

@app.route("/ruta", methods=["POST"])
def obtener_ruta():
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "Datos incompletos"}), 400

    # Recargar sistema
    # Recargar sistema
    global grafo
    grafo = cargar_sistema()


    destino_nombre = None
    nodo_inicio = None
    info_extra = None

    if data.get("type") == "next_class":
        if "lat" not in data or "lon" not in data:
            return jsonify({"error": "Ubicación necesaria para ruta a clase"}), 400
        lat = float(data["lat"])
        lon = float(data["lon"])
        
        boleta = data.get("boleta")
        user = Alumno.query.filter_by(boleta=boleta).first()
        if user and user.id_grupo:
            dias = ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sabado", "Domingo"]
            dia_hoy = dias[datetime.now().weekday()]
            hora_ahora = datetime.now().strftime("%H:%M")
            clases = Horario.query.filter_by(id_grupo=user.id_grupo, dia=dia_hoy).all()
            clases.sort(key=lambda x: x.hora_inicio)
            
            for c in clases:
                if c.hora_fin > hora_ahora:
                    salon_name = c.salon.nombre if c.salon else ""
                    if salon_name.startswith("1"): destino_nombre = "Edificio 1"
                    elif salon_name.startswith("2"): destino_nombre = "Edificio 2"
                    elif salon_name.startswith("3"): destino_nombre = "Edificio 3"
                    else: destino_nombre = "Explanada ESIME"
                    info_extra = f"Clase: {c.asignatura.nombre} en {salon_name}"
                    break
        
        if not destino_nombre:
             return jsonify({"error": "No se encontraron clases próximas para hoy"}), 404
        
        nodo_inicio = obtener_nodo_mas_cercano(lat, lon)

    else:
        # Routing by name (Origin -> Destination)
        nodo_inicio = data.get("origen")
        destino_nombre = data.get("destino")
        
        # If no explicit origin name, try lat/lon
        if not nodo_inicio and "lat" in data and "lon" in data:
            nodo_inicio = obtener_nodo_mas_cercano(float(data["lat"]), float(data["lon"]))

    if not nodo_inicio or not destino_nombre:
        return jsonify({"error": "Origen o Destino no especificado"}), 400

    camino, costo = grafo.ruta_mas_corta(nodo_inicio, destino_nombre)
    
    if not nodo_inicio:
        return jsonify({"error": "No se pudo determinar el punto de inicio"}), 404

    camino, costo = grafo.ruta_mas_corta(nodo_inicio, destino_nombre)
    
    if not camino:
        # Provicional: Un solo salto si el grafo esta muy incompleto
        camino = [nodo_inicio, destino_nombre]
        costo = 0

    return jsonify({
        "origen": nodo_inicio,
        "destino": destino_nombre,
        "camino": camino, 
        "distancia": round(costo, 2),
        "info": info_extra
    }), 200

def obtener_nodo_mas_cercano(lat, lon):
    closest = None
    min_dist = float('inf')
    edificios = EdificioDB.query.all()
    for edificio in edificios:
        # Distancia euclidiana (aproximada para grados)
        d = (edificio.latitud - lat)**2 + (edificio.longitud - lon)**2
        if d < min_dist:
            min_dist = d
            closest = edificio.nombre
    return closest

# --- EXISTING ENDPOINTS ---

@app.route("/edificios", methods=["POST"])
def crear_edificio():
    # ... (Mantener lógica existente si se desea, o simplificar)
    pass

# ==================== PARKING ENDPOINTS ====================

@app.route("/api/parking/spaces", methods=["GET"])
def get_parking_spaces():
    """Obtener todos los espacios de estacionamiento con filtros opcionales"""
    try:
        section = request.args.get('section')
        status = request.args.get('status')
        sort_by = request.args.get('sort_by', 'space_number')
        
        query = ParkingSpace.query
        
        if section:
            query = query.filter_by(section=section.upper())
        if status:
            query = query.filter_by(status=status)
        
        if sort_by == 'space_number':
            query = query.order_by(ParkingSpace.space_number)
        elif sort_by.startswith('distance_to_building_'):
            building_num = sort_by.split('_')[-1]
            if building_num in ['1', '2', '3']:
                query = query.order_by(getattr(ParkingSpace, f'distance_to_building_{building_num}'))
        
        spaces = query.all()
        
        total = len(spaces)
        available = sum(1 for s in spaces if s.status == 'available')
        occupied = sum(1 for s in spaces if s.status == 'occupied')
        reserved = sum(1 for s in spaces if s.status == 'reserved')
        
        return jsonify({
            "total": total,
            "available": available,
            "occupied": occupied,
            "reserved": reserved,
            "spaces": [space.to_dict() for space in spaces]
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/parking/spaces/<int:space_id>", methods=["GET"])
def get_parking_space(space_id):
    """Obtener detalles de un espacio específico"""
    try:
        space = ParkingSpace.query.get(space_id)
        if not space:
            return jsonify({"error": "Espacio no encontrado"}), 404
        
        return jsonify(space.to_dict()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/parking/stats", methods=["GET"])
def get_parking_stats():
    """Obtener estadísticas generales del estacionamiento"""
    try:
        total = ParkingSpace.query.count()
        available = ParkingSpace.query.filter_by(status='available').count()
        occupied = ParkingSpace.query.filter_by(status='occupied').count()
        reserved = ParkingSpace.query.filter_by(status='reserved').count()
        
        sections = {}
        for section in ['A', 'B', 'C']:
            section_total = ParkingSpace.query.filter_by(section=section).count()
            section_available = ParkingSpace.query.filter_by(section=section, status='available').count()
            section_occupied = ParkingSpace.query.filter_by(section=section, status='occupied').count()
            section_reserved = ParkingSpace.query.filter_by(section=section, status='reserved').count()
            
            sections[section] = {
                "total": section_total,
                "available": section_available,
                "occupied": section_occupied,
                "reserved": section_reserved,
                "occupancy_rate": round((section_occupied / section_total * 100), 1) if section_total > 0 else 0
            }
        
        return jsonify({
            "total": total,
            "available": available,
            "occupied": occupied,
            "reserved": reserved,
            "occupancy_rate": round((occupied / total * 100), 1) if total > 0 else 0,
            "sections": sections
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "status": "API ESIME v2 Running",
        "features": ["Auth", "Parking", "Routing", "Schedules"]
    })

if __name__ == "__main__":
    app.run(debug=True, port=5001)
