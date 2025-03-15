import sqlite3
from datetime import datetime

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
    
    # Tabla de compras
    c.execute('''CREATE TABLE IF NOT EXISTS compras (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        monto REAL,
        puntos_obtenidos INTEGER,
        fecha_compra DATE,
        FOREIGN KEY(user_id) REFERENCES usuarios(user_id)
    )''')
    
    conn.commit()
    conn.close()
