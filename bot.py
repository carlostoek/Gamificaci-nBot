import os
import logging
from aiogram import Bot, Dispatcher
from aiogram.utils import executor
from dotenv import load_dotenv
from database import init_db
from handlers.user_handlers import register_user_handlers
from handlers.admin_handlers import register_admin_handlers
from handlers.callback_handlers import register_callback_handlers

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

# Registrar handlers
register_user_handlers(dp)
register_admin_handlers(dp, ADMIN_ID)
register_callback_handlers(dp)

# Inicializar base de datos
init_db()

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
