import sqlite3
import logging
from datetime import datetime

# Nombre del archivo de la base de datos
DB_NAME = "database.db"

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_db():
    """Crea las tablas necesarias en la base de datos."""
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        # Tabla de usuarios
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER UNIQUE,
                username TEXT,
                puntos INTEGER DEFAULT 0,
                nivel INTEGER DEFAULT 1,
                fecha_ingreso TEXT
            )
        """)

        # Tabla de logros
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS logros (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                logro TEXT,
                FOREIGN KEY (user_id) REFERENCES usuarios(user_id)
            )
        """)

        # Tabla de compras
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS compras (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                monto INTEGER,
                puntos_asignados INTEGER,
                fecha TEXT,
                FOREIGN KEY (user_id) REFERENCES usuarios(user_id)
            )
        """)

        conn.commit()
        conn.close()
        logger.info("✅ Base de datos inicializada correctamente.")
    except Exception as e:
        logger.error(f"❌ Error al inicializar la base de datos: {e}")

def registrar_usuario(user_id, username):
    """Registra un nuevo usuario si no existe en la base de datos."""
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM usuarios WHERE user_id = ?", (user_id,))
        user = cursor.fetchone()
        
        if not user:
            fecha_actual = datetime.now().strftime("%Y-%m-%d")
            cursor.execute("INSERT INTO usuarios (user_id, username, fecha_ingreso) VALUES (?, ?, ?)", 
                           (user_id, username, fecha_actual))
            conn.commit()
            mensaje = f"✅ Usuario {username} registrado correctamente."
        else:
            mensaje = f"⚠️ Usuario {username} ya está registrado."

        conn.close()
        return mensaje
    except Exception as e:
        logger.error(f"❌ Error al registrar usuario: {e}")
        return "❌ Ocurrió un error al registrarte."
