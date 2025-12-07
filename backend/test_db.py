import os
from dotenv import load_dotenv
import psycopg

load_dotenv()

DB_CONFIG = {
    'host': os.environ.get('DB_HOST', 'localhost'),
    'database': os.environ.get('DB_NAME', 'judicial_blockchain'),
    'user': os.environ.get('DB_USER', 'postgres'),
    'password': os.environ.get('DB_PASSWORD', 'postgres'),
    'port': os.environ.get('DB_PORT', '5432')
}

print("Intentando conectar con:")
print(f"Host: {DB_CONFIG['host']}")
print(f"Database: {DB_CONFIG['database']}")
print(f"User: {DB_CONFIG['user']}")
print(f"Port: {DB_CONFIG['port']}")
print(f"Password: {'*' * len(DB_CONFIG['password'])}")

try:
    conn = psycopg.connect(
        host=DB_CONFIG['host'],
        dbname=DB_CONFIG['database'],
        user=DB_CONFIG['user'],
        password=DB_CONFIG['password'],
        port=DB_CONFIG['port']
    )
    print("\n✓ Conexión exitosa!")
    conn.close()
except Exception as e:
    print(f"\n✗ Error de conexión: {e}")