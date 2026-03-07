"""
ARCHIVO: config.py

Este archivo maneja la configuración de la aplicación y sus diferentes entornos.
Define la cadena de conexión a la base de datos, los ajustes de seguridad
y la integración con proveedores de autenticación externos como Azure AD.
Permite alternar entre un entorno local y uno institucional dinámicamente.
"""

# IMPORTACIONES
import os
from dotenv import load_dotenv

load_dotenv()


# CLASES DE CONFIGURACION

class BaseConfig:
    """
    CONFIGURACION BASE
    
    Configuración compartida por todos los entornos del sistema.
    Establece la clave secreta y deshabilita el rastreo de modificaciones
    de SQLAlchemy para mejorar el rendimiento.
    """
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class LocalConfig(BaseConfig):
    """
    CONFIGURACION LOCAL
    
    Modo local: Utiliza SQLite y autenticación básica basada en el número de boleta.
    Este es el modo por defecto diseñado para desarrollo o pruebas. No requiere
    configuración de variables de red adicionales, ya que opera sobre el archivo
    'campus.db'.
    """
    ENV_NAME = 'local'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///campus.db'
    DATA_PROVIDER = 'sqlite'
    AUTH_PROVIDER = 'local'


class InstitutionalConfig(BaseConfig):
    """
    CONFIGURACION INSTITUCIONAL
    
    Modo institucional: Utiliza base de datos externa y Azure AD para autenticación.
    Este entorno está diseñado para su despliegue en producción cuando la escuela
    conecta sus sistemas internos. Requiere validación y configuración a través de
    variables de entorno.
    """
    ENV_NAME = 'institutional'
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        'sqlite:///campus.db'
    )
    DATA_PROVIDER = os.environ.get('DATA_PROVIDER', 'sqlserver')
    AUTH_PROVIDER = 'azure'

    # CONFIGURACION DE AZURE AD
    AZURE_TENANT_ID = os.environ.get('AZURE_TENANT_ID', '')
    AZURE_CLIENT_ID = os.environ.get('AZURE_CLIENT_ID', '')
    AZURE_CLIENT_SECRET = os.environ.get('AZURE_CLIENT_SECRET', '')
    AZURE_AUTHORITY = os.environ.get(
        'AZURE_AUTHORITY',
        'https://login.microsoftonline.com/common'
    )

    # CONFIGURACION DE API INSTITUCIONAL
    INSTITUTIONAL_API_URL = os.environ.get('INSTITUTIONAL_API_URL', '')
    INSTITUTIONAL_API_KEY = os.environ.get('INSTITUTIONAL_API_KEY', '')


# DICCIONARIO DE CONFIGURACIONES
_configs = {
    'local': LocalConfig,
    'institutional': InstitutionalConfig,
}


# FUNCIONES PRINCIPALES

def get_config():
    """
    OBTENER CONFIGURACION
    
    Esta función examina la variable de entorno 'APP_ENV' para determinar
    el entorno actual de ejecución de la aplicación.
    
    Valores posibles de APP_ENV:
    - local: Entorno de desarrollo aislado con SQLite (valor por defecto).
    - institutional: Entorno de producción en red con Azure y proveedores externos.
    
    Retorna la instancia de configuración apropiada.
    """
    env = os.environ.get('APP_ENV', 'local')
    config_class = _configs.get(env, LocalConfig)
    return config_class()
