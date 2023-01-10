import sys
import logging
import login_gmail_selenium.common.constant as Constant
from datetime import *


def log_false_email(text):
    with open(Constant.FALSE_EMAIL_FILE, 'a+') as log:
        date_time = datetime.now()
        print(f"{date_time}: {text}", file=log)
