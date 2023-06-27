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


class GoogleProfile(ChromeProfile):

    def __init__(self, email, password, backup_email, auth_type=AUTH_TYPES[2], path=None, prox=None, prox_type=None,
                 insecure=False, false_email_callback=None, change_password_callback=None):
        super().__init__(auth_type, path, prox, prox_type, insecure)
        self.email = email
        self.password = password
        self.backup_email = backup_email
        self.false_email_callback = false_email_callback
        self.change_password_callback = change_password_callback
        self.profile_name = email
        self.profile_folder = Constant.PROFILE_GOOGLE_FOLDER

    def check_login_status(self):
        self.driver.get("https://accounts.google.com/")
        try:
            username_xpath = "//*[@id=\"yDmH0d\"]/c-wiz/div/div[2]/div/c-wiz/c-wiz/div/div[3]/div/div/header/h1"
            WebDriverWait(self.driver, Constant.LOADING_TIMEOUT).until(EC.visibility_of_element_located(
                (By.XPATH, username_xpath)))
            username = self.driver.find_element(By.XPATH, username_xpath)
            if username:
                pass
            else:
                raise ValueError(f"Stuck at my account home page {self.email}")
        except TimeoutException:
            # Account has not been logged in yet
            self.login()

    def login(self):
        driver = self.driver
        driver.get("https://accounts.google.com/signin/v2/identifier?flowName=GlifWebSignIn&flowEntry=ServiceLogin")
        username_xpath = '//*[@id="identifierId"]'
        login_text_retrieve_script = 'return document.querySelector("input[type=\'email\']");'
        try:
            # First time login on device, type username
            type_text(driver=self.driver, text=self.email, xpath=username_xpath, loading=True,
                      script=login_text_retrieve_script, paste_text=100)
        except NoSuchElementException:
            raise
        except (Exception, ValueError):
            # Profile already has at least 1 username, choose profile with correct email
            if "signinchooser" in driver.current_url:
                desired_profile = driver.find_element(By.XPATH, f"//div[contains(text(), '{self.email}')]")
                if desired_profile:
                    desired_profile.click()
                else:
                    new_profile_xpath = "//*[@id=\"view_container\"]/div/div/div[2]/div/div[1]/div/form/span/" \
                                        "section/div/div/div/div/ul/li[2]"
                    ensure_click(driver, new_profile_xpath)
                    type_text(driver=self.driver, text=self.email, xpath=username_xpath, loading=True,
                              script=login_text_retrieve_script)
            # Account has been logged in from another device
            elif "webreauth" in driver.current_url:
                continue_xpath = "//*[@id=\"identifierNext\"]/div/button"
                driver.find_element(By.XPATH, continue_xpath).click()
            else:
                # Usually internet/proxy issue here so will be raised TimeoutException
                raise

        # Mail address incorrectly typed, this is caused by Selenium itself (I guess), fix not required
        if 'identifier' in driver.current_url:
            raise ValueError("Selenium failed to type username")

        self.check_challenge()
        # If no problem or challenge occurs, proceed to type password
        password_text_retrieve_script = 'return document.querySelector("input[type=\'password\']");'
        password_xpath = '//*[@id="password"]/div[1]/div/div[1]/input'
        type_text(driver=self.driver, text=self.password, xpath=password_xpath, loading=True, refresh=True,
                  script=password_text_retrieve_script)
        if 'challenge/pwd' in driver.current_url:
            # Something happens to the account
            get_error_div_script = "return document.querySelectorAll('svg[class=\"stUf5b LxE1Id\"]')[0].childNodes;"
            error_div = driver.execute_script(get_error_div_script)
            if error_div:
                self.handle_false_email(Constant.ACCOUNT_PASSWORD_CHANGED_MESSAGE)
            # Selenium failed to type password
            raise ValueError("Selenium failed to type password")
        self.check_challenge()
        # TODO: still need to handle 1 more case here, when everything is finished,
        #  need to check on account.google to see if logged in or not

    def check_challenge(self):
        driver = self.driver
        # Bypass when google ask for backup email
        if 'challenge/selection' in driver.current_url:
            path = '//*[@id="view_container"]/div/div/div[2]/div/div[1]/div/form/span/section/div/div/div/ul/li[3]'
            backup_email_click_script = '''
            document.querySelectorAll('form span section div div div ul li')[2].childNodes[0].click();
            '''
            ensure_click(self.driver, path, script=backup_email_click_script)
            backup_xpath = '//*[@id=\"knowledge-preregistered-email-response\"]'
            backup_email_type_script = 'return document.querySelector("input[type=\'email\']");'
            type_text(driver=self.driver, text=self.backup_email, xpath=backup_xpath, loading=True,
                      script=backup_email_type_script)
            # Check challenge after finish backup email
            self.check_challenge()
        elif 'disabled/explanation' in driver.current_url:
            self.handle_false_email(Constant.ACCOUNT_DISABLED_MESSAGE)
        elif 'speedbump/changepassword' in driver.current_url:
            self.change_password()
            if 'disabled/explanation' in driver.current_url:
                self.handle_false_email(Constant.ACCOUNT_DISABLED_MESSAGE)
        elif 'challenge/recaptcha' in driver.current_url:
            self.handle_false_email(Constant.ACCOUNT_REQUIRED_CAPTCHA_MESSAGE)
        elif 'signin/rejected' in driver.current_url:
            self.handle_false_email(Constant.ACCOUNT_REJECTED_MESSAGE)
        elif 'speedbump' in driver.current_url or \
                'challenge/sk/presend' in driver.current_url or \
                'challenge/dp' in driver.current_url or \
                'challenge/ootp' in driver.current_url or \
                'challenge/ipp' in driver.current_url or \
                'challenge/iap' in driver.current_url:
            # speedbump/idvreenable -> require phone verification
            # challenge/sk/presend -> require phone verification
            # challenge/dp -> select a number
            # ootp -> required OTP
            # ipp -> required OTP
            # iap -> require phone verification
            self.handle_false_email(Constant.ACCOUNT_VERIFICATION_MESSAGE)

    def change_password(self):
        new_pass = helper.create_random_password()
        password_path = '//*[@id="passwd"]/div[1]/div/div[1]/input'
        type_text(driver=self.driver, text=new_pass, xpath=password_path)
        confirm_pass_path = '//*[@id="confirm-passwd"]/div[1]/div/div[1]/input'
        type_text(driver=self.driver, text=new_pass, xpath=confirm_pass_path)
        self.change_email_password(new_password=new_pass)
        if self.change_password_callback is not None:
            self.change_password_callback(self.email, new_pass)

    def handle_false_email(self, text):
        # Raise error, noted the email and exit the flow
        if self.false_email_callback is not None:
            self.false_email_callback(self.email, self.password, self.backup_email, text)
        log_false_email(f"{text}: <{self.email}:{self.password}:{self.backup_email}>")
        raise ValueError(f"{text} ({self.email})")

    def change_email_password(self, new_password):
        with open(Constant.CHANGED_EMAILS_FILE, 'a') as f:
            f.write("\n" + f"<{self.email}:{self.password}:{self.backup_email}>"
                           f"{Constant.CHANGED_PASSWORD_SEPARATOR}"
                           f"<{self.email}:{new_password}:{self.backup_email}>")

    def start(self):
        self.adjust_viewport()
        self.check_login_status()
        sleep_for(Constant.SHORT_WAIT)
        self.driver.execute_cdp_cmd(cmd='Network.clearBrowserCache', cmd_args={})
