#!/usr/bin/env python3
"""
ARCHIVO: init_parking.py

SCRIPT DE INICIALIZACION DE ESTACIONAMIENTOS

Programa para rellenar de manera transaccional o forzar la inicializacion de
espacios de estacionamiento de profesores (Secciones A, B, C) calculando
teoricamente distancias contra recintos educativos primarios.
"""
from app import app, db
from models import ParkingSpace
import math

# COORDENADAS DE REFERENCIA DE EDIFICIOS
BUILDINGS = {
    "building_1": (19.329712, -99.112289),  # Referencia Edificio 1 / Cafeteria
    "building_2": (19.330421, -99.111893),  # Referencia Edificio 2
    "building_3": (19.329710, -99.111490),  # Referencia Edificio 3
}

# COORDENADAS BASE PARA SECCIONES LOTE
PARKING_SECTIONS = {
    "A": {
        "base_lat": 19.329500,  # Ubicación cardinal cercania Edificio 3
        "base_lon": -99.111400,
        "lat_offset": 0.000015,  # Separación aproximada 1.5 metros longitudinal
        "lon_offset": 0.000025,  # Separación inter-vehicular 2.5 metros
    },
    "B": {
        "base_lat": 19.330300,  # Ubicación periférica cercania Edificio 2
        "base_lon": -99.111700,
        "lat_offset": 0.000015,
        "lon_offset": 0.000025,
    },
    "C": {
        "base_lat": 19.329600,  # Ubicación limítrofe Cafeteria y Edificio 1
        "base_lon": -99.112100,
        "lat_offset": 0.000015,
        "lon_offset": 0.000025,
    },
}

def haversine_distance(coord1, coord2):
    """
    CALCULO DE DISTANCIA HAVERSINE
    
    Mide y devuelve la longitud euclidiana ajustada entre dos pares asimétricos calculando 
    el radio terrestre perimetral como pivote (fórmula esférica).
    """
    R = 6371000  # Proporción referencial del radio de la tierra expresado en metros
    lat1, lon1 = math.radians(coord1[0]), math.radians(coord1[1])
    lat2, lon2 = math.radians(coord2[0]), math.radians(coord2[1])

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c

def generate_parking_spaces():
    """
    GENERADOR MASIVO DE ESPACIOS CUBICULARES
    
    Produce la inserción iterada de los casilleros vehiculares asumiendo topologías físicas estimadas.
    """
    
    with app.app_context():
        # Confirmar o abortar solapamiento base
        existing_count = ParkingSpace.query.count()
        if existing_count > 0:
            print(f"ADVERTENCIA: Ya existen {existing_count} espacios en la base de datos local.")
            response = input("¿Deseas purgarlos y regenerar la coleccion? (s/n): ")
            if response.lower() != 's':
                print("Operando de purga omitida por decision del usuario. Abortando.")
                return
            
            # Purgatoria de tablas locales
            ParkingSpace.query.delete()
            db.session.commit()
            print("Purga confirmada. Espacios pre-existentes eliminados radicalmente.")
        
        spaces_created = 0
        
        # Generar lotes secuenciales
        for section, config in PARKING_SECTIONS.items():
            print(f"\nGenerando la super seccion estructural {section} en memoria...")
            
            rows = 6  # Limitante máximo dictaminado a 6 filas frontales
            spaces_per_row = 5  # Matriz resultante 6 x 5 configurada nominalmente
            
            for row in range(rows):
                for pos in range(spaces_per_row):
                    # Acumular o procesar indice de espacio posicional escalar
                    space_num = row * spaces_per_row + pos + 1
                    space_number = f"{section}-{space_num:02d}"
                    
                    # Interpolar matriz topológica de geo-coordenadas
                    lat = config["base_lat"] + (row * config["lat_offset"])
                    lon = config["base_lon"] + (pos * config["lon_offset"])
                    
                    # Trazar metadatos pre-calculados al conjunto civil edilicio
                    space_coords = (lat, lon)
                    dist_b1 = haversine_distance(space_coords, BUILDINGS["building_1"])
                    dist_b2 = haversine_distance(space_coords, BUILDINGS["building_2"])
                    dist_b3 = haversine_distance(space_coords, BUILDINGS["building_3"])
                    
                    # Generar abstraccion persistente en la clase generica ParkingSpace
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
                        print(f"  > Exito nominal iterando {space_num}/30 cuadriculas en subseccion de trabajo local {section}")
        
        # Aplicacion e insercion persistente sobre disco relacional
        db.session.commit()
        
        print(f"\nReporte final: Se volcaron exitosamente un acumulado de {spaces_created} registros dimensionales de aparcamiento.")
        print("\nRESUMEN NUMERICO ESQUEMATIZADO POR SECCIONAL:")
        
        for section in ["A", "B", "C"]:
            count = ParkingSpace.query.filter_by(section=section).count()
            print(f"  Dominio {section}: {count} casilleros localizados")
        
        # Emitir rastreo preliminar de control
        print("\nEJEMPLOS INFORMATIVOS VOLCADOS EN CAPA DB:")
        examples = ParkingSpace.query.filter(
            ParkingSpace.space_number.in_(['A-01', 'A-15', 'B-01', 'B-15', 'C-01', 'C-15'])
        ).all()
        
        for space in examples:
            print(f"  {space.space_number}: ({space.lat:.6f}, {space.lon:.6f}) - "
                  f"EDIF. 1: {space.distance_to_building_1:.0f}m, "
                  f"EDIF. 2: {space.distance_to_building_2:.0f}m, "
                  f"EDIF. 3: {space.distance_to_building_3:.0f}m")

if __name__ == "__main__":
    print("INICIALIZADOR FISICO METRICO - APARCAMIENTOS DOCENTES EN GLOBO TERRITORIAL")
    print("=" * 50)
    generate_parking_spaces()
