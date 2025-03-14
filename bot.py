import os
import logging
import sqlite3
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from dotenv import load_dotenv

# -------------------- Configuración inicial --------------------

# Cargar variables de entorno desde un archivo .env
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")  # Token del bot
ADMIN_ID = int(os.getenv("ADMIN_ID"))  # ID del administrador

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Inicializar bot y dispatcher
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# -------------------- Configuración de la Base de Datos --------------------

DB_NAME = "database.db"  # Nombre de la base de datos SQLite

def init_db():
    """Inicializa la base de datos y crea las tablas necesarias."""
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER UNIQUE,
                username TEXT,
                puntos INTEGER DEFAULT 0,
                nivel INTEGER DEFAULT 1
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS logros (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                logro TEXT,
                FOREIGN KEY (user_id) REFERENCES usuarios (user_id)
            )
        """)
        conn.commit()
        conn.close()
        logger.info("Base de datos inicializada correctamente.")
    except Exception as e:
        logger.error(f"Error al inicializar la base de datos: {e}")

init_db()  # Se ejecuta al iniciar el bot

# -------------------- Handlers --------------------

@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    """Mensaje de bienvenida y registro automático del usuario en la base de datos."""
    user_id = message.from_user.id
    username = message.from_user.username

    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM usuarios WHERE user_id = ?", (user_id,))
        user = cursor.fetchone()

        if user:
            await message.reply(f"¡Hola {username}! Ya estás registrado en el sistema.")
        else:
            cursor.execute("INSERT INTO usuarios (user_id, username) VALUES (?, ?)", (user_id, username))
            conn.commit()
            await message.reply(f"¡Bienvenido {username}! Ahora estás registrado en el sistema y puedes ganar puntos.")

        conn.close()
    except Exception as e:
        logger.error(f"Error en /start: {e}")
        await message.reply("❌ Ocurrió un error al procesar tu solicitud.")

@dp.message_handler(commands=["puntaje"])
async def mi_puntaje(message: types.Message):
    """Consulta el puntaje y nivel del usuario."""
    user_id = message.from_user.id

    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT puntos, nivel FROM usuarios WHERE user_id = ?", (user_id,))
        user = cursor.fetchone()

        if user:
            puntos, nivel = user
            await message.reply(f"🎯 Tu puntaje actual es: {puntos} puntos.\n⭐ Tu nivel actual es: {nivel}.")
        else:
            await message.reply("❌ No estás registrado. Usa /start para registrarte.")

        conn.close()
    except Exception as e:
        logger.error(f"Error en /puntaje: {e}")
        await message.reply("❌ Ocurrió un error al procesar tu solicitud.")

@dp.message_handler(commands=["sumar_puntos"])
async def sumar_puntos(message: types.Message):
    """Suma puntos al usuario (solo para administradores)."""
    user_id = message.from_user.id

    if user_id != ADMIN_ID:
        await message.reply("❌ No tienes permisos para usar este comando.")
        return

    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT puntos FROM usuarios WHERE user_id = ?", (user_id,))
        user = cursor.fetchone()

        if user:
            nuevos_puntos = user[0] + 10
            cursor.execute("UPDATE usuarios SET puntos = ? WHERE user_id = ?", (nuevos_puntos, user_id))
            conn.commit()
            await message.reply(f"🎉 ¡Has ganado 10 puntos! Tu nuevo puntaje es: {nuevos_puntos}.")
        else:
            await message.reply("❌ No estás registrado. Usa /start para registrarte.")

        conn.close()
    except Exception as e:
        logger.error(f"Error en /sumar_puntos: {e}")
        await message.reply("❌ Ocurrió un error al procesar tu solicitud.")

@dp.message_handler(commands=["ranking"])
async def ranking(message: types.Message):
    """Muestra el ranking de los usuarios con más puntos."""
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT username, puntos FROM usuarios ORDER BY puntos DESC LIMIT 10")
        top_usuarios = cursor.fetchall()

        if top_usuarios:
            ranking_msg = "🏆 Ranking de Usuarios:\n"
            for i, (username, puntos) in enumerate(top_usuarios, start=1):
                ranking_msg += f"{i}. {username}: {puntos} puntos\n"
            await message.reply(ranking_msg)
        else:
            await message.reply("❌ No hay usuarios registrados.")

        conn.close()
    except Exception as e:
        logger.error(f"Error en /ranking: {e}")
        await message.reply("❌ Ocurrió un error al procesar tu solicitud.")

# -------------------- Iniciar el bot --------------------

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
