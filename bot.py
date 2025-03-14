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

@dp.message_handler(commands=["sumarpuntos"], is_chat_admin=True)
async def sumar_puntos_admin(message: types.Message):
    """Permite que los administradores asignen puntos manualmente."""
    args = message.text.split()
    if len(args) != 3:
        await message.reply("Uso correcto: `/sumarpuntos <user_id> <puntos>`", parse_mode="Markdown")
        return
    
    user_id, puntos = args[1], args[2]
    if not user_id.isdigit() or not puntos.isdigit():
        await message.reply("⚠️ Debes ingresar valores numéricos válidos.")
        return

    user_id = int(user_id)
    puntos = int(puntos)

    respuesta = sumar_puntos(user_id, puntos)
    await message.reply(respuesta)

# Iniciar bot
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
