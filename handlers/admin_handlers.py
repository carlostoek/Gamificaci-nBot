from aiogram import types
from aiogram.dispatcher import Dispatcher
import sqlite3

def register_handlers(dp: Dispatcher):
    @dp.message_handler(commands=['sumarpuntos'])
    async def cmd_sumarpuntos(message: types.Message):
        if message.from_user.id != ADMIN_ID:
            return
        
        _, user_id, puntos = message.text.split()
        conn = sqlite3.connect('vip_gamification.db')
        c = conn.cursor()
        
        # Aplicar bonificaciones
        c.execute('SELECT meses_consecutivos FROM usuarios WHERE user_id = ?', (user_id,))
        meses = c.fetchone()[0]
        bonus = 100 if meses >= 3 else 0
        
        puntos_totales = int(puntos) + bonus
        c.execute('UPDATE usuarios SET puntos = puntos + ? WHERE user_id = ?', (puntos_totales, user_id))
        
        await message.reply(f"✅ {puntos_totales} puntos asignados a @{message.from_user.username}")
        conn.commit()
        conn.close()
