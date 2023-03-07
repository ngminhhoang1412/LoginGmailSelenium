import login_gmail_selenium.util as LGS_util
import login_gmail_selenium.common as LGS_common
import time
import os

if __name__ == '__main__':
    option = 2
    if option == 1:
        # No proxy
        profile = LGS_util.profile.ChromeProfile('gmail',
                                                 'password',
                                                 'backup')
    elif option == 2:
        # For private proxy
        proxy_folder = os.path.join(LGS_common.constant.PROXY_FOLDER, f'proxy_auth')
        profile = LGS_util.profile.ChromeProfile('gmail',
                                                 'password',
                                                 'backup',
                                                 'private',
                                                 None,
                                                 'username:pass@ip:port',
                                                 'http',
                                                 proxy_folder)
    else:
        # For public proxy
        profile = None

    driver = profile.retrieve_driver()
    profile.start()
    driver.get('https://www.google.com/')
    time.sleep(100)
    driver.quit()
