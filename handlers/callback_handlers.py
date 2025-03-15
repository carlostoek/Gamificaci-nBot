from aiogram import types
from aiogram.dispatcher import Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database import actualizar_puntos

def register_callback_handlers(dp: Dispatcher):
    # Publicar encuesta con botones
    @dp.message_handler(commands=['publicar_encuesta'])
    async def publicar_encuesta(message: types.Message):
        teclado = InlineKeyboardMarkup()
        teclado.add(
            InlineKeyboardButton("🔥 Me encantó (+5)", callback_data="reaccion:5"),
            InlineKeyboardButton("👍 Bueno (+3)", callback_data="reaccion:3")
        )
        await message.reply("¿Qué te pareció este contenido?", reply_markup=teclado)

    # Manejar reacciones
    @dp.callback_query_handler(lambda c: c.data.startswith('reaccion:'))
    async def procesar_reaccion(callback: types.CallbackQuery):
        puntos = int(callback.data.split(':')[1])
        actualizar_puntos(callback.from_user.id, puntos)
        await callback.answer(f"🎉 ¡+{puntos} puntos!", show_alert=True)
