import os
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from dotenv import load_dotenv
from database import init_db, registrar_usuario

# Cargar variables de entorno
load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Inicializar bot y dispatcher
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Inicializar base de datos
init_db()

@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    """Comando de inicio que registra al usuario."""
    user_id = message.from_user.id
    username = message.from_user.username or "Usuario Desconocido"
    
    mensaje = registrar_usuario(user_id, username)
    await message.reply(mensaje)

# Iniciar bot
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
