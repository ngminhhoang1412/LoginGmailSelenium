from login_gmail_selenium.util.base_profile import ChromeProfile
import undetected_chromedriver as uc2
import os
import shutil
import login_gmail_selenium.common.constant as Constant
import selenium.webdriver.support.expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from login_gmail_selenium.common.log import log_false_email
from login_gmail_selenium.util import helper
from login_gmail_selenium.util.driver import Driver
from login_gmail_selenium.util.helper import type_text, sleep_for, ensure_click, \
    get_version
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

AUTH_TYPES = [
    'private',
    'public',
    None
]


class Profile(ChromeProfile):
    def __init__(self,profile_name, auth_type=AUTH_TYPES[2], path=None, prox=None, prox_type=None,
                 insecure=False):
        super().__init__(auth_type, path, prox, prox_type, insecure)
        self.profile_name = profile_name
        self.profile_folder = Constant.BLANK_PROFILE_FOLDER
