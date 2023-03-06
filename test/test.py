from login_gmail_selenium.util.profile import ChromeProfile
import time


if __name__ == '__main__':
    profile = ChromeProfile('lrod44536@gmail.com', 'Pt6o4FWy8k', 'karasalab906008@hotmail.com')
    driver = profile.retrieve_driver()
    time.sleep(10000)
    profile.start()
    driver.get('https://www.google.com/')
    time.sleep(100)
