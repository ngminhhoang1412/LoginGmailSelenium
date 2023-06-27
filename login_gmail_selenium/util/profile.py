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

current_path = os.path.dirname(os.path.abspath(__file__))
root_path = os.path.dirname(current_path)
extension_path = os.path.join(root_path, 'extension')

WEBRTC = os.path.join(extension_path, 'webrtc_control.zip')
ACTIVE = os.path.join(extension_path, 'always_active.zip')
FINGERPRINT = os.path.join(extension_path, 'fingerprint_defender.zip')
TIMEZONE = os.path.join(extension_path, 'spoof_timezone.zip')
VEEPN = os.path.join(extension_path, 'veepn.zip')

NO_PROXY_POSTFIX = '_no_proxy'
PUBLIC_PROXY_POSTFIX = '_public_proxy'
AUTH_TYPES = [
    'private',
    'public',
    None
]


class ChromeProfile:

    VIEWPORTS = ['2560,1440', '1920,1080', '1440,900',
                 '1536,864', '1366,768', '1280,1024', '1024,768']

    def __init__(self,
                 email,
                 password,
                 backup_email,
                 auth_type=AUTH_TYPES[2],
                 path=None,
                 prox=None,
                 prox_type=None,
                 insecure=False,
                 false_email_callback=None,
                 change_password_callback=None):
        self.email = email
        self.password = password
        self.backup_email = backup_email
        self.proxy_folder = None
        self.auth_type = auth_type
        self.path = path
        self.proxy = prox or "empty"
        self.proxy_type = prox_type
        self.driver = None
        self.insecure = insecure
        self.false_email_callback = false_email_callback
        self.cache_folders = []
        self.change_password_callback = change_password_callback

    def create_driver(self):
        options = uc2.ChromeOptions()
        path = os.path.join(Constant.PROFILE_FOLDER, self.email)
        if Constant.DISK_SPACE or os.path.isdir(path):
            # If disk space is still available then create a new Chrome profile
            # or the Chrome profile already exist then use it
            options.add_argument(f"--user-data-dir={path}")
            if self.auth_type is AUTH_TYPES[0]:
                folder_name = self.email
            elif self.auth_type is AUTH_TYPES[1]:
                folder_name = f"{self.email}{PUBLIC_PROXY_POSTFIX}"
            else:
                folder_name = f"{self.email}{NO_PROXY_POSTFIX}"
            options.add_argument(f"--profile-directory={folder_name}")
            profile_path = os.path.join(path, folder_name)
            self.cache_folders.append(os.path.join(profile_path, 'optimization_guide_prediction_model_downloads'))
            self.cache_folders.append(os.path.join(profile_path, 'Cache'))
            self.cache_folders.append(os.path.join(profile_path, 'Service Worker', 'CacheStorage'))
            self.cache_folders.append(os.path.join(path, 'SwReporter'))
            self.cache_folders.append(os.path.join(path, 'pnacl'))
            self.cache_folders.append(os.path.join(path, 'OnDeviceHeadSuggestModel'))
            self.cache_folders.append(os.path.join(path, 'MediaFoundationWidevineCdm'))
            self.cache_folders.append(os.path.join(path, 'GrShaderCache'))
            self.cache_folders.append(os.path.join(path, 'ClientSidePhishing'))
            self.cache_folders.append(os.path.join(path, 'hyphen-data'))
            self.cache_folders.append(os.path.join(path, 'ZxcvbnData'))
            self.cache_folders.append(os.path.join(path, 'Safe Browsing'))
        options.add_argument("--start-maximized")
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-popup-blocking")

        if self.insecure:
            options.add_argument("--disable-web-security")
            options.add_argument("--allow-running-insecure-content")
            
        # header = Headers(
        #     browser='chrome'
        # ).generate()
        # agent = f"user-agent={header['User-Agent']}"
        # options.add_argument(agent)
        # options.add_argument('--mute-audio')
        # options.add_argument('--no-sandbox')
        # options.add_argument('--disable-dev-shm-usage')
        # options.add_argument('--disable-features=UserAgentClientHint')
        # options.add_argument('--allow-insecure-localhost')
        # options.add_argument('--disable-blink-features=AutomationControlled')
        # options.add_argument('--no-first-run --no-service-autorun --password-store=basic')

        # Note: For cache
        # --disable-features=OptimizationGuideModelDownloading,OptimizationHintsFetching,OptimizationTargetPrediction,OptimizationHints
        # https://bugs.chromium.org/p/chromium/issues/detail?id=1311753
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
        options.add_extension(VEEPN)
        # if CUSTOM_EXTENSIONS:
        #     for extension in CUSTOM_EXTENSIONS:
        #         options.add_extension(extension)

        # Either private proxy, public proxy or no proxy at all
        if self.auth_type == AUTH_TYPES[0]:
            self.create_proxy_folder()
            options.add_argument(f"--load-extension={self.proxy_folder}")
        elif self.auth_type == AUTH_TYPES[1]:
            options.add_argument(f'--proxy-server={self.proxy_type}://{self.proxy}')
        else:
            options.add_argument('--no-proxy-server')
        service = Service(executable_path=Constant.PATCHED_DRIVER)
        return Driver(service=service, options=options, version_main=get_version(), quit_callback=self.clear_cache)

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
            self.handle_false_email("Selenium failed to type username")
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

    def retrieve_driver(self):
        self.driver = self.create_driver()
        return self.driver

    def start(self):
        self.adjust_viewport()
        self.check_login_status()
        sleep_for(Constant.SHORT_WAIT)
        self.driver.execute_cdp_cmd(cmd='Network.clearBrowserCache', cmd_args={})

    def adjust_viewport(self):
        pass

    def create_proxy_folder(self):
        self.proxy_folder = os.path.join(Constant.PROXY_FOLDER, f'proxy_auth_{self.email}')
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

    def handle_false_email(self, text):
        # Raise error, noted the email and exit the flow
        if self.false_email_callback is not None:
            self.false_email_callback(self.email, self.password, self.backup_email, text)
        log_false_email(f"{text}: <{self.email}:{self.password}:{self.backup_email}>")
        raise ValueError(f"{text} ({self.email})")

    def clear_cache(self):
        for i in self.cache_folders:
            shutil.rmtree(i)
        try:
            if self.proxy_folder:
                shutil.rmtree(self.proxy_folder, ignore_errors=True)
        except (Exception, ValueError):
            pass

    def change_email_password(self, new_password):
        with open(Constant.CHANGED_EMAILS_FILE, 'a') as f:
            f.write("\n" + f"<{self.email}:{self.password}:{self.backup_email}>"
                           f"{Constant.CHANGED_PASSWORD_SEPARATOR}"
                           f"<{self.email}:{new_password}:{self.backup_email}>")
