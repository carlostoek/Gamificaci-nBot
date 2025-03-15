import sqlite3
from datetime import datetime

# -------------------- Funciones de la Base de Datos --------------------

def init_db():
    """Inicializa la base de datos y crea las tablas necesarias."""
    conn = sqlite3.connect('vip_gamification.db')
    c = conn.cursor()
    
    # Tabla de usuarios
    c.execute('''CREATE TABLE IF NOT EXISTS usuarios (
        user_id INTEGER PRIMARY KEY,
        username TEXT,
        fecha_ingreso DATE,
        puntos INTEGER DEFAULT 0,
        nivel INTEGER DEFAULT 1,
        renovacion_automatica BOOLEAN DEFAULT FALSE,
        meses_consecutivos INTEGER DEFAULT 0
    )''')
    
    # Tabla de logros
    c.execute('''CREATE TABLE IF NOT EXISTS logros (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        nombre_logro TEXT,
        fecha_obtencion DATE,
        FOREIGN KEY(user_id) REFERENCES usuarios(user_id)
    )''')
    
    # Tabla de interacciones
    c.execute('''CREATE TABLE IF NOT EXISTS interacciones (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        tipo_interaccion TEXT,
        fecha DATETIME,
        puntos_obtenidos INTEGER,
        FOREIGN KEY(user_id) REFERENCES usuarios(user_id)
    )''')
    
    conn.commit()
    conn.close()

def registrar_usuario(user_id: int, username: str):
    """Registra un nuevo usuario en la base de datos."""
    conn = sqlite3.connect('vip_gamification.db')
    c = conn.cursor()
    try:
        c.execute('INSERT OR IGNORE INTO usuarios (user_id, username, fecha_ingreso) VALUES (?, ?, ?)',
                  (user_id, username, datetime.now().strftime("%Y-%m-%d")))
        conn.commit()
    finally:
        conn.close()

def obtener_usuario(user_id: int):
    """Obtiene los datos de un usuario."""
    conn = sqlite3.connect('vip_gamification.db')
    c = conn.cursor()
    c.execute('SELECT * FROM usuarios WHERE user_id = ?', (user_id,))
    usuario = c.fetchone()
    conn.close()
    return usuario

def actualizar_puntos(user_id: int, puntos: int):
    """Actualiza los puntos de un usuario."""
    conn = sqlite3.connect('vip_gamification.db')
    c = conn.cursor()
    c.execute('UPDATE usuarios SET puntos = puntos + ? WHERE user_id = ?', (puntos, user_id))
    conn.commit()
    conn.close()

def top_usuarios():
    """Devuelve el top 10 de usuarios con más puntos."""
    conn = sqlite3.connect('vip_gamification.db')
    c = conn.cursor()
    c.execute('SELECT username, puntos FROM usuarios ORDER BY puntos DESC LIMIT 10')
    resultados = c.fetchall()
    conn.close()
    return resultados
