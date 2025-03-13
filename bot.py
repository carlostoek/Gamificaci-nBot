import logging
from aiogram import Bot, Dispatcher
from aiogram.types import ParseMode
from aiogram.utils import executor
from handlers import register_handlers
from database import init_db

API_TOKEN = "TU_BOT_TOKEN"

# Configurar el logging para ver errores
logging.basicConfig(level=logging.INFO)

# Inicializar el bot y el dispatcher
bot = Bot(token=API_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher(bot)

# Inicializar la base de datos
init_db()

# Registrar los manejadores
register_handlers(dp)

# Ejecutar el bot
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
