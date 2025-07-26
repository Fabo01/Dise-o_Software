-- Script de inicialización para PostgreSQL
-- Este script se ejecuta cuando se crea el contenedor por primera vez

-- Crear extensiones útiles
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- Configurar encoding
SET default_text_search_config = 'spanish';

-- Crear esquemas adicionales si es necesario
-- CREATE SCHEMA IF NOT EXISTS analytics;
-- CREATE SCHEMA IF NOT EXISTS reports;

-- Log de inicialización completada
-- Nota: pg_settings es una vista de solo lectura, no se puede modificar directamente
