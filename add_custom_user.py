from app import app, db
from models import Usuario

def agregar_usuario():
    with app.app_context():
        boleta = "2025350215"
        nombre = "Alex Sosa"
        
        # Check if exists
        e = Usuario.query.filter_by(boleta=boleta).first()
        if e:
            print(f"El usuario {nombre} ({boleta}) ya existe.")
            return

        nuevo = Usuario(
            boleta=boleta,
            nombre=nombre,
            carrera="Ingeniería en Sistemas Computacionales", # Default assumption
            vehiculo="auto" # Default
        )
        db.session.add(nuevo)
        db.session.commit()
        print(f"Usuario agregado: {nombre} - {boleta}")

if __name__ == "__main__":
    agregar_usuario()
