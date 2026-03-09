#!/usr/bin/env python3
"""
ARCHIVO: seed_map_data.py

SCRIPT DE INICIALIZACION DE DATOS DEL MAPA

Lee los archivos JSON de la carpeta map_data/ e inserta los datos
en la base de datos del mapa si las tablas estan vacias.

Este script se ejecuta automaticamente al iniciar la aplicacion
o puede ejecutarse manualmente con:

    python3 seed_map_data.py

Los datos del mapa son independientes de los datos institucionales
y no se pierden al conectar otra base de datos escolar.
"""

import json
import os
import math


def load_json(filename):
    """
    CARGAR ARCHIVO JSON

    Lee un archivo JSON desde la carpeta map_data/.
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(base_dir, 'map_data', filename)

    if not os.path.exists(filepath):
        print(f"[SEED] Archivo no encontrado: {filepath}")
        return None

    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def haversine_distance(lat1, lon1, lat2, lon2):
    """
    CALCULO DE DISTANCIA HAVERSINE

    Calcula la distancia en metros entre dos coordenadas GPS.
    """
    R = 6371000
    lat1_r, lat2_r = math.radians(lat1), math.radians(lat2)
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)

    a = math.sin(dlat / 2) ** 2 + math.cos(lat1_r) * math.cos(lat2_r) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c


def seed_buildings(db):
    """
    POBLAR EDIFICIOS

    Inserta los edificios del campus desde buildings.json
    si la tabla esta vacia.
    """
    from models import EdificioDB

    existing = EdificioDB.query.count()
    if existing > 0:
        print(f"[SEED] Edificios: Ya existen {existing} registros. Omitiendo.")
        return

    buildings = load_json('buildings.json')
    if not buildings:
        return

    count = 0
    for b in buildings:
        edificio = EdificioDB(
            nombre=b['name'],
            latitud=b['lat'],
            longitud=b['lon'],
            tipo=b.get('type', 'academico'),
            campus_id=b.get('campus_id', 1)
        )
        db.session.add(edificio)
        count += 1

    db.session.commit()
    print(f"[SEED] Edificios: {count} registros insertados.")


def seed_parking(db):
    """
    POBLAR ESTACIONAMIENTO

    Inserta las secciones y espacios de estacionamiento
    desde parking.json si las tablas estan vacias.
    """
    from models import ParkingSection, ParkingSpace

    existing_sections = ParkingSection.query.count()
    if existing_sections > 0:
        print(f"[SEED] Estacionamiento: Ya existen {existing_sections} secciones. Omitiendo.")
        return

    parking_data = load_json('parking.json')
    if not parking_data:
        return

    ref_buildings = parking_data.get('reference_buildings', {})
    campus_id = parking_data.get('campus_id', 1)

    spaces_created = 0

    for section_data in parking_data.get('sections', []):
        # Crear la seccion
        section = ParkingSection(
            name=section_data['name'],
            total_spaces=section_data['total_spaces'],
            campus_id=campus_id
        )
        db.session.add(section)
        db.session.flush()  # Obtener el ID asignado

        # Generar los espacios de la seccion
        rows = section_data.get('rows', 9)
        spaces_per_row = section_data.get('spaces_per_row', 10)
        base_lat = section_data['base_lat']
        base_lon = section_data['base_lon']
        lat_offset = section_data.get('lat_offset', 0.000012)
        lon_offset = section_data.get('lon_offset', 0.000020)

        space_count = 0
        for row in range(rows):
            for pos in range(spaces_per_row):
                space_count += 1
                if space_count > section_data['total_spaces']:
                    break

                space_number = f"{section_data['name'].replace('Seccion ', '')}-{space_count:03d}"
                lat = base_lat + (row * lat_offset)
                lon = base_lon + (pos * lon_offset)

                # Calcular distancias a edificios de referencia
                dist_b1 = haversine_distance(lat, lon, ref_buildings['building_1']['lat'], ref_buildings['building_1']['lon']) if 'building_1' in ref_buildings else None
                dist_b2 = haversine_distance(lat, lon, ref_buildings['building_2']['lat'], ref_buildings['building_2']['lon']) if 'building_2' in ref_buildings else None
                dist_b3 = haversine_distance(lat, lon, ref_buildings['building_3']['lat'], ref_buildings['building_3']['lon']) if 'building_3' in ref_buildings else None

                space = ParkingSpace(
                    space_number=space_number,
                    section_id=section.id,
                    row_number=row + 1,
                    position_number=pos + 1,
                    lat=lat,
                    lon=lon,
                    status='available',
                    distance_to_building_1=round(dist_b1, 1) if dist_b1 else None,
                    distance_to_building_2=round(dist_b2, 1) if dist_b2 else None,
                    distance_to_building_3=round(dist_b3, 1) if dist_b3 else None,
                    campus_id=campus_id,
                )
                db.session.add(space)
                spaces_created += 1

            if space_count > section_data['total_spaces']:
                break

    db.session.commit()
    print(f"[SEED] Estacionamiento: {len(parking_data['sections'])} secciones y {spaces_created} espacios insertados.")


def seed_all(db):
    """
    EJECUTAR TODOS LOS SEEDS

    Ejecuta todos los scripts de seed para poblar la base de datos del mapa.
    Solo inserta datos si las tablas estan vacias.
    """
    print("[SEED] Verificando datos del mapa...")
    seed_buildings(db)
    seed_parking(db)
    print("[SEED] Proceso de seed completado.")


if __name__ == '__main__':
    # Ejecucion manual desde terminal
    from app import app, db as app_db
    with app.app_context():
        seed_all(app_db)
