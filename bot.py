import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.utils import executor
from config import TOKEN, CHANNEL_ID
import handlers

# Configurar logging
logging.basicConfig(level=logging.INFO)

# Instanciar bot y dispatcher
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Cargar manejadores
handlers.register_handlers(dp)

# Iniciar el bot
if __name__ == "__main__":
    print("✅ Bot de gamificación iniciado correctamente.")
    executor.start_polling(dp, skip_updates=True)
