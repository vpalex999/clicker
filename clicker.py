import os
import platform
import time
from selenium import webdriver
from selenium.webdriver.common.by import By

BUTTON_ORDERS = (By.LINK_TEXT, "Заявления")


def get_driver():
    driver_path = {
        "Win": os.path.normpath(os.path.abspath('chromedriver.exe')),
        "Linux": os.path.normpath(os.path.abspath('chromedriver')),
    }

    os_type = platform.system()
    return driver_path[os_type]


if __name__ == "__main__":
    wd = webdriver.Chrome(executable_path=get_driver())
    wd.maximize_window()
    wd.get("https://www.gosuslugi.ru/")
    input("Выполните вход в ЛК\nПо завершении нажмите любую клавишу.")
    btn_orders = wd.find_element(*BUTTON_ORDERS)
    btn_orders.click()

    time.sleep(5)
