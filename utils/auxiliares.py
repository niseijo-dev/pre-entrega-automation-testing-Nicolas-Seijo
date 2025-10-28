#Importo "By" de Selenium
from selenium.webdriver.common.by import By

# Declaro las constantes
USER = "standard_user"
PASSWORD = "secret_sauce"
URL = "https://www.saucedemo.com/"

def login(driver):
    driver.get(URL)
 
    # Encuentra e ingresa las credenciales con las constantes declaradas.
    driver.find_element(By.ID, "user-name").send_keys(USER)
    driver.find_element(By.ID, "password").send_keys(PASSWORD)

    # Hace click en login
    driver.find_element(By.ID, "login-button").click()