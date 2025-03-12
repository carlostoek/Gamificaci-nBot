import sqlite3

# Conectar a la base de datos (o crearla si no existe)
conn = sqlite3.connect("bot.db")
cursor = conn.cursor()

# Crear la tabla de usuarios si no existe
cursor.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY,
        username TEXT,
        puntos INTEGER DEFAULT 0,
        nivel INTEGER DEFAULT 1,
        fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')

# Guardar cambios y cerrar conexión
conn.commit()
conn.close()

def agregar_usuario(user_id, username):
    """ Agrega un usuario si no existe en la base de datos. """
    conn = sqlite3.connect("bot.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM usuarios WHERE id = ?", (user_id,))
    if not cursor.fetchone():
        cursor.execute("INSERT INTO usuarios (id, username) VALUES (?, ?)", (user_id, username))
        conn.commit()
    conn.close()

def actualizar_puntos(user_id, puntos):
    """ Suma puntos a un usuario. """
    conn = sqlite3.connect("bot.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE usuarios SET puntos = puntos + ? WHERE id = ?", (puntos, user_id))
    conn.commit()
    conn.close()

def obtener_puntos(user_id):
    """ Obtiene los puntos de un usuario. """
    conn = sqlite3.connect("bot.db")
    cursor = conn.cursor()
    cursor.execute("SELECT puntos FROM usuarios WHERE id = ?", (user_id,))
    puntos = cursor.fetchone()
    conn.close()
    return puntos[0] if puntos else 0
