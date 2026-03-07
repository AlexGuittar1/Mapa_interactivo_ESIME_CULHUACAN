"""
ARCHIVO: models.py

Este archivo contiene la definición de todos los modelos de la base de datos
utilizando SQLAlchemy. Define la estructura, tipos de datos y relaciones 
entre entidades fundamentales como usuarios, horarios, rutas de navegación
y el sistema dinámico de estacionamiento.
"""

# IMPORTACIONES
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# MODELOS DE NAVEGACION

class EdificioDB(db.Model):
    """
    MODELO EDIFICIO
    
    Representa un edificio físico dentro del campus de la institución,
    almacenando sus coordenadas geográficas para referenciarlo en el mapa.
    """
    __tablename__ = "edificios"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), unique=True, nullable=False)
    latitud = db.Column(db.Float, nullable=False)
    longitud = db.Column(db.Float, nullable=False)

    def to_dict(self):
        return {"id": self.id, "nombre": self.nombre, "lat": self.latitud, "lon": self.longitud}

class CaminoDB(db.Model):
    """
    MODELO CAMINO
    
    Representa un trayecto o ruta directa entre dos puntos topológicos, 
    utilizada por el motor de enrutamiento para trazar caminos dentro del campus.
    """
    __tablename__ = "caminos"
    id = db.Column(db.Integer, primary_key=True)
    origen = db.Column(db.String(50), nullable=False)
    destino = db.Column(db.String(50), nullable=False)
    distancia = db.Column(db.Float, nullable=False)

    def to_dict(self):
        return {"origen": self.origen, "destino": self.destino, "distancia": self.distancia}

# MODELOS ACADEMICOS Y DE HORARIOS


class Alumno(db.Model):
    """
    MODELO ALUMNO
    
    Identidad principal del usuario dentro de la aplicación.
    Almacena datos personales, identificadores institucionales y mantiene
    las relaciones con inscripciones, reservas y configuraciones.
    """
    __tablename__ = "alumnos"
    id = db.Column(db.Integer, primary_key=True)
    boleta = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True)
    nombre = db.Column(db.String(100), nullable=False)
    carrera = db.Column(db.String(100))
    vehiculo = db.Column(db.String(20))
    id_grupo = db.Column(db.Integer, db.ForeignKey('grupos.id'))
    # CAMPOS DE INTEGRACION INSTITUCIONAL
    institutional_id = db.Column(db.String(100), unique=True, nullable=True)
    auth_provider = db.Column(db.String(20), default='local')
    last_login = db.Column(db.DateTime, nullable=True)
    is_synced = db.Column(db.Boolean, default=False)

    # RELACIONES
    inscripciones = db.relationship('Inscripcion', back_populates='alumno', lazy=True, cascade='all, delete-orphan')
    saved_places = db.relationship('SavedPlace', back_populates='user', lazy=True, cascade='all, delete-orphan')
    occupied_spaces = db.relationship('ParkingSpace', foreign_keys='ParkingSpace.occupied_by', back_populates='occupant', lazy=True)
    reserved_spaces = db.relationship('ParkingSpace', foreign_keys='ParkingSpace.reserved_by', back_populates='reserver', lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "boleta": self.boleta,
            "email": self.email,
            "nombre": self.nombre,
            "carrera": self.carrera,
            "vehiculo": self.vehiculo,
            "auth_provider": self.auth_provider,
        }

class Materia(db.Model):
    """
    MODELO MATERIA
    
    Define una asignatura curricular del plan de estudios.
    Contiene información propia del curso como valor de créditos y semestre.
    """
    __tablename__ = "materias"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(200), unique=True, nullable=False)
    codigo = db.Column(db.String(20), unique=True)
    creditos = db.Column(db.Integer)
    semestre = db.Column(db.Integer)

    # RELACIONES
    materias_grupos = db.relationship('MateriaGrupo', back_populates='materia', lazy=True, cascade='all, delete-orphan')

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "codigo": self.codigo,
            "creditos": self.creditos,
            "semestre": self.semestre
        }

class Profesor(db.Model):
    """
    MODELO PROFESOR
    
    Identidad del docente que imparte las materias, incluyendo datos de
    contacto e información administrativa como el departamento.
    """
    __tablename__ = "profesores"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(200), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True)
    departamento = db.Column(db.String(100))

    # RELACIONES
    materias_grupos = db.relationship('MateriaGrupo', back_populates='profesor', lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "email": self.email,
            "departamento": self.departamento
        }

class Salon(db.Model):
    """
    MODELO SALON
    
    Espacio físico destinado a la docencia. Permite asociar
    las clases a un lugar físico dentro del esquema de edificios,
    y establece propiedades operativas como capacidad o tipo de aula.
    """
    __tablename__ = "salones"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), unique=True, nullable=False)
    edificio_id = db.Column(db.Integer, db.ForeignKey('edificios.id'))
    capacidad = db.Column(db.Integer)
    tipo = db.Column(db.String(20))  # 'aula', 'laboratorio', 'auditorio'

    # RELACIONES
    edificio = db.relationship('EdificioDB', backref=db.backref('salones', lazy=True))
    horarios = db.relationship('Horario', back_populates='salon', lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "edificio_id": self.edificio_id,
            "edificio": self.edificio.nombre if self.edificio else None,
            "capacidad": self.capacidad,
            "tipo": self.tipo
        }

class Grupo(db.Model):
    """
    MODELO GRUPO
    
    Organización académica de un bloque de estudiantes. Define atributos
    agrupadores como semestre, turno, bloque de carrera y su identificador.
    """
    __tablename__ = "grupos"
    id = db.Column(db.Integer, primary_key=True)
    clave = db.Column(db.String(20), unique=True, nullable=False)  # ej: "1CM54", "3CV12"
    semestre = db.Column(db.Integer, nullable=False)
    turno = db.Column(db.String(20))  # 'matutino', 'vespertino', 'mixto'
    carrera = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    # RELACIONES
    materias_grupos = db.relationship('MateriaGrupo', back_populates='grupo', lazy=True, cascade='all, delete-orphan')

    def to_dict(self):
        return {
            "id": self.id,
            "clave": self.clave,
            "semestre": self.semestre,
            "turno": self.turno,
            "carrera": self.carrera
        }

class MateriaGrupo(db.Model):
    """
    MODELO MATERIA GRUPO
    
    Tabla relacional central que asocia una materia específica impartida
    a un grupo en particular, añadiendo el profesor a cargo y el ciclo.
    """
    __tablename__ = "materias_grupos"
    id = db.Column(db.Integer, primary_key=True)
    materia_id = db.Column(db.Integer, db.ForeignKey('materias.id'), nullable=False)
    grupo_id = db.Column(db.Integer, db.ForeignKey('grupos.id'), nullable=False)
    profesor_id = db.Column(db.Integer, db.ForeignKey('profesores.id'))
    ciclo_escolar = db.Column(db.String(20), nullable=False, default='2025-2026')

    # RELACIONES
    materia = db.relationship('Materia', back_populates='materias_grupos')
    grupo = db.relationship('Grupo', back_populates='materias_grupos')
    profesor = db.relationship('Profesor', back_populates='materias_grupos')
    horarios = db.relationship('Horario', back_populates='materia_grupo', lazy=True, cascade='all, delete-orphan')
    inscripciones = db.relationship('Inscripcion', back_populates='materia_grupo', lazy=True, cascade='all, delete-orphan')

    __table_args__ = (
        db.UniqueConstraint('materia_id', 'grupo_id', 'ciclo_escolar', name='uq_materia_grupo_ciclo'),
    )

    def to_dict(self):
        return {
            "id": self.id,
            "materia": self.materia.nombre if self.materia else None,
            "grupo": self.grupo.clave if self.grupo else None,
            "profesor": self.profesor.nombre if self.profesor else None,
            "ciclo_escolar": self.ciclo_escolar
        }

class Horario(db.Model):
    """
    MODELO HORARIO
    
    Estructura normalizada para los tiempos y días de la semana en
    los que se imparte una MateriaGrupo, en qué salón y bajo qué modalidad.
    """
    __tablename__ = "horarios"
    id = db.Column(db.Integer, primary_key=True)
    materia_grupo_id = db.Column(db.Integer, db.ForeignKey('materias_grupos.id'), nullable=False)
    dia_semana = db.Column(db.Integer, nullable=False)  # 1=Lunes, 7=Domingo
    hora_inicio = db.Column(db.String(10), nullable=False)  # Formato "HH:MM"
    hora_fin = db.Column(db.String(10), nullable=False)
    salon_id = db.Column(db.Integer, db.ForeignKey('salones.id'))
    tipo_clase = db.Column(db.String(20), default='teoria')  # 'teoria', 'laboratorio', 'practica'

    # RELACIONES
    materia_grupo = db.relationship('MateriaGrupo', back_populates='horarios')
    salon = db.relationship('Salon', back_populates='horarios')

    DIAS_SEMANA = {
        1: 'Lunes',
        2: 'Martes',
        3: 'Miércoles',
        4: 'Jueves',
        5: 'Viernes',
        6: 'Sábado',
        7: 'Domingo'
    }

    def to_dict(self):
        return {
            "id": self.id,
            "materia": self.materia_grupo.materia.nombre if self.materia_grupo else None,
            "grupo": self.materia_grupo.grupo.clave if self.materia_grupo else None,
            "profesor": self.materia_grupo.profesor.nombre if self.materia_grupo and self.materia_grupo.profesor else None,
            "dia_semana": self.dia_semana,
            "dia_nombre": self.DIAS_SEMANA.get(self.dia_semana, 'Desconocido'),
            "hora_inicio": self.hora_inicio,
            "hora_fin": self.hora_fin,
            "salon": self.salon.nombre if self.salon else None,
            "tipo_clase": self.tipo_clase
        }

class Inscripcion(db.Model):
    """
    MODELO INSCRIPCION
    
    Tabla puente que representa la matrícula de un alumno a una asignatura
    específica en un grupo dado. Retiene el estado académico.
    """
    __tablename__ = "inscripciones"
    id = db.Column(db.Integer, primary_key=True)
    alumno_id = db.Column(db.Integer, db.ForeignKey('alumnos.id'), nullable=False)
    materia_grupo_id = db.Column(db.Integer, db.ForeignKey('materias_grupos.id'), nullable=False)
    fecha_inscripcion = db.Column(db.DateTime, default=db.func.current_timestamp())
    calificacion = db.Column(db.Float)
    estado = db.Column(db.String(20), default='activo')  # 'activo', 'baja', 'completado'

    # RELACIONES
    alumno = db.relationship('Alumno', back_populates='inscripciones')
    materia_grupo = db.relationship('MateriaGrupo', back_populates='inscripciones')

    __table_args__ = (
        db.UniqueConstraint('alumno_id', 'materia_grupo_id', name='uq_alumno_materia_grupo'),
    )

    def to_dict(self):
        return {
            "id": self.id,
            "alumno": self.alumno.nombre if self.alumno else None,
            "boleta": self.alumno.boleta if self.alumno else None,
            "materia": self.materia_grupo.materia.nombre if self.materia_grupo else None,
            "grupo": self.materia_grupo.grupo.clave if self.materia_grupo else None,
            "fecha_inscripcion": self.fecha_inscripcion.isoformat() if self.fecha_inscripcion else None,
            "calificacion": self.calificacion,
            "estado": self.estado
        }

# MODELOS DE ESTACIONAMIENTO Y MARCADORES


class SavedPlace(db.Model):
    """
    MODELO LUGAR GUARDADO
    
    Permite al usuario conservar y bautizar un punto geográfico
    de interés particular en el lienzo del mapa de la escuela.
    """
    __tablename__ = "saved_places"
    id = db.Column(db.Integer, primary_key=True)
    user_boleta = db.Column(db.String(20), db.ForeignKey('alumnos.boleta'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    lat = db.Column(db.Float, nullable=False)
    lon = db.Column(db.Float, nullable=False)
    type = db.Column(db.String(20), default='custom')
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    # RELACIONES
    user = db.relationship('Alumno', back_populates='saved_places')

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "lat": self.lat,
            "lon": self.lon,
            "type": self.type,
            "user_boleta": self.user_boleta
        }

class ParkingSection(db.Model):
    """
    MODELO SECCION DE ESTACIONAMIENTO
    
    Representa una región delimitada dentro del área del estacionamiento,
    agrupando lógicamente un número definido de lugares o cajones.
    """
    __tablename__ = "parking_sections"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    total_spaces = db.Column(db.Integer, nullable=False)
    map_image_url = db.Column(db.String(255), nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "total_spaces": self.total_spaces,
            "map_image_url": self.map_image_url
        }

class ParkingSpace(db.Model):
    """
    MODELO ESPACIO DE ESTACIONAMIENTO
    
    Detalla la anatomía individual y el estado de cada cajón dentro
    del área de parqueo institucional, vinculando a los usuarios que
    atribuyen ocupaciones o realizan reservas y exponiendo coordenadas.
    """
    __tablename__ = "parking_spaces"
    id = db.Column(db.Integer, primary_key=True)
    space_number = db.Column(db.String(10), unique=True, nullable=False)
    section_id = db.Column(db.Integer, db.ForeignKey('parking_sections.id'), nullable=False)
    row_number = db.Column(db.Integer)
    position_number = db.Column(db.Integer)
    lat = db.Column(db.Float, nullable=False)
    lon = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='available')
    occupied_by = db.Column(db.String(20), db.ForeignKey('alumnos.boleta'))
    occupied_at = db.Column(db.DateTime)
    reserved_by = db.Column(db.String(20), db.ForeignKey('alumnos.boleta'))
    reserved_at = db.Column(db.DateTime)
    reservation_expires_at = db.Column(db.DateTime)
    distance_to_building_1 = db.Column(db.Float)
    distance_to_building_2 = db.Column(db.Float)
    distance_to_building_3 = db.Column(db.Float)
    last_updated = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    # RELACIONES
    occupant = db.relationship('Alumno', foreign_keys=[occupied_by], back_populates='occupied_spaces')
    reserver = db.relationship('Alumno', foreign_keys=[reserved_by], back_populates='reserved_spaces')
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
    la retención de un cajón asignado previamente vía plataforma.
    """
    __tablename__ = "parking_reservations"
    id = db.Column(db.Integer, primary_key=True)
    space_id = db.Column(db.Integer, db.ForeignKey('parking_spaces.id'), nullable=False)
    user_boleta = db.Column(db.String(20), db.ForeignKey('alumnos.boleta'), nullable=False)
    reserved_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    expires_at = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), default='active')
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    # RELACIONES
    space = db.relationship('ParkingSpace', backref=db.backref('reservations', lazy=True))
    user = db.relationship('Alumno', backref=db.backref('parking_reservations', lazy=True))

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
    
    Registro tipo bitácora forense de la evolución de estados 
    (disponible, ocupado, reservado) que ocurren en los cajones de forma perpetua.
    """
    __tablename__ = "parking_history"
    id = db.Column(db.Integer, primary_key=True)
    space_id = db.Column(db.Integer, db.ForeignKey('parking_spaces.id'), nullable=False)
    user_boleta = db.Column(db.String(20))
    action = db.Column(db.String(20), nullable=False)
    previous_status = db.Column(db.String(20))
    new_status = db.Column(db.String(20))
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())

    # RELACIONES
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
