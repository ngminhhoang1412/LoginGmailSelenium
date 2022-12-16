import random
import math
import os
import common.constant as Constant
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from time import sleep
from random import randint, uniform
import selenium.webdriver.support.expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def sleep_for(period):
    sleep(randint(period[0], period[1]))


def type_text(driver, text, xpath, custom_enter=None, paste_text=Constant.PASTE_PERCENTAGE, loading=False,
              refresh=False, script=None):
    input_keyword = None
    try:
        ensure_click(driver, xpath, refresh=refresh)

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

    except NoSuchElementException:
        if script:
            def retry_with_script():
                nonlocal input_keyword
                input_keyword = driver.execute_script(script)
                sleep_for(Constant.SHORT_WAIT)
                input_keyword.clear()
                input_keyword.send_keys(text)
            execute_with_retry(driver, retry_with_script)
        else:
            # TODO: need handling, still meet this case often
            raise
    # After making sure text is already typed, if error, already raised above
    input_keyword.send_keys(Keys.ENTER)

    sleep_for(Constant.SHORT_WAIT)
    if loading:
        sleep(Constant.LOADING_TIMEOUT)


def ensure_click(driver, xpath, retry=Constant.RETRY, refresh=False, script=None):
    try:
        ensure_wait_for_element(driver, xpath)

        def click_search():
            driver.find_element(By.XPATH, xpath).click()
        execute_with_retry(driver, click_search, retry=retry, refresh=refresh)

    except NoSuchElementException:
        if script:
            sleep_for(Constant.SHORT_WAIT)

            def click_with_script():
                driver.execute_script(script)

            execute_with_retry(driver, click_with_script, retry=retry, refresh=refresh)
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
                    refresh_page(driver)
            if i == retry - 1:
                raise
            sleep(Constant.SHORT_TIMEOUT)


def refresh_page(driver):
    driver.get(driver.current_url)
    sleep(Constant.TRANSITION_TIMEOUT)
    driver.refresh()
    sleep(Constant.TRANSITION_TIMEOUT)


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

def get_version(path='C:\Program Files\Google\Chrome\Application'):
    """

    Args:
       path: link to Chrome Application
    """
    try:
        subfolders = [f.name for f in os.scandir(path) if f.is_dir()]
        for folder in subfolders:
            version = folder.split('.')[0]
            if version.isnumeric():
                bit = 1
                return version
    except:
        return 0

