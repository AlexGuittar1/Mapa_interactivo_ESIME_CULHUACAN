"""
ARCHIVO: app.py

Este archivo define la aplicación Flask principal. Configura la base de datos,
inicializa los servicios globales, expone los puntos de enlace de la API 
(Rutas, Autenticación, Estacionamiento, Edificios, etc.) y orquesta la 
interacción general entre el cliente frontend y el backend en Python.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from models import db, EdificioDB, CaminoDB, Alumno, Grupo, Horario, Inscripcion, MateriaGrupo, SavedPlace, ParkingSpace, ParkingReservation, ParkingHistory, ParkingSection
from config import get_config
from repositories import create_user_repository, create_schedule_repository
from services.auth_service import AuthService
from services.schedule_service import ScheduleService

from datetime import datetime
import time
import random

# CONFIGURACION DE APLICACION
config = get_config()
app = Flask(__name__)
CORS(app)

app.config["SQLALCHEMY_DATABASE_URI"] = config.SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = config.SQLALCHEMY_TRACK_MODIFICATIONS
app.config["SECRET_KEY"] = config.SECRET_KEY

db.init_app(app)

from kml_router import KMLRouter
import os

# SERVICIOS GLOBALES
# (Declarados globalmente para ser accesibles tras el contexto de la aplicación)
user_repo = None
schedule_repo = None
auth_service = None
schedule_service = None

# VARIABLES GLOBALES DE NAVEGACION
grafo = None
kml_router = None

def init_system():
    """
    INICIALIZAR SISTEMA
    
    Crea las tablas de la base de datos si no existen, instancía repositorios,
    servicios de negocio y el enrutador KML para cálculos geográficos.
    """
    global grafo, kml_router, user_repo, schedule_repo, auth_service, schedule_service
    with app.app_context():
        db.create_all()

        # Instanciar repositorios y servicios de autenticación y academia
        user_repo = create_user_repository(config)
        schedule_repo = create_schedule_repository(config)
        auth_service = AuthService(user_repo, getattr(config, 'AUTH_PROVIDER', 'local'))
        schedule_service = ScheduleService(schedule_repo, user_repo)
        print(f"[CONFIG] Entorno: {config.ENV_NAME} | Auth: {getattr(config, 'AUTH_PROVIDER', 'local')} | Data: {config.DATA_PROVIDER}")

        # Inicializar enrutador topológico KML
        try:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            kml_path = os.path.join(base_dir, "..", "Camino ESIME caminable.kml")
            kml_router = KMLRouter(kml_path)
            print(f"[KML] Graph loaded with {len(kml_router.graph.nodes)} nodes")
        except Exception as e:
            print(f"[KML] Error loading: {e}")

init_system()

@app.route("/api/route", methods=["POST"])
def get_route():
    """
    OBTENER RUTA
    
    Endpoint que responde peticiones de enrutamiento punto a punto.
    Espera coordenadas de origen y destino en el cuerpo JSON.
    Devuelve la ruta más corta y una estimación de tiempo a pie.
    """
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
        "path": path, # Formato matricial: [[lat, lon], ...]
        "distance": distance, # Métrica dada en metros
        "eta_minutes": round(distance / 83.3, 1) # Promedio paso peatonal: ~5 km/h (83.3 m/min)
    })

@app.route("/auth/check-email", methods=["POST"])
def check_email():
    """
    VERIFICAR CORREO
    
    Consulta si la cuenta de correo provista ya existe en la base de datos.
    Emulsión del flujo de autenticación paso-a-paso.
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
    
    Endpoint dedicado a popular los recuadros faltantes en el esquema relacional
    cuando un usuario es autenticado vía Azure y le faltan datos institucionales (ej: boleta).
    """
    data = request.get_json()
    # Asignación de un grupo aleatorio para fines de demostración cuando ocurre registro manual
    grupo = Grupo.query.order_by(db.func.random()).first()
    create_data = {
        'boleta': data.get('boleta'),
        'nombre': data.get('nombre'),
        'email': data.get('email'),
        'carrera': data.get('carrera', 'Ingeniería'),
        'vehiculo': data.get('vehiculo', 'ninguno'),
        'id_grupo': grupo.id if grupo else None,
    }
    user, error = auth_service.complete_profile(create_data)
    if error:
        return jsonify({"error": error}), 400
    return jsonify(user), 201

@app.route("/auth/register", methods=["POST"])
def register():
    """
    REGISTRO GENERICO DE USUARIOS
    
    Función que registra una cuenta manual a través de esquemas por defecto.
    Se inyecta grupo pseudoaleatorio en un entorno simulado de registro institucional.
    """
    data = request.get_json()
    grupo = Grupo.query.order_by(db.func.random()).first()
    create_data = {
        'boleta': data.get('boleta'),
        'nombre': data.get('nombre'),
        'carrera': data.get('carrera'),
        'vehiculo': data.get('vehiculo', 'ninguno'),
        'id_grupo': grupo.id if grupo else None,
    }
    user, error = auth_service.register(create_data)
    if error:
        return jsonify({"error": error}), 400
    return jsonify(user), 201

@app.route("/auth/login", methods=["POST"])
def login():
    """
    INICIO DE SESION MANUAL
    
    Autenticación tradicional evaluando credenciales de control (boleta/clave) directos en hash nativo.
    """
    data = request.get_json()
    user, error = auth_service.login(data)
    if error:
        return jsonify({"error": error}), 404
    return jsonify(user), 200

# ACCESO MEDIANTE DIRECTORIO ACTIVO AZURE 
@app.route("/auth/azure-login", methods=["POST"])
def azure_login():
    """
    INICIO DE SESION AZURE AD
    
    Valida un token emitido por Azure Active Directory local para usuarios institucionales reales.
    Utiliza el header HTTP provisto con clave portadora (Bearer token).
    """
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer '):
        return jsonify({"error": "Se requiere token Bearer de Azure AD"}), 401
    
    token = auth_header.split(' ', 1)[1]
    user, error = auth_service.login({'azure_token': token})
    if error:
        return jsonify({"error": error}), 401
    return jsonify(user), 200

# PUNTOS DE ENLACE GENERALES

@app.route("/api/parking", methods=["GET"])
def get_parking():
    """
    OBTENER ESTACIONAMIENTOS ACTIVOS
    
    Recupera el listado completo de los espacios en uso a partir del modelo ParkingSpace.
    """
    # Usar ParkingSpace por eliminación de esquemas anteriores obsoletos
    spaces = ParkingSpace.query.all()
    return jsonify([s.to_dict() for s in spaces]), 200

@app.route("/api/user/<boleta>/schedule", methods=["GET"])
def get_schedule(boleta):
    """
    OBTENER HORARIO DIARIO
    
    Despliega el panel de clases del día activo, consultando el horario enlazado a la boleta.
    """
    horarios, error = schedule_service.get_today_schedule(boleta)
    if error:
        return jsonify({"error": error}), 404
    return jsonify(horarios), 200

@app.route("/api/buildings", methods=["GET"])
def get_buildings():
    """
    OBTENER EDIFICIOS
    
    Desencadena el inventario físico de infraestructuras base disponibles.
    """
    edificios = EdificioDB.query.all()
    return jsonify([e.to_dict() for e in edificios]), 200

@app.route("/api/user/<boleta>", methods=["PUT"])
def update_user(boleta):
    """
    ACTUALIZAR USUARIO
    
    Gestiona cambios de perfil (vehículo de transporte, correo, o estatus de carrera) del alumno.
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
    
    Múltiple propósito:
    [GET] Devuelve las coordenadas preferidas de un estudiante asociado al token o URL.
    [POST] Guarda un punto de interés nuevo y permanente dentro de su perfil activo.
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
    
    Erradica de la base de datos el lugar personalizado por el identificador proveído.
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
    
    Reescribe información parcial (nombre, tipo o coordenadas) del registro indicado temporal o permanentemente.
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
    
    Actualiza el archivo estático JSON frontal que sirve de manifiesto rápido geoespacial.
    """
    data = request.get_json()
    import json
    import os
    
    # Ruta natural al archivo de configuraciones topológicas del cliente
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
    
    Subsistema que edita en disco la inicialización visual que dibuja el cliente al cargar.
    """
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
    """
    OBTENER SALONES POR EDIFICIO
    
    Retorna los espacios formativos en base al edificio. Actualmente mitigado por 
    la ausencia de relación estricta en base de datos tipo SQLite local.
    """
    # En este momento SQLite no vincula la llave foránea 'edificio_id' nativamente en Salon.
    # Por prevencion de caídas en el servidor de pruebas se extrae todo globalmente.
    from models import Salon
    salones = Salon.query.all()
    # Lógica artificial provisional hasta reconstruir jerarquías o usar PostgreSQL en nube:
    # Retornar una muestra estática simulando filtrado local.
    return jsonify([s.to_dict() for s in salones[:20]]), 200

# NAVEGACION

@app.route("/ruta", methods=["POST"])
def obtener_ruta():
    """
    CALCULAR RUTA ESTATICA / EVENTUAL
    
    Función de direccionamiento semántico legado. Permite enrutar especificando
    tipos de comandos inteligentes ("next_class") u orígenes nominales libres.
    """
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "Datos incompletos"}), 400

    # Refrescar caché del grafo y estado en hilo del cliente
    global grafo
    
    # NOTA TÉCNICA: "cargar_sistema()" fue una función anterior; ahora manejada globalmente.
    # Este bloque mantendrá su consistencia pasiva de compatibilidad si existiese, 
    # asumiendo validación local.
    
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
        if user:
            # Invocar al servicio estructural de calendarización en la agenda local
            dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
            dia_hoy = dias[datetime.now().weekday()]
            hora_ahora = datetime.now().strftime("%H:%M")
            horarios, _ = schedule_service.get_today_schedule(boleta)
            
            if horarios:
                # Localizar qué clase temporalmente tiene vigencia restante durante el bloque actual
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
             return jsonify({"error": "No se encontraron clases próximas para hoy"}), 404
        
        nodo_inicio = obtener_nodo_mas_cercano(lat, lon)

    else:
        # Ruta convencional calculada basándose textualmente en la petición del dispositivo
        nodo_inicio = data.get("origen")
        destino_nombre = data.get("destino")
        
        # Si el origen carece de identificador de área explícito, intentar inyectarlo por proximidad GPS
        if not nodo_inicio and "lat" in data and "lon" in data:
            nodo_inicio = obtener_nodo_mas_cercano(float(data["lat"]), float(data["lon"]))

    if not nodo_inicio or not destino_nombre:
        return jsonify({"error": "Origen o Destino no especificado"}), 400

    camino, costo = grafo.ruta_mas_corta(nodo_inicio, destino_nombre)
    
    if not nodo_inicio:
        return jsonify({"error": "No se pudo determinar el punto de inicio"}), 404

    camino, costo = grafo.ruta_mas_corta(nodo_inicio, destino_nombre)
    
    if not camino:
        # Solución in-situ de contingencia: Un vínculo rectilíneo simple asumiendo una deficiencia del grafo maestro.
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
    
    Realiza una búsqueda secuencial y simple comparando los edificios 
    físicos definidos previamente. Útil para determinar en qué edificio
    está posicionado actualmente un visitante perdido.
    """
    closest = None
    min_dist = float('inf')
    edificios = EdificioDB.query.all()
    for edificio in edificios:
        # Distancia euclidiana burda pero rápida, asumiendo plano recto local urbano
        d = (edificio.latitud - lat)**2 + (edificio.longitud - lon)**2
        if d < min_dist:
            min_dist = d
            closest = edificio.nombre
    return closest

# PUNTOS DE ENLACE OBSOLETOS O EXISTENTES A REVISAR

@app.route("/edificios", methods=["POST"])
def crear_edificio():
    """Mantiene compatibilidad con herramientas heredadas externas, si las hay."""
    pass

# MÓDULO DE ESTACIONAMIENTO AVANZADO

from datetime import datetime, timedelta

def check_expired_reservations():
    """
    VERIFICAR RESERVAS VENCIDAS
    
    Libera automáticamente del sistema las reservas caducadas por el motor de tiempo temporal,
    y registra históricamente la acción ("expire") dentro de la bitácora transaccional.
    """
    now = datetime.now()
    try:
        expired_spaces = ParkingSpace.query.filter(
            ParkingSpace.status == 'reserved',
            ParkingSpace.reservation_expires_at != None,
            ParkingSpace.reservation_expires_at < now
        ).all()
        
        for space in expired_spaces:
            history = ParkingHistory(
                space_id=space.id,
                user_boleta=space.reserved_by,
                action='expire',
                previous_status='reserved',
                new_status='available',
                timestamp=now
            )
            db.session.add(history)
            
            space.status = 'available'
            space.reserved_by = None
            space.reserved_at = None
            space.reservation_expires_at = None
            
        if expired_spaces:
            db.session.commit()
    except Exception as e:
        print(f"Error checking expirations: {e}")

@app.route("/api/parking/spaces", methods=["GET"])
def get_parking_spaces():
    """
    OBTENER ESPACIOS DE ESTACIONAMIENTO GRUPALES
    
    Devuelve un compendio con la totalidad de los lugares de estacionamiento
    estructuradamente clasificados sobre su respectiva sección física o bahía.
    """
    check_expired_reservations()
    try:
        sections = ParkingSection.query.order_by(ParkingSection.id).all()
        spaces = ParkingSpace.query.all()
        
        result_sections = []
        for sec in sections:
            sec_spaces = [s for s in spaces if s.section_id == sec.id]
            
            # Ordenamos los espacios subyacentes por metadato identificador ascendente ("space_number")
            sec_spaces.sort(key=lambda x: x.id)
            
            sec_total = sec.total_spaces
            sec_available = sum(1 for s in sec_spaces if s.status == 'available')
            sec_occupied = sum(1 for s in sec_spaces if s.status == 'occupied')
            sec_reserved = sum(1 for s in sec_spaces if s.status == 'reserved')
            
            result_sections.append({
                "id": sec.id,
                "name": sec.name,
                "total_spaces": sec_total,
                "map_image_url": sec.map_image_url,
                "stats": {
                    "available": sec_available,
                    "occupied": sec_occupied,
                    "reserved": sec_reserved
                },
                "spaces": [s.to_dict() for s in sec_spaces]
            })
            
        total_spaces = sum(s.total_spaces for s in sections)
        available = sum(1 for s in spaces if s.status == 'available')
        occupied = sum(1 for s in spaces if s.status == 'occupied')
        reserved = sum(1 for s in spaces if s.status == 'reserved')
        
        return jsonify({
            "total": total_spaces,
            "available": available,
            "occupied": occupied,
            "reserved": reserved,
            "sections": result_sections
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/parking/spaces/<int:space_id>", methods=["GET"])
def get_parking_space(space_id):
    """
    OBTENER METADATOS DE ESPACIO INDIVIDUAL
    
    Provee la información microscópica y el estatus general (disponible, reservado, ocupado)
    para un cuadrante singular determinado por su ID base.
    """
    check_expired_reservations()
    try:
        space = ParkingSpace.query.get(space_id)
        if not space:
            return jsonify({"error": "Espacio no encontrado"}), 404
        
        return jsonify(space.to_dict()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/parking/spaces/<int:space_id>/status", methods=["PUT"])
def update_parking_space_status(space_id):
    """
    ACTUALIZAR ESTADO DE ESPACIO DE ESTACIONAMIENTO
    
    Intercambia la disponibilidad de una bahía local acatando rigurosamente
    las validaciones operativas perimetrales y protecciones contra denegación de ocupación múltiple.
    """
    check_expired_reservations()
    try:
        data = request.json
        new_status = data.get('status')
        user_boleta = data.get('user_boleta')
        
        if not user_boleta:
            return jsonify({"error": "Falta la identificación del usuario (user_boleta)"}), 400
            
        if new_status not in ['available', 'occupied', 'reserved']:
            return jsonify({"error": "Estado inválido"}), 400

        space = ParkingSpace.query.get(space_id)
        if not space:
            return jsonify({"error": "Espacio no encontrado"}), 404
            
        now = datetime.now()
        previous_status = space.status

        # REGLA 1: RESERVA DE CUBICULO ('reserved')
        if new_status == 'reserved':
            if space.status != 'available':
                return jsonify({"error": "El espacio no está disponible"}), 400
                
            # Validar límite anti-monopolio: El usuario ya posee reserva activa o auto validado?
            active_usage = ParkingSpace.query.filter(
                ((ParkingSpace.status == 'reserved') & (ParkingSpace.reserved_by == user_boleta)) |
                ((ParkingSpace.status == 'occupied') & (ParkingSpace.occupied_by == user_boleta))
            ).first()
            if active_usage:
                text = "reserva activa" if active_usage.status == 'reserved' else "coche estacionado"
                return jsonify({"error": f"Ya tienes un(a) {text} en el espacio {active_usage.space_number}"}), 403
                
            # Validar congelamiento post-cancelación temporal (Cooldown 1 hora)
            one_hour_ago = now - timedelta(hours=1)
            cooldown = ParkingHistory.query.filter(
                ParkingHistory.space_id == space_id,
                ParkingHistory.user_boleta == user_boleta,
                ParkingHistory.action == 'free',
                ParkingHistory.timestamp >= one_hour_ago
            ).first()
            if cooldown:
                return jsonify({"error": "Por políticas anti-monopolio, debes esperar 1 hora para reservar este mismo lugar nuevamente."}), 403
                
            space.status = 'reserved'
            space.reserved_by = user_boleta
            space.reserved_at = now
            space.reservation_expires_at = now + timedelta(minutes=10)
            
            history = ParkingHistory(space_id=space.id, user_boleta=user_boleta, action='reserve', previous_status=previous_status, new_status=new_status, timestamp=now)
            db.session.add(history)

        # REGLA 2: OCUPACION PERMANENTE ('occupied')
        elif new_status == 'occupied':
            if space.status == 'occupied':
                return jsonify({"error": "El espacio ya está ocupado"}), 400
            if space.status == 'reserved' and space.reserved_by != user_boleta:
                return jsonify({"error": "El espacio está reservado por alguien más."}), 403
                
            # Consumo o migración legítima desde estado 'available' o 'reserved' propio
            space.status = 'occupied'
            space.occupied_by = user_boleta
            space.occupied_at = now
            space.reserved_by = None
            space.reserved_at = None
            space.reservation_expires_at = None
            
            history = ParkingHistory(space_id=space.id, user_boleta=user_boleta, action='occupy', previous_status=previous_status, new_status=new_status, timestamp=now)
            db.session.add(history)

        # REGLA 3: LIBERACION DE ESPACIO ('available')
        elif new_status == 'available':
            if space.status == 'available':
                return jsonify({"error": "El espacio ya está libre"}), 400
            
            # El actor solicitante de la liberación debe mantener titularidad formal del candado
            if space.status == 'occupied' and space.occupied_by != user_boleta:
                return jsonify({"error": "No puedes liberar un espacio ajeno"}), 403
            if space.status == 'reserved' and space.reserved_by != user_boleta:
                return jsonify({"error": "No puedes liberar la reserva de alguien más"}), 403
            
            space.status = 'available'
            space.occupied_by = None
            space.occupied_at = None
            space.reserved_by = None
            space.reserved_at = None
            space.reservation_expires_at = None
            
            history = ParkingHistory(space_id=space.id, user_boleta=user_boleta, action='free', previous_status=previous_status, new_status=new_status, timestamp=now)
            db.session.add(history)
        
        db.session.commit()
        return jsonify(space.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@app.route("/api/parking/stats", methods=["GET"])
def get_parking_stats():
    """
    OBTENER ESTADISTICAS DEL ESTACIONAMIENTO DE TIPO MACRO
    
    Genera un panel numérico procesado en vivo que inyecta métricas cruzadas, 
    tasas de ocupación e historiales matemáticos a los monitores para ser leídos.
    """
    try:
        total = ParkingSpace.query.count()
        available = ParkingSpace.query.filter_by(status='available').count()
        occupied = ParkingSpace.query.filter_by(status='occupied').count()
        reserved = ParkingSpace.query.filter_by(status='reserved').count()
        
        sections = {}
        all_sections = ParkingSection.query.all()
        for sec in all_sections:
            section_name = sec.name
            section_total = sec.total_spaces
            section_available = ParkingSpace.query.filter_by(section_id=sec.id, status='available').count()
            section_occupied = ParkingSpace.query.filter_by(section_id=sec.id, status='occupied').count()
            section_reserved = ParkingSpace.query.filter_by(section_id=sec.id, status='reserved').count()
            
            sections[section_name] = {
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
