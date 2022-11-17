from login_gmail_selenium.util.profile import ChromeProfile


def login(email, password, backup_email):
    profile = ChromeProfile(email, password, backup_email)
    profile.start()


if __name__ == '__main__':
    login('terabox269@gmail.com', 'dung@123', 'ngudfwsfd@gmail.com')
