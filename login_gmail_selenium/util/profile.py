import undetected_chromedriver as uc2
import os
import login_gmail_selenium.common.constant as Constant
from login_gmail_selenium.util.helper import type_text, sleep_for, ensure_click, get_version
from glob import glob
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import selenium.webdriver.support.expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from login_gmail_selenium.common.log import log_false_email

WEBRTC = os.path.join('extension', 'webrtc_control.zip')
ACTIVE = os.path.join('extension', 'always_active.zip')
FINGERPRINT = os.path.join('extension', 'fingerprint_defender.zip')
TIMEZONE = os.path.join('extension', 'spoof_timezone.zip')
CUSTOM_EXTENSIONS = glob(os.path.join('extension', '*.zip')) + \
                    glob(os.path.join('extension', '*.crx'))


class ChromeProfile:
    VIEWPORTS = ['2560,1440', '1920,1080', '1440,900',
                 '1536,864', '1366,768', '1280,1024', '1024,768']
    dirname = os.path.abspath(__file__ + "/../../")

    def __init__(self, email, password, backup_email, auth_type=None, path=None,
                 prox=None, prox_type=None, proxy_folder=None, is_disk_available=True, insecure=False):
        self.email = email
        self.password = password
        self.backup_email = backup_email
        self.proxy_folder = proxy_folder
        self.auth_type = auth_type
        self.path = path
        self.proxy = prox or "empty"
        self.proxy_type = prox_type
        self.driver = None
        self.is_disk_available = is_disk_available
        self.insecure = insecure

    def create_driver(self):
        options = uc2.ChromeOptions()
        path = os.path.join(Constant.PROFILE_FOLDER, self.email)
        if self.is_disk_available or os.path.isdir(path):
            # If disk space is still available then create a new Chrome profile
            # or the Chrome profile already exist then use it
            options.add_argument(f"--user-data-dir={path}")
            options.add_argument(f"--profile-directory={self.email}")
        options.add_argument("--start-maximized")
        if self.insecure:
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
            "profile.default_content_setting_values.geolocation": 1
        }
        options.add_experimental_option("prefs", prefs)
        options.add_extension(WEBRTC)
        options.add_extension(FINGERPRINT)
        options.add_extension(TIMEZONE)
        options.add_extension(ACTIVE)
        if CUSTOM_EXTENSIONS:
            for extension in CUSTOM_EXTENSIONS:
                options.add_extension(extension)

        # Either private proxy, public proxy or no proxy at all
        if self.auth_type == 'private':
            self.create_proxy_folder()
            options.add_argument(f"--load-extension={self.proxy_folder}")
        elif self.auth_type == 'public':
            options.add_argument(f'--proxy-server={self.proxy_type}://{self.proxy}')
        else:
            options.add_argument('--no-proxy-server')
        service = Service(executable_path=Constant.PATCHED_DRIVER)
        return uc2.Chrome(service=service, options=options, version_main=get_version())

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
        login_text_retrieve_script = 'return document.querySelector("input[type=\'email\']");'
        try:
            # First time login on device, type username
            type_text(driver=self.driver, text=self.email, xpath=username_xpath, loading=True,
                      script=login_text_retrieve_script, paste_text=100)
        except NoSuchElementException:
            # TODO: this site can't be reach
            raise
        except (Exception, ValueError):
            # Profile already has at least 1 username, choose profile with correct email
            if "signinchooser" in driver.current_url:
                desired_profile = driver.find_elements_by_xpath(f"//*[contains(text(), '{self.email}')]")
                if desired_profile:
                    desired_profile[0].click()
                else:
                    new_profile_xpath = "//*[@id=\"view_container\"]/div/div/div[2]/div/div[1]/div/form/span/" \
                                        "section/div/div/div/div/ul/li[2]"
                    driver.find_elements_by_xpath(new_profile_xpath)[0].click()
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
        self.check_challenge()

        if 'challenge/pwd' in driver.current_url:
            # Something happens to the account
            get_error_div_script = "return document.querySelectorAll('form > span > " \
                                   "div > div[aria-live]')[0].childNodes;"
            error_div = driver.execute_script(get_error_div_script)
            if error_div:
                get_error_msg_script = "return document.querySelectorAll('form > span > div > div[aria-live]')[0]." \
                                       "childNodes[1].firstChild.textContent;"
                error_msg = driver.execute_script(get_error_msg_script)
                self.handle_false_email(f"Google error: {error_msg}")
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
        elif 'disabled/explanation' in driver.current_url:
            self.handle_false_email('Account disabled')
        elif 'speedbump' in driver.current_url or \
                'challenge/sk/presend' in driver.current_url or \
                'challenge/dp' in driver.current_url:
            # speedbump/changepassword -> require changing password ???
            # speedbump/idvreenable -> require phone verification ???
            # challenge/sk/presend -> require phone verification ???
            # challenge/dp -> select a number ???
            self.handle_false_email('Account required verification steps')

    def retrieve_driver(self):
        self.driver = self.create_driver()
        return self.driver

    def start(self):
        self.check_login_status()
        sleep_for(Constant.SHORT_WAIT)

    def handle_false_email(self, text, callback=None):
        # Raise error, noted the email and exit the flow
        if callback != None:
            callback
        log_false_email(f"{text}: <{self.email}:{self.password}:{self.backup_email}>")
        raise ValueError(f"{text} ({self.email})")

    def create_proxy_folder(self):
        proxy_string = self.proxy
        proxy = proxy_string.replace('@', ':')
        proxy = proxy.split(':')
        manifest_json = """
        {
            "version": "1.0.0",
            "manifest_version": 2,
            "name": "Chrome Proxy",
            "permissions": [
                "proxy",
                "tabs",
                "unlimitedStorage",
                "storage",
                "<all_urls>",
                "webRequest",
                "webRequestBlocking"
            ],
            "background": {
                "scripts": ["background.js"]
            },
            "minimum_chrome_version":"22.0.0"
        }
         """

        background_js = """
        var config = {
                mode: "fixed_servers",
                rules: {
                singleProxy: {
                    scheme: "http",
                    host: "%s",
                    port: parseInt(%s)
                },
                bypassList: ["localhost"]
                }
            };
        chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});
        function callbackFn(details) {
            return {
                authCredentials: {
                    username: "%s",
                    password: "%s"
                }
            };
        }
        chrome.webRequest.onAuthRequired.addListener(
                    callbackFn,
                    {urls: ["<all_urls>"]},
                    ['blocking']
        );
        """ % (proxy[2], proxy[-1], proxy[0], proxy[1])

        os.makedirs(self.proxy_folder, exist_ok=True)
        with open(os.path.join(self.proxy_folder, "manifest.json"), 'w') as fh:
            fh.write(manifest_json)

        with open(os.path.join(self.proxy_folder, "background.js"), 'w') as fh:
            fh.write(background_js)
