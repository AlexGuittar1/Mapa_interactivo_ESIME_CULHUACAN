"""
SCRIPT DE MIGRACION POST-REFACTORIZACION
==========================================
Ejecuta:
1. Limpieza de usuarios antiguos (conserva solo Omar Sosa y Adrian Frias)
2. Establece contrasenas bcrypt para ambos usuarios
3. Corrige horario de Estructura de Datos (grupo 3CV35)
4. Crea backups y elimina bases de datos legacy

Fecha: 2026-03-10
"""
import os
import sys
import shutil
import sqlite3
from datetime import datetime

import bcrypt

# Rutas
BACKEND_DIR = os.path.dirname(os.path.abspath(__file__))
INSTANCE_DIR = os.path.join(BACKEND_DIR, 'instance')
SCHOOL_DB = os.path.join(INSTANCE_DIR, 'school.db')
BACKUP_DIR = os.path.join(BACKEND_DIR, 'backups_pre_migration')

# IDs de usuarios a conservar
KEEP_USER_IDS = [1, 2]  # 1=Adrian Frias, 2=Omar Sosa

# Contrasena a establecer
NEW_PASSWORD = 'nueva123'

def hash_password_bcrypt(password):
    """Genera hash bcrypt para la contrasena."""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def create_backup(db_path, backup_dir):
    """Crea backup de un archivo de base de datos."""
    if not os.path.exists(db_path):
        return None
    os.makedirs(backup_dir, exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    basename = os.path.basename(db_path)
    backup_path = os.path.join(backup_dir, f"{basename}.backup_{timestamp}")
    shutil.copy2(db_path, backup_path)
    print(f"  [BACKUP] {basename} -> {backup_path}")
    return backup_path

def step1_cleanup_users(conn):
    """Elimina todos los usuarios excepto los indicados en KEEP_USER_IDS."""
    print("\n" + "="*60)
    print("PASO 1: LIMPIEZA DE USUARIOS ANTIGUOS")
    print("="*60)
    
    cursor = conn.cursor()
    
    # Contar usuarios antes
    cursor.execute("SELECT COUNT(*) FROM alumnos")
    total_before = cursor.fetchone()[0]
    print(f"  Usuarios actuales: {total_before}")
    
    # Listar los que se van a eliminar
    placeholders = ','.join('?' * len(KEEP_USER_IDS))
    cursor.execute(f"SELECT id, boleta, nombre FROM alumnos WHERE id NOT IN ({placeholders})", KEEP_USER_IDS)
    to_delete = cursor.fetchall()
    
    if not to_delete:
        print("  No hay usuarios para eliminar.")
        return
    
    print(f"  Usuarios a eliminar: {len(to_delete)}")
    for uid, boleta, nombre in to_delete:
        print(f"    - [{uid}] {boleta}: {nombre}")
    
    delete_ids = [row[0] for row in to_delete]
    delete_placeholders = ','.join('?' * len(delete_ids))
    
    # Orden de eliminacion correcto (FK constraints):
    # 1. inscripciones (referencia alumno_id)
    cursor.execute(f"DELETE FROM inscripciones WHERE alumno_id IN ({delete_placeholders})", delete_ids)
    print(f"  [1/2] Inscripciones eliminadas: {cursor.rowcount}")
    
    # 2. alumnos
    cursor.execute(f"DELETE FROM alumnos WHERE id IN ({delete_placeholders})", delete_ids)
    print(f"  [2/2] Alumnos eliminados: {cursor.rowcount}")
    
    conn.commit()
    
    # Verificar
    cursor.execute("SELECT COUNT(*) FROM alumnos")
    total_after = cursor.fetchone()[0]
    print(f"\n  Usuarios restantes: {total_after}")
    
    cursor.execute("SELECT id, boleta, nombre FROM alumnos")
    for uid, boleta, nombre in cursor.fetchall():
        print(f"    ✓ [{uid}] {boleta}: {nombre}")

def step2_set_passwords(conn):
    """Establece contrasena bcrypt para ambos usuarios."""
    print("\n" + "="*60)
    print("PASO 2: ESTABLECER CONTRASENAS BCRYPT")
    print("="*60)
    
    cursor = conn.cursor()
    password_hash = hash_password_bcrypt(NEW_PASSWORD)
    
    print(f"  Algoritmo: bcrypt")
    print(f"  Hash generado: {password_hash[:20]}...")
    print(f"  Verificacion: {bcrypt.checkpw(NEW_PASSWORD.encode(), password_hash.encode())}")
    
    for uid in KEEP_USER_IDS:
        cursor.execute("SELECT boleta, nombre, password_hash FROM alumnos WHERE id = ?", (uid,))
        row = cursor.fetchone()
        if row:
            boleta, nombre, old_hash = row
            old_type = "pbkdf2" if old_hash and old_hash.startswith("pbkdf2:") else ("bcrypt" if old_hash and old_hash.startswith("$2b$") else "sin hash")
            cursor.execute("UPDATE alumnos SET password_hash = ? WHERE id = ?", (password_hash, uid))
            # Generar hash unico para cada usuario
            password_hash = hash_password_bcrypt(NEW_PASSWORD)
            print(f"  ✓ {nombre} ({boleta}): {old_type} -> bcrypt")
    
    conn.commit()

def step3_fix_schedule(conn):
    """Corrige horario de Estructura de Datos para grupo 3CV35."""
    print("\n" + "="*60)
    print("PASO 3: CORREGIR HORARIO ESTRUCTURA DE DATOS")
    print("="*60)
    
    cursor = conn.cursor()
    
    # Buscar dinamicamente el materia_grupo_id
    cursor.execute("""
        SELECT mg.id, m.nombre, g.clave
        FROM materias_grupos mg
        JOIN materias m ON mg.materia_id = m.id
        JOIN grupos g ON mg.grupo_id = g.id
        WHERE m.nombre LIKE '%ESTRUCTURA DE DATOS%'
          AND m.nombre NOT LIKE '%LAB%'
          AND g.clave = '3CV35'
    """)
    result = cursor.fetchone()
    
    if not result:
        print("  ERROR: No se encontro Estructura de Datos para grupo 3CV35")
        return
    
    mg_id, materia, grupo = result
    print(f"  Materia: {materia} | Grupo: {grupo} | MG_ID: {mg_id}")
    
    # Mostrar horarios actuales
    cursor.execute("""
        SELECT id, dia_semana, hora_inicio, hora_fin
        FROM horarios
        WHERE materia_grupo_id = ?
        ORDER BY dia_semana
    """, (mg_id,))
    horarios = cursor.fetchall()
    
    print("  Horarios actuales:")
    for hid, dia, inicio, fin in horarios:
        dias = {1:'Lun', 2:'Mar', 3:'Mie', 4:'Jue', 5:'Vie', 6:'Sab'}
        print(f"    {dias.get(dia, dia)}: {inicio}-{fin} (id={hid})")
    
    # Corregir Martes (dia_semana=2): 15:00 -> 19:00
    cursor.execute("""
        UPDATE horarios
        SET hora_inicio = '19:00', hora_fin = '20:30'
        WHERE materia_grupo_id = ? AND dia_semana = 2 AND hora_inicio = '15:00'
    """, (mg_id,))
    martes_fixed = cursor.rowcount
    print(f"\n  Martes 15:00->19:00: {'✓ Corregido' if martes_fixed else '⚠ No encontrado'}")
    
    # Corregir Viernes (dia_semana=5): 16:30 -> 20:30
    cursor.execute("""
        UPDATE horarios
        SET hora_inicio = '20:30', hora_fin = '22:00'
        WHERE materia_grupo_id = ? AND dia_semana = 5 AND hora_inicio = '16:30'
    """, (mg_id,))
    viernes_fixed = cursor.rowcount
    print(f"  Viernes 16:30->20:30: {'✓ Corregido' if viernes_fixed else '⚠ No encontrado'}")
    
    conn.commit()
    
    # Mostrar horarios corregidos
    cursor.execute("""
        SELECT id, dia_semana, hora_inicio, hora_fin
        FROM horarios
        WHERE materia_grupo_id = ?
        ORDER BY dia_semana
    """, (mg_id,))
    print("\n  Horarios corregidos:")
    for hid, dia, inicio, fin in cursor.fetchall():
        dias = {1:'Lun', 2:'Mar', 3:'Mie', 4:'Jue', 5:'Vie', 6:'Sab'}
        marker = " ← CORREGIDO" if (dia == 2 and inicio == '19:00') or (dia == 5 and inicio == '20:30') else ""
        print(f"    {dias.get(dia, dia)}: {inicio}-{fin}{marker}")

def step4_cleanup_legacy_dbs():
    """Crea backups y elimina bases de datos legacy."""
    print("\n" + "="*60)
    print("PASO 4: LIMPIEZA DE BASES DE DATOS LEGACY")
    print("="*60)
    
    legacy_files = [
        os.path.join(BACKEND_DIR, 'campus.db'),
        os.path.join(INSTANCE_DIR, 'campus.db'),
        os.path.join(INSTANCE_DIR, 'campus_backup_20260214_133603.db'),
        os.path.join(BACKEND_DIR, 'school.db'),
    ]
    
    for filepath in legacy_files:
        if os.path.exists(filepath):
            # Crear backup antes de eliminar
            create_backup(filepath, BACKUP_DIR)
            os.remove(filepath)
            print(f"  ✓ Eliminado: {os.path.relpath(filepath, BACKEND_DIR)}")
        else:
            print(f"  - No existe: {os.path.relpath(filepath, BACKEND_DIR)}")
    
    # Verificar que las DBs activas siguen existiendo
    print("\n  Bases de datos activas:")
    for active in ['instance/map.db', 'instance/school.db']:
        path = os.path.join(BACKEND_DIR, active)
        exists = os.path.exists(path)
        size = os.path.getsize(path) if exists else 0
        print(f"    {'✓' if exists else '✗'} {active} ({size / 1024:.1f} KB)")

def step5_verify(conn):
    """Ejecuta verificaciones finales."""
    print("\n" + "="*60)
    print("PASO 5: VERIFICACION FINAL")
    print("="*60)
    
    cursor = conn.cursor()
    errors = []
    
    # 1. Solo 2 usuarios
    cursor.execute("SELECT COUNT(*) FROM alumnos")
    count = cursor.fetchone()[0]
    if count == 2:
        print(f"  ✓ Usuarios: {count} (correcto)")
    else:
        errors.append(f"Usuarios: esperado 2, encontrado {count}")
        print(f"  ✗ Usuarios: {count} (ERROR)")
    
    # 2. Contrasenas son bcrypt
    cursor.execute("SELECT boleta, nombre, password_hash FROM alumnos")
    for boleta, nombre, phash in cursor.fetchall():
        if phash and phash.startswith('$2b$'):
            print(f"  ✓ {nombre}: bcrypt hash correcto")
        else:
            errors.append(f"{nombre}: hash no es bcrypt")
            print(f"  ✗ {nombre}: hash NO es bcrypt ({phash[:20] if phash else 'NULL'})")
    
    # 3. No hay registros huerfanos en inscripciones
    cursor.execute("""
        SELECT COUNT(*) FROM inscripciones i
        LEFT JOIN alumnos a ON i.alumno_id = a.id
        WHERE a.id IS NULL
    """)
    orphans = cursor.fetchone()[0]
    if orphans == 0:
        print(f"  ✓ Sin inscripciones huerfanas")
    else:
        errors.append(f"Inscripciones huerfanas: {orphans}")
        print(f"  ✗ Inscripciones huerfanas: {orphans}")
    
    # 4. Horario correcto
    cursor.execute("""
        SELECT h.dia_semana, h.hora_inicio 
        FROM horarios h
        JOIN materias_grupos mg ON h.materia_grupo_id = mg.id
        JOIN materias m ON mg.materia_id = m.id
        JOIN grupos g ON mg.grupo_id = g.id
        WHERE m.nombre LIKE '%ESTRUCTURA DE DATOS%'
          AND m.nombre NOT LIKE '%LAB%'
          AND g.clave = '3CV35'
        ORDER BY h.dia_semana
    """)
    schedule = cursor.fetchall()
    schedule_ok = True
    for dia, inicio in schedule:
        if dia == 2 and inicio != '19:00':
            schedule_ok = False
        if dia == 5 and inicio != '20:30':
            schedule_ok = False
    
    if schedule_ok:
        print(f"  ✓ Horario Estructura de Datos: correcto")
    else:
        errors.append("Horario incorrecto")
        print(f"  ✗ Horario Estructura de Datos: ERROR")
    
    # 5. No hay DBs legacy
    legacy_exist = []
    for path in ['campus.db', 'instance/campus.db', 'instance/campus_backup_20260214_133603.db', 'school.db']:
        full = os.path.join(BACKEND_DIR, path)
        if os.path.exists(full):
            legacy_exist.append(path)
    
    if not legacy_exist:
        print(f"  ✓ Sin bases de datos legacy")
    else:
        errors.append(f"DBs legacy restantes: {legacy_exist}")
        print(f"  ✗ DBs legacy restantes: {legacy_exist}")
    
    print("\n" + "="*60)
    if errors:
        print(f"RESULTADO: {len(errors)} ERROR(ES)")
        for e in errors:
            print(f"  ✗ {e}")
    else:
        print("RESULTADO: MIGRACION EXITOSA ✓")
    print("="*60)
    
    return len(errors) == 0


if __name__ == '__main__':
    print("="*60)
    print("MIGRACION POST-REFACTORIZACION")
    print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)
    
    # Crear backup de school.db antes de cualquier modificacion
    create_backup(SCHOOL_DB, BACKUP_DIR)
    
    # Conectar a school.db
    conn = sqlite3.connect(SCHOOL_DB)
    conn.execute("PRAGMA foreign_keys = ON")
    
    try:
        step1_cleanup_users(conn)
        step2_set_passwords(conn)
        step3_fix_schedule(conn)
        step4_cleanup_legacy_dbs()
        success = step5_verify(conn)
    except Exception as e:
        print(f"\n  ERROR FATAL: {e}")
        conn.rollback()
        raise
    finally:
        conn.close()
    
    sys.exit(0 if success else 1)
