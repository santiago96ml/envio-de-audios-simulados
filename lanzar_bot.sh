#!/bin/bash

# Activar el entorno virtual de Python
echo "Activando entorno virtual..."
source venv/bin/activate

# Iniciar el servidor de Appium en segundo plano, redirigiendo la salida
echo "Iniciando Appium en segundo plano..."
appium > /dev/null 2>&1 &

# Esperar 5 segundos para asegurar que Appium se haya iniciado completamente
echo "Esperando que Appium se inicie (5 segundos)..."
sleep 5

# Ejecutar el script del bot de Python
echo "Lanzando el bot de LinkedIn..."
python3 bot_appium.py
