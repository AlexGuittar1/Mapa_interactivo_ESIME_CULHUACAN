#!/usr/bin/env python3
"""
ARCHIVO: migrate_campus_to_school.py

MIGRACION DE DATOS DE CAMPUS.DB A SCHOOL.DB

Este script copia todos los datos institucionales (alumnos, materias,
profesores, grupos, horarios, inscripciones, salones) desde la base
de datos antigua campus.db hacia la nueva base school.db.

Se ejecuta una sola vez despues de la refactorizacion dual-database.

Uso:
    python3 migrate_campus_to_school.py
"""

import sqlite3
import os

# RUTAS DE LAS BASES DE DATOS
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CAMPUS_DB = os.path.join(BASE_DIR, 'instance', 'campus.db')
SCHOOL_DB = os.path.join(BASE_DIR, 'instance', 'school.db')

# TABLAS A MIGRAR (en orden de dependencias)
SCHOOL_TABLES = [
    'alumnos',
    'materias',
    'profesores',
    'salones',
    'grupos',
    'materias_grupos',
    'horarios',
    'inscripciones',
]


def migrate():
    """
    EJECUTAR MIGRACION

    Copia los datos de todas las tablas institucionales de campus.db a school.db.
    Solo copia si la tabla destino esta vacia.
    """
    if not os.path.exists(CAMPUS_DB):
        print(f"[MIGRACION] Error: No se encontro {CAMPUS_DB}")
        return False

    # Primero, crear las tablas en school.db usando la app Flask
    print("[MIGRACION] Creando tablas en school.db...")
    from app import app, db
    with app.app_context():
        db.create_all()

    # Conectar a ambas bases de datos
    campus_conn = sqlite3.connect(CAMPUS_DB)
    school_conn = sqlite3.connect(SCHOOL_DB)

    campus_conn.row_factory = sqlite3.Row
    total_migrated = 0

    try:
        for table in SCHOOL_TABLES:
            # Verificar si la tabla existe en campus.db
            campus_cursor = campus_conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
                (table,)
            )
            if not campus_cursor.fetchone():
                print(f"  [{table}] No existe en campus.db, omitiendo.")
                continue

            # Verificar si la tabla destino ya tiene datos
            try:
                school_cursor = school_conn.execute(f"SELECT COUNT(*) FROM {table}")
                existing_count = school_cursor.fetchone()[0]
                if existing_count > 0:
                    print(f"  [{table}] Ya tiene {existing_count} registros, omitiendo.")
                    continue
            except sqlite3.OperationalError:
                print(f"  [{table}] No existe en school.db, omitiendo.")
                continue

            # Obtener columnas de la tabla en campus.db
            campus_cursor = campus_conn.execute(f"PRAGMA table_info({table})")
            campus_columns = [col[1] for col in campus_cursor.fetchall()]

            # Obtener columnas de la tabla en school.db
            school_cursor = school_conn.execute(f"PRAGMA table_info({table})")
            school_columns = [col[1] for col in school_cursor.fetchall()]

            # Solo copiar columnas que existen en ambas
            common_columns = [c for c in campus_columns if c in school_columns]

            if not common_columns:
                print(f"  [{table}] No hay columnas comunes, omitiendo.")
                continue

            # Leer datos de campus.db
            columns_str = ', '.join(common_columns)
            campus_cursor = campus_conn.execute(f"SELECT {columns_str} FROM {table}")
            rows = campus_cursor.fetchall()

            if not rows:
                print(f"  [{table}] Sin datos en campus.db.")
                continue

            # Insertar en school.db
            placeholders = ', '.join(['?' for _ in common_columns])
            insert_sql = f"INSERT OR IGNORE INTO {table} ({columns_str}) VALUES ({placeholders})"

            count = 0
            for row in rows:
                try:
                    school_conn.execute(insert_sql, tuple(row))
                    count += 1
                except sqlite3.IntegrityError as e:
                    # Omitir registros duplicados
                    pass

            school_conn.commit()
            total_migrated += count
            print(f"  [{table}] {count} registros migrados.")

    except Exception as e:
        print(f"[MIGRACION] Error: {e}")
        return False
    finally:
        campus_conn.close()
        school_conn.close()

    print(f"\n[MIGRACION] Completado: {total_migrated} registros totales migrados a school.db")
    return True


if __name__ == '__main__':
    print("=" * 50)
    print("MIGRACION: campus.db -> school.db")
    print("=" * 50)
    migrate()
