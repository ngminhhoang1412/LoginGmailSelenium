from login_gmail_selenium.util.profile import ChromeProfile


def login(email, password, backup_email):
    profile = ChromeProfile(email, password, backup_email)
    profile.start()
