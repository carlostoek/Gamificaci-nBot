from aiogram import types
from aiogram.dispatcher import Dispatcher
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from database import actualizar_puntos

def register_callback_handlers(dp: Dispatcher):
    @dp.message_handler(commands=['publicar_encuesta'])
    async def crear_encuesta(message: types.Message):
        teclado = InlineKeyboardMarkup().row(
            InlineKeyboardButton("🔥 Me encantó (+5)", callback_data="reaccion:5"),
            InlineKeyboardButton("👍 Buen contenido (+3)", callback_data="reaccion:3")
        )
        await message.reply("¿Qué te pareció este contenido?", reply_markup=teclado)

    @dp.callback_query_handler(lambda c: c.data.startswith('reaccion:'))
    async def procesar_reaccion(callback: types.CallbackQuery):
        puntos = int(callback.data.split(':')[1])
        actualizar_puntos(callback.from_user.id, puntos)
        await callback.answer(f"🎉 ¡+{puntos} puntos!", show_alert=True)
