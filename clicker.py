"""
Usage:
    clicker config <filename> [webdriver <webdriver>]

Options:
    config          flag for using config filename.
    <filename>      get a configuration file (*.yaml).
    webdriver       flag for using external webdriver.
    <webdriver>     get an external webdriver.
"""

import os
import platform
import time
from typing import Optional

from docopt import docopt
from selenium import webdriver
from selenium.webdriver.common.by import By

from config import Config

# локатор: проверка присутствия формы авторизации.
BUTTON_LOGIN = (By.XPATH, "//button[contains(text(), 'Войти')]")

# локатор: поле ввода логина формы авторизации.
INPUT_LOGIN = (
    By.XPATH, "//input[contains(@name, 'Телефон  /  Email  /  СНИЛС')]")

# локатор: поле ввода пароля формы авторизации.
INPUT_PASSWORD = (By.XPATH, "//input[contains(@name, 'Пароль')]")

# локатор: подтверждение, что авторизация прошла.
IS_AUTHORIZED_USER = (By.XPATH, "//a[contains(@class, 'authorized-user')]")

# локатор: Заявление сохранено.
IS_ORDER_SAVED = (By.XPATH, "//h1[contains(text(), 'Заявление сохранено')]")

# локатор: кнопка Отправить заявление.
BUTTON_SEND_ORDER = (
    By.XPATH, "//button/*[@contains(text(), 'Отправить заявление')]")

# локатор: кнопка перейти на Главную.
BUTTON_TO_MAIN = (By.XPATH, "//button/*[contains(text(), 'На главную')]")

# локатор: кнопка "Отправить заявление" в состоянии - выключена(неактивна).
IS_SEND_ORDER_DISABLED = (
    By.XPATH, "//button[@disabled='true' and /*[contains(text(), 'Отправить заявление')]]")

url_login = "https://esia.gosuslugi.ru/login/"
url_gos = "https://www.gosuslugi.ru/"


def get_driver(filename: Optional[str] = None):
    if filename is not None:
        return os.path.normpath(filename)

    driver_path = {
        "Windows": os.path.normpath(os.path.abspath('chromedriver.exe')),
        "Linux": os.path.normpath(os.path.abspath('chromedriver')),
    }

    os_type = platform.system()
    return driver_path[os_type]


if __name__ == "__main__":
    arguments = docopt(__doc__)  # type: ignore
    print(arguments)
    config = Config.from_file(arguments["<filename>"])
    external_driver = arguments["<webdriver>"]
    wd = webdriver.Chrome(executable_path=get_driver(external_driver))

    wd.implicitly_wait(6)
    wd.maximize_window()
    # идем на авторизацию.
    wd.get(url_login)
    button_login = wd.find_element(*BUTTON_LOGIN)

    field_login = wd.find_element(*INPUT_LOGIN)
    field_login.click()
    field_login.send_keys(config.login)

    field_password = wd.find_element(*INPUT_PASSWORD)
    field_password.click()
    field_password.send_keys(config.password)

    button_login.click()

    # ждать авторизации
    wd.implicitly_wait(6)
    wd.find_element(*IS_AUTHORIZED_USER)

    # переход на форму заявления
    wd.get(config.order)
    wd.implicitly_wait(3)
    # цикл отправки формы.
    while True:
        try:
            time.sleep(.2)
            wd.find_element(*IS_ORDER_SAVED)
            btn = wd.find_element(*BUTTON_SEND_ORDER)
            btn.click()
        except Exception as err:
            wd.refresh()
        else:
            #break
            wd.get(config.order)