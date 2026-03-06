from abc import ABC, abstractmethod
from typing import Optional, List, Dict, Any


class UserRepository(ABC):
    """Interfaz abstracta para acceso a datos de usuarios.

    Permite intercambiar la fuente de datos (SQLite, SQL Server,
    PostgreSQL, MongoDB, API REST institucional) sin modificar
    la lógica de la aplicación.

    Para integrar un nuevo proveedor de datos, solo hay que:
    1. Crear una clase que herede de UserRepository
    2. Implementar todos los métodos abstractos
    3. Registrarla en repositories/__init__.py
    """

    @abstractmethod
    def find_by_boleta(self, boleta: str) -> Optional[Dict[str, Any]]:
        """Buscar alumno por número de boleta."""
        pass

    @abstractmethod
    def find_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """Buscar alumno por correo electrónico."""
        pass

    @abstractmethod
    def find_by_institutional_id(self, inst_id: str) -> Optional[Dict[str, Any]]:
        """Buscar alumno por ID institucional (Azure Object ID, etc)."""
        pass

    @abstractmethod
    def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Crear nuevo registro de alumno. Retorna el dict del alumno creado."""
        pass

    @abstractmethod
    def update(self, boleta: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Actualizar datos del alumno. Retorna None si no existe."""
        pass

    @abstractmethod
    def exists_by_boleta(self, boleta: str) -> bool:
        """Verificar si existe un alumno con la boleta dada."""
        pass


class ScheduleRepository(ABC):
    """Interfaz abstracta para acceso a datos de horarios."""

    @abstractmethod
    def get_schedule_by_boleta(self, boleta: str, dia: Optional[str] = None) -> List[Dict]:
        """Obtener horario del alumno, opcionalmente filtrado por día."""
        pass

    @abstractmethod
    def get_schedule_by_grupo(self, grupo_clave: str, dia: Optional[str] = None) -> List[Dict]:
        """Obtener horario de un grupo académico."""
        pass
