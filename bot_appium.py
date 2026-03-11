
import random
import time
import subprocess
import wave
import os
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions.pointer_input import PointerInput

def get_human_driver() -> webdriver.Remote:
    """
    Configura y devuelve un driver de Appium con capacidades diseñadas
    para emular un dispositivo real y persistir la sesión de LinkedIn.
    """
    options = UiAutomator2Options()

    options.automation_name = "UiAutomator2"
    options.app_package = "com.linkedin.android"
    options.app_activity = "com.linkedin.android.authenticator.LaunchActivity"
    options.no_reset = True
    options.new_command_timeout = 240

    try:
        driver = webdriver.Remote("http://127.0.0.1:4723", options=options)
        return driver
    except Exception as e:
        print(f"Error al conectar con el servidor de Appium: {e}")
        exit()

def human_click(driver: webdriver.Remote, element_text: str) -> None:
    """
    Realiza un clic "humano" en un elemento, con pausas y una ligera
    aleatoriedad en la ubicación del clic para evitar la detección.
    """
    try:
        print(f"Buscando el elemento con texto: '{element_text}'")
        wait = WebDriverWait(driver, 15)
        element = wait.until(EC.presence_of_element_located((AppiumBy.XPATH, f'//*[@text="{element_text}"]')))

        print("Elemento encontrado. Calculando clic humano...")
        location = element.location
        size = element.size

        offset_x = random.randint(-size['width'] // 4, size['width'] // 4)
        offset_y = random.randint(-size['height'] // 4, size['height'] // 4)

        click_x = location['x'] + size['width'] // 2 + offset_x
        click_y = location['y'] + size['height'] // 2 + offset_y

        finger = PointerInput("touch", "finger")
        actions = ActionChains(driver)

        actions.w3c_actions.pointer_action.move_to_location(click_x, click_y)
        actions.w3c_actions.pointer_action.pointer_down()
        actions.w3c_actions.pointer_action.pause(random.uniform(0.05, 0.15))
        actions.w3c_actions.pointer_action.pointer_up()

        actions.perform()
        print("Clic humano ejecutado.")

    except Exception as e:
        print(f"No se pudo hacer clic en el elemento '{element_text}'. Error: {e}")
        driver.save_screenshot(f"error_click_{element_text}.png")

def human_swipe(driver: webdriver.Remote, direction: str = "down") -> None:
    """
    Simula un scroll (swipe) con "micro-temblores" y aceleración variable.
    """
    print(f"Realizando swipe humano hacia {direction}...")
    dims = driver.get_window_rect()
    width = dims['width']
    height = dims['height']

    start_x = random.randint(int(width * 0.4), int(width * 0.6))
    end_x = start_x + random.randint(-int(width * 0.1), int(width * 0.1))

    if direction == "down":
        start_y = random.randint(int(height * 0.7), int(height * 0.8))
        end_y = random.randint(int(height * 0.2), int(height * 0.3))
    else:  # up
        start_y = random.randint(int(height * 0.2), int(height * 0.3))
        end_y = random.randint(int(height * 0.7), int(height * 0.8))

    finger = PointerInput("touch", "finger")
    actions = ActionChains(driver)

    actions.w3c_actions.pointer_action.move_to_location(start_x, start_y)
    actions.w3c_actions.pointer_action.pointer_down()
    actions.w3c_actions.pointer_action.pause(random.uniform(0.1, 0.2))
    actions.w3c_actions.pointer_action.move_to_location(end_x, end_y)
    actions.w3c_actions.pointer_action.pointer_up()

    actions.perform()
    print("Swipe completado.")

def obtener_duracion_audio(ruta_archivo: str) -> float:
    try:
        with wave.open(ruta_archivo, 'r') as f:
            frames = f.getnframes()
            rate = f.getframerate()
            return frames / float(rate)
    except Exception as e:
        print(f"Error leyendo duración del audio: {e}")
        return 5.0 # Fallback de seguridad

def enviar_audio_en_vivo(driver: webdriver.Remote, ruta_audio: str = "audios_in/audio_prueba.wav") -> None:
    """
    Simula la grabación y envío de una nota de voz. PhantomMic inyectará
    el audio automáticamente cuando la app abra el micrófono.
    """
    if not os.path.exists(ruta_audio):
        print(f"¡ERROR CRÍTICO! No se encuentra el archivo de audio local en: {os.path.abspath(ruta_audio)}")
        return

    duracion_real = obtener_duracion_audio(ruta_audio)
    buffer_humano = random.uniform(0.25, 0.75)
    duracion_total = duracion_real + buffer_humano
    
    print(f"Iniciando nota de voz: {duracion_real:.2f}s (Audio) + {buffer_humano:.2f}s (Buffer) = {duracion_total:.2f}s de presión táctil.")
    
    try:
        driver.hide_keyboard()
    except Exception:
        pass

    time.sleep(random.uniform(0.8, 1.5))

    try:
        caja_texto = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((AppiumBy.CLASS_NAME, "android.widget.EditText"))
        )
        pantalla = driver.get_window_size()
        ancho_pantalla = pantalla['width']
        loc = caja_texto.location
        size_caja = caja_texto.size
        touch_x = int(ancho_pantalla * 0.90)
        touch_y = loc['y'] + (size_caja['height'] // 2)
        
        print(f"Coordenadas calculadas del micrófono: X={touch_x}, Y={touch_y}")
        
        print("Preparando acción de mantener presionado el micrófono...")
        
        actions = ActionChains(driver)
        actions.w3c_actions.pointer_action.move_to_location(touch_x, touch_y)
        actions.w3c_actions.pointer_action.pointer_down()
        actions.w3c_actions.pointer_action.pause(duracion_total)
        actions.w3c_actions.pointer_action.pointer_up()

        print("Dedo apoyado. Reproduciendo audio en VirtualMic...")
        # Iniciar reproducción de audio a través del micrófono virtual (PulseAudio)
        audio_process = subprocess.Popen([
            "paplay", 
            "--device=VirtualMic", 
            ruta_audio
        ])

        # Se ejecuta todo el bloque de una vez en Appium (bloquea hasta que termine la duración)
        actions.perform()
        
        print("Grabación finalizada. Buscando botón de confirmación...")
        
        # Asegurarse de que el proceso termine
        try:
            audio_process.terminate()
            audio_process.wait(timeout=2)
        except Exception:
            pass
        
        confirm_button = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((AppiumBy.XPATH, "//*[@text='Enviar' or @text='Send' or @content-desc='Enviar' or @content-desc='Send']"))
        )
        confirm_button.click()
        print("Audio inyectado, confirmado y enviado exitosamente.")

        time.sleep(random.uniform(1.0, 2.0))

    except Exception as e:
        print(f"Error al intentar enviar la nota de voz: {e}")
        driver.save_screenshot("error_audio.png")

def abrir_chat_inteligente(driver: webdriver.Remote, nombre: str) -> None:
    """
    Abre un chat de forma inteligente, buscando primero en la pantalla actual
    y luego utilizando la barra de búsqueda si es necesario.
    """
    try:
        print(f"Intento 1: Buscando a '{nombre}' directamente en la pantalla.")
        human_click(driver, nombre)
        print(f"Chat con '{nombre}' abierto directamente.")
    except Exception:
        print(f"Intento 2: '{nombre}' no está visible. Usando la barra de búsqueda.")
        try:
            search_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((AppiumBy.XPATH, "//*[@content-desc='Search'] | //*[@text='Search messages']"))
            )
            search_element.click()
            search_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((AppiumBy.XPATH, "//*[@text='Search']"))
            )
            search_input.send_keys(nombre)
            time.sleep(2)
            human_click(driver, nombre)
            print(f"Chat con '{nombre}' abierto desde la búsqueda.")
        except Exception as e_search:
            print(f"No se pudo encontrar o abrir el chat del contacto '{nombre}'. Error: {e_search}")
            driver.save_screenshot(f"error_abrir_chat_{nombre}.png")

def editar_ultimo_mensaje(driver: webdriver.Remote, texto_original: str, nuevo_texto: str) -> None:
    """
    Busca un mensaje específico por su texto, lo mantiene presionado 5 segundos
    para desplegar el menú de opciones inferior, y edita el contenido con el
    nuevo texto proporcionado, reemplazando el anterior.
    """
    try:
        wait = WebDriverWait(driver, 15)
        
        print(f"Buscando el mensaje a editar: '{texto_original}'...")
        # Usa un XPath que busque texto exacto o parcial si hace falta. Para mayor precisión usamos exacto.
        mensaje = wait.until(EC.presence_of_element_located((AppiumBy.XPATH, f"//*[@text='{texto_original}']")))
        
        print("Mensaje encontrado. Manteniendo presionado durante al menos 5 segundos...")
        loc = mensaje.location
        size = mensaje.size
        touch_x = loc['x'] + (size['width'] // 2)
        touch_y = loc['y'] + (size['height'] // 2)
        
        # Mantener pulsado el mensaje por ~5.5 segundos
        actions = ActionChains(driver)
        actions.w3c_actions.pointer_action.move_to_location(touch_x, touch_y)
        actions.w3c_actions.pointer_action.pointer_down()
        actions.w3c_actions.pointer_action.pause(5.5)
        actions.w3c_actions.pointer_action.pointer_up()
        actions.perform()
        
        print("Buscando la opción 'Editar' o 'Edit' en la sección desplegada...")
        btn_editar = wait.until(EC.presence_of_element_located((
            AppiumBy.XPATH, "//*[@text='Editar' or @text='Edit' or @content-desc='Editar' or @content-desc='Edit']"
        )))
        btn_editar.click()
        
        print("Apertura de la edición. Localizando la caja de texto original...")
        caja_texto = wait.until(EC.presence_of_element_located((AppiumBy.CLASS_NAME, "android.widget.EditText")))
        
        print("Borrando texto anterior y colocando el nuevo...")
        # clear() suele ser suficiente en Appium. Si llegase a fallar, habría que emular un 'select all + delete key'
        caja_texto.clear()
        caja_texto.send_keys(nuevo_texto)
        
        print("Confirmando la edición del mensaje...")
        # Suele ser una tilde/Guardar o el mismo botón de "Send"/"Enviar"
        btn_confirmar = wait.until(EC.presence_of_element_located((
            AppiumBy.XPATH, "//*[@text='Enviar' or @text='Send' or @content-desc='Enviar' or @content-desc='Send' or @text='Guardar' or @text='Save' or @content-desc='Guardar']"
        )))
        btn_confirmar.click()
        
        print(f"Mensaje editado con éxito. Nuevo estado: '{nuevo_texto}'")
        time.sleep(1.5)
        
    except Exception as e:
        print(f"No se pudo completar la edición del mensaje. Error: {e}")
        driver.save_screenshot("error_editar_mensaje.png")

def send_voice_note(ruta_audio: str, target_user: str) -> None:
    """
    Función de entrada para ser llamada por server.py.
    Abre Appium, busca el contacto y le envía el audio.
    """
    print(f"Iniciando el bot de Appium para enviar audio a '{target_user}'...")
    driver = get_human_driver()
    time.sleep(10)
    
    print("Iniciando interacción con el contacto...")
    abrir_chat_inteligente(driver, target_user)
    enviar_audio_en_vivo(driver, ruta_audio)
    
    print("Esperando 5 segundos antes de cerrar...")
    time.sleep(5)
    driver.quit()
    print(f"\nEl envío de la nota de voz a '{target_user}' ha finalizado exitosamente.")

def edit_message_flow(target_user: str, texto_original: str, nuevo_texto: str) -> None:
    """
    Función de entrada para ser llamada por el servidor u otros scripts.
    Se conecta, abre el chat del usuario, y edita un mensaje con texto específico.
    """
    print(f"Iniciando Appium para editar un mensaje de '{target_user}'...")
    driver = get_human_driver()
    time.sleep(10)
    
    print("Iniciando interacción con el contacto para edición...")
    abrir_chat_inteligente(driver, target_user)
    
    editar_ultimo_mensaje(driver, texto_original, nuevo_texto)
    
    print("Esperando 5 segundos antes de cerrar...")
    time.sleep(5)
    driver.quit()
    print(f"\nLa edición del mensaje para '{target_user}' ha finalizado exitosamente.")

if __name__ == "__main__":
    print("Iniciando el bot de evasión para LinkedIn...")
    driver = get_human_driver()
    time.sleep(10)
    print("Comenzando caminata aleatoria por el feed...")
    for _ in range(random.randint(3, 5)):
        human_swipe(driver, direction="down")
        time.sleep(random.uniform(2, 5))
    print('''
--- Fin de la caminata aleatoria ---
''')
    print("Iniciando interacción con un contacto...")
    abrir_chat_inteligente(driver, "Santiago Meneguzzi")
    enviar_audio_en_vivo(driver)
    
    # --- EJEMPLO DE CÓMO USAR LA EDICIÓN DE MENSAJES ---
    # Para probar la edición de texto, puedes descomentar la siguiente línea 
    # y asegurarte de que exista un mensaje con el texto "Mensaje de prueba" en el chat.
    # editar_ultimo_mensaje(driver, texto_original="Mensaje de prueba", nuevo_texto="Mensaje editado por el bot!")
    # ----------------------------------------------------

    print("Esperando 5 segundos antes de cerrar...")
    time.sleep(5)
    driver.quit()
    print("\nEl bot ha finalizado su ejecución de forma segura.")
