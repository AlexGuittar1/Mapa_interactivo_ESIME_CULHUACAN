"""
Repository Factory — Capa de Abstracción de Datos

Crea las instancias correctas de repositorios según la configuración
del entorno (APP_ENV). Para agregar un nuevo proveedor de datos:

1. Crear un archivo con las clases que implementen UserRepository
   y/o ScheduleRepository
2. Registrar el nuevo proveedor en las funciones factory de abajo
"""


def create_user_repository(config):
    """Factory: crea el repositorio de usuarios según configuración.

    Args:
        config: Objeto de configuración (LocalConfig o InstitutionalConfig)

    Returns:
        Instancia de UserRepository
    """
    provider = getattr(config, 'DATA_PROVIDER', 'sqlite')

    if provider == 'sqlite':
        from repositories.sqlite_repository import SQLiteUserRepository
        return SQLiteUserRepository()

    elif provider == 'sqlserver':
        # Futuro: la escuela implementa SQLServerUserRepository
        # from repositories.sqlserver_repository import SQLServerUserRepository
        # return SQLServerUserRepository(config.SQLALCHEMY_DATABASE_URI)
        raise NotImplementedError(
            "SQL Server provider no implementado. "
            "La escuela debe proporcionar SQLServerUserRepository."
        )

    elif provider == 'api':
        # Futuro: la escuela expone API REST
        # from repositories.api_repository import APIUserRepository
        # return APIUserRepository(config.INSTITUTIONAL_API_URL, config.INSTITUTIONAL_API_KEY)
        raise NotImplementedError(
            "API provider no implementado. "
            "La escuela debe proporcionar APIUserRepository."
        )

    else:
        raise ValueError(f"Proveedor de datos desconocido: {provider}")


def create_schedule_repository(config):
    """Factory: crea el repositorio de horarios según configuración."""
    provider = getattr(config, 'DATA_PROVIDER', 'sqlite')

    if provider == 'sqlite':
        from repositories.sqlite_repository import SQLiteScheduleRepository
        return SQLiteScheduleRepository()

    else:
        # Para otros proveedores, usar SQLite como fallback para horarios
        # ya que los horarios son datos internos de la app
        from repositories.sqlite_repository import SQLiteScheduleRepository
        return SQLiteScheduleRepository()
