"""
Script para crear usuario administrador en la base de datos
"""
import psycopg
from werkzeug.security import generate_password_hash
import os
from dotenv import load_dotenv

load_dotenv()

# Configuración de base de datos
DB_CONFIG = {
    'host': os.environ.get('DB_HOST', 'localhost'),
    'dbname': os.environ.get('DB_NAME', 'judicial_blockchain'),
    'user': os.environ.get('DB_USER', 'postgres'),
    'password': os.environ.get('DB_PASSWORD', 'postgres'),
    'port': os.environ.get('DB_PORT', '5432')
}

def create_admin_user():
    """Crea el usuario administrador"""
    try:
        conn = psycopg.connect(**DB_CONFIG)
        cur = conn.cursor()
        
        # Verificar si el usuario ya existe
        cur.execute("SELECT id FROM users WHERE username = 'admin'")
        existing_user = cur.fetchone()
        
        if existing_user:
            print("Usuario 'admin' ya existe. Actualizando contraseña...")
            password_hash = generate_password_hash('admin123')
            cur.execute(
                "UPDATE users SET password_hash = %s WHERE username = 'admin'",
                (password_hash,)
            )
        else:
            print("Creando usuario 'admin'...")
            password_hash = generate_password_hash('admin123')
            cur.execute("""
                INSERT INTO users (username, email, password_hash, role, full_name)
                VALUES (%s, %s, %s, %s, %s)
            """, ('admin', 'admin@judicial.com', password_hash, 'admin', 'Administrador del Sistema'))
        
        conn.commit()
        cur.close()
        conn.close()
        
        print("✅ Usuario admin creado/actualizado exitosamente")
        print("📝 Credenciales:")
        print("   Usuario: admin")
        print("   Contraseña: admin123")
        
    except psycopg.Error as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    create_admin_user()
