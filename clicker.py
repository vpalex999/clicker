"""
Usage:
    clicker config <filename>

Options:
    <filename>      the configuration file (*.yaml)
"""

import os
import platform
import time

from docopt import docopt
from selenium import webdriver
from selenium.webdriver.common.by import By

from config import Config

BUTTON_ORDERS = (By.LINK_TEXT, "Заявления")
BUTTON_LOGIN = (By.XPATH, "//button[contains(text(), 'Войти')]")
INPUT_LOGIN = (
    By.XPATH, "//input[contains(@name, 'Телефон  /  Email  /  СНИЛС')]")
INPUT_PASSWORD = (By.XPATH, "//input[contains(@name, 'Пароль')]")
IS_AUTHORIZED_USER = (By.XPATH, "//a[contains(@class, 'authorized-user')]")

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
    arguments = docopt(__doc__)  # type: ignore
    config = Config.from_file(arguments["<filename>"])
    wd = webdriver.Chrome(executable_path=get_driver())
    wd.implicitly_wait(6)
    wd.maximize_window()
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

    # обработать форму подозрительной активности.

    # input("Выполните вход в ЛК\nПо завершении нажмите любую клавишу.")
    # btn_orders = wd.find_element(*BUTTON_ORDERS)
    # btn_orders.click()

    time.sleep(10)
