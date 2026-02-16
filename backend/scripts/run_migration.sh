#!/bin/bash
# ============================================================================
# Script de Ejecución Completa - Refactorización de Base de Datos
# Versión: 2.0
# Fecha: 2026-02-14
# ============================================================================

set -e  # Salir si hay errores

echo "============================================================================"
echo "REFACTORIZACIÓN DE BASE DE DATOS - SISTEMA DE HORARIOS ESIME"
echo "============================================================================"
echo ""

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Rutas
DB_PATH="backend/instance/campus.db"
DB_BACKUP="backend/instance/campus_backup_$(date +%Y%m%d_%H%M%S).db"
MIGRATION_SQL="backend/migrations/migrate_horarios_v2.sql"
IMPORT_SCRIPT="backend/scripts/import_horarios.py"
SQL_DATA="backend/instance/horarios_sqlite.sql"

# Paso 1: Verificar archivos
echo -e "${YELLOW}[1/5] Verificando archivos...${NC}"
if [ ! -f "$DB_PATH" ]; then
    echo -e "${RED}❌ Error: Base de datos no encontrada: $DB_PATH${NC}"
    exit 1
fi

if [ ! -f "$MIGRATION_SQL" ]; then
    echo -e "${RED}❌ Error: Script de migración no encontrado: $MIGRATION_SQL${NC}"
    exit 1
fi

if [ ! -f "$IMPORT_SCRIPT" ]; then
    echo -e "${RED}❌ Error: Script de importación no encontrado: $IMPORT_SCRIPT${NC}"
    exit 1
fi

if [ ! -f "$SQL_DATA" ]; then
    echo -e "${RED}❌ Error: Archivo de datos no encontrado: $SQL_DATA${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Todos los archivos encontrados${NC}"
echo ""

# Paso 2: Backup de base de datos
echo -e "${YELLOW}[2/5] Creando backup de base de datos...${NC}"
cp "$DB_PATH" "$DB_BACKUP"
echo -e "${GREEN}✅ Backup creado: $DB_BACKUP${NC}"
echo ""

# Paso 3: Ejecutar migración SQL
echo -e "${YELLOW}[3/5] Ejecutando migración SQL...${NC}"
sqlite3 "$DB_PATH" < "$MIGRATION_SQL"
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Migración SQL completada${NC}"
else
    echo -e "${RED}❌ Error en migración SQL${NC}"
    echo -e "${YELLOW}⚠️  Restaurando backup...${NC}"
    cp "$DB_BACKUP" "$DB_PATH"
    exit 1
fi
echo ""

# Paso 4: Importar datos
echo -e "${YELLOW}[4/5] Importando datos de horarios...${NC}"
python3 "$IMPORT_SCRIPT" "$DB_PATH" "$SQL_DATA"
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Importación completada${NC}"
else
    echo -e "${RED}❌ Error en importación${NC}"
    echo -e "${YELLOW}⚠️  Restaurando backup...${NC}"
    cp "$DB_BACKUP" "$DB_PATH"
    exit 1
fi
echo ""

# Paso 5: Verificación
echo -e "${YELLOW}[5/5] Verificando integridad de datos...${NC}"
echo ""
echo "Conteo de registros:"
echo "-------------------"
sqlite3 "$DB_PATH" "SELECT 'Alumnos: ' || COUNT(*) FROM alumnos;"
sqlite3 "$DB_PATH" "SELECT 'Materias: ' || COUNT(*) FROM materias;"
sqlite3 "$DB_PATH" "SELECT 'Profesores: ' || COUNT(*) FROM profesores;"
sqlite3 "$DB_PATH" "SELECT 'Grupos: ' || COUNT(*) FROM grupos;"
sqlite3 "$DB_PATH" "SELECT 'Salones: ' || COUNT(*) FROM salones;"
sqlite3 "$DB_PATH" "SELECT 'Materias-Grupos: ' || COUNT(*) FROM materias_grupos;"
sqlite3 "$DB_PATH" "SELECT 'Horarios: ' || COUNT(*) FROM horarios;"
sqlite3 "$DB_PATH" "SELECT 'Inscripciones: ' || COUNT(*) FROM inscripciones;"
echo ""

echo "============================================================================"
echo -e "${GREEN}✅ REFACTORIZACIÓN COMPLETADA EXITOSAMENTE${NC}"
echo "============================================================================"
echo ""
echo "Próximos pasos:"
echo "1. Reiniciar la aplicación Flask"
echo "2. Probar endpoints de horarios"
echo "3. Verificar que los datos se muestren correctamente"
echo ""
echo "Backup disponible en: $DB_BACKUP"
echo "============================================================================"
