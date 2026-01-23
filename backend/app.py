from flask import Flask, request, jsonify
from flask_cors import CORS
from models import db, EdificioDB, CaminoDB, Usuario, Salon, Horario, Estacionamiento, Grupo, Asignatura, Profesor
from repositorio import cargar_sistema

from datetime import datetime
import time
import random

app = Flask(__name__)
CORS(app) # Enable CORS for Frontend

# Configuración de la base de datos
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///campus.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

# Variables globales para sistema de navegación
grafo = None


# Inicializar sistema (AVL + Grafo)
def init_system():
    global grafo
    with app.app_context():
        # db.create_all() # Schema already exists
        # Verificar si hay edificios antes de cargar, si no, esperar a poblar
        try:
             if EdificioDB.query.first():
                grafo = cargar_sistema()
        except:
             pass


init_system()

# --- AUTH ---

@app.route("/auth/check-email", methods=["POST"])
def check_email():
    data = request.get_json()
    email = data.get('email')
    
    user = Usuario.query.filter_by(email=email).first()
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
    if Usuario.query.filter_by(boleta=boleta).first():
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
    if Usuario.query.filter_by(boleta=data.get('boleta')).first():
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
    user = Usuario.query.filter_by(boleta=boleta).first()
    if user:
        return jsonify(user.to_dict()), 200
    return jsonify({"error": "Usuario no encontrado"}), 404

# --- DATA ENDPOINTS ---

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
        user = Usuario.query.filter_by(boleta=boleta).first()
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

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "status": "API ESIME v2 Running",
        "features": ["Auth", "Parking", "Routing", "Schedules"]
    })

if __name__ == "__main__":
    app.run(debug=True, port=5001)
