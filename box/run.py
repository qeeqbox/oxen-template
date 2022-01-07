'''
    __G__ = "(G)bd249ce4"
    box -> run
'''

from sys import argv
from binascii import unhexlify
from pickle import loads
from logger import log_string

log_string("in")

if len(argv) == 2:
    log_string("Parsing arguments")
    parsed = loads(unhexlify(argv[1]))
    log_string("Parsed -> {}".format(parsed))
    log_string("Done!!")
