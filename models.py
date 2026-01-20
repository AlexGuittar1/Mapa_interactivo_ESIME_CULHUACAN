from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class EdificioDB(db.Model):
    __tablename__ = "edificios"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), unique=True, nullable=False)
    latitud = db.Column(db.Float, nullable=False)
    longitud = db.Column(db.Float, nullable=False) # Coordenada central o de entrada

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "lat": self.latitud,
            "lon": self.longitud
        }

class CaminoDB(db.Model):
    __tablename__ = "caminos"

    id = db.Column(db.Integer, primary_key=True)
    origen = db.Column(db.String(50), nullable=False)
    destino = db.Column(db.String(50), nullable=False)
    distancia = db.Column(db.Float, nullable=False)

    def to_dict(self):
        return {
            "origen": self.origen,
            "destino": self.destino,
            "distancia": self.distancia
        }

# --- Nuevos Modelos ---

class Usuario(db.Model):
    __tablename__ = "usuarios"
    
    id = db.Column(db.Integer, primary_key=True)
    boleta = db.Column(db.String(20), unique=True, nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    carrera = db.Column(db.String(100))
    # vehiculo: 'auto', 'moto', 'bici', 'ninguno'
    vehiculo = db.Column(db.String(20), default='ninguno') 

    def to_dict(self):
        return {
            "boleta": self.boleta,
            "nombre": self.nombre,
            "carrera": self.carrera,
            "vehiculo": self.vehiculo
        }

class Salon(db.Model):
    __tablename__ = "salones"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(20), nullable=False) # e.g. "1101"
    edificio_id = db.Column(db.Integer, db.ForeignKey('edificios.id'), nullable=False)
    
    edificio = db.relationship('EdificioDB', backref=db.backref('salones', lazy=True))

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "edificio": self.edificio.nombre
        }

class Horario(db.Model):
    __tablename__ = "horarios"

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    materia = db.Column(db.String(100), nullable=False)
    salon_id = db.Column(db.Integer, db.ForeignKey('salones.id'), nullable=False)
    dia = db.Column(db.String(15), nullable=False) # Lunes, Martes...
    hora_inicio = db.Column(db.String(10), nullable=False) # "07:00"
    hora_fin = db.Column(db.String(10), nullable=False)   # "08:30"

    salon = db.relationship('Salon')
    usuario = db.relationship('Usuario', backref=db.backref('clases', lazy=True))

    def to_dict(self):
        return {
            "materia": self.materia,
            "sala": self.salon.nombre,
            "edificio": self.salon.edificio.nombre,
            "dia": self.dia,
            "hora": f"{self.hora_inicio} - {self.hora_fin}"
        }

class Estacionamiento(db.Model):
    __tablename__ = "estacionamiento"

    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.String(10), unique=True)
    ocupado = db.Column(db.Boolean, default=False)
    latitud = db.Column(db.Float)
    longitud = db.Column(db.Float)
    tipo = db.Column(db.String(20), default='general') # alumnos, profesores, motos

    def to_dict(self):
        return {
            "id": self.id,
            "numero": self.numero,
            "ocupado": self.ocupado,
            "coords": [self.latitud, self.longitud],
            "tipo": self.tipo
        }
