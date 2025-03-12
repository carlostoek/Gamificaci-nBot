# Usa una imagen oficial de Python
FROM python:3.10

# Establece el directorio de trabajo en el contenedor
WORKDIR /app

# Copia solo requirements.txt primero para aprovechar el caché de Docker
COPY requirements.txt .  

# Instalar las dependencias de Python desde requirements.txt
RUN pip install --no-cache-dir -r requirements.txt  

# Instalar dependencias del sistema necesarias
RUN apt-get update && apt-get install -y sqlite3 && rm -rf /var/lib/apt/lists/*  

# Ahora copia el resto de los archivos del proyecto al contenedor
COPY . .

# Asegurar permisos de ejecución en el script principal
RUN chmod +x main.py  

# Define el comando para ejecutar el bot
CMD ["python", "main.py"]
