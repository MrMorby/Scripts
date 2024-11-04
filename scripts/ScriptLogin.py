import random
import string
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


#url de inicio de sesión
login_url = 'http://localhost/control/login.php'

#url de inicio de sesión exitoso
succes_url = 'http://localhost/control/stock.php'

#función para generar una cadena aleatoria
def random_string(lenght=5):
    return''.join(random.choices(string.ascii_letters + string.digits, k = lenght))

#inicializar el webDriver
driver = webdriver.Chrome()

#abrimos la pagina de lógin
driver.get(login_url)

try: 
    for i in range(1000):
        #10 vueltas
        user_name = random_string()
        user_password = random_string()

        #esperamos a que el campo esté presente y luego ingresamos las credenciales
        WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.NAME,"user_name"))).clear()
        driver.find_element(By.NAME,"user_name").send_keys(user_name)
        WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.NAME,"user_password"))).clear()
        driver.find_element(By.NAME,"user_password").send_keys(user_password)

        #enviar formulario del login 
        driver.find_element(By.NAME,"user_password").submit()

        #esperamos que cargue tras el intento

        #verificar si la url cambió si es así el login es exitoso
        if driver.current_url == succes_url:
            print(f"Intento{i+1}: Inicio de sesión exitoso con el usuario = '{user_name}' y la contraseña '{user_password}' ")
            driver.get(login_url)
        else:
            try:
                error_message = driver.find_element(By.ID, "error-message").text
                print(f"Intento{i+1}: Inicio de sesión fallido con el usuario = '{user_name}' y la contraseña '{user_password}'.Mensaje de error: '{error_message}' ")
            except:
                print(f"Intento{i+1}: Inicio de sesión fallido con el usuario = '{user_name}' y la contraseña '{user_password}'. Pero no se encontró mensaje de error")
            
            #recargar la página para el siguiente intento
            driver.get(login_url)
except Exception as e:
    print("error: ", e)

finally:
    #cerramos el navegador después de todos los intentos
    driver.quit()

        