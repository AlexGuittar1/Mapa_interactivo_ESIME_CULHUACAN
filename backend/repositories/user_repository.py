"""
ARCHIVO: repositories/user_repository.py

INTERFACES DE REPOSITORIOS

Contiene las clases abstractas para los repositorios primarios de
la aplicación. Define los protocolos y arquitecturas que debe cumplir
una interfazar conectora en el patrón repositorio.
"""
from abc import ABC, abstractmethod
from typing import Optional, List, Dict, Any


class UserRepository(ABC):
    """
    INTERFAZ DE REPOSITORIO DE USUARIO
    
    Interfaz abstracta protectora para regular el acceso a datos.

    Permite intercambiar subyacentemente la fuente de conexión real
    (SQLite local, SQL Server alojado, PostgreSQL, MongoDB, API REST externa)
    sin modificar nunca la lógica central de la aplicación cliente.

    Para integrar nuevos puentes de datos, únicamente precisa:
    1. Instaurar una clase que herede desde este contrato UserRepository.
    2. Sobrecargar de funcionalidad todos los métodos listados como abstractmethod.
    3. Registrar formalmente la exportación a través de repositories/__init__.py.
    """

    @abstractmethod
    def find_by_boleta(self, boleta: str) -> Optional[Dict[str, Any]]:
        """Buscar métrica enlazando al número clave unívoco o boleta."""
        pass

    @abstractmethod
    def find_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """Enlazar y descubrir información del perfil con un correo verificado."""
        pass

    @abstractmethod
    def find_by_institutional_id(self, inst_id: str) -> Optional[Dict[str, Any]]:
        """Buscar alumno operando la cadena remota ID Institucional (Azure Object ID u oAuth)."""
        pass

    @abstractmethod
    def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Inyectar instancia persistente del registro Alumno retornando diccionario de valores instanciados."""
        pass

    @abstractmethod
    def update(self, boleta: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Sustituir información contenida en el diccionario activo. Falla o claudica al no hallarlo."""
        pass

    @abstractmethod
    def exists_by_boleta(self, boleta: str) -> bool:
        """Afirmar positivamente si consta evidencia de un alumno cobijado en esta misma boleta."""
        pass


class ScheduleRepository(ABC):
    """
    INTERFAZ DE REPOSITORIO DE HORARIOS
    
    Plantilla abstracta regulando cómo exponer o iterar bloques temporales semánticos.
    """

    @abstractmethod
    def get_schedule_by_boleta(self, boleta: str, dia: Optional[str] = None) -> List[Dict]:
        """Obtener horario desglosado cruzado contra registros formales de inscripción, filtrable opcionalmente por un día particular."""
        pass

    @abstractmethod
    def get_schedule_by_grupo(self, grupo_clave: str, dia: Optional[str] = None) -> List[Dict]:
        """Exportar listado masivo del cronograma general asimilado dentro de las aulas y bloques curriculares por clave (ej. 1CM10)."""
        pass
