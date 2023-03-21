import os
import platform
import time
from selenium import webdriver
from selenium.webdriver.common.by import By

BUTTON_ORDERS = (By.LINK_TEXT, "Заявления")
BUTTON_LOGIN = (By.XPATH, "//button[contains(text(), 'Войти')]")
INPUT_LOGIN = (By.XPATH, "//input[contains(@name, 'Телефон  /  Email  /  СНИЛС')]")
INPUT_PASSWORD = (By.XPATH, "//input[contains(@name, 'Пароль')]")

url_login = "https://esia.gosuslugi.ru/login/"
url_gos = "https://www.gosuslugi.ru/"


def get_driver():
    driver_path = {
        "Win": os.path.normpath(os.path.abspath('chromedriver.exe')),
        "Linux": os.path.normpath(os.path.abspath('chromedriver')),
    }

    os_type = platform.system()
    return driver_path[os_type]


if __name__ == "__main__":
    wd = webdriver.Chrome(executable_path=get_driver())
    wd.implicitly_wait(6)
    wd.maximize_window()
    wd.get(url_login)
    button_login = wd.find_element(*BUTTON_LOGIN)
    
    field_login = wd.find_element(*INPUT_LOGIN)
    field_login.click()
    field_login.send_keys("ццццц")
    
    field_password = wd.find_element(*INPUT_PASSWORD)
    field_password.click()
    field_password.send_keys("ццццц")
    
    button_login.click()
    
    # обработать форму подозрительной активности.
    # логин и пароль вынести в конфиг
    
    input("Выполните вход в ЛК\nПо завершении нажмите любую клавишу.")
    btn_orders = wd.find_element(*BUTTON_ORDERS)
    btn_orders.click()

    time.sleep(5)
