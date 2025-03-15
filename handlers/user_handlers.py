from aiogram import types
from aiogram.dispatcher import Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database import registrar_usuario, obtener_usuario, top_10_usuarios

def register_user_handlers(dp: Dispatcher):
    # Comando /start con botones inline
    @dp.message_handler(commands=['start'])
    async def cmd_start(message: types.Message):
        user_id = message.from_user.id
        username = message.from_user.username
        registrar_usuario(user_id, username)
        
        # Crear teclado inline
        teclado = InlineKeyboardMarkup(row_width=2)
        teclado.add(
            InlineKeyboardButton("👤 Mi Perfil", callback_data="menu_perfil"),
            InlineKeyboardButton("🏆 Ranking", callback_data="menu_ranking"),
            InlineKeyboardButton("🎮 Misiones", callback_data="menu_misiones"),
            InlineKeyboardButton("❓ Ayuda", callback_data="menu_ayuda")
        )
        
        await message.reply("🌟 **Bienvenido al Sistema VIP**\nElige una opción:", reply_markup=teclado)
@dp.callback_query_handler(lambda c: c.data == "menu_perfil")
async def mostrar_perfil(callback: types.CallbackQuery):
    usuario = obtener_usuario(callback.from_user.id)
    if usuario:
        respuesta = (
            f"👤 **Perfil de @{usuario[1]}**\n\n"
            f"⭐ Nivel: {usuario[4]}\n"
            f"🔢 Puntos: {usuario[3]}\n"
            f"📅 Miembro desde: {usuario[2]}"
        )
    else:
        respuesta = "❌ No estás registrado. Usa /start para registrarte."
    
    teclado = InlineKeyboardMarkup().add(InlineKeyboardButton("🔙 Volver", callback_data="menu_principal"))
    await callback.message.edit_text(respuesta, reply_markup=teclado)
    # Handler para "Mi Perfil"
    @dp.callback_query_handler(lambda c: c.data == "menu_perfil")
    async def mostrar_perfil(callback: types.CallbackQuery):
        usuario = obtener_usuario(callback.from_user.id)
        if usuario:
            respuesta = (
                f"👤 **Perfil de @{usuario[1]}**\n\n"
                f"⭐ Nivel: {usuario[4]}\n"
                f"🔢 Puntos: {usuario[3]}\n"
                f"📅 Miembro desde: {usuario[2]}"
            )
        else:
            respuesta = "❌ No estás registrado. Usa /start para registrarte."
        
        # Botón para volver al menú
        teclado = InlineKeyboardMarkup().add(InlineKeyboardButton("🔙 Volver", callback_data="menu_principal"))
        await callback.message.edit_text(respuesta, reply_markup=teclado)

    # Handler para "Ranking"
    @dp.callback_query_handler(lambda c: c.data == "menu_ranking")
    async def mostrar_ranking(callback: types.CallbackQuery):
        top_usuarios = top_10_usuarios()
        respuesta = "🏆 **Top 10 Usuarios**\n\n"
        for idx, (username, puntos) in enumerate(top_usuarios, 1):
            respuesta += f"{idx}. {username}: {puntos} puntos\n"
        
        # Botón para volver al menú
        teclado = InlineKeyboardMarkup().add(InlineKeyboardButton("🔙 Volver", callback_data="menu_principal"))
        await callback.message.edit_text(respuesta, reply_markup=teclado)

    # Handler para "Volver al Menú"
    @dp.callback_query_handler(lambda c: c.data == "menu_principal")
    async def volver_al_menu(callback: types.CallbackQuery):
        # Recrear el menú principal
        teclado = InlineKeyboardMarkup(row_width=2)
        teclado.add(
            InlineKeyboardButton("👤 Mi Perfil", callback_data="menu_perfil"),
            InlineKeyboardButton("🏆 Ranking", callback_data="menu_ranking"),
            InlineKeyboardButton("🎮 Misiones", callback_data="menu_misiones"),
            InlineKeyboardButton("❓ Ayuda", callback_data="menu_ayuda")
        )
        await callback.message.edit_text("🌟 **Menú Principal**\nElige una opción:", reply_markup=teclado)
