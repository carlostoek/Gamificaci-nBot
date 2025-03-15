from aiogram import types
from aiogram.dispatcher import Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database import actualizar_puntos, obtener_usuario

def register_admin_handlers(dp: Dispatcher, admin_id: int):
    # Menú de administrador
    @dp.message_handler(commands=['admin'])
    async def cmd_admin(message: types.Message):
        if message.from_user.id != admin_id:
            return
        
        teclado = InlineKeyboardMarkup()
        teclado.add(
            InlineKeyboardButton("➕ Sumar puntos", callback_data="admin_sumar_puntos"),
            InlineKeyboardButton("📊 Estadísticas", callback_data="admin_estadisticas")
        )
        await message.reply("🔧 **Panel de Administrador**", reply_markup=teclado)

    # Handler para "Sumar puntos"
    @dp.callback_query_handler(lambda c: c.data == "admin_sumar_puntos")
    async def pedir_datos_sumar_puntos(callback: types.CallbackQuery):
        await callback.message.edit_text(
            "🔢 Ingresa el ID del usuario y los puntos separados por un espacio:\nEjemplo: `123456789 100`",
            parse_mode="Markdown"
        )
        # Guardar estado para capturar la respuesta
        from aiogram.dispatcher import FSMContext
        await callback.message.answer("Esperando datos... (Envía /cancelar para salir)")

    # Capturar datos para sumar puntos
    @dp.message_handler(lambda m: m.from_user.id == admin_id and m.text.replace(' ', '').isdigit())
    async def procesar_sumar_puntos(message: types.Message):
        user_id, puntos = map(int, message.text.split())
        usuario = obtener_usuario(user_id)
        if usuario:
            actualizar_puntos(user_id, puntos)
            await message.reply(f"✅ {puntos} puntos asignados a @{usuario[1]}.")
        else:
            await message.reply("❌ Usuario no encontrado.")
