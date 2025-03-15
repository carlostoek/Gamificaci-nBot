from aiogram import types
from aiogram.dispatcher import Dispatcher
from database import registrar_usuario, obtener_usuario, top_10_usuarios  # <--- Nombre correcto

def register_user_handlers(dp: Dispatcher):
    @dp.message_handler(commands=['start'])
    async def cmd_start(message: types.Message):
        user_id = message.from_user.id
        username = message.from_user.username
        registrar_usuario(user_id, username)
        await message.reply("¡Bienvenido! Usa los botones para navegar.")

    @dp.callback_query_handler(lambda c: c.data == "menu_ranking")
    async def mostrar_ranking(callback: types.CallbackQuery):
        top_usuarios = top_10_usuarios()  # <--- Función correctamente importada
        respuesta = "🏆 **Top 10 Usuarios**\n\n"
        for idx, (username, puntos) in enumerate(top_usuarios, 1):
            respuesta += f"{idx}. {username}: {puntos} puntos\n"
        await callback.message.edit_text(respuesta)
