import os
import logging
import asyncpg
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from dotenv import load_dotenv

# -------------------- Configuración inicial --------------------

# Cargar variables de entorno desde un archivo .env
load_dotenv()

# Obtener variables de entorno
TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))
DATABASE_URL = os.getenv("DATABASE_URL")  # URL de conexión a PostgreSQL

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Inicializar bot y dispatcher
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# -------------------- Configuración de la Base de Datos --------------------

async def init_db():
    """Inicializa la base de datos y crea las tablas necesarias."""
    try:
        conn = await asyncpg.connect(DATABASE_URL)
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id SERIAL PRIMARY KEY,
                user_id BIGINT UNIQUE,
                username TEXT,
                puntos INTEGER DEFAULT 0,
                nivel INTEGER DEFAULT 1
            )
        """)
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS logros (
                id SERIAL PRIMARY KEY,
                user_id BIGINT REFERENCES usuarios(user_id),
                logro TEXT
            )
        """)
        await conn.close()
        logger.info("Base de datos inicializada correctamente.")
    except Exception as e:
        logger.error(f"Error al inicializar la base de datos: {e}")

# -------------------- Handlers --------------------

@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    """Mensaje de bienvenida y registro automático del usuario en la base de datos."""
    user_id = message.from_user.id
    username = message.from_user.username

    try:
        conn = await asyncpg.connect(DATABASE_URL)
        user = await conn.fetchrow("SELECT * FROM usuarios WHERE user_id = $1", user_id)

        if user:
            await message.reply(f"¡Hola {username}! Ya estás registrado en el sistema.")
        else:
            await conn.execute("INSERT INTO usuarios (user_id, username) VALUES ($1, $2)", user_id, username)
            await message.reply(f"¡Bienvenido {username}! Ahora estás registrado en el sistema y puedes ganar puntos.")

        await conn.close()
    except Exception as e:
        logger.error(f"Error en /start: {e}")
        await message.reply("❌ Ocurrió un error al procesar tu solicitud.")

@dp.message_handler(commands=["puntaje"])
async def mi_puntaje(message: types.Message):
    """Consulta el puntaje y nivel del usuario."""
    user_id = message.from_user.id

    try:
        conn = await asyncpg.connect(DATABASE_URL)
        user = await conn.fetchrow("SELECT puntos, nivel FROM usuarios WHERE user_id = $1", user_id)

        if user:
            puntos, nivel = user["puntos"], user["nivel"]
            await message.reply(f"🎯 Tu puntaje actual es: {puntos} puntos.\n⭐ Tu nivel actual es: {nivel}.")
        else:
            await message.reply("❌ No estás registrado. Usa /start para registrarte.")

        await conn.close()
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
        conn = await asyncpg.connect(DATABASE_URL)
        user = await conn.fetchrow("SELECT puntos FROM usuarios WHERE user_id = $1", user_id)

        if user:
            nuevos_puntos = user["puntos"] + 10
            await conn.execute("UPDATE usuarios SET puntos = $1 WHERE user_id = $2", nuevos_puntos, user_id)
            await message.reply(f"🎉 ¡Has ganado 10 puntos! Tu nuevo puntaje es: {nuevos_puntos}.")
        else:
            await message.reply("❌ No estás registrado. Usa /start para registrarte.")

        await conn.close()
    except Exception as e:
        logger.error(f"Error en /sumar_puntos: {e}")
        await message.reply("❌ Ocurrió un error al procesar tu solicitud.")

@dp.message_handler(commands=["ranking"])
async def ranking(message: types.Message):
    """Muestra el ranking de los usuarios con más puntos."""
    try:
        conn = await asyncpg.connect(DATABASE_URL)
        top_usuarios = await conn.fetch("SELECT username, puntos FROM usuarios ORDER BY puntos DESC LIMIT 10")

        if top_usuarios:
            ranking_msg = "🏆 Ranking de Usuarios:\n"
            for i, usuario in enumerate(top_usuarios, start=1):
                ranking_msg += f"{i}. {usuario['username']}: {usuario['puntos']} puntos\n"
            await message.reply(ranking_msg)
        else:
            await message.reply("❌ No hay usuarios registrados.")

        await conn.close()
    except Exception as e:
        logger.error(f"Error en /ranking: {e}")
        await message.reply("❌ Ocurrió un error al procesar tu solicitud.")

# -------------------- Iniciar el bot --------------------

if __name__ == "__main__":
    # Inicializar la base de datos antes de iniciar el bot
    import asyncio
    asyncio.get_event_loop().run_until_complete(init_db())

    # Iniciar el bot
    executor.start_polling(dp, skip_updates=True)
