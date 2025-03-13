import sqlite3

DB_NAME = "gamificacion.db"

def init_db():
    """Crea la base de datos si no existe."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            puntos INTEGER DEFAULT 0,
            nivel INTEGER DEFAULT 1
        )
    ''')
    
    conn.commit()
    conn.close()

def agregar_usuario(user_id, username):
    """Añade un usuario a la base de datos si no existe."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM usuarios WHERE user_id = ?', (user_id,))
    if cursor.fetchone() is None:
        cursor.execute('INSERT INTO usuarios (user_id, username) VALUES (?, ?)', (user_id, username))
        conn.commit()

    conn.close()

def sumar_puntos(user_id, username, puntos=1):
    """Suma puntos a un usuario y verifica si sube de nivel."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    agregar_usuario(user_id, username)

    cursor.execute('UPDATE usuarios SET puntos = puntos + ? WHERE user_id = ?', (puntos, user_id))
    conn.commit()
    conn.close()

def obtener_puntos(user_id):
    """Obtiene los puntos de un usuario."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute('SELECT puntos, nivel FROM usuarios WHERE user_id = ?', (user_id,))
    resultado = cursor.fetchone()
    
    conn.close()
    return resultado if resultado else (0, 1)

def obtener_top_usuarios():
    """Obtiene el top 10 de usuarios con más puntos."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute('SELECT username, puntos FROM usuarios ORDER BY puntos DESC LIMIT 10')
    top = cursor.fetchall()
    
    conn.close()
    return top
