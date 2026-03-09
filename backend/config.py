"""
ARCHIVO: config.py

CONFIGURACION DE LA APLICACION Y SUS ENTORNOS

Define la cadena de conexion a las bases de datos (mapa e institucional),
los ajustes de seguridad y la integracion con proveedores de autenticacion
externos como Azure AD.

Soporta dos modos de operacion:
  - standalone: Solo usa la base de datos del mapa (para demo o desarrollo)
  - institutional: Usa la base de datos del mapa + base de datos de la escuela

La base de datos del MAPA siempre es local (SQLite por defecto).
La base de datos ESCOLAR puede ser externa (Azure SQL, PostgreSQL, SQL Server).
"""

# IMPORTACIONES
import os
from dotenv import load_dotenv

load_dotenv()


# CLASES DE CONFIGURACION


class BaseConfig:
    """
    CONFIGURACION BASE

    Configuracion compartida por todos los entornos del sistema.
    Establece la clave secreta, deshabilita el rastreo de modificaciones
    de SQLAlchemy y define las URIs de ambas bases de datos.
    """
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # MODO DE OPERACION
    # standalone: Solo mapa (demo/desarrollo)
    # institutional: Mapa + datos escolares externos
    APP_MODE = os.environ.get('APP_MODE', 'standalone')

    # URI DE LA BASE DE DATOS DEL MAPA (siempre local)
    MAP_DATABASE_URL = os.environ.get('MAP_DATABASE_URL', 'sqlite:///map.db')

    # URI DE LA BASE DE DATOS ESCOLAR (intercambiable)
    SCHOOL_DATABASE_URL = os.environ.get('SCHOOL_DATABASE_URL', 'sqlite:///school.db')

    # URI PRINCIPAL (requerida por SQLAlchemy, apunta al mapa por defecto)
    SQLALCHEMY_DATABASE_URI = MAP_DATABASE_URL

    # BINDS PARA MULTIPLES BASES DE DATOS
    SQLALCHEMY_BINDS = {
        'map': MAP_DATABASE_URL,
        'school': SCHOOL_DATABASE_URL,
    }


class LocalConfig(BaseConfig):
    """
    CONFIGURACION LOCAL

    Modo local: Utiliza SQLite tanto para el mapa como para datos escolares.
    Autenticacion basica basada en el numero de boleta.

    Este es el modo por defecto disenado para desarrollo o pruebas.
    No requiere configuracion de variables de red adicionales.
    """
    ENV_NAME = 'local'
    DATA_PROVIDER = 'sqlite'
    AUTH_PROVIDER = 'local'


class InstitutionalConfig(BaseConfig):
    """
    CONFIGURACION INSTITUCIONAL

    Modo institucional: Utiliza SQLite local para el mapa y una base de datos
    externa para los datos escolares. Azure AD para autenticacion.

    La base de datos escolar se configura con la variable de entorno
    SCHOOL_DATABASE_URL. Ejemplos:

    SQLite (demo):
        SCHOOL_DATABASE_URL=sqlite:///school.db

    PostgreSQL:
        SCHOOL_DATABASE_URL=postgresql://user:pass@host:5432/school_db

    Azure SQL:
        SCHOOL_DATABASE_URL=mssql+pyodbc://user:pass@server.database.windows.net/db?driver=ODBC+Driver+18+for+SQL+Server

    SQL Server:
        SCHOOL_DATABASE_URL=mssql+pyodbc://user:pass@server/db?driver=ODBC+Driver+17+for+SQL+Server
    """
    ENV_NAME = 'institutional'
    APP_MODE = 'institutional'
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

    Examina la variable de entorno APP_ENV para determinar el entorno actual.

    Valores posibles de APP_ENV:
    - local: Entorno de desarrollo con SQLite (valor por defecto)
    - institutional: Entorno de produccion con base de datos externa y Azure AD

    Retorna la instancia de configuracion apropiada.
    """
    env = os.environ.get('APP_ENV', 'local')
    config_class = _configs.get(env, LocalConfig)
    return config_class()
