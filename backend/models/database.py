"""
ARCHIVO: models/database.py

INSTANCIA CENTRAL DE SQLALCHEMY

Archivo separado que contiene la instancia unica de SQLAlchemy (db)
para evitar importaciones circulares entre __init__.py y los sub-modulos.

Todos los modelos importan db desde aqui:
    from models.database import db
"""

from flask_sqlalchemy import SQLAlchemy

# INSTANCIA UNICA DE SQLALCHEMY
# Compartida entre ambas bases de datos usando SQLALCHEMY_BINDS
db = SQLAlchemy()
