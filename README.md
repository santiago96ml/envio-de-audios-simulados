# 🚀 LeadLinked AI - Voice Automation

**LeadLinked AI** es un sistema de prospección inteligente diseñado para automatizar el envío de notas de voz personalizadas en LinkedIn. El proyecto utiliza una combinación de **Appium** para la automatización de la interfaz móvil y **PulseAudio** para la inyección de audio a nivel de hardware virtual.

## 🛠️ Stack Tecnológico
* **Lenguaje:** Python 3.10+
* **Automatización Móvil:** Appium + UIAutomator2
* **Servidor de Audio:** PulseAudio (Linux)
* **Procesamiento de Audio:** FFmpeg & paplay

## 📂 Estructura del Proyecto
* `bot_appium.py`: Core del bot (Navegación e interacción).
* `audios_in/`: Directorio de archivos `.wav` para inyectar.
* `config/`: Archivos de configuración de entorno.

## 📝 Historial de Cambios (Changelog)

### Versión 1.1
* **Fiabilidad de Audio Mejorada:** Se ha reescrito por completo la lógica de envío de notas de voz para simular de forma infalible la interacción humana.
    1. **Presión Inmediata:** El bot ahora presiona el botón de grabar y *luego* espera a que la aplicación active el micrófono.
    2. **Sincronización Perfecta:** La inyección de audio con FFmpeg se inicia únicamente después de una pausa de seguridad, asegurando que LinkedIn esté escuchando.
    3. **Buffer Humano:** Se ha añadido un tiempo extra de presión después de que el audio termina para emular una grabación natural.
* **Ruta de Audio Unificada:** Se establece `audios_in/audio_prueba.wav` como el archivo de audio por defecto para todas las operaciones, eliminando ambigüedades.
* **Mayor Tolerancia:** El tiempo de espera para encontrar el botón 'Enviar' se ha aumentado a 15 segundos, haciendo el bot más robusto ante demoras de la red o del dispositivo.
