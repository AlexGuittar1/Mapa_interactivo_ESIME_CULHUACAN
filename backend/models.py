from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class EdificioDB(db.Model):
    __tablename__ = "edificios"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), unique=True, nullable=False)
    latitud = db.Column(db.Float, nullable=False)
    longitud = db.Column(db.Float, nullable=False)

    def to_dict(self):
        return {"id": self.id, "nombre": self.nombre, "lat": self.latitud, "lon": self.longitud}

class CaminoDB(db.Model):
    __tablename__ = "caminos"
    id = db.Column(db.Integer, primary_key=True)
    origen = db.Column(db.String(50), nullable=False)
    destino = db.Column(db.String(50), nullable=False)
    distancia = db.Column(db.Float, nullable=False)

    def to_dict(self):
        return {"origen": self.origen, "destino": self.destino, "distancia": self.distancia}

class Usuario(db.Model):
    __tablename__ = "usuarios"
    id = db.Column(db.Integer, primary_key=True)
    boleta = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True)
    nombre = db.Column(db.String(100), nullable=False)
    carrera = db.Column(db.String(100))
    vehiculo = db.Column(db.String(20), default='ninguno')
    id_grupo = db.Column(db.Integer, db.ForeignKey('grupos.id_grupo')) 

    grupo = db.relationship('Grupo', backref=db.backref('alumnos', lazy=True))

    def to_dict(self):
        return {
            "boleta": self.boleta,
            "email": self.email,
            "nombre": self.nombre,
            "carrera": self.carrera,
            "vehiculo": self.vehiculo,
            "grupo": self.grupo.clave if self.grupo else None
        }

class Asignatura(db.Model):
    __tablename__ = "asignaturas"
    id_asignatura = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String, nullable=False)

class Grupo(db.Model):
    __tablename__ = "grupos"
    id_grupo = db.Column(db.Integer, primary_key=True)
    clave = db.Column(db.String, nullable=False) # e.g. 3CV12

class Profesor(db.Model):
    __tablename__ = "profesores"
    id_profesor = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String, nullable=False)

class Salon(db.Model):
    __tablename__ = "salones"
    id_salon = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(20), nullable=False)
    # Note: The database inspection showed id_salon but NOT edificio_id as a separate verified FK in PRAGMA, 
    # but the original code had it. We will assume mapping via name or we need to check if 'edificio_id' exists.
    # The 'inspect_db' output for salones only showed id_salon and nombre. 
    # We will infer building from name or need a mapping strategy if column is missing.
    # BUT wait, the original models had edificio_id. Let's assume the DB might NOT have it if it wasn't in 'inspect_db' output.
    # The inspect_db output for salones was: (0, 'id_salon', 'INTEGER'...), (1, 'nombre', 'TEXT'...)
    # So NO edificio_id column in actual DB currently? 
    # If so, we can't map it easily yet without modification or heuristics.
    # However, 'horarios' links everything.

class Horario(db.Model):
    __tablename__ = "horarios"
    id_horario = db.Column(db.Integer, primary_key=True)
    id_asignatura = db.Column(db.Integer, db.ForeignKey('asignaturas.id_asignatura'))
    id_grupo = db.Column(db.Integer, db.ForeignKey('grupos.id_grupo'))
    id_profesor = db.Column(db.Integer, db.ForeignKey('profesores.id_profesor'))
    id_salon = db.Column(db.Integer, db.ForeignKey('salones.id_salon'))
    dia = db.Column(db.String(15))
    hora_inicio = db.Column(db.String(10))
    hora_fin = db.Column(db.String(10))

    asignatura = db.relationship('Asignatura')
    grupo = db.relationship('Grupo')
    profesor = db.relationship('Profesor')
    salon = db.relationship('Salon')

    def to_dict(self):
        # Heuristic to infer building from salon name (e.g. "1101" -> "Edificio 1")
        salon_name = self.salon.nombre if self.salon else ""
        building_map = {"1": "Edificio 1", "2": "Edificio 2", "3": "Edificio 3"}
        inferred_building = building_map.get(salon_name[0], "Campus ESIME") if salon_name else "Desconocido"
        
        return {
            "materia": self.asignatura.nombre if self.asignatura else "Desconocida",
            "grupo": self.grupo.clave if self.grupo else "?",
            "profesor": self.profesor.nombre if self.profesor else "?",
            "sala": salon_name,
            "edificio": inferred_building,
            "dia": self.dia,
            "hora": f"{self.hora_inicio} - {self.hora_fin}"
        }

class Estacionamiento(db.Model):
    __tablename__ = "estacionamiento"
    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.String(10), unique=True)
    ocupado = db.Column(db.Boolean, default=False)
    latitud = db.Column(db.Float)
    longitud = db.Column(db.Float)
    tipo = db.Column(db.String(20), default='general')

    def to_dict(self):
        return {
            "id": self.id,
            "numero": self.numero,
            "ocupado": self.ocupado,
            "coords": [self.latitud, self.longitud],
            "tipo": self.tipo
        }

class SavedPlace(db.Model):
    __tablename__ = "saved_places"
    id = db.Column(db.Integer, primary_key=True)
    user_boleta = db.Column(db.String(20), db.ForeignKey('usuarios.boleta'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    lat = db.Column(db.Float, nullable=False)
    lon = db.Column(db.Float, nullable=False)
    type = db.Column(db.String(20), default='custom') # 'custom', 'favorite', etc.
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    user = db.relationship('Usuario', backref=db.backref('saved_places', lazy=True))

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "lat": self.lat,
            "lon": self.lon,
            "type": self.type,
            "user_boleta": self.user_boleta
        }

class ParkingSpace(db.Model):
    __tablename__ = "parking_spaces"
    id = db.Column(db.Integer, primary_key=True)
    space_number = db.Column(db.String(10), unique=True, nullable=False)  # e.g., "A-12"
    section = db.Column(db.String(5), nullable=False)  # "A", "B", "C"
    row_number = db.Column(db.Integer)
    position_number = db.Column(db.Integer)
    lat = db.Column(db.Float, nullable=False)
    lon = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='available')  # available, occupied, reserved
    occupied_by = db.Column(db.String(20), db.ForeignKey('usuarios.boleta'))
    occupied_at = db.Column(db.DateTime)
    reserved_by = db.Column(db.String(20), db.ForeignKey('usuarios.boleta'))
    reserved_at = db.Column(db.DateTime)
    reservation_expires_at = db.Column(db.DateTime)
    distance_to_building_1 = db.Column(db.Float)
    distance_to_building_2 = db.Column(db.Float)
    distance_to_building_3 = db.Column(db.Float)
    last_updated = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    # Relationships
    occupant = db.relationship('Usuario', foreign_keys=[occupied_by], backref=db.backref('occupied_spaces', lazy=True))
    reserver = db.relationship('Usuario', foreign_keys=[reserved_by], backref=db.backref('reserved_spaces', lazy=True))

    def to_dict(self):
        return {
            "id": self.id,
            "space_number": self.space_number,
            "section": self.section,
            "row": self.row_number,
            "position": self.position_number,
            "lat": self.lat,
            "lon": self.lon,
            "status": self.status,
            "occupied_by": self.occupied_by,
            "occupied_at": self.occupied_at.isoformat() if self.occupied_at else None,
            "reserved_by": self.reserved_by,
            "reserved_at": self.reserved_at.isoformat() if self.reserved_at else None,
            "reservation_expires_at": self.reservation_expires_at.isoformat() if self.reservation_expires_at else None,
            "distances": {
                "building_1": self.distance_to_building_1,
                "building_2": self.distance_to_building_2,
                "building_3": self.distance_to_building_3
            },
            "last_updated": self.last_updated.isoformat() if self.last_updated else None
        }

class ParkingReservation(db.Model):
    __tablename__ = "parking_reservations"
    id = db.Column(db.Integer, primary_key=True)
    space_id = db.Column(db.Integer, db.ForeignKey('parking_spaces.id'), nullable=False)
    user_boleta = db.Column(db.String(20), db.ForeignKey('usuarios.boleta'), nullable=False)
    reserved_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    expires_at = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), default='active')  # active, expired, cancelled, completed
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    # Relationships
    space = db.relationship('ParkingSpace', backref=db.backref('reservations', lazy=True))
    user = db.relationship('Usuario', backref=db.backref('parking_reservations', lazy=True))

    def to_dict(self):
        return {
            "id": self.id,
            "space_id": self.space_id,
            "space_number": self.space.space_number if self.space else None,
            "user_boleta": self.user_boleta,
            "reserved_at": self.reserved_at.isoformat() if self.reserved_at else None,
            "expires_at": self.expires_at.isoformat() if self.expires_at else None,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }

class ParkingHistory(db.Model):
    __tablename__ = "parking_history"
    id = db.Column(db.Integer, primary_key=True)
    space_id = db.Column(db.Integer, db.ForeignKey('parking_spaces.id'), nullable=False)
    user_boleta = db.Column(db.String(20))
    action = db.Column(db.String(20), nullable=False)  # occupy, vacate, reserve, cancel
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())

    # Relationships
    space = db.relationship('ParkingSpace', backref=db.backref('history', lazy=True))

    def to_dict(self):
        return {
            "id": self.id,
            "space_id": self.space_id,
            "space_number": self.space.space_number if self.space else None,
            "user_boleta": self.user_boleta,
            "action": self.action,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None
        }
