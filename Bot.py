import logging
import sqlite3
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.utils import executor

# 🔹 Configuración
TOKEN = "7676417512:AAEgAR_NWZWraG5SjPR2eIzHdk8angR0UxQ"
ADMIN_ID = 6181290784  # Reemplázalo con tu ID de Telegram

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# 🔹 Base de Datos SQLite
conn = sqlite3.connect("gamificacion.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS usuarios (
    user_id INTEGER PRIMARY KEY,
    puntos INTEGER DEFAULT 0,
    nivel TEXT DEFAULT '🔥 Nuevo Kinky'
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS compras (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    monto INTEGER,
    estado TEXT DEFAULT 'pendiente'
)
""")

conn.commit()

# 🔹 Teclado Principal (Dashboard)
def get_main_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=2)
    buttons = [
        InlineKeyboardButton("📊 Ver Puntos", callback_data="ver_puntos"),
        InlineKeyboardButton("🏆 Ranking", callback_data="ver_ranking"),
        InlineKeyboardButton("🎖 Insignias", callback_data="ver_insignias"),
        InlineKeyboardButton("🔝 Niveles", callback_data="ver_niveles"),
        InlineKeyboardButton("🛒 Registrar Compra", callback_data="registrar_compra")
    ]
    keyboard.add(*buttons)
    return keyboard

# 🔹 Comando /start
@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    user_id = message.from_user.id
    cursor.execute("INSERT OR IGNORE INTO usuarios (user_id) VALUES (?)", (user_id,))
    conn.commit()
    
    await message.answer("🔥 ¡Bienvenido al sistema de gamificación! Usa los botones para ver tu progreso:", 
                         reply_markup=get_main_keyboard())

# 🔹 Ver Puntos
@dp.callback_query_handler(lambda c: c.data == "ver_puntos")
async def ver_puntos(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    cursor.execute("SELECT puntos, nivel FROM usuarios WHERE user_id = ?", (user_id,))
    user_data = cursor.fetchone()

    if user_data:
        puntos, nivel = user_data
        await bot.answer_callback_query(callback_query.id)
        await bot.send_message(user_id, f"🔥 Tienes {puntos} puntos.\n📈 Nivel actual: {nivel}")
    else:
        await bot.answer_callback_query(callback_query.id, "❌ No tienes datos registrados.")

# 🔹 Ranking (Top 10)
@dp.callback_query_handler(lambda c: c.data == "ver_ranking")
async def ver_ranking(callback_query: CallbackQuery):
    cursor.execute("SELECT user_id, puntos FROM usuarios ORDER BY puntos DESC LIMIT 10")
    ranking = cursor.fetchall()

    mensaje = "🏆 **TOP 10 Usuarios** 🏆\n\n"
    for i, (user_id, puntos) in enumerate(ranking, start=1):
        mensaje += f"{i}. 🆔 {user_id} - {puntos} puntos\n"

    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, mensaje)

# 🔹 Ver Insignias
@dp.callback_query_handler(lambda c: c.data == "ver_insignias")
async def ver_insignias(callback_query: CallbackQuery):
    mensaje = """🎖 **Insignias Disponibles** 🎖

🏆 *Kinky Rookie* → Primer mes en el canal (+20 puntos).
🔥 *Kinky Fanático* → 50 reacciones en publicaciones (+50 puntos).
💰 *Kinky Supporter* → Primera compra (+100 puntos).
🎟️ *Kinky VIP Buyer* → Gasto acumulado de $500 (+500 puntos).
"""
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, mensaje)

# 🔹 Ver Niveles
@dp.callback_query_handler(lambda c: c.data == "ver_niveles")
async def ver_niveles(callback_query: CallbackQuery):
    mensaje = """🔝 **Niveles y Requisitos** 🔝

🔥 *Nuevo Kinky* (0-99 puntos) → Acceso al canal.
💎 *Kinky VIP* (100-499 puntos) → Contenido adicional cada mes.
👑 *Kinky Elite* (500-999 puntos) → Acceso anticipado a contenido especial + sorteos.
🚀 *Kinky Legend* (+1000 puntos) → Descuento en suscripción + insignia especial.
"""
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, mensaje)

# 🔹 Registrar Compra
@dp.callback_query_handler(lambda c: c.data == "registrar_compra")
async def registrar_compra(callback_query: CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, "🛒 Ingresa el monto de tu compra:")

@dp.message_handler(lambda message: message.text.isdigit())
async def procesar_compra(message: types.Message):
    user_id = message.from_user.id
    monto = int(message.text)

    cursor.execute("INSERT INTO compras (user_id, monto) VALUES (?, ?)", (user_id, monto))
    conn.commit()

    await message.answer("✅ Tu compra ha sido registrada y está pendiente de aprobación.")

    # Notificación a la Administradora
    await bot.send_message(ADMIN_ID, f"🛒 Nueva compra registrada:\n\n👤 Usuario: {user_id}\n💰 Monto: {monto} pesos.\n\n✅ Usa /aprobar_compra {user_id} {monto} para aprobar.")

# 🔹 Aprobar Compra (Solo Administradora)
@dp.message_handler(lambda message: message.text.startswith("/aprobar_compra") and str(message.from_user.id) == str(ADMIN_ID))
async def aprobar_compra(message: types.Message):
    try:
        _, user_id, monto = message.text.split()
        user_id, monto = int(user_id), int(monto)

        cursor.execute("UPDATE compras SET estado='aprobada' WHERE user_id = ? AND monto = ?", (user_id, monto))
        cursor.execute("UPDATE usuarios SET puntos = puntos + ? WHERE user_id = ?", (monto, user_id))
        conn.commit()

        await message.answer("✅ Compra aprobada y puntos añadidos.")
        await bot.send_message(user_id, f"🎉 ¡Tu compra de {monto} pesos ha sido aprobada! Se te han agregado {monto} puntos.")

    except Exception as e:
        await message.answer(f"❌ Error: {e}")

# 🔹 Iniciar el bot
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True)
