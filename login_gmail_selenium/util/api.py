import requests
import login_gmail_selenium.common.constant as Constant


class ApiHelper:
    def __init__(self):
        pass

    @staticmethod
    def update_false_email(false_email, message):
        r = requests.put(f"{Constant.ENDPOINT}/api/mails/{false_email}"
                         f"?status=RequiredVerification&message={message}")
        return ApiHelper.handle_request(r)

    @staticmethod
    def handle_request(res):
        if res.status_code == 200:
            return res.json()['success']
        else:
            res.raise_for_status()
            return None
