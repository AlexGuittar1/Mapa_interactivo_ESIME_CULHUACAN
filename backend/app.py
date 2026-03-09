"""
ARCHIVO: app.py

APLICACION PRINCIPAL FLASK

Este archivo define la aplicacion Flask principal. Configura las bases de datos
(mapa e institucional), inicializa los servicios globales, expone los endpoints
de la API y orquesta la interaccion entre el frontend y el backend.

ARQUITECTURA DUAL DE BASES DE DATOS:
  - MAP (map.db): Edificios, rutas, estacionamiento, lugares guardados
  - SCHOOL (school.db): Alumnos, materias, horarios, inscripciones

El sistema funciona en dos modos:
  - standalone: Solo usa la base de datos del mapa (para demo)
  - institutional: Usa ambas bases de datos (para produccion)
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from models import db, EdificioDB, CaminoDB, Alumno, Grupo, Horario, Inscripcion, MateriaGrupo, SavedPlace, ParkingSpace, ParkingReservation, ParkingHistory, ParkingSection
from config import get_config
from repositories import create_user_repository, create_schedule_repository
from services.auth_service import AuthService
from services.schedule_service import ScheduleService
from services.routing_service import RoutingService
from services.parking_service import ParkingService
from services.school_adapter import create_school_adapter

from datetime import datetime, timedelta
import time
import random
import os

# CONFIGURACION DE APLICACION
config = get_config()
app = Flask(__name__)
CORS(app)

# RATE LIMITER: Proteccion contra fuerza bruta
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=[],  # Sin limite global (solo en endpoints especificos)
    storage_uri="memory://"
)

# CONFIGURACION DE BASES DE DATOS DUALES
app.config["SQLALCHEMY_DATABASE_URI"] = config.SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_BINDS"] = config.SQLALCHEMY_BINDS
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = config.SQLALCHEMY_TRACK_MODIFICATIONS
app.config["SECRET_KEY"] = config.SECRET_KEY

db.init_app(app)

# SERVICIOS GLOBALES
user_repo = None
schedule_repo = None
auth_service = None
schedule_service = None

# INSTANCIAS DE SERVICIOS DE MAPA
routing_service = RoutingService()
parking_service = ParkingService()
school_adapter = None

# VARIABLES GLOBALES DE NAVEGACION (compatibilidad con sistema legado)
grafo = None
kml_router = None


def init_system():
    """
    INICIALIZAR SISTEMA

    Crea las tablas de ambas bases de datos si no existen,
    migra datos desde campus.db si school.db esta vacia,
    instancia repositorios, servicios de negocio, ejecuta el seed
    del mapa y carga el enrutador KML.
    """
    global grafo, kml_router, user_repo, schedule_repo, auth_service, schedule_service, school_adapter

    with app.app_context():
        # Crear tablas en ambas bases de datos
        db.create_all()

        # Ejecutar seed de datos del mapa (solo si las tablas estan vacias)
        from seed_map_data import seed_all
        seed_all(db)

        # Auto-migrar datos de campus.db a school.db si school esta vacia
        from models import Alumno
        alumno_count = Alumno.query.count()
        if alumno_count == 0:
            print("[MIGRACION] school.db vacia, intentando migrar desde campus.db...")
            try:
                from migrate_campus_to_school import migrate
                migrate()
            except Exception as e:
                print(f"[MIGRACION] No se pudo migrar: {e}")
                print("[MIGRACION] Ejecuta manualmente: python3 migrate_campus_to_school.py")

        # Instanciar repositorios y servicios
        user_repo = create_user_repository(config)
        schedule_repo = create_schedule_repository(config)
        auth_service = AuthService(user_repo, getattr(config, 'AUTH_PROVIDER', 'local'))
        schedule_service = ScheduleService(schedule_repo, user_repo)
        school_adapter = create_school_adapter(config)

        # Inicializar servicio de enrutamiento
        routing_service.initialize()
        kml_router = routing_service.kml_router

        # LOGS DE DIAGNOSTICO
        from models import EdificioDB, ParkingSpace, ParkingSection, Inscripcion
        app_mode = getattr(config, 'APP_MODE', 'standalone')
        print(f"\n[CONFIG] Entorno: {config.ENV_NAME} | Modo: {app_mode} | Auth: {getattr(config, 'AUTH_PROVIDER', 'local')} | Data: {config.DATA_PROVIDER}")
        print(f"[CONFIG] MAP DB: {config.MAP_DATABASE_URL}")
        print(f"[CONFIG] SCHOOL DB: {config.SCHOOL_DATABASE_URL}")
        print(f"[MAP DB] Edificios: {EdificioDB.query.count()}")
        print(f"[MAP DB] Secciones estacionamiento: {ParkingSection.query.count()}")
        print(f"[MAP DB] Espacios estacionamiento: {ParkingSpace.query.count()}")
        print(f"[SCHOOL DB] Alumnos: {Alumno.query.count()}")
        print(f"[SCHOOL DB] Inscripciones: {Inscripcion.query.count()}")
        print("")

init_system()


# ENDPOINTS DE ENRUTAMIENTO


@app.route("/api/route", methods=["POST"])
def get_route():
    """
    OBTENER RUTA

    Calcula la ruta mas corta entre dos coordenadas GPS.
    Espera coordenadas de origen y destino en el cuerpo JSON.
    """
    data = request.get_json()
    start_lat = data.get('start_lat')
    start_lon = data.get('start_lon')
    end_lat = data.get('end_lat')
    end_lon = data.get('end_lon')

    if not all([start_lat, start_lon, end_lat, end_lon]):
        return jsonify({"error": "Missing coordinates"}), 400

    result = routing_service.calculate_route(start_lat, start_lon, end_lat, end_lon)
    if result is None:
        return jsonify({"error": "Router not initialized"}), 500

    return jsonify(result)


# ENDPOINTS DE AUTENTICACION


@app.route("/auth/check-email", methods=["POST"])
def check_email():
    """
    VERIFICAR CORREO

    Consulta si la cuenta de correo proporcionada ya existe en la base de datos.
    """
    data = request.get_json()
    email = data.get('email')
    user, exists = auth_service.check_email(email)
    if exists:
        return jsonify({"exists": True, "user": user}), 200
    return jsonify({"exists": False}), 200


@app.route("/auth/complete-profile", methods=["POST"])
def complete_profile():
    """
    COMPLETAR PERFIL DEL USUARIO

    Completa los datos faltantes cuando un usuario se autentica via Azure.
    """
    data = request.get_json()
    grupo = Grupo.query.order_by(db.func.random()).first()
    create_data = {
        'boleta': data.get('boleta'),
        'nombre': data.get('nombre'),
        'email': data.get('email'),
        'carrera': data.get('carrera', 'Ingenieria'),
        'vehiculo': data.get('vehiculo', 'ninguno'),
        'id_grupo': grupo.id if grupo else None,
    }
    user, error = auth_service.complete_profile(create_data)
    if error:
        return jsonify({"error": error}), 400
    return jsonify(user), 201


@app.route("/auth/register", methods=["POST"])
@limiter.limit("3 per minute")
def register():
    """
    REGISTRO DE USUARIOS

    Registra una cuenta nueva con datos basicos.
    """
    data = request.get_json()
    grupo = Grupo.query.order_by(db.func.random()).first()
    create_data = {
        'boleta': data.get('boleta'),
        'nombre': data.get('nombre'),
        'password': data.get('password'),
        'carrera': data.get('carrera'),
        'vehiculo': data.get('vehiculo', 'ninguno'),
        'id_grupo': grupo.id if grupo else None,
    }
    user, error = auth_service.register(create_data)
    if error:
        return jsonify({"error": error}), 400
    return jsonify(user), 201


@app.route("/auth/login", methods=["POST"])
@limiter.limit("5 per minute")
def login():
    """
    INICIO DE SESION SEGURO

    Autenticacion por numero de boleta + contrasena.
    Rate limited: maximo 5 intentos por minuto por IP.
    """
    data = request.get_json()
    user, error = auth_service.login(data)
    if error:
        return jsonify({"error": error}), 401
    return jsonify(user), 200


@app.route("/auth/set-password", methods=["POST"])
@limiter.limit("3 per minute")
def set_password():
    """
    ESTABLECER CONTRASENA PARA USUARIOS MIGRADOS

    Permite a usuarios existentes que no tienen contrasena crear una.
    """
    data = request.get_json()
    boleta = data.get('boleta')
    password = data.get('password')
    user, error = auth_service.set_password(boleta, password)
    if error:
        return jsonify({"error": error}), 400
    return jsonify(user), 200


@app.route("/auth/azure-login", methods=["POST"])
def azure_login():
    """
    INICIO DE SESION AZURE AD

    Valida un token emitido por Azure Active Directory.
    """
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer '):
        return jsonify({"error": "Se requiere token Bearer de Azure AD"}), 401

    token = auth_header.split(' ', 1)[1]
    user, error = auth_service.login({'azure_token': token})
    if error:
        return jsonify({"error": error}), 401
    return jsonify(user), 200


# ENDPOINTS GENERALES


@app.route("/api/parking", methods=["GET"])
def get_parking():
    """
    OBTENER ESTACIONAMIENTOS

    Devuelve la lista completa de espacios de estacionamiento.
    """
    spaces = ParkingSpace.query.all()
    return jsonify([s.to_dict() for s in spaces]), 200


@app.route("/api/user/<boleta>/schedule", methods=["GET"])
def get_schedule(boleta):
    """
    OBTENER HORARIO DIARIO

    Devuelve las clases del dia actual para la boleta dada.
    """
    horarios, error = schedule_service.get_today_schedule(boleta)
    if error:
        return jsonify({"error": error}), 404
    return jsonify(horarios), 200


@app.route("/api/buildings", methods=["GET"])
def get_buildings():
    """
    OBTENER EDIFICIOS

    Devuelve la lista de edificios del campus.
    """
    edificios = EdificioDB.query.all()
    return jsonify([e.to_dict() for e in edificios]), 200


@app.route("/api/user/<boleta>", methods=["PUT"])
def update_user(boleta):
    """
    ACTUALIZAR USUARIO

    Modifica datos del perfil del alumno.
    """
    data = request.get_json()
    user, error = auth_service.update_user(boleta, data)
    if error:
        return jsonify({"error": error}), 404
    return jsonify(user), 200


@app.route("/api/saved-places", methods=["GET", "POST"])
def manage_saved_places():
    """
    ADMINISTRAR LUGARES GUARDADOS

    GET: Devuelve los lugares guardados de un usuario.
    POST: Guarda un nuevo punto de interes.
    """
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
    """
    BORRAR LUGAR GUARDADO
    """
    place = SavedPlace.query.get(id)
    if place:
        db.session.delete(place)
        db.session.commit()
        return jsonify({"message": "Eliminado"}), 200
    return jsonify({"error": "No encontrado"}), 404


@app.route("/api/saved-places/<int:id>", methods=["PUT"])
def update_saved_place(id):
    """
    ACTUALIZAR LUGAR GUARDADO
    """
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
    """
    GUARDAR UBICACIONES GEOGRAFICAS ESTATICAS
    """
    data = request.get_json()
    import json

    path = os.path.join("frontend", "src", "locations.json")

    try:
        with open(path, "w") as f:
            json.dump(data, f, indent=2)
        return jsonify({"message": "Ubicaciones guardadas correctamente"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/map-config", methods=["POST"])
def save_map_config():
    """
    GUARDAR CONFIGURACION DE MAPA
    """
    data = request.get_json()
    import json

    path = os.path.join("frontend", "src", "mapConfig.json")
    try:
        with open(path, "w") as f:
            json.dump(data, f, indent=2)
        return jsonify({"message": "Configuracion del mapa guardada"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/buildings/<int:id>/classrooms", methods=["GET"])
def get_classrooms(id):
    """
    OBTENER SALONES POR EDIFICIO
    """
    from models import Salon
    salones = Salon.query.all()
    return jsonify([s.to_dict() for s in salones[:20]]), 200


# NAVEGACION LEGADA


@app.route("/ruta", methods=["POST"])
def obtener_ruta():
    """
    CALCULAR RUTA (SISTEMA LEGADO)

    Permite enrutar especificando comandos inteligentes u origenes nominales.
    """
    data = request.get_json()

    if not data:
        return jsonify({"error": "Datos incompletos"}), 400

    global grafo

    destino_nombre = None
    nodo_inicio = None
    info_extra = None

    if data.get("type") == "next_class":
        if "lat" not in data or "lon" not in data:
            return jsonify({"error": "Ubicacion necesaria para ruta a clase"}), 400
        lat = float(data["lat"])
        lon = float(data["lon"])

        boleta = data.get("boleta")
        user = Alumno.query.filter_by(boleta=boleta).first()
        if user:
            dias = ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sabado", "Domingo"]
            dia_hoy = dias[datetime.now().weekday()]
            hora_ahora = datetime.now().strftime("%H:%M")
            horarios, _ = schedule_service.get_today_schedule(boleta)

            if horarios:
                for h in horarios:
                    if h.get('hora_fin', '') > hora_ahora:
                        salon_name = h.get('salon', '') or ''
                        if salon_name.startswith("1"): destino_nombre = "Edificio 1"
                        elif salon_name.startswith("2"): destino_nombre = "Edificio 2"
                        elif salon_name.startswith("3"): destino_nombre = "Edificio 3"
                        else: destino_nombre = "Explanada ESIME"
                        info_extra = f"Clase: {h.get('materia', '')} en {salon_name}"
                        break

        if not destino_nombre:
            return jsonify({"error": "No se encontraron clases proximas para hoy"}), 404

        nodo_inicio = obtener_nodo_mas_cercano(lat, lon)

    else:
        nodo_inicio = data.get("origen")
        destino_nombre = data.get("destino")

        if not nodo_inicio and "lat" in data and "lon" in data:
            nodo_inicio = obtener_nodo_mas_cercano(float(data["lat"]), float(data["lon"]))

    if not nodo_inicio or not destino_nombre:
        return jsonify({"error": "Origen o Destino no especificado"}), 400

    camino, costo = grafo.ruta_mas_corta(nodo_inicio, destino_nombre)

    if not camino:
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
    """
    OBTENER AREA CERCANA POR COORDENADAS

    Busca el edificio mas cercano a las coordenadas dadas.
    """
    closest = None
    min_dist = float('inf')
    edificios = EdificioDB.query.all()
    for edificio in edificios:
        d = (edificio.latitud - lat) ** 2 + (edificio.longitud - lon) ** 2
        if d < min_dist:
            min_dist = d
            closest = edificio.nombre
    return closest


# ENDPOINTS DE ESTACIONAMIENTO (USANDO SERVICIO)


@app.route("/edificios", methods=["POST"])
def crear_edificio():
    """Mantiene compatibilidad con herramientas heredadas."""
    pass


@app.route("/api/parking/spaces", methods=["GET"])
def get_parking_spaces():
    """
    OBTENER ESPACIOS DE ESTACIONAMIENTO

    Devuelve todos los espacios agrupados por seccion con estadisticas.
    """
    try:
        result = parking_service.get_all_spaces()
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/parking/spaces/<int:space_id>", methods=["GET"])
def get_parking_space(space_id):
    """
    OBTENER ESPACIO INDIVIDUAL
    """
    try:
        space = parking_service.get_space(space_id)
        if not space:
            return jsonify({"error": "Espacio no encontrado"}), 404
        return jsonify(space.to_dict()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/parking/spaces/<int:space_id>/status", methods=["PUT"])
def update_parking_space_status(space_id):
    """
    ACTUALIZAR ESTADO DE ESPACIO DE ESTACIONAMIENTO
    """
    try:
        data = request.json
        new_status = data.get('status')
        user_boleta = data.get('user_boleta')
        user_lat = data.get('user_lat')
        user_lng = data.get('user_lng')

        success, result, status_code = parking_service.update_space_status(
            space_id, new_status, user_boleta,
            user_lat=user_lat, user_lng=user_lng
        )

        if success:
            return jsonify(result), status_code
        else:
            return jsonify({"error": result}), status_code

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@app.route("/api/parking/stats", methods=["GET"])
def get_parking_stats():
    """
    OBTENER ESTADISTICAS DEL ESTACIONAMIENTO
    """
    try:
        stats = parking_service.get_stats()
        return jsonify(stats), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ENDPOINT RAIZ


@app.route("/", methods=["GET"])
def home():
    mode = getattr(config, 'APP_MODE', 'standalone')
    return jsonify({
        "status": "API ESIME v3 Running",
        "mode": mode,
        "features": ["Auth", "Parking", "Routing", "Schedules", "DualDB"]
    })


if __name__ == "__main__":
    app.run(debug=True, port=5001)
