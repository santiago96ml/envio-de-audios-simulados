from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import JSONResponse
import os
import shutil
from bot_appium import send_voice_note  # Importamos nuestra lógica de Appium

app = FastAPI(title="LeadLinked AI - Webhook")

# Asegurarse de que el directorio audios_in existe
UPLOAD_DIR = "audios_in"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/webhook/n8n/audio")
async def receive_audio_from_n8n(
    target_user: str = Form(...),
    audio: UploadFile = File(...)
):
    """
    Recibe un audio y un usuario objetivo desde n8n (o Chatwoot),
    lo guarda localmente y desencadena la automatización de Appium.
    """
    if not audio.filename:
        raise HTTPException(status_code=400, detail="No se proporcionó ningún archivo de audio.")

    # Guardar el archivo recibido
    file_path = os.path.join(UPLOAD_DIR, audio.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(audio.file, buffer)

    print(f"[*] Recibido {audio.filename} para el usuario {target_user}")

    # Ejecutar la automatización de LinkedIn
    try:
        # Llamamos a nuestro bot pasándole el archivo y el usuario objetivo.
        # En un escenario real bloqueante, esto tardará lo que tarde la automatización.
        # Para producción, esto debería encolarse (ej. Celery/Redis).
        send_voice_note(file_path, target_user)
        
        return JSONResponse(content={
            "status": "success",
            "message": f"Nota de voz enviada exitosamente a {target_user}"
        })
        
    except Exception as e:
        print(f"[✗] Error en la automatización: {e}")
        return JSONResponse(status_code=500, content={
            "status": "error",
            "detail": str(e)
        })

if __name__ == "__main__":
    import uvicorn
    # Corre el servidor en el puerto 8000
    uvicorn.run(app, host="0.0.0.0", port=8000)
