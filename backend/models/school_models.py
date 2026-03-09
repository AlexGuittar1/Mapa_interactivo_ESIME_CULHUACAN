"""
ARCHIVO: models/school_models.py

MODELOS DE DATOS INSTITUCIONALES

Define las tablas que almacenan informacion academica e institucional:
alumnos, materias, profesores, salones, grupos, horarios e inscripciones.

Estos modelos pertenecen a la base de datos SCHOOL (bind_key = 'school')
y pueden ser reemplazados por la base de datos propia de cada escuela.

Para integrar una escuela diferente, se deben mapear sus tablas existentes
a estos modelos o crear un adaptador en services/school_adapter.py.
"""

from models.database import db


# MODELOS DE USUARIOS


class Alumno(db.Model):
    """
    MODELO ALUMNO

    Identidad principal del usuario dentro de la aplicacion.
    Almacena datos personales, identificadores institucionales y mantiene
    las relaciones con inscripciones y configuraciones academicas.
    """
    __tablename__ = "alumnos"
    __bind_key__ = "school"

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
    password_hash = db.Column(db.String(256), nullable=True)
    last_login = db.Column(db.DateTime, nullable=True)
    is_synced = db.Column(db.Boolean, default=False)

    # RELACIONES (dentro de la misma base de datos SCHOOL)
    inscripciones = db.relationship('Inscripcion', back_populates='alumno', lazy=True, cascade='all, delete-orphan')

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


# MODELOS ACADEMICOS


class Materia(db.Model):
    """
    MODELO MATERIA

    Define una asignatura curricular del plan de estudios.
    Contiene informacion propia del curso como valor de creditos y semestre.
    """
    __tablename__ = "materias"
    __bind_key__ = "school"

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
    contacto e informacion administrativa como el departamento.
    """
    __tablename__ = "profesores"
    __bind_key__ = "school"

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

    Espacio fisico destinado a la docencia. Permite asociar
    las clases a un lugar fisico con propiedades como capacidad o tipo.

    NOTA: edificio_id es una referencia logica al edificio en la base MAP.
    No es una FK real porque el edificio vive en otra base de datos.
    """
    __tablename__ = "salones"
    __bind_key__ = "school"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), unique=True, nullable=False)
    edificio_id = db.Column(db.Integer)
    capacidad = db.Column(db.Integer)
    tipo = db.Column(db.String(20))  # 'aula', 'laboratorio', 'auditorio'

    # RELACIONES
    horarios = db.relationship('Horario', back_populates='salon', lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "edificio_id": self.edificio_id,
            "capacidad": self.capacidad,
            "tipo": self.tipo
        }


class Grupo(db.Model):
    """
    MODELO GRUPO

    Organizacion academica de un bloque de estudiantes. Define atributos
    agrupadores como semestre, turno, bloque de carrera y su identificador.
    """
    __tablename__ = "grupos"
    __bind_key__ = "school"

    id = db.Column(db.Integer, primary_key=True)
    clave = db.Column(db.String(20), unique=True, nullable=False)
    semestre = db.Column(db.Integer, nullable=False)
    turno = db.Column(db.String(20))
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

    Tabla relacional central que asocia una materia especifica impartida
    a un grupo en particular, anadiendo el profesor a cargo y el ciclo.
    """
    __tablename__ = "materias_grupos"
    __bind_key__ = "school"

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

    Estructura normalizada para los tiempos y dias de la semana en
    los que se imparte una MateriaGrupo, en que salon y bajo que modalidad.
    """
    __tablename__ = "horarios"
    __bind_key__ = "school"

    id = db.Column(db.Integer, primary_key=True)
    materia_grupo_id = db.Column(db.Integer, db.ForeignKey('materias_grupos.id'), nullable=False)
    dia_semana = db.Column(db.Integer, nullable=False)
    hora_inicio = db.Column(db.String(10), nullable=False)
    hora_fin = db.Column(db.String(10), nullable=False)
    salon_id = db.Column(db.Integer, db.ForeignKey('salones.id'))
    tipo_clase = db.Column(db.String(20), default='teoria')

    # RELACIONES
    materia_grupo = db.relationship('MateriaGrupo', back_populates='horarios')
    salon = db.relationship('Salon', back_populates='horarios')

    DIAS_SEMANA = {
        1: 'Lunes',
        2: 'Martes',
        3: 'Miercoles',
        4: 'Jueves',
        5: 'Viernes',
        6: 'Sabado',
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

    Tabla puente que representa la matricula de un alumno a una asignatura
    especifica en un grupo dado. Retiene el estado academico.
    """
    __tablename__ = "inscripciones"
    __bind_key__ = "school"

    id = db.Column(db.Integer, primary_key=True)
    alumno_id = db.Column(db.Integer, db.ForeignKey('alumnos.id'), nullable=False)
    materia_grupo_id = db.Column(db.Integer, db.ForeignKey('materias_grupos.id'), nullable=False)
    fecha_inscripcion = db.Column(db.DateTime, default=db.func.current_timestamp())
    calificacion = db.Column(db.Float)
    estado = db.Column(db.String(20), default='activo')

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
