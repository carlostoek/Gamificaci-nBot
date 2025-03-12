from aiogram import Dispatcher, types
from config import ADMIN_ID

async def start_command(message: types.Message):
    """ Responde al comando /start """
    await message.answer(f"🎮 ¡Bienvenido al sistema de gamificación!\n\n🔹 Pronto podrás ganar puntos y desbloquear premios.")

async def admin_panel(message: types.Message):
    """ Panel de administrador """
    if message.from_user.id == ADMIN_ID:
        await message.answer("⚙️ Panel de administración activado.")
    else:
        await message.answer("❌ No tienes permiso para acceder a esta función.")

def register_handlers(dp: Dispatcher):
    dp.register_message_handler(start_command, commands="start")
    dp.register_message_handler(admin_panel, commands="admin")
