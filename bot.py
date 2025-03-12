import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

# ----------------------------
# Configuración y variables
# ----------------------------
TOKEN = os.getenv("BOT_TOKEN")  # Debe estar definida en las variables de entorno
# Si necesitas usar algún canal o grupo, puedes definirlo aquí también:
CHANNEL_ID = os.getenv("CHANNEL_ID", None)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

logging.basicConfig(level=logging.INFO)

# ----------------------------
# Módulo: Puntos (XP)
# ----------------------------
def register_points_handlers(dp: Dispatcher):
    @dp.message_handler(commands=["mispuntos"])
    async def mispuntos_handler(message: types.Message):
        # Lógica básica: por ahora se envía un valor fijo. Luego se puede integrar con una base de datos.
        xp = 0  # Valor inicial o consultado de la DB
        await message.reply(f"🎯 Tienes {xp} XP.\n(Función en desarrollo)")

# ----------------------------
# Módulo: Ranking
# ----------------------------
def register_ranking_handlers(dp: Dispatcher):
    @dp.message_handler(commands=["ranking"])
    async def ranking_handler(message: types.Message):
        # Lógica básica para el ranking: se muestra un mensaje de ejemplo.
        ranking_text = (
            "🏆 **Top 10 de XP**:\n"
            "1. UsuarioX - 0 XP\n"
            "2. UsuarioY - 0 XP\n"
            "(Función en desarrollo)"
        )
        await message.reply(ranking_text, parse_mode="Markdown")

# ----------------------------
# Módulo: Registro de Compras
# ----------------------------
def register_purchase_handlers(dp: Dispatcher):
    @dp.message_handler(commands=["registrarcompra"])
    async def registrar_compra_handler(message: types.Message):
        # Esta función deberá registrar la compra y actualizar los XP del usuario.
        await message.reply("💰 Compra registrada. (Función en desarrollo)")

# ----------------------------
# Módulo: Ayuda
# ----------------------------
def register_help_handler(dp: Dispatcher):
    @dp.message_handler(commands=["help"])
    async def help_handler(message: types.Message):
        help_text = (
            "🤖 **Bot de Gamificación VIP - Ayuda**\n\n"
            "Comandos disponibles:\n"
            "/mispuntos - Consulta tus XP.\n"
            "/ranking - Muestra el ranking de usuarios.\n"
            "/registrarcompra - Registra una compra manual.\n"
            "(Más funciones próximamente)"
        )
        await message.reply(help_text, parse_mode="Markdown")

# ----------------------------
# Función para registrar todos los handlers
# ----------------------------
def register_all_handlers(dp: Dispatcher):
    register_points_handlers(dp)
    register_ranking_handlers(dp)
    register_purchase_handlers(dp)
    register_help_handler(dp)
    # Aquí podrás agregar más módulos sin interferir con los existentes.

# ----------------------------
# Función principal del bot
# ----------------------------
def main():
    register_all_handlers(dp)
    executor.start_polling(dp, skip_updates=True)

if __name__ == "__main__":
    main()
