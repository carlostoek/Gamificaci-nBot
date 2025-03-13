from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
import os
from database import init_db, obtener_puntos, obtener_top_usuarios, sumar_puntos

TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Inicializar base de datos
init_db()

@dp.message_handler(commands=['mipuntaje'])
async def mi_puntaje(message: types.Message):
    puntos, nivel = obtener_puntos(message.from_user.id)
    await message.reply(f"📊 *Tu puntaje actual:*\n\n🔹 Puntos: {puntos}\n🔹 Nivel: {nivel}", parse_mode="Markdown")

@dp.message_handler(commands=['top'])
async def top_usuarios(message: types.Message):
    top = obtener_top_usuarios()
    
    if not top:
        await message.reply("Aún no hay jugadores en el ranking.")
        return

    ranking = "\n".join([f"{i+1}. {user[0]} - {user[1]} puntos" for i, user in enumerate(top)])
    await message.reply(f"🏆 *Top 10 Jugadores:*\n\n{ranking}", parse_mode="Markdown")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
