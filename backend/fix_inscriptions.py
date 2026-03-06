from app import app, db
from models import Alumno, MateriaGrupo, Materia, Inscripcion

def fix_inscriptions():
    with app.app_context():
        # 1. Localizar los usuarios por nombre (Asegurándonos del typo en DB "Hernádez")
        target_names = ["Frias Rodriguez Adrian", "Sosa Hernádez Omar Alejandro"]
        alumnos = Alumno.query.filter(Alumno.nombre.in_(target_names)).all()
        
        if not alumnos:
            print("No se encontraron los alumnos objetivo.")
            return

        alumno_ids = [a.id for a in alumnos]
        print(f"Alumnos encontrados: {[a.nombre for a in alumnos]} (IDs: {alumno_ids})")

        # 2. Localizar la materia específica (Búsqueda permisiva por "HUMANIDADES I")
        materia = Materia.query.filter(Materia.nombre.like("%HUMANIDADES I%")).first()

        if not materia:
            print("No se encontró la materia: HUMANIDADES I")
            return
            
        print(f"Materia encontrada: {materia.nombre} (ID: {materia.id})")

        # 3. Buscar los MateriaGrupo asociados a esta materia
        materia_grupos = MateriaGrupo.query.filter_by(materia_id=materia.id).all()
        mg_ids = [mg.id for mg in materia_grupos]
        
        if not mg_ids:
            print("No se encontraron grupos para esta materia.")
            return

        print(f"Grupos de la materia encontrados (IDs: {mg_ids})")

        # 4. Eliminar las inscripciones correspondientes
        inscripciones_a_borrar = Inscripcion.query.filter(
            Inscripcion.alumno_id.in_(alumno_ids),
            Inscripcion.materia_grupo_id.in_(mg_ids)
        ).all()

        if not inscripciones_a_borrar:
            print("No se encontraron inscripciones para eliminar. Ya está limpio.")
            return
            
        print(f"Encontradas {len(inscripciones_a_borrar)} inscripciones para borrar.")
        
        for ins in inscripciones_a_borrar:
            print(f"Borrando inscripción: Alumno ID {ins.alumno_id} -> MateriaGrupo ID {ins.materia_grupo_id}")
            db.session.delete(ins)
            
        db.session.commit()
        print("¡Inscripciones eliminadas exitosamente! Base de datos actualizada.")

if __name__ == "__main__":
    fix_inscriptions()
