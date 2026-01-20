from flask import Flask, request, jsonify
from flask_cors import CORS
from models import db, EdificioDB, CaminoDB, Usuario, Salon, Horario, Estacionamiento
from repositorio import cargar_sistema
from navegacion import calcular_ruta_usuario
from edificio import Edificio
from datetime import datetime
import time

app = Flask(__name__)
CORS(app) # Enable CORS for Frontend

# Configuración de la base de datos
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///campus.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

# Variables globales para sistema de navegación
arbol = None
grafo = None

# Inicializar sistema (AVL + Grafo)
def init_system():
    global arbol, grafo
    with app.app_context():
        db.create_all()
        # Verificar si hay edificios antes de cargar, si no, esperar a poblar
        if EdificioDB.query.first():
            arbol, grafo = cargar_sistema()

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

    # Crear nuevo usuario
    nuevo_usuario = Usuario(
        boleta=boleta, 
        nombre=nombre, 
        email=email,
        carrera=data.get('carrera', 'Ingeniería'),
        vehiculo=data.get('vehiculo', 'ninguno')
    )
    db.session.add(nuevo_usuario)
    db.session.commit()
    
    return jsonify(nuevo_usuario.to_dict()), 201

@app.route("/auth/register", methods=["POST"])
def register():
    data = request.get_json()
    if Usuario.query.filter_by(boleta=data.get('boleta')).first():
        return jsonify({"error": "Usuario ya existe"}), 400
    
    nuevo_usuario = Usuario(
        boleta=data['boleta'], 
        nombre=data['nombre'], 
        carrera=data.get('carrera'),
        vehiculo=data.get('vehiculo', 'ninguno')
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
    
    # Obtener día actual
    dias = ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sabado", "Domingo"]
    dia_actual = dias[datetime.now().weekday()]
    
    clases = Horario.query.filter_by(usuario_id=user.id, dia=dia_actual).all()
    # Ordenar por hora
    clases.sort(key=lambda x: x.hora_inicio)
    
    return jsonify([c.to_dict() for c in clases]), 200

@app.route("/api/buildings", methods=["GET"])
def get_buildings():
    edificios = EdificioDB.query.all()
    return jsonify([e.to_dict() for e in edificios]), 200

@app.route("/api/buildings/<int:id>/classrooms", methods=["GET"])
def get_classrooms(id):
    salones = Salon.query.filter_by(edificio_id=id).all()
    return jsonify([s.to_dict() for s in salones]), 200

# --- NAVIGATION ---

@app.route("/ruta", methods=["POST"])
def obtener_ruta():
    data = request.get_json()
    
    if not data or "lat" not in data or "lon" not in data:
        return jsonify({"error": "Datos incompletos"}), 400

    lat = float(data["lat"])
    lon = float(data["lon"])
    
    # Recargar sistema si es necesario (por si se agregan cosas al vuelo)
    if arbol is None or grafo is None:
         init_system()

    # Si se pide "next_class", calcular destino
    destino_nombre = None
    if data.get("type") == "next_class":
        boleta = data.get("boleta")
        user = Usuario.query.filter_by(boleta=boleta).first()
        if user:
             # Lógica simplificada: Buscar primera clase futura hoy
             # DEMO: Retorna un salón fijo si no encuentra
             destino_nombre = "Edificio 1" 
    elif "destino" in data:
        destino_nombre = data["destino"]
    
    if not destino_nombre:
        # Por defecto calc ruta al edificio mas cercano si no hay destino? 
        return jsonify({"error": "Destino no especificado"}), 400

    # Usar la lógica existente de navegacion.py
    # Pero navegacion.py requiere un input de usuario de consola? 
    # Vamos a adaptar calcular_ruta_usuario para que acepte destino fijo
    
    # IMPORTANTE: Requerimos refactorizar navegacion.py o usar grafo directamente
    # Por ahora, usamos el grafo directamente si está disponible
    
    # Buscar nodo mas cercano a la lat/lon del usuario
    nodo_inicio = obtener_nodo_mas_cercano(lat, lon)
    
    camino, costo = grafo.ruta_mas_corta(nodo_inicio, destino_nombre)
    
    if not camino:
         return jsonify({"error": "No se encontró ruta"}), 404

    return jsonify({
        "origen": nodo_inicio,
        "destino": destino_nombre,
        "camino": camino, 
        "distancia": costo
    }), 200

def obtener_nodo_mas_cercano(lat, lon):
    # Mock simple: busca edificio con eurística de distancia menor
    closest = None
    min_dist = float('inf')
    for edificio in EdificioDB.query.all():
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
