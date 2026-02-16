#!/usr/bin/env python3
"""
Script de Importación de Horarios ESIME
Versión: 2.0
Fecha: 2026-02-14

Transforma datos de horarios_sqlite.sql (formato desnormalizado)
a la nueva estructura normalizada de base de datos.
"""

import sqlite3
import re
import sys
from pathlib import Path

def parse_horario_field(field_value):
    """
    Parsea campo como '13:00 a 14:30\n1103' 
    Retorna: (hora_inicio, hora_fin, salon)
    """
    if not field_value or field_value == 'NULL':
        return None, None, None
    
    lines = field_value.strip().split('\n')
    if len(lines) == 0:
        return None, None, None
    
    # Extraer horario
    horario_match = re.match(r'(\d{1,2}:\d{2})\s*a\s*(\d{1,2}:\d{2})', lines[0])
    if not horario_match:
        return None, None, None
    
    hora_inicio = horario_match.group(1)
    hora_fin = horario_match.group(2)
    
    # Extraer salón (si existe)
    salon = lines[1].strip() if len(lines) > 1 else None
    
    return hora_inicio, hora_fin, salon

def extract_semestre_from_grupo(clave):
    """Extrae semestre del primer dígito de la clave"""
    match = re.match(r'(\d)', clave)
    return int(match.group(1)) if match else 1

def extract_turno_from_grupo(clave):
    """Extrae turno del prefijo CM/CV/CX"""
    if 'CM' in clave:
        return 'matutino'
    elif 'CV' in clave:
        return 'vespertino'
    elif 'CX' in clave:
        return 'mixto'
    return 'matutino'

def import_horarios_from_sql(db_path, sql_file_path):
    """
    Importa horarios desde archivo SQL desnormalizado
    a la nueva estructura normalizada
    """
    print("=" * 80)
    print("IMPORTACIÓN DE HORARIOS - ESIME")
    print("=" * 80)
    
    # Verificar archivos
    if not Path(db_path).exists():
        print(f"❌ Error: Base de datos no encontrada: {db_path}")
        return False
    
    if not Path(sql_file_path).exists():
        print(f"❌ Error: Archivo SQL no encontrado: {sql_file_path}")
        return False
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Leer archivo SQL original
    print(f"\n📂 Leyendo archivo: {sql_file_path}")
    with open(sql_file_path, 'r', encoding='utf-8') as f:
        sql_content = f.read()
    
    # Extraer todos los INSERT statements
    insert_pattern = r"INSERT INTO horarios \(materia, grupo, lunes, martes, miercoles, jueves, viernes, profesor\) VALUES \((.*?)\);"
    matches = re.findall(insert_pattern, sql_content, re.DOTALL)
    
    print(f"✅ Encontrados {len(matches)} registros para procesar\n")
    
    materias_dict = {}
    profesores_dict = {}
    grupos_dict = {}
    salones_dict = {}
    
    registros_procesados = 0
    registros_omitidos = 0
    
    print("🔄 Procesando registros...")
    
    for idx, match in enumerate(matches, 1):
        if idx % 100 == 0:
            print(f"   Procesados: {idx}/{len(matches)}")
        
        # Parsear valores usando regex más robusto
        values = []
        # Buscar valores entre comillas o NULL
        for val in re.finditer(r"'((?:[^'\\]|\\.)*)'\s*(?:,|$)|NULL\s*(?:,|$)", match):
            if val.group(1) is not None:
                # Reemplazar escapes
                values.append(val.group(1).replace("\\'", "'"))
            else:
                values.append(None)
        
        if len(values) < 8:
            registros_omitidos += 1
            continue
        
        materia_nombre = values[0]
        grupo_clave = values[1]
        profesor_nombre = values[7]
        
        # Saltar registros sin asignar
        if not profesor_nombre or profesor_nombre == '-- Sin Asignar --':
            registros_omitidos += 1
            continue
        
        if not materia_nombre or not grupo_clave:
            registros_omitidos += 1
            continue
        
        try:
            # 1. Insertar materia única
            if materia_nombre not in materias_dict:
                cursor.execute(
                    "INSERT OR IGNORE INTO materias (nombre) VALUES (?)",
                    (materia_nombre,)
                )
                cursor.execute("SELECT id FROM materias WHERE nombre = ?", (materia_nombre,))
                result = cursor.fetchone()
                if result:
                    materias_dict[materia_nombre] = result[0]
            
            # 2. Insertar profesor único
            if profesor_nombre not in profesores_dict:
                cursor.execute(
                    "INSERT OR IGNORE INTO profesores (nombre) VALUES (?)",
                    (profesor_nombre,)
                )
                cursor.execute("SELECT id FROM profesores WHERE nombre = ?", (profesor_nombre,))
                result = cursor.fetchone()
                if result:
                    profesores_dict[profesor_nombre] = result[0]
            
            # 3. Insertar grupo único
            if grupo_clave not in grupos_dict:
                semestre = extract_semestre_from_grupo(grupo_clave)
                turno = extract_turno_from_grupo(grupo_clave)
                cursor.execute(
                    "INSERT OR IGNORE INTO grupos (clave, semestre, turno) VALUES (?, ?, ?)",
                    (grupo_clave, semestre, turno)
                )
                cursor.execute("SELECT id FROM grupos WHERE clave = ?", (grupo_clave,))
                result = cursor.fetchone()
                if result:
                    grupos_dict[grupo_clave] = result[0]
            
            # 4. Crear relación materia-grupo-profesor
            materia_id = materias_dict.get(materia_nombre)
            grupo_id = grupos_dict.get(grupo_clave)
            profesor_id = profesores_dict.get(profesor_nombre)
            
            if not materia_id or not grupo_id:
                registros_omitidos += 1
                continue
            
            cursor.execute("""
                INSERT OR IGNORE INTO materias_grupos (materia_id, grupo_id, profesor_id, ciclo_escolar)
                VALUES (?, ?, ?, '2025-2026')
            """, (materia_id, grupo_id, profesor_id))
            
            cursor.execute("""
                SELECT id FROM materias_grupos 
                WHERE materia_id = ? AND grupo_id = ? AND ciclo_escolar = '2025-2026'
            """, (materia_id, grupo_id))
            result = cursor.fetchone()
            if not result:
                registros_omitidos += 1
                continue
            
            mg_id = result[0]
            
            # 5. Procesar horarios por día
            dias = {
                2: values[2],  # lunes
                3: values[3],  # martes
                4: values[4],  # miercoles
                5: values[5],  # jueves
                6: values[6],  # viernes
            }
            
            for dia_num, horario_field in dias.items():
                if horario_field:
                    hora_inicio, hora_fin, salon_nombre = parse_horario_field(horario_field)
                    
                    if hora_inicio and hora_fin:
                        # Insertar salón si existe
                        salon_id = None
                        if salon_nombre:
                            if salon_nombre not in salones_dict:
                                # Determinar tipo de salón
                                tipo = 'laboratorio' if 'Lab' in salon_nombre else 'aula'
                                cursor.execute(
                                    "INSERT OR IGNORE INTO salones (nombre, tipo) VALUES (?, ?)",
                                    (salon_nombre, tipo)
                                )
                                cursor.execute("SELECT id FROM salones WHERE nombre = ?", (salon_nombre,))
                                result = cursor.fetchone()
                                if result:
                                    salones_dict[salon_nombre] = result[0]
                            salon_id = salones_dict.get(salon_nombre)
                        
                        # Determinar tipo de clase
                        tipo_clase = 'laboratorio' if 'LAB.' in materia_nombre.upper() else 'teoria'
                        
                        # Insertar horario
                        cursor.execute("""
                            INSERT INTO horarios 
                            (materia_grupo_id, dia_semana, hora_inicio, hora_fin, salon_id, tipo_clase)
                            VALUES (?, ?, ?, ?, ?, ?)
                        """, (mg_id, dia_num, hora_inicio, hora_fin, salon_id, tipo_clase))
            
            registros_procesados += 1
            
        except Exception as e:
            print(f"\n⚠️  Error procesando registro {idx}: {e}")
            registros_omitidos += 1
            continue
    
    conn.commit()
    
    # Estadísticas finales
    print("\n" + "=" * 80)
    print("RESUMEN DE IMPORTACIÓN")
    print("=" * 80)
    
    cursor.execute("SELECT COUNT(*) FROM materias")
    print(f"✅ Materias insertadas:        {cursor.fetchone()[0]:>6}")
    
    cursor.execute("SELECT COUNT(*) FROM profesores")
    print(f"✅ Profesores insertados:      {cursor.fetchone()[0]:>6}")
    
    cursor.execute("SELECT COUNT(*) FROM grupos")
    print(f"✅ Grupos insertados:          {cursor.fetchone()[0]:>6}")
    
    cursor.execute("SELECT COUNT(*) FROM salones")
    print(f"✅ Salones insertados:         {cursor.fetchone()[0]:>6}")
    
    cursor.execute("SELECT COUNT(*) FROM materias_grupos")
    print(f"✅ Materias-Grupos creados:    {cursor.fetchone()[0]:>6}")
    
    cursor.execute("SELECT COUNT(*) FROM horarios")
    print(f"✅ Horarios insertados:        {cursor.fetchone()[0]:>6}")
    
    print(f"\n📊 Registros procesados:       {registros_procesados:>6}")
    print(f"⚠️  Registros omitidos:        {registros_omitidos:>6}")
    print(f"📝 Total en archivo:           {len(matches):>6}")
    
    conn.close()
    
    print("\n✅ Importación completada exitosamente!")
    print("=" * 80)
    
    return True

if __name__ == "__main__":
    # Rutas por defecto
    db_path = 'backend/instance/campus.db'
    sql_file_path = 'backend/instance/horarios_sqlite.sql'
    
    # Permitir argumentos de línea de comandos
    if len(sys.argv) > 1:
        db_path = sys.argv[1]
    if len(sys.argv) > 2:
        sql_file_path = sys.argv[2]
    
    success = import_horarios_from_sql(db_path, sql_file_path)
    sys.exit(0 if success else 1)
