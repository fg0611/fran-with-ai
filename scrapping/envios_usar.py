from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import random
import pandas as pd

def espera_random(desde, hasta):
    return round(random.uniform(desde, hasta), 1)

# Configuración
EDGE_DRIVER_PATH = r"C:\Users\Francisco\Desktop\DEV_STUFF\00_OPTIBOT\automatizacion-wp\msedgedriver.exe"

def iniciar_navegador():
    options = Options()
    options.add_argument("--start-maximized")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    
    service = Service(EDGE_DRIVER_PATH)
    driver = webdriver.Edge(service=service, options=options)
    return driver

def esperar_sesion(driver):
    print("🔍 Por favor escanea el código QR de WhatsApp Web...")
    
    try:
        # 1. Esperar a que desaparezca el QR (máximo 2 minutos)
        WebDriverWait(driver, 120).until(
            EC.invisibility_of_element_located((By.XPATH, '//canvas[@aria-label="Scan me!"]')))
        print("🔄 QR escaneado correctamente")
        
        # 2. Esperar y cerrar el modal de bienvenida (si existe)
        try:
            boton_ok_xpath = '//*[@id="app"]/div/span[2]/div/div/div/div/div/div/div[2]/div/button'
            boton_ok = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((By.XPATH, boton_ok_xpath)))
            boton_ok.click()
            print("✅ Modal de bienvenida cerrado")
            time.sleep(espera_random(2, 4))  # Pequeña pausa después de cerrar el modal
        except:
            print("⚠️ No se encontró modal de bienvenida (puede ignorarse)")
        
        # 3. Espera simplificada - Solo verificar lista de chats
        print("🔄 Verificando carga de la lista de chats...")
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, '//div[@aria-label="Chat list"]')))
        
        # 4. Pausa adicional fija de 4 segundos
        time.sleep(espera_random(3, 5))
        print("✅ Sesión lista después de espera adicional")
        
        print("✅ Sesión completamente cargada y lista")
        
    except Exception as e:
        print(f"❌ Error crítico durante inicio de sesión: {str(e)}")
        # Tomar screenshot para diagnóstico
        driver.save_screenshot("error_sesion.png")
        print("📸 Se ha guardado un screenshot como 'error_sesion.png'")
        raise

def enviar_mensaje(driver, numero, mensaje):
    try:
        btn_path = '//*[@id="app"]/div/div[3]/div/div[3]/header/header/div/span/div/div[1]/button'
        # Paso 3: Buscar botón New chat
        new_chat_btn = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, btn_path)))
        new_chat_btn.click()
        time.sleep(espera_random(2, 4))
        # Paso 4: Pegar número telefónico (el input ya está autoseleccionado)
        input_search = driver.switch_to.active_element
        input_search.send_keys(Keys.CONTROL + 'a')  # Seleccionar todo por si hay texto
        input_search.send_keys(Keys.BACKSPACE)      # Limpiar
        input_search.send_keys(numero)
        time.sleep(espera_random(2, 4))  # Esperar resultados de búsqueda
        
        # Paso 5: Intentar hacer click en el contacto
        try:
            # xpath_contact = '//*[@id="app"]/div/div[3]/div/div[2]/div[1]/span/div/span/div/div[2]/div[2]/div/div/div[2]/div'
            xpath_contact = '//*[@id="app"]/div/div[3]/div/div[2]/div[1]/span/div/span/div/div[2]/div[3]'
            contact_btn = WebDriverWait(driver, random.randint(2, 3)).until(
                EC.element_to_be_clickable((By.XPATH, xpath_contact)))
            contact_btn.click()
        except:
            print(f"❌ No se encontró el contacto {numero} - Saltando...")
            # Limpiar búsqueda fallida
            input_search.send_keys(Keys.CONTROL + 'a', Keys.BACKSPACE)
            xpath_back = '//*[@id="app"]/div/div[3]/div/div[2]/div[1]/span/div/span/div/header/div/div[1]/div'
            back_btn = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, xpath_back)))
            back_btn.click()

            return False
        
        # Paso 6: Pegar mensaje (el input ya está autoseleccionado)
        time.sleep(espera_random(2, 4))
        msg_input = driver.switch_to.active_element
        msg_input.send_keys(f'{mensaje}')
        
        # Paso 7: Enviar mensaje
        send_btn = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, '//button[@aria-label="Send"]')))
        send_btn.click()
        
        print(f"✅ Mensaje enviado a {numero}")
        time.sleep(espera_random(2, 4))  # Esperar entre mensajes
        return True
        
    except Exception as e:
        print(f"⚠️ Error con {numero}: {str(e)}")
        return False
    
def mover_mouse_random(driver):
    actions = ActionChains(driver)
    width = driver.execute_script("return window.innerWidth")  # Ancho de la ventana
    height = driver.execute_script("return window.innerHeight")  # Alto de la ventana
    iterations = random.randint(1, 3)
    for _ in range(iterations):
        # Genera coordenadas aleatorias dentro de la ventana
        x = random.randint(0, width)
        y = random.randint(0, height)
        # Mueve el mouse a la posición (x, y)
        actions.move_by_offset(x, y).perform()
        time.sleep(random.uniform(0.5, 0.9))  # Espera aleatoria
        
        # Opcional: Vuelve a la posición original (evita desplazamientos acumulativos)
        actions.move_by_offset(-x, -y).perform()

def main():
    driver = iniciar_navegador()
    try:
        driver.get("https://web.whatsapp.com")
        esperar_sesion(driver)
        
        nombre_arch = 'tatuajes_2.csv'
        df = pd.read_csv(nombre_arch)
        # df = pd.read_csv(nombre_arch, header=None, skiprows=1)
        if df.empty:
            print("❌ Error : el archivo origen esta vacio")
            return
        n_muestra = random.randint(10, 20)
        df_contactar = None
        # Tomar las primeras 20 filas (o menos si hay menos)
        df_contactar = df.head(n_muestra)
        # Guardar el CSV original sin las primeras 20 filas
        df_sin_20 = df.iloc[n_muestra:]
        df_sin_20.to_csv(nombre_arch, index=False)
        
        if not df_contactar.empty:
            for indice, fila in df_contactar.iterrows():
                negocio = fila[0]
                numero = fila[2].replace(' ', '').replace('-', '')
                numero = f'351{numero[-7:]}'
                # numero = fila[2]
                mensaje = f"Hola {negocio}! Queremos acercarte opciones de cobertura médica con Sancor Salud, Prevención Salud y Avalian. ¿Querés que te contemos cómo funciona? Estamos para ayudarte sin compromiso."
                # print(f'{numero} {mensaje}')
                mover_mouse_random(driver)
                enviar_mensaje(driver, numero, mensaje)
        else:
            print("❌ Error : primeros_20 esta vacio")
            
        print("🎉 Proceso completado")
        
    except Exception as e:
        print(f"❌ Error crítico: {str(e)}")
    finally:
        print(1)
        # driver.quit()

if __name__ == "__main__":
    main()