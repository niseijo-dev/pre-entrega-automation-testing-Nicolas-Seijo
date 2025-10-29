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
    # Hago log in en la página y espero 10s
    login(driver)
    wait = WebDriverWait(driver, 10)

    #Localizo y espero a que el titulo aparezca.
    titleLocalizador = (By.CLASS_NAME, "title")
    titleElemento = wait.until(EC.visibility_of_element_located(titleLocalizador))

    # Verifico que el texto de 'title' sea el correcto
    assert titleElemento.text == "Products"

    #Obtengo la cantidad de productos localizandolo como 'inventory_item' y verifico que no sean 0
    products = driver.find_elements(By.CLASS_NAME, "inventory_item")
    assert len(products) > 0, "No se encontraron productos en la página"

    # Obtengo el nombre y precio del primer producto
    nombrePrimerProd = driver.find_element(By.CSS_SELECTOR, "#item_4_title_link > div").text
    precioPrimerProd = driver.find_element(By.XPATH, "(//div[@class='inventory_item_price'])[1]").text

    # Imprime el nombre y precio del primer producto
    print ("PRIMER PRODUCTO:")
    print("NOMBRE: ", nombrePrimerProd)
    print("PRECIO: ", precioPrimerProd)

def test_carrito(driver):
    #Logueo en la página
    login(driver)

    # Obtengo el nombre del primer producto
    nombreProducto = driver.find_element(By.CSS_SELECTOR, "#item_4_title_link > div").text
    # Localizo el primer boton 'Add to cart' y le doy click
    botonAgregar = driver.find_element(By.XPATH, "(//button[text()='Add to cart'])[1]")
    botonAgregar.click()

    # Espera de 10 segundos
    wait = WebDriverWait(driver, 10)
    #Localizo el indicador de productos del carrito y esperando a que aparezca obtengo el elemento
    numeroCarritoLocalizador = (By.CLASS_NAME, "shopping_cart_badge")
    numeroCarrito = wait.until(EC.visibility_of_element_located(numeroCarritoLocalizador))

    #Verifico que el texto del indicador de cantidad de productos del carrito sea 1
    assert numeroCarrito.text == "1", "El contador del carrito no es 1"

    # Localizo el elemento 'Link' del Carrito, osea el botón para ir al carrito, y lo clickeo.
    linkCarrito = driver.find_element(By.CLASS_NAME, "shopping_cart_link")
    linkCarrito.click()

    # Localizo el nombre del item del carrito y esperando a que aparezca extraigo su texto
    itemCarritoLocalizador = (By.CLASS_NAME, "inventory_item_name")
    itemCarrito = wait.until(EC.visibility_of_element_located(itemCarritoLocalizador)).text
    
    # Verifico que el nombre del producto en el carrito sea el mismo que el del catálogo
    assert nombreProducto == itemCarrito, "El producto en el carrito no coincide" 
