-- ============================================================================
-- SCRIPT DE MIGRACIÓN: Sistema de Horarios ESIME
-- Versión: 2.0
-- Fecha: 2026-02-14
-- Descripción: Refactorización completa del sistema de horarios
-- ============================================================================

-- Paso 1: Backup de datos existentes
-- ============================================================================
BEGIN TRANSACTION;

-- Crear tabla temporal para backup de usuarios
CREATE TABLE IF NOT EXISTS usuarios_backup AS SELECT * FROM usuarios;

-- Paso 2: Eliminar tablas obsoletas
-- ============================================================================

DROP TABLE IF EXISTS estacionamiento;
DROP TABLE IF EXISTS horario;
DROP TABLE IF EXISTS horarios;
DROP TABLE IF EXISTS asignaturas;
DROP TABLE IF EXISTS grupos;
DROP TABLE IF EXISTS profesores;
DROP TABLE IF EXISTS salones;

-- Paso 3: Renombrar usuarios a alumnos
-- ============================================================================

ALTER TABLE usuarios RENAME TO alumnos;

-- Paso 4: Crear nuevas tablas normalizadas
-- ============================================================================

-- Tabla: materias
CREATE TABLE materias (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT UNIQUE NOT NULL,
    codigo TEXT UNIQUE,
    creditos INTEGER,
    semestre INTEGER
);

CREATE INDEX idx_materias_nombre ON materias(nombre);

-- Tabla: profesores
CREATE TABLE profesores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE,
    departamento TEXT
);

CREATE INDEX idx_profesores_nombre ON profesores(nombre);

-- Tabla: salones
CREATE TABLE salones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT UNIQUE NOT NULL,
    edificio_id INTEGER,
    capacidad INTEGER,
    tipo TEXT CHECK(tipo IN ('aula', 'laboratorio', 'auditorio')),
    FOREIGN KEY (edificio_id) REFERENCES edificios(id) ON DELETE SET NULL
);

CREATE INDEX idx_salones_nombre ON salones(nombre);
CREATE INDEX idx_salones_edificio ON salones(edificio_id);

-- Tabla: grupos
CREATE TABLE grupos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    clave TEXT UNIQUE NOT NULL,
    semestre INTEGER NOT NULL,
    turno TEXT CHECK(turno IN ('matutino', 'vespertino', 'mixto')),
    carrera TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_grupos_clave ON grupos(clave);
CREATE INDEX idx_grupos_semestre ON grupos(semestre);

-- Tabla: materias_grupos (tabla central)
CREATE TABLE materias_grupos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    materia_id INTEGER NOT NULL,
    grupo_id INTEGER NOT NULL,
    profesor_id INTEGER,
    ciclo_escolar TEXT NOT NULL DEFAULT '2025-2026',
    
    FOREIGN KEY (materia_id) REFERENCES materias(id) ON DELETE CASCADE,
    FOREIGN KEY (grupo_id) REFERENCES grupos(id) ON DELETE CASCADE,
    FOREIGN KEY (profesor_id) REFERENCES profesores(id) ON DELETE SET NULL,
    
    UNIQUE(materia_id, grupo_id, ciclo_escolar)
);

CREATE INDEX idx_mg_materia ON materias_grupos(materia_id);
CREATE INDEX idx_mg_grupo ON materias_grupos(grupo_id);
CREATE INDEX idx_mg_profesor ON materias_grupos(profesor_id);

-- Tabla: horarios
CREATE TABLE horarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    materia_grupo_id INTEGER NOT NULL,
    dia_semana INTEGER NOT NULL CHECK(dia_semana BETWEEN 1 AND 7),
    hora_inicio TIME NOT NULL,
    hora_fin TIME NOT NULL,
    salon_id INTEGER,
    tipo_clase TEXT CHECK(tipo_clase IN ('teoria', 'laboratorio', 'practica')) DEFAULT 'teoria',
    
    FOREIGN KEY (materia_grupo_id) REFERENCES materias_grupos(id) ON DELETE CASCADE,
    FOREIGN KEY (salon_id) REFERENCES salones(id) ON DELETE SET NULL,
    
    CHECK(hora_inicio < hora_fin)
);

CREATE INDEX idx_horarios_mg ON horarios(materia_grupo_id);
CREATE INDEX idx_horarios_dia ON horarios(dia_semana);
CREATE INDEX idx_horarios_salon ON horarios(salon_id);

-- Tabla: inscripciones
CREATE TABLE inscripciones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    alumno_id INTEGER NOT NULL,
    materia_grupo_id INTEGER NOT NULL,
    fecha_inscripcion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    calificacion REAL,
    estado TEXT CHECK(estado IN ('activo', 'baja', 'completado')) DEFAULT 'activo',
    
    FOREIGN KEY (alumno_id) REFERENCES alumnos(id) ON DELETE CASCADE,
    FOREIGN KEY (materia_grupo_id) REFERENCES materias_grupos(id) ON DELETE CASCADE,
    
    UNIQUE(alumno_id, materia_grupo_id)
);

CREATE INDEX idx_inscripciones_alumno ON inscripciones(alumno_id);
CREATE INDEX idx_inscripciones_mg ON inscripciones(materia_grupo_id);

-- Paso 5: Crear vista para consultas frecuentes
-- ============================================================================

CREATE VIEW vista_horarios_completos AS
SELECT 
    h.id,
    m.nombre AS materia,
    g.clave AS grupo,
    p.nombre AS profesor,
    h.dia_semana,
    h.hora_inicio,
    h.hora_fin,
    s.nombre AS salon,
    h.tipo_clase,
    mg.ciclo_escolar
FROM horarios h
JOIN materias_grupos mg ON h.materia_grupo_id = mg.id
JOIN materias m ON mg.materia_id = m.id
JOIN grupos g ON mg.grupo_id = g.id
LEFT JOIN profesores p ON mg.profesor_id = p.id
LEFT JOIN salones s ON h.salon_id = s.id;

COMMIT;

-- ============================================================================
-- FIN DEL SCRIPT DE MIGRACIÓN
-- ============================================================================
