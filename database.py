import sqlite3

# Conectar a la base de datos SQLite
def get_db():
    conn = sqlite3.connect("puntajes.db")
    return conn

# Crear la tabla de usuarios si no existe
def init_db():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER UNIQUE,
                        username TEXT,
                        puntajes INTEGER DEFAULT 0)''')
    conn.commit()
    conn.close()

# Registrar un nuevo usuario si no existe
def registrar_usuario(user_id, username):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''INSERT OR IGNORE INTO usuarios (user_id, username) VALUES (?, ?)''', (user_id, username))
    conn.commit()
    conn.close()

# Obtener los puntajes de un usuario
def obtener_puntajes(user_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''SELECT puntajes FROM usuarios WHERE user_id = ?''', (user_id,))
    puntajes = cursor.fetchone()
    conn.close()
    return puntajes[0] if puntajes else 0

# Sumar puntos a un usuario
def sumar_puntos(user_id, puntos):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''UPDATE usuarios SET puntajes = puntajes + ? WHERE user_id = ?''', (puntos, user_id))
    conn.commit()
    conn.close()
