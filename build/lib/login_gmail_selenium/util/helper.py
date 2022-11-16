import os
import random
import shutil
import zipfile

import requests
import math

from cryptography.fernet import Fernet

import login_gmail_selenium.common.constant as Constant
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
import fake_headers.browsers as browsers
from time import sleep
from random import randint, uniform
import selenium.webdriver.support.expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def sleep_for(period):
    sleep(randint(period[0], period[1]))


def get_random_number(period):
    return randint(period[0], period[1])


def scroll_to_element(driver, element, retry=Constant.RETRY):
    for i in range(retry):
        sleep_for(Constant.SHORT_WAIT)
        driver.execute_script("arguments[0].scrollIntoView();", element)
        desired_y = (element.size['height'] / 2) + element.location['y']
        current_y = (driver.execute_script('return window.innerHeight') / 2) + driver.execute_script(
            'return window.pageYOffset')
        scroll_y_by = desired_y - current_y
        driver.execute_script("window.scrollBy(0, arguments[0]);", scroll_y_by)


def type_text(driver, text, xpath, custom_enter=None, paste_text=Constant.PASTE_PERCENTAGE, loading=False):
    ensure_click(driver, xpath)

    input_keyword = ensure_find_element(driver, xpath)
    input_keyword.clear()

    if random.randrange(100) < paste_text:
        input_keyword.send_keys(text)
    else:
        for letter in text:
            input_keyword.send_keys(letter)
            sleep(uniform(.1, .4))

    # TODO: improve later with this block, search icon can be unable to find
    # if random.choice([True, False]) and (custom_enter is not None):
    #     icon = driver.find_element(By.XPATH, )
    #     ensure_click(driver, icon)
    # else:
    input_keyword.send_keys(Keys.ENTER)

    sleep_for(Constant.SHORT_WAIT)
    if loading:
        sleep(Constant.LOADING_TIMEOUT)


def ensure_click(driver, xpath, retry=Constant.RETRY, refresh=False):
    ensure_wait_for_element(driver, xpath)

    def click_search():
        driver.find_element(By.XPATH, xpath).click()
    execute_with_retry(driver, click_search, retry=retry, refresh=refresh)
    sleep_for(Constant.SHORT_WAIT)


def update_chrome_version():
    link = 'https://gist.githubusercontent.com/MShawon/29e185038f22e6ac5eac822a1e422e9d/raw/versions.txt'

    output = requests.get(link, timeout=60).text
    chrome_versions = output.split('\n')

    browsers.chrome_ver = chrome_versions


def execute_with_retry(driver, callback, error=Exception, retry=Constant.RETRY, with_result=False, refresh=False):
    for i in range(retry):
        try:
            if with_result:
                return callback()
            else:
                callback()
            break
        except error:
            if refresh:
                should_refresh = i == math.floor(retry / 2)
                if should_refresh:
                    driver.get(driver.current_url)
                    sleep(Constant.TRANSITION_TIMEOUT)
                    driver.refresh()
                    sleep(Constant.TRANSITION_TIMEOUT)
            if i == retry - 1:
                raise
            sleep(Constant.SHORT_TIMEOUT)


def ensure_wait_for_element(driver, xpath):
    try:
        WebDriverWait(driver, Constant.LOADING_TIMEOUT).until(EC.visibility_of_element_located(
            (By.XPATH, xpath)))
    except TimeoutException:
        # Item might be there already but not fully loaded (i guess)
        pass


def ensure_find_element(driver, xpath):
    def get_element():
        return driver.find_element(By.XPATH, xpath)

    return execute_with_retry(driver, get_element, with_result=True)


def random_scroll(driver):
    sleep_for(Constant.SHORT_WAIT)
    for i in range(7):
        sleep_for(Constant.WIDE_WAIT)
        action = random.choice([Keys.DOWN, Keys.END, Keys.UP, Keys.HOME, Keys.SPACE,
                                Keys.F11, Keys.ARROW_DOWN, Keys.ARROW_UP, Keys.F5])
        driver.find_element(By.TAG_NAME, 'body').send_keys(action)


def encrypt_file(file_path):
    key = Constant.env["KEY"]
    key = key.encode('utf-8')
    fernet = Fernet(key)
    with open(file_path, 'rb') as file:
        original = file.read()

    encrypted = fernet.encrypt(original)
    with open(file_path, 'wb') as encrypted_file:
        encrypted_file.write(encrypted)


def delete(path):
    if os.path.isfile(path) or os.path.islink(path):
        os.remove(path)
    elif os.path.isdir(path):
        shutil.rmtree(path)
    else:
        raise ValueError("Path {} is not a file or dir.".format(path))


def unzip(in_path, out_path):
    with zipfile.ZipFile(in_path, "r") as zip_ref:
        zip_ref.extractall(out_path)


def decrypt(path):
    key = Constant.env["KEY"]
    key = key.encode('utf-8')
    fernet = Fernet(key)
    with open(path, 'rb') as enc_file:
        encrypted = enc_file.read()
    decrypted = fernet.decrypt(encrypted)
    with open(path, 'wb') as dec_file:
        dec_file.write(decrypted)
