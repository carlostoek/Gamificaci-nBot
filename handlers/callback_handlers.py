from aiogram import types
from aiogram.dispatcher import Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database import actualizar_puntos

def register_callback_handlers(dp: Dispatcher):
    # Publicar encuesta con botones inline
    @dp.message_handler(commands=['encuesta'])
    async def crear_encuesta(message: types.Message):
        teclado = InlineKeyboardMarkup(row_width=2)
        teclado.add(
            InlineKeyboardButton("🔥 Excelente (+10)", callback_data="reaccion:10"),
            InlineKeyboardButton("👍 Bueno (+5)", callback_data="reaccion:5"),
            InlineKeyboardButton("😐 Regular (+2)", callback_data="reaccion:2")
        )
        await message.reply(
            "📢 **Encuesta Diaria**\n\n"
            "¿Cómo calificarías el contenido de hoy?",
            reply_markup=teclado
        )

    # Procesar reacciones
    @dp.callback_query_handler(lambda c: c.data.startswith('reaccion:'))
    async def manejar_reaccion(callback: types.CallbackQuery):
        puntos = int(callback.data.split(':')[1])
        actualizar_puntos(callback.from_user.id, puntos)
        await callback.answer(f"🎉 ¡Has ganado {puntos} puntos!", show_alert=True)
