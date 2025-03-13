from aiogram import types
from aiogram.dispatcher import Dispatcher
from database import obtener_puntos, obtener_top_usuarios

def register_handlers(dp: Dispatcher):
    """Registra los comandos en el dispatcher."""

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
