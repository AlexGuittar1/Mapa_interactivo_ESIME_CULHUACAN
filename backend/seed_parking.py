import os
import sys

# Ajustar PYTHONPATH para poder importar models
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from models import ParkingSpace, ParkingSection, ParkingHistory

def seed_parking():
    with app.app_context():
        print("Borrando historial antiguo...")
        ParkingHistory.query.delete()
        print("Borrando espacios antiguos...")
        ParkingSpace.query.delete()
        print("Borrando secciones antiguas...")
        ParkingSection.query.delete()
        
        # 1. Crear Secciones
        print("Creando nuevas Secciones...")
        sections_data = [
            {"id": 1, "name": "Sección 1", "total": 90},
            {"id": 2, "name": "Sección 2", "total": 90},
            {"id": 3, "name": "Sección 3", "total": 85},
            {"id": 4, "name": "Sección 4", "total": 80},
        ]
        
        sections = {}
        for s_data in sections_data:
            sec = ParkingSection(name=s_data["name"], total_spaces=s_data["total"])
            db.session.add(sec)
            db.session.commit() # Commit to get ID
            sections[s_data["id"]] = sec.id
            
        # 2. Generar Espacios para cada sección
        print("Generando 345 espacios totales...")
        for s_data in sections_data:
            sec_id = sections[s_data["id"]]
            total = s_data["total"]
            for i in range(1, total + 1):
                # Generador básico de coordenadas y row
                space = ParkingSpace(
                    space_number=f"S{s_data['id']}-{i:03d}",
                    section_id=sec_id,
                    row_number=(i // 10) + 1,
                    position_number=(i % 10) + 1,
                    lat=19.329 + (s_data['id'] * 0.001), 
                    lon=-99.112 + (i * 0.0001),
                    status="available"
                )
                db.session.add(space)
                
        db.session.commit()
        print("✅ Generación de Parking Automática Completada.")
        print(f"Total Secciones: {ParkingSection.query.count()}")
        print(f"Total Espacios: {ParkingSpace.query.count()}")

if __name__ == "__main__":
    seed_parking()
