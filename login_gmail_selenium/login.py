from util.profile import ChromeProfile

def login(email, password, backup_email):
    profile = ChromeProfile(email, password, backup_email)
    profile.start()
    profile.get_version_browser()

if __name__ == '__main__':
    login('terabox269@gmail.com', 'dung@123', 'ngudfwsfd@gmail.com')