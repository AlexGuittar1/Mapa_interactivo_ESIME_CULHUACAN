import sqlite3
import os

db_path = 'instance/campus.db'

def setup_database():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # 1. Subject handling
    target_subjects = {
        'Inteligencia Artificial': 1,
        'Compiladores': 2,
        'Estructura de Datos': 3,
        'Redes de Computadoras': 4,
        'Sistemas Operativos': 5,
        'Lenguajes de bajo nivel': 6
    }
    
    subjects_map = {}
    for name in target_subjects:
        cursor.execute("SELECT id_asignatura FROM asignaturas WHERE nombre = ?", (name,))
        res = cursor.fetchone()
        if res:
            subjects_map[name] = res[0]
        else:
            cursor.execute("INSERT INTO asignaturas (nombre) VALUES (?)", (name,))
            subjects_map[name] = cursor.lastrowid

    # 1.5 Building and Path handling (Restored from poblar_bd.py and locations.json)
    # Ensure Buildings exist with CORRECT Visual Coordinates
    edificios_data = [
        {"nombre": "Edificio 1", "lat": 19.328729874100386, "lon": -99.11197900772095},
        {"nombre": "Edificio 2", "lat": 19.32922089251882, "lon": -99.11195218563081},
        {"nombre": "Edificio 3", "lat": 19.32971697148389, "lon": -99.11190390586854},
        {"nombre": "Biblioteca", "lat": 19.329995382487894, "lon": -99.11160349845886},
        {"nombre": "Cafeteria", "lat": 19.32942843594261, "lon": -99.11115556955339},
        {"nombre": "Estacionamiento", "lat": 19.32957523479046, "lon": -99.11261200904848},
    ]
    
    edificios_map = {}
    for e in edificios_data:
        cursor.execute("SELECT id FROM edificios WHERE nombre = ?", (e["nombre"],))
        res = cursor.fetchone()
        if res:
            edificios_map[e["nombre"]] = res[0]
            # Update coords just in case
            cursor.execute("UPDATE edificios SET latitud=?, longitud=? WHERE id=?", (e["lat"], e["lon"], res[0]))
        else:
            cursor.execute("INSERT INTO edificios (nombre, latitud, longitud) VALUES (?, ?, ?)", 
                          (e["nombre"], e["lat"], e["lon"]))
            edificios_map[e["nombre"]] = cursor.lastrowid

    # Populate Paths (Caminos)
    cursor.execute("DELETE FROM caminos;") # Reset paths
    caminos_data = [
        ("Edificio 1", "Edificio 2", 50),
        ("Edificio 2", "Edificio 3", 40),
        ("Edificio 1", "Biblioteca", 100),
        ("Biblioteca", "Cafeteria", 60),
        ("Cafeteria", "Edificio 1", 30),
        ("Edificio 2", "Estacionamiento", 150)
    ]
    
    for o, d, dist in caminos_data:
        cursor.execute("INSERT INTO caminos (origen, destino, distancia) VALUES (?, ?, ?)", (o, d, dist))

    # 2. Salon handling
    needed_salones = ['1101', '1201', '1202', '1203', '1301', '1302']
    salones_map = {}
    for sname in needed_salones:
        cursor.execute("SELECT id_salon FROM salones WHERE nombre = ?", (sname,))
        res = cursor.fetchone()
        if res:
            salones_map[sname] = res[0]
        else:
            # Determine Edificio ID dynamically
            if sname.startswith('11'):
                ed_name = "Edificio 1"
            elif sname.startswith('12'):
                ed_name = "Edificio 2"
            elif sname.startswith('13'):
                ed_name = "Edificio 3"
            else:
                ed_name = "Edificio 1"
            
            edificio_id = edificios_map.get(ed_name, 1)
            cursor.execute("INSERT INTO salones (nombre, edificio_id) VALUES (?, ?);", (sname, edificio_id))
            salones_map[sname] = cursor.lastrowid

    # 3. Group handling
    groups = {
        1: '3CV1',
        2: '3CV3',
        3: '3CV14'
    }
    for gid, gclave in groups.items():
        cursor.execute("INSERT OR REPLACE INTO grupos (id_grupo, clave) VALUES (?, ?);", (gid, gclave))

    # 4. User Rebuilding - THE SINGLE SOURCE OF TRUTH
    # First, wipe existing users to ensure NO duplicates or old entries
    cursor.execute("DELETE FROM usuarios;")
    
    users = [
        ('2024351279', 'afriasr@ipn.mx', 'Frias Rodriguez Adrian', 'Ingeniería en Computación', 'ninguno', 3),
        ('2025350215', 'ososah@ipn.mx', 'Sosa Hernádez Omar Alejandro', 'Ingeniería en Computación', 'ninguno', 3),
        ('2024000001', 'user1@ipn.mx', 'Juan Perez Lopez', 'Ingeniería en Computación', 'ninguno', 1),
        ('2024000002', 'user2@ipn.mx', 'Maria Garcia Ruiz', 'Ingeniería en Computación', 'ninguno', 1),
        ('2024000003', 'user3@ipn.mx', 'Luis Rodriguez Diaz', 'Ingeniería en Computación', 'automovil', 1),
        ('2024000004', 'user4@ipn.mx', 'Ana Martinez Solis', 'Ingeniería en Computación', 'moto', 1),
        ('2024000005', 'user5@ipn.mx', 'Pedro Sanchez Vera', 'Ingeniería en Computación', 'bicicleta', 2),
        ('2024000006', 'user6@ipn.mx', 'Lucia Lopez Mendez', 'Ingeniería en Computación', 'ninguno', 2),
        ('2024000007', 'user7@ipn.mx', 'Carlos Hernandez Cruz', 'Ingeniería en Computación', 'automovil', 2),
        ('2024000008', 'user8@ipn.mx', 'Elena Gomez Santos', 'Ingeniería en Computación', 'ninguno', 2),
    ]
    
    for boleta, email, nombre, carrera, vehiculo, id_grupo in users:
        cursor.execute("""
            INSERT INTO usuarios (boleta, email, nombre, carrera, vehiculo, id_grupo) 
            VALUES (?, ?, ?, ?, ?, ?);
        """, (boleta, email, nombre, carrera, vehiculo, id_grupo))

    # 5. Schedule Rebuilding - Using Full Day Names
    cursor.execute("DELETE FROM horarios;")

    # 3CV14 - Lenguajes de bajo nivel + All 3CV3 Subjects
    # First: Define Lenguajes de bajo nivel specific to 3CV14 (Times optimized to avoid overlaps)
    cv14_unique = [
        ('Lunes', '07:00', '08:30', '1101', 3, subjects_map['Lenguajes de bajo nivel']),
        ('Martes', '07:00', '08:30', '1101', 3, subjects_map['Lenguajes de bajo nivel']),  # Moved from 8:30 to avoid IA overlap
        ('Miércoles', '07:00', '08:30', '1101', 3, subjects_map['Lenguajes de bajo nivel']),
        ('Jueves', '08:30', '10:00', '1101', 3, subjects_map['Lenguajes de bajo nivel']),  # Moved from 10:00 to avoid IA overlap
        ('Viernes', '08:30', '10:00', '1101', 3, subjects_map['Lenguajes de bajo nivel']),
    ]
    
    # 3CV1
    cv1_horario = [
        ('Lunes', '07:00', '08:30', '1201', 1, subjects_map['Inteligencia Artificial']),
        ('Lunes', '08:30', '10:00', '1201', 1, subjects_map['Compiladores']),
        ('Martes', '07:00', '08:30', '1202', 1, subjects_map['Estructura de Datos']),
        ('Martes', '08:30', '10:00', '1202', 1, subjects_map['Redes de Computadoras']),
        ('Miércoles', '08:30', '10:00', '1203', 1, subjects_map['Sistemas Operativos']),
        ('Jueves', '07:00', '08:30', '1201', 1, subjects_map['Inteligencia Artificial']),
        ('Viernes', '08:30', '10:00', '1202', 1, subjects_map['Redes de Computadoras']),
    ]
    
    # 3CV3
    cv3_horario = [
        ('Lunes', '10:30', '12:00', '1301', 2, subjects_map['Redes de Computadoras']),
        ('Lunes', '08:30', '10:00', '1301', 2, subjects_map['Sistemas Operativos']),
        ('Martes', '08:30', '10:00', '1302', 2, subjects_map['Inteligencia Artificial']),
        ('Jueves', '10:30', '12:00', '1301', 2, subjects_map['Inteligencia Artificial']),
        ('Jueves', '07:00', '08:30', '1301', 2, subjects_map['Sistemas Operativos']),
        ('Viernes', '07:00', '08:30', '1302', 2, subjects_map['Compiladores']),
    ]

    # Create hybrid schedule for 3CV14 (id_grupo=3) by copying 3CV3 classes but changing group ID
    cv14_hybrid = cv14_unique + [ (dia, ini, fin, salon, 3, sub_id) for (dia, ini, fin, salon, grp, sub_id) in cv3_horario ]

    all_horarios = cv14_hybrid + cv1_horario + cv3_horario
    for dia, inicio, fin, salon_name, grupo, sub_id in all_horarios:
        cursor.execute("""
            INSERT INTO horarios (dia, hora_inicio, hora_fin, id_salon, id_grupo, id_asignatura) 
            VALUES (?, ?, ?, ?, ?, ?);
        """, (dia, inicio, fin, salones_map[salon_name], grupo, sub_id))

    conn.commit()
    conn.close()
    print("Clean Database Setup Complete! Exactly 10 users populated.")

if __name__ == "__main__":
    setup_database()
