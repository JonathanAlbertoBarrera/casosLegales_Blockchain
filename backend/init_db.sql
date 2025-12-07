-- Script de inicialización para PostgreSQL
-- Crear base de datos y tablas necesarias

-- Crear base de datos (ejecutar como superusuario)
-- CREATE DATABASE judicial_blockchain;

-- Conectar a la base de datos
\c judicial_blockchain;

-- Tabla de usuarios
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL CHECK (role IN ('admin', 'judge', 'clerk', 'lawyer', 'viewer')),
    full_name VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de sesiones (opcional)
CREATE TABLE IF NOT EXISTS sessions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    session_token VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP NOT NULL
);

-- Índices para mejor rendimiento
CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_sessions_token ON sessions(session_token);
CREATE INDEX IF NOT EXISTS idx_sessions_user_id ON sessions(user_id);

-- Insertar usuario administrador por defecto (password: admin123)
INSERT INTO users (username, email, password_hash, role, full_name)
VALUES (
    'admin',
    'admin@judicial.com',
    'scrypt:32768:8:1$9fYHQnJq2KjVLvMp$d8b4c8b5e5c7f2e8a6d8b4c8b5e5c7f2e8a6d8b4c8b5e5c7f2e8a6d8b4c8b5e5c7f2e8a6d8b4c8b5e5c7f2e8a6d8b4c8b5e5c7f2',
    'admin',
    'Administrador del Sistema'
) ON CONFLICT (username) DO NOTHING;

-- Insertar algunos usuarios de prueba
INSERT INTO users (username, email, password_hash, role, full_name)
VALUES
    ('juez_rodriguez', 'maria.rodriguez@judicial.com', 'scrypt:32768:8:1$9fYHQnJq2KjVLvMp$d8b4c8b5e5c7f2e8a6d8b4c8b5e5c7f2e8a6d8b4c8b5e5c7f2e8a6d8b4c8b5e5c7f2e8a6d8b4c8b5e5c7f2e8a6d8b4c8b5e5c7f2', 'judge', 'María Rodríguez'),
    ('secretaria', 'secretaria@judicial.com', 'scrypt:32768:8:1$9fYHQnJq2KjVLvMp$d8b4c8b5e5c7f2e8a6d8b4c8b5e5c7f2e8a6d8b4c8b5e5c7f2e8a6d8b4c8b5e5c7f2e8a6d8b4c8b5e5c7f2e8a6d8b4c8b5e5c7f2', 'clerk', 'Ana Secretaria'),
    ('abogado', 'abogado@bufete.com', 'scrypt:32768:8:1$9fYHQnJq2KjVLvMp$d8b4c8b5e5c7f2e8a6d8b4c8b5e5c7f2e8a6d8b4c8b5e5c7f2e8a6d8b4c8b5e5c7f2e8a6d8b4c8b5e5c7f2e8a6d8b4c8b5e5c7f2', 'lawyer', 'Carlos Abogado')
ON CONFLICT (username) DO NOTHING;

-- Función para actualizar timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Trigger para actualizar automáticamente updated_at
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Comentarios sobre las tablas
COMMENT ON TABLE users IS 'Tabla de usuarios del sistema judicial';
COMMENT ON TABLE sessions IS 'Tabla de sesiones activas';

COMMENT ON COLUMN users.role IS 'Roles: admin, judge, clerk, lawyer, viewer';
COMMENT ON COLUMN users.password_hash IS 'Hash de contraseña usando Werkzeug';

-- Mostrar resultado
SELECT 'Base de datos inicializada correctamente' AS status;
SELECT COUNT(*) AS total_usuarios FROM users;
