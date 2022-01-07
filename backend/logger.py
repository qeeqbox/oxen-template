from contextlib import contextmanager
from logging import getLogger, DEBUG

logger = getLogger('oxen')
logger.setLevel(DEBUG)

@contextmanager
def ignore_excpetion(*exceptions):
    try:
        yield
    except exceptions:
        #print("{} {} {}".format(datetime.utcnow(), EXCLAMATION_MARK, error))
        pass

def setup_task_logger(parsed):
    log_string("Setup task {} logger".format(parsed['task']), "Yellow")


def cancel_task_logger(parsed):
    log_string("Closing task {} logger".format(parsed['task']), "Yellow")

def log_string(_str, color=None, task=None):
    logger.info(_str)