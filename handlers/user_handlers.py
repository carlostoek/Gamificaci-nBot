from aiogram import types
from aiogram.dispatcher import Dispatcher
import sqlite3

def register_handlers(dp: Dispatcher):
    @dp.message_handler(commands=['mispuntos'])
    async def cmd_mispuntos(message: types.Message):
        user_id = message.from_user.id
        conn = sqlite3.connect('vip_gamification.db')
        c = conn.cursor()
        c.execute('SELECT puntos, nivel FROM usuarios WHERE user_id = ?', (user_id,))
        resultado = c.fetchone()
        await message.reply(f"🏅 Nivel: {resultado[1]}\n🔢 Puntos: {resultado[0]}")
        conn.close()

    @dp.message_handler(commands=['ranking'])
    async def cmd_ranking(message: types.Message):
        conn = sqlite3.connect('vip_gamification.db')
        c = conn.cursor()
        c.execute('SELECT username, puntos FROM usuarios ORDER BY puntos DESC LIMIT 10')
        ranking = ["🏆 Ranking VIP:"]
        for idx, (user, pts) in enumerate(c.fetchall(), 1):
            ranking.append(f"{idx}. {user}: {pts} puntos")
        await message.reply("\n".join(ranking))
        conn.close()
