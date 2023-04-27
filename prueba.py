# Prueba de automatización Selenium con Python
# --------------------------------------------
import os
import requests
import unittest
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
script_dir = os.path.dirname(os.path.realpath(__file__))
chromepath = os.path.join(script_dir, "drivers/chromedriver")
firefoxpath= os.path.join(script_dir, "drivers/geckodriver")
class PythonSelenium(unittest.TestCase) :
    def setUp(self): # Inicializamos el driver requerido en selenium para la prueba front
        ser = Service(chromepath)
        op = webdriver.ChromeOptions()
        driver = webdriver.Chrome(service=ser, options=op)
        driver.get("https://duckduckgo.com/")
        self.driver = driver
    
    def click(self, by_locator):
        """ Performs click to locator find element """
        try:
            WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(by_locator)).click()
        except TimeoutException:
            assert False, "Locator is missing"
        except:
            assert False, "Couldn't perform click"

    def send_keys(self, by_locator, text):
        """ Send keys to locator with text """
        try:
            WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(by_locator)).send_keys(text)
        except TimeoutException:
            assert False, "Locator is missing"
        except:
            assert False, "Couldn't perform send_keys"

    def url_changed(self, expected_url):
        """ Check url has changed """
        try:
            WebDriverWait(self.driver, 10).until(EC.url_to_be(expected_url))

        except TimeoutException:
            assert False, "Missing expected URL"

    def test_status(self): # Este test incluye la prueba de back donde comprobamos el código y la fuente de la respuesta.
        response = requests.get("https://api.duckduckgo.com/api/?q=Toledo&format=json")
        res = response.json()
        print("Status code: "+str(response.status_code))
        print("AbstractSource: "+res['AbstractSource'])
        self.assertEqual(response.status_code,200)
        self.assertEqual('Wikipedia', res['AbstractSource'])

        url_list = [res['AbstractURL'], res['RelatedTopics'][0]['FirstURL']]

        print(url_list)
        print("\n")
    def test_buscador(self): # Este test incluye la prueba donde se navega a través de la web, usando las herramientas de selenium   
        self.assertIn("DuckDuckGo", self.driver.title)
        self.send_keys((By.XPATH, "//*[@id='search_form_input_homepage']"), "Toledo")
        self.click((By.XPATH, "//*[@id='search_button_homepage']"))
        self.click((By.XPATH, "//*[@href='https://es.wikipedia.org/wiki/Toledo']"))
        self.url_changed("https://es.wikipedia.org/wiki/Toledo")
        self.assertIn("Toledo - Wikipedia, la enciclopedia libre", self.driver.title)

    def tearDown(self): # Cerramos el driver 
        self.driver.close()

if __name__ == "__main__":
 unittest.main()

