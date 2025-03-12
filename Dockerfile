# Usa una imagen oficial de Python
FROM python:3.10

# Establece el directorio de trabajo en el contenedor
WORKDIR /app

# Instalar dependencias del sistema necesarias antes de instalar Python packages
RUN apt-get update && apt-get install -y \
    libpq-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copia solo requirements.txt primero para aprovechar el caché de Docker
COPY requirements.txt .  

# Instalar las dependencias de Python
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt  

# Ahora copia el resto de los archivos del proyecto al contenedor
COPY . .

# Asegurar permisos de ejecución en el script principal
RUN chmod +x bot.py  

# Define el comando para ejecutar el bot
CMD ["python", "bot.py"]
