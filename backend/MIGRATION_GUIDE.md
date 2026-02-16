# 📋 Guía de Migración - Sistema de Horarios ESIME

## 🎯 Resumen

Esta guía documenta el proceso completo de refactorización de la base de datos del sistema de horarios, transformando una estructura desnormalizada en una arquitectura normalizada (3NF) robusta y escalable.

## 📁 Archivos Generados

### 1. **Documentación**
- `database_refactoring_plan.md` - Plan técnico completo con análisis y justificaciones

### 2. **Scripts de Migración**
- `backend/migrations/migrate_horarios_v2.sql` - Script SQL de migración
- `backend/scripts/import_horarios.py` - Script Python de importación de datos
- `backend/scripts/run_migration.sh` - Script bash de ejecución completa

### 3. **Modelos Actualizados**
- `backend/models.py` - Modelos Flask SQLAlchemy refactorizados

## 🚀 Ejecución de la Migración

### Opción 1: Ejecución Automática (Recomendada)

```bash
cd /Users/alexsosa/Documentos/Navegación_ESIME
./backend/scripts/run_migration.sh
```

Este script ejecuta automáticamente:
1. ✅ Verificación de archivos
2. ✅ Backup de base de datos
3. ✅ Migración SQL
4. ✅ Importación de datos
5. ✅ Verificación de integridad

### Opción 2: Ejecución Manual

#### Paso 1: Backup
```bash
cp backend/instance/campus.db backend/instance/campus_backup.db
```

#### Paso 2: Migración SQL
```bash
sqlite3 backend/instance/campus.db < backend/migrations/migrate_horarios_v2.sql
```

#### Paso 3: Importación de Datos
```bash
python3 backend/scripts/import_horarios.py
```

## 📊 Cambios en la Estructura

### Tablas Eliminadas
- ❌ `estacionamiento` (duplicada)
- ❌ `horario` (legacy)
- ❌ `horarios` (antigua)
- ❌ `asignaturas` (refactorizada)
- ❌ `grupos` (refactorizada)
- ❌ `profesores` (refactorizada)
- ❌ `salones` (refactorizada)
- ❌ `usuarios` (renombrada)

### Tablas Nuevas/Actualizadas
- ✅ `alumnos` (renombrada de usuarios)
- ✅ `materias` (nueva estructura)
- ✅ `profesores` (nueva estructura)
- ✅ `salones` (nueva estructura con FK a edificios)
- ✅ `grupos` (nueva estructura con metadata)
- ✅ `materias_grupos` (tabla central - NUEVA)
- ✅ `horarios` (normalizada - NUEVA)
- ✅ `inscripciones` (tabla puente - NUEVA)

### Tablas Mantenidas
- ✅ `edificios`
- ✅ `caminos`
- ✅ `parking_spaces`
- ✅ `parking_reservations`
- ✅ `parking_history`
- ✅ `saved_places`

## 🔍 Verificación Post-Migración

### Consultas de Verificación

```sql
-- Contar registros por tabla
SELECT 'Materias' as tabla, COUNT(*) as total FROM materias
UNION ALL
SELECT 'Profesores', COUNT(*) FROM profesores
UNION ALL
SELECT 'Grupos', COUNT(*) FROM grupos
UNION ALL
SELECT 'Salones', COUNT(*) FROM salones
UNION ALL
SELECT 'Materias-Grupos', COUNT(*) FROM materias_grupos
UNION ALL
SELECT 'Horarios', COUNT(*) FROM horarios;

-- Ver horarios completos (usando vista)
SELECT * FROM vista_horarios_completos LIMIT 10;

-- Verificar integridad referencial
PRAGMA foreign_key_check;
```

### Consultas de Ejemplo

```sql
-- Horario de un grupo específico
SELECT 
    m.nombre as materia,
    p.nombre as profesor,
    CASE h.dia_semana
        WHEN 1 THEN 'Lunes'
        WHEN 2 THEN 'Martes'
        WHEN 3 THEN 'Miércoles'
        WHEN 4 THEN 'Jueves'
        WHEN 5 THEN 'Viernes'
    END as dia,
    h.hora_inicio || ' - ' || h.hora_fin as horario,
    s.nombre as salon
FROM horarios h
JOIN materias_grupos mg ON h.materia_grupo_id = mg.id
JOIN materias m ON mg.materia_id = m.id
JOIN grupos g ON mg.grupo_id = g.id
LEFT JOIN profesores p ON mg.profesor_id = p.id
LEFT JOIN salones s ON h.salon_id = s.id
WHERE g.clave = '1CM54'
ORDER BY h.dia_semana, h.hora_inicio;

-- Materias de un profesor
SELECT DISTINCT
    m.nombre as materia,
    g.clave as grupo,
    COUNT(h.id) as sesiones_semanales
FROM materias_grupos mg
JOIN materias m ON mg.materia_id = m.id
JOIN grupos g ON mg.grupo_id = g.id
JOIN profesores p ON mg.profesor_id = p.id
LEFT JOIN horarios h ON mg.id = h.materia_grupo_id
WHERE p.nombre LIKE '%Pablo Gopar%'
GROUP BY m.nombre, g.clave;

-- Ocupación de salones
SELECT 
    s.nombre as salon,
    COUNT(h.id) as horas_ocupadas,
    s.tipo
FROM salones s
LEFT JOIN horarios h ON s.id = h.salon_id
GROUP BY s.id
ORDER BY horas_ocupadas DESC;
```

## 🔄 Rollback (Si es necesario)

Si algo sale mal durante la migración:

```bash
# Restaurar backup
cp backend/instance/campus_backup.db backend/instance/campus.db

# Reiniciar aplicación
./run_app.sh
```

## 📝 Actualización de Código de Aplicación

### Cambios Necesarios en Endpoints

Los endpoints existentes que usan `Usuario` deben actualizarse a `Alumno`:

```python
# ANTES
from models import Usuario

user = Usuario.query.filter_by(boleta=boleta).first()

# DESPUÉS
from models import Alumno

alumno = Alumno.query.filter_by(boleta=boleta).first()
```

### Nuevos Endpoints Sugeridos

```python
# Obtener horario de un alumno
@app.route('/api/alumnos/<boleta>/horario', methods=['GET'])
def get_alumno_horario(boleta):
    alumno = Alumno.query.filter_by(boleta=boleta).first()
    if not alumno:
        return jsonify({"error": "Alumno no encontrado"}), 404
    
    horarios = []
    for inscripcion in alumno.inscripciones:
        for horario in inscripcion.materia_grupo.horarios:
            horarios.append(horario.to_dict())
    
    return jsonify(horarios)

# Obtener materias de un grupo
@app.route('/api/grupos/<clave>/materias', methods=['GET'])
def get_grupo_materias(clave):
    grupo = Grupo.query.filter_by(clave=clave).first()
    if not grupo:
        return jsonify({"error": "Grupo no encontrado"}), 404
    
    materias = []
    for mg in grupo.materias_grupos:
        materias.append({
            "materia": mg.materia.nombre,
            "profesor": mg.profesor.nombre if mg.profesor else None,
            "horarios": [h.to_dict() for h in mg.horarios]
        })
    
    return jsonify(materias)
```

## ⚠️ Notas Importantes

1. **Backup Automático**: El script crea un backup con timestamp antes de migrar
2. **Transacciones**: La migración usa transacciones para garantizar atomicidad
3. **Foreign Keys**: SQLite requiere `PRAGMA foreign_keys = ON` para validación
4. **Datos Existentes**: Los alumnos existentes se preservan (tabla renombrada)
5. **Parking**: Las tablas de parking se actualizan para usar FK a `alumnos`

## 📈 Métricas Esperadas

Después de la importación, deberías ver aproximadamente:

- **Materias**: ~50-80 materias únicas
- **Profesores**: ~40-60 profesores
- **Grupos**: ~50-70 grupos
- **Salones**: ~100-150 salones
- **Materias-Grupos**: ~200-300 combinaciones
- **Horarios**: ~800-1200 sesiones semanales

## 🎓 Próximos Pasos

1. ✅ Ejecutar migración
2. ✅ Verificar datos
3. ⏭️ Actualizar endpoints de API
4. ⏭️ Crear endpoints de inscripciones
5. ⏭️ Implementar UI de consulta de horarios
6. ⏭️ Agregar validación de conflictos
7. ⏭️ Implementar sistema de notificaciones

## 📞 Soporte

Si encuentras problemas durante la migración:

1. Revisa los logs de error
2. Verifica que todos los archivos existan
3. Confirma que el backup se creó correctamente
4. Consulta `database_refactoring_plan.md` para detalles técnicos

---

**Versión:** 2.0  
**Fecha:** 2026-02-14  
**Estado:** ✅ Listo para ejecución
