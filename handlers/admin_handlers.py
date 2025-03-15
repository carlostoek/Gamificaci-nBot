from aiogram import types
from aiogram.dispatcher import Dispatcher
from database import actualizar_puntos, obtener_usuario

def register_admin_handlers(dp: Dispatcher, admin_id: int):
    """Registra los comandos de administrador."""
    
    @dp.message_handler(commands=['sumarpuntos'])
    async def cmd_sumarpuntos(message: types.Message):
        # Verificar permisos
        if message.from_user.id != admin_id:
            await message.reply("❌ Solo para administradores.")
            return
        
        try:
            # Obtener parámetros del comando
            _, user_id, puntos = message.text.split()
            user_id = int(user_id)
            puntos = int(puntos)
            
            # Aplicar bonificación por renovación consecutiva
            usuario = obtener_usuario(user_id)
            bonus = 100 if usuario and usuario[6] >= 3 else 0  # Índice 6 = meses_consecutivos
            
            # Actualizar puntos
            actualizar_puntos(user_id, puntos + bonus)
            await message.reply(f"✅ {puntos + bonus} puntos asignados al usuario {user_id}.")
        
        except Exception as e:
            await message.reply(f"⚠️ Error: {str(e)}. Usa: /sumarpuntos [user_id] [puntos]")
