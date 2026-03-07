"""
ARCHIVO: seed_inscripciones.py

SCRIPT DE POBLACION DE DATOS DE PRUEBA (INSCRIPCIONES)

Rellena forzosamente registros matriculares para perfiles precargados locales
permitiendo el testeo estructural local.
"""
from app import app, db
from models import Alumno, Materia, Grupo, MateriaGrupo, Inscripcion
import sys

def seed_data():
    """
    RUTINA DE INYECCION MATRICULAR
    """
    with app.app_context():
        alumnos = {
            'Frias Rodriguez Adrian': Alumno.query.filter_by(nombre='Frias Rodriguez Adrian').first(),
            'Sosa Hernández Omar Alejandro': Alumno.query.filter_by(nombre='Sosa Hernádez Omar Alejandro').first()
        }
        
        for name, a in alumnos.items():
            if not a:
                print(f"Error: Alumno {name} not found.")
                sys.exit(1)

        materias_data = [
            {'nombre': 'Lenguajes de Bajo Nivel', 'codigo': 'LBN-01', 'creditos': 8, 'semestre': 3},
            {'nombre': 'Ecuaciones Diferenciales', 'codigo': 'ED-01', 'creditos': 8, 'semestre': 3},
            {'nombre': 'Humanidades III', 'codigo': 'HUM-03', 'creditos': 6, 'semestre': 3},
            {'nombre': 'Estructuras de Datos', 'codigo': 'EDD-01', 'creditos': 8, 'semestre': 3}
        ]
        
        grupos_data = [
            {'clave': '3CV14', 'semestre': 3, 'turno': 'vespertino', 'carrera': 'Ingeniería en Computación'},
            {'clave': '3CV31', 'semestre': 3, 'turno': 'vespertino', 'carrera': 'Ingeniería en Computación'},
            {'clave': '3CV26', 'semestre': 3, 'turno': 'vespertino', 'carrera': 'Ingeniería en Computación'},
            {'clave': '3CV35', 'semestre': 3, 'turno': 'vespertino', 'carrera': 'Ingeniería en Computación'}
        ]

        # INSERCION Y MATRICULACION DE MATERIAS
        materias = {}
        for md in materias_data:
            m = Materia.query.filter((Materia.nombre == md['nombre']) | (Materia.nombre == 'Humanidades') | (Materia.nombre == 'Estructura de Datos')).first() # try generic match
            if not m:
                m = Materia(nombre=md['nombre'], codigo=md['codigo'], creditos=md['creditos'], semestre=md['semestre'])
                db.session.add(m)
                db.session.commit() # commit to get ID
            materias[md['nombre']] = m

        # EXTRACCION TOLERANTE POR REGEX O PARSEO APROXIMADO
        # Cargar las requeridas exactamente por nombre asumiendo posibles variaciones menores en su inyeccion iterativa
        materias['Lenguajes de Bajo Nivel'] = Materia.query.filter(Materia.nombre.ilike('%Lenguajes de Bajo Nivel%')).first() or materias['Lenguajes de Bajo Nivel']
        materias['Ecuaciones Diferenciales'] = Materia.query.filter(Materia.nombre.ilike('%Ecuaciones Diferenciales%')).first() or materias['Ecuaciones Diferenciales']
        materias['Humanidades'] = Materia.query.filter(Materia.nombre.ilike('%Humanidades%')).first() or materias['Humanidades III']
        materias['Estructura de Datos'] = Materia.query.filter(Materia.nombre.ilike('%Estructura%Dato%')).first() or materias['Estructuras de Datos']

        # CREACION DE GRUPOS DISPONIBLES
        grupos = {}
        for gd in grupos_data:
            g = Grupo.query.filter_by(clave=gd['clave']).first()
            if not g:
                g = Grupo(clave=gd['clave'], semestre=gd['semestre'], turno=gd['turno'], carrera=gd['carrera'])
                db.session.add(g)
                db.session.commit()
            grupos[gd['clave']] = g

        # HOMOLOGACION DE MATERIAS CONTRA GRUPOS DISPONIBLES
        relaciones = [
            ('Lenguajes de Bajo Nivel', '3CV14'),
            ('Ecuaciones Diferenciales', '3CV31'),
            ('Humanidades', '3CV26'),
            ('Estructura de Datos', '3CV35')
        ]

        mg_dict = {}
        for m_nombre, g_clave in relaciones:
            m_id = materias[m_nombre].id
            g_id = grupos[g_clave].id
            
            mg = MateriaGrupo.query.filter_by(materia_id=m_id, grupo_id=g_id, ciclo_escolar='2025-2026').first()
            if not mg:
                mg = MateriaGrupo(materia_id=m_id, grupo_id=g_id, ciclo_escolar='2025-2026')
                db.session.add(mg)
                db.session.commit()
            mg_dict[f"{m_nombre}-{g_clave}"] = mg

        # COMPROBACION E INSCRIPCION CERRADA DE ALUMNOS (PERFILES)
        for name, a in alumnos.items():
            for m_nombre, g_clave in relaciones:
                mg = mg_dict[f"{m_nombre}-{g_clave}"]
                insc = Inscripcion.query.filter_by(alumno_id=a.id, materia_grupo_id=mg.id).first()
                if not insc:
                    insc = Inscripcion(alumno_id=a.id, materia_grupo_id=mg.id, estado='activo')
                    db.session.add(insc)
                    db.session.commit()

        # DISPERSION ALEATORIA E INYECCION DE HORARIOS CLASE 
        import random
        from models import Horario
        for name, mg in mg_dict.items():
            for dia in range(1, 6): # 1=Lunes, 5=Viernes
                dia_hora = Horario.query.filter_by(materia_grupo_id=mg.id, dia_semana=dia).first()
                if not dia_hora:
                    horas = ["15:00", "16:30", "18:00", "19:30"]
                    h = random.choice(horas)
                    from datetime import datetime, timedelta
                    h_dt = datetime.strptime(h, "%H:%M")
                    h_fin = (h_dt + timedelta(hours=1, minutes=30)).strftime("%H:%M")

                    nuevo_h = Horario(
                        materia_grupo_id=mg.id,
                        dia_semana=dia,
                        hora_inicio=h,
                        hora_fin=h_fin,
                        salon_id=1, # Default salon / dummy
                        tipo_clase='teoria'
                    )
                    db.session.add(nuevo_h)
                    db.session.commit()
        
        print("\nINDEXACION Y POBLACION DE DATA FINALIZADA CON EXITO.")

if __name__ == "__main__":
    seed_data()
