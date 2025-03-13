from aiogram import Dispatcher, types
from config import ADMIN_ID

async def start_command(message: types.Message):
    await message.answer("🎮 ¡Bienvenido al sistema de gamificación en Railway!\n\n🔹 Pronto podrás ganar puntos y desbloquear premios.")

async def admin_panel(message: types.Message):
    if message.from_user.id == ADMIN_ID:
        await message.answer("⚙️ Panel de administración activado.")
    else:
        await message.answer("❌ No tienes permiso para acceder a esta función.")
        @dp.message_handler(commands=['mipuntaje'])
    async def mi_puntaje(message: types.Message):
        puntos, nivel = obtener_puntos(message.from_user.id)
        await message.reply(f"📊 *Tu puntaje actual:*\n\n🔹 Puntos: {puntos}\n🔹 Nivel: {nivel}", parse_mode="Markdown")

    @dp.message_handler(commands=['top'])
    async def top_usuarios(message: types.Message):
        top = obtener_top_usuarios()

        if not top:
            await message.reply("Aún no hay jugadores en el ranking.")
            return

        ranking = "\n".join([f"{i+1}. {user[0]} - {user[1]} puntos" for i, user in enumerate(top)])
        await message.reply(f"🏆 *Top 10 Jugadores:*\n\n{ranking}", parse_mode="Markdown")

def register_handlers(dp: Dispatcher):
    dp.register_message_handler(start_command, commands="start")
    dp.register_message_handler(admin_panel, commands="admin")
