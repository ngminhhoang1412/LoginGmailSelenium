import undetected_chromedriver as uc2
import os
import common.constant as Constant
from util.helper import type_text, sleep_for, ensure_click, get_version
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import selenium.webdriver.support.expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, NoSuchElementException


class ChromeProfile:

    VIEWPORTS = ['2560,1440', '1920,1080', '1440,900',
                 '1536,864', '1366,768', '1280,1024', '1024,768']
    ACTIVE = os.path.join('extension', 'always_active.zip')

    def __init__(self, email, password, backup_email):
        self.email = email
        self.password = password
        self.backup_email = backup_email
        self.driver = None

    def create_driver(self):

        options = uc2.ChromeOptions()
        path = os.path.join(Constant.PROFILE_FOLDER, self.email)
        options.add_argument(f"--user-data-dir={path}")
        options.add_argument(f"--profile-directory={self.email}")
        options.add_argument("--start-maximized")
        options.add_argument("--disable-web-security")
        options.add_argument("--allow-running-insecure-content")
        prefs = {
            "intl.accept_languages": 'en_US,en',
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False,
            "profile.default_content_setting_values.notifications": 2,
            "download_restrictions": 3,
            "profile.exit_type": "Normal",
            "profile.exited_cleanly": True,
        }
        options.add_experimental_option("prefs", prefs)
        options.add_extension(self.ACTIVE)
        service = Service(executable_path=Constant.PATCHED_DRIVER)
        return uc2.Chrome(options=options, version_main=get_version())

    def check_login_status(self):
        self.driver.get("https://accounts.google.com/")
        try:
            username_xpath = "//*[@id=\"yDmH0d\"]/c-wiz/div/div[2]/div/c-wiz/c-wiz/div/div[3]/div/div/header/h1"
            WebDriverWait(self.driver, Constant.LOADING_TIMEOUT).until(EC.visibility_of_element_located(
                (By.XPATH, username_xpath)))
            username = self.driver.find_element(By.XPATH, username_xpath)
            if username:
                print(username.text)
            else:
                raise ValueError(f"Stuck at my account home page {self.email}")
        except TimeoutException:
            # Account has not been logged in yet
            self.login()

    def login(self):
        driver = self.driver
        driver.get("https://accounts.google.com/signin/v2/identifier?flowName=GlifWebSignIn&flowEntry=ServiceLogin")
        username_xpath = '//*[@id="identifierId"]'
        try:
            # First time login on device, type username
            type_text(driver=self.driver, text=self.email, xpath=username_xpath, loading=True, paste_text=100)
            for x in range(Constant.RETRY):
                if not "challenge" in driver.current_url:
                    type_text(driver=self.driver, text=self.email, xpath=username_xpath, loading=True, paste_text=100)
                else:
                    break
        except TimeoutException:
            # Profile already has at least 1 username, choose profile with correct email
            if "signinchooser" in driver.current_url:
                desired_profile = driver.find_elements_by_xpath(f"//*[contains(text(), '{self.email}')]")
                if desired_profile:
                    desired_profile[0].click()
                else:
                    new_profile_xpath = "//*[@id=\"view_container\"]/div/div/div[2]/div/div[1]/div/form/span/" \
                                        "section/div/div/div/div/ul/li[2]"
                    driver.find_elements_by_xpath(new_profile_xpath)[0].click()
                    type_text(driver=self.driver, text=self.email, xpath=username_xpath, loading=True, paste_text=100)
            # Account has been logged in from another device
            elif "webreauth" in driver.current_url:
                continue_xpath = "//*[@id=\"identifierNext\"]/div/button"
                driver.find_element(By.XPATH, continue_xpath).click()
            else:
                # Usually internet/proxy issue here so will be raised TimeoutException
                raise TimeoutException("This site can't be reached")
        self.check_challenge()
        # If no problem or challenge occurs, proceed to type password
        password_xpath = '//*[@id="password"]/div[1]/div/div[1]/input'
        '//*[@id="password"]/div[1]/div/div[1]/input'
        type_text(driver=self.driver, text=self.password, xpath=password_xpath, loading=True, paste_text=100)
        error_xpath = '//*[@id="view_container"]/div/div/div[2]/div/div[1]/div/form/span/section/div/div/div[2]/div[2]'
        error = None
        try:
            error = driver.find_element(By.XPATH, error_xpath)
        except (NoSuchElementException, TimeoutException):
            pass
        if error:
            self.handle_false_email('Either password changed or something is wrong with account')
        self.check_challenge()

    def check_challenge(self):
        driver = self.driver
        # Bypass when google ask for backup email
        if 'challenge/selection' in driver.current_url:
            path = '//*[@id="view_container"]/div/div/div[2]/div/div[1]/div/form/span/section/div/div/div/ul/li[3]'
            ensure_click(self.driver, path)
            backup_xpath = '//*[@id=\"knowledge-preregistered-email-response\"]'
            type_text(driver=self.driver, text=self.backup_email, xpath=backup_xpath, loading=True)
        elif 'disabled/explanation' in driver.current_url:
            self.handle_false_email('Account disabled')
        # TODO: still 2 more cases to handle: number sent to phone & phone required to login

    def retrieve_driver(self):
        self.driver = self.create_driver()

        return self.driver

    def start(self):
        self.retrieve_driver()
        self.check_login_status()
        sleep_for(Constant.SHORT_WAIT)

    def handle_false_email(self, text):
        pass
