"""
ARCHIVO: repositories/sqlite_repository.py

Implementación basada en SQLite y SQLAlchemy local de las interfaces de 
repositorio para control de perfiles de usuario y planificación de horarios.
"""
from repositories.user_repository import UserRepository, ScheduleRepository
from models import db, Alumno, Horario, MateriaGrupo, Inscripcion, Grupo


class SQLiteUserRepository(UserRepository):
    """
    REPOSITORIO DE USUARIOS SQLITE
    
    Implementación SQLite y ORM local del repositorio base de alumnos.
    Esta es la implementación activa por defecto, operando de manera aislada 
    sobre campus.db local bajo el paraguas de Flask-SQLAlchemy.
    """

    def find_by_boleta(self, boleta):
        user = Alumno.query.filter_by(boleta=boleta).first()
        return user.to_dict() if user else None

    def find_by_email(self, email):
        user = Alumno.query.filter_by(email=email).first()
        return user.to_dict() if user else None

    def find_by_institutional_id(self, inst_id):
        user = Alumno.query.filter_by(institutional_id=inst_id).first()
        return user.to_dict() if user else None

    def create(self, data):
        nuevo = Alumno(
            boleta=data.get('boleta'),
            nombre=data.get('nombre', ''),
            email=data.get('email'),
            carrera=data.get('carrera', 'Ingeniería'),
            vehiculo=data.get('vehiculo', 'ninguno'),
            id_grupo=data.get('id_grupo'),
            institutional_id=data.get('institutional_id'),
            auth_provider=data.get('auth_provider', 'local'),
        )
        db.session.add(nuevo)
        db.session.commit()
        return nuevo.to_dict()

    def update(self, boleta, data):
        user = Alumno.query.filter_by(boleta=boleta).first()
        if not user:
            return None
        allowed_fields = ['nombre', 'carrera', 'vehiculo', 'email',
                          'institutional_id', 'auth_provider', 'last_login', 'is_synced']
        for key, value in data.items():
            if key in allowed_fields and hasattr(user, key):
                setattr(user, key, value)
        db.session.commit()
        return user.to_dict()

    def exists_by_boleta(self, boleta):
        return Alumno.query.filter_by(boleta=boleta).first() is not None


class SQLiteScheduleRepository(ScheduleRepository):
    """
    REPOSITORIO DE HORARIOS SQLITE
    
    Implementación formal y resoluta en base local de la obtención
    de los esquemas temporales asociados a profesores o directivos.
    """

    # Mapa referencial para traducir iteradores lógicos nominales a días numerales
    DIAS_MAP = {
        'Lunes': 1, 'Martes': 2, 'Miércoles': 3,
        'Jueves': 4, 'Viernes': 5, 'Sábado': 6, 'Domingo': 7
    }

    def get_schedule_by_boleta(self, boleta, dia=None):
        user = Alumno.query.filter_by(boleta=boleta).first()
        if not user:
            return []

        # Obtener mapeo matricial relacional a través de las inscripciones
        inscripciones = Inscripcion.query.filter_by(alumno_id=user.id).all()
        if inscripciones:
            return self._get_horarios_from_inscripciones(inscripciones, dia)

        # Mecanismo contingente (Fallback): Atraer las asignaturas referenciando el id_grupo en bruto
        if user.id_grupo:
            return self._get_horarios_from_grupo_id(user.id_grupo, dia)

        return []

    def get_schedule_by_grupo(self, grupo_clave, dia=None):
        grupo = Grupo.query.filter_by(clave=grupo_clave).first()
        if not grupo:
            return []

        materias_grupos = MateriaGrupo.query.filter_by(grupo_id=grupo.id).all()
        horarios = []
        for mg in materias_grupos:
            query = Horario.query.filter_by(materia_grupo_id=mg.id)
            if dia:
                dia_num = self.DIAS_MAP.get(dia)
                if dia_num:
                    query = query.filter_by(dia_semana=dia_num)
            horarios.extend([h.to_dict() for h in query.all()])

        return sorted(horarios, key=lambda x: x.get('hora_inicio', ''))

    def _get_horarios_from_inscripciones(self, inscripciones, dia=None):
        horarios = []
        for insc in inscripciones:
            query = Horario.query.filter_by(materia_grupo_id=insc.materia_grupo_id)
            if dia:
                dia_num = self.DIAS_MAP.get(dia)
                if dia_num:
                    query = query.filter_by(dia_semana=dia_num)
            horarios.extend([h.to_dict() for h in query.all()])
        return sorted(horarios, key=lambda x: x.get('hora_inicio', ''))

    def _get_horarios_from_grupo_id(self, id_grupo, dia=None):
        """
        OBTENER CRONOGRAMA POR GRUPO CONOCIDO
        
        Mecanismo iterativo de contingencia (fallback de compatibilidad),
        buscando colapsar la carencia de horario usando 'id_grupo' adscrito al perfil directo del alumno.
        """
        # Ubicar y aislar la entidad Grupo portadora de esta misma ID
        grupo = Grupo.query.filter_by(id=id_grupo).first()
        if not grupo:
            return []
        return self.get_schedule_by_grupo(grupo.clave, dia)
