from aiogram import types
from database import registrar_usuario, obtener_puntajes, sumar_puntos

# Registrar usuario en la base de datos al enviar /start
async def start(message: types.Message):
    user_id = message.from_user.id
    username = message.from_user.username
    registrar_usuario(user_id, username)
    await message.answer(f"¡Hola {username}! Estás registrado en el sistema. Usa /puntaje para ver tus puntos.")

# Consultar los puntos de un usuario
async def puntaje(message: types.Message):
    user_id = message.from_user.id
    puntos = obtener_puntajes(user_id)
    await message.answer(f"Tu puntaje actual es: {puntos} puntos.")

# Comando para sumar puntos
async def sumar_puntos_usuario(message: types.Message):
    user_id = message.from_user.id
    # Se pueden definir más lógicas para sumar puntos, aquí lo haré de forma estática
    sumar_puntos(user_id, 10)  # Suma 10 puntos como ejemplo
    await message.answer("¡Has sumado 10 puntos!")

# Registrar todos los comandos
def register_handlers(dp):
    dp.register_message_handler(start, commands=["start"])
    dp.register_message_handler(puntaje, commands=["puntaje"])
    dp.register_message_handler(sumar_puntos_usuario, commands=["sumar_puntos"])
