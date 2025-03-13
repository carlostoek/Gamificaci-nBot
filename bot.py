from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
import os
import logging
from database import agregar_usuario, actualizar_puntos, obtener_puntos

TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

logging.basicConfig(level=logging.INFO)

@dp.message_handler(commands=["start"])
async def cmd_start(message: types.Message):
    """ Registra al usuario y muestra un mensaje de bienvenida. """
    user_id = message.from_user.id
    username = message.from_user.username or f"Usuario_{user_id}"
    
    # Registrar usuario en la base de datos
    agregar_usuario(user_id, username)
    
    await message.reply(f"🎮 Hey, hola! ¡Bienvenido, @{username}! Tu progreso será guardado en el sistema.")

@dp.message_handler(commands=["puntos"])
async def cmd_puntos(message: types.Message):
    """ Muestra los puntos del usuario. """
    user_id = message.from_user.id
    puntos = obtener_puntos(user_id)
    await message.reply(f"⭐ Tienes **{puntos} puntos**.")

@dp.message_handler(commands=["sumar"])
async def cmd_sumar_puntos(message: types.Message):
    """ Suma puntos al usuario. """
    user_id = message.from_user.id
    actualizar_puntos(user_id, 10)
    puntos = obtener_puntos(user_id)
    await message.reply(f"🎉 ¡Has ganado **10 puntos**! Ahora tienes **{puntos} puntos**.")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
