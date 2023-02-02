from login_gmail_selenium.util.profile import ChromeProfile
import time
import os

if __name__ == '__main__':
    profile = ChromeProfile('rungcaengwrwuthi15@gmail.com', 'p8S9Qec1A4', 'thaddeus050756@hotmail.com')
    driver = profile.retrieve_driver()
    profile.start()
    driver.get('https://www.google.com/')
    time.sleep(100)
