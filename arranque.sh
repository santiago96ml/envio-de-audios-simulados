#!/bin/bash

# Iniciar PulseAudio y desactivar el auto-suspendido para evitar ruido inicial
pulseaudio --start --exit-idle-time=-1 || true
pactl unload-module module-suspend-on-idle || true

# Crear Sink con parámetros NATIVOS de Android (48kHz, Mono)
pactl unload-module module-null-sink || true
pactl load-module module-null-sink sink_name=VirtualMic sink_properties=device.description="Virtual_Microphone" rate=48000 channels=1

# Forzar volumen al 100% en el sink y su monitor
pactl set-sink-volume VirtualMic 100%
pactl set-source-volume VirtualMic.monitor 100%

# Establecer como micrófono predeterminado
pactl set-default-source VirtualMic.monitor

echo "Micrófono virtual configurado. Iniciando emulador..."

# Subir el driver y el audio, apuntando al emulador específico
echo "Instalando PhantomMic Driver..."
adb -s emulator-5554 install phantom_mic.apk

echo "Subiendo archivo de audio..."
adb -s emulator-5554 push audios_in/audio_prueba.wav /sdcard/audio_prueba.wav

# Crear el archivo de configuración para PhantomMic y subirlo
echo "Creando y subiendo configuración de PhantomMic..."
echo "audio_prueba" > phantom.txt
adb -s emulator-5554 push phantom.txt /sdcard/phantom.txt

echo " Iniciando configuración rápida para LeadLinked AI..."

# 1. Instalar LinkedIn
echo " Instalando app..."
adb -s emulator-5554 install linkedin.apk

# 2. Abrir la app
echo " Abriendo LinkedIn..."
adb -s emulator-5554 shell monkey -p com.linkedin.android -c android.intent.category.LAUNCHER 1 > /dev/null 2>&1

echo "⏳ Esperando 10 segundos para que cargue la app..."
sleep 10

# 3. Inyectar Correo
echo " HACE CLIC en 'Iniciar Sesión' y luego en el campo de 'Correo electrónico'."
read -p "Presioná ENTER cuando el cursor esté parpadeando..."
adb -s emulator-5554 shell input text "santiagomercadoluna26@gmail.com"

# 4. Inyectar Nueva Contraseña
echo " HACE CLIC en el campo de 'Contraseña'."
read -p "Presioná ENTER cuando el cursor esté parpadeando..."
adb -s emulator-5554 shell input text "aAntiagob168"

echo "✅ Listo. Hacé clic en 'Iniciar sesión' en el celular."

# 5. El Código de Verificación (NUEVO)
echo "------------------------------------------------"
echo " ATENCIÓN: LinkedIn te va a pedir el código de verificación."
echo " Buscá el código en tu correo y hacé clic en el campo numérico del emulador."
read -p "⌨️  Escribí el código acá en la terminal y presioná ENTER: " CODIGO_2FA

# Inyectamos el código que escribiste
adb -s emulator-5554 shell input text "$CODIGO_2FA"

echo "✅ Código inyectado. ¡Apretá enviar y ya estamos adentro de la Matrix!"
echo "------------------------------------------------"