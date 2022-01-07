from sys import stdout
from logging import getLogger, DEBUG

logger = getLogger('oxen')
logger.setLevel(DEBUG)

def log_string(_str, color=None, task=None):
    print("[Oxen-Box]",_str)
    stdout.flush()