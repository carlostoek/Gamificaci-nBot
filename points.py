import sqlite3
import logging
from database import DB_NAME

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Puntos por interacciones y compras
PUNTOS_REACCION = 5
PUNTOS_RENOVACION_ANTICIPADA = 50
PUNTOS_RENOVACION_AUTO = 160
BONUS_FIDELIDAD = 100

def sumar_puntos(user_id, puntos):
    """Suma puntos a un usuario y actualiza su nivel si es necesario."""
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        # Obtener puntos actuales
        cursor.execute("SELECT puntos FROM usuarios WHERE user_id = ?", (user_id,))
        user = cursor.fetchone()

        if user:
            puntos_actuales = user[0] + puntos
            cursor.execute("UPDATE usuarios SET puntos = ? WHERE user_id = ?", (puntos_actuales, user_id))
            conn.commit()
            mensaje = f"🎉 Has ganado {puntos} puntos. Total: {puntos_actuales} puntos."
        else:
            mensaje = "⚠️ No estás registrado en el sistema."

        conn.close()
        return mensaje
    except Exception as e:
        logger.error(f"❌ Error al sumar puntos: {e}")
        return "❌ Ocurrió un error al sumar puntos."

def obtener_puntos(user_id):
    """Consulta los puntos actuales de un usuario."""
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        cursor.execute("SELECT puntos FROM usuarios WHERE user_id = ?", (user_id,))
        user = cursor.fetchone()
        
        conn.close()
        return user[0] if user else 0
    except Exception as e:
        logger.error(f"❌ Error al obtener puntos: {e}")
        return 0

def obtener_ranking():
    """Obtiene el top 10 de usuarios con más puntos."""
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        cursor.execute("SELECT username, puntos FROM usuarios ORDER BY puntos DESC LIMIT 10")
        ranking = cursor.fetchall()
        
        conn.close()
        return ranking
    except Exception as e:
        logger.error(f"❌ Error al obtener ranking: {e}")
        return []
