"""
ARCHIVO: services/school_adapter.py

ADAPTADOR DE DATOS INSTITUCIONALES

Proporciona una interfaz unificada para acceder a los datos academicos
de cualquier escuela, independientemente de donde esten almacenados.

Dos implementaciones disponibles:
  - LocalSchoolAdapter: Lee de la base de datos local SQLite (modo demo)
  - InstitutionalSchoolAdapter: Lee de la base de datos externa de la escuela

Para integrar una nueva escuela, se debe:
1. Crear una nueva clase que herede de SchoolAdapterBase
2. Implementar todos los metodos abstractos
3. Registrarla en create_school_adapter()
"""

from abc import ABC, abstractmethod


class SchoolAdapterBase(ABC):
    """
    CLASE BASE DEL ADAPTADOR ESCOLAR

    Define la interfaz que cualquier adaptador de datos institucionales
    debe implementar. Todas las escuelas deben proporcionar estos metodos.
    """

    @abstractmethod
    def get_student(self, boleta):
        """
        Obtener los datos de un estudiante por su numero de boleta.
        Retorna un diccionario con los datos o None si no existe.
        """
        pass

    @abstractmethod
    def get_student_by_email(self, email):
        """
        Obtener los datos de un estudiante por su correo electronico.
        Retorna una tupla (diccionario_usuario, existe: bool).
        """
        pass

    @abstractmethod
    def get_schedule(self, boleta, day_of_week=None):
        """
        Obtener el horario de un estudiante por su boleta.
        Si day_of_week se proporciona, filtra por dia de la semana (1=Lunes, 7=Domingo).
        Retorna una lista de diccionarios con las clases.
        """
        pass

    @abstractmethod
    def register_student(self, nombre, boleta, carrera=None, vehiculo=None, email=None):
        """
        Registrar un nuevo estudiante.
        Retorna el diccionario del estudiante creado o None si ya existe.
        """
        pass

    @abstractmethod
    def update_student(self, boleta, **kwargs):
        """
        Actualizar los datos de un estudiante.
        Retorna el diccionario del estudiante actualizado o None si no existe.
        """
        pass

    @abstractmethod
    def authenticate(self, boleta):
        """
        Autenticar un estudiante por su boleta.
        Retorna el diccionario del estudiante o None si no existe.
        """
        pass


class LocalSchoolAdapter(SchoolAdapterBase):
    """
    ADAPTADOR LOCAL (SQLITE)

    Lee los datos academicos de la base de datos local SQLite.
    Usado en modo standalone y desarrollo.
    """

    def get_student(self, boleta):
        from models import Alumno
        alumno = Alumno.query.filter_by(boleta=boleta).first()
        return alumno.to_dict() if alumno else None

    def get_student_by_email(self, email):
        from models import Alumno
        alumno = Alumno.query.filter_by(email=email).first()
        if alumno:
            return alumno.to_dict(), True
        return None, False

    def get_schedule(self, boleta, day_of_week=None):
        from models import Alumno, Inscripcion, Horario
        alumno = Alumno.query.filter_by(boleta=boleta).first()
        if not alumno:
            return []

        inscripciones = Inscripcion.query.filter_by(
            alumno_id=alumno.id, estado='activo'
        ).all()

        schedule = []
        for insc in inscripciones:
            mg = insc.materia_grupo
            if mg:
                horarios = mg.horarios
                if day_of_week is not None:
                    horarios = [h for h in horarios if h.dia_semana == day_of_week]
                for h in horarios:
                    schedule.append(h.to_dict())

        schedule.sort(key=lambda x: x.get('hora_inicio', ''))
        return schedule

    def register_student(self, nombre, boleta, carrera=None, vehiculo=None, email=None):
        from models import db, Alumno, Grupo
        import random

        existing = Alumno.query.filter_by(boleta=boleta).first()
        if existing:
            return None

        # Asignar grupo aleatorio si existe alguno
        grupo = Grupo.query.order_by(db.func.random()).first()

        alumno = Alumno(
            nombre=nombre,
            boleta=boleta,
            carrera=carrera or 'Sin asignar',
            vehiculo=vehiculo or 'Ninguno',
            email=email,
            id_grupo=grupo.id if grupo else None,
        )
        db.session.add(alumno)
        db.session.commit()
        return alumno.to_dict()

    def update_student(self, boleta, **kwargs):
        from models import db, Alumno
        alumno = Alumno.query.filter_by(boleta=boleta).first()
        if not alumno:
            return None

        for key, value in kwargs.items():
            if hasattr(alumno, key):
                setattr(alumno, key, value)

        db.session.commit()
        return alumno.to_dict()

    def authenticate(self, boleta):
        return self.get_student(boleta)


class InstitutionalSchoolAdapter(SchoolAdapterBase):
    """
    ADAPTADOR INSTITUCIONAL (BASE DE DATOS EXTERNA)

    Lee los datos academicos de la base de datos propia de la escuela.

    NOTA PARA INTEGRADORES:
    Esta clase debe ser personalizada por cada escuela para mapear
    sus tablas existentes a la interfaz del adaptador.

    Si las tablas de la escuela tienen nombres o columnas diferentes,
    ajusta las consultas SQL en cada metodo.

    Ejemplo: Si en la escuela la tabla de alumnos se llama 'estudiantes'
    y la boleta se llama 'matricula', modifica get_student() asi:

        def get_student(self, boleta):
            result = db.session.execute(
                text("SELECT * FROM estudiantes WHERE matricula = :m"),
                {"m": boleta}
            )
            row = result.fetchone()
            if row:
                return {
                    "boleta": row.matricula,
                    "nombre": row.nombre_completo,
                    ...
                }
            return None
    """

    def __init__(self, database_url=None):
        self.database_url = database_url

    def get_student(self, boleta):
        # Implementar segun la estructura de la base de datos de la escuela
        from models import Alumno
        alumno = Alumno.query.filter_by(boleta=boleta).first()
        return alumno.to_dict() if alumno else None

    def get_student_by_email(self, email):
        from models import Alumno
        alumno = Alumno.query.filter_by(email=email).first()
        if alumno:
            return alumno.to_dict(), True
        return None, False

    def get_schedule(self, boleta, day_of_week=None):
        # Implementar segun la estructura de horarios de la escuela
        from models import Alumno, Inscripcion
        alumno = Alumno.query.filter_by(boleta=boleta).first()
        if not alumno:
            return []

        inscripciones = Inscripcion.query.filter_by(
            alumno_id=alumno.id, estado='activo'
        ).all()

        schedule = []
        for insc in inscripciones:
            mg = insc.materia_grupo
            if mg:
                horarios = mg.horarios
                if day_of_week is not None:
                    horarios = [h for h in horarios if h.dia_semana == day_of_week]
                for h in horarios:
                    schedule.append(h.to_dict())

        schedule.sort(key=lambda x: x.get('hora_inicio', ''))
        return schedule

    def register_student(self, nombre, boleta, carrera=None, vehiculo=None, email=None):
        # En modo institucional, el registro puede requerir sincronizacion
        # con el sistema de la escuela
        from models import db, Alumno

        existing = Alumno.query.filter_by(boleta=boleta).first()
        if existing:
            return None

        alumno = Alumno(
            nombre=nombre,
            boleta=boleta,
            carrera=carrera or 'Sin asignar',
            vehiculo=vehiculo or 'Ninguno',
            email=email,
            auth_provider='institutional',
        )
        db.session.add(alumno)
        db.session.commit()
        return alumno.to_dict()

    def update_student(self, boleta, **kwargs):
        from models import db, Alumno
        alumno = Alumno.query.filter_by(boleta=boleta).first()
        if not alumno:
            return None

        for key, value in kwargs.items():
            if hasattr(alumno, key):
                setattr(alumno, key, value)

        db.session.commit()
        return alumno.to_dict()

    def authenticate(self, boleta):
        return self.get_student(boleta)


def create_school_adapter(config):
    """
    FABRICA DE ADAPTADORES ESCOLARES

    Crea el adaptador correcto segun el modo de operacion (APP_MODE).

    Argumentos:
        config: Objeto de configuracion (LocalConfig o InstitutionalConfig)

    Retorna:
        Instancia de SchoolAdapterBase
    """
    mode = getattr(config, 'APP_MODE', 'standalone')

    if mode == 'institutional':
        database_url = getattr(config, 'SCHOOL_DATABASE_URL', None)
        return InstitutionalSchoolAdapter(database_url)
    else:
        return LocalSchoolAdapter()
