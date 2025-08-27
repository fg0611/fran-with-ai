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
from dotenv import load_dotenv
import os
from supabase import create_client
import re
from datetime import datetime

# Configuración
load_dotenv(dotenv_path=r"C:\Users\Francisco\Desktop\DEV_STUFF\00_OPTIBOT\automatizacion-wp\fran-with-ai\send\.env")
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
admin_phone = os.environ.get("ADMIN_PHONE")

supabase = create_client(url, key)

EDGE_DRIVER_PATH = r"C:\Users\Francisco\Desktop\DEV_STUFF\00_OPTIBOT\automatizacion-wp\fran-with-ai\send\drivers\msedgedriver.exe"
busqueda = 'diseno'
dir_archivo = f'C:/Users/Francisco/Desktop/DEV_STUFF/00_OPTIBOT/automatizacion-wp/fran-with-ai/send/archivos/{busqueda}.csv'

fecha_envio = datetime.now().isoformat(timespec='minutes').replace(':', '-')
historial_csv = f'enviados-{busqueda}-{fecha_envio}.csv'

def limpiar_string(s):
    return re.sub(r'[^\w\s]', '', s, flags=re.UNICODE)
    # return re.sub(r'[^a-zA-Z0-9\s]', '', s)

def buscar_lead(numero_contacto):
    try:
        response = supabase.table("leads").select("*").eq("id", numero_contacto).limit(1).execute()
        data = response.data
        if data:
            print("ℹ️ Lead encontrado:", data[0])
            return data[0]  # lead existente
        else:
            print("ℹ️ El Lead no existe aún")
            return None  # lead no encontrado
    except Exception as e:
        print("❌ Error al buscar lead:", e)
        return None

# Función para insertar contacto
def insertar_lead(numero_contacto, nombre):
    nuevo_lead = {
        "id": numero_contacto,
        "is_active": True,
        "origin": admin_phone,
        "name": nombre,
        "current_step": "greeting",
    }
    try:
        response = supabase.table("leads").insert(nuevo_lead).execute()
        print("✅ Lead insertado correctamente:", response.data)
        return True
    except Exception as e:
        print("❌ Error al insertar lead:", e)
        return False

# Insertar mensaje en chats
def insertar_chat(numero_contacto, mensaje):
    nuevo_chat = {
        "session_id": numero_contacto,
        "message": mensaje,
        "is_from_user": False,
        "metadata": {}
    }
    try:
        response = supabase.table("chats").insert(nuevo_chat).execute()
        print("✅ mensaje guardado en chats", response.data)
        return True
    except Exception as e:
        print("❌ Error al insertar chat:", e)
        return False

def espera_random(desde, hasta):
    return round(random.uniform(desde, hasta), 1)

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
        print("🔄 QR disponible")
        
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
            xpath_contact = '//*[@id="app"]/div/div[3]/div/div[2]/div[1]/span/div/span/div/div[2]/div[3]'
            contact_btn = WebDriverWait(driver, random.randint(2, 3)).until(
                EC.element_to_be_clickable((By.XPATH, xpath_contact)))
        except:
            print('No encontró el primer xpath del contacto, va al segundo de nro conocido')
            try:
                xpath_contact = '//*[@id="app"]/div[1]/div[3]/div/div[2]/div[1]/span/div/span/div/div[2]/div[2]/div/div/div[2]/div'
                contact_btn = WebDriverWait(driver, random.randint(2, 3)).until(
                    EC.element_to_be_clickable((By.XPATH, xpath_contact))
                )
            except:
                print(f"❌ No se encontró el contacto {numero} - Saltando...")
                # Limpiar búsqueda fallida
                input_search.send_keys(Keys.CONTROL + 'a', Keys.BACKSPACE)
                xpath_back = '//*[@id="app"]/div/div[3]/div/div[2]/div[1]/span/div/span/div/header/div/div[1]/div'
                back_btn = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, xpath_back)))
                back_btn.click()
                return False
        
        contact_btn.click()
        print(f"✅ Botón de contacto encontrado")
        
        # Paso 6: Pegar mensaje (el input ya está autoseleccionado)
        time.sleep(espera_random(2, 4))
        # msg_input = driver.switch_to.active_element
        msg_input = driver.find_element(By.XPATH, '//*[@id="main"]/footer//div[@contenteditable="true"]')
        # msg_input = driver.find_element(By.XPATH, '//*[@id="main"]/footer/div[1]/div/span/div/div[2]/div/div[3]/div[1]//div[@contenteditable="true"]')
        # msg_input.send_keys(mensaje)

        driver.execute_script("""
            var element = arguments[0];
            var text = arguments[1];
            
            element.focus();
            element.innerText = text;
            
            // Dispara eventos con pequeño retraso
            setTimeout(function() {
                var evt = new InputEvent('input', {
                    bubbles: true,
                    data: text,
                    inputType: 'insertText'
                });
                element.dispatchEvent(evt);
            }, 100);
        """, msg_input, mensaje)
        
        # Paso 7: Enviar mensaje
        try:
            send_btn = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, '//button[@aria-label="Send"]')))
            send_btn.click()
            print(f"✅ Mensaje enviado a {numero}")
            time.sleep(espera_random(2, 4))  # Esperar entre mensajes
            return True
        except Exception as e:
            print(f"❌ No se pudo enviar el mensaje a {numero}. Error: {e}")
            return False
            
    except Exception as e:
        print(f"❌ Ocurrió un error general: {e}")
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

        conteo = pd.read_csv(dir_archivo).shape[0]
        
        if not conteo:
            print("❌ Error : el archivo origen esta vacio")
            return
        
        contactados = 0
        pausa_larga = random.uniform(120, 300)

        while conteo:
            df = pd.read_csv(dir_archivo)
            # df = pd.read_csv(busqueda, header=None, skiprows=1)
            n_muestra = random.randint(1, 3)

            df_contactar = df.head(n_muestra)
            df_sin_muestra = df.iloc[n_muestra:]
            conteo = df_sin_muestra.shape[0]
            # Guardar el CSV original sin las filas usadas
            df_sin_muestra.to_csv(dir_archivo, index=False)
            # Tomar las primeras filas en base a la muestra (o menos si hay menos)
            # CSV acumulativo
            
            for indice, fila in df_contactar.iterrows():

                if contactados >= n_muestra:
                    print(f"⏳ Pausa de {pausa_larga/60:.1f} minutos antes del próximo lote...")
                    time.sleep(pausa_larga)
                    contactados = 0  # Reiniciar contador
                    pausa_larga = random.uniform(120, 300)  # Nueva pausa aleatoria                

                negocio = limpiar_string(fila[0]) if fila[0] else fila[0]
                numero = fila[2]
                # numero = re.sub(r'\D', '', str(fila[2]))
                # ver si existe el lead
                lead = buscar_lead(numero)
                if lead:
                    print("❌ El LEAD ya existe no se enviara el mensaje")
                    continue

                mensaje = f'¡Hola *{negocio}*!\n\nDesde *Precios de Prepagas*, te acercamos propuestas de cobertura médica para particulares, familias y *PyMEs*.\nComercializamos *Sancor Salud*, *Prevención Salud* y *Avalian*.\n\nSi sos PyME, podés armar tu grupo a partir de *5 personas*, que pueden ser empleados o familiares, con planes y tarifas especiales. También tenemos beneficios adicionales para grupos de más de 30 personas.\n\n¿Querés conocer las opciones? Simplemente respondé *SÍ* o *Info* para que podamos ayudarte a encontrar la mejor propuesta sin compromiso.'
                mover_mouse_random(driver)
                envio = enviar_mensaje(driver, numero, mensaje)
                # --- Lógica de actualización de CSV e inserción en Supabase ---
                if envio:
                    contactados += 1
                    df_contactar.loc[indice, "enviado"] = True
                    print(f"✅ Mensaje enviado y se guardará el lead en Supabase")
                    
                    # Insertar en Supabase solo si el mensaje se envió
                    nuevo_lead = insertar_lead(numero, negocio)
                    if nuevo_lead:
                        insertar_chat(numero, mensaje)
                else:
                    df_contactar.loc[indice, "enviado"] = False
                    print(f"❌ Mensaje no enviado. No se creará el lead en Supabase, pero se guardará en el historial.")
                
                # Guardar en histórico acumulativo, independientemente del resultado del envío
                if os.path.exists(historial_csv):
                    df_hist = pd.read_csv(historial_csv)
                    df_hist = pd.concat([df_hist, df_contactar.loc[[indice]]], ignore_index=True)
                else:
                    df_hist = df_contactar.loc[[indice]]
                
                df_hist.to_csv(historial_csv, index=False)
                # -------------------------------------------------------------             
            
        print("🎉 Proceso completado")
        
    except Exception as e:
        print(f"❌ Error crítico: {str(e)}")
    finally:
        print("Terminó el script")
        # driver.quit()

if __name__ == "__main__":
    main()