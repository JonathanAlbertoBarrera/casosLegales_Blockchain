"""
API REST para el Sistema Judicial Blockchain
Proporciona endpoints para gestionar casos, usuarios y autenticación
"""

from flask import Flask, request, jsonify, session
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from datetime import datetime, timedelta
import secrets
from court_system import CourtSystem
from functools import wraps
from typing import Optional, Dict, Any

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', secrets.token_hex(32))
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['SESSION_COOKIE_SECURE'] = False  # True en producción con HTTPS

# Configurar CORS
CORS(app, supports_credentials=True, origins=["http://localhost:3000", "http://localhost:5173"])

# Sistema judicial global
court_system = CourtSystem(difficulty=3)

# Configuración de base de datos
DB_CONFIG = {
    'host': os.environ.get('DB_HOST', 'localhost'),
    'database': os.environ.get('DB_NAME', 'judicial_blockchain'),
    'user': os.environ.get('DB_USER', 'postgres'),
    'password': os.environ.get('DB_PASSWORD', 'postgres'),
    'port': os.environ.get('DB_PORT', '5432')
}


def get_db_connection():
    """Crea una conexión a la base de datos PostgreSQL"""
    try:
        conn = psycopg2.connect(**DB_CONFIG, cursor_factory=RealDictCursor)
        return conn
    except psycopg2.Error as e:
        print(f"Error conectando a la base de datos: {e}")
        return None


def init_database():
    """Inicializa las tablas de la base de datos"""
    conn = get_db_connection()
    if not conn:
        print("  No se pudo conectar a PostgreSQL. Usando modo sin base de datos.")
        return False
    
    try:
        cur = conn.cursor()
        
        # Tabla de usuarios
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username VARCHAR(100) UNIQUE NOT NULL,
                email VARCHAR(255) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                role VARCHAR(50) NOT NULL,
                full_name VARCHAR(255),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Tabla de sesiones (opcional, Flask maneja sesiones por defecto)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                id SERIAL PRIMARY KEY,
                user_id INTEGER REFERENCES users(id),
                session_token VARCHAR(255) UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                expires_at TIMESTAMP NOT NULL
            )
        """)
        
        conn.commit()
        cur.close()
        conn.close()
        print(" Base de datos inicializada correctamente")
        return True
    except psycopg2.Error as e:
        print(f" Error inicializando base de datos: {e}")
        return False


def login_required(f):
    """Decorador para proteger rutas que requieren autenticación"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({"error": "No autorizado", "message": "Debe iniciar sesión"}), 401
        return f(*args, **kwargs)
    return decorated_function


# ============================================================================
# RUTAS DE AUTENTICACIÓN
# ============================================================================

@app.route('/api/auth/register', methods=['POST'])
def register():
    """Registra un nuevo usuario"""
    data = request.get_json()
    
    required_fields = ['username', 'email', 'password', 'role', 'full_name']
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Campos requeridos faltantes"}), 400
    
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Error de base de datos"}), 500
    
    try:
        cur = conn.cursor()
        
        # Verificar si el usuario ya existe
        cur.execute("SELECT id FROM users WHERE username = %s OR email = %s",
                   (data['username'], data['email']))
        if cur.fetchone():
            return jsonify({"error": "Usuario o email ya existe"}), 409
        
        # Crear nuevo usuario
        password_hash = generate_password_hash(data['password'])
        cur.execute("""
            INSERT INTO users (username, email, password_hash, role, full_name)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id, username, email, role, full_name
        """, (data['username'], data['email'], password_hash, data['role'], data['full_name']))
        
        user = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        
        return jsonify({
            "message": "Usuario registrado exitosamente",
            "user": dict(user)
        }), 201
        
    except psycopg2.Error as e:
        return jsonify({"error": f"Error en base de datos: {str(e)}"}), 500


@app.route('/api/auth/login', methods=['POST'])
def login():
    """Inicia sesión de usuario"""
    data = request.get_json()
    
    if not data.get('username') or not data.get('password'):
        return jsonify({"error": "Usuario y contraseña requeridos"}), 400
    
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Error de base de datos"}), 500
    
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE username = %s", (data['username'],))
        user = cur.fetchone()
        cur.close()
        conn.close()
        
        if not user or not check_password_hash(user['password_hash'], data['password']):
            return jsonify({"error": "Credenciales inválidas"}), 401
        
        # Crear sesión
        session['user_id'] = user['id']
        session['username'] = user['username']
        session['role'] = user['role']
        
        return jsonify({
            "message": "Inicio de sesión exitoso",
            "user": {
                "id": user['id'],
                "username": user['username'],
                "email": user['email'],
                "role": user['role'],
                "full_name": user['full_name']
            }
        }), 200
        
    except psycopg2.Error as e:
        return jsonify({"error": f"Error en base de datos: {str(e)}"}), 500


@app.route('/api/auth/logout', methods=['POST'])
@login_required
def logout():
    """Cierra sesión de usuario"""
    session.clear()
    return jsonify({"message": "Sesión cerrada exitosamente"}), 200


@app.route('/api/auth/me', methods=['GET'])
@login_required
def get_current_user():
    """Obtiene información del usuario actual"""
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Error de base de datos"}), 500
    
    try:
        cur = conn.cursor()
        cur.execute("SELECT id, username, email, role, full_name, created_at FROM users WHERE id = %s",
                   (session['user_id'],))
        user = cur.fetchone()
        cur.close()
        conn.close()
        
        if not user:
            return jsonify({"error": "Usuario no encontrado"}), 404
        
        return jsonify({"user": dict(user)}), 200
        
    except psycopg2.Error as e:
        return jsonify({"error": f"Error en base de datos: {str(e)}"}), 500


# ============================================================================
# RUTAS DE GESTIÓN JUDICIAL
# ============================================================================

@app.route('/api/cases', methods=['GET'])
@login_required
def get_all_cases():
    """Obtiene todos los casos judiciales"""
    cases = court_system.get_all_cases()
    return jsonify({"cases": cases}), 200


@app.route('/api/cases/<case_id>', methods=['GET'])
@login_required
def get_case(case_id):
    """Obtiene detalles de un caso específico"""
    case_details = court_system.get_case_details(case_id)
    
    if not case_details:
        return jsonify({"error": "Caso no encontrado"}), 404
    
    # Incluir historial
    history = court_system.get_case_history(case_id)
    
    return jsonify({
        "case": case_details,
        "history": history
    }), 200


@app.route('/api/cases', methods=['POST'])
@login_required
def create_case():
    """Crea un nuevo caso judicial"""
    data = request.get_json()
    
    required_fields = ['case_id', 'case_type', 'plaintiff_name', 'defendant_name', 
                      'judge_id', 'description']
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Campos requeridos faltantes"}), 400
    
    success = court_system.create_case(
        case_id=data['case_id'],
        case_type=data['case_type'],
        plaintiff_name=data['plaintiff_name'],
        defendant_name=data['defendant_name'],
        judge_id=data['judge_id'],
        description=data['description'],
        miner_address=session['username']
    )
    
    if success:
        return jsonify({"message": "Caso creado exitosamente"}), 201
    else:
        return jsonify({"error": "Error creando caso"}), 400


@app.route('/api/cases/<case_id>/documents', methods=['POST'])
@login_required
def add_document(case_id):
    """Añade un documento a un caso"""
    data = request.get_json()
    
    if not data.get('document_name') or not data.get('document_content'):
        return jsonify({"error": "Nombre y contenido del documento requeridos"}), 400
    
    success = court_system.add_document(
        case_id=case_id,
        document_name=data['document_name'],
        document_content=data['document_content'],
        uploader=session['username'],
        miner_address=session['username']
    )
    
    if success:
        return jsonify({"message": "Documento añadido exitosamente"}), 201
    else:
        return jsonify({"error": "Error añadiendo documento"}), 400


@app.route('/api/cases/<case_id>/hearings', methods=['POST'])
@login_required
def schedule_hearing(case_id):
    """Programa una audiencia"""
    data = request.get_json()
    
    required_fields = ['hearing_type', 'date', 'location']
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Campos requeridos faltantes"}), 400
    
    success = court_system.schedule_hearing(
        case_id=case_id,
        hearing_type=data['hearing_type'],
        date=data['date'],
        location=data['location'],
        miner_address=session['username']
    )
    
    if success:
        return jsonify({"message": "Audiencia programada exitosamente"}), 201
    else:
        return jsonify({"error": "Error programando audiencia"}), 400


@app.route('/api/cases/<case_id>/judgment', methods=['POST'])
@login_required
def issue_judgment(case_id):
    """Emite una sentencia"""
    data = request.get_json()
    
    required_fields = ['ruling', 'verdict', 'details']
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Campos requeridos faltantes"}), 400
    
    success = court_system.issue_judgment(
        case_id=case_id,
        ruling=data['ruling'],
        verdict=data['verdict'],
        details=data['details'],
        miner_address=session['username']
    )
    
    if success:
        return jsonify({"message": "Sentencia emitida exitosamente"}), 201
    else:
        return jsonify({"error": "Error emitiendo sentencia"}), 400


@app.route('/api/judges', methods=['POST'])
@login_required
def register_judge():
    """Registra un nuevo juez"""
    data = request.get_json()
    
    if not data.get('name') or not data.get('specialty'):
        return jsonify({"error": "Nombre y especialidad requeridos"}), 400
    
    judge_id = court_system.register_judge(data['name'], data['specialty'])
    
    return jsonify({
        "message": "Juez registrado exitosamente",
        "judge_id": judge_id
    }), 201


@app.route('/api/judges', methods=['GET'])
@login_required
def get_judges():
    """Obtiene lista de jueces registrados"""
    return jsonify({"judges": court_system.judges}), 200


@app.route('/api/blockchain/verify', methods=['GET'])
@login_required
def verify_blockchain():
    """Verifica la integridad de la blockchain"""
    is_valid = court_system.verify_blockchain_integrity()
    return jsonify({"valid": is_valid}), 200


@app.route('/api/blockchain/statistics', methods=['GET'])
@login_required
def get_statistics():
    """Obtiene estadísticas del sistema"""
    stats = court_system.get_statistics()
    return jsonify({"statistics": stats}), 200


@app.route('/api/blockchain/export', methods=['GET'])
@login_required
def export_blockchain():
    """Exporta la blockchain completa"""
    blockchain_data = court_system.export_blockchain()
    return jsonify({"blockchain": blockchain_data}), 200


@app.route('/api/documents/verify', methods=['POST'])
@login_required
def verify_document():
    """Verifica la autenticidad de un documento"""
    data = request.get_json()
    
    if not data.get('case_id') or not data.get('document_content'):
        return jsonify({"error": "case_id y document_content requeridos"}), 400
    
    result = court_system.verify_document(data['case_id'], data['document_content'])
    
    if result:
        return jsonify(result), 200
    else:
        return jsonify({"error": "Caso no encontrado"}), 404


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "Judicial Blockchain API",
        "timestamp": datetime.now().isoformat()
    }), 200


# ============================================================================
# INICIALIZACIÓN
# ============================================================================

if __name__ == '__main__':
    print("  Iniciando Sistema Judicial Blockchain API...")
    
    # Inicializar base de datos
    db_initialized = init_database()
    
    if not db_initialized:
        print("  Ejecutando sin base de datos. Algunas funcionalidades estarán limitadas.")
    
    # Inicializar algunos jueces por defecto
    court_system.register_judge("María Rodríguez", "civil")
    court_system.register_judge("Carlos Mendoza", "penal")
    court_system.register_judge("Ana López", "laboral")
    
    print("\n Sistema inicializado correctamente")
    print(" API ejecutándose en http://localhost:5000")
    print(" Documentación disponible en /api/health\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
