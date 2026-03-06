-- ============================================
-- Migración V3: Campos de Integración Institucional
-- ============================================
-- Fecha: 2026-03-02
-- Descripción: Agrega campos para soportar integración
-- con Azure AD y sistemas institucionales externos.
--
-- IMPORTANTE: Esta migración es NO DESTRUCTIVA.
-- No modifica datos existentes, solo agrega columnas.
-- ============================================

-- Campo para ID externo (Azure Object ID, etc.)
ALTER TABLE alumnos ADD COLUMN institutional_id VARCHAR(100) UNIQUE;

-- Proveedor de autenticación: 'local' | 'azure_ad'
ALTER TABLE alumnos ADD COLUMN auth_provider VARCHAR(20) DEFAULT 'local';

-- Registro de último acceso (auditoría)
ALTER TABLE alumnos ADD COLUMN last_login DATETIME;

-- Bandera de sincronización con sistema externo
ALTER TABLE alumnos ADD COLUMN is_synced BOOLEAN DEFAULT 0;

-- Índices para búsqueda eficiente
CREATE INDEX IF NOT EXISTS idx_alumnos_email ON alumnos(email);
CREATE INDEX IF NOT EXISTS idx_alumnos_institutional_id ON alumnos(institutional_id);
CREATE INDEX IF NOT EXISTS idx_alumnos_auth_provider ON alumnos(auth_provider);
