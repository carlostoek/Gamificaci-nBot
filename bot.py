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

# ... (otros handlers)

# -------------------- Iniciar el bot --------------------

if __name__ == "__main__":
    # Inicializar la base de datos antes de iniciar el bot
    import asyncio
    asyncio.get_event_loop().run_until_complete(init_db())

    # Iniciar el bot
    executor.start_polling(dp, skip_updates=True)
