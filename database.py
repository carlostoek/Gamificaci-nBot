import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect('vip_gamification.db')
    c = conn.cursor()
    
    c.execute('''CREATE TABLE IF NOT EXISTS usuarios (
        user_id INTEGER PRIMARY KEY,
        username TEXT,
        fecha_ingreso DATE,
        puntos INTEGER DEFAULT 0,
        nivel INTEGER DEFAULT 1
    )''')
    
    conn.commit()
    conn.close()

def actualizar_nivel(user_id: int):
    """Actualiza el nivel del usuario según sus puntos."""
    conn = sqlite3.connect('vip_gamification.db')
    c = conn.cursor()
    c.execute('SELECT puntos FROM usuarios WHERE user_id = ?', (user_id,))
    puntos = c.fetchone()[0]
    
    # Definir niveles (ejemplo: 100 puntos por nivel)
    nuevo_nivel = puntos // 100
    c.execute('UPDATE usuarios SET nivel = ? WHERE user_id = ?', (nuevo_nivel, user_id))
    
    conn.commit()
    conn.close()

def registrar_usuario(user_id: int, username: str):
    conn = sqlite3.connect('vip_gamification.db')
    c = conn.cursor()
    c.execute('INSERT OR IGNORE INTO usuarios (user_id, username, fecha_ingreso) VALUES (?, ?, ?)',
              (user_id, username, datetime.now().strftime("%Y-%m-%d")))
    conn.commit()
    conn.close()

def obtener_usuario(user_id: int):
    conn = sqlite3.connect('vip_gamification.db')
    c = conn.cursor()
    c.execute('SELECT * FROM usuarios WHERE user_id = ?', (user_id,))
    usuario = c.fetchone()
    conn.close()
    return usuario

def actualizar_puntos(user_id: int, puntos: int):
    conn = sqlite3.connect('vip_gamification.db')
    c = conn.cursor()
    c.execute('UPDATE usuarios SET puntos = puntos + ? WHERE user_id = ?', (puntos, user_id))
    conn.commit()
    conn.close()

def top_10_usuarios():
    """Devuelve el top 10 de usuarios con más puntos."""
    conn = sqlite3.connect('vip_gamification.db')
    c = conn.cursor()
    c.execute('SELECT username, puntos FROM usuarios ORDER BY puntos DESC LIMIT 10')
    resultados = c.fetchall()
    conn.close()
    return resultados  # <--- Función añadida
