#!/usr/bin/env python3
"""
Script para inicializar los 90 espacios de estacionamiento de profesores.
Genera espacios en 3 secciones (A, B, C) con coordenadas y distancias calculadas.
"""

from app import app, db
from models import ParkingSpace
import math

# Coordenadas de referencia de los edificios principales
BUILDINGS = {
    "building_1": (19.329712, -99.112289),  # Edificio 1 / Cafetería
    "building_2": (19.330421, -99.111893),  # Edificio 2
    "building_3": (19.329710, -99.111490),  # Edificio 3
}

# Coordenadas base para cada sección del estacionamiento
PARKING_SECTIONS = {
    "A": {
        "base_lat": 19.329500,  # Cerca de Edificio 3
        "base_lon": -99.111400,
        "lat_offset": 0.000015,  # ~1.5m entre filas
        "lon_offset": 0.000025,  # ~2.5m entre espacios
    },
    "B": {
        "base_lat": 19.330300,  # Cerca de Edificio 2
        "base_lon": -99.111700,
        "lat_offset": 0.000015,
        "lon_offset": 0.000025,
    },
    "C": {
        "base_lat": 19.329600,  # Cerca de Cafetería/Edificio 1
        "base_lon": -99.112100,
        "lat_offset": 0.000015,
        "lon_offset": 0.000025,
    },
}

def haversine_distance(coord1, coord2):
    """Calcula la distancia en metros entre dos coordenadas usando la fórmula de Haversine"""
    R = 6371000  # Radio de la Tierra en metros
    lat1, lon1 = math.radians(coord1[0]), math.radians(coord1[1])
    lat2, lon2 = math.radians(coord2[0]), math.radians(coord2[1])

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c

def generate_parking_spaces():
    """Genera los 90 espacios de estacionamiento"""
    
    with app.app_context():
        # Verificar si ya existen espacios
        existing_count = ParkingSpace.query.count()
        if existing_count > 0:
            print(f"⚠️  Ya existen {existing_count} espacios en la base de datos.")
            response = input("¿Deseas eliminarlos y regenerar? (s/n): ")
            if response.lower() != 's':
                print("Operación cancelada.")
                return
            
            # Eliminar espacios existentes
            ParkingSpace.query.delete()
            db.session.commit()
            print("✅ Espacios existentes eliminados.")
        
        spaces_created = 0
        
        # Generar 30 espacios por sección
        for section, config in PARKING_SECTIONS.items():
            print(f"\n🅿️  Generando sección {section}...")
            
            rows = 6  # 6 filas
            spaces_per_row = 5  # 5 espacios por fila = 30 espacios por sección
            
            for row in range(rows):
                for pos in range(spaces_per_row):
                    # Calcular número de espacio (1-30 por sección)
                    space_num = row * spaces_per_row + pos + 1
                    space_number = f"{section}-{space_num:02d}"
                    
                    # Calcular coordenadas
                    lat = config["base_lat"] + (row * config["lat_offset"])
                    lon = config["base_lon"] + (pos * config["lon_offset"])
                    
                    # Calcular distancias a cada edificio
                    space_coords = (lat, lon)
                    dist_b1 = haversine_distance(space_coords, BUILDINGS["building_1"])
                    dist_b2 = haversine_distance(space_coords, BUILDINGS["building_2"])
                    dist_b3 = haversine_distance(space_coords, BUILDINGS["building_3"])
                    
                    # Crear espacio
                    space = ParkingSpace(
                        space_number=space_number,
                        section=section,
                        row_number=row + 1,
                        position_number=pos + 1,
                        lat=lat,
                        lon=lon,
                        status='available',
                        distance_to_building_1=round(dist_b1, 1),
                        distance_to_building_2=round(dist_b2, 1),
                        distance_to_building_3=round(dist_b3, 1)
                    )
                    
                    db.session.add(space)
                    spaces_created += 1
                    
                    if space_num % 10 == 0:
                        print(f"  ✓ Creados {space_num}/30 espacios en sección {section}")
        
        # Guardar en base de datos
        db.session.commit()
        
        print(f"\n✅ ¡Completado! Se crearon {spaces_created} espacios de estacionamiento.")
        print("\n📊 Resumen por sección:")
        
        for section in ["A", "B", "C"]:
            count = ParkingSpace.query.filter_by(section=section).count()
            print(f"  Sección {section}: {count} espacios")
        
        # Mostrar algunos ejemplos
        print("\n📝 Ejemplos de espacios creados:")
        examples = ParkingSpace.query.filter(
            ParkingSpace.space_number.in_(['A-01', 'A-15', 'B-01', 'B-15', 'C-01', 'C-15'])
        ).all()
        
        for space in examples:
            print(f"  {space.space_number}: ({space.lat:.6f}, {space.lon:.6f}) - "
                  f"Edificio 1: {space.distance_to_building_1:.0f}m, "
                  f"Edificio 2: {space.distance_to_building_2:.0f}m, "
                  f"Edificio 3: {space.distance_to_building_3:.0f}m")

if __name__ == "__main__":
    print("🚗 Inicializador de Espacios de Estacionamiento")
    print("=" * 50)
    generate_parking_spaces()
