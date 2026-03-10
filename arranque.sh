#!/bin/bash

echo "🚀 Iniciando configuración rápida para LeadLinked AI..."

# 1. Instalar LinkedIn
echo "📦 Instalando app..."
adb -s emulator-5554 install linkedin.apk

# 2. Abrir la app
echo "📱 Abriendo LinkedIn..."
adb -s emulator-5554 shell monkey -p com.linkedin.android -c android.intent.category.LAUNCHER 1 > /dev/null 2>&1

echo "⏳ Esperando 10 segundos para que cargue la app..."
sleep 10

# 3. Inyectar Correo
echo "👉 HACE CLIC en 'Iniciar Sesión' y luego en el campo de 'Correo electrónico'."
read -p "Presioná ENTER cuando el cursor esté parpadeando..."
adb -s emulator-5554 shell input text "santiagomercadoluna26@gmail.com"

# 4. Inyectar Nueva Contraseña
echo "👉 HACE CLIC en el campo de 'Contraseña'."
read -p "Presioná ENTER cuando el cursor esté parpadeando..."
adb -s emulator-5554 shell input text "aAntiagob168"

echo "✅ Listo. Hacé clic en 'Iniciar sesión' en el celular."

# 5. El Código de Verificación (NUEVO)
echo "------------------------------------------------"
echo "🚨 ATENCIÓN: LinkedIn te va a pedir el código de verificación."
echo "👉 Buscá el código en tu correo y hacé clic en el campo numérico del emulador."
read -p "⌨️  Escribí el código acá en la terminal y presioná ENTER: " CODIGO_2FA

# Inyectamos el código que escribiste
adb -s emulator-5554 shell input text "$CODIGO_2FA"

echo "✅ Código inyectado. ¡Apretá enviar y ya estamos adentro de la Matrix!"
echo "------------------------------------------------"
