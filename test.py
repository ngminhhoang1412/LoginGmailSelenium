from login_gmail_selenium.util.profile import ChromeProfile
import time

if __name__ == '__main__':
    profile = ChromeProfile('muhamhmadfirdeasyusoa@gmail.com', 'Pnvgjzdwfpus68', 'LaibaCardenasgbZ59698@hotmail.com')
    driver = profile.retrieve_driver()
    profile.start()
    driver.get('https://www.google.com/')
    time.sleep(100)
