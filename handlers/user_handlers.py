from aiogram import types
from aiogram.dispatcher import Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database import obtener_usuario, top_10_usuarios

def register_user_handlers(dp: Dispatcher):
    # Menú principal con botones
    @dp.message_handler(commands=['start'])
    async def cmd_start(message: types.Message):
        teclado = InlineKeyboardMarkup(row_width=2)
        teclado.add(
            InlineKeyboardButton("📊 Mis puntos", callback_data="menu_mis_puntos"),
            InlineKeyboardButton("🏆 Ranking", callback_data="menu_ranking"),
            InlineKeyboardButton("ℹ️ Ayuda", callback_data="menu_ayuda")
        )
        await message.reply("🎮 **Menú Principal**\nElige una opción:", reply_markup=teclado)

    # Handler para "Mis puntos"
    @dp.callback_query_handler(lambda c: c.data == "menu_mis_puntos")
    async def mostrar_puntos(callback: types.CallbackQuery):
        usuario = obtener_usuario(callback.from_user.id)
        respuesta = (
            f"🏅 **Tus puntos**\n\n"
            f"🔢 Puntos: {usuario[3]}\n"
            f"⭐ Nivel: {usuario[4]}"
        )
        await callback.message.edit_text(respuesta)

    # Handler para "Ranking"
    @dp.callback_query_handler(lambda c: c.data == "menu_ranking")
    async def mostrar_ranking(callback: types.CallbackQuery):
        top_usuarios = top_10_usuarios()
        respuesta = "🏆 **Top 10 Usuarios**\n\n"
        for idx, (username, puntos) in enumerate(top_usuarios, 1):
            respuesta += f"{idx}. {username}: {puntos} puntos\n"
        await callback.message.edit_text(respuesta)

    # Handler para "Ayuda"
    @dp.callback_query_handler(lambda c: c.data == "menu_ayuda")
    async def mostrar_ayuda(callback: types.CallbackQuery):
        texto = (
            "❓ **Ayuda**\n\n"
            "Usa los botones para navegar:\n"
            "📊 Mis puntos: Muestra tu progreso.\n"
            "🏆 Ranking: Muestra el top 10.\n"
            "ℹ️ Ayuda: Muestra este mensaje."
        )
        await callback.message.edit_text(texto)
