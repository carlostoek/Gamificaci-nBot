from aiogram import types
from aiogram.dispatcher import Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import sqlite3

def register_handlers(dp: Dispatcher):
    @dp.message_handler(commands=['publicar_encuesta'])
    async def publicar_encuesta(message: types.Message):
        teclado = InlineKeyboardMarkup().add(
            InlineKeyboardButton("🔥 Me encantó", callback_data="reaccion:5")
        )
        await message.reply(
            "¿Te gustó este contenido?",
            reply_markup=teclado
        )

    @dp.callback_query_handler(lambda c: c.data.startswith('reaccion:'))
    async def procesar_reaccion(callback: types.CallbackQuery):
        puntos = int(callback.data.split(':')[1])
        user_id = callback.from_user.id
        
        conn = sqlite3.connect('vip_gamification.db')
        c = conn.cursor()
        c.execute('UPDATE usuarios SET puntos = puntos + ? WHERE user_id = ?', (puntos, user_id))
        conn.commit()
        conn.close()
        
        await callback.answer(f"🎉 +{puntos} puntos obtenidos!")
