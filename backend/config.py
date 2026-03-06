import os
from dotenv import load_dotenv

load_dotenv()


class BaseConfig:
    """Configuración base compartida por todos los entornos."""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class LocalConfig(BaseConfig):
    """Modo local: SQLite + autenticación por boleta.
    
    Este es el modo por defecto. No requiere ninguna configuración
    adicional y funciona con la base de datos local campus.db.
    """
    ENV_NAME = 'local'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///campus.db'
    DATA_PROVIDER = 'sqlite'
    AUTH_PROVIDER = 'local'


class InstitutionalConfig(BaseConfig):
    """Modo institucional: Base de datos externa + Azure AD.
    
    Este modo se activa cuando la escuela integra sus propios sistemas.
    Requiere configurar las variables de entorno correspondientes.
    """
    ENV_NAME = 'institutional'
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        'sqlite:///campus.db'  # Fallback a SQLite si no se configura
    )
    DATA_PROVIDER = os.environ.get('DATA_PROVIDER', 'sqlserver')
    AUTH_PROVIDER = 'azure'

    # Azure AD
    AZURE_TENANT_ID = os.environ.get('AZURE_TENANT_ID', '')
    AZURE_CLIENT_ID = os.environ.get('AZURE_CLIENT_ID', '')
    AZURE_CLIENT_SECRET = os.environ.get('AZURE_CLIENT_SECRET', '')
    AZURE_AUTHORITY = os.environ.get(
        'AZURE_AUTHORITY',
        'https://login.microsoftonline.com/common'
    )

    # API Institucional (alternativa a DB directa)
    INSTITUTIONAL_API_URL = os.environ.get('INSTITUTIONAL_API_URL', '')
    INSTITUTIONAL_API_KEY = os.environ.get('INSTITUTIONAL_API_KEY', '')


# Registro de configuraciones disponibles
_configs = {
    'local': LocalConfig,
    'institutional': InstitutionalConfig,
}


def get_config():
    """Obtiene la configuración según la variable de entorno APP_ENV.
    
    Uso:
        APP_ENV=local          → SQLite + auth por boleta (default)
        APP_ENV=institutional  → DB externa + Azure AD
    """
    env = os.environ.get('APP_ENV', 'local')
    config_class = _configs.get(env, LocalConfig)
    return config_class()
