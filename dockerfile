FROM python:3.11

WORKDIR /app

# 1. Instalar dependencias del sistema y configurar repositorio de Microsoft
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    gnupg2 \
    unixodbc-dev \
    && curl -fsSL https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor -o /usr/share/keyrings/microsoft.gpg \
    && echo "deb [arch=amd64 signed-by=/usr/share/keyrings/microsoft.gpg] https://packages.microsoft.com/debian/11/prod bullseye main" > /etc/apt/sources.list.d/mssql-tools.list \
    && apt-get update \
    # 2. Instalar Drivers ODBC (Aceptando la licencia EULA explícitamente)
    && ACCEPT_EULA=Y apt-get install -y --no-install-recommends \
    msodbcsql17 \
    mssql-tools \
    && rm -rf /var/lib/apt/lists/*

# 3. Instalar dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copiar el código de la aplicación
COPY . .

# 5. Comando de arranque (ajusta si tu comando de reflex es diferente)
CMD ["reflex", "run"]