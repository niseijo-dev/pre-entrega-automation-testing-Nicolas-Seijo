#Importo Pytest
import pytest

#Importo Selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utils.auxiliares import login

#Declaro la fixture con scope="function" para que se ejecute antes y después de cada test.
@pytest.fixture(scope="function")
def driver():
    service = Service() 
    driver = webdriver.Edge(service=service)
    
    # Reintenta buscar elementos por 5 segundos antes de fallar.
    driver.implicitly_wait(5) 
    driver.maximize_window()
    
    # Uso 'yield' entregar el driver a la función de prueba.
    yield driver
    
    #Hago .quit() para cerrar todo en cada test.
    driver.quit()

def test_catalogo(driver):
    login(driver)
    wait = WebDriverWait(driver, 10)

    titleLocalizador = (By.CLASS_NAME, "title")
    titleElemento = wait.until(EC.visibility_of_element_located(titleLocalizador))

    assert titleElemento.text == "Products"

    products = driver.find_elements(By.CLASS_NAME, "inventory_item")
    assert len(products) > 0, "No se encontraron productos en la página"

    nombrePrimerProd = driver.find_element(By.XPATH, "(//div[@class='inventory_item_name'])[1]").text
    precioPrimerProd = driver.find_element(By.XPATH, "(//div[@class='inventory_item_price'])[1]").text

    print ("PRIMER PRODUCTO:")
    print("NOMBRE: ", nombrePrimerProd)
    print("PRECIO: ", precioPrimerProd)
