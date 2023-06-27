import os
import shutil

import undetected_chromedriver as uc2
from selenium.webdriver.chrome.service import Service

import login_gmail_selenium.common.constant as Constant
from login_gmail_selenium.util.driver import Driver
from login_gmail_selenium.util.helper import sleep_for, get_version

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
                 auth_type=AUTH_TYPES[2],
                 path=None,
                 prox=None,
                 prox_type=None,
                 insecure=False):
        self.proxy_folder = None
        self.auth_type = auth_type
        self.path = path
        self.proxy = prox or "empty"
        self.proxy_type = prox_type
        self.driver = None
        self.insecure = insecure
        self.profile_name = None
        self.cache_folders = []
        self.profile_folder = None

    def create_driver(self):
        options = uc2.ChromeOptions()
        path = os.path.join(self.profile_folder, self.profile_name)
        if Constant.DISK_SPACE or os.path.isdir(path):
            # If disk space is still available then create a new Chrome profile
            # or the Chrome profile already exist then use it
            options.add_argument(f"--user-data-dir={path}")
            if self.auth_type is AUTH_TYPES[0]:
                folder_name = self.profile_name
            elif self.auth_type is AUTH_TYPES[1]:
                folder_name = f"{self.profile_name}{PUBLIC_PROXY_POSTFIX}"
            else:
                folder_name = f"{self.profile_name}{NO_PROXY_POSTFIX}"
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

    def retrieve_driver(self):
        self.driver = self.create_driver()
        return self.driver

    def start(self):
        # self.adjust_viewport()
        sleep_for(Constant.SHORT_WAIT)
        self.driver.execute_cdp_cmd(cmd='Network.clearBrowserCache', cmd_args={})

    def adjust_viewport(self):
        pass

    def create_proxy_folder(self):
        self.proxy_folder = os.path.join(Constant.PROXY_FOLDER, f'proxy_auth_{self.profile_name}')
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

    def clear_cache(self):
        for i in self.cache_folders:
            shutil.rmtree(i)
        try:
            if self.proxy_folder:
                shutil.rmtree(self.proxy_folder, ignore_errors=True)
        except (Exception, ValueError):
            pass
