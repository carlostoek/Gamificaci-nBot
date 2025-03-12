import logging
from aiogram import Bot, Dispatcher
from aiogram.utils import executor
from config import TOKEN
import handlers

# Configurar logging para Railway
logging.basicConfig(level=logging.INFO)

# Instanciar bot y dispatcher
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Registrar handlers
handlers.register_handlers(dp)

# Iniciar el bot
if __name__ == "__main__":
    print("✅ Bot de gamificación iniciado en Railway.")
    executor.start_polling(dp, skip_updates=True)
