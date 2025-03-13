from aiogram import Bot, Dispatcher
from aiogram.utils import executor
import os
from database import init_db
from handlers import register_handlers

TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Inicializar base de datos
init_db()

# Registrar los handlers
register_handlers(dp)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
