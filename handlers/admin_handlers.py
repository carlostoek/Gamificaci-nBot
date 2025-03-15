from aiogram import types
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database import actualizar_puntos, obtener_usuario

def register_admin_handlers(dp: Dispatcher, admin_id: int):
    # Panel de administrador con botones inline
    @dp.message_handler(commands=['admin'])
    async def panel_administrador(message: types.Message):
        if message.from_user.id != admin_id:
            return
        
        teclado = InlineKeyboardMarkup(row_width=2)
        teclado.add(
            InlineKeyboardButton("➕ Sumar Puntos", callback_data="admin_sumar_puntos"),
            InlineKeyboardButton("📊 Estadísticas", callback_data="admin_estadisticas"),
            InlineKeyboardButton("📢 Publicar Encuesta", callback_data="admin_publicar_encuesta"),
            InlineKeyboardButton("🔙 Salir", callback_data="menu_principal")
        )
        await message.reply("🔧 **Panel de Administrador**", reply_markup=teclado)

    # Handler para "Sumar Puntos"
    @dp.callback_query_handler(lambda c: c.data == "admin_sumar_puntos")
    async def pedir_datos_sumar_puntos(callback: types.CallbackQuery):
        await callback.message.edit_text(
            "🔢 **Ingresa los datos en este formato:**\n\n"
            "`ID_Usuario Cantidad_Puntos`\n"
            "Ejemplo: `123456789 150`",
            parse_mode="Markdown"
        )
        # Configurar estado para esperar la entrada
        from bot import dp
        await dp.current_state().set_state("esperando_datos_puntos")

    # Procesar datos para sumar puntos
    @dp.message_handler(state="esperando_datos_puntos")
    async def procesar_sumar_puntos(message: types.Message, state: FSMContext):
        try:
            user_id, puntos = map(int, message.text.split())
            usuario = obtener_usuario(user_id)
            if usuario:
                actualizar_puntos(user_id, puntos)
                await message.reply(f"✅ +{puntos} puntos asignados a @{usuario[1]}!")
            else:
                await message.reply("❌ Usuario no encontrado.")
        except:
            await message.reply("⚠️ Formato incorrecto. Usa: `ID_Usuario Puntos`")
        finally:
            await state.finish()
