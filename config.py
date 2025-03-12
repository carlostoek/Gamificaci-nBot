import os
from dotenv import load_dotenv

# Cargar variables del archivo .env
load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID", "0"))  # Convertir a entero
ADMIN_ID = int(os.getenv("ADMIN_TELEGRAM_ID", "0"))
