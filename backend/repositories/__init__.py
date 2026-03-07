"""
ARCHIVO: repositories/__init__.py

FABRICA DE REPOSITORIOS (CAPA DE ABSTRACCION DE DATOS)

Crea las instancias correctas de repositorios según la configuración
del entorno (APP_ENV). Para agregar un nuevo proveedor de datos:

1. Crear un archivo con las clases que implementen UserRepository
   y/o ScheduleRepository
2. Registrar el nuevo proveedor orgánicamente en las funciones de la fábrica adjunta
"""


def create_user_repository(config):
    """
    FABRICA DE REPOSITORIO DE USUARIOS
    
    Crea el repositorio de usuarios según configuración activa en ejecución.

    Argumentos:
        config: Objeto de configuración (LocalConfig o InstitutionalConfig)

    Retorna:
        Instancia implementada de UserRepository
    """
    provider = getattr(config, 'DATA_PROVIDER', 'sqlite')

    if provider == 'sqlite':
        from repositories.sqlite_repository import SQLiteUserRepository
        return SQLiteUserRepository()

    elif provider == 'sqlserver':
        # Futuro: La escuela estructura e incorpora un SQLServerUserRepository
        # from repositories.sqlserver_repository import SQLServerUserRepository
        # return SQLServerUserRepository(config.SQLALCHEMY_DATABASE_URI)
        raise NotImplementedError(
            "SQL Server provider no implementado. "
            "La escuela debe proporcionar SQLServerUserRepository."
        )

    elif provider == 'api':
        # Futuro: La escuela expone una API REST formal
        # from repositories.api_repository import APIUserRepository
        # return APIUserRepository(config.INSTITUTIONAL_API_URL, config.INSTITUTIONAL_API_KEY)
        raise NotImplementedError(
            "API provider no implementado. "
            "La escuela debe proporcionar APIUserRepository."
        )

    else:
        raise ValueError(f"Proveedor de datos desconocido: {provider}")


def create_schedule_repository(config):
    """
    FABRICA DE REPOSITORIO DE HORARIOS
    
    Crea el repositorio de horarios según la configuración de conexión validada.
    """
    provider = getattr(config, 'DATA_PROVIDER', 'sqlite')

    if provider == 'sqlite':
        from repositories.sqlite_repository import SQLiteScheduleRepository
        return SQLiteScheduleRepository()

    else:
        # Para otros proveedores relacionales, usar SQLite local como sistema de rescate de disponibilidad (fallback)
        # ya que los horarios son actualmente datos internos orgánicos de la aplicación central
        from repositories.sqlite_repository import SQLiteScheduleRepository
        return SQLiteScheduleRepository()
