import random
import math

import login_gmail_selenium.common.constant as Constant
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from time import sleep
from random import randint, uniform
import selenium.webdriver.support.expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def sleep_for(period):
    sleep(randint(period[0], period[1]))


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


