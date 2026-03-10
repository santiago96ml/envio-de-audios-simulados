
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
    Simula la grabación y envío de una nota de voz en vivo en un chat de LinkedIn,
    inyectando un audio real en el proceso.
    """
    if not os.path.exists(ruta_audio):
        print(f"¡ERROR CRÍTICO! No se encuentra el archivo de audio en la ruta: {os.path.abspath(ruta_audio)}")
        return

    duracion_real = obtener_duracion_audio(ruta_audio)
    buffer_humano = random.uniform(0.25, 0.75)
    duracion_total = duracion_real + buffer_humano
    
    print(f"Iniciando nota de voz: {duracion_real:.2f}s (Audio) + {buffer_humano:.2f}s (Buffer) = {duracion_total:.2f}s de presión táctil.")
    
    # Resiliencia: Esconder el teclado si está abierto
    try:
        print("Intentando esconder el teclado...")
        driver.hide_keyboard()
        print("Teclado escondido (o ya estaba oculto).")
    except Exception:
        pass # Ignorar si no hay teclado

    dwell_time_before = random.uniform(0.8, 1.5)
    print(f"Pausa de deliberación: {dwell_time_before:.2f}s")
    time.sleep(dwell_time_before)

    try:
        # 1. Encontrar la barra de escribir mensaje (es el único EditText en pantalla)
        print("Buscando caja de texto como anclaje espacial...")
        caja_texto = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((AppiumBy.CLASS_NAME, "android.widget.EditText"))
        )
        
        # 2. Calcular coordenadas físicas del micrófono (a la derecha de la caja)
        pantalla = driver.get_window_size()
        ancho_pantalla = pantalla['width']
        
        loc = caja_texto.location
        size_caja = caja_texto.size
        
        # X: 90% a la derecha de la pantalla. Y: Centro vertical de la caja de texto.
        touch_x = int(ancho_pantalla * 0.90) 
        touch_y = loc['y'] + (size_caja['height'] // 2)
        
        print(f"Coordenadas calculadas del micrófono: X={touch_x}, Y={touch_y}")
        
        # 1. Bajar el dedo
        actions = ActionChains(driver)
        actions.w3c_actions.pointer_action.move_to_location(touch_x, touch_y)
        actions.w3c_actions.pointer_action.pointer_down()
        actions.perform()
        print("Dedo apoyado. Abriendo micrófono...")
        
        time.sleep(0.8) # Espera a que la app reaccione
        
        # 2. Inyectar Voz Real
        print(f"Inyectando voz real: {ruta_audio}")
        proceso_audio = subprocess.Popen(["ffmpeg", "-re", "-i", ruta_audio, "-f", "pulse", "VirtualMic"])
        
        # 3. Mantener presionado mientras dura el audio
        time.sleep(duracion_total + 1.2)
        
        # 4. Levantar el dedo
        actions_up = ActionChains(driver)
        actions_up.w3c_actions.pointer_action.pointer_up()
        actions_up.perform()
        print("Grabación finalizada. Buscando botón de confirmación...")
        
        # 6. Confirmar el envío
        print("Esperando cuadro de diálogo de confirmación...")
        confirm_button = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((AppiumBy.XPATH, "//*[@text='Enviar' or @text='Send' or @content-desc='Enviar' or @content-desc='Send']"))
        )
        confirm_button.click() # Clic directo en el elemento ya localizado.
        print("Audio inyectado, confirmado y enviado exitosamente.")

        dwell_time_after = random.uniform(1.0, 2.0)
        print(f"Pausa post-envío: {dwell_time_after:.2f}s")
        time.sleep(dwell_time_after)

    except Exception as e:
        print(f"Error al intentar enviar la nota de voz: {e}")
        driver.save_screenshot("error_audio.png")

def abrir_chat_inteligente(driver: webdriver.Remote, nombre: str) -> None:
    """
    Abre un chat de forma inteligente, buscando primero en la pantalla actual
    y luego utilizando la barra de búsqueda si es necesario.
    """
    try:
        # Intento 1: Buscar directamente en la pantalla actual
        print(f"Intento 1: Buscando a '{nombre}' directamente en la pantalla.")
        human_click(driver, nombre)
        print(f"Chat con '{nombre}' abierto directamente.")
    except Exception:
        # Intento 2: Usar la barra de búsqueda si falla el primer intento
        print(f"Intento 2: '{nombre}' no está visible. Usando la barra de búsqueda.")
        try:
            # Hacer clic en el icono/barra de búsqueda
            search_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((AppiumBy.XPATH, "//*[@content-desc='Search'] | //*[@text='Search messages']"))
            )
            search_element.click()
            print("Elemento de búsqueda clickeado.")

            # Escribir el nombre en el campo de búsqueda que aparece
            search_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((AppiumBy.XPATH, "//*[@text='Search']"))
            )
            search_input.send_keys(nombre)
            print(f"Nombre '{nombre}' ingresado en la búsqueda.")

            time.sleep(2) # Esperar resultados

            # Hacer clic en el resultado
            human_click(driver, nombre)
            print(f"Chat con '{nombre}' abierto desde la búsqueda.")

        except Exception as e_search:
            print(f"No se pudo encontrar o abrir el chat del contacto '{nombre}'. Error: {e_search}")
            driver.save_screenshot(f"error_abrir_chat_{nombre}.png")

if __name__ == "__main__":
    print("Iniciando el bot de evasión para LinkedIn...")
    driver = get_human_driver()

    print("Esperando 10 segundos a que la app se estabilice...")
    time.sleep(10)

    print("Comenzando caminata aleatoria por el feed...")
    for _ in range(random.randint(3, 5)):
        human_swipe(driver, direction="down")
        time.sleep(random.uniform(2, 5))

    print("\n--- Fin de la caminata aleatoria ---\n")
    print("Iniciando interacción con un contacto...")

    # ¡NUEVA LÓGICA INTELIGENTE CON NOMBRE CORREGIDO!
    abrir_chat_inteligente(driver, "Santiago Meneguzzi")

    enviar_audio_en_vivo(driver)

    print("Esperando 5 segundos antes de cerrar...")
    time.sleep(5)

    driver.quit()
    print("\nEl bot ha finalizado su ejecución de forma segura.")
