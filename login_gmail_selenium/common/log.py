import login_gmail_selenium.common.constant as Constant
from datetime import *
import sys


def log_false_email(text):
    with open(Constant.FALSE_EMAIL_FILE, 'a+') as log:
        date_time = datetime.now()
        print_unrecognized_encoding(f"{date_time}: {text}", file=log)


def print_unrecognized_encoding(*objects, sep=' ', end='\n', file=sys.stdout):
    enc = file.encoding
    if enc == 'UTF-8':
        print(*objects, sep=sep, end=end, file=file)
    else:
        f: () = lambda obj: str(obj).encode(enc, errors='replace').decode(enc)
        print(*map(f, objects), sep=sep, end=end, file=file)


def convert(s):
    str1 = ""
    return str1.join(s)