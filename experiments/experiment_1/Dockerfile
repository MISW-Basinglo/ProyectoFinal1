# Usa una imagen base de Python
FROM python:3.9-slim

# Establecer directorio de trabajo
WORKDIR /app

# Copiar el archivo requirements.txt y el código de la aplicación
COPY requirements.txt requirements.txt
COPY . .

# Instalar las dependencias de Python
RUN pip install -r requirements.txt

# Comando para ejecutar la aplicación Flask
CMD ["python", "main.py"]
