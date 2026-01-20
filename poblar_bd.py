from app import app, db
from models import Usuario, EdificioDB, CaminoDB, Salon, Horario, Estacionamiento

def poblar():
    with app.app_context():
        db.create_all()
        
        # Limpiar datos existentes (opcional, para resetear)
        # db.drop_all() 
        # db.create_all()

        if EdificioDB.query.first():
            print("La base de datos ya tiene datos.")
            return

        print("Poblando Base de Datos...")

        # 1. Edificios
        edificios = [
            {"nombre": "Edificio 1", "lat": 19.311311, "lon": -99.111867},
            {"nombre": "Edificio 2", "lat": 19.311500, "lon": -99.112000},
            {"nombre": "Edificio 3", "lat": 19.311200, "lon": -99.112200},
            {"nombre": "Biblioteca", "lat": 19.311000, "lon": -99.111500},
            {"nombre": "Cafeteria", "lat": 19.311400, "lon": -99.111400},
            {"nombre": "Estacionamiento", "lat": 19.311800, "lon": -99.112500},
        ]
        
        objs_edificios = {}
        for e in edificios:
            nuevo = EdificioDB(nombre=e["nombre"], latitud=e["lat"], longitud=e["lon"])
            db.session.add(nuevo)
            objs_edificios[e["nombre"]] = nuevo
        
        db.session.commit() # Para tener IDs
        
        # 2. Salones (Ejemplo Edificio 1)
        e1_id = objs_edificios["Edificio 1"].id
        salones = ["1101", "1102", "1103"]
        
        objs_salones = {}
        for s in salones:
            nuevo = Salon(nombre=s, edificio_id=e1_id)
            db.session.add(nuevo)
            objs_salones[s] = nuevo
            
        db.session.commit()

        # 3. Usuario Demo
        student = Usuario(
            boleta="2020640001",
            nombre="Alex Sosa",
            carrera="Ing. Sistemas Computacionales",
            vehiculo="auto"
        )
        db.session.add(student)
        db.session.commit()

        # 4. Horario Demo (Lunes)
        horario = Horario(
            usuario_id=student.id,
            materia="Inteligencia Artificial",
            salon_id=objs_salones["1101"].id,
            dia="Lunes",
            hora_inicio="07:00",
            hora_fin="08:30"
        )
        db.session.add(horario)
        
        horario2 = Horario(
             usuario_id=student.id,
             materia="Compiladores",
             salon_id=objs_salones["1102"].id,
             dia="Lunes",
             hora_inicio="08:30",
             hora_fin="10:00"
        )
        db.session.add(horario2)


        # 5. Estacionamiento
        for i in range(1, 11):
            ocupado = (i % 3 == 0) # Mock ocupacion
            slot = Estacionamiento(
                numero=f"E-{i}",
                ocupado=ocupado,
                latitud=19.311800 + (i*0.00001), 
                longitud=-99.112500,
                tipo="alumnos"
            )
            db.session.add(slot)

        # 6. Caminos (Grafo)
        caminos = [
            ("Edificio 1", "Edificio 2", 50),
            ("Edificio 2", "Edificio 3", 40),
            ("Edificio 1", "Biblioteca", 100),
            ("Biblioteca", "Cafeteria", 60),
            ("Cafeteria", "Edificio 1", 30),
            ("Edificio 2", "Estacionamiento", 150)
        ]
        
        for o, d, dist in caminos:
            nuevo = CaminoDB(origen=o, destino=d, distancia=dist)
            db.session.add(nuevo)
            
        db.session.commit()
        print("Datos cargados exitosamente.")

if __name__ == "__main__":
    poblar()
