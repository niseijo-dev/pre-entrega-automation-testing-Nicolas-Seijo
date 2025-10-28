import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

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
