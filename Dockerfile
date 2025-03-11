FROM python:3.10  # Usa una imagen oficial de Python (puedes elegir la versión que prefieras)

# Instalar dependencias del sistema necesarias
RUN apt-get update && apt-get install -y sqlite3

# Establece el directorio de trabajo en el contenedor
WORKDIR /app

# Copia todos los archivos del proyecto al contenedor
COPY . .

# Instalar las dependencias de Python desde requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Define el comando para ejecutar el bot
CMD ["python", "main.py"]  # O el archivo que usas para iniciar el bot
