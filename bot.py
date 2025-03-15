import os
import logging
from aiogram import Bot, Dispatcher
from aiogram.utils import executor
from dotenv import load_dotenv
from database import init_db
from handlers import user_handlers, admin_handlers, callback_handlers

# Cargar variables de entorno
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Inicializar bot y dispatcher
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Registrar manejadores
user_handlers.register_handlers(dp)
admin_handlers.register_handlers(dp)
callback_handlers.register_handlers(dp)

# Inicializar la base de datos
init_db()

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
