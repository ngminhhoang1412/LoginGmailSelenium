import sys
import logging
import TeraBoxUtility.common.constant as Constant

logger = logging.getLogger(__name__)


def log_error(exception, is_critical=False):
    if is_critical:
        logger.critical(exception, exc_info=True)
    else:
        logger.error(exception, exc_info=True)


def print_unrecognized_encoding(*objects, sep=' ', end='\n', file=sys.stdout):
    enc = file.encoding
    if enc == 'UTF-8':
        print(*objects, sep=sep, end=end, file=file)
    else:
        f: () = lambda obj: str(obj).encode(enc, errors='replace').decode(enc)
        print(*map(f, objects), sep=sep, end=end, file=file)


class OneLineExceptionFormatter(logging.Formatter):
    def formatException(self, exc_info):
        """
        Format an exception so that it prints on a single line.
        """
        result = super(OneLineExceptionFormatter, self).formatException(exc_info)
        return repr(result)  # or format into one line however you want to

    def format(self, record):
        # Stick the message and the traceback of exception together
        s = super(OneLineExceptionFormatter, self).format(record)
        if record.exc_text:
            s = s.replace('\n', '') + '|'
        return s


def configure_logging():
    handler = logging.FileHandler(Constant.LOG_FILE, 'a+', 'utf-8')
    # NOTE: in case you want the exception log to be 1 line
    # formatter = OneLineExceptionFormatter('%(asctime)s|%(levelname)s: %(message)s',
    #                                       '%d/%m/%Y %H:%M:%S')
    formatter = logging.Formatter('%(asctime)s|%(levelname)s: %(message)s',
                                  '%d/%m/%Y %H:%M:%S')
    handler.setFormatter(formatter)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)


def setup_logging():
    configure_logging()
