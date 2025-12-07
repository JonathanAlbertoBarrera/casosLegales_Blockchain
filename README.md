#  Sistema Judicial Blockchain

Sistema completo de gestión de casos judiciales basado en blockchain, desarrollado con Python (backend) y React (frontend). Implementa transparencia, inmutabilidad y trazabilidad para procesos judiciales.

## Características Principales

- **Blockchain Inmutable**: Cada caso judicial es registrado en una blockchain con SHA-256
- **Gestión Completa de Casos**: Creación, documentos, audiencias y sentencias
- **Autenticación Segura**: Sistema de login con PostgreSQL
- **Verificación de Integridad**: Validación completa de la cadena de bloques
- **Hashing de Documentos**: Almacenamiento de evidencias mediante hashes

##  Requisitos Previos

- Python 3.8 o superior
- Node.js 16 o superior
- PostgreSQL 12 o superior
- npm o yarn

##  Instalación

### 1. Clonar el Repositorio

```powershell
git clone https://github.com/JonathanAlbertoBarrera/casosLegales_Blockchain.git
cd casosLegales_Blockchain
```

### 2. Configurar Backend

```powershell
# Navegar al directorio backend
cd backend

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
.\venv\Scripts\Activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
Copy-Item .env.example .env
# Editar .env con tus credenciales de PostgreSQL
```

### 3. Configurar Base de Datos

```powershell
# Crear base de datos en PostgreSQL
# Opción 1: Usando psql
psql -U postgres
CREATE DATABASE judicial_blockchain;
\q

# Opción 2: Usando pgAdmin (interfaz gráfica)

# Inicializar tablas
psql -U postgres -d judicial_blockchain -f init_db.sql
```

**Configuración de `.env`:**
```env
SECRET_KEY=tu-clave-secreta-aqui
DB_HOST=localhost
DB_NAME=judicial_blockchain
DB_USER=postgres
DB_PASSWORD=tu_password
DB_PORT=5432
```

### 4. Configurar Frontend

```powershell
# Navegar al directorio frontend (desde raíz)
cd frontend

# Instalar dependencias
npm install
```

##  Uso del Sistema

### Ejecutar Demo de Blockchain (Solo Python)

Para ver una demostración completa del sistema blockchain sin interfaz:

```powershell
cd backend
python demo.py
```

Esto mostrará:
- Creación de blockchain judicial
- Registro de 3 casos de ejemplo (civil, penal, laboral)
- Añadir documentos y programar audiencias
- Emitir sentencias
- Verificar integridad de la cadena
- Estadísticas del sistema

### Ejecutar Aplicación Completa

#### 1. Iniciar Backend (Terminal 1)

```powershell
cd backend
.\venv\Scripts\Activate
python app.py
```

El servidor estará disponible en: `http://localhost:5000`

#### 2. Iniciar Frontend (Terminal 2)

```powershell
cd frontend
npm run dev
```

La aplicación estará disponible en: `http://localhost:3000`

### 3. Acceder al Sistema

Abrir navegador en `http://localhost:3000`

**Credenciales de prueba:**
- **Usuario**: `admin`
- **Contraseña**: `admin123`


##  Seguridad

- **Hashing SHA-256**: Todos los bloques usan SHA-256 para integridad
- **Proof of Work**: Protección contra manipulación de la cadena
- **Seudónimos**: Partes involucradas identificadas por hashes
- **Documentos**: Solo se almacenan hashes, no contenido real
- **Autenticación**: Contraseñas hasheadas con Werkzeug
- **Sesiones**: Manejo seguro de sesiones con Flask

## Estadísticas del Sistema

El sistema proporciona:
- Total de bloques en la cadena
- Total de transacciones
- Casos únicos registrados
- Casos por tipo (civil, penal, laboral)
- Casos por estado (presentado, en_proceso, resuelto)
- Verificación de integridad

##  Desarrollo

### Agregar Nuevos Roles

Editar `init_db.sql` y agregar el rol en la constraint:

```sql
CHECK (role IN ('admin', 'judge', 'clerk', 'lawyer', 'viewer', 'nuevo_rol'))
```

### Agregar Nuevos Tipos de Casos

Modificar validación en `court_system.py`:

```python
valid_types = ["civil", "penal", "laboral", "nuevo_tipo"]
```

##  Troubleshooting

### Error de conexión a PostgreSQL
```
Verificar que PostgreSQL esté ejecutándose
Verificar credenciales en .env
Verificar que la base de datos existe
```

### Error al iniciar frontend
```powershell
# Limpiar cache y reinstalar
Remove-Item -Recurse -Force node_modules
Remove-Item package-lock.json
npm install
```

### Error "Module not found" en Python
```powershell
# Verificar que el entorno virtual está activado
.\venv\Scripts\Activate
pip install -r requirements.txt
```


##  Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crear una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -m 'Añadir nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abrir un Pull Request

##  Licencia

Este proyecto está bajo la Licencia MIT. Ver archivo `LICENSE` para más detalles.

##  Autor

**Jonathan Alberto Barrera**
- GitHub: [@JonathanAlbertoBarrera](https://github.com/JonathanAlbertoBarrera)

## Contexto Académico

Proyecto desarrollado para la materia de Seguridad Informática (7mo semestre).
Fecha: Diciembre 2025


**Sistema Judicial Blockchain - Transparencia, Seguridad e Inmutabilidad** 