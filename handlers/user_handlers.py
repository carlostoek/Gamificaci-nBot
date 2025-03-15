from aiogram import types
from aiogram.dispatcher import Dispatcher
from database import registrar_usuario, obtener_usuario, top_usuarios

def register_user_handlers(dp: Dispatcher):
    @dp.message_handler(commands=['start'])
    async def cmd_start(message: types.Message):
        user_id = message.from_user.id
        username = message.from_user.username
        registrar_usuario(user_id, username)
        await message.reply(f"🎉 ¡Bienvenido @{username}! Ahora estás registrado en el sistema VIP.")

    @dp.message_handler(commands=['mispuntos'])
    async def cmd_mispuntos(message: types.Message):
        user = obtener_usuario(message.from_user.id)
        if user:
            await message.reply(f"🏅 **Tu progreso**\n\n🔢 Puntos: {user[3]}\n⭐ Nivel: {user[4]}")
        else:
            await message.reply("❌ Primero debes registrarte con /start")

    @dp.message_handler(commands=['ranking'])
    async def cmd_ranking(message: types.Message):
        ranking = "🏆 **Ranking VIP**\n\n"
        for idx, (username, puntos) in enumerate(top_usuarios(), 1):
            ranking += f"{idx}. {username}: {puntos} puntos\n"
        await message.reply(ranking)
