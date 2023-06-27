import login_gmail_selenium.common.constant as Constant
from login_gmail_selenium.util.base_profile import ChromeProfile, AUTH_TYPES


class Profile(ChromeProfile):
    def __init__(self, profile_name, auth_type=AUTH_TYPES[2], path=None, prox=None, prox_type=None,
                 insecure=False):
        super().__init__(auth_type, path, prox, prox_type, insecure)
        self.profile_name = profile_name
        self.profile_folder = Constant.BLANK_PROFILE_FOLDER
