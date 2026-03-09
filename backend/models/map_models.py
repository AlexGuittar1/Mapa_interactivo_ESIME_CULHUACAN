"""
ARCHIVO: models/map_models.py

MODELOS DE DATOS DEL MAPA DEL CAMPUS

Define las tablas que almacenan informacion geografica del campus:
edificios, caminos, lugares guardados, secciones de estacionamiento,
espacios individuales, reservas e historial de estacionamiento.

Estos modelos pertenecen a la base de datos MAP (bind_key = 'map')
y son independientes de los datos institucionales de cualquier escuela.

Todos los modelos incluyen un campo campus_id para soporte multi-campus futuro.
"""

from models.database import db


# MODELOS DE NAVEGACION


class EdificioDB(db.Model):
    """
    MODELO EDIFICIO

    Representa un edificio fisico dentro del campus de la institucion,
    almacenando sus coordenadas geograficas para referenciarlo en el mapa.
    """
    __tablename__ = "edificios"
    __bind_key__ = "map"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    latitud = db.Column(db.Float, nullable=False)
    longitud = db.Column(db.Float, nullable=False)
    tipo = db.Column(db.String(50), default='academico')
    campus_id = db.Column(db.Integer, default=1)

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "lat": self.latitud,
            "lon": self.longitud,
            "tipo": self.tipo,
            "campus_id": self.campus_id
        }


class CaminoDB(db.Model):
    """
    MODELO CAMINO

    Representa un trayecto o ruta directa entre dos puntos topologicos,
    utilizada por el motor de enrutamiento para trazar caminos dentro del campus.
    """
    __tablename__ = "caminos"
    __bind_key__ = "map"

    id = db.Column(db.Integer, primary_key=True)
    origen = db.Column(db.String(50), nullable=False)
    destino = db.Column(db.String(50), nullable=False)
    distancia = db.Column(db.Float, nullable=False)
    campus_id = db.Column(db.Integer, default=1)

    def to_dict(self):
        return {
            "origen": self.origen,
            "destino": self.destino,
            "distancia": self.distancia,
            "campus_id": self.campus_id
        }


# MODELOS DE LUGARES GUARDADOS


class SavedPlace(db.Model):
    """
    MODELO LUGAR GUARDADO

    Permite al usuario conservar y nombrar un punto geografico
    de interes particular en el mapa de la escuela.

    NOTA: user_boleta es una referencia logica al alumno, no una FK real
    porque el alumno esta en otra base de datos (school). La integridad
    se valida a nivel de aplicacion.
    """
    __tablename__ = "saved_places"
    __bind_key__ = "map"

    id = db.Column(db.Integer, primary_key=True)
    user_boleta = db.Column(db.String(20), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    lat = db.Column(db.Float, nullable=False)
    lon = db.Column(db.Float, nullable=False)
    type = db.Column(db.String(20), default='custom')
    campus_id = db.Column(db.Integer, default=1)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "lat": self.lat,
            "lon": self.lon,
            "type": self.type,
            "user_boleta": self.user_boleta
        }


# MODELOS DE ESTACIONAMIENTO


class ParkingSection(db.Model):
    """
    MODELO SECCION DE ESTACIONAMIENTO

    Representa una region delimitada dentro del area del estacionamiento,
    agrupando logicamente un numero definido de lugares o cajones.
    """
    __tablename__ = "parking_sections"
    __bind_key__ = "map"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    total_spaces = db.Column(db.Integer, nullable=False)
    map_image_url = db.Column(db.String(255), nullable=True)
    campus_id = db.Column(db.Integer, default=1)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "total_spaces": self.total_spaces,
            "map_image_url": self.map_image_url,
            "campus_id": self.campus_id
        }


class ParkingSpace(db.Model):
    """
    MODELO ESPACIO DE ESTACIONAMIENTO

    Detalla la anatomia individual y el estado de cada cajon dentro
    del area de parqueo institucional.

    NOTA: occupied_by y reserved_by son referencias logicas a la boleta
    del alumno. No son FK reales porque el alumno vive en otra base de datos.
    La integridad se valida a nivel de aplicacion.
    """
    __tablename__ = "parking_spaces"
    __bind_key__ = "map"

    id = db.Column(db.Integer, primary_key=True)
    space_number = db.Column(db.String(10), unique=True, nullable=False)
    section_id = db.Column(db.Integer, db.ForeignKey('parking_sections.id'), nullable=False)
    row_number = db.Column(db.Integer)
    position_number = db.Column(db.Integer)
    lat = db.Column(db.Float, nullable=False)
    lon = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='available')
    occupied_by = db.Column(db.String(20))
    occupied_at = db.Column(db.DateTime)
    reserved_by = db.Column(db.String(20))
    reserved_at = db.Column(db.DateTime)
    reservation_expires_at = db.Column(db.DateTime)
    distance_to_building_1 = db.Column(db.Float)
    distance_to_building_2 = db.Column(db.Float)
    distance_to_building_3 = db.Column(db.Float)
    campus_id = db.Column(db.Integer, default=1)
    last_updated = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    # RELACIONES INTERNAS (misma base de datos MAP)
    section = db.relationship('ParkingSection', backref=db.backref('spaces', lazy=True))

    def to_dict(self):
        return {
            "id": self.id,
            "space_number": self.space_number,
            "section_id": self.section_id,
            "section_name": self.section.name if self.section else None,
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
    """
    MODELO RESERVA DE ESTACIONAMIENTO

    Gestiona el ciclo de vida, historial e integridad temporal de
    la retencion de un cajon asignado previamente via plataforma.
    """
    __tablename__ = "parking_reservations"
    __bind_key__ = "map"

    id = db.Column(db.Integer, primary_key=True)
    space_id = db.Column(db.Integer, db.ForeignKey('parking_spaces.id'), nullable=False)
    user_boleta = db.Column(db.String(20), nullable=False)
    reserved_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    expires_at = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), default='active')
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    # RELACIONES INTERNAS
    space = db.relationship('ParkingSpace', backref=db.backref('reservations', lazy=True))

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
    """
    MODELO HISTORIAL DE ESTACIONAMIENTO

    Registro tipo bitacora de la evolucion de estados
    (disponible, ocupado, reservado) que ocurren en los cajones.
    """
    __tablename__ = "parking_history"
    __bind_key__ = "map"

    id = db.Column(db.Integer, primary_key=True)
    space_id = db.Column(db.Integer, db.ForeignKey('parking_spaces.id'), nullable=False)
    user_boleta = db.Column(db.String(20))
    action = db.Column(db.String(20), nullable=False)
    previous_status = db.Column(db.String(20))
    new_status = db.Column(db.String(20))
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())

    # RELACIONES INTERNAS
    space = db.relationship('ParkingSpace', backref=db.backref('history', lazy=True))

    def to_dict(self):
        return {
            "id": self.id,
            "space_id": self.space_id,
            "space_number": self.space.space_number if self.space else None,
            "user_boleta": self.user_boleta,
            "action": self.action,
            "previous_status": self.previous_status,
            "new_status": self.new_status,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None
        }
