"""
ARCHIVO: models/__init__.py

PAQUETE DE MODELOS (RE-EXPORTACION COMPLETA)

Este archivo re-exporta la instancia de SQLAlchemy (db) y todos los modelos
de ambas bases de datos para mantener compatibilidad con los imports existentes.

Uso:
    from models import db, Alumno, ParkingSpace, EdificioDB
"""

# IMPORTAR db DESDE EL MODULO CENTRAL (evita importacion circular)
from models.database import db

# RE-EXPORTAR MODELOS DEL MAPA
from models.map_models import (
    EdificioDB,
    CaminoDB,
    SavedPlace,
    ParkingSection,
    ParkingSpace,
    ParkingReservation,
    ParkingHistory,
)

# RE-EXPORTAR MODELOS INSTITUCIONALES
from models.school_models import (
    Alumno,
    Materia,
    Profesor,
    Salon,
    Grupo,
    MateriaGrupo,
    Horario,
    Inscripcion,
)

# LISTA COMPLETA DE EXPORTACIONES
__all__ = [
    'db',
    # Modelos del mapa
    'EdificioDB',
    'CaminoDB',
    'SavedPlace',
    'ParkingSection',
    'ParkingSpace',
    'ParkingReservation',
    'ParkingHistory',
    # Modelos institucionales
    'Alumno',
    'Materia',
    'Profesor',
    'Salon',
    'Grupo',
    'MateriaGrupo',
    'Horario',
    'Inscripcion',
]
